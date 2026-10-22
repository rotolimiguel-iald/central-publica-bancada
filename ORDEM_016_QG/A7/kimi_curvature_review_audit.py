"""Check new claims in the received Kimi report, without rerunning loops."""
from pathlib import Path
from datetime import datetime, timezone
from time import process_time, perf_counter
import hashlib, json
import sympy as s
H = Path(__file__).resolve().parent
D = H / 'kimi_curvature_review_audit'
D.mkdir(exist_ok=True)
review = H / 'received_reviews/679d8876-d8b9-44db-ae96-3f8f8f67fb54.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p, v):
    b = json.dumps(v, ensure_ascii=False, indent=2).encode()
    assert not p.exists(), str(p)
    t = p.with_name(p.name + '.tmp'); t.write_bytes(b)
    assert t.read_bytes() == b; t.replace(p)
fresh(D / 'PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)), review_sha256=sha(review),
    checks_planned=['RNC scalar first derivative', 'symbol sign', 'K homogeneity',
                    'independent hh invariants', 'existing nonzero curved Hessian'],
    no_loop_recomputed=True, full_Q2=False))
cpu, wall = process_time(), perf_counter()
checks = []
def check(name, expr):
    assert s.simplify(expr) == 0, (name, expr)
    checks.append(name)
x = s.Matrix(s.symbols('x0:4')); z = (x.T*x)[0]
K, q2, eps = s.symbols('K q2 eps')
ginv = s.eye(4) + K*(z*s.eye(4)-x*x.T)/3
drift = []
for j in range(4):
    invpart = sum(s.diff(ginv[i,j],x[i]) for i in range(4))
    volpart = s.diff(-K*z/2,x[j])
    check(f'inverse_derivative_{j}', invpart+K*x[j])
    check(f'volume_derivative_{j}', volpart+K*x[j])
    check(f'nonzero_total_{j}', invpart+volpart+2*K*x[j])
    drift.append(str(s.expand(invpart+volpart)))
for name, E in [('metric_TL',-2*K), ('metric_trace',6*K), ('ghost',3*K)]:
    correct = 1/(q2-E)
    proposed = 1/(q2+E)
    check(name+'_inverse_correct', (q2-E)*correct-1)
    assert s.simplify((q2-E)*proposed-1) != 0
check('two_Omega_insertions_order_K_squared', s.diff((eps*K)**2,eps).subs(eps,0))
# Symmetric bilinear tensor invariant basis: ranks checked, not inferred by names.
def B(i,j):
    A=s.zeros(4)
    A[i,j]=1; A[j,i]=1
    return A
basis=[B(i,j) for i in range(4) for j in range(i,4)]
p=s.Matrix([1,0,0,0])
rows=[]
for i,A in enumerate(basis):
    for C in basis[i:]:
        rows.append([s.trace(A*C),s.trace(A)*s.trace(C),
            (p.T*A*p)[0]*s.trace(C)+(p.T*C*p)[0]*s.trace(A),
            (p.T*A*C*p)[0]])
rank=s.Matrix(rows).rank()
assert rank==4,rank
checks.append('four_independent_K_p_squared_hh_invariants')
# Only arithmetic on the already delivered conformal Hessian. No fresh loop.
prior=(H/'ghost_curved_hessian/DERIVACAO.md').read_text('utf-8-sig')
assert '-19K(df)²/2' in prior
f=s.symbols('f')
check('conformal_gradient_second_variation', s.diff(-s.Rational(19,2)*K*f*f,f,2)+19*K)
fresh(D/'results.json',dict(statute='REAL_EXACT_LOCAL_AUDIT',checks=len(checks),
    check_names=checks,scalar_RNC_first_derivative=drift,hh_invariant_rank=rank,
    corrected_denominators=['q²+2K','q²-6K','q²-3K'],
    rejected=['RNC first derivative cancels', 'D=-(nabla²+E) has symbol q²+E',
              'two linear-Omega vertices have first order in K',
              'maximal symmetry leaves just one Kp² invariant in hh'],
    scope_correction='Free on-shell heat coefficient is not the h-dependent heat functional or its Hessian',
    accepted_existing='Bundle curvature traces and -571/15 free heat combination agree with prior local calculation',
    existing_ghost_hessian_sha256=sha(H/'ghost_curved_hessian/DERIVACAO.md'),
    analytic_caveat='Finite determinant factorization, phases and regularization not established by commutation alone',
    no_loop_recomputed=True,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),review,D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),rank=rank,drift=drift,cpu_seconds=process_time()-cpu)))
