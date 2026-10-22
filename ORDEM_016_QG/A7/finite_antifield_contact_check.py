"""Rank-three extension contact and the finite principal hc Ward sector."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'finite_antifield_contact';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    b=json.dumps(o,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    prescription='Same R=FP[(1-a)mu^(2a)z^a *] on a single pair',
    target='Rank3 contact for R0=K F and hc combination with previously measured rank4 contact',
    conventions='Use polynomial symbols; retain an arbitrary lambda for unfixed relative global factors',
    controls=['omit trace contact in R0','cancel raw Ward by arbitrary relative normalization',
              'restore only the metric contact','reverse both local subtractions'],
    scope='Principal local flat hc, constant cutoff; not full curved causal anomaly',
    script_sha256=sha(Path(__file__)),
    source_sha256=sha(HERE/'antifield_vertex/results.json'),
    hessian_contact_sha256=sha(HERE/'finite_principal_contact/results.json')))
wall=time.perf_counter();cpu=time.process_time();a=s.Symbol('a');q=s.symbols('q0:4');Q=s.Matrix(q)
lam=s.Symbol('lambda');source=json.loads((HERE/'antifield_vertex/results.json').read_bytes())
rawcoef=list(map(s.Rational,source['coefficients_over_A0']))
assert rawcoef[2]==0
prior=json.loads((HERE/'finite_principal_contact/results.json').read_bytes())
n4=list(map(s.Rational,prior['finite_contact_coefficients_over_C']))
coeff3=s.diff(8*(a-2)*(a-3)*(a-4),a).subs(a,0)
coeff1=s.diff(4*(a-2)*(a-3),a).subs(a,0)
def powers(inds):return tuple(inds.count(i) for i in range(4))
def residue(n,powers,sgn):
    f=s.expand(sum(sgn[i]*q[i]**2 for i in range(4))**(n-2))
    for i,p in enumerate(powers):f=(-1)**p*s.diff(f,q[i],p)
    return -f/s.Integer(4**(n-1)*s.factorial(n-1)*s.factorial(n-2))
def tensor_contact(inds,sgn):
    i,j,k=inds
    pairs=[(i,j,k),(i,k,j),(j,k,i)]
    return s.expand(-coeff3*residue(5,powers(list(inds)),sgn)-coeff1*sum(
        sgn[u]*residue(4,powers([w]),sgn) for u,v,w in pairs if u==v))
aa,bb=s.symbols('aa bb');eqs=[]
for inds in [(0,1,2),(0,0,1)]:
    i,j,k=inds;q2=sum(x*x for x in q)
    expected=aa*q[i]*q[j]*q[k]+bb*q2*((i==j)*q[k]+(i==k)*q[j]+(j==k)*q[i])
    eqs+=s.Poly(tensor_contact(inds,(1,1,1,1))-expected,*q).coeffs()
sol=s.solve(eqs,[aa,bb],dict=True);assert len(sol)==1;aa,bb=sol[0][aa],sol[0][bb]
checks=[];source_coeff=None;examples=[]
def lap(f,sgn):return s.expand(sum(sgn[i]*s.diff(f,q[i],2) for i in range(4)))
for sgn in [(1,1,1,1),(1,-1,-1,-1)]:
    g=s.diag(*sgn);q2=(Q.T*g*Q)[0];signature='Euclidean' if sgn[1]==1 else 'Lorentz'
    for inds in combinations_with_replacement(range(4),3):
        i,j,k=inds
        expected=aa*q[i]*q[j]*q[k]+bb*q2*((sgn[i] if i==j else 0)*q[k]+
            (sgn[i] if i==k else 0)*q[j]+(sgn[j] if j==k else 0)*q[i])
        assert s.expand(tensor_contact(inds,sgn)-expected)==0
        checks.append(f'{signature}_rank3_{inds}')
    def tr(H):return s.trace(g*H)
    def itr(H):return H-g*tr(H)/2
    def K(v):
        vf=g*v;return Q*vf.T+vf*Q.T
    def C(H):return g*(itr(H)*g*Q)
    def E(H):return (q2*itr(H)-itr(K(C(H)))).applyfunc(s.expand)
    def paired(H,T):return s.trace(g*H*g*T)
    def pH(H):return (Q.T*g*H*g*Q)[0]
    def quartic(H,T,cs):
        vs=[q2*q2*paired(H,T),q2*q2*tr(H)*tr(T),q2*(tr(H)*pH(T)+tr(T)*pH(H)),
            q2*(Q.T*g*H*g*T*g*Q)[0],pH(H)*pH(T)]
        return s.expand(sum(c*v for c,v in zip(cs,vs)))
    for k in range(4):
        v=s.eye(4)[:,k];pv=(Q.T*v)[0]
        R=rawcoef[0]*q2*K(v)+rawcoef[1]*(Q*Q.T)*pv
        assert E(R)==s.zeros(4)
        N=R.applyfunc(lambda f:s.expand(aa*f+bb*q2*lap(f,sgn)/2))
        nc=(s.expand(aa*rawcoef[0]-s.Rational(7,4)*bb),
            s.expand(aa*rawcoef[1]),bb/2)
        guess=nc[0]*q2*K(v)+nc[1]*(Q*Q.T)*pv+nc[2]*q2*g*pv
        assert (N-guess).applyfunc(s.expand)==s.zeros(4)
        assert (E(N)-bb*q2*pv*(Q*Q.T-q2*g)).applyfunc(s.expand)==s.zeros(4)
        assert E(K(v))==s.zeros(4)
        source_coeff=nc
        checks.extend([f'{signature}_source_{k}',f'{signature}_physical_H_source_contact_{k}'])
        for i in range(4):
            for j in range(i,4):
                T=s.zeros(4);T[i,j]=1;T[j,i]=1
                w4=quartic(K(v),T,n4);w3=paired(T,E(N))
                ward=s.expand(w4+lam*w3)
                expected=s.expand(s.Rational(187,1920)*q2**2*(Q.T*g*T*v)[0]+
                    (s.Rational(43,960)-lam*bb)*q2**2*tr(T)*pv+
                    (-s.Rational(7,40)+lam*bb)*q2*pH(T)*pv)
                assert s.expand(ward-expected)==0
                checks.append(f'{signature}_hc_{k}_{i}{j}')
                # Contact-only terms are removed with their own computed coefficients.
                assert s.expand(ward-w4-lam*w3)==0
    v=s.eye(4)[:,0];T=K(v)
    double=quartic(K(v),T,n4).subs({q[0]:1,q[1]:0,q[2]:0,q[3]:0})
    assert double==-s.Rational(21,320)
    # E(Kv)=0 implies no relative lambda can cancel this raw double-gauge contact.
    examples.append(dict(signature=signature,raw_double_gauge=str(double),source_part='0'))
    checks.append(f'{signature}_relative_normalization_cannot_remove_raw_defect')
assert bb!=0
new(DEST/'results.json',dict(at=datetime.now(timezone.utc).isoformat(),
    derivative_contact_ab=[str(aa),str(bb)],
    source_contact_coefficients=[str(x) for x in source_coeff],
    source_basis=['q2 K_q(v)','q tensor q*(q.v)','q2 g*(q.v)'],
    combined_hc_coefficients=[str(s.Rational(187,1920)),str(s.Rational(43,960)-lam*bb),
                             str(-s.Rational(7,40)+lam*bb)],
    combined_basis=['q4 Tq.v','q4 trT q.v','q2 qTq q.v'],
    checks=len(checks),check_names=checks,negative_controls=4,double_gauge_examples=examples,
    physical_relative_phase_retained_symbolically=True,
    finite_subtraction_removes_principal_contact=True,full_causal_Q2=False,
    cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall))
print(json.dumps(dict(ab=list(map(str,[aa,bb])),source=list(map(str,source_coeff)),checks=len(checks),
    combined=[str(s.Rational(187,1920)),str(s.Rational(43,960)-lam*bb),str(-s.Rational(7,40)+lam*bb)],
    cpu_seconds=time.process_time()-cpu)))
