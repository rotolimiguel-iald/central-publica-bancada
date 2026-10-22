"""Independent simplex check of the constant-ghost transverse residual."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_vertex_engine import marked,simplex_log,AXES,gauge
HERE=Path(__file__).resolve().parent;DEST=HERE/'metric_primitive_zero_ghost_audit';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_vertex_engine.py'),
    target='Independent Feynman-simplex extraction and transverse null test for ANY Z',
    known_counterexample_sha256=sha(HERE/'metric_primitive_zero_ghost/results.json')))
start,cpu=perf_counter(),process_time();checks=[]
def check(name,expr):assert s.simplify(expr)==0,(name,expr);checks.append(name)
p=AXES[0];v=p;zero=s.zeros(4,1);H=s.zeros(4);H[1,1]=1;T=H
val,g,m,ng,nm=marked(T,H,p,zero,v)
g2=simplex_log(ng,-zero,-p);m2=simplex_log(nm,-p,-p)
check('ghost_simplex_vs_radial',g2-g)
check('metric_simplex_vs_radial',m2-m)
check('full_simplex_result',g2-m2/4-s.Rational(1,6))
z=s.Matrix(s.symbols('z0:4'))
check('transverse_source_kills_any_Z',s.trace(T*gauge(p,z)))
check('zero_ghost_gauge_variation',sum(gauge(zero,v)))
check('source_transverse',sum(T*p))
assert val!=0
new(DEST/'results.json',dict(statute='DERIVED_CONSTANT_GHOST_TRANSVERSE_OBSTRUCTION_TO_FIELD_ONLY_CHANGE',
    counterexample='p=v=e0,l=0,H=T=e11',R1=str(val),ghost=str(g2),metric=str(m2),
    checks_passed=len(checks),checks=checks,
    scope='No Z alone or quadratic metric A2 can match this component; local translation-equivariant linear field change commutes with constant translations',
    additional_BV_generators_not_excluded=True,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start))
print(json.dumps(dict(checks=len(checks),R1=str(val),ghost=str(g2),metric=str(m2)),ensure_ascii=False))
