"""First-curvature parametrix jets and the h-star/c bubble in a normal chart.

Euclidean auxiliary algebra. K coefficient only; smooth reference W is excluded
explicitly, not asserted zero for a state. Every propagator strips 1/(4*pi^2).
"""
from functools import lru_cache
import sympy as s
x=s.symbols('x0:4'); z,L=s.symbols('z L')
def d(i,j):return s.Integer(i==j)
def dx(f,i):return s.expand(s.diff(f,x[i])+2*x[i]*(s.diff(f,z)+s.diff(f,L)/z))
def base(a,b,c,e):return (d(a,c)*d(b,e)+d(a,e)*d(b,c)-d(a,b)*d(c,e))/2
def lower_cross(a,c):return -(d(a,c)*z-x[a]*x[c])/6
def lower_cross_y(a,c,j):return (x[a]*d(c,j)-d(a,j)*x[c])/2
def metric1(a,b):return -(d(a,b)*z-x[a]*x[b])/3
def spin1(a,b,c,e):
    return (lower_cross(a,c)*d(b,e)+d(a,c)*lower_cross(b,e)
           +lower_cross(a,e)*d(b,c)+d(a,e)*lower_cross(b,c)
           -metric1(a,b)*d(c,e))/2
def spin1_y(a,b,c,e,j):
    return (lower_cross_y(a,c,j)*d(b,e)+d(a,c)*lower_cross_y(b,e,j)
           +lower_cross_y(a,e,j)*d(b,c)+d(a,e)*lower_cross_y(b,c,j))/2
@lru_cache(None)
def hjet(order,a,b,c,e,yi=-1,xi=-1):
    S=base(a,b,c,e)
    if order==0:
        f=S/z if yi<0 else 2*x[yi]*S/z**2
    else:
        A=spin1(a,b,c,e); V=d(a,b)*d(c,e)/2
        f=A/z+S/4+V*L if yi<0 else spin1_y(a,b,c,e,yi)/z+2*x[yi]*A/z**2-2*x[yi]*V/z
    return s.expand(f if xi<0 else dx(f,xi))
@lru_cache(None)
def gjet(order,m,n,yi,xi=-1):
    if order==0:f=2*d(m,n)*x[yi]/z**2
    else:
        P=(d(m,n)*z-x[m]*x[n])/6
        Py=(x[m]*d(n,yi)-d(m,yi)*x[n])/2
        f=Py/z+2*x[yi]*P/z**2+s.Rational(5,2)*d(m,n)*x[yi]/z
    return s.expand(f if xi<0 else dx(f,xi))

def kernel(T,v,p,order):
    """(v terms, derivative-v terms divided by i), source at X, ghost at Y=0."""
    A=[];B=[]
    pairs=[(0,0)] if order==0 else [(0,1),(1,0)]
    tv=[(a,b,T[a,b]) for a in range(4) for b in range(4) if T[a,b]!=0]
    vr=[(r,v[r]) for r in range(4) if v[r]!=0]
    for a,b,t in tv:
      for m in range(4):
       for mu in range(4):
        for nu in range(4):
         for go,ho in pairs:
          # c^m partial_m h_ab and 2 h_am partial_b c^m.
          for fac,c,e,xi,gxi in [(t,a,b,m,-1),(2*t,a,m,-1,b)]:
           G=gjet(go,m,nu,mu,gxi)
           if G==0:continue
           for r,vrho in vr:
            V=hjet(ho,c,e,mu,nu,r,xi)
            if mu==nu:V-=sum(hjet(ho,c,e,al,al,r,xi) for al in range(4))/2
            A.append(-fac*G*vrho*V)
            D=p[mu]*hjet(ho,c,e,r,nu,-1,xi)+p[nu]*hjet(ho,c,e,mu,r,-1,xi)
            if mu==nu:D-=sum(p[al]*hjet(ho,c,e,al,r,-1,xi) for al in range(4))
            B.append(-fac*G*vrho*D)
    return s.expand(sum(A)),s.expand(sum(B))

@lru_cache(None)
def spherical_moment(powers):
    if any(k%2 for k in powers):return s.Integer(0)
    n=sum(powers)//2
    return s.prod(s.rf(s.Rational(1,2),k//2) for k in powers)/s.rf(2,n)
def average(f):
    f=s.expand(f.subs(z,1))
    return s.expand(sum(c*spherical_moment(powers) for powers,c in s.Poly(f,*x).terms()))
def local_log_profile(T,v,p,order):
    A,B=kernel(T,v,p,order)
    px=sum(p[i]*x[i] for i in range(4))
    # e^{-ip.x}, derivative v = +ip v; global source phase i is removed.
    expr=A*px**3/6-B*px**2/2 if order==0 else -A*px+B
    return average(expr)
