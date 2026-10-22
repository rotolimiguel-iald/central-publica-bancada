"""Mixed X/Y derivative labels for the existing metric and ghost parametrices.

This reuses the frozen labelled pair extension; derivative slots carry their
own connections. It does not change the partial normalization.
"""
from functools import lru_cache
from itertools import product
import sympy as s
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T
B=T.B

@lru_cache(None)
def yjet(kind,order,ind,word):
    if kind=='metric':return L.metric(order,ind,word)
    assert kind=='ghost'
    if not word:
        a,b=ind;d=T.delta(a,b)
        return L.clean(((d,T.F,()),)) if order==0 else L.clean(((B.P1[a,b],T.F,()),(-B.distance1*d,(2,0),()),(d/4,T.ONE,()),(-s.Rational(5,4)*d,T.LG,())))
    j,*rest=word;rest=tuple(rest);out=list(L.partial(yjet(kind,order,ind,rest),1,j))
    if order:
        for pos,b in enumerate(rest):
            for c in range(4):
                changed=rest[:pos]+(c,)+rest[pos+1:];gam=-T.gamma(T.y,c,j,b)
                out.extend((gam*a,p,w) for a,p,w in yjet(kind,0,ind,changed))
        a,b=ind
        for c in range(4):
            gam=-T.gamma(T.y,c,j,b)
            out.extend((gam*v,p,w) for v,p,w in yjet(kind,0,(a,c),rest))
    return L.clean(out)

@lru_cache(None)
def cov(kind,order,ind,xword=(),yword=()):
    if not xword:return yjet(kind,order,ind,yword)
    j,*rest=xword;rest=tuple(rest);out=list(L.partial(cov(kind,order,ind,rest,yword),0,j))
    if order:
        for pos,b in enumerate(rest):
            for c in range(4):
                changed=rest[:pos]+(c,)+rest[pos+1:];gam=-T.gamma(T.x,c,j,b)
                out.extend((gam*a,p,w) for a,p,w in cov(kind,0,ind,changed,yword))
        for pos in ((0,1) if kind=='metric' else (0,)):
            a=ind[pos]
            for c in range(4):
                changed=ind[:pos]+(c,)+ind[pos+1:]
                gam=-T.gamma(T.x,c,j,a) if kind=='metric' else T.gamma(T.x,a,j,c)
                out.extend((gam*v,p,w) for v,p,w in cov(kind,0,changed,rest,yword))
    return L.clean(out)

@lru_cache(None)
def euler(kind,order,ind,yword=()):
    out=[]
    for i in range(4):out.extend(cov(kind,order,ind,(i,i),yword))
    if order:
        for i,j in product(range(4),repeat=2):
            coeff=(T.xx*T.delta(i,j)-T.x[i]*T.x[j])/3
            out.extend((coeff*a,p,w) for a,p,w in cov(kind,0,ind,(i,j),yword))
        if kind=='ghost':out.extend((3*a,p,w) for a,p,w in cov(kind,0,ind,(),yword))
        else:
            out.extend((-2*a,p,w) for a,p,w in cov(kind,0,ind,(),yword))
            if ind[0]==ind[1]:
                for r in range(4):out.extend((2*a,p,w) for a,p,w in cov(kind,0,(r,r)+ind[2:],(),yword))
        for i in range(4):out.extend((-T.xx*a/2,p,w) for a,p,w in cov(kind,0,ind,(i,i),yword))
    return L.clean(out)

def pair_contact(kind1,ind1,kind2,ind2,xword2=(),yword1=(),yword2=(),order=1):
    return s.expand(sum(L.pair(euler(kind1,j,ind1,yword1),(),cov(kind2,order-j,ind2,xword2,yword2),()) for j in range(order+1)))
