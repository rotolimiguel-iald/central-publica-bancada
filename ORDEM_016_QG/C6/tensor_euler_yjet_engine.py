"""First-curvature pair contacts with ordered covariant Y jets on both lines.

The X Euler operator acts only on the first line. Coefficients are kept
bilocal until differentiation finishes. No physical normalization is chosen.
"""
from functools import lru_cache
from itertools import product
import sympy as s
import tensor_euler_zerojet as T
import bilocal_covariant_jet_engine as J
from smooth_line_compatibility_check_v2 import multiply

@lru_cache(None)
def profile(order, ind, word):
    value=s.expand(J.yjet('metric',order,ind,word))
    grouped={}
    for term in s.Add.make_args(value):
        if term==0:continue
        pw=term.as_powers_dict();n=-pw.get(T.B.w,0);ell=pw.get(T.B.L,0)
        assert n>=0 and int(n)==n and ell>=0 and int(ell)==ell,(term,n,ell)
        key=(int(n),int(ell));coef=s.cancel(term*T.B.w**n/T.B.L**ell)
        assert not coef.has(T.B.w,T.B.L)
        grouped[key]=grouped.get(key,0)+coef
    return tuple((s.expand(c),key) for key,c in sorted(grouped.items()) if s.expand(c)!=0)

@lru_cache(None)
def unit(word):
    # All Y slots are covariant. Its order-zero profile is ordinary partials.
    return tuple((2*c,p) for c,p in profile(0,(0,1,0,1),word))

@lru_cache(None)
def first(ind, u, v):
    A0=profile(0,ind,u);A1=profile(1,ind,u);U=unit(v)
    value=sum(T.PD(A1,((0,i),(0,i)),U,()) for i in range(4))
    for i,j in product(range(4),repeat=2):
        c=(T.xx*T.delta(i,j)-T.x[i]*T.x[j])/3
        value+=multiply(c,T.PD(A0,((0,i),(0,j)),U,()))
    for i in range(4):
        value+=multiply(-2*T.x[i],T.PD(A0,((0,i),),U,()))
        for g,replaced in T.connection_lines(ind,0,i):
            R=profile(0,replaced,u)
            value+=multiply(2*g,T.PD(R,((0,i),),U,()))
            value+=multiply(s.diff(g,T.x[i]),T.PD(R,(),U,()))
    for c,replaced in T.potential_lines(ind,0):value+=c*T.PD(profile(0,replaced,u),(),U,())
    value+=multiply(-T.xx/2,sum(T.PD(A0,((0,i),(0,i)),U,()) for i in range(4)))
    return s.expand(value)

@lru_cache(None)
def second(ind,u,v):
    return s.expand(sum(T.PD(unit(u),((0,i),(0,i)),profile(1,ind,v),()) for i in range(4)))

def contact(i,j,u=(),v=()):
    return s.expand(T.S(j)*first(i,u,v)+T.S(i)*second(j,u,v))
