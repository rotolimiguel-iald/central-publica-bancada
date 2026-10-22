"""Unweighted one-loop c* c c triangle in the principal tangent model."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from one_loop_scale_engine import q,ANGULAR_FACTOR,log_coefficient
HERE=Path(__file__).resolve().parent;DEST=HERE/'ghost_antifield_triangle';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'one_loop_scale_engine.py'),
    vertices='c* c.partial c, +barc C(L_c h), +barc C(L_c h)',
    external='c*(-p-r)=Y, c(p)=v, c(r)=w',
    internal='metric q, ghosts k=q+p and l=r-q',
    numerator='sum Sij [(l.V_i(q,p)v)*(Y.V_j(-q,r)w) -(Y.V_i(q,p)v)*(k.V_j(-q,r)w)]',
    denominator='q²(q+p)²(q-r)²',
    convention='i from source,4kappa from metric propagator, Grassmann/action weights excluded',
    comparison='Compare with local ghost-coordinate-change bracket; no equality assumed',
    controls=['external odd-leg exchange','independent simplex Feynman parameterization'],
    full_Q2=False,gate_changed=False))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,expr):
    assert s.expand(expr)==0,(name,expr);checks.append(name)
def reject(name,expr):
    assert s.expand(expr)!=0,name;neg.append(name)
bs=[]
for i in range(4):
    for j in range(i,4):
        H=s.zeros(4);H[i,j]=H[j,i]=1;bs.append(H)
S=s.Matrix(10,10,lambda i,j:s.trace(bs[i]*bs[j])-s.trace(bs[i])*s.trace(bs[j])/2).inv()
def V(H,k,l):
    r=k+l
    return s.Matrix(4,4,lambda nu,rho:s.expand(-(
        k[rho]*(H*r)[nu]+r.dot(l)*H[rho,nu]+l[nu]*(H*r)[rho]
        -r[nu]*k[rho]*s.trace(H)/2-r[nu]*(H*l)[rho])))
def num(Y,v,w,p,r):
    qq=s.Matrix(q);k=qq+p;l=r-qq
    left=[V(H,qq,p)*v for H in bs];right=[V(H,-qq,r)*w for H in bs]
    return s.expand(sum(S[i,j]*(l.dot(left[i])*Y.dot(right[j])-Y.dot(left[i])*k.dot(right[j]))
        for i in range(10) for j in range(10)))
def pole(n,p,r):return s.cancel(log_coefficient(n,[(0,0,0,0),tuple(p),tuple(-r)],[0,0,0])/ANGULAR_FACTOR)
def fp(n,p,r):
    x,y=s.symbols('x y');shift=x*p-y*r
    expr=s.expand(n.subs({q[i]:q[i]-shift[i] for i in range(4)},simultaneous=True))
    delta=x*p.dot(p)+y*r.dot(r)-shift.dot(shift);total=0
    for exps,c in s.Poly(expr,*q).terms():
        if any(a%2 for a in exps):continue
        a=sum(exps)//2
        if a<1:continue
        avg=s.prod(s.gamma(s.Rational(1,2)+v//2)/s.gamma(s.Rational(1,2)) for v in exps)/s.gamma(2+a)
        total+=2*c*avg*(-1)**(a-1)*s.binomial(a+1,2)*delta**(a-1)
    return s.integrate(s.integrate(s.expand(total),(y,0,1-x)),(x,0,1))
def F(p,v):return -s.Rational(3,8)*p.dot(p)*v+s.Rational(1,4)*p*p.dot(v)
def bracket(p,v,r,w):return v.dot(r)*w-w.dot(p)*v
def coord(p,v,r,w):return bracket(p,F(p,v),r,w)+bracket(p,v,r,F(r,w))-F(p+r,bracket(p,v,r,w))
axes=[s.eye(4)[:,i] for i in range(4)]
p=s.Matrix([1,0,0,0]);r=s.Matrix([0,1,0,0]);cases=[]
for index,(yi,vi,wi) in enumerate([(0,0,1),(0,1,0),(1,0,0),(2,2,1),(0,2,2),(3,3,0)]):
    Y,v,w=axes[yi],axes[vi],axes[wi]
    n=num(Y,v,w,p,r);value=pole(n,p,r)
    check(f'Feynman_simplex_{index}',value-fp(n,p,r))
    exchanged=num(Y,w,v,r,p)
    check(f'odd_external_exchange_numerator_{index}',n+exchanged.subs({q[i]:-q[i] for i in range(4)},simultaneous=True))
    check(f'odd_external_exchange_pole_{index}',value+pole(exchanged,r,p))
    candidate=(Y.T*coord(p,v,r,w))[0]
    cases.append(dict(case=[yi,vi,wi],value=str(value),coordinate_candidate=str(candidate)))

# A fully nonaxis test independent of the fitted/axis polarizations.
p1=s.Matrix([1,2,-1,1]);r1=s.Matrix([-1,0,1,2])
Y=s.Matrix([1,-1,2,0]);v=s.Matrix([2,0,1,-1]);w=s.Matrix([-1,2,0,1])
n=num(Y,v,w,p1,r1);value=pole(n,p1,r1)
check('nonaxis_Feynman_simplex',value-fp(n,p1,r1))
check('nonaxis_odd_exchange',value+pole(num(Y,w,v,r1,p1),r1,p1))
cases.append(dict(case='nonaxis',value=str(value),coordinate_candidate=str((Y.T*coord(p1,v,r1,w))[0])))
reject('triangle_erased',value)
# Determine, rather than assume, whether one scalar multiple explains these cases.
ratios=[s.sympify(c['value'])/s.sympify(c['coordinate_candidate']) for c in cases if s.sympify(c['coordinate_candidate'])!=0]
ratio=ratios[0] if ratios else None
matches=ratio is not None and all(s.sympify(c['value'])==ratio*s.sympify(c['coordinate_candidate']) for c in cases)
result=dict(statute='REAL_CSTAR_CC_TRIANGLE_UNWEIGHTED_PRINCIPAL_LOG',
    cases=cases,constant_multiple_of_coordinate_candidate_on_tested_cases=matches,
    first_ratio=str(ratio),checks_passed=len(checks),checks=checks,negative_controls=neg,
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    overall_Grassmann_Wick_effective_sign_applied=False,full_Q2=False,gate_changed=False)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False),flush=True)
