"""Independent Feynman parameter and polynomial Ward checks after slot correction."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from metric_principal_vertices import basis,eh_cubic_16k,clear_caches
from one_loop_scale_engine import q,log_coefficient,ANGULAR_FACTOR

HERE=Path(__file__).resolve().parent;DEST=HERE/'metric_bubble_independent'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),result_sha256=sha(HERE/'metric_bubble_v2/results.json'),
    controls=['Dirichlet angular moments and Feynman parameters independent of radial recurrence',
              'nonaxis external momentum and dense polarizations',
              'symbolic single longitudinal tensor identity for arbitrary momenta',
              'quadratic linearized curvature form, no nonlinear covariant action inferred'],
    gate_changed=False))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,a,b=0):
    assert s.expand(a-b)==0,(name,a,b);checks.append(name)
def reject(name,a):
    assert s.expand(a)!=0,name;neg.append(name)
bs=[basis(i,j) for i in range(4) for j in range(i,4)]
labels=[(i,j) for i in range(4) for j in range(i,4)]
S=s.Matrix(10,10,lambda a,b:sum(bs[a][k]*bs[b][k] for k in range(16))
    -s.Rational(1,2)*sum(bs[a][5*k] for k in range(4))*sum(bs[b][5*k] for k in range(4))).inv()
zero=(0,0,0,0);axes=[tuple(int(i==j) for j in range(4)) for i in range(4)]
mons=[s.S.One]+list(q)+[x*x for x in q]+[q[i]*q[j] for i in range(4) for j in range(i+1,4)]
def coefficients(H,p):
    def W(k):return s.Matrix(10,10,lambda i,j:eh_cubic_16k(H,p,bs[i],k,bs[j],tuple(-p[a]-k[a] for a in range(4))))
    c=W(zero);plus=[W(e) for e in axes];minus=[W(tuple(-x for x in e)) for e in axes]
    cs=[c]+[(plus[i]-minus[i])/2 for i in range(4)]+[(plus[i]+minus[i])/2-c for i in range(4)]
    cs += [W(tuple(axes[i][k]+axes[j][k] for k in range(4)))-plus[i]-plus[j]+c
           for i in range(4) for j in range(i+1,4)]
    clear_caches();return cs
def numerator(ca,cb):
    expr=0
    for m,A in zip(mons,ca):
        transformed=S*A*S
        for n,B in zip(mons,cb):
            expr+=sum(transformed[i,j]*B[i,j] for i in range(10) for j in range(10))*m*n/16
    return s.expand(expr)
def fp(num,p):
    # Derivation: combine denominators, q=l-xp, Delta=x(1-x)p².
    # Radial integral: log coefficient for l^(2r)/(l²+Delta)² is (-1)^r(r+1)Delta^r.
    # Independent moments from Dirichlet(1/2,1/2,1/2,1/2).
    x=s.symbols('x');shifted=s.expand(num.subs({q[i]:q[i]-x*p[i] for i in range(4)},simultaneous=True))
    delta=x*(1-x)*sum(v*v for v in p);acc=0
    for powers,c in s.Poly(shifted,*q).terms():
        if any(v%2 for v in powers):continue
        r=sum(powers)//2
        avg=s.prod(s.gamma(s.Rational(1,2)+v//2)/s.gamma(s.Rational(1,2)) for v in powers)/s.gamma(2+r)
        acc+=c*avg*(-1)**r*(r+1)*delta**r
    return s.integrate(s.expand(acc),(x,0,1))
def inv(A,B,p):
    p=s.Matrix(p);p2=p.dot(p);a=(p.T*A*p)[0];b=(p.T*B*p)[0]
    return [s.trace(A*B)*p2**2,s.trace(A)*s.trace(B)*p2**2,
            (a*s.trace(B)+b*s.trace(A))*p2,(p.T*A*B*p)[0]*p2,a*b]
result=json.loads((HERE/'metric_bubble_v2/results.json').read_bytes())
metric=list(map(s.sympify,result['metric_coefficients_over_A0']))
ghost=list(map(s.sympify,result['ghost_coefficients_over_A0']))
total=list(map(s.sympify,result['combined_Hessian_coefficients_over_hbar_A0']))
lookup={x:i for i,x in enumerate(labels)}
p=(1,0,0,0)
pairs=[((1,2),(1,2)),((1,1),(2,2)),((0,0),(1,1)),((0,1),(0,1)),((0,0),(0,0))]
cache={}
for pair in pairs:
    for label in pair:
        if label not in cache:cache[label]=coefficients(bs[lookup[label]],p)
for index,(a,b) in enumerate(pairs):
    num=numerator(cache[a],cache[b])
    A=s.Matrix(4,4,bs[lookup[a]]);B=s.Matrix(4,4,bs[lookup[b]])
    expected=sum(c*v for c,v in zip(metric,inv(A,B,p)))
    check(f'Feynman_parameters_metric_{index}',fp(num,p),expected)

A=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
B=s.Matrix([[2,-1,1,0],[-1,0,2,1],[1,2,3,-2],[0,1,-2,1]])
p=(1,2,-1,1)
num=numerator(coefficients(tuple(A),p),coefficients(tuple(B),p))
expected=sum(c*v for c,v in zip(metric,inv(A,B,p)))
check('nonaxis_dense_Feynman_parameters',fp(num,p),expected)
check('nonaxis_dense_radial',log_coefficient(num,[zero,p],[0,0])/ANGULAR_FACTOR,expected)

pp=s.Matrix(s.symbols('p0:4'));v=s.Matrix(s.symbols('v0:4'))
H=s.zeros(4)
for index,(i,j) in enumerate(labels):H[i,j]=H[j,i]=s.Symbol(f'h{index}')
K=pp*v.T+v*pp.T
check('single_longitudinal_identity_all_p_v_H',sum(c*x for c,x in zip(total,inv(K,H,pp))))
reject('metric_alone_not_transverse',sum(c*x for c,x in zip(metric,inv(K,H,pp))))
reject('ghost_alone_not_transverse',sum(c*x for c,x in zip(ghost,inv(K,H,pp))))
reject('relative_loop_sign_changes_Ward',sum((m/2+g)*x for m,g,x in zip(metric,ghost,inv(K,H,pp))))

def ric(A,p):return (p.dot(p)*A+(p*p.T)*s.trace(A)-p*(A*p).T-(A*p)*p.T)/2
def scalar(A,p):return p.dot(p)*s.trace(A)-(p.T*A*p)[0]
# Arbitrary H, B dense and arbitrary p: bilinear curvature identity.
curvature=-s.Rational(61,30)*s.trace(ric(H,pp)*ric(B,pp))+s.Rational(19,60)*scalar(H,pp)*scalar(B,pp)
check('linearized_curvature_bilinear',sum(c*x for c,x in zip(total,inv(H,B,pp))),curvature)
new(DEST/'results.json',dict(statute='REAL_INDEPENDENT_PRINCIPAL_BUBBLE_CHECK',
    checks_passed=len(checks),checks=checks,negative_controls=neg,
    new_direction_value_over_A0=str(expected),
    coefficients_over_A0=list(map(str,metric)),
    transverse_coefficients_over_hbar_A0=list(map(str,total)),
    linearized_curvature_coefficients=['-61/30','19/60'],
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    full_curved_ward=False,full_quantum_anomaly_computed=False,gate_changed=False))
print(json.dumps(dict(checks=len(checks),negative_controls=len(neg),
    new_direction_value=str(expected),single_longitudinal_identity=True,
    wall_seconds=perf_counter()-start),ensure_ascii=False))
