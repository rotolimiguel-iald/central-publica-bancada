"""Exhaust all55 symmetric metric fibers; retain anisotropic source in BV."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from smooth_general_fiber_engine import metric_fiber_basis,mixed_tensor,general_source,general_hessian,general_current
from smooth_mixed_gradient_engine import gradient_tensor
from smooth_variable_ward_engine import gauge,einstein,green_current_E
from position_metric_bubble_engine import LABELS
H=Path(__file__).resolve().parent;D=H/'smooth_general_fiber';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(raw);assert q.read_bytes()==raw;q.replace(p)
inputs=[Path(__file__),H/'smooth_general_fiber_engine.py',H/'smooth_variable_ward_engine.py',
 H/'smooth_mixed_gradient_engine.py',H/'smooth_source_rotation/results.json',
 H/'smooth_firstjet_source/results.json',H/'smooth_variable_bv/DERIVACAO.md']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='General real symmetric coincident metric reference fiber:55-dimensional exact contraction and BV primitive',
 method='Full basis, joint fiber/derivative transpose; linear reconstruction of I/T; anisotropic polynomial controls',
 exclusions=['physical state positivity','BRST-compatible full propagator pair','full Q2','curvature'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=0
def ck(n,v):
    global checks
    assert s.expand(v)==0,(n,s.expand(v));checks+=1
tables=[]
for left in range(10):
 for right in range(left,10):
    fiber=metric_fiber_basis(left,right);T=mixed_tensor(fiber)
    for a,b,i,j in product(range(10),range(10),range(4),range(4)):
        ck(('transpose',left,right,a,b,i,j),s.Rational(T.get((a,b,i,j),0)-T.get((b,a,j,i),0)))
    tables.append(dict(left=left,right=right,tensor=[dict(a=a,b=b,i=i,j=j,value=str(v))
        for (a,b,i,j),v in sorted(T.items())]))
 print('FIBER',left,'tables',len(tables),'cpu',time.process_time()-cpu,flush=True)

# Linearity identifies the old isotropic sectors in the general basis.
for sector in ['metric_I','metric_T']:
    combined={}
    for entry in tables:
        l,r=entry['left'],entry['right'];a,b=LABELS[l];c,d=LABELS[r]
        weight=F(int(a==c and b==d)+int(a==d and b==c),2) if sector=='metric_I' else F(int(a==b and c==d))
        if not weight:continue
        for row in entry['tensor']:
            key=tuple(row[k] for k in ['a','b','i','j'])
            combined[key]=combined.get(key,F())+weight*F(row['value'])
    old=gradient_tensor(sector)
    for key in set(combined)|set(old):ck(('linearity',sector,key),s.Rational(combined.get(key,0)-old.get(key,0)))

# Ghost contact vanishes on all16 coincident fibers by oriented slot structure.
for a in range(4):
 for b in range(4):
    f=tuple(F(int(i==a and j==b)) for i in range(4) for j in range(4))
    assert not mixed_tensor(f,False),(a,b)
    checks+=1

# Written general proof below uses transpose; these are independent dense controls.
x=s.symbols('x0:4');h=s.Matrix(4,4,lambda a,b:(a+b+1)*x[(a+b)%4]**2+x[a]*x[b])
c=s.Matrix([x[(i+1)%4]**3+(i+1)*x[i]*x[(i+2)%4] for i in range(4)])
w=1+x[0]**3+x[1]*x[2]+x[3]
def inner(a,b):return s.trace(a*b)
def div(j):return sum(s.diff(j[i],x[i]) for i in range(4))
selected=[(0,0),(0,4),(1,8)]
for left,right in selected:
 f=metric_fiber_basis(left,right);g=gauge(c,x);r=general_source(f,c,w,x)
 nh=general_hessian(f,h,w,x);ng=general_hessian(f,g,w,x)
 er=einstein(r,x);eh=einstein(h,x)
 jn=general_current(f,h,g,w,x);je=green_current_E(h,r,x)
 ck(('greenN',left,right),div(jn)-inner(h,ng)+inner(nh,g))
 variation=-(inner(g,nh)+inner(h,ng))/2-inner(eh,r)
 ck(('BV',left,right),variation+inner(h,ng+er)-div([jn[i]/2+je[i] for i in range(4)]))

# Rotation has Gc=0; do not replace the general R by L G.
f=metric_fiber_basis(0,0);cr=s.Matrix([-x[1],x[0],0,0]);wr=x[0]**2-x[2]**2
assert gauge(cr,x)==s.zeros(4)
rr=general_source(f,cr,wr,x);er=einstein(rr,x)
assert rr!=s.zeros(4)
result=dict(at=datetime.now(timezone.utc).isoformat(),
 status='GENERAL_SMOOTH_FIBER_MIXED_CONTACT_AND_BV_PRIMITIVE',checks=checks,cpu_seconds=time.process_time()-cpu,
 dimension=55,source_general_previous_checks=8800,firstjet_previous_checks=6645,
 generality='By linearity55 arbitrary smooth diagonal coefficient functions; general independent first-Y jets enter the already verified R formula',
 anisotropic_control=dict(fiber='W_00|00=wr(center)',w=str(wr),c=list(map(str,cr)),
     Gc_zero=True,Rc=list(map(str,rr)),E_Rc=list(map(str,er))),
 proof='Every basis tensor has joint transpose; N_W selfadjoint, so B=-CE integral(1/2 hN_Wh+hdagger R_Wc) gives s0B=-CE integral h(N_WG+ER_W)c modulo explicit currents',
 full_Q2=False,reference_selected=False)
put('tensor_basis.json',tables);put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'tensor_basis.json',D/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
