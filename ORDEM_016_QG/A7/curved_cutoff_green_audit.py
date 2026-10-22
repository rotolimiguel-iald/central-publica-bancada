"""Independent coefficient/Green-current audit of the candidate localized D_t.

The ten symmetric fibers are exhaustive for the coefficient symmetry check.
The Lie-closure check is separate; this script pays the integrated adjoint step.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
from curved_cutoff_descent_engine import *
H=Path(__file__).resolve().parent; D=H/'curved_cutoff_green'; D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    assert not p.exists(); b=json.dumps(v,indent=2).encode(); q=p.with_suffix('.tmp')
    q.write_bytes(b);assert q.read_bytes()==b;q.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    target='All coefficient adjoints; actual curved localized Green current for polarized ghost insertions',
    no_quantum_anomaly_identification=True))
cpu=process_time();checks=0
def check(a,b=0):
    global checks
    assert a==b,(a,b); checks+=1
def inner(A,B):return sum((A[a][b]*B[a][b] for a,b in product(range(4),repeat=2)),F())
def tr(A):return sum(A[i][i] for i in range(4))
def C(X,Y,i,j,t):
    d1,d2,d3,d4=F(1,2)-t/2,F(9,4)+t/2,-1-t/2,t
    return (-int(i==j)*(d1*inner(X,Y)+d2*tr(X)*tr(Y))
            -d3*(X[i][j]*tr(Y)+tr(X)*Y[i][j])
            -d4/2*sum(X[i][a]*Y[j][a]+X[j][a]*Y[i][a] for a in range(4)))
def algebraic(X,Y,t):return (t+F(7,3))*inner(X,Y)+(-t-F(22,3))*tr(X)*tr(Y)
def tensor(jet,word,o):return [[jet(word,(a,b),o) for b in range(4)] for a in range(4)]
basis=[[[F(int((a,b)==(i,j) or (a,b)==(j,i))) for b in range(4)] for a in range(4)]
       for i in range(4) for j in range(i,4)]
# Affine in t: t=0,1 tests coefficients exactly, not approximation in t.
for t in [F(0),F(1)]:
    for X,Y in product(basis,repeat=2):
        check(algebraic(X,Y,t),algebraic(Y,X,t))
        for i,j in product(range(4),repeat=2):
            check(C(X,Y,i,j,t),C(Y,X,i,j,t))
            check(C(X,Y,i,j,t),C(X,Y,j,i,t))

metric=polynomial_jet(spaceform_metric_initial,2)
def hi(ix,o):
    if o:return {}
    a,b=sorted(ix)
    return plus({ZERO:F(a+b+1)},mono((a,b),2),mono((a,(b+1)%4),-1),mono((a,b,(a+2)%4),1))
h=polynomial_jet(hi,2)
total=lambda w,ix,o: metric(w,ix,o)+h(w,ix,o)
u=polynomial_jet(lower_vector_initial([plus({ZERO:F(i-1)},mono((i,),2),mono((i,(i+1)%4),3)) for i in range(4)]),1)
v=polynomial_jet(lower_vector_initial([plus({ZERO:F(3-i)},mono(((i+1)%4,),-1),mono((i,i),2)) for i in range(4)]),1)
Vu,Vv=lie_tensor(u,total),lie_tensor(v,total)
chi=polynomial_jet(lambda ix,o:plus({ZERO:F(2)},mono((0,),3),mono((2,),-1),mono((1,1),2)) if not o else {},0)
samples=[];nonzero_current=0
for t in [F(0),F(1),F(-2)]:
    Dh=ward_operator(h,t)
    for X in basis:
        for o in range(3):
            rhs=F()
            if o:rhs+=sum(C(X,tensor(h,(i,j),o-1),i,j,t) for i,j in product(range(4),repeat=2))
            if o>=2:rhs+=algebraic(X,tensor(h,(),o-2),t)
            check(inner(X,tensor(Dh,(),o)),rhs)
    for label,X,Y in [('gauge_gauge',Vv,Vu),('gauge_field',Vu,h)]:
        MX,MY=localized_operator(chi,X,t),localized_operator(chi,Y,t)
        for o in range(3):
            lhs=sum((inner(tensor(X,(),k),tensor(MY,(),o-k))-inner(tensor(MX,(),k),tensor(Y,(),o-k))
                     for k in range(o+1)),F())
            divergence=F()
            if o:
                for k in range(o):
                    for l in range(o-k):
                        m=o-1-k-l
                        for i,j in product(range(4),repeat=2):
                            divergence+=chi((i,),(),k)*(C(tensor(X,(),l),tensor(Y,(j,),m),i,j,t)
                                -C(tensor(X,(j,),l),tensor(Y,(),m),i,j,t))
                            divergence+=chi((),(),k)*(C(tensor(X,(i,),l),tensor(Y,(j,),m),i,j,t)
                                +C(tensor(X,(),l),tensor(Y,(i,j),m),i,j,t)
                                -C(tensor(X,(i,j),l),tensor(Y,(),m),i,j,t)
                                -C(tensor(X,(j,),l),tensor(Y,(i,),m),i,j,t))
            check(lhs,divergence)
            nonzero_current+=int(bool(divergence))
            samples.append(dict(t=str(t),pair=label,order=o,WZ_or_Green_density=str(lhs),divergence=str(divergence)))
assert nonzero_current>0
fresh(D/'results.json',dict(statute='DERIVED_EXPLICIT_GREEN_CURRENT_FOR_CANDIDATE_NONLINEAR_WZ',checks=checks,
    nonzero_divergence_samples=nonzero_current,samples=samples,cpu_seconds=process_time()-cpu,
    identity='X.MY-(MX).Y = div_i{K chi C^ij(X,nabla_jY)-K chi C^ij(nabla_jX,Y)}',
    negative_control='Dropping the current makes the nonzero density fail, even though its integral vanishes at compact support',
    interpretation='Polarize two odd ghost directions: Lie closure removes commutator variation; remainder is this divergence',
    actual_quantum_h2c_identified=False,full_Q2=False,representative_selected=False,prescription_changed=False))
files=[Path(__file__),H/'curved_cutoff_descent_engine.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,nonzero_divergence_samples=nonzero_current,cpu=process_time()-cpu)))
