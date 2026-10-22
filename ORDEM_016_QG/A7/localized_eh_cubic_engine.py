"""Full localized cubic EH vertex as matrices on internal first jets.

Stored convention matches existing GammaGamma Fourier-polynomial vertices:
V_full = chi V_GG - 8 (d chi).b3, with Fourier i stripped from each derivative.
This does not set d chi to zero or discard its derivative in later adjunction.
"""
from functools import lru_cache
from fractions import Fraction as F
from metric_boundary_current_engine import boundary_current
from position_metric_bubble_engine import BASIS, empty, lincomb, vertex_data

ZERO=(0,0,0,0)
AXES=tuple(tuple(int(i==j) for i in range(4)) for j in range(4))

@lru_cache(None)
def boundary_vertex_data(A, gradient):
    """Return boundary W0 and Wi; internal labels are (field, four derivatives)."""
    W0=empty();W1=[empty() for _ in range(4)]
    if not any(gradient):return W0,W1
    def contraction(fields):
        return -8*sum(F(g)*v for g,v in zip(gradient,boundary_current(*fields)))
    for a,B in enumerate(BASIS):
        for b,C in enumerate(BASIS):
            # A derivative on one internal leg; symmetry supplies the other.
            for i,p in enumerate(AXES):
                value=contraction(((A,ZERO),(B,p),(C,ZERO)))
                if value:W0[10*(i+1)+a][b]=value;W0[b][10*(i+1)+a]=value
            if b<a:continue
            for i,p in enumerate(AXES):
                value=contraction(((A,p),(B,ZERO),(C,ZERO)))
                if value:W1[i][a][b]=value;W1[i][b][a]=value
    return W0,W1

def localized_vertex_data(A, value, gradient):
    bulk=vertex_data(tuple(A));boundary=boundary_vertex_data(tuple(A),tuple(gradient))
    return (lincomb((value,bulk[0]),(F(1),boundary[0])),
            [lincomb((value,bulk[1][i]),(F(1),boundary[1][i])) for i in range(4)])

def jet_vector(B,p):
    values=[B[4*a+b] for a,b in __import__('position_metric_bubble_engine').LABELS]
    return values+[q*v for q in p for v in values]

def evaluate(vertex, p, B, q, C, r):
    b=jet_vector(B,q);c=jet_vector(C,r)
    def pairing(W):return sum(b[i]*v*c[j] for i,row in enumerate(W) for j,v in row.items())
    return pairing(vertex[0])+sum(p[i]*pairing(vertex[1][i]) for i in range(4))
