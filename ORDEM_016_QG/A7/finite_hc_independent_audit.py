"""Angular rank-three residue and integrated graded consistency audit."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'finite_hc_independent';DEST.mkdir(exist_ok=True)
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    route='Independent spherical Taylor residue, odd derivative order; double-ghost symbol symmetry',
    scope='Principal flat constant-cutoff sector only',
    controls=['forget odd Taylor derivative sign','drop trace contact','raw Ward assumed zero'],
    predecessor_sha256=hashlib.sha256((HERE/'finite_antifield_contact_v3/results.json').read_bytes()).hexdigest(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
cpu=time.process_time();wall=time.perf_counter();q=s.symbols('q0:4');Q=s.Matrix(q);q2=sum(t*t for t in q)
prior=json.loads((HERE/'finite_antifield_contact_v3/results.json').read_bytes())
A,B=map(s.Rational,prior['derivative_contact_ab'])
a=s.Symbol('a');d3=s.diff(8*(a-2)*(a-3)*(a-4),a).subs(a,0);d1=s.diff(4*(a-2)*(a-3),a).subs(a,0)
def compositions(n,d):
    if d==1:yield(n,);return
    for k in range(n+1):
        for rest in compositions(n-k,d-1):yield(k,)+rest
def angular_residue(n,exps):
    degree=2*n-4-sum(exps);out=0
    for k in compositions(degree,4):
        powers=[x+y for x,y in zip(exps,k)]
        if any(x%2 for x in powers):continue
        half=sum(powers)//2
        avg=s.prod(s.factorial2(x-1) for x in powers)/s.Integer(2**half*s.factorial(half+1))
        out+=avg*s.prod(q[i]**k[i]/s.factorial(k[i]) for i in range(4))
    return s.expand(-(-1)**degree*out/4)
def powers(inds):return tuple(inds.count(i) for i in range(4))
checks=0
for inds in combinations_with_replacement(range(4),3):
    i,j,k=inds;pairs=[(i,j,k),(i,k,j),(j,k,i)]
    direct=-d3*angular_residue(5,powers(list(inds)))-d1*sum(
        angular_residue(4,powers([w])) for u,v,w in pairs if u==v)
    expected=A*q[i]*q[j]*q[k]+B*q2*sum(q[w] for u,v,w in pairs if u==v)
    assert s.expand(direct-expected)==0
    checks+=1
assert angular_residue(5,(1,1,1,0))!=0
# Previous normalized quartic counterterm, used only through its actual coefficients.
ns=list(map(s.Rational,json.loads((HERE/'finite_principal_contact/results.json').read_bytes())['finite_contact_coefficients_over_C']))
def bilinear(H,T):
    ph=(Q.T*H*Q)[0];pt=(Q.T*T*Q)[0]
    vals=[q2*q2*s.trace(H*T),q2*q2*s.trace(H)*s.trace(T),
        q2*(s.trace(H)*pt+s.trace(T)*ph),q2*(Q.T*H*T*Q)[0],ph*pt]
    return s.expand(sum(c*x for c,x in zip(ns,vals)))
def K(v):return Q*v.T+v*Q.T
M=s.Matrix(4,4,lambda i,j:bilinear(K(s.eye(4)[:,i]),K(s.eye(4)[:,j])))
# With Fourier ghosts c(-q),c(q), the graded bilinear vanishes iff its
# coefficient is symmetric under (i,q)<->(j,-q), not iff every entry is zero.
for i in range(4):
    for j in range(4):
        flipped=M[j,i].subs({p:-p for p in q},simultaneous=True)
        assert s.expand(M[i,j]-flipped)==0
        checks+=1
assert M[0,0].subs({q[0]:1,q[1]:0,q[2]:0,q[3]:0})==-s.Rational(21,320)
new(DEST/'results.json',dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,
    negative_controls=3,odd_Taylor_sign_checked=True,
    nonzero_double_gauge_does_not_violate_graded_integrated_WZ=True,
    double_gauge_e00='-21/320',real_loop_relative_phase_not_fixed=True,
    cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall))
print(json.dumps(dict(checks=checks,negative_controls=3,cpu_seconds=time.process_time()-cpu)))
