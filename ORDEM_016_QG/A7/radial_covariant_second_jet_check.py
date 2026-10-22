"""Exact parallel-transport and lower-order checks of second-curvature jets."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
from itertools import product,combinations_with_replacement
import hashlib,json
from radial_covariant_second_jet_engine import *
from radial_covariant_jet_engine import radial_jets
H=Path(__file__).resolve().parent;D=H/'radial_covariant_second_jet';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),engine_sha256=sha(H/'radial_covariant_second_jet_engine.py'),
    target='K0/K1 vs prior jets, K2 symmetric Taylor zero, metric parallel, curvature commutator',full_Q2=False))
cpu=process_time();checks=0;nonzero=0
def check(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1
g=[[int(a==b) for b in range(4)] for a in range(4)]
As=[g,[[int(a==0 and b==0) for b in range(4)] for a in range(4)],
    [[int((a,b) in [(0,1),(1,0)]) for b in range(4)] for a in range(4)]]
for index,A in enumerate(As):
    value,sym=radial_second_jets(A,(1,2,-1,1));old,_,_=radial_jets(A,(1,2,-1,1))
    for w in [()]+list(product(range(4),repeat=2))+list(product(range(4),repeat=4)):
        for a in range(4):
            for b in range(a,4):
                for o in (0,1):check(value(w,a,b,o),old(w,a,b,o))
    for w in combinations_with_replacement(range(4),4):
        for a in range(4):
            for b in range(a,4):check(sym(w,a,b,2))
    if index==0:
        zero,_=radial_second_jets(A)
        for w in product(range(4),repeat=4):
            for a in range(4):
                for b in range(a,4):check(zero(w,a,b,2))
    else:
        nonzero+=sum(value(w,a,b,2)!=0 for w in product(range(4),repeat=4) for a in range(4) for b in range(a,4))
    # [nabla_i,nabla_j] h_ab = -R^c_aij h_cb -R^c_bij h_ac.
    for i,j,a,b in product(range(4),repeat=4):
        expected=-sum((int(c==i)*int(a==j)-int(c==j)*int(a==i))*A[c][b]
                      +(int(c==i)*int(b==j)-int(c==j)*int(b==i))*A[a][c] for c in range(4))
        check(value((i,j),a,b,1)-value((j,i),a,b,1),expected)
    print(json.dumps(dict(case=index,checks=checks,cpu=process_time()-cpu)),flush=True)
check(nonzero>0,True)
fresh(D/'results.json',dict(statute='DERIVED_RADIAL_COVARIANT_SECOND_JETS',checks=checks,nonzero_K2_words=nonzero,
    cpu_seconds=process_time()-cpu,full_Q2=False,scope='Word length<=4; constant curvature; radial frame coframe and Christoffel expansion'))
files=[Path(__file__),H/'radial_covariant_second_jet_engine.py',H/'spaceform_covariant_jet_engine.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,nonzero=nonzero,cpu=process_time()-cpu)))
