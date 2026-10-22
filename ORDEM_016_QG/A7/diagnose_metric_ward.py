"""Independent diagnostics of the nonzero longitudinal principal loop sum."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import json,hashlib
from metric_principal_vertices import *

HERE=Path(__file__).resolve().parent
DEST=HERE/'metric_diagnostic'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),vertex_sha256=sha(HERE/'metric_principal_vertices.py'),
    previous_sha256=sha(HERE/'metric_bubble/results.json'),
    targets=['complete polarization classical cubic Ward at nonaxis momenta',
             'metric pairing inverse computed independently, without prescribed block inverse'],
    cancel_not_assumed=True))
t,cpu=perf_counter(),process_time()
bs=[basis(i,j) for i in range(4) for j in range(i,4)]
momenta=[((1,-1,0,1),(0,1,2,-1)),((2,1,-1,0),(-1,3,0,2))]
fails=[];checks=0;nonzero=0
for k,p in momenta:
    r=tuple(-k[i]-p[i] for i in range(4))
    for n in range(4):
        v=tuple(int(i==n) for i in range(4))
        for a,H in enumerate(bs):
            for b,J in enumerate(bs[a:],a):
                first=eh_cubic_16k(gauge_matrix(k,v),k,H,p,J,r)
                second=2*eh_quadratic_8k(lie_matrix(H,p,k,v),tuple(k[i]+p[i] for i in range(4)),J,r)
                third=2*eh_quadratic_8k(H,p,lie_matrix(J,r,k,v),tuple(k[i]+r[i] for i in range(4)))
                value=first+second+third
                checks+=1
                if first:nonzero+=1
                if value:fails.append(dict(k=k,p=p,n=n,a=a,b=b,value=value,terms=[first,second,third]))
    clear_caches()
new(DEST/'classical_results.json',dict(checks=checks,failures=fails,
    nonzero_examples=nonzero,wall_seconds=perf_counter()-t,cpu_seconds=process_time()-cpu))
print(json.dumps(dict(checks=checks,failures=len(fails),first_failures=fails[:3],
    nonzero=nonzero,wall_seconds=perf_counter()-t)))
