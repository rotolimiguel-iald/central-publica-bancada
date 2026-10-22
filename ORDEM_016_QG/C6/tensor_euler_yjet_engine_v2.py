"""Label-preserving successor of tensor_euler_yjet_engine.py; original retained."""
from functools import lru_cache
from itertools import product
import sympy as s
import tensor_euler_zerojet as T
import labelled_bilocal_jet_engine as L
from smooth_line_compatibility_check_v2 import multiply
profile=L.metric
unit=L.unit

@lru_cache(None)
def first(ind, u, v):
    A0=profile(0,ind,u);A1=profile(1,ind,u);U=unit(v)
    value=sum(L.pair(A1,((0,i),(0,i)),U,()) for i in range(4))
    for i,j in product(range(4),repeat=2):
        c=(T.xx*T.delta(i,j)-T.x[i]*T.x[j])/3
        value+=multiply(c,L.pair(A0,((0,i),(0,j)),U,()))
    for i in range(4):
        value+=multiply(-2*T.x[i],L.pair(A0,((0,i),),U,()))
        for g,replaced in T.connection_lines(ind,0,i):
            R=profile(0,replaced,u)
            value+=multiply(2*g,L.pair(R,((0,i),),U,()))
            value+=multiply(s.diff(g,T.x[i]),L.pair(R,(),U,()))
    for c,replaced in T.potential_lines(ind,0):value+=c*L.pair(profile(0,replaced,u),(),U,())
    value+=multiply(-T.xx/2,sum(L.pair(A0,((0,i),(0,i)),U,()) for i in range(4)))
    return s.expand(value)

@lru_cache(None)
def second(ind,u,v):
    return s.expand(sum(L.pair(unit(u),((0,i),(0,i)),profile(1,ind,v),()) for i in range(4)))

def contact(i,j,u=(),v=()):
    return s.expand(T.S(j)*first(i,u,v)+T.S(i)*second(j,u,v))
