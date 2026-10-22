"""Compare action-derived quadratic Hessian with the free operator used in loops."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from time import process_time
from functools import lru_cache
import hashlib,json
from metric_principal_vertices import basis,eh_quadratic_8k,inner,trace
from radial_covariant_jet_engine import radial_jets
H=Path(__file__).resolve().parent;D=H/'metric_action_hessian_calibration';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),
    target='Quadratic Gamma-Gamma plus potential versus free Einstein Hessian on curved background',
    source_sha256=sha(H/'metric_principal_vertices.py'),full_Q2=False))
cpu=process_time();checks=[];differences=[]
labels=[(i,j) for i in range(4) for j in range(i,4)];basis10=[basis(*l) for l in labels]
axes=[tuple(int(i==j) for i in range(4)) for j in range(4)]
@lru_cache(None)
def qcoef(b,i,e,j):return F(eh_quadratic_8k(basis10[b],axes[i],basis10[e],axes[j]),2)
for p in [(0,0,0,0),(1,2,-1,1)]:
    for a,A in enumerate(basis10):
        am=[A[4*i:4*i+4] for i in range(4)];j,_,_=radial_jets(am,p)
        for order in (0,1):
            em=[[F() for _ in range(4)] for _ in range(4)]
            for u in range(4):
                for v in range(4):
                    e=-sum(j((i,i),u,v,order) for i in range(4))
                    if u==v:e+=sum(j((i,i),m,m,order) for i in range(4) for m in range(4))/2
                    e+=sum(j((u,m),m,v,order)+j((v,m),m,u,order) for m in range(4))
                    e-=sum(j((u,v),m,m,order)+j((v,u),m,m,order) for m in range(4))/2
                    if u==v:
                        e-=sum(j((l,m),m,l,order) for l in range(4) for m in range(4))
                        e+=sum(j((l,l),m,m,order) for l in range(4) for m in range(4))/2
                    if order:
                        e+=2*am[u][v]
                        if u==v:e+=trace(A)
                    em[u][v]=e
            for b,B in enumerate(basis10):
                actual=sum(qcoef(b,i,e,k)*j((i,k),u,v,order)
                    for e,(u,v) in enumerate(labels) for i in range(4) for k in range(4))
                if order:actual-=6*(F(inner(A,B))-F(trace(A)*trace(B),2))
                expected=sum(B[4*u+v]*em[u][v] for u in range(4) for v in range(4))
                if actual!=expected:differences.append(dict(p=p,a=a,b=b,order=order,actual=str(actual),expected=str(expected),difference=str(actual-expected)))
                else:checks.append([p,a,b,order])
fresh(D/'results.json',dict(statute='REAL_ACTION_VS_FREE_HESSIAN_COMPARISON',matching=len(checks),differences=differences,cpu_seconds=process_time()-cpu,full_Q2=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(matching=len(checks),differences=len(differences),sample=differences[:8],cpu=process_time()-cpu)))
