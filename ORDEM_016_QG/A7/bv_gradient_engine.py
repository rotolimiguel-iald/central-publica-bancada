"""Two skew-fiber BV terms proportional to the ghost gradient; IO-free.

For E and symmetric T, each map is antisymmetric under E<->T. Thus a
quadratic odd-antifield generator with one derivative of c can produce it.
They vanish at r=0 and preserve the already fixed constant-ghost identity.
"""
import marked_polynomial_engine as p
def einstein(H,k):
    return p.madd(p.mscale(p.itr(H),p.dot(k,k)),p.mscale(p.itr(p.gauge(k,p.C(H,k))),-1))
def terms(E,r,v):
    first=p.mscale(p.madd(p.sym(r,p.mv(E,v)),p.mscale(p.sym(v,p.mv(E,r)),-1)),p.QQ(1,2))
    second=p.mscale(p.madd(p.mscale(p.sym(v,r),p.trace(E)),p.mscale(p.I,-p.dot(v,p.mv(E,r)))),p.QQ(1,2))
    return [first,second]
