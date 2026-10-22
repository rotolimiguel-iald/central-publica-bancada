"""Raw K² constant-field radial bubble, before anchored-leg adjoints.

All matrices retain tensor fiber structure. No I/O or assertions of Q2.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import lcm
import sympy as s
from position_metric_bubble_engine import *
from metric_second_curvature_bitensor_engine import green_jet
from curved_source_jet_engine import x as sx,z as sz,L as sL
from metric_curvature_vertices import eh_cubic_potential_16k_over_K

@lru_cache(None)
def second_data():
    entries=[];denominator=1
    for i in range(4):
        for j in range(4):
            M=green_jet(2,i,j)
            for a in range(10):
                for b in range(10):
                    if not M[a,b]:continue
                    terms=s.Poly(s.expand(sz**2*M[a,b]),*sx,sz,sL).terms()
                    for powers,c in terms:
                        assert powers[-1]<=1
                        denominator=lcm(denominator,int(s.denom(c)))
                    entries.append((10*(i+1)+a,10*(j+1)+b,terms))
    return denominator,[(i,j,[(w,int(c*denominator)) for w,c in terms]) for i,j,terms in entries]
def second_integer(x):
    z=sum(t*t for t in x);denom,entries=second_data();G,GL=empty(),empty()
    for i,j,terms in entries:
        values=[0,0]
        for w,c in terms:
            v=c*z**w[4]
            for k in range(4):v*=x[k]**w[k]
            values[w[5]]+=v
        if values[0]:G[i][j]=values[0]
        if values[1]:GL[i][j]=values[1]
    return G,GL,denom*z*z
@lru_cache(None)
def potential(A):
    W=empty()
    for a,Ea in enumerate(BASIS):
        for b,Eb in enumerate(BASIS):
            v=eh_cubic_potential_16k_over_K(A,Ea,Eb)
            if v:W[a][b]=v
    return W
def second_node(A,B,x):
    x=tuple(x);z=sum(t*t for t in x)
    G0,G1,_,d0,d1=green_integer(x);G2,GL,d2=second_integer(x)
    a2,_,ac=vertex_data(A);b2,_,_=vertex_data(B)
    wa,wb=potential(A),potential(B)
    wc=lincomb(*[(F(x[i],2),ac[i]) for i in range(4)])
    def contraction(W,V,U,T):return frob(sandwich(U,W,T),V)
    zero=contraction(a2,b2,G0,G0)
    one=contraction(a2,b2,G0,G1)+contraction(a2,b2,G1,G0)
    two=contraction(a2,b2,G0,G2)+contraction(a2,b2,G2,G0)
    g11=contraction(a2,b2,G1,G1)
    derivative=F(two,d0*d2)+F(g11,d1*d1)-F(z*one,2*d0*d1)+F(13*z*z*zero,120*d0*d0)
    conn=F(contraction(wc,b2,G0,G1)+contraction(wc,b2,G1,G0),d0*d1)
    conn-=F(5*z*contraction(wc,b2,G0,G0),12*d0*d0)
    cross=F()
    for W,V in [(wa,b2),(a2,wb)]:
        cross-=F(contraction(W,V,G0,G1)+contraction(W,V,G1,G0),d0*d1)
        cross+=F(z*contraction(W,V,G0,G0),2*d0*d0)
    cross-=F(contraction(wc,wb,G0,G0),d0*d0)
    pp=F(contraction(wa,wb,G0,G0),d0*d0)
    log=F(contraction(a2,b2,G0,GL)+contraction(a2,b2,GL,G0),d0*d2)
    return tuple(v*z*z/16 for v in (derivative,conn,cross,pp,log))
