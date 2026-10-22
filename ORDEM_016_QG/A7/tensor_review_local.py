"""Targeted audit of the received tensor-contact review, not a new extension."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s

H=Path(__file__).resolve().parent
O=H/'tensor_review_local'
O.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    b=(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    assert not p.exists(), p
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b); assert t.read_bytes()==b and b; t.replace(p)
review=H/'received_reviews/9eefec6b-74ed-41c0-a50f-d5098179eba0.md'
source=H/'tensor_extension/DERIVACAO_TENSORIAL.md'
put(O/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(source),review_sha256=sha(review),
    scope='Formal Laurent audit conditional on meromorphic distribution family and Green identity',
    targets=['scheme first jet versus full analytic prefactor',
        'log derivative sensitivity to second scheme jet',
        'meromorphic derivation of z D_n contact',
        'one derivative commutator instance','doubled regulator typo'],
    forbidden=['undefined log(z)*delta products','epsilon limits without proof',
        'new canonical prescription','Q2 or gate closure']))
start=time.process_time(); checks=[]
def ck(name,expr):
    residual=s.simplify(expr)
    assert residual==0,(name,residual)
    checks.append(name)
a,g1,g2,r,v0,v1,v2,C=s.symbols('a g1 g2 r v0 v1 v2 C')
def fp(expr): return s.expand(expr).coeff(a,0)
U=r/a+v0+v1*a+v2*a*a
g=1+g1*a+g2*a*a
ck('simple_pole_uses_only_first_scheme_jet',fp(g*U)-(v0+g1*r))
ck('log_derivative_uses_second_scheme_jet',fp(g*s.diff(U,a))-(v1-g2*r))
ck('preserving_primitive_fixes_g1_only',fp(g*U).subs(v0,s.Symbol('D2')+r).subs(g1,-1)-s.Symbol('D2'))
ck('different_prefactor_same_primitive',fp((1-a+a*a)*U)-fp((1-a)*U))
ck('different_prefactor_different_log_extension',fp((1-a+a*a)*s.diff(U,a))-fp((1-a)*s.diff(U,a))+r)
def residue(n): return -s.Rational(1,4**(n-1)*s.factorial(n-1)*s.factorial(n-2))
def h(n): return s.harmonic(n-1)+s.harmonic(n-2)-1
# z Res(U_n)=Res(U_(n-1)); z Box^m delta =4m(m+1)Box^(m-1)delta.
for n in range(3,9):
    b=4*(n-2)*(n-1)
    ck(f'residue_multiplication_n{n}',b*residue(n)-residue(n-1))
    defect=(h(n-1)-h(n))*residue(n-1)
    ck(f'meromorphic_D_contact_n{n}',defect+
        (s.Rational(1,n-1)+s.Rational(1,n-2))*residue(n-1))
ck('D3_defect_3_over_8',(h(2)-h(3))*residue(2)-s.Rational(3,8))
ck('derivative_commutator_xBoxdelta_coefficient',2*residue(3)+s.Rational(1,16))
ck('derivative_commutator_partialdelta_coefficient',-4*residue(3)-s.Rational(1,8))
# The review's literal (mu²z)^a*z^(-1+a) doubles the z regulator.
z,mu=s.symbols('z mu',positive=True)
literal=(mu**2*z)**a*z**(-1+a)
intended=mu**(2*a)*z**(-1+a)
ck('doubled_regulator_log_derivative_error',s.diff(literal-intended,a).subs(a,0)-s.log(z)/z)
result=dict(status='PASS_CONDITIONAL_FORMAL_AUDIT',checks=len(checks),check_names=checks,
    cpu_seconds=time.process_time()-start,
    accepted='Core scalar/tensor coefficients remain consistent in the stated flat one-pair scope',
    rejected=['The prefactor 1-a is uniquely determined as a whole by R2=D2',
        'Cancellation of undefined log(z)*delta establishes a proof'],
    retained_open=['Meromorphic distribution existence and light-cone boundary values are analytic inputs',
        'Unproved epsilon distribution limits in the review are not adopted',
        'Full curved causal Ward coefficient'],
    formula='partial_mu R2 - R(partial_mu z^-2) = (C/8) partial_mu delta',
    controls=dict(g2_shift_on_log='-r',literal_regulator_error='log(z)/z'))
put(O/'results.json',result)
put(O/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
    for p in [Path(__file__),review,source,O/'PRE_REGISTER.json',O/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
