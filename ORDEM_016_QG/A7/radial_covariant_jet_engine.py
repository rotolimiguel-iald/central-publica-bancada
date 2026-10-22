"""Normal-chart jets of h=e A e^T exp(i p.x), constant radial components A.

Only coefficients K^0,K^1 for even derivative words of length<=4.
No I/O. Symmetric covariant Taylor jets must have zero first-K coefficient.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from functools import lru_cache
from ghost_covariant_word_engine import jet

def radial_jets(A,p):
    A=tuple(tuple(row) for row in A);p=tuple(p)
    def second_coframe(i,j,a,b):
        return (-F(2,3)*int(i==j)*A[a][b]+F(1,6)*(
            int(a==i)*A[b][j]+int(a==j)*A[b][i]+
            int(b==i)*A[a][j]+int(b==j)*A[a][i]))
    @lru_cache(None)
    def value(w,a,b,order=1):
        w=tuple(w);n=len(w);assert n in (0,2,4)
        base=jet(w,a,b,A,p,order)
        if not order:return base
        for i,j in combinations(range(n),2):
            v=second_coframe(w[i],w[j],a,b)*(-1)**((n-2)//2)
            for t,k in enumerate(w):
                if t not in (i,j):v*=p[k]
            base+=v
        return base
    @lru_cache(None)
    def symmetric(w,a,b,order=1):
        words=set(permutations(w))
        return sum((value(v,a,b,order) for v in words),F())/len(words)
    @lru_cache(None)
    def outer_symmetric(j,w,a,b):
        words=set(permutations(w))
        return sum((value((j,)+v,a,b,1) for v in words),F())/len(words)
    return value,symmetric,outer_symmetric
