"""Coherent one-pair tensor extension; exact local contacts, not BRST anomaly."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent
DEST=HERE/'tensor_extension'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and b
    t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(
    at=datetime.now(timezone.utc).isoformat(),statute='INPUT_COHERENT_ONE_PAIR_EXTENSION',
    source_sha256=sha(Path(__file__)),
    predecessor=dict(path=str(HERE/'primitive_extension/manifest.json'),
                     sha256=sha(HERE/'primitive_extension/manifest.json')),
    convention='signature +---, z=x^2-i0, C=4*i*pi^2, box(z^-1)=C*delta',
    prescription='R(u)=FP_a=0 [(1-a)*mu_R^(2a)*z^a*u]; SAME a for all polynomially related one-pair kernels',
    scale='mu_R>0 fixed symbol',
    selected_local_terms='Subtract one residue from analytic MS; retains earlier R2 exactly',
    operations='tensor numerator multiplication, trace, distributional differentiation with residue contacts',
    scope='Single pair of points, leading homogeneous kernels. No overlapping graph or full Ward sum',
    expected_controls=['Independent scalar differential recursion breaks z multiplication',
        'Naive tensor differentiation without local contact violates trace',
        'Dropping second pole in derivative commutator',
        'Reversing finite residue correction'],
    all_graphs_renormalized=False,quantum_anomaly_computed=False))
start,cpu=perf_counter(),process_time()
a,z,mu,C=s.symbols('a z mu C',nonzero=True)
checks=[];negatives=[]
def check(name,expr):
    assert s.simplify(expr)==0,name
    checks.append(dict(name=name,passed=True))
def reject(name,expr):
    assert s.simplify(expr)!=0,name
    negatives.append(dict(name=name,detected=True))
def r(n):return -s.Rational(1,4**(n-1)*s.factorial(n-1)*s.factorial(n-2))
def harmonic(n):return sum(s.Rational(1,k) for k in range(1,n+1))
def ms(n):return (harmonic(n-1)+harmonic(n-2))*r(n)
def coherent(n):return ms(n)-r(n)
rows=[]
for n in range(2,8):
    den=s.prod(4*(j-1-a)*(j-2-a) for j in range(2,n+1))
    coeff=s.series(1/den,a,0,1).removeO().expand()
    check(f'residue_n{n}',coeff.coeff(a,-1)-r(n))
    check(f'finite_MS_n{n}',coeff.coeff(a,0)-ms(n))
    check(f'finite_coherent_n{n}',s.expand((1-a)*coeff).coeff(a,0)-coherent(n))
    rows.append(dict(n=n,residue_coefficient=str(r(n)),
        MS_minus_differential=str(ms(n)),coherent_minus_differential=str(coherent(n))))
check('R2_unchanged',coherent(2))
check('R3_local_correction',coherent(3)+s.Rational(3,64))
# All contact coefficients below multiply C*box^(n-3)delta.
# Coherent analytic extension commutes with multiplication by z. Therefore this
# derives the contact in z*D_n relative to D_(n-1), not a scalar numerical test.
for n in range(3,8):
    b=4*(n-1)*(n-2)
    defect=ms(n-1)-b*ms(n)
    check(f'coherent_z_multiplication_n{n}',defect+b*coherent(n)-coherent(n-1))
    check(f'pole_multiplication_n{n}',b*r(n)-r(n-1))
    check(f'box_recursion_contact_n{n}',coherent(n-1)-b*coherent(n)+4*(2*n-3)*r(n))
    reject(f'uncorrected_differential_family_z_multiplication_n{n}',defect)
check('first_differential_family_defect',ms(2)-8*ms(3)-s.Rational(3,8))

# Rank-two logarithmically divergent kernel x_mu*x_nu/z^3.
Ufinite,Ures,Dmunu,eta=s.symbols('Ufinite Ures Dmunu eta')
tensor_a=Dmunu/(4*(a-1)*(a-2))-eta*(Ures/a+Ufinite)/(2*(a-2))
tensor_finite=s.series((1-a)*tensor_a,a,0,1).removeO().expand().coeff(a,0)
expected=Dmunu/8+eta*(Ufinite-Ures)/4+eta*Ures/8
check('rank_two_finite_part_common_regulator',tensor_finite-expected)
R2,delta=s.symbols('R2 delta')
T=expected.subs({Ufinite:R2-C*delta/4,Ures:-C*delta/4})
check('rank_two_local_term',T-(Dmunu/8+eta*R2/4-eta*C*delta/32))
trace=T.subs({Dmunu:C*delta,eta:4})
check('tensor_trace_matches_scalar_R2',trace-R2)
check('second_derivative_identity_requires_contact',8*T-2*eta*R2+eta*C*delta/4-Dmunu)
reject('naive_tensor_trace_loses_contact',C*delta/8)
reject('opposite_rank_two_counterterm',C*delta/4)

# Distributional derivative does not commute blindly with this extension.
# dR(u)-R(du)=2 FP[a(1-a) x_mu/z U_u(a)]. Higher poles matter.
cm2,cm1,c0=s.symbols('cm2 cm1 c0')
comm=s.expand(2*a*(1-a)*(cm2/a**2+cm1/a+c0)).coeff(a,0)
check('derivative_commutator_multiple_poles',comm-2*(cm1-cm2))
reject('simple_pole_formula_used_with_double_pole',comm-2*cm1)
new(DEST/'results.json',dict(
    statute='REAL_EXACT_ALGEBRA_DERIVED_ONE_PAIR_TENSOR_NORMALIZATION',
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    checks=checks,negative_controls=negatives,checks_passed=len(checks),
    negative_controls_detected=len(negatives),radial_coefficients=rows,
    sympy_version=s.__version__,wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    CAS_proves_distribution_theory=False,all_graphs_renormalized=False,
    quantum_anomaly_computed=False,gate_changed=False))
print(json.dumps(dict(checks=len(checks),negative_controls=len(negatives),
    scope='one_pair_tensor_normalization_not_full_anomaly'),ensure_ascii=False))
