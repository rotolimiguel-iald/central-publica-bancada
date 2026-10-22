"""Identify the homogeneous parameter of the local quadratic primitive."""
from pathlib import Path
from time import process_time
from datetime import datetime,timezone
import hashlib,json
from fractions import Fraction as F
from oneform_second_curvature_engine_v2 import einstein_gauge
from radial_covariant_second_jet_engine import radial_second_jets
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'local_ward_family_einstein';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    claim='d(deltaH_t)/dt = -K E/2 through K²; explains unchosen homogeneous Ward freedom',full_Q2=False))
cpu=process_time();checks=0
for p in [(1,0,0,0),(1,2,-1,1)]:
    p2=sum(v*v for v in p)
    for flatA in BASIS:
        A=[flatA[4*i:4*i+4] for i in range(4)];tr=sum(A[i][i] for i in range(4))
        pa=[sum(A[i][j]*p[j] for j in range(4)) for i in range(4)];pap=sum(p[i]*pa[i] for i in range(4))
        value,_=radial_second_jets(A,p)
        for a in range(4):
            for b in range(4):
                flat=(-F(1,2)*p2*A[a][b]+F(1,2)*int(a==b)*p2*tr
                    -F(1,2)*(p[a]*p[b]*tr+int(a==b)*pap)+(p[a]*pa[b]+p[b]*pa[a])/2)
                curved=A[a][b]-int(a==b)*tr
                for o,target in [(0,flat),(1,curved)]:
                    actual=-einstein_gauge(value,(),a,b,o)/2
                    assert actual==target,(p,a,b,o,actual,target);checks+=1
fresh(D/'results.json',dict(statute='DERIVED_HOMOGENEOUS_FAMILY_IS_EINSTEIN_HESSIAN',checks=checks,
    identity='partial_t deltaH_t = -K E/2',consequence='E G=0 leaves this parameter undetermined by the measured Ward component',
    excludes='Not a classification of the other31 fit directions; no nonlinear BV/cohomology classification',cpu_seconds=process_time()-cpu))
files=[Path(__file__),D/'PRE_REGISTER.json',D/'results.json',H/'oneform_second_curvature_engine_v2.py',H/'radial_covariant_second_jet_engine.py']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,cpu=process_time()-cpu)))
