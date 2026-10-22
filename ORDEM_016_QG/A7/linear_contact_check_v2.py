"""Metric-action contact along LINEAR h=u*g; no scalar quantum replacement.

The earlier exponential-family calculation is correct in its coordinate but
subtracts its own quadratic Taylor polynomial, not the original h-free action.
This version keeps the original linear metric split on this restricted family.
"""
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter, process_time
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
DEST=HERE/'linear_normalization_v2'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    data=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as out:out.write(data)
    assert t.read_bytes()==data and data
    t.replace(p)
plan=dict(at=datetime.now(timezone.utc).isoformat(),
    statute='INPUT_LINEAR_METRIC_SPLIT_CONTACT_PLAN',
    source_sha256=sha(Path(__file__)),
    predecessor=dict(path=str(HERE/'linear_contact_check.py'),sha256=sha(HERE/'linear_contact_check.py'),
        correction='Exponential coordinate has a different free/interacting split; keep it as auxiliary only'),
    normalization='Equation158 of Frob1803.10235v3 for linear insertions; full nonlinear prescription still open',
    family='h_mu_nu=u*gbar_mu_nu; gnew=(1+u)*gbar; u formal around zero',
    model='Einstein-Hilbert part of A087 only; no sigma, no gauge/ghost contributions in this restricted calculation',
    signature=[1,-1,-1,-1],background='Rbar=12K,Lambda=3K',max_action_degree=8,
    scope='classical functional derivatives needed in linear temporal contact; not an hbar anomaly coefficient',
    sources=[dict(path=str(HERE/'model_inputs/DERIVACAO_OPERADORES.md'),
        sha256=sha(HERE/'model_inputs/DERIVACAO_OPERADORES.md'))],
    complete_temporal_prescription=False,quantum_anomaly_computed=False)
new(DEST/'PRE_REGISTER.json',plan)
start,cpu=perf_counter(),process_time()
u,f,K,kappa,R,Lambda,eps=s.symbols('u f K kappa R Lambda eps',real=True)
p=s.symbols('p0:4',real=True); df=s.symbols('f0:4',real=True)
hess={(i,j):s.Symbol(f'u{i}{j}',real=True) for i in range(4) for j in range(i,4)}
fhess={(i,j):s.Symbol(f'f{i}{j}',real=True) for i in range(4) for j in range(i,4)}
eta=[1,-1,-1,-1]
q=sum(eta[i]*p[i]**2 for i in range(4))
cross=sum(eta[i]*p[i]*df[i] for i in range(4))
box=sum(eta[i]*hess[i,i] for i in range(4))
boxf=sum(eta[i]*fhess[i,i] for i in range(4))
def D(a,i):
    assert not any(a.has(x) for x in (*hess.values(),*fhess.values()))
    return s.diff(a,u)*p[i]+s.diff(a,f)*df[i]+sum(s.diff(a,p[j])*hess[tuple(sorted((i,j)))]+s.diff(a,df[j])*fhess[tuple(sorted((i,j)))] for j in range(4))
def euler(a):
    return s.diff(a,u)-sum(D(s.diff(a,p[i]),i) for i in range(4))+sum(D(D(s.diff(a,hess[i,i]),i),i) for i in range(4))
checks=[];negatives=[]
def check(name,a):
    assert s.simplify(a)==0,name
    checks.append(dict(name=name,passed=True))
def reject(name,a):
    assert s.simplify(a)!=0,name
    negatives.append(dict(name=name,detected=True))

# Independently contract conformal connection differences to derive curvature.
# Set phi=log(1+u)/2 only AFTER this tensor calculation.
v=s.symbols('v0:4'); ph={(i,j):s.Symbol(f'v{i}{j}') for i in range(4) for j in range(i,4)}
delta=lambda a,b:s.Integer(a==b)
def C(a,b,c):return delta(a,b)*v[c]+delta(a,c)*v[b]-delta(b,c)*eta[b]*eta[a]*v[a]
def derivative_C(a,b,c,d):return delta(a,b)*ph[tuple(sorted((c,d)))]+delta(a,c)*ph[tuple(sorted((b,d)))]-delta(b,c)*eta[b]*eta[a]*ph[tuple(sorted((a,d)))]
ric_der=sum(eta[m]*(sum(derivative_C(a,m,m,a)-derivative_C(a,m,a,m) for a in range(4))) for m in range(4))
ric_quad=sum(eta[m]*sum(C(a,a,b)*C(b,m,m)-C(a,m,b)*C(b,m,a) for a in range(4) for b in range(4)) for m in range(4))
check('conformal_Ricci_derivative_trace',ric_der+6*sum(eta[i]*ph[i,i] for i in range(4)))
check('conformal_Ricci_quadratic_trace',ric_quad+6*sum(eta[i]*v[i]**2 for i in range(4)))
L=-f*((1+u)*R-3*box+s.Rational(3,2)*q/(1+u)-2*Lambda*(1+u)**2)/(2*kappa)
EL=euler(L)
expected=(-f*R+4*Lambda*f*(1+u)+3*f*box/(1+u)-s.Rational(3,2)*f*q/(1+u)**2+3*cross/(1+u)+3*boxf)/(2*kappa)
check('metric_linear_split_Euler_contact',EL-expected)
Lparts=-f*((1+u)*R+s.Rational(3,2)*q/(1+u)-2*Lambda*(1+u)**2)/(2*kappa)-3*cross/(2*kappa)
check('integration_by_parts_with_cutoff',euler(Lparts)-EL)
shell={R:12*K,Lambda:3*K}
zero={u:0,**{x:0 for x in p},**{x:0 for x in hess.values()}}
check('localized_background_contact',EL.subs(shell).subs(zero)-3*boxf/(2*kappa))
reject('dropping_localized_background_contact',EL.subs(shell).subs(zero))
scale={x:eps*x for x in [u,*p,*hess.values()]}
poly=s.series(L.subs(shell).subs(scale,simultaneous=True),eps,0,9).removeO().expand()
Lfree=sum(poly.coeff(eps,n) for n in range(3))
Vexact=3*f*u*q/(4*kappa*(1+u))
check('exact_interaction_after_original_linear_split',L.subs(shell)-Lfree-Vexact)
EV=euler(Vexact)
EVclosed=-3/(4*kappa)*(f*q/(1+u)**2+2*f*u*box/(1+u)+2*u*cross/(1+u))
check('interaction_contact_closed_form',EV-EVclosed)
expected_series=s.series(EVclosed.subs(scale,simultaneous=True),eps,0,8).removeO().expand()
for n in range(3,9):check(f'original_metric_vertex_{n}_contact_{n-1}',euler(poly.coeff(eps,n))-expected_series.coeff(eps,n-1))
reject('missing_cutoff_gradient_in_interaction_contact',-3*u*cross/(2*kappa*(1+u)))
reject('interaction_contact_must_not_include_free_contact',EL.subs(shell)-EV)
check('cosmological_trace_family_has_no_cubic_vertex',s.diff(Lambda*f*(1+u)**2/kappa,u,3))
# Removing the cutoff-gradient term from the fully varied interaction is wrong;
# dropping the integrated-by-parts term linear in u does NOT change cubic+ V.
check('box_cutoff_belongs_to_linear_action_not_cubic_interaction',s.diff(EV,fhess[0,0]))
reject('wrong_interaction_kinetic_sign',euler(-Vexact)-EV)
result=dict(statute='REAL_EXACT_CAS_METRIC_LINEAR_FAMILY_CONTACT_NOT_ANOMALY',
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    sympy_version=s.__version__,checks=checks,negative_controls=negatives,
    checks_passed=len(checks),negative_controls_detected=len(negatives),
    full_contact=str(s.factor(expected)),interaction=str(Vexact),interaction_contact=str(s.factor(EVclosed)),
    action_vertex_coefficients={str(n):str(poly.coeff(eps,n)) for n in range(3,9)},
    complete_temporal_prescription=False,quantum_anomaly_computed=False,gate_changed=False,
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:result[k] for k in ['statute','checks_passed','negative_controls_detected','wall_seconds','cpu_seconds']},ensure_ascii=False))
