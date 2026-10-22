"""Raw pair on exact ordered gauge Taylor generator, through firstK.

Includes high harmonics and the whole Laurent finite part. It computes
the metric/ghost pair, not the antifield source, tadpole or smooth W.
"""
from fractions import Fraction as F
from first_curvature_gauge_generating_engine import gauge_generator
from curved_harmonic_fourier_engine import node_weights
import position_metric_ordered_operator_engine as M
import ghost_direct_position_engine as G
from position_metric_bubble_engine import transpose,frob,sandwich

def pair_node(T,p,v,x,order):
    assert order in (0,1)
    x=tuple(x);p=tuple(p);v=tuple(v);z=sum(q*q for q in x)
    totals=[]
    for kind in ('metric','ghost'):
        ismetric=kind=='metric'
        G0,G1,GL,d0,d1=M.green_integer(x) if ismetric else G.green(x)
        bv=M.vertex_data(T) if ismetric else G.vertex(T)
        b2,b1=bv[:2]
        bp=M.potential(T) if ismetric else None
        specs=[(2,-1,0)]+[(1,i,0) for i in range(4)]
        if ismetric:specs.append((0,-1,1))
        output=[F(),F(),F()]
        for nx,xi,ex in specs:
            for ny,yj,ey in specs:
                if ex+ey>order:continue
                BY=b2 if ny==2 else (b1[yj] if ny==1 else bp)
                if not ismetric:BY=transpose(BY)
                sign=(-1 if ny==1 else 1)*(-1)**(ex+ey+order)
                for r in range(order-ex-ey+1):
                    o=order-ex-ey-r;m=nx+ny-2*r
                    polys=gauge_generator(p,v,x,xi,yj,o)
                    for j,vec in enumerate(polys):
                        if not any(vec):continue
                        mh=m-j;assert mh>=0
                        AX=M.weighted(vec,nx,xi) if ismetric else G.weighted(vec,nx,xi)
                        def c(U,V):return frob(sandwich(U,AX,V),BY)
                        values=[F(c(G0,G0),d0*d0)] if r==0 else [
                            F(c(G0,G1)+c(G1,G0),d0*d1)-F(z,2)*F(c(G0,G0),d0*d0),
                            F(c(G0,GL)+c(GL,G0),d0*d1)]
                        for ell,value in enumerate(values):
                            if not value:continue
                            weights=node_weights(mh,ell,x,p,4 if order==0 else 6)
                            for k in range(3):output[k]+=sign*value*weights[k]/(16 if ismetric else 1)
        totals.append(tuple(output))
    return tuple(totals)
