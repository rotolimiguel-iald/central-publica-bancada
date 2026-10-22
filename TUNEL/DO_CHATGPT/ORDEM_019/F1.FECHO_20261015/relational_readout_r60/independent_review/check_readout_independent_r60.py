"""Independent R60 algebra and byte-custody checks; no constructor imports."""
from pathlib import Path
import ast
import datetime as dt
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
checks = []

def pin(path):
    path = Path(path)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

def record(name, passed, detail):
    checks.append({"name": name, "pass": bool(passed), "detail": detail})
    assert passed, name

def zero(expr):
    return s.simplify(expr) == 0

# Parameterize odds directly: positivity removes the square-root branch ambiguity.
r, u, v, ga, gb = s.symbols("r u v ga gb", positive=True)
b = r/(1+r)
readings = [ga*u*(1-b), gb*u*b, ga*v*b, gb*v*(1-b)]
q = s.factor(readings[1]*readings[2]/(readings[0]*readings[3]))
record("odds_and_inverse", q == r*r and zero(s.sqrt(q)/(1+s.sqrt(q))-b),
       "For positive odds r, Q=r^2 and b=r/(1+r); unique b in (0,1).")
g11,g21,g12,g22 = s.symbols("g11 g21 g12 g22", positive=True)
drift = [g11*u*(1-b), g21*u*b, g12*v*b, g22*v*(1-b)]
record("gain_drift_multiplier", zero(drift[1]*drift[2]/(drift[0]*drift[3])-r*r*g21*g12/(g11*g22)),
       "Q carries g_A2*g_B1/(g_A1*g_B2), so arbitrary drift destroys identification.")
target = [16,6,8,48]
alternative = [s.Rational(12,5),s.Rational(9,5),s.Rational(6,5),s.Rational(18,5)]
alt = [alternative[0]*10*s.Rational(2,3),alternative[1]*10/s.Integer(3),
       alternative[2]*20/s.Integer(3),alternative[3]*20*s.Rational(2,3)]
record("drift_two_worlds", alt == target,
       "b=1/3 with gains (12/5,9/5,6/5,18/5) yields the reported (16,6,8,48), also possible at b=1/5 with stable gains.")

# Derive lossy moments through quadrature covariance, rather than copying the inversion.
n,ea,eb = s.symbols("n ea eb", positive=True)
I2=s.eye(2); Z=s.diag(1,-1)
V=( (n+s.Rational(1,2))*I2 ).row_join(s.sqrt(n*(n+1))*Z)
V=V.col_join((s.sqrt(n*(n+1))*Z).row_join((n+s.Rational(1,2))*I2))
L=s.diag(s.sqrt(ea),s.sqrt(ea),s.sqrt(eb),s.sqrt(eb))
noise=s.diag((1-ea)/2,(1-ea)/2,(1-eb)/2,(1-eb)/2)
W=L*V*L.T+noise
x=s.simplify(W[0,0]-s.Rational(1,2)); y=s.simplify(W[2,2]-s.Rational(1,2))
z=s.simplify(W[0,2]**2)
record("vacuum_loss_covariance", zero(x-ea*n) and zero(y-eb*n) and zero(z-ea*eb*n*(n+1)),
       "Attenuation plus independent vacuum covariance yields x,y,z in calibrated quadrature units.")
d=s.factor(z-x*y)
record("pair_inverse_composition", all(zero(a-b) for a,b in zip([x*y/d,d/y,d/x],[n,ea,eb])),
       "All three original parameters are recovered on n>0, etaA,etaB>0 under pure-input vacuum-loss assumptions.")
jac=s.Matrix([x,y,z]).jacobian([n,ea,eb]).det()
record("pair_jacobian", zero(jac+ea*eb*n*n), "det=-etaA*etaB*n^2.")
X,Y,D=s.symbols("X Y D", positive=True)
nn=X*Y/D; aa=D/Y; bb=D/X
record("inverse_image", zero(aa*nn-X) and zero(bb*nn-Y) and zero(aa*bb*nn*(nn+1)-(X*Y+D)),
       "The exact image is X,Y>0 and 0<D<=min(X,Y); the latter inequalities are precisely eta<=1. This does not establish purity.")

# Construct an actual mixed Gaussian covariance from a thermal state and a symplectic map.
nu=s.sqrt(3)/2
c=s.sqrt((s.sqrt(3)+1)/2); h=s.sqrt((s.sqrt(3)-1)/2)
S=(c*I2).row_join(h*Z).col_join((h*Z).row_join(c*I2))
J=s.Matrix([[0,1],[-1,0]]); Omega=s.diag(J,J)
Vm=s.simplify(nu*S*S.T)
record("mixed_covariance_constructed", s.simplify(S*Omega*S.T-Omega)==s.zeros(4) and nu>s.Rational(1,2),
       "Symplectic S maps a thermal covariance nu I, nu=sqrt(3)/2>1/2, to a physical nonpure two-mode Gaussian state.")
record("mixed_moments", zero(Vm[0,0]-s.Rational(3,2)) and zero(Vm[2,2]-s.Rational(3,2)) and zero(Vm[0,2]**2-s.Rational(3,2)),
       "Mixed input n=1 has |m|^2=3/2 and no loss; same three observed moments as pure n=2, eta=1/2.")
record("indistinguishable_pair_worlds", [a.subs({n:2,ea:s.Rational(1,2),eb:s.Rational(1,2)}) for a in [x,y,z]]==[1,1,s.Rational(3,2)],
       "Both worlds pass positivity/efficiency guards; purity cannot be inferred from these moments.")
f=lambda a:s.sqrt(a)/(1+s.sqrt(a))
mean_est=(f(1)+f(9))/2; from_mean=f(5)
record("expectation_estimator_distinction", mean_est==s.Rational(5,8) and not zero(mean_est-from_mean),
       "Illustrative positive random readings A1=B1=B2=1, A2 equiprobable 1 or 9: E[inverse]=5/8 != inverse(E[readings])=sqrt(5)/(1+sqrt(5)); not an experiment or noise model fit.")

# Byte custody, without running any author script or touching the eight destinations.
source_pins=json.loads((BASE/'ROOT_SOURCE_PINS_R60.json').read_text(encoding='utf-8'))['sources']
record("root_source_pins", all(pin(i['path'])==i for i in source_pins), "Five primary/dependency source pins measured directly.")
result=json.loads((BASE/'RESULT_R60.json').read_text(encoding='utf-8'))
start=json.loads((BASE/'ALGEBRA_START.json').read_text(encoding='utf-8'))
record("reported_execution_chain", result['count']==len(result['checks'])==34 and all(c['pass'] for c in result['checks']) and result['preregistered']==pin(BASE/'PREREG_R60.json') and result['script']==pin(BASE/'verify_readout_r60.py'),
       "Constructor reports 34 checks; their recorded pins match current bytes. They were not rerun by reviewer.")
plan=json.loads((BASE/'MEMORY_PLAN_R60.json').read_text(encoding='utf-8'))
prior=json.loads((BASE.parent/'pair_covariance_r59/MEMORY_PLAN_R59.json').read_text(encoding='utf-8'))
paths=[r['path'] for r in plan['surfaces']]
record("eight_surfaces_allowlist", len(paths)==len(set(paths))==8 and paths==[r['path'] for r in prior['surfaces']],
       "Same eight destinations as previous reviewed layer; Claude uses MEMORY_2.md.")
rows=[]
for row in plan['surfaces']:
    raw=Path(row['path']).read_bytes();extra=Path(row['append']['path']).read_bytes()
    passed=(pin(row['path'])==row['before'] and len(raw)==row['before_bytes'] and
            pin(row['append']['path'])==row['append'] and plan['marker'].encode() not in raw and
            hashlib.sha256(raw+extra).hexdigest()==row['after_sha256'])
    rows.append({'path':row['path'],'pass':passed,'before_bytes':len(raw),'append_bytes':len(extra)})
record("baseline_and_append_bytes", all(r['pass'] for r in rows), rows)
record("plan_applier_report_pins", plan['applier']==pin(BASE/'memory_r60.py') and plan['report']==pin(BASE/'RELATORIO_R60.txt'),
       "Plan pins match the reviewed applier and report.")
for name in ['memory_r60.py','support_r60.py']:
    ast.parse((BASE/name).read_text(encoding='utf-8'),filename=name)
record("applier_and_helper_ast", True, "Parsed only; neither imported nor executed.")
output={'status':'PASS','reviewer':'codex-mission-memory-review','utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'checks':checks,'count':len(checks),'script':pin(__file__),'sources':source_pins,
        'scope':'Independent exact algebra/covariance and read-only byte checks; no observed data, provider, Lean build, mission mutation or memory application.'}
with (HERE/'INDEPENDENT_CHECKS_R60.json').open('x',encoding='utf-8') as f:
    json.dump(output,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','count':len(checks),'output':pin(HERE/'INDEPENDENT_CHECKS_R60.json')},ensure_ascii=False))
