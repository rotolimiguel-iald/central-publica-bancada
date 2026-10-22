"""Locate the difference between a full log multiplier and the local UV log."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from collections import defaultdict
import hashlib,json,time,uuid
import sympy as s
from source_full_fourier_engine import kernels,at_node
from first_curvature_gauge_generating_engine import oneform_generator,AXES
from curved_harmonic_fourier_engine import node_weights
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'source_firstK_log_partition';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'source_full_fourier_engine.py',H/'source_firstK_symbol/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 question='Does the common FourierLog difference arise from explicit log(z) kernels or noncommuting source ordering?',
 method='Split actual sum by raw-curvature order, external-curvature order, raw-log power and external polynomial degree; do not force UV equality.',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();nodes=json.loads((H/'angular_cubature_degree12/results.json').read_bytes())['nodes']
prior=json.loads((H/'source_firstK_symbol/results.json').read_bytes());data=[];checks=0
for fixture in prior['values'][:3]:
    T=tuple(BASIS[fixture['T']]);p=tuple(fixture['p']);v=tuple(fixture['v']);pieces=defaultdict(F)
    for node in nodes:
        x=tuple(node['vector']);w=F(node['weight'])
        for rorder in (0,1):
            o=1-rorder
            for r,k,raw in kernels(T,rorder):
                if not raw:continue
                ext=oneform_generator((),(AXES[k],) if k>=0 else (),AXES[r],p,v,x,o)
                values=at_node(raw,x);m=(2 if k>=0 else 3)-2*rorder
                for j,c in enumerate(ext):
                    if not c:continue
                    for ell,value in enumerate(values):
                        if not value:continue
                        phase=(-1)**(m-j)
                        coefficient=node_weights(m-j,ell,x,p,6)[1]
                        pieces[(rorder,o,ell,j)]+=w*phase*c*value*coefficient
    total=sum(pieces.values(),F());assert total==F(fixture['full'][1]);checks+=1
    no_raw_log=sum((val for key,val in pieces.items() if key[2]==0),F())
    raw_log=sum((val for key,val in pieces.items() if key[2]==1),F())
    local=F(fixture['local_UV_Log'])
    row=dict(T=fixture['T'],total=str(total),without_explicit_logz=str(no_raw_log),explicit_logz=str(raw_log),
        local_UV=str(local),no_raw_log_minus_UV=str(no_raw_log-local),
        pieces=[dict(raw_order=k[0],external_order=k[1],logz_power=k[2],external_degree=k[3],value=str(v)) for k,v in sorted(pieces.items())])
    data.append(row);print(json.dumps({k:v for k,v in row.items() if k!='pieces'}),flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),status='SOURCE_LOG_DIFFERENCE_PARTITIONED',
 values=data,checks=checks,cpu_seconds=time.process_time()-cpu,full_Q2=False,curved_adjunction_validated=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='values'}))
