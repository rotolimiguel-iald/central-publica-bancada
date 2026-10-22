"""Preregister and measure h* h c and the principal h* c c BV component."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_vertex_engine import (AXES,BASIS,marked,ghost_triangle,gauge,lie,bracket,R0,simplex_log)
HERE=Path(__file__).resolve().parent;DEST=HERE/'marked_vertex';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_vertex_engine.py'),
    method='Differentiate -U P Q^-1 V in external h with fixed background gauge',
    metric='U P H1 P Q^-1 V; W=16kappa H1, gives -metric/4 after removal of 4i*kappa',
    ghost='U P Q^-1 V_h Q^-1 V; gives +ghost after removal of 4i*kappa',
    external='h*(T,-p-r),h(H,p),c(v,r)',
    BV='K triangle + R0(B) - Lie_v R0(w) + Lie_w R0(v) - R1(Kw,v) + R1(Kv,w)',
    expectation='measure residual; do not impose zero or refit signs',
    scopes_excluded=['curvature','cutoff contacts','finite anomaly','full Q2'],gate_changed=False))
start,cpu=perf_counter(),process_time();checks=[];cases=[]
def check(name,e):
    assert s.expand(e)==0,(name,e);checks.append(name)
def pair(T,H):return s.trace(T*H)
p,r=AXES[0],AXES[1]
specs=[(BASIS[0],AXES[0],AXES[1]),(BASIS[1],AXES[0],AXES[1]),
       (BASIS[4],AXES[1],AXES[0]),(BASIS[2],AXES[2],AXES[1])]
for index,(T,v,w) in enumerate(specs):
    left,lg,lm,ln,lmn=marked(T,gauge(r,w),r,p,v)
    right,rg,rm,rn,rmn=marked(T,gauge(p,v),p,r,w)
    for tag,val,n,a,b in [('left_ghost',lg,ln,-p,-p-r),('left_metric',lm,lmn,-r,-p-r),
                         ('right_ghost',rg,rn,-r,-p-r),('right_metric',rm,rmn,-p,-p-r)]:
        check(f'simplex_{index}_{tag}',val-simplex_log(n,a,b))
    tri=ghost_triangle(2*T*(p+r),v,w,p,r)
    free=pair(T,R0(p+r,bracket(p,v,r,w))-lie(R0(r,w),r,p,v)+lie(R0(p,v),p,r,w))
    residual=s.expand(tri+free-left+right)
    case=dict(index=index,left=str(left),right=str(right),left_ghost=str(lg),left_metric=str(lm),
              right_ghost=str(rg),right_metric=str(rm),triangle=str(tri),free=str(free),residual=str(residual))
    cases.append(case);print(json.dumps(case),flush=True)
result=dict(statute='REAL_MARKED_PRINCIPAL_KERNELS_MEASURED',cases=cases,
    checks_passed=len(checks),checks=checks,all_BV_residuals_zero=all(s.sympify(c['residual'])==0 for c in cases),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    full_Q2=False,gate_changed=False)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','cases')}),flush=True)
