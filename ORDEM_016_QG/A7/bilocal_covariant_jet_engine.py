"""Covariant two-endpoint jets through first curvature, before anchoring.

All Y slots are covariant; the ghost has one contravariant X vector slot.
Derivative words are outermost-first. The auxiliary w is retained until
all derivatives finish. No I/O, fitting or provider calls.
"""
from functools import lru_cache
import sympy as s
import bilocal_first_curvature_engine as B

def gamma(point,c,a,b):
    return -(B.d(c,b)*point[a]+B.d(c,a)*point[b]-2*B.d(a,b)*point[c])/3

@lru_cache(None)
def raw(kind,order,indices):
    if kind=='metric':return B.metric(order,*indices)
    assert kind=='ghost'
    return B.ghost(order,*indices)

@lru_cache(None)
def yjet(kind,order,indices,word):
    if not word:return raw(kind,order,indices)
    j,*rest=word;rest=tuple(rest)
    value=B.derivative(yjet(kind,order,indices,rest),'Y',j)
    if order:
        # The suffix derivative slots live at Y and also carry connections.
        for pos,b in enumerate(rest):
            for c in range(4):
                newword=rest[:pos]+(c,)+rest[pos+1:]
                value-=gamma(B.y,c,j,b)*yjet(kind,0,indices,newword)
        slots=(2,3) if kind=='metric' else (1,)
        for pos in slots:
            b=indices[pos]
            for c in range(4):
                newindices=indices[:pos]+(c,)+indices[pos+1:]
                value-=gamma(B.y,c,j,b)*yjet(kind,0,newindices,rest)
    return s.expand(value)

@lru_cache(None)
def xyjet(kind,order,indices,yword,xj):
    if xj<0:return yjet(kind,order,indices,yword)
    value=B.derivative(yjet(kind,order,indices,yword),'X',xj)
    if order:
        if kind=='metric':
            for pos in (0,1):
                b=indices[pos]
                for c in range(4):
                    newindices=indices[:pos]+(c,)+indices[pos+1:]
                    value-=gamma(B.x,c,xj,b)*yjet(kind,0,newindices,yword)
        else:
            # Contravariant vector index at X: PLUS connection, reversed slots.
            a=indices[0]
            for c in range(4):
                value+=gamma(B.x,a,xj,c)*yjet(kind,0,(c,indices[1]),yword)
    return s.expand(value)

def anchor(f):
    return s.cancel(B.anchored(f).subs(B.w,B.xx))

def coordinate_yward(B0,B1):
    """Return 2[-div B0 + div(div B1)] at Y=0 through firstK.

    B0(order,a,b) has two contravariant Y indices, symmetric a,b.
    B1(order,j,a,b) has three contravariant Y indices, symmetric a,b.
    X slots are spectators. Input arrays are coordinate components before
    anchoring, not matrices frozen in a Y-dependent parallel frame.
    Output pairs of lists (K0,K1), with covector c_b as external field.
    """
    result=[]
    for order in (0,1):
        rows=[]
        for b in range(4):
            value=0
            for a in range(4):
                value-=B.derivative(B0(order,a,b),'Y',a)
                for j in range(4):
                    value+=B.derivative(B.derivative(B1(order,j,a,b),'Y',j),'Y',a)
                    if order:
                        for r in range(4):
                            # Derivative of the connection in the FIRST divergence.
                            value+=s.diff(gamma(B.y,j,j,r),B.y[a])*B1(0,r,a,b)
                            value+=s.diff(gamma(B.y,a,j,r),B.y[a])*B1(0,j,r,b)
                            value+=s.diff(gamma(B.y,b,j,r),B.y[a])*B1(0,j,a,r)
            rows.append(anchor(2*value))
        result.append(rows)
    return result
