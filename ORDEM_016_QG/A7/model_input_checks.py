"""Exact input checks for A7.b. This does not calculate a quantum anomaly."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time
import sympy as sp

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[1]
DEST = HERE / 'model_inputs'
DEST.mkdir(exist_ok=True)
START = time.perf_counter()
CPU_START = time.process_time()
SOURCES = [
 'QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md',
 'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md',
 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',
 'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md',
]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save_new(p, data):
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    assert not p.exists(), f'Preserve existing artifact: {p}'
    tmp = p.with_suffix(p.suffix + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(p)

source_pins = {str(CHAT / p): sha(CHAT / p) for p in SOURCES}
save_new(DEST / 'PRE_REGISTER.json', dict(
    status='INPUT_CHECKS_ONLY_NOT_A_QUANTUM_PRESCRIPTION',
    at=datetime.now(timezone.utc).isoformat(), source_sha256=sha(Path(__file__)),
    sources=source_pins, dimension=4, signature='+---',
    curvature_convention='R_abcd=K(g_ac g_bd-g_ad g_bc), Ric=3K g, Lambda=3K',
    model='Metric minimal sector of087; xi propagators excluded by model restriction, not integration.',
    scalar_comparison='Unprojected Einstein-sigma with constant background keeps three tangent scalar fluctuations.',
    planned_checks=['curvature contractions', 'on-shell cosmological constant',
                    'trace reversal', 'gauge-fixed Hessian lower-order terms',
                    'principal gauge and ghost identities', 'graded ghost inverse',
                    'scalar quadratic term', 'negative controls'],
    quantum_anomaly_computed=False, products_prescription_fixed=False))

checks = []
negatives = []

def zero(expr):
    if isinstance(expr, sp.MatrixBase):
        return all(sp.expand(v) == 0 for v in expr)
    return sp.simplify(expr) == 0

def check(name, expr):
    ok = zero(expr)
    checks.append(dict(name=name, ok=bool(ok)))
    assert ok, (name, expr)

def reject(name, expr):
    detected = not zero(expr)
    negatives.append(dict(name=name, detected=bool(detected)))
    assert detected, name

eta = sp.diag(1, -1, -1, -1)
K = sp.Symbol('K', positive=True)
kappa = sp.Symbol('kappa', real=True, nonzero=True)
Lambda, box = sp.symbols('Lambda box', real=True)
indices = [(a,b) for a in range(4) for b in range(a,4)]
hvars = sp.symbols('h0:10')
h = sp.zeros(4)
for (a,b), value in zip(indices,hvars):
    h[a,b] = h[b,a] = value
hup = eta*h*eta
tr = sp.trace(eta*h)

def reverse(x):
    return x - eta*sp.trace(eta*x)/2

def riemann(a,b,c,d):
    return K*(eta[a,c]*eta[b,d]-eta[a,d]*eta[b,c])

ric = sp.Matrix(4,4,lambda b,d: sum(eta[a,c]*riemann(a,b,c,d)
                                             for a in range(4) for c in range(4)))
R = sp.trace(eta*ric)
check('Ricci contraction of declared curvature convention', ric - 3*K*eta)
check('scalar curvature', R - 12*K)
background_equation = ric - R*eta/2 + Lambda*eta
check('on-shell condition Lambda=3K', background_equation.subs(Lambda,3*K))
reject('Lambda=0 at nonzero K must fail on-shell',background_equation.subs(Lambda,0))
check('trace reversal squares to identity in dimension four', reverse(reverse(h))-h)

curvature_h = sp.Matrix(4,4,lambda a,b: sum(riemann(a,r,b,s)*hup[r,s]
                                               for r in range(4) for s in range(4)))
check('R_arbs h^rs', curvature_h - K*(eta*tr-h))
LR = (ric*eta*h+h*eta*ric)/2 - curvature_h - R*h/2 + eta*sum(
    ric[r,s]*hup[r,s] for r in range(4) for s in range(4))/2
check('curvature part of deltaG from source066', LR - (-2*K*h+K*eta*tr/2))
metric_hessian = (-box*reverse(h)/2 + LR + 3*K*h)/(2*kappa)
normalized = -4*kappa*reverse(metric_hessian)
check('normalized metric operator', normalized - (box*h-2*K*h+2*K*eta*tr))
check('trace equation', sp.trace(eta*normalized)-(box+6*K)*tr)
f = sp.Symbol('f',real=True)
scale_subs = {hvars[n]: f*eta[a,b] for n,(a,b) in enumerate(indices)}
check('constant scale variation of Einstein equation',
      (LR+3*K*h).subs(scale_subs)-3*K*f*eta)

endomorphism = normalized-box*h
endmatrix = sp.Matrix([endomorphism[a,b] for a,b in indices]).jacobian(hvars)
reverse_matrix = sp.Matrix([reverse(h)[a,b] for a,b in indices]).jacobian(hvars)
check('trace-reversal matrix involution',reverse_matrix**2-sp.eye(10))
check('normalization determinant nonzero',reverse_matrix.det()+1)
eigenvalues = endmatrix.eigenvals()
assert eigenvalues == {-2*K:9,6*K:1}, eigenvalues
checks.append(dict(name='curvature endomorphism has nine traceless and one trace eigenvalues',ok=True))
reject('dropping trace term changes the operator',normalized-(box*h-2*K*h))
reject('wrong overall Hessian normalization',4*kappa*reverse(metric_hessian)-normalized)

p = sp.Matrix(sp.symbols('p0:4'))
v = sp.Matrix(sp.symbols('v0:4'))
pu = eta*p
p2 = (p.T*eta*p)[0]

def C(x):
    return reverse(x)*pu

def symdiv(w):
    return (p*w.T+w*p.T)/2-eta*(pu.T*w)[0]/2

gauge_h = p*v.T+v*p.T
check('principal ghost C(Kv)=p_squared v', C(gauge_h)-p2*v)
ric_principal = (p*(h*pu).T+(h*pu)*p.T-p2*h-p*p.T*tr)/2
scalar_principal = (pu.T*h*pu)[0]-p2*tr
einstein_principal = ric_principal-eta*scalar_principal/2
check('principal Einstein decomposition',einstein_principal-(-p2*reverse(h)/2+symdiv(C(h))))
gauge_subs = {hvars[n]:gauge_h[a,b] for n,(a,b) in enumerate(indices)}
check('principal ungauged Hessian kills gauge direction',einstein_principal.subs(gauge_subs, simultaneous=True))
check('principal gauge-fixed normalization',
      -2*reverse(einstein_principal-symdiv(C(h)))-p2*h)
reject('uncancelled de Donder term is not scalar principal symbol',
       -2*reverse(einstein_principal)-p2*h)

q = sp.Symbol('q',nonzero=True)
ghost_hessian = sp.BlockMatrix([[sp.zeros(4),-q*sp.eye(4)],[q*sp.eye(4),sp.zeros(4)]]).as_explicit()
ghost_green = sp.BlockMatrix([[sp.zeros(4),sp.eye(4)/q],[-sp.eye(4)/q,sp.zeros(4)]]).as_explicit()
check('graded ghost Hessian antisymmetric',ghost_hessian+ghost_hessian.T)
check('graded ghost right inverse',ghost_hessian*ghost_green-sp.eye(8))
check('graded ghost left inverse',ghost_green*ghost_hessian-sp.eye(8))
wrong_green = sp.BlockMatrix([[sp.zeros(4),sp.eye(4)/q],[sp.eye(4)/q,sp.zeros(4)]]).as_explicit()
reject('ungraded ghost inverse must be rejected',ghost_hessian*wrong_green-sp.eye(8))

# An explicit S3 chart agrees at quadratic order with geodesic coordinates.
# No assertion about their equality at cubic/higher order is made.
t, cm = sp.symbols('t cm', real=True)
x = sp.Matrix(sp.symbols('x0:3'))
dx = sp.Matrix(4,3,lambda a,i: sp.Symbol(f'dx{a}_{i}'))
xnorm = (x.T*x)[0]
chart_metric = sp.eye(3)+t**2*(x*x.T)/(1-t**2*xnorm)
sigma_density = cm*t**2*sum(eta[a,b]*(dx.row(a)*chart_metric*dx.row(b).T)[0]
                            for a in range(4) for b in range(4))/2
quadratic_sigma = sp.expand(sigma_density.series(t,0,3).removeO()).coeff(t,2)
expected_sigma = cm*sum(eta[a,a]*dx[a,i]**2 for a in range(4) for i in range(3))/2
check('constant sigma background retains three scalar kinetic terms',quadratic_sigma-expected_sigma)
dt_vars = [dx[0,i] for i in range(3)]
kinetic_sigma = sp.hessian(quadratic_sigma,dt_vars)
check('scalar kinetic Hessian rank three when cm nonzero',kinetic_sigma-cm*sp.eye(3))
reject('constant background is not removal of scalar fluctuations',quadratic_sigma)
check('restriction of constant map has no matter action',
      sigma_density.subs({dx[a,i]:0 for a in range(4) for i in range(3)}))

for name,value in source_pins.items():
    assert sha(Path(name)) == value
result = dict(status='PASS_INPUT_CHECKS_ONLY', source_sha256=sha(Path(__file__)),
              plan_sha256=sha(DEST/'PRE_REGISTER.json'),
              at=datetime.now(timezone.utc).isoformat(), sympy_version=sp.__version__,
              checks=checks, negative_controls=negatives,
              formulas=dict(metric='P h = box h - 2 K h + 2 K g tr(h)',
                            ghost='Q v = box v + 3 K v',
                            metric_normalization='B = -I_tr/(4 kappa)',
                            scalar_kinetic=str(quadratic_sigma)),
              eigenvalues={str(k):int(v) for k,v in eigenvalues.items()},
              quantum_anomaly_computed=False, products_prescription_fixed=False,
              wall_seconds=time.perf_counter()-START,cpu_seconds=time.process_time()-CPU_START)
save_new(DEST/'results.json', result)
print(json.dumps(result,ensure_ascii=False,indent=2))
