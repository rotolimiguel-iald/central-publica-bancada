"""Principal four-derivative ghost bubble from the actual linear de Donder gauge.

Computes the unweighted Euclidean numerator trace integral. Closed-ghost sign,
Wick factors and action-effective normalization remain separate, as preregistered.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from one_loop_scale_engine import q,n,ANGULAR_FACTOR,sphere_average_monomial,log_coefficient

HERE=Path(__file__).resolve().parent
DEST=HERE/'ghost_bubble'
DEST.mkdir(exist_ok=True)
BV=HERE.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists() and b,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'one_loop_scale_engine.py'),
    bv_source_sha256=sha(BV),bv_source=str(BV),
    convention='Euclidean principal symbol, Fourier exp(+ikx), real symmetric external polarizations',
    interaction='barc*C(L_c h), plus sign in BV069 section4',
    vertex='V_nu,rho(H,p,k)=-(p_rho*((k+p)^T H)_nu+((k+p).k)*H_rho,nu+k_nu*((k+p)^T H)_rho-((k+p)_nu*p_rho/2)*trH-(k+p)_nu*(k^T H)_rho)',
    numerator='trace[V(B,-p,q+p) V(A,p,q)]',
    denominator='q^2*(q+p)^2, leading flat symbol only',
    target='logarithmic coefficient of principal order p^4 ghost bubble, not full self-energy or BRST anomaly',
    before_computation=['Do not apply closed ghost-loop sign, symmetry factor or Wick i*hbar here',
        'Fix two-vertex trace and momentum routing as written; no fitting after Ward',
        'Determine five covariant tensor coefficients then validate all symmetric basis pairs',
        'Compare independent Feynman-parameter angular integral'],
    quantum_anomaly_computed=False,gate_changed=False))
start,cpu=perf_counter(),process_time()
checks=[];neg=[]
def check(name,expr):
    if isinstance(expr,s.MatrixBase):ok=all(s.simplify(x)==0 for x in expr)
    else:ok=s.simplify(expr)==0
    assert ok,name;checks.append(dict(name=name,passed=True))
def reject(name,expr):
    assert s.simplify(expr)!=0,name;neg.append(dict(name=name,detected=True))

def V(H,p,k):
    p,k=s.Matrix(p),s.Matrix(k);r=k+p
    return s.Matrix(4,4,lambda nu,rho:s.expand(-(
        p[rho]*(H*r)[nu]+r.dot(k)*H[rho,nu]+k[nu]*(H*r)[rho]
        -r[nu]*p[rho]*s.trace(H)/2-r[nu]*(H*k)[rho])))
def V_from_Lie(H,p,k):
    """Independent index construction: first Lie derivative, then C."""
    p,k=s.Matrix(p),s.Matrix(k);out=k+p;result=s.zeros(4)
    for rho in range(4):
        lie=s.Matrix(4,4,lambda a,b:s.I*(p[rho]*H[a,b]+k[a]*H[rho,b]+k[b]*H[a,rho]))
        for nu in range(4):
            result[nu,rho]=s.expand(s.I*sum(out[a]*lie[a,nu] for a in range(4))-s.I*out[nu]*s.trace(lie)/2)
    return result
def numerator(H,J,p):
    pp=s.Matrix(p);qq=s.Matrix(q)
    return s.expand(s.trace(V(J,-pp,qq+pp)*V(H,pp,qq)))
def pole(H,J,p):
    return s.factor(log_coefficient(numerator(H,J,p),[(0,0,0,0),tuple(p)],[0,0])/ANGULAR_FACTOR)
def invariants(H,J,p):
    p=s.Matrix(p);pp=p.dot(p);hp=(p.T*H*p)[0];jp=(p.T*J*p)[0]
    return [s.trace(H*J)*pp**2,s.trace(H)*s.trace(J)*pp**2,
        (hp*s.trace(J)+jp*s.trace(H))*pp,(p.T*H*J*p)[0]*pp,hp*jp]
def fp_pole(H,J,p):
    """Independent Feynman parameterization and shifted loop variable."""
    x=s.symbols('x',real=True);pp=s.Matrix(p)
    expr=numerator(H,J,p).subs({q[i]:q[i]-x*pp[i] for i in range(4)},simultaneous=True)
    poly=s.Poly(s.expand(expr),*q);Delta=x*(1-x)*pp.dot(pp)
    acc=0
    for exps,c in poly.terms():
        j=sum(exps)
        if j%2==0:
            acc+=c*sphere_average_monomial(exps)*(-1)**(j//2)*(j//2+1)*Delta**(j//2)
    return s.simplify(s.integrate(s.expand(acc),(x,0,1)))
def basis(i,j):
    H=s.zeros(4);H[i,j]=1;H[j,i]=1;return H
p0=(1,0,0,0)
units={(i,j):basis(i,j) for i in range(4) for j in range(i,4)}
H=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
pv=s.symbols('p0:4');kv=s.symbols('k0:4')
check('vertex_is_C_of_Lie_derivative',V(H,pv,kv)-V_from_Lie(H,pv,kv))
check('constant_metric_vertex',V(H,(0,0,0,0),kv)+sum(x*x for x in kv)*H)

chosen=[((1,2),(1,2)),((1,1),(2,2)),((0,0),(1,1)),((0,1),(0,1)),((0,0),(0,0))]
matrix=[];values=[]
for i,(left,right) in enumerate(chosen):
    H,J=units[left],units[right]
    value=pole(H,J,p0);values.append(value);matrix.append(invariants(H,J,p0))
    check(f'independent_Feynman_parameter_case_{i}',value-fp_pole(H,J,p0))
coef=s.Matrix(matrix).inv()*s.Matrix(values)

# Complete bilinear-basis verification at one nonzero p. O(4) covariance and
# homogeneity then extend the result to arbitrary p; separately test a new direction.
keys=list(units)
for i,left in enumerate(keys):
    for right in keys[i:]:
        H,J=units[left],units[right]
        predicted=sum(a*b for a,b in zip(coef,invariants(H,J,p0)))
        check('basis_'+str(left)+'_'+str(right),pole(H,J,p0)-predicted)
H=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
J=s.Matrix([[2,-1,1,0],[-1,0,2,1],[1,2,3,-2],[0,1,-2,1]])
p1=(1,2,-1,1)
pred=sum(a*b for a,b in zip(coef,invariants(H,J,p1)))
check('independent_external_momentum_direction',pole(H,J,p1)-pred)
check('external_polarization_exchange',pole(H,J,p1)-pole(J,H,tuple(-v for v in p1)))
check('zero_external_momentum_has_no_log',pole(H,J,(0,0,0,0)))

longitudinal=pole(units[(0,0)],units[(0,0)],p0)
reject('isolated_ghost_bubble_assumed_transverse',longitudinal)
reject('ghosts_treated_as_four_independent_scalar_vertices',
    pole(units[(1,2)],units[(1,2)],p0))
reject('wrong_sign_of_trace_reversal_term',
    V(H,pv,kv)[0,0]-(V(H,pv,kv)[0,0]- (s.Matrix(kv)+s.Matrix(pv))[0]*pv[0]*s.trace(H)))

new(DEST/'results.json',dict(statute='REAL_PRINCIPAL_GHOST_BUBBLE_COEFFICIENT_UNWEIGHTED',
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'one_loop_scale_engine.py'),
    plan_sha256=sha(DEST/'PRE_REGISTER.json'),checks=checks,negative_controls=neg,
    checks_passed=len(checks),negative_controls_detected=len(neg),
    invariant_order=['trAB*p4','trA*trB*p4','(pAp*trB+pBp*trA)*p2','pABp*p2','pAp*pBp'],
    coefficients_over_angular_factor=[str(v) for v in coef],
    angular_factor=str(ANGULAR_FACTOR),fit_values=[str(v) for v in values],
    longitudinal_component_over_angular_factor=str(longitudinal),
    sympy_version=s.__version__,wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    ghost_loop_sign_and_effective_action_factor_applied=False,
    curvature_terms_computed=False,full_metric_sector_computed=False,
    quantum_anomaly_computed=False,gate_changed=False))
print(json.dumps(dict(checks=len(checks),negative_controls=len(neg),
    coefficients=[str(v) for v in coef],scope='principal_ghost_bubble_unweighted'),ensure_ascii=False))
