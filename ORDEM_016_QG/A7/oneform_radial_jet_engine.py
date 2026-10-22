"""Odd covariant jets extracted from the first-curvature Ward probe; no I/O."""
from functools import lru_cache
from fractions import Fraction as F
from itertools import combinations,permutations
from ghost_covariant_word_engine import gamma

def oneform(v,p):
    @lru_cache(None)
    def jet(w,a,order):
        n=len(w);assert n in (1,3,5)
        if order==0:
            out=F(v[a])*(-1)**((n-1)//2)
            for i in w:out*=p[i]
            return out
        if n==1:return F()
        out=F()
        # Differentiate exactly one Christoffel, including derivative slots.
        for k in range(1,n):
            for j in range(k):
                for slot in range(k+1,n+1):
                    target=w[slot] if slot<n else a
                    for c in range(4):
                        value=-gamma(c,w[k],target,w[j])*(-1)**((n-3)//2)
                        if not value:continue
                        ww=list(w);aa=a
                        if slot<n:ww[slot]=c
                        else:aa=c
                        value*=v[aa]
                        for t,i in enumerate(ww):
                            if t not in (j,k):value*=p[i]
                        out+=value
        # h_coordinate=e h_radial with e=I-K(zI-xx)/6.
        for i,j in combinations(range(n),2):
            a1,a2=w[i],w[j]
            c2=-F(1,3)*int(a1==a2)*v[a]+F(1,6)*(int(a==a1)*v[a2]+int(a==a2)*v[a1])
            value=c2*(-1)**((n-3)//2)
            for t,b in enumerate(w):
                if t not in (i,j):value*=p[b]
            out+=value
        return out
    @lru_cache(None)
    def h(w,a,b,order):return jet(w+(a,),b,order)+jet(w+(b,),a,order)
    @lru_cache(None)
    def hs(w,a,b,order):
        words=set(permutations(w))
        return sum((h(t,a,b,order) for t in words),F())/len(words)
    return jet,hs
