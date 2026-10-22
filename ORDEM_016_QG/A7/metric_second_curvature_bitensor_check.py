"""Check Jacobi endpoint jets, lower-order matches and coincident heat logs."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from metric_second_curvature_bitensor_engine import *
from metric_radial_bitensor_engine import metric_radial_jet
H=Path(__file__).resolve().parent;D=H/'metric_second_curvature_bitensor';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'metric_second_curvature_bitensor_engine.py'),
    target='Endpoint Jacobi maps and connection through K²; firstK matches old independent coordinate jets; secondK log matches coincident heat jets',
    smooth_W='Excluded as a separate reference-dependent contribution, not asserted absent in physical state',full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,e):
    numerator=s.together(e).as_numer_denom()[0]
    assert s.expand(numerator.subs(z,sum(t*t for t in x)))==0,(n,str(e))
    checks.append(n)
# Exact scalar Jacobi solutions for constant sectional curvature.
t=s.symbols('t')
for name,expr,expected in [('JX',t/s.sin(t),1+t*t/6+7*t**4/360),
    ('JY',-t/s.tan(t),-1+t*t/3+t**4/45),
    ('A',s.tan(t/2)/t,s.Rational(1,2)+t*t/24),
    ('volume',(s.sin(t)/t)**3,1-t*t/2+13*t**4/120)]:
    check(name,s.series(expr,t,0,5 if name!='A' else 4).removeO()-expected)
for order in (0,1):
    for i in range(-1,4):
        for j in range(-1,4):
            M=green_jet(order,i,j)-metric_radial_jet(order,i,j)
            for a in range(10):
                for b in range(10):check(f'old_jets_{order}_{i}_{j}_{a}_{b}',M[a,b])
    print(json.dumps(dict(order_checked=order,cpu=process_time()-cpu)),flush=True)
f=metric_fiber();F,AX,JX,JY,S,V2=data()
for i in range(4):
    for j in range(4):
        M=green_jet(2,i,j)
        # Log(z) contributes -2 lnLambda; prefactor1/(4pi²)=2A0.
        difference=-4*M.diff(L)-f['mixed'][i,j]*S
        for a in range(10):
            for b in range(10):check(f'coincident_log_{i}_{j}_{a}_{b}',difference[a,b])
    print(json.dumps(dict(second_order_row=i,cpu=process_time()-cpu)),flush=True)
fresh(D/'results.json',dict(statute='DERIVED_SECOND_K_ENDPOINT_JETS_WITH_EXACT_CONTROLS',checks=len(checks),check_names=checks,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False,
    hypotheses=['Spaceform Jacobi endpoint transport','Local heat parametrix, W treated separately']))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'metric_second_curvature_bitensor_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu=process_time()-cpu)))
