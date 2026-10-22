"""Finite local difference of raw metric pair and its harmonic reference.

Uses the same ordered covariant jets and signs as the paid logarithmic
operator. Does not add a tadpole, a smooth reference or a counterterm.
"""
from position_metric_ordered_operator_engine import (
    F, BASIS, green_integer, vertex_data, potential, external_jets,
    weighted, frob, sandwich,
)
from finite_angular_contact_engine import node_weights

def finite_node(A, B, p, x, order, jet_provider=external_jets):
    x = tuple(x)
    z = sum(v*v for v in x)
    G0,G1,GL,d0,d1 = green_integer(x)
    b2,b1,_ = vertex_data(B)
    bp = potential(B)
    specs = [(2,-1,0)]+[(1,i,0) for i in range(4)]+[(0,-1,1)]
    result = [F(),F(),F(),F()]
    # Components ordered (r0,no log),(r0,log),(r1,no log),(r1,log).
    for nx,xi,ex in specs:
        for ny,yj,ey in specs:
            if ex+ey>order:continue
            BY = b2 if ny==2 else (b1[yj] if ny==1 else bp)
            for r in range(min(1,order-ex-ey)+1):
                n=nx+ny-2*r
                o=order-ex-ey-r
                if n<=0:continue # l0 representation has zero derivative contact
                jets=jet_provider(A,p,o,n,xi,yj)
                if not jets:continue
                sign=(-1 if ny==1 else 1)*(-1 if (ex+ey)%2 else 1)*(-1)**n
                for ell in range(2 if r else 1):
                    weights=node_weights(n,ell,x)
                    vec=[F() for _ in range(10)]
                    for word,denom,v in jets:
                        factor=weights.get(word,F()) # no second Taylor factorial
                        for a in range(10):vec[a]+=factor*v[a]
                    if not any(vec):continue
                    AX=weighted(vec,nx,xi)
                    def c(U,V):return frob(sandwich(U,AX,V),BY)
                    if r==0:
                        value=F(c(G0,G0),d0*d0)
                    elif ell==1:
                        value=F(c(G0,GL)+c(GL,G0),d0*d1)
                    else:
                        value=F(c(G0,G1)+c(G1,G0),d0*d1)
                        value-=F(z,2)*F(c(G0,G0),d0*d0)
                    result[2*r+ell]+=sign*value*z*z/16
    return tuple(result)
