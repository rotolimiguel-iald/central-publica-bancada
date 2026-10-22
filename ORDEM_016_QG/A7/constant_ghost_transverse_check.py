"""Complete transverse symmetric-tensor basis check at l=0 and v parallel p."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_vertex_engine import marked,AXES
HERE=Path(__file__).resolve().parent;DEST=HERE/'constant_ghost_transverse';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    b=json.dumps(o,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_vertex_engine.py'),
    target='P_T R1(H,p;0,v) P_T = -(p.v)[E(H)/6 + P_T trE(H)/12]',
    restriction='p nonzero, v parallel p, H transverse symmetric; 6x6 complete basis at p=v=e0',
    proposed_coefficients_source_sha256=sha(HERE/'constant_ghost_eom/results.json'),
    extension='O4 covariance and homogeneous momenta degree3; not arbitrary v or curved finite anomaly'))
start,cpu=perf_counter(),process_time();p=v=AXES[0];zero=s.zeros(4,1);Pt=s.eye(4)-p*p.T
basis=[]
for i in range(1,4):
    for j in range(i,4):
        H=s.zeros(4);H[i,j]=H[j,i]=1;basis.append(H)
results=[];nonzero=0
for hi,H in enumerate(basis):
    # For transverse H and unit p, the ungauged Einstein Hessian is H-P_T trH.
    E=H-Pt*s.trace(H)
    assert E*p==zero
    pred=-E/6-Pt*s.trace(E)/12
    for ti,T in enumerate(basis):
        value,g,m,*_=marked(T,H,p,zero,v)
        expected=s.trace(T*pred)
        assert value==expected,(hi,ti,value,expected)
        if value:nonzero+=1
        results.append(dict(H=hi,T=ti,value=str(value),predicted=str(expected)))
    print(json.dumps(dict(completed_H=hi,components=len(results))),flush=True)
assert nonzero
res=dict(statute='DERIVED_TRANSVERSE_CONSTANT_GHOST_IDENTITY_FOR_V_PARALLEL_P',
    checks_passed=len(results),nonzero_components=nonzero,cases=results,
    formula='P_T R1 P_T=-(p.v)[E(H)/6+P_T trE(H)/12]',
    restriction='l=0, p nonzero, v parallel p, H transverse symmetric',
    complete_general_R1_matched=False,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',res)
print(json.dumps({k:v for k,v in res.items() if k!='cases'},ensure_ascii=False))
