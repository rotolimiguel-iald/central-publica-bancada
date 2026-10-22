"""Second-curvature integrated operator, with explicitly ordered Taylor jets."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
from position_metric_ordered_operator_engine import *
from ghost_covariant_word_engine import hessian_terms
H=Path(__file__).resolve().parent;D=H/'position_metric_ordered_second';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),engine_sha256=sha(H/'position_metric_ordered_operator_engine.py'),
    target='Two invariant coefficients from independent pairs; two held-out fiber controls; direct covariant ghost operator; add tadpole',
    pairs=[[1,1],[0,4],[0,0],[4,0]],full_Q2=False))
cpu=process_time();nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes'];values=[];checks=0
def check(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1
for a,b in [(1,1),(0,4),(0,0),(4,0)]:
    total=[F() for _ in range(4)]
    for ni,node in enumerate(nodes):
        v=ordered_node(BASIS[a],BASIS[b],(0,0,0,0),tuple(node['vector']),2)
        for i in range(4):total[i]+=F(node['weight'])*v[i]
        if ni%32==0:print(json.dumps(dict(pair=[a,b],node=ni,cpu=process_time()-cpu)),flush=True)
    new=sum(total[:3]);check(total[3])
    values.append(dict(pair=[a,b],pieces=list(map(str,total)),value=str(new)))
    print(json.dumps(values[-1]),flush=True)
coeff=[F(values[0]['value'])/2,F(values[1]['value'])]
check(F(values[2]['value']),sum(coeff));check(F(values[3]['value']),coeff[1])
# hessian_terms was independently derived from the ghost heat density.
op=hessian_terms();ghost=[]
for a,b in [(1,1),(0,4),(0,0),(4,0)]:
    A=[BASIS[a][4*i:4*i+4] for i in range(4)];B=[BASIS[b][4*i:4*i+4] for i in range(4)]
    val,_=radial_second_jets(A)
    v=sum((c*B[i][j]*val(w,u,v,2-ko) for (ko,i,j,u,v,w),c in op.items() if ko<=2 and B[i][j]),F())
    ghost.append(v)
gcoeff=[ghost[0]/2,ghost[1]];check(ghost[2],sum(gcoeff));check(ghost[3],gcoeff[1])
metric=[-coeff[0]/2+12,-coeff[1]/2];total=[a+b for a,b in zip(metric,gcoeff)]
fresh(D/'results.json',dict(statute='DERIVED_SECOND_K_LOG_HESSIAN_COVARIANT_ORDER',checks=checks,values=values,
    basis=['trAB','trA trB'],raw_metric=list(map(str,coeff)),metric_with_tadpole=list(map(str,metric)),ghost=list(map(str,gcoeff)),total=list(map(str,total)),
    cpu_seconds=process_time()-cpu,full_Q2=False,scope='Constant-curvature logarithmic local symbol, radial-frame constant external fields; no finite/smooth/cutoff assertion'))
files=[Path(__file__),H/'position_metric_ordered_operator_engine.py',H/'radial_covariant_second_jet_engine.py',H/'ghost_covariant_word_engine.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,raw_metric=list(map(str,coeff)),ghost=list(map(str,gcoeff)),total=list(map(str,total)),cpu=process_time()-cpu)))
