"""Independent position-space control of mixed potential/derivative bubbles."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from math import factorial
from functools import lru_cache
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from position_metric_bubble_engine import *
from metric_curvature_vertices import eh_cubic_potential_16k_over_K
H=Path(__file__).resolve().parent;D=H/'position_metric_potential';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'position_metric_bubble_engine.py',H/'metric_curvature_vertices.py',H/'metric_curvature_vertices/results.json']],
    target='Reproduce the Kp2 mixed potential/derivative bubble by position Wick contraction; both vertex placements',
    angular_bound='At most two internal derivatives and matching Taylor degree: angular<=4',
    normalization='raw metric bubble/A0, no effective Hessian -1/2',full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
@lru_cache(None)
def W0(A):
    W=empty()
    for a,E in enumerate(BASIS):
        for b,B in enumerate(BASIS):
            v=eh_cubic_potential_16k_over_K(A,E,B)
            if v:W[a][b]=v
    return W
def node(A,B,p,x):
    z=sum(t*t for t in x);px=sum(a*b for a,b in zip(p,x));G,_,_,d0,_=green_integer(x)
    a2,a1,_=vertex_data(A);b2,b1,_=vertex_data(B)
    X={0:W0(A),1:lincomb(*[(-p[i],a1[i]) for i in range(4)]),2:a2}
    Y={0:W0(B),1:lincomb(*[(p[i],b1[i]) for i in range(4)]),2:b2}
    out=F()
    for nx,ny in [(0,1),(0,2),(1,0),(2,0)]:
        n=nx+ny
        out+=F((-1)**n*px**n*frob(sandwich(G,X[nx]),Y[ny]),factorial(n)*d0*d0)
    return out*z*z/16
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
coeff=list(map(F,['-32','20','-34','80']))
values=[]
for a in range(10):
    for b in range(a,10):
        A,B=BASIS[a],BASIS[b];p=(1,0,0,0)
        am=s.Matrix(4,4,A);bm=s.Matrix(4,4,B);pv=s.Matrix(p)
        iv=[s.trace(am*bm),s.trace(am)*s.trace(bm),am[0,0]*s.trace(bm)+bm[0,0]*s.trace(am),(am*bm)[0,0]]
        expected=sum(c*F(v) for c,v in zip(coeff,iv))
        actual=sum((F(n['weight'])*node(A,B,p,tuple(n['vector'])) for n in nodes),F())
        check(f'potential_pair_{a}_{b}',actual,expected)
        values.append(dict(a=a,b=b,actual=str(actual),expected=str(expected)))
    print(json.dumps(dict(row=a,cpu_seconds=process_time()-cpu)),flush=True)
fresh(D/'results.json',dict(statute='REAL_POSITION_VS_MOMENTUM_MIXED_POTENTIAL_METRIC_LOG',checks=len(checks),values=values,coefficients=list(map(str,coeff)),cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu_seconds=process_time()-cpu)))
