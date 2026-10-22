"""Necessary zero-ghost-momentum test of a pure quadratic metric redefinition."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_vertex_engine import marked,gauge,AXES
HERE=Path(__file__).resolve().parent;DEST=HERE/'metric_primitive_zero_ghost';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_vertex_engine.py'),
    target='S=R1-R1coord vanishes for ghost momentum l=0 if S=-2 A2(H,K_l v)',
    fixed='Previously chosen Z representative; not all allowed ghost/metric changes',
    cases='p=e0; H=e11 then dense symmetric; v=e0/e1; T=e00/e01/e11',
    stop='First nonzero is sufficient counterexample; otherwise report limited test only',
    no_Lean_or_external_calls=True))
start,cpu=perf_counter(),process_time()
p=AXES[0];zero=s.zeros(4,1)
h0=s.zeros(4);h0[1,1]=1
hd=s.Matrix([[1,2,0,-1],[2,0,1,0],[0,1,-1,2],[-1,0,2,1]])
t0=s.zeros(4);t0[0,0]=1
t1=s.zeros(4);t1[0,1]=t1[1,0]=1
t2=s.zeros(4);t2[1,1]=1
cases=[];found=False
for hi,H in enumerate([h0,hd]):
    if found:break
    for vi,v in enumerate(AXES[:2]):
        if found:break
        # F(0)=0, so R1coord=-K_p Z(H,p;0,v).
        Z=-v*s.trace(H)*p.dot(p)/24+H*v*p.dot(p)/12+H*p*p.dot(v)/12
        prediction=-gauge(p,Z)
        for ti,T in enumerate([t0,t1,t2]):
            val,g,m,ng,nm=marked(T,H,p,zero,v)
            pred=s.trace(T*prediction);diff=s.cancel(val-pred)
            item=dict(H=hi,v=vi,T=ti,R1=str(val),ghost_insertion=str(g),
                metric_insertion=str(m),coordinate_prediction=str(pred),difference=str(diff))
            cases.append(item);print(json.dumps(item),flush=True)
            if diff:
                found=True;break
result=dict(statute='DERIVED_COUNTEREXAMPLE_FIXED_Z_PURE_QUADRATIC_METRIC_CHANGE' if found else 'LIMITED_ZERO_GHOST_TEST_ONLY',
    counterexample_found=found,cases=cases,
    implication='For this fixed Z, S cannot equal -2 A2(H,K_l v) for all inputs' if found else 'No obstruction found in selected examples',
    alternatives_open=['Change Z by its homogeneous freedom','Include allowed linear metric redefinition and induced corrections'],
    full_Q2=False,gate_changed=False,source_sha256=sha(Path(__file__)),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=False))
