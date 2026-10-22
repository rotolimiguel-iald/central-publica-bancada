"""Check specific new claims in the returned review; no rerun of the loop."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
from ghost_minimal_heat_engine import s,basis,invariants
H=Path(__file__).resolve().parent;D=H/'kimi_metric_review_audit';D.mkdir(exist_ok=True)
job='2177daf6-29db-4d0c-940a-63d4c582fa04'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,v):
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 source_sha256=sha(Path(__file__)),review_sha256=sha(H/'received_reviews'/f'{job}.md'),
 source_result_sha256=sha(H/'metric_bubble_v2/results.json'),
 objective='Check E01 counterexample, determinant Hessian sign and double-gauge phrase against actual code',
 full_Q2=False,gate_changed=False))
start,cpu=perf_counter(),process_time();old=json.loads((H/'metric_bubble_v2/results.json').read_bytes())
cc=list(map(s.Rational,old['combined_Hessian_coefficients_over_hbar_A0']))
F=lambda A,B:sum(a*b for a,b in zip(cc,invariants(A,B,(1,0,0,0))))
e01=F(basis(0,1),basis(0,1));e11=F(basis(1,1),basis(1,1));checks=[]
def check(n,e):assert s.simplify(e)==0,(n,e);checks.append(n)
check('E01_is_longitudinal_and_zero',e01)
check('E11_is_nonzero_transverse',e11+s.Rational(7,10))
assert e01!=-s.Rational(61,240)
for nu in range(4):
 for rho in range(nu,4):
  A=basis(0,nu)*(2 if nu==0 else 1);B=basis(0,rho)*(2 if rho==0 else 1)
  check(f'double_gauge_{nu}_{rho}',F(A,B))
# Exact scalar log differentiation checks the sign missed by the review.
a,b,u,v=s.symbols('a b u v');log=s.log(1+a*u+b*v)
check('boson_second_variation_sign',s.diff(log/2,a,b).subs({a:0,b:0})+u*v/2)
check('ghost_second_variation_sign',s.diff(-log,a,b).subs({a:0,b:0})-u*v)
ratio=s.symbols('ratio');check('relative_weight_condition',s.solve(ratio/s.Integer(8)+s.Rational(1,16),ratio)[0]+s.Rational(1,2))
new(D/'results.json',dict(statute='REAL_LOCAL_REVIEW_OF_SPECIFIC_MODEL_CLAIMS',checks=len(checks),check_names=checks,
 E01=str(e01),E11=str(e11),
 review_errors=['E01 value -61/240 is false; actual0',
 'Cancellation only fixes a:b=-1:2, not overall sign/norm',
 'F_log is Hessian of Gamma here, not its negative: second derivative of log changes weights',
 'Section9 uses sbarc=+b and omits free K_gauge c, against BV069',
 'Separate curved transversality tests omit source contribution and commutator mixing'],
 source_wording_correction='Ten double-gauge contractions mean unordered pairs of four vector basis gauge images, not diagonal pairs in full ten-dimensional symmetric fiber',
 accepted='Transposed Wick contraction; arithmetic; principal longitudinal identity; Ric/R representation with scoped caveats',
 no_loop_recomputed=True,full_Q2=False,gate_changed=False,
 wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu))
files=[Path(__file__),D/'PRE_REGISTER.json',D/'results.json']
new(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=len(checks),E01=str(e01),E11=str(e11),cpu_seconds=process_time()-cpu)))
