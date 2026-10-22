"""Exact local variational contacts on a conformal family of the A087 metric action.

This is not a scalar quantum model, a graviton propagator, or an anomaly calculation.
"""
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter, process_time
import json
import hashlib
import sympy as s

HERE=Path(__file__).resolve().parent
CHAT=HERE.parents[1]
DEST=HERE/'linear_normalization'
DEST.mkdir(exist_ok=True)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as stream:stream.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)

sources=[HERE/'model_inputs/DERIVACAO_OPERADORES.md',
    CHAT/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
    CHAT/'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md']
plan=dict(at=datetime.now(timezone.utc).isoformat(),
    statute='INPUT_PARTIAL_LINEAR_NORMALIZATION_BEFORE_CONTACT_CALCULATION',
    source_sha256=sha(Path(__file__)),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
    imported_source=dict(url='https://arxiv.org/pdf/1803.10235v3',
        theorem='9',equations=['158','174-185'],printed_pages='40-43',
        read_via='web PDF text, not local hash or visual QA'),
    prescription='Impose equation158 on all linear insertions; nonlinear EG extensions remain unfixed',
    calculation='Euler derivative of the metric EH action restricted to g_new=exp(2phi)*g_background',
    scope='Covariant normal-coordinate jets at a point in four Lorentzian dimensions, constant background curvature',
    inputs=dict(signature=[1,-1,-1,-1],background_scalar_curvature='12*K',Lambda='3*K',
        kappa='real nonzero',cutoff='smooth compact f; its derivatives retained',
        field_degree_max=8,metric_family='conformal pullback only, not quantization of phi'),
    expected_controls=['Wrong kinetic sign','Dropping cutoff terms after integration by parts',
        'Treating on-shell background as localized equations with df=0 everywhere',
        'Removing quadratic action after rather than before differentiating'],
    complete_temporal_prescription=False,quantum_anomaly_computed=False)
new(DEST/'PRE_REGISTER.json',plan)
start,cpu=perf_counter(),process_time()
phi,f,K,kappa,R,Lambda,eps=s.symbols('phi f K kappa R Lambda eps',real=True)
pv=s.symbols('p0:4',real=True)
fv=s.symbols('f0:4',real=True)
pp={(i,j):s.Symbol(f'p{i}{j}',real=True) for i in range(4) for j in range(i,4)}
ff={(i,j):s.Symbol(f'f{i}{j}',real=True) for i in range(4) for j in range(i,4)}
eta=[1,-1,-1,-1]
q=sum(eta[i]*pv[i]**2 for i in range(4))
cross=sum(eta[i]*pv[i]*fv[i] for i in range(4))
boxphi=sum(eta[i]*pp[i,i] for i in range(4))
boxf=sum(eta[i]*ff[i,i] for i in range(4))

def D(expr,i):
    out=s.diff(expr,phi)*pv[i]+s.diff(expr,f)*fv[i]
    for j in range(4):
        ij=tuple(sorted((i,j)))
        out+=s.diff(expr,pv[j])*pp[ij]+s.diff(expr,fv[j])*ff[ij]
    # Called only on expressions containing jets of order at most one.
    assert not any(expr.has(x) for x in (*pp.values(),*ff.values())), 'third jet needed'
    return s.expand(out)

def euler(L):
    out=s.diff(L,phi)
    for i in range(4):
        out-=D(s.diff(L,pv[i]),i)
        out+=D(D(s.diff(L,pp[i,i]),i),i)
    return s.expand(out)

exp2=s.exp(2*phi)
# Standard conformal curvature formula used as input; this calculation checks its
# local variational consequences, not its derivation from the Riemann tensor.
L=-f*(exp2*(R-6*boxphi-6*q)-2*Lambda*s.exp(4*phi))/(2*kappa)
expected=exp2/kappa*(-f*R+4*Lambda*f*exp2+6*f*boxphi+6*f*q+6*cross+3*boxf)
checks=[];negatives=[]
def check(name,expr):
    assert s.simplify(expr)==0,name
    checks.append(dict(name=name,passed=True))
def reject(name,expr):
    assert s.simplify(expr)!=0,name
    negatives.append(dict(name=name,detected=True))

EL=euler(L)
check('covariant_Euler_contact_in_four_Lorentzian_jets',EL-expected)
Lparts=-(f*R*exp2+6*f*exp2*q+6*exp2*cross-2*Lambda*f*s.exp(4*phi))/(2*kappa)
check('integration_by_parts_preserves_contact_if_cutoff_retained',euler(Lparts)-EL)
Ldrop=-(f*R*exp2+6*f*exp2*q-2*Lambda*f*s.exp(4*phi))/(2*kappa)
check('exact_error_if_cutoff_cross_term_is_dropped',EL-euler(Ldrop)-3*exp2*boxf/kappa)
reject('discarding_cutoff_cross_term_changes_contact',EL-euler(Ldrop))
reject('kinetic_sign_mutation',euler(L+6*f*exp2*q/kappa)-EL)
shell={R:12*K,Lambda:3*K}
zero={phi:0,**{x:0 for x in pv},**{x:0 for x in pp.values()}}
check('background_localized_contact_is_not_zero',EL.subs(shell).subs(zero)-3*boxf/kappa)
reject('localized_on_shell_action_is_not_stationary_for_variable_cutoff',EL.subs(shell).subs(zero))
constantcut={**{x:0 for x in fv},**{x:0 for x in ff.values()}}
check('constant_cutoff_on_shell_background_contact_zero',EL.subs(shell).subs(zero).subs(constantcut))

field_jets=[phi,*pv,*pp.values()]
scale={x:eps*x for x in field_jets}
polynomial=s.series(L.subs(shell).subs(scale,simultaneous=True),eps,0,9).removeO().expand()
V8=s.Add(*(polynomial.coeff(eps,n) for n in range(3,9)))
expected_series=s.series(expected.subs(shell).subs(scale,simultaneous=True),eps,0,8).removeO().expand()
expectedV=s.Add(*(expected_series.coeff(eps,n) for n in range(2,8)))
check('vary_cubic_to_octic_interaction_equals_contact_degrees_two_to_seven',euler(V8)-expectedV)
for n in range(3,9):
    check(f'action_degree_{n}_contact_degree_{n-1}',euler(polynomial.coeff(eps,n))-expected_series.coeff(eps,n-1))
background_removed=expected_series.coeff(eps,0)+expected_series.coeff(eps,1)
reject('full_contact_mistaken_for_interaction_contact',background_removed)
drop_poly=s.series(Ldrop.subs(shell).subs(scale,simultaneous=True),eps,0,9).removeO().expand()
dropV=s.Add(*(drop_poly.coeff(eps,n) for n in range(3,9)))
remaining_error=3*boxf/kappa*sum((2*phi)**n/s.factorial(n) for n in range(2,8))
check('cutoff_error_survives_subtraction_of_free_action',euler(V8)-euler(dropV)-remaining_error)
reject('cutoff_error_does_not_disappear_in_interaction',remaining_error)
result=dict(statute='REAL_EXACT_CAS_OF_DERIVED_METRIC_PULLBACK_CONTACT',
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    sympy_version=s.__version__,checks=checks,negative_controls=negatives,
    checks_passed=len(checks),negative_controls_detected=len(negatives),
    contact_closed_form=str(s.factor(expected)),
    restricted_action_interaction_through_degree8=str(V8),
    quantum_anomaly_computed=False,complete_temporal_prescription=False,
    field_redefinition_in_quantum_measure_claimed=False,
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:result[k] for k in ['statute','checks_passed','negative_controls_detected','wall_seconds','cpu_seconds']},ensure_ascii=False))
