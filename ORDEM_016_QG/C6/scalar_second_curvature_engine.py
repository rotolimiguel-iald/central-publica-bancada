"""Massless scalar Hadamard singular jet through K² in the same space form."""
from functools import lru_cache
from itertools import product
import sympy as s
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T
from smooth_line_compatibility_check_v2 import multiply

x,y=T.x,T.y;xx,yy,xy=T.xx,T.yy,T.xy
distance1=-(xx*yy-xy**2)/3
distance2=-(xx+yy-4*xy)*(xx*yy-xy**2)/45

@lru_cache(None)
def scalar(order,word):
    if order<2:return L.scalar(order,word)
    assert order==2
    # U0/r²-K/2 log(r²), U0=(sqrt(K)r/sin(sqrt(K)r))**(3/2).
    # No smooth state term is added. r²=w+K distance1+K² distance2.
    base=((distance1**2,(3,0),()),(-distance2,(2,0),()),(-distance1/2,T.F,()),
          (s.Rational(19,480)*sum((x[i]-y[i])**2 for i in range(4)),T.ONE,()))
    for side,i in word:base=L.partial(base,side,i)
    return L.clean(base)

@lru_cache(None)
def contact(mu,nu,r,order):
    a=[scalar(o,((1,mu),)) for o in range(order+1)]
    b=[scalar(o,((0,r),(1,nu))) for o in range(order+1)]
    def lap(o):
        return sum(L.pair(a[j],((0,i),(0,i)),b[o-j],()) for j in range(o+1) for i in range(4))
    def geometry(o,k):
        ans=0
        for j in range(o+1):
            for u,v in product(range(4),repeat=2):
                c=(xx*T.delta(u,v)-x[u]*x[v])*(s.Rational(1,3) if k==1 else xx/15)
                ans+=multiply(c,L.pair(a[j],((0,u),(0,v)),b[o-j],()))
            for i in range(4):
                c=-2*x[i] if k==1 else -s.Rational(4,15)*xx*x[i]
                ans+=multiply(c,L.pair(a[j],((0,i),),b[o-j],()))
        return s.expand(ans)
    flat=lap(0)
    if order==0:return s.expand(flat)
    first=lap(1)+geometry(0,1)
    if order==1:return s.expand(first+multiply(-xx/2,flat))
    return s.expand(lap(2)+geometry(1,1)+geometry(0,2)+multiply(-xx/2,first)+multiply(s.Rational(13,120)*xx**2,flat))
