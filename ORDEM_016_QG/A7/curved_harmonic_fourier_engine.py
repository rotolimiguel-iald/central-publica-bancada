"""Pure meromorphic homogeneous Fourier multipliers, including l>m.

The common phase i^m and C=-4*pi² are separated. L denotes the common
Fourier logarithm log(4*mu²/p²)-2*EulerGamma. Handles raw log powers0/1.
"""
from functools import lru_cache
from fractions import Fraction as F
from math import factorial
import sympy as s
L=s.Symbol('FourierLog')
def harmonic(n,power=1):return sum((F(1,k**power) for k in range(1,n+1)),F())
@lru_cache(None)
def coefficients(m,l,ell):
    assert m>=0 and l>=0 and (m-l)%2==0 and ell in (0,1)
    k=(m-l)//2;N=(m+l+4)//2
    if k>=0:
        pref=-F(1,2**(m+2)*factorial(k)*factorial(N-1))
        h=harmonic(k)+harmonic(N-1)
        if ell==0:return (pref*(h-1),pref,F())
        h2=harmonic(k,2)+harmonic(N-1,2)
        return (pref*(h*h+h2)/2,pref*h,pref/2)
    pref=-F((-1)**(-k)*factorial(-k-1),2**(m+2)*factorial(N-1))
    if ell==0:return (pref,F(),F())
    h=harmonic(-k-1)+harmonic(N-1)
    return (pref*h,pref,F())

@lru_cache(None)
def node_weights(m,ell,node,p,lmax):
    """Multiplier before raw kernel evaluation, radial factor included.

    A raw kernel of degree -m-4 integrates against these weights.
    Multiplication by an external polynomial of degree j requires m-j.
    """
    z=sum(F(x*x) for x in node);p2=sum(F(x*x) for x in p);xp=sum(F(a*b) for a,b in zip(node,p))
    assert p2>0
    cheb=[F(1),2*xp]
    for l in range(2,lmax+1):cheb.append(2*xp*cheb[-1]-z*p2*cheb[-2])
    out=[F(),F(),F()]
    for l in range(m%2,lmax+1,2):
        k=(m-l)//2
        radial=z**((m+4-l)//2)*p2**k*(l+1)*cheb[l]
        cs=coefficients(m,l,ell)
        for j in range(3):out[j]+=radial*cs[j]
    return tuple(out)

def direct_meromorphic(m,l,ell):
    a=s.Symbol('regulator');k=(m-l)//2;N=(m+l+4)//2
    if k>=0:ratio=1/(a*s.prod(a-j for j in range(1,k+1))*s.prod(j-a for j in range(1,N)))
    else:ratio=s.prod(j+a for j in range(1,-k))/s.prod(j-a for j in range(1,N))
    # Gamma(1+a)/Gamma(1-a) has no quadratic term in its log after
    # absorbing -2*EulerGamma in L, so this suffices for ell<=1.
    expansion=s.series(s.exp(a*L)*ratio,a,0,2).removeO()
    value=s.expand((1-a)*(s.diff(expansion,a) if ell else expansion)).coeff(a,0)
    pref=-s.Rational((-1)**abs(k),2**(m+2))
    return s.expand(pref*value)
