"""Audit sparse Wick algebra and measure the first-curvature radial profile.

This is NOT an integrated covariant Hessian or the full causal Ward anomaly.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from position_metric_bubble_engine import *
H=Path(__file__).resolve().parent;D=H/'position_metric_curvature_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    supersedes_sha256='8758a48f8d26abd60f7e9806b1bbae96ea7dd6464089ac0c1823acd8fd099f6a',
    correction='Radial profile is ordered in endpoints; allow distinct pAp trB and pBp trA. No symmetrization assumed.',
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'position_metric_bubble_engine.py',H/'metric_bubble_v2/results.json',H/'angular_cubature/results.json']],
    target='Full100 ordered fiber pairs: planar crosscheck and firstK radial profile, retain logarithmic terms',
    angular_bound='N<=4 internal derivatives; flat Taylor degree N => degree<=2N<=8; firstK correction lowers Taylor by2, hence<=6, including external coframe and spin connection',
    exclusions=['K2','potential vertex','finite extension','integrated covariant Hessian','full causal Q2'],
    no_new_model_calls=True))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
def leg(E,q):
    ev=[E[4*i+j] for i,j in LABELS]
    return ev+[q[i]*v for i in range(4) for v in ev]
def quadratic(A,u,v):return sum(u[i]*a*v[j] for i,row in enumerate(A) for j,a in row.items())
for a,A in enumerate(BASIS):
    W2,W1,_=vertex_data(A)
    for t in range(4):
        E=BASIS[(3*a+t)%10];B=BASIS[(a+2*t+1)%10]
        p=tuple((i+t)%3-1 for i in range(4));q=tuple((2*i+t)%5-2 for i in range(4));r=tuple((i+2*t)%4-2 for i in range(4))
        W=lincomb((1,W2),*[(p[i],W1[i]) for i in range(4)])
        check(f'vertex_decomposition_{a}_{t}',quadratic(W,leg(E,q),leg(B,r)),eh_cubic_16k(A,p,E,q,B,r))
# Four-index contraction independently, including asymmetric Green matrix.
G,_,_,_,_=green_integer((1,2,-1,0))
for a,b in [(0,4),(1,6),(4,7)]:
    A=vertex_data(BASIS[a])[0];B=vertex_data(BASIS[b])[1][0]
    explicit=sum(v*w*G[i].get(k,0)*G[j].get(l,0)
        for i,row in enumerate(A) for j,v in row.items()
        for k,row2 in enumerate(B) for l,w in row2.items())
    check(f'four_index_{a}_{b}',frob(sandwich(G,A),B),explicit)
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
flat_coeff=list(map(F,json.loads((H/'metric_bubble_v2/results.json').read_bytes())['metric_coefficients_over_A0']))
def invariants(A,B,p):
    am=s.Matrix(4,4,A);bm=s.Matrix(4,4,B);pv=s.Matrix(p);p2=(pv.T*pv)[0]
    pa=(pv.T*am*pv)[0];pb=(pv.T*bm*pv)[0];ab=(pv.T*am*bm*pv)[0]
    basic=[s.trace(am*bm),s.trace(am)*s.trace(bm),pa*s.trace(bm)+pb*s.trace(am),ab]
    return list(map(F,[p2*p2*basic[0],p2*p2*basic[1],p2*basic[2],p2*ab,pa*pb])),list(map(F,[p2*basic[0],p2*basic[1],pa*s.trace(bm),pb*s.trace(am),ab]))
def mean(A,B,p):
    total=[F(),F(),F()]
    for node in nodes:
        values=contracted_node(A,B,p,tuple(node['vector']))
        for i in range(3):total[i]+=F(node['weight'])*values[i]
    return total
p=(1,0,0,0);values=[]
for a in range(10):
    for b in range(10):
        A,B=BASIS[a],BASIS[b];flat,curve,log=mean(A,B,p)
        iv,ic=invariants(A,B,p)
        check(f'flat55_{a}_{b}',flat,sum(c*v for c,v in zip(flat_coeff,iv)))
        values.append(dict(a=a,b=b,flat=str(flat),curve=str(curve),log=str(log),basis5=list(map(str,ic))))
    print(json.dumps(dict(completed_row=a,cpu=process_time()-cpu)),flush=True)
fresh(D/'raw_values.json',dict(checks=len(checks),values=values,cpu_seconds=process_time()-cpu))
M=s.Matrix([v['basis5'] for v in values]);c=s.Matrix([v['curve'] for v in values]);l=s.Matrix([v['log'] for v in values])
fit,params=M.gauss_jordan_solve(c);fitl,paramsl=M.gauss_jordan_solve(l)
check('unique_five_invariant_fit',len(params),0);check('unique_log_fit',len(paramsl),0)
for a,b in [(1,3),(4,7),(5,5)]:
    A,B=BASIS[a],BASIS[b];p2=(1,2,-1,1)
    f,c,l=mean(A,B,p2);iv,ic=invariants(A,B,p2)
    check(f'nonaxis_flat_{a}_{b}',f,sum(k*v for k,v in zip(flat_coeff,iv)))
    check(f'nonaxis_curve_{a}_{b}',c,sum(F(k)*v for k,v in zip(fit,ic)))
    check(f'nonaxis_log_{a}_{b}',l,sum(F(k)*v for k,v in zip(fitl,ic)))
    first=contracted_node(A,B,p2,(1,2,1,-1));scaled=contracted_node(A,B,p2,(2,4,2,-2))
    check(f'radial_homogeneity_{a}_{b}',first,scaled)
fresh(D/'results.json',dict(statute='REAL_RADIAL_PROFILE_ONLY_NOT_COVARIANT_HESSIAN',
    checks=len(checks),check_names=checks,values=values,
    curvature_coefficients=list(map(str,fit)),log_coefficients=list(map(str,fitl)),
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False,gate_changed=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'position_metric_bubble_engine.py',D/'PRE_REGISTER.json',D/'raw_values.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),curve=list(map(str,fit)),log=list(map(str,fitl)),cpu_seconds=process_time()-cpu)))
