"""Measure transverse constant-ghost vertices against the free Einstein Hessian."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_vertex_engine import marked,AXES
HERE=Path(__file__).resolve().parent;DEST=HERE/'constant_ghost_eom';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    b=json.dumps(o,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_vertex_engine.py'),
    target='Transverse R1 at ghost momentum0 compared to a(p.v)E(H)+b(p.v)P_T trE(H)',
    scope='p=v=e0, four measured polarizations; no general factorization assumed'))
start,cpu=perf_counter(),process_time();p=v=AXES[0];z=s.zeros(4,1)
def h(i,j):
    m=s.zeros(4);m[i,j]=m[j,i]=1;return m
def E(H):
    C=H*p-p*s.trace(H)/2
    Cd=(p*C.T+C*p.T)/2-s.eye(4)*p.dot(C)/2
    return p.dot(p)*(H-s.eye(4)*s.trace(H)/2)-2*Cd
cases=[]
for H,T in [(h(1,1),h(1,1)),(h(1,1),h(2,2)),(h(2,3),h(2,3)),(s.diag(0,1,-1,0),s.diag(0,1,-1,0))]:
    val,g,m,*_=marked(T,H,p,z,v);eh=E(H)
    cases.append(dict(H=list(map(str,H)),T=list(map(str,T)),value=str(val),
        contraction_E=str(s.trace(T*eh)),trace_product=str(s.trace(T)*s.trace(eh))))
alpha,beta=s.symbols('alpha beta')
eq=[alpha*s.sympify(x['contraction_E'])+beta*s.sympify(x['trace_product'])-s.sympify(x['value']) for x in cases]
sol=s.solve(eq[:2],[alpha,beta],dict=True)
assert len(sol)==1
residuals=[str(s.simplify(x.subs(sol[0]))) for x in eq]
result=dict(statute='MEASURED_TRANSVERSE_CONSTANT_GHOST_EOM_PROBE',cases=cases,
    fitted={str(k):str(v) for k,v in sol[0].items()},residuals=residuals,
    all_four_match=all(x=='0' for x in residuals),not_general_tensor_proof=True,
    full_Q2=False,gate_changed=False,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result)
print(json.dumps(result,ensure_ascii=False))
