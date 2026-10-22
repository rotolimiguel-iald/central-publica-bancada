"""Algebraic normalization checks for a fixed primitive Lorentzian extension.

Distributional boundary values and the Fourier fundamental-solution normalization
are written analytic inputs; the CAS verifies radial identities and coefficients.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from time import perf_counter,process_time
import sympy as s

HERE=Path(__file__).resolve().parent
DEST=HERE/'primitive_extension'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw
    tmp.replace(p)
plan=dict(at=datetime.now(timezone.utc).isoformat(),
    statute='INPUT_PRIMITIVE_EXTENSION_FIXED_BEFORE_ALGEBRA',
    source_sha256=sha(Path(__file__)),
    source=dict(url='https://arxiv.org/html/0705.3340v4',section='3.3 end and 3.4',
        equations='223-227',scope='Existence and analytic finite part; numerical constants below independently derived'),
    signature='+---',boundary_value='z=x^2-i0',scale='mu_R>0 fixed reference; never fitted to a Ward result',
    primitive='R2=-1/4 box(log(mu_R^2*z)/z)',
    finite_choice='No extra delta term beyond this differential prescription',
    higher_powers='Rn=box(R_(n-1))/(4*(n-1)*(n-2)), n>=3',
    contact_input='box(1/(x^2-i0))=4*i*pi^2 delta from Fourier inverse of box',
    CAS_scope='Off-origin radial differential algebra and formal Laurent coefficients, not proof of distributional extension',
    all_graphs_renormalized=False,quantum_anomaly_computed=False)
new(DEST/'PRE_REGISTER.json',plan)
start,cpu=perf_counter(),process_time()
z,mu,alpha=s.symbols('z mu alpha',positive=True)
def box(a):return s.expand(4*z*s.diff(a,z,2)+8*s.diff(a,z))
checks=[];negatives=[]
def check(name,a):
    assert s.simplify(a)==0,name
    checks.append(dict(name=name,passed=True))
def reject(name,a):
    assert s.simplify(a)!=0,name
    negatives.append(dict(name=name,detected=True))
log_kernel=s.log(mu**2*z)/z
check('primitive_agrees_off_origin',-box(log_kernel)/4-z**-2)
reject('copying_suppressed_prefactor_minus_half_doubles_primitive',-box(log_kernel)/2-z**-2)
check('analytic_radial_recurrence',box(z**(alpha-1))-4*alpha*(alpha-1)*z**(alpha-2))
# Formal coefficients of the analytic family BEFORE applying box:
# U_alpha=box(mu^(2alpha)*z^(alpha-1))/(4alpha(alpha-1)).
series=s.series(mu**(2*alpha)*z**(alpha-1)/(4*alpha*(alpha-1)),alpha,0,1).removeO().expand()
check('Laurent_pole_coefficient',series.coeff(alpha,-1)+1/(4*z))
check('Laurent_finite_part',series.coeff(alpha,0)+(s.log(mu**2*z)+1)/(4*z))
coeffs={}
for n in range(2,6):
    coeff=-s.Rational(1,4**(n-1)*s.factorial(n-1)*s.factorial(n-2))
    diff=log_kernel
    for _ in range(n-1):diff=box(diff)
    check(f'Rn_{n}_off_origin',coeff*diff-z**(-n))
    coeffs[str(n)]=str(coeff)
check('scale_derivative_before_box',s.diff(log_kernel,mu)*mu-2/z)
# Fourier convention exp(-ipx), inverse box G=-1/(p^2+i0).
# The spacelike contour integral yields G=-i/(4pi^2 z).
C=4*s.I*s.pi**2
A=-s.I/(4*s.pi**2)
check('fundamental_solution_normalization',A*C-1)
MS_residue=-C/4
scale_R=-C/2
scale_G_squared=A**2*scale_R
check('normalized_principal_bubble_scale_contact',scale_G_squared-s.I/(8*s.pi**2))
reject('opposite_i0_without_contact_conjugation',(-A)*C-1)
reject('dropping_finite_local_difference_MS_vs_differential',C/4)
result=dict(statute='REAL_CAS_RADIAL_COEFFICIENTS_DERIVED_PRIMITIVE_EXTENSION',
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    sympy_version=s.__version__,checks=checks,negative_controls=negatives,
    checks_passed=len(checks),negative_controls_detected=len(negatives),
    repeated_box_coefficients=coeffs,MS_residue_delta=str(MS_residue),
    mu_dmu_R2_delta=str(scale_R),mu_dmu_G0_squared_delta=str(scale_G_squared),
    extra_wick_i_hbar_factors_included=False,
    distributional_extension_theorem_verified_by_CAS=False,
    all_graphs_renormalized=False,quantum_anomaly_computed=False,
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:result[k] for k in ['statute','checks_passed','negative_controls_detected','wall_seconds','cpu_seconds']},ensure_ascii=False))
