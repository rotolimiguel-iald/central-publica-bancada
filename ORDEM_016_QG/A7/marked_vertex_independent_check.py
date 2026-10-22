"""Independent Wick signs, nonaxis checks and falsifying controls for marked BV."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_vertex_engine import (marked,ghost_triangle,gauge,lie,bracket,R0,simplex_log,AXES)
HERE=Path(__file__).resolve().parent;DEST=HERE/'marked_vertex_independent';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_vertex_engine.py'),
    extra_cases='Nonaxis dense; nonorthogonal integer pair; collinear; zero first momentum',
    controls='Discard either insertion, flip triangle, wrong metric factor or Grassmann sign',
    independent='Exterior permutations and Gaussian Wick recursion; simplex integration',
    scope='Exact examples of principal h*cc identity, not all tensor components or finite Q2'))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,e):
    assert s.expand(e)==0,(name,e);checks.append(name)
def reject(name,e):
    assert s.expand(e)!=0,(name,e);neg.append(name)

# All names below denote odd variables. Pull external variables to the left;
# Wick contract remaining variables, with <eta_a bar_b>=G_ab, reverse=-G_ab.
def externalize(word,external):
    target=list(external)+[x for x in word if x not in external]
    assert len(set(word))==len(word)
    indices=[target.index(x) for x in word]
    swaps=sum(indices[i]>indices[j] for i in range(len(indices)) for j in range(i+1,len(indices)))
    return (-1)**swaps,[x for x in target if x not in external]
def wick(word,prop):
    if not word:return s.S.One
    return sum((-1)**(j-1)*prop.get((word[0],word[j]),0)*wick(word[1:j]+word[j+1:],prop)
               for j in range(1,len(word)))
def covariance(pairs):
    d={}
    for a,b,value in pairs:d[(a,b)]=value;d[(b,a)]=-value
    return d
g,h=s.symbols('g h')
sign,word=externalize(['T','a','bbar','v'],['T','v'])
check('mixed_bubble_Wick_sign',sign*wick(word,covariance([('a','bbar',g)]))-g)
# In the effective action -log Z the connected two-vertex term is negative.
check('effective_bubble_after_Q_inverse_minus',-(-1)-1)
sign,word=externalize(['T','a','bbar','v','dbar','e'],['T','v'])
check('ghost_line_insertion_Wick_sign',sign*wick(word,covariance([('a','dbar',g),('e','bbar',h)]))-g*h)
sign,word=externalize(['a','b','dbar','v','ebar','w'],['v','w'])
check('cstar_triangle_direct_pairing',sign*wick(word,covariance([('a','dbar',g),('b','ebar',h)]))-g*h)
check('cstar_triangle_cross_pairing',sign*wick(word,covariance([('a','ebar',g),('b','dbar',h)]))+g*h)
reject('ignoring_external_odd_permutation',wick(word,covariance([('a','dbar',g),('b','ebar',h)]))-g*h)

T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
v=s.Matrix([2,0,1,-1]);w=s.Matrix([-1,2,0,1])
cases=[]
for index,(p,r) in enumerate([(s.Matrix([1,2,-1,1]),s.Matrix([-1,0,1,2])),
                              (s.Matrix([2,0,0,0]),s.Matrix([1,3,0,0])),
                              (s.Matrix([1,0,0,0]),s.Matrix([2,0,0,0])),
                              (s.zeros(4,1),s.Matrix([1,-1,2,0]))]):
    a,ag,am,an,amn=marked(T,gauge(r,w),r,p,v)
    b,bg,bm,bn,bmn=marked(T,gauge(p,v),p,r,w)
    tri=ghost_triangle(2*T*(p+r),v,w,p,r)
    free=s.trace(T*(R0(p+r,bracket(p,v,r,w))-lie(R0(r,w),r,p,v)+lie(R0(p,v),p,r,w)))
    check(f'BV_principal_nonaxis_{index}',tri+free-a+b)
    # Check one whole nonaxis pair with the independent integration method.
    if index==0:
        check('nonaxis_simplex_ghost',ag-simplex_log(an,-p,-p-r))
        check('nonaxis_simplex_metric',am-simplex_log(amn,-r,-p-r))
        reject('omit_metric_insertion',tri+free-ag+bg)
        reject('omit_ghost_insertion',tri+free+am/4-bm/4)
        reject('flip_cstar_triangle_sign',-tri+free-a+b)
        reject('metric_weight_wrong_by_factor_two',tri+free-ag+am/2+bg-bm/2)
    case=dict(index=index,p=list(map(str,p)),r=list(map(str,r)),left=str(a),right=str(b),
              left_ghost=str(ag),left_metric=str(am),right_ghost=str(bg),right_metric=str(bm),
              triangle=str(tri),free=str(free),residual=str(s.expand(tri+free-a+b)))
    cases.append(case);print(json.dumps(case),flush=True)
result=dict(statute='REAL_NONAXIS_PRINCIPAL_MARKED_BV_CHECKS',checks_passed=len(checks),
    checks=checks,negative_controls=neg,cases=cases,wall_seconds=perf_counter()-start,
    cpu_seconds=process_time()-cpu,source_sha256=sha(Path(__file__)),
    plan_sha256=sha(DEST/'PRE_REGISTER.json'),arbitrary_tensor_identity_proven=False,full_Q2=False,gate_changed=False)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ('cases','checks')}),flush=True)
