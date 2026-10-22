"""Measure adjoint correction without fitting to Ward/transversality."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from position_metric_adjoint_engine import *
H=Path(__file__).resolve().parent;D=H/'position_metric_adjoint';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'position_metric_adjoint_engine.py'),
    target='First-K adjoint correction from integrating anchored derivative; independent of Ward=0',
    convention='density +1/6 T sym3(A) gradB for nx2, +1/2 T sym3(A) gradB for nx1; integration by parts yields minus outer derivative',
    full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
prior=list(map(F,json.loads((H/'position_metric_curvature_v2/results.json').read_bytes())['curvature_coefficients']))
def inv(A,B,p):
    a=s.Matrix(4,4,A);b=s.Matrix(4,4,B);pv=s.Matrix(p);p2=(pv.T*pv)[0]
    return list(map(F,[p2*s.trace(a*b),p2*s.trace(a)*s.trace(b),(pv.T*a*pv)[0]*s.trace(b),(pv.T*b*pv)[0]*s.trace(a),(pv.T*a*b*pv)[0]]))
lookup={t:i for i,t in enumerate(LABELS)}
pairs=[(lookup[a],lookup[b]) for a,b in [((1,2),(1,2)),((1,1),(2,2)),((0,0),(1,1)),((1,1),(0,0)),((0,1),(0,1))]]
values=[];p=(1,0,0,0)
for a,b in pairs:
    A,B=BASIS[a],BASIS[b]
    actual=sum((F(n['weight'])*adjoint_node(A,B,p,tuple(n['vector'])) for n in nodes),F())
    ic=inv(A,B,p)
    values.append(dict(a=a,b=b,value=str(actual),basis5=list(map(str,ic))))
    print(json.dumps(dict(a=a,b=b,correction=str(actual),cpu=process_time()-cpu)),flush=True)
fresh(D/'raw_values.json',dict(values=values,cpu_seconds=process_time()-cpu))
M=s.Matrix([v['basis5'] for v in values]);v=s.Matrix([v['value'] for v in values]);fit,params=M.gauss_jordan_solve(v)
assert len(params)==0
combined=[a+F(b) for a,b in zip(prior,fit)]
fresh(D/'results.json',dict(statute='DERIVED_FIRST_K_ADJOINT_CANDIDATE',coefficients=list(map(str,fit)),combined=list(map(str,combined)),
    mixed_difference=str(combined[2]-combined[3]),symmetric_mixed_terms=combined[2]==combined[3],
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'position_metric_adjoint_engine.py',D/'PRE_REGISTER.json',D/'raw_values.json',D/'results.json']]))
print(json.dumps(dict(coefficients=list(map(str,fit)),combined=list(map(str,combined)),symmetric=combined[2]==combined[3],cpu=process_time()-cpu)))
