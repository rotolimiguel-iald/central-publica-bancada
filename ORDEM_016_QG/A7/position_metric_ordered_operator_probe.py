"""Compare independent ordered Taylor/IBP construction against first-K table."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
from position_metric_ordered_operator_engine import *
H=Path(__file__).resolve().parent;D=H/'position_metric_ordered_operator_probe';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),engine_sha256=sha(H/'position_metric_ordered_operator_engine.py'),
    target='Direct ordered Taylor plus IBP, no imposed Ward or symmetry; compare previous firstK raw bubble',pairs=[[1,1],[0,4]],full_Q2=False))
cpu=process_time();nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
ref=list(map(F,json.loads((H/'first_curvature_total_hessian/results.json').read_bytes())['metric_raw_bubble']))
p=(1,0,0,0);values=[]
for a,b in [(1,1),(0,4)]:
    total=[F() for _ in range(4)]
    for ni,node in enumerate(nodes):
        v=ordered_node(BASIS[a],BASIS[b],p,tuple(node['vector']),1)
        for i in range(4):total[i]+=F(node['weight'])*v[i]
        if ni%32==0:print(json.dumps(dict(pair=[a,b],node=ni,cpu=process_time()-cpu)),flush=True)
    A=s.Matrix(4,4,BASIS[a]);B=s.Matrix(4,4,BASIS[b]);q=s.Matrix(p)
    inv=[s.trace(A*B),s.trace(A)*s.trace(B),(q.T*A*q)[0]*s.trace(B),(q.T*B*q)[0]*s.trace(A),(q.T*A*B*q)[0]]
    old=sum(c*F(v) for c,v in zip(ref,inv));new=sum(total[:3])
    values.append(dict(pair=[a,b],pieces=list(map(str,total)),old=str(old),new=str(new),difference=str(new-old)))
    print(json.dumps(values[-1]),flush=True)
fresh(D/'results.json',dict(statute='MEASURE_ORDERED_OPERATOR_COMPARISON',values=values,cpu_seconds=process_time()-cpu,full_Q2=False))
files=[Path(__file__),H/'position_metric_ordered_operator_engine.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(values=values,cpu=process_time()-cpu)))
