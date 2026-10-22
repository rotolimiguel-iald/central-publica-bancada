"""Full h*hc principal vertex in a sparse polynomial ring; IO-free.

The Einstein cubic has total momentum degree two. With metric momentum a*e0,
the coefficients of q-degree d scale as a**(2-d). Its exact q-polynomial
at a=1 comes from the already verified unisolvent interpolation engine.
"""
from functools import lru_cache
import marked_polynomial_engine as p
from marked_vertex_engine import cubic_coefficients,BASIS as SBASIS,AXES as SAXES

LABELS=[(i,j) for i in range(4) for j in range(i,4)]
BASIS=[[[p.ONE if (i,j) in ((u,v),(v,u)) else p.ZERO for j in range(4)] for i in range(4)] for u,v in LABELS]
MONS=[p.ONE]+list(p.q)+[x*x for x in p.q]+[p.q[i]*p.q[j] for i in range(4) for j in range(i+1,4)]
DEGREES=[0]+[1]*4+[2]*10
def rat(x):
    x=x.as_numer_denom() if hasattr(x,'as_numer_denom') else (x,1)
    return p.QQ(int(x[0]),int(x[1]))
@lru_cache(None)
def cubic_sparse(hi):
    coefficients=cubic_coefficients(tuple(SBASIS[hi]),tuple(SAXES[0]))
    return [[sum((rat(C[j,k])*mon*p.a**(2-degree) for C,mon,degree in zip(coefficients,MONS,DEGREES)),p.ZERO)
             for k in range(10)] for j in range(10)]
@lru_cache(None)
def source_vectors(ti):
    l=p.add(p.add(p.P,p.Q),p.scale(p.q,-1))
    return [p.itr(A) for A in p.source_duals(BASIS[ti],p.q,l)]
@lru_cache(None)
def metric_end(vi):
    return [p.itr(B) for B in p.ghost_duals(p.add(p.P,p.scale(p.q,-1)),p.Q,p.axes[vi])]
@lru_cache(None)
def ghost_end(vi):return p.ghost_duals(p.scale(p.q,-1),p.Q,p.axes[vi])
@lru_cache(None)
def insertion(hi):return p.ghost_matrix(BASIS[hi],p.P,p.add(p.Q,p.scale(p.q,-1)))
UVG=p.UV([p.ZERO4,p.scale(p.Q,-1),p.scale(p.add(p.P,p.Q),-1)])
UVM=p.UV([p.ZERO4,p.scale(p.P,-1),p.scale(p.add(p.P,p.Q),-1)])
def numerators(hi,ti,vi):
    us=source_vectors(ti);end=ghost_end(vi);gv=insertion(hi)
    ng=sum((gv[m][n]*p.inner(us[m],end[n]) for m in range(4) for n in range(4)),p.ZERO)
    other=metric_end(vi);W=cubic_sparse(hi);nm=p.ZERO
    for j,(ja,jb) in enumerate(LABELS):
        for k,(ka,kb) in enumerate(LABELS):
            if W[j][k]:
                dot=sum((us[m][ja][jb]*other[m][ka][kb] for m in range(4)),p.ZERO)
                if dot:nm+=W[j][k]*dot
    return ng,nm
def vertex(hi,ti,vi):
    ng,nm=numerators(hi,ti,vi)
    g,m=UVG.extract(ng),UVM.extract(nm)
    return g-m/4,g,m
