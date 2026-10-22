"""Finite harmonic-reference contact of the directed ghost pair.

Same nonminimal ghost vertex and bitensor as the independent direct log
calculation. Retains ordered external jets; no heat-determinant inference.
"""
from ghost_direct_position_engine import green, vertex, weighted, F, BASIS
from position_metric_ordered_operator_engine import external_jets
from position_metric_bubble_engine import transpose, frob, sandwich
from finite_angular_contact_engine import node_weights

def finite_node(A,B,p,x,order, jet_provider=external_jets):
    x=tuple(x);z=sum(v*v for v in x)
    G0,G1,GL,d0,d1=green(x)
    b2,b1=vertex(B)
    specs=[(2,-1)]+[(1,i) for i in range(4)]
    total=[F() for _ in range(4)]
    for nx,xi in specs:
        for ny,yj in specs:
            BY=transpose(b2 if ny==2 else b1[yj])
            for r in range(min(order,1)+1):
                m=nx+ny-2*r;o=order-r
                if m<=0:continue
                jets=jet_provider(A,p,o,m,xi,yj)
                if not jets:continue
                sign=(-1 if ny==1 else 1)*(-1)**m
                for ell in range(2 if r else 1):
                    weights=node_weights(m,ell,x)
                    vec=[F() for _ in range(10)]
                    for word,denom,v in jets:
                        factor=weights.get(word,F())
                        for a in range(10):vec[a]+=factor*v[a]
                    if not any(vec):continue
                    WX=weighted(vec,nx,xi)
                    def c(U,V):return frob(sandwich(U,WX,V),BY)
                    if r==0:value=F(c(G0,G0),d0*d0)
                    elif ell==1:value=F(c(G0,GL)+c(GL,G0),d0*d1)
                    else:
                        value=F(c(G0,G1)+c(G1,G0),d0*d1)
                        value-=F(z,2)*F(c(G0,G0),d0*d0)
                    total[2*r+ell]+=sign*z*z*value
    return tuple(total)
