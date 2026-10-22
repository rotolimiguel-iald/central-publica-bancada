"""Integrate by parts the single derivative on the anchored external leg.

Difference between nabla_j sym(nabla^3) and sym(nabla^4) on the other
leg, evaluated using constant radial-frame plane waves; first curvature only.
"""
from itertools import combinations_with_replacement
from functools import lru_cache
from fractions import Fraction as F
from math import factorial
from position_metric_bubble_engine import *
from radial_covariant_jet_engine import radial_jets

TRIPLES=list(combinations_with_replacement(range(4),3))
PAIRS=list(combinations_with_replacement(range(4),2))
def multiplicity(w):
    d=factorial(len(w))
    for i in set(w):d//=factorial(w.count(i))
    return d
def mono(w,x):
    v=multiplicity(w)
    for i in w:v*=x[i]
    return v
@lru_cache(None)
def jet_data(A,p):
    AM=[A[4*i:4*i+4] for i in range(4)]
    _,_,outer=radial_jets(AM,p)
    return {(j,w):tuple(outer(j,w,a,b) for a,b in LABELS) for j in range(4) for w in TRIPLES}
def weighted_vertex(vector,kind,index=0):
    terms=[]
    for a,c in enumerate(vector):
        if c:
            data=vertex_data(BASIS[a])
            terms.append((c,data[0] if kind==2 else data[1][index]))
    return lincomb(*terms) if terms else empty()
def adjoint_node(A,B,p,x):
    x=tuple(x);z=sum(t*t for t in x);G,_,_,d0,_=green_integer(x)
    jets=jet_data(tuple(A),tuple(p));_,b1,_=vertex_data(tuple(B))
    correction=F()
    for j in range(4):
        t3=[sum((mono(w,x)*jets[j,w][a] for w in TRIPLES),F()) for a in range(10)]
        W=weighted_vertex(t3,2)
        correction-=F(1,6)*frob(sandwich(G,W),b1[j])
        for i in range(4):
            t2=[sum((mono(w,x)*jets[j,tuple(sorted((i,)+w))][a] for w in PAIRS),F()) for a in range(10)]
            W=weighted_vertex(t2,1,i)
            correction-=F(1,2)*frob(sandwich(G,W),b1[j])
    return correction*z*z/(16*d0*d0)
