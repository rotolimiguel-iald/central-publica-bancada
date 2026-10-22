"""Classical E K_gauge=0 calibration of odd radial jets used in loop probe."""
from pathlib import Path
from fractions import Fraction as F
from time import process_time
import hashlib,json
from oneform_radial_jet_engine import oneform
H=Path(__file__).resolve().parent;D=H/'oneform_classical_ward';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'oneform_radial_jet_engine.py'),claim='Classical Einstein Hessian annihilates gauge variation through firstK'))
cpu=process_time();checks=[]
for p in [(1,0,0,0),(1,2,-1,1)]:
    for v in [tuple(int(i==j) for i in range(4)) for j in range(4)]:
        jet,_=oneform(v,p)
        def h(w,a,b,o):return jet(w+(a,),b,o)+jet(w+(b,),a,o)
        for o in (0,1):
            for a in range(4):
                for b in range(4):
                    E=-sum(h((i,i),a,b,o) for i in range(4))
                    if a==b:E+=sum(h((i,i),m,m,o) for i in range(4) for m in range(4))/2
                    E+=sum(h((a,m),m,b,o)+h((b,m),m,a,o) for m in range(4))
                    E-=sum(h((a,b),m,m,o)+h((b,a),m,m,o) for m in range(4))/2
                    if a==b:
                        E-=sum(h((l,m),m,l,o) for l in range(4) for m in range(4))
                        E+=sum(h((l,l),m,m,o) for l in range(4) for m in range(4))/2
                    if o:
                        E+=2*h((),a,b,0)
                        if a==b:E+=sum(h((),m,m,0) for m in range(4))
                    assert E==0,(p,v,o,a,b,str(E));checks.append([p,v,o,a,b])
fresh(D/'results.json',dict(statute='REAL_CLASSICAL_WARD_CALIBRATION',checks=len(checks),cpu_seconds=process_time()-cpu))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'oneform_radial_jet_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu=process_time()-cpu)))
