"""Principal marked one-loop kernels; pure exact algebra, no IO on import.

Fourier +i, covariant h. Reported kernels remove common 4*i*kappa*A0.
The mixed h*c effective vertex is -U P Q^-1 V before stripping phases.
Its h derivative gives a ghost insertion minus 1/4 a metric insertion.
"""
from functools import lru_cache
import sympy as s
from metric_principal_vertices import eh_cubic_16k, clear_caches
from one_loop_scale_engine import q, ANGULAR_FACTOR, log_coefficient

LABELS=[(i,j) for i in range(4) for j in range(i,4)]
BASIS=[]
for i,j in LABELS:
    H=s.zeros(4); H[i,j]=H[j,i]=1; BASIS.append(H)
S=s.Matrix(10,10,lambda i,j:s.trace(BASIS[i]*BASIS[j])-s.trace(BASIS[i])*s.trace(BASIS[j])/2).inv()
QQ=s.Matrix(q)
MONS=[s.S.One]+list(q)+[x*x for x in q]+[q[i]*q[j] for i in range(4) for j in range(i+1,4)]
AXES=[s.eye(4)[:,i] for i in range(4)]

def gauge(p,v): return p*v.T+v*p.T
def lie(H,k,l,v): return v.dot(k)*H+l*(H*v).T+(H*v)*l.T
def bracket(p,v,r,w): return v.dot(r)*w-w.dot(p)*v
def U(T,H,k,l): return k*s.trace(T*H)+2*H*T*l
def V(H,k,l):
    r=k+l
    return s.Matrix(4,4,lambda nu,rho:s.expand(-(
        k[rho]*(H*r)[nu]+r.dot(l)*H[rho,nu]+l[nu]*(H*r)[rho]
        -r[nu]*k[rho]*s.trace(H)/2-r[nu]*(H*l)[rho])))
def R0(p,v):
    return -s.Rational(3,8)*p.dot(p)*gauge(p,v)+s.Rational(1,2)*p*p.T*p.dot(v)
def normalized_log(n,shifts):
    return s.cancel(log_coefficient(s.expand(n),[tuple(x) for x in shifts],[0]*len(shifts))/ANGULAR_FACTOR)

@lru_cache(None)
def cubic_coefficients(h_tuple,p_tuple):
    p=s.Matrix(p_tuple)
    def W(node):
        return s.Matrix(10,10,lambda j,k:eh_cubic_16k(
            h_tuple,tuple(p),tuple(BASIS[j]),tuple(-node),tuple(BASIS[k]),tuple(node-p)))
    zero=s.zeros(4,1);c=W(zero)
    plus=[W(e) for e in AXES]; minus=[W(-e) for e in AXES]
    cs=[c]+[(plus[i]-minus[i])/2 for i in range(4)]
    cs += [(plus[i]+minus[i])/2-c for i in range(4)]
    cs += [W(AXES[i]+AXES[j])-plus[i]-plus[j]+c for i in range(4) for j in range(i+1,4)]
    point=s.Matrix([2,-1,1,3]);interp=s.zeros(10)
    for mon,C in zip(MONS,cs):interp+=mon.subs(dict(zip(q,point)))*C
    assert interp==W(point),'Cubic interpolation failed off nodes'
    clear_caches()
    return tuple(cs)

def marked_numerators(T,H,p,r,v):
    """h*(T,-p-r), h(H,p), c(v,r); common source metric momentum q."""
    l=p+r-QQ;k=r-QQ
    us=s.Matrix(10,4,lambda i,m:s.expand(U(T,BASIS[i],QQ,l)[m]))
    right_g=[V(B,-QQ,r)*v for B in BASIS]
    insertion=V(H,p,k)
    ghost=s.expand(sum(S[i,j]*s.expand((us[i,:]*insertion*right_g[j])[0])
                       for i in range(10) for j in range(10) if S[i,j]))
    # q metric and q-p metric; their endpoint pairing is S_ij S_km.
    left=S*us
    right=S*s.Matrix(10,4,lambda m,a:s.expand((V(BASIS[m],p-QQ,r)*v)[a]))
    W=cubic_coefficients(tuple(H),tuple(p))
    metric=0
    for mon,C in zip(MONS,W):
        metric+=mon*sum(C[j,k]*s.expand(left[j,:].dot(right[k,:]))
                        for j in range(10) for k in range(10) if C[j,k])
    return s.expand(ghost),s.expand(metric)

def marked(T,H,p,r,v):
    ng,nm=marked_numerators(T,H,p,r,v)
    zero=s.zeros(4,1)
    g=normalized_log(ng,[zero,-r,-p-r])
    m=normalized_log(nm,[zero,-p,-p-r])
    return g-m/4,g,m,ng,nm

def ghost_triangle(Y,v,w,p,r):
    k=QQ+p;l=r-QQ
    a=[V(H,QQ,p)*v for H in BASIS]
    b=[V(H,-QQ,r)*w for H in BASIS]
    n=s.expand(sum(S[i,j]*(l.dot(a[i])*Y.dot(b[j])-Y.dot(a[i])*k.dot(b[j]))
                   for i in range(10) for j in range(10) if S[i,j]))
    return normalized_log(n,[s.zeros(4,1),p,-r])

def simplex_log(n,shift1,shift2):
    """Independent Feynman-simplex UV coefficient for three massless factors."""
    x,y=s.symbols('x y');shift=x*shift1+y*shift2
    expr=s.expand(n.subs({q[i]:q[i]-shift[i] for i in range(4)},simultaneous=True))
    delta=x*shift1.dot(shift1)+y*shift2.dot(shift2)-shift.dot(shift);out=0
    for exps,c in s.Poly(expr,*q).terms():
        if any(a%2 for a in exps):continue
        a=sum(exps)//2
        if a<1:continue
        avg=s.prod(s.gamma(s.Rational(1,2)+v//2)/s.gamma(s.Rational(1,2)) for v in exps)/s.gamma(2+a)
        out+=2*c*avg*(-1)**(a-1)*s.binomial(a+1,2)*delta**(a-1)
    return s.integrate(s.integrate(s.expand(out),(y,0,1-x)),(x,0,1))
