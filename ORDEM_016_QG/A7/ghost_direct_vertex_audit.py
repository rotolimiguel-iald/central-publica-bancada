"""Independent polynomial vertex and endpoint reciprocity controls."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
import marked_polynomial_engine as p
from ghost_direct_position_engine import *
H=Path(__file__).resolve().parent;D=H/'ghost_direct_vertex_audit';D.mkdir(exist_ok=True)
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def fresh(f,v):
    b=json.dumps(v,indent=2).encode();assert not f.exists()
    t=f.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(f)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    target='Compare integrated-by-parts vertex with existing nonminimal polynomial Q1; Green reciprocity and directed transpose control'))
cpu=process_time();checks=0;asymmetric=0
def check(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1
k,l=p.P,p.Q;out=p.add(k,l)
for A in BASIS:
    am=[[p.R(A[4*i+j]) for j in range(4)] for i in range(4)]
    ref=p.ghost_matrix(am,k,l);W2,W1=vertex(A)
    for nu in range(4):
        for rho in range(4):
            direct=p.ZERO
            for mu in range(4):
                for lam in range(4):
                    v=W2[4*(lam+1)+rho].get(4*(mu+1)+nu,0)
                    direct+=p.QQ(v)*l[lam]*out[mu]
                for j in range(4):
                    v=W1[j][rho].get(4*(mu+1)+nu,0)
                    direct+=p.QQ(v)*k[j]*out[mu]
            check(direct,ref[nu][rho])
    asymmetric+=sum(W2[i].get(j,0)!=W2[j].get(i,0) for i in range(20) for j in range(20))
point=(1,2,-1,1);forward=green(point);reverse=green(tuple(-v for v in point))
for m in range(3):
    for i in range(20):
        for j in range(20):check(forward[m][i].get(j,0),reverse[m][j].get(i,0))
check(asymmetric>0,True)
fresh(D/'results.json',dict(statute='REAL_DIRECT_GHOST_VERTEX_AND_RECIPROCITY',checks=checks,
    asymmetric_vertex_entries=asymmetric,cpu_seconds=process_time()-cpu,full_Q2=False))
files=[Path(__file__),H/'ghost_direct_position_engine.py',H/'marked_polynomial_engine.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(f),sha256=sha(f)) for f in files]))
print(json.dumps(dict(checks=checks,asymmetric=asymmetric,cpu=process_time()-cpu)))
