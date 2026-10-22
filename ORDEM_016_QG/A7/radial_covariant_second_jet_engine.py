"""Spaceform normal-chart radial-frame tensor jets through second curvature.

Pure polynomial recursion. h_ab(x)=e_a^i A_ij e_b^j exp(ip.x),
e=I-K(zI-xx)/6+K² z(zI-xx)/120. All derivative indices covariant.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import permutations
from spaceform_covariant_jet_engine import ZERO,mono,plus,times,deriv,connection

def radial_second_jets(A,p=(0,0,0,0)):
    A=tuple(tuple(row) for row in A);p=tuple(p)
    z=plus(*(mono((i,i)) for i in range(4)))
    N=[[plus(z if a==b else {},mono((a,b),-1)) for b in range(4)] for a in range(4)]
    def scale(v,c):return {e:c*x for e,x in v.items() if c*x}
    @lru_cache(None)
    def initial(a,b,order):
        if order==0:return {ZERO:F(A[a][b])} if A[a][b] else {}
        NA=plus(*(scale(N[a][j],A[j][b]) for j in range(4)))
        AN=plus(*(scale(N[j][b],A[a][j]) for j in range(4)))
        if order==1:return scale(plus(NA,AN),F(-1,6))
        NAN=plus(*(scale(times(N[a][j],N[k][b]),A[j][k]) for j in range(4) for k in range(4)))
        return plus(scale(times(z,plus(NA,AN)),F(1,120)),scale(NAN,F(1,36)))
    @lru_cache(None)
    def field(w,a,b,order):
        if not w:return initial(a,b,order)
        i,rest=w[0],w[1:];lower=field(rest,a,b,order)
        parts=[deriv(lower,i),scale(lower,p[i])]
        indices=list(rest)+[a,b]
        for slot,target in enumerate(indices):
            for k in range(4):
                changed=indices.copy();changed[slot]=k
                for ko in range(1,order+1):
                    f=field(tuple(changed[:-2]),changed[-2],changed[-1],order-ko)
                    if f:
                        g=connection(ko,k,i,target)
                        if g:parts.append(scale(times(g,f),-1))
        return plus(*parts)
    @lru_cache(None)
    def value(w,a,b,order):
        w=tuple(w);n=len(w)
        assert n%2==0 and 0<=order<=2 and n<=4
        if n<2*order:return F()
        return F((-1)**((n-2*order)//2))*field(w,a,b,order).get(ZERO,F())
    @lru_cache(None)
    def symmetric(w,a,b,order):
        words=set(permutations(w))
        return sum((value(v,a,b,order) for v in words),F())/len(words)
    return value,symmetric
