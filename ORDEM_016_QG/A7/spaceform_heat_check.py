"""Derive the local traced heat coefficient from radial transport, not import it."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'spaceform_heat';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),curvature_result_sha256=sha(HERE/'connection_curvature/results.json'),
    model_sha256=sha(HERE/'model_inputs/DERIVACAO_OPERADORES.md'),
    prescription='Local Euclidean heat symbol D=-(nabla^2+E), diagonal asymptotic; not a new Lorentz state',
    derivation='Scalar radial transport in spaceform + radial gauge connection + parallel E exponential',
    target='tr a4 for S2,T*, and 1/2 S2 minus T*, fixed on-shell background K',
    excluded='off-shell metric Hessian of effective action; finite causal anomaly; global heat trace/zero modes',
    no_universal_a4_formula_used_as_input=True,full_Q2=False))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,expr):
    if isinstance(expr,s.MatrixBase):ok=all(s.simplify(v)==0 for v in expr)
    else:ok=s.simplify(expr)==0
    assert ok,(name,expr);checks.append(name)
def reject(name,expr):
    assert s.simplify(expr)!=0,name;neg.append(name)
r,t=s.symbols('r t',positive=True);K=s.symbols('K',positive=True)
f=s.sin(s.sqrt(K)*r)/s.sqrt(K);Ar=3*s.diff(f,r)/f
u=s.Function('u')(t,r);Ar_generic=s.Function('Ar')(r)
pref=t**-2*s.exp(-r*r/(4*t))
direct=(s.diff(pref*u,t)-s.diff(pref*u,r,2)-Ar_generic*s.diff(pref*u,r))/pref
derived=s.diff(u,t)-s.diff(u,r,2)-Ar_generic*s.diff(u,r)+r*s.diff(u,r)/t+(Ar_generic*r-3)*u/(2*t)
check('transport_from_heat_PDE',s.expand(direct-derived))
u0=s.series((r/f)**s.Rational(3,2),r,0,7).removeO()
def lap(expr):return s.diff(expr,r,2)+Ar*s.diff(expr,r)
u0_exact=(r/f)**s.Rational(3,2)
# For the truncated series the transport residual has no terms through r4.
check('u0_transport_to_required_order',s.series(r*s.diff(u0,r)+(Ar*r-3)*u0/2,r,0,6).removeO())
rhs=s.series(lap(u0)/u0,r,0,3).removeO()
a1=sum(coef*r**e[0]/(e[0]+1) for e,coef in s.Poly(rhs,r).terms())
u1=s.series(u0*a1,r,0,3).removeO()
check('a1_transport',s.expand(r*s.diff(a1,r)+a1-rhs))
scalar_a2=u1.subs(r,0)
scalar_a4=s.limit(lap(u1)/2,r,0)
check('scalar_first_coefficient',scalar_a2-2*K)
check('scalar_second_coefficient',scalar_a4-s.Rational(29,15)*K**2)

# Only the traced connection contribution is asserted. In an orthonormal
# radial frame tr A_mu=0, x^mu A_mu=0; to quadratic order A_mu=1/2 x^nu Omega_nu,mu.
# Therefore tr(u1_connection)=tr(sum A_mu^2)/3 and tr(u2_connection)=Delta/6 of that.
xx=s.symbols('x0:4');I=s.eye(4)
labels=[(i,j) for i in range(4) for j in range(i,4)]
basis=[]
for i,j in labels:
    H=s.zeros(4);H[i,j]=H[j,i]=1;basis.append(H)
tracevec=s.Matrix([int(i==j) for i,j in labels])
Em=-2*K*s.eye(10)+2*K*tracevec*tracevec.T;Eg=3*K*I
def omega(nu,mu):
    om=s.zeros(4)
    if mu!=nu:om[nu,mu]=K;om[mu,nu]=-K
    return om
def induced(om):
    ims=[om*H+H*om.T for H in basis]
    return s.Matrix(10,10,lambda a,b:ims[b][labels[a][0],labels[a][1]])
connection={}
for label,rank,endom,rep in [('metric',10,Em,induced),('ghost',4,Eg,lambda om:om)]:
    aa=[sum((xx[nu]*rep(omega(nu,mu))/2 for nu in range(4)),s.zeros(rank)) for mu in range(4)]
    check(label+'_radial_gauge',sum((xx[mu]*aa[mu] for mu in range(4)),s.zeros(rank)))
    for mu,A in enumerate(aa):
        check(label+f'_trace_connection_{mu}',s.trace(A))
        check(label+f'_parallel_E_commutation_{mu}',endom*A-A*endom)
    potential=sum(s.trace(A*A) for A in aa)
    value=s.expand(sum(s.diff(potential,x,2) for x in xx)/6)
    omega_trace=sum(s.trace(rep(omega(nu,mu))**2) for nu in range(4) for mu in range(4))
    check(label+'_connection_transport',value-omega_trace/12)
    connection[label]=value
old=json.loads((HERE/'connection_curvature/results.json').read_bytes())
check('metric_connection_previous_trace',connection['metric']-s.sympify(old['trace_Omega2_symmetric'],locals={'K':K})/12)
check('ghost_connection_previous_trace',connection['ghost']-s.sympify(old['trace_Omega2_vector'],locals={'K':K})/12)
metric_a4=s.expand(10*scalar_a4+scalar_a2*s.trace(Em)+s.trace(Em*Em)/2+connection['metric'])
ghost_a4=s.expand(4*scalar_a4+scalar_a2*s.trace(Eg)+s.trace(Eg*Eg)/2+connection['ghost'])
metric_series=s.series((1+t*scalar_a2+t*t*scalar_a4)*(9*s.exp(-2*K*t)+s.exp(6*K*t)),t,0,3).removeO()+t*t*connection['metric']
ghost_series=s.series((1+t*scalar_a2+t*t*scalar_a4)*4*s.exp(3*K*t),t,0,3).removeO()+t*t*connection['ghost']
check('metric_parallel_endomorphism_spectral_check',metric_series.coeff(t,2)-metric_a4)
check('ghost_parallel_endomorphism_spectral_check',ghost_series.coeff(t,2)-ghost_a4)
weighted=s.expand(metric_a4/2-ghost_a4)
weighted_a2=s.expand((10*scalar_a2+s.trace(Em))/2-(4*scalar_a2+s.trace(Eg)))
reject('discard_connection_contribution',connection['metric']/2-connection['ghost'])
reject('opposite_endomorphism_sign',-2*scalar_a2*(s.trace(Em)/2-s.trace(Eg)))
reject('incorrect_determinant_ghost_weight',metric_a4/2+ghost_a4-weighted)
result=dict(statute='DERIVED_LOCAL_FREE_SPACEFORM_HEAT_TRACE_WITH_EXACT_CAS',
    convention='D=-(nabla²+E); H_E=(Itr/4kappa)D_metric,Q_E=-D_ghost; only minimal-operator heat traces',
    scalar_u0=str(u0),scalar_a1_reduced=str(a1),scalar_a2=str(scalar_a2),scalar_a4=str(scalar_a4),
    metric_connection_a4=str(connection['metric']),ghost_connection_a4=str(connection['ghost']),
    metric_a4=str(metric_a4),ghost_a4=str(ghost_a4),half_metric_minus_ghost_a4=str(weighted),
    half_metric_minus_ghost_a2=str(weighted_a2),weighted_rank=1,
    checks_passed=len(checks),checks=checks,negative_controls=neg,
    full_Q2=False,curved_self_energy_computed=False,gate_changed=False,
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='checks'}),flush=True)
