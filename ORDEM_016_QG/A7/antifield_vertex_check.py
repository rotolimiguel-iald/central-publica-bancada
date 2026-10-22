"""One-loop principal h* c insertion and antighost consistency, exact algebra."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from one_loop_scale_engine import q,log_coefficient,ANGULAR_FACTOR

HERE=Path(__file__).resolve().parent;DEST=HERE/'antifield_vertex';DEST.mkdir(exist_ok=True)
BV=HERE.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),bv_source_sha256=sha(BV),
    engine_sha256=sha(HERE/'one_loop_scale_engine.py'),
    diagram='external h*(-p),c(p); source h*(L_c h) at metric q and ghost p-q; ghost vertex at metric -q and external c(p)',
    numerator='sum_ij,m U_m(T,E_i,q,p-q) S0_ij V_m,rho(E_j,-q,p) v_rho',
    source_vertex='physical vertex i*U, U_m=k_m tr(T H)+2(H T l)_m',
    denominator='q²*(q-p)²',
    extracted='unweighted principal logarithmic kernel only; -4i*kappa from free inverses and source phase kept separate from Grassmann/effective action convention',
    expectation='three O4 covariant rank3 structures, do NOT assume pure gauge',
    excluded='curvature, finite terms, cutoff, full QME, full anomaly ghost1/form4'))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,value):
    ok=all(s.expand(x)==0 for x in value) if isinstance(value,s.MatrixBase) else s.expand(value)==0
    assert ok,(name,value);checks.append(name)
def reject(name,value):
    assert s.expand(value)!=0,name;neg.append(name)
labels=[(i,j) for i in range(4) for j in range(i,4)];bs=[]
for i,j in labels:
    H=s.zeros(4);H[i,j]=H[j,i]=1;bs.append(H)
S=s.Matrix(10,10,lambda i,j:s.trace(bs[i]*bs[j])-s.trace(bs[i])*s.trace(bs[j])/2).inv()
def U(T,H,k,l):
    k,l=s.Matrix(k),s.Matrix(l)
    return k*s.trace(T*H)+2*H*T*l
def V(H,k,l):
    k,l=s.Matrix(k),s.Matrix(l);r=k+l
    return s.Matrix(4,4,lambda nu,rho:s.expand(-(
        k[rho]*(H*r)[nu]+r.dot(l)*H[rho,nu]+l[nu]*(H*r)[rho]
        -r[nu]*k[rho]*s.trace(H)/2-r[nu]*(H*l)[rho])))
def numerator(T,v,p):
    p,v,qq=s.Matrix(p),s.Matrix(v),s.Matrix(q)
    us=[U(T,H,qq,p-qq) for H in bs]
    vs=[V(H,-qq,p)*v for H in bs]
    return s.expand(sum(S[i,j]*us[i].dot(vs[j]) for i in range(10) for j in range(10)))
def pole(T,v,p):
    return s.cancel(log_coefficient(numerator(T,v,p),[(0,0,0,0),tuple(-x for x in p)],[0,0])/ANGULAR_FACTOR)
def invariants(T,v,p):
    p,v=s.Matrix(p),s.Matrix(v);p2=p.dot(p);pv=p.dot(v)
    return [2*p2*(v.T*T*p)[0],(p.T*T*p)[0]*pv,p2*s.trace(T)*pv]
axes=[s.eye(4)[:,i] for i in range(4)];p=axes[0]
lookup={pair:i for i,pair in enumerate(labels)}
fit=[(bs[lookup[(0,1)]],axes[1]),(bs[lookup[(1,1)]],axes[0]),(bs[lookup[(0,0)]],axes[0])]
M=s.Matrix([invariants(T,v,p) for T,v in fit]);assert M.det()!=0
values=s.Matrix([pole(T,v,p) for T,v in fit]);coefs=M.inv()*values
for a,T in enumerate(bs):
    for n,v in enumerate(axes):
        check(f'basis_source_{a}_{n}',pole(T,v,p)-sum(c*x for c,x in zip(coefs,invariants(T,v,p))))

T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
pp=s.Matrix([1,2,-1,1]);vv=s.Matrix([2,-1,1,3])
expected=sum(c*x for c,x in zip(coefs,invariants(T,vv,pp)))
check('nonaxis_dense_source',pole(T,vv,pp)-expected)

# Source pairing independently from Lie derivative before contraction with T.
k=s.Matrix(s.symbols('k0:4'));l=s.Matrix(s.symbols('l0:4'))
H=s.Matrix([[2,-1,1,0],[-1,0,2,1],[1,2,3,-2],[0,1,-2,1]])
direct=s.Matrix([sum(T[a,b]*(k[m]*H[a,b]+l[a]*H[m,b]+l[b]*H[a,m])
    for a in range(4) for b in range(4)) for m in range(4)])
check('source_is_Lie_pairing',U(T,H,k,l)-direct)
r=k+l
for nu,e in enumerate(axes):
    CT=(r*e.T+e*r.T)/2-r[nu]*s.eye(4)/2
    check(f'antighost_vertex_from_source_{nu}',U(CT,H,k,l)+V(H,k,l)[nu,:].T)

# Independent Feynman parameter integration, Dirichlet moments.
x=s.symbols('x')
num=numerator(T,vv,pp)
shift=s.expand(num.subs({q[i]:q[i]+x*pp[i] for i in range(4)},simultaneous=True))
delta=x*(1-x)*pp.dot(pp);acc=0
for exps,c in s.Poly(shift,*q).terms():
    if any(a%2 for a in exps):continue
    degree=sum(exps)//2
    avg=s.prod(s.gamma(s.Rational(1,2)+a//2)/s.gamma(s.Rational(1,2)) for a in exps)/s.gamma(2+degree)
    acc+=c*avg*(-1)**degree*(degree+1)*delta**degree
check('independent_Feynman_parameters',s.integrate(s.expand(acc),(x,0,1))-expected)

# Check the ungauged Einstein principal Hessian applied to the inferred source map.
P=s.Matrix(s.symbols('p0:4'));v=s.Matrix(s.symbols('v0:4'));p2=P.dot(P);pv=P.dot(v)
R=coefs[0]*p2*(P*v.T+v*P.T)+coefs[1]*P*P.T*pv+coefs[2]*p2*s.eye(4)*pv
ric=(p2*R+P*P.T*s.trace(R)-P*(R*P).T-(R*P)*P.T)/2
ein=ric-s.eye(4)*s.trace(ric)/2
ein_zero=all(s.expand(z)==0 for z in ein)
reject('source_loop_erased',values[0])
reject('source_as_scalar_trace_only',expected-coefs[2]*invariants(T,vv,pp)[2])
result=dict(statute='REAL_PRINCIPAL_ANTIFIELD_GHOST_KERNEL_UNWEIGHTED',
    coefficients_over_A0=list(map(str,coefs)),invariant_order=['2p²(v.Tp)','(p.Tp)(p.v)','p²trT(p.v)'],
    fit_values=list(map(str,values)),checks_passed=len(checks),checks=checks,negative_controls=neg,
    einstein_Hessian_of_source_zero=ein_zero,
    residual_Einstein_components=[[str(s.expand(ein[i,j])) for j in range(4)] for i in range(4)],
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    overall_Grassmann_Wick_effective_sign_applied=False,full_Q2=False,gate_changed=False)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','residual_Einstein_components']},ensure_ascii=False))
