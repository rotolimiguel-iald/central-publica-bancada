"""Metric/ghost pair with tensor test at X and gauge ghost at Y=0.

No integration by parts of the gauge-ghost leg. This is the orientation
used by source(E test,c), with full RNC derivative/frame contributions.
"""
from fractions import Fraction as F
from functools import lru_cache
from first_curvature_gauge_generating_engine import AXES,word_value
from curved_harmonic_fourier_engine import node_weights
import position_metric_ordered_operator_engine as M
import ghost_direct_position_engine as G
from position_metric_bubble_engine import transpose,frob,sandwich

def entries(T):return tuple(F(T[4*a+b]) for a,b in M.LABELS)
@lru_cache(None)
def ghost_gauge_vectors(p,v):
    G0=tuple(F(p[a]*v[b]+p[b]*v[a]) for a,b in M.LABELS)
    DG1=[]
    for j in range(4):
        DG1.append(tuple(word_value((AXES[j],AXES[a]),AXES[b],p,v,1)+
                         word_value((AXES[j],AXES[b]),AXES[a],p,v,1) for a,b in M.LABELS))
    return G0,tuple(DG1)

def x_components(T,p,x,nx,xi):
    """Rows (K order, polynomial degree, phase exponent i, fiber vector)."""
    vec=entries(T)
    if nx!=1:return [(0,0,0,vec)]
    z=sum(q*q for q in x);px=sum(q*r for q,r in zip(p,x))
    tx=[sum(T[4*a+b]*x[b] for b in range(4)) for a in range(4)]
    spin=tuple((x[a]*T[4*xi+b]+x[b]*T[4*a+xi]-int(xi==a)*tx[b]-int(xi==b)*tx[a])/F(2) for a,b in M.LABELS)
    frame=tuple(F(z*p[xi]-x[xi]*px,6)*c for c in vec)
    return [(0,0,3,tuple(F(p[xi])*c for c in vec)),(1,1,0,spin),(1,2,3,frame)]

def y_components(p,v,ny,yj):
    vec,curve=ghost_gauge_vectors(tuple(p),tuple(v))
    if ny!=1:return [(0,1,vec)]
    return [(0,2,tuple(F(p[yj])*c for c in vec)),(1,0,curve[yj])]

def oriented_pair_node(T,p,v,x,order):
    T=tuple(T);p=tuple(p);v=tuple(v);x=tuple(x);z=sum(t*t for t in x);totals=[]
    for ismetric in (True,False):
        green=M.green_integer if ismetric else G.green
        weighted=M.weighted if ismetric else G.weighted
        G0,G1,GL,d0,d1=green(x);out=[F(),F(),F()]
        specs=[(2,-1,0)]+[(1,i,0) for i in range(4)]
        if ismetric:specs.append((0,-1,1))
        for nx,xi,ex in specs:
            for ny,yj,ey in specs:
                if ex+ey>order:continue
                for xo,j,phx,xvec in x_components(T,p,x,nx,xi):
                    if not any(xvec):continue
                    for yo,phy,yvec in y_components(p,v,ny,yj):
                        if not any(yvec):continue
                        r=order-ex-ey-xo-yo
                        if r not in (0,1):continue
                        m=nx+ny-2*r;mh=m-j;assert mh>=0
                        phase=(phx+phy-mh-1)%4;assert phase in (0,2),(nx,ny,xo,yo,r,j,phase)
                        sign=(-1)**(phase//2+ex+ey)
                        AX=weighted(xvec,nx,xi);BY=weighted(yvec,ny,yj)
                        if not ismetric:BY=transpose(BY)
                        def c(U,V):return frob(sandwich(U,AX,V),BY)
                        values=[F(c(G0,G0),d0*d0)] if r==0 else [
                            F(c(G0,G1)+c(G1,G0),d0*d1)-F(z,2)*F(c(G0,G0),d0*d0),
                            F(c(G0,GL)+c(GL,G0),d0*d1)]
                        for ell,value in enumerate(values):
                            if not value:continue
                            w=node_weights(mh,ell,x,p,6)
                            for k in range(3):out[k]+=sign*value*w[k]/(16 if ismetric else 1)
        totals.append(tuple(out))
    return tuple(totals)
