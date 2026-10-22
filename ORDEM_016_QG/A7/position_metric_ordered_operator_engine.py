"""Covariant Taylor expansion then explicit anchored-leg integration by parts.

Unlike a radial field profile, derivatives act on every tensor slot of the
jet. No fit, Ward target, I/O or modification of predecessor coefficients.
"""
from itertools import combinations_with_replacement,permutations
from math import factorial
from functools import lru_cache
from position_metric_second_curvature_engine_v2 import *
from radial_covariant_second_jet_engine import radial_second_jets

@lru_cache(None)
def external_jets(A,p,order,n,xi,yj):
    am=[A[4*i:4*i+4] for i in range(4)]
    val,_=radial_second_jets(am,p)
    out=[]
    for w in combinations_with_replacement(range(4),n):
        words=set(permutations(w));vec=[]
        for a,b in LABELS:
            v=sum((val(((yj,) if yj>=0 else ())+v+((xi,) if xi>=0 else ()),a,b,order) for v in words),F())/len(words)
            vec.append(v)
        if any(vec):
            denom=1
            for i in set(w):denom*=factorial(w.count(i))
            out.append((w,denom,tuple(vec)))
    return out

def weighted(vector,kind,index=-1):
    terms=[]
    for a,c in enumerate(vector):
        if c:
            W=potential(BASIS[a]) if kind==0 else vertex_data(BASIS[a])[0 if kind==2 else 1]
            if kind==1:W=W[index]
            terms.append((c,W))
    return lincomb(*terms) if terms else empty()

def ordered_node(A,B,p,x,order):
    x=tuple(x);z=sum(v*v for v in x)
    G0,G1,GL,d0,d1=green_integer(x)
    if order==2:G2,G2L,d2=second_integer(x)
    b2,b1,_=vertex_data(B);bp=potential(B)
    specs=[(2,-1,0)]+[(1,i,0) for i in range(4)]+[(0,-1,1)]
    values=[F(),F(),F()];logs=F()
    for nx,xi,ex in specs:
        for ny,yj,ey in specs:
            if ex+ey>order:continue
            BY=b2 if ny==2 else (b1[yj] if ny==1 else bp)
            sign=(-1 if ny==1 else 1)*(-1 if ex+ey==1 else 1)
            for r in range(order-ex-ey+1):
                n=nx+ny-2*r;o=order-ex-ey-r
                if n<0:continue
                jets=external_jets(A,p,o,n,xi,yj)
                if not jets:continue
                vec=[F() for _ in range(10)]
                for w,den,v in jets:
                    factor=F(1,den)
                    for i in w:factor*=x[i]
                    for a in range(10):vec[a]+=factor*v[a]
                if not any(vec):continue
                AX=weighted(vec,nx,xi)
                def c(U,V):return frob(sandwich(U,AX,V),BY)
                c0=F(c(G0,G0),d0*d0)
                if r==0:value=c0;log=F()
                elif r==1:
                    value=F(c(G0,G1)+c(G1,G0),d0*d1)-F(z,2)*c0
                    log=F(c(G0,GL)+c(GL,G0),d0*d1)
                else:
                    value=F(c(G0,G2)+c(G2,G0),d0*d2)+F(c(G1,G1),d1*d1)
                    value-=F(z,2)*F(c(G0,G1)+c(G1,G0),d0*d1)
                    value+=F(13*z*z,120)*c0
                    log=F(c(G0,G2L)+c(G2L,G0),d0*d2)
                values[r]+=sign*value*z*z/16
                logs+=sign*log*z*z/16
    return tuple(values)+(logs,)
