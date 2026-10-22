"""Covariant one-form jets through K² and derivative order five; pure code.

Return the coefficient after removing the common Fourier factor i.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import permutations
from spaceform_covariant_jet_engine import ZERO,mono,plus,times,deriv,connection

def oneform_second(v,p):
    v=tuple(v);p=tuple(p)
    z=plus(*(mono((i,i)) for i in range(4)))
    def scale(poly,c):return {e:c*x for e,x in poly.items() if c*x}
    @lru_cache(None)
    def initial(a,o):
        if o==0:return {ZERO:F(v[a])} if v[a] else {}
        Nv=plus(scale(z,v[a]),*(mono((a,j),-v[j]) for j in range(4)))
        return scale(Nv,F(-1,6)) if o==1 else scale(times(z,Nv),F(1,120))
    @lru_cache(None)
    def field(w,a,o):
        if not w:return initial(a,o)
        i,rest=w[0],w[1:];f=field(rest,a,o)
        parts=[deriv(f,i),scale(f,p[i])];indices=list(rest)+[a]
        for slot,target in enumerate(indices):
            for c in range(4):
                changed=indices.copy();changed[slot]=c
                for ko in range(1,o+1):
                    lower=field(tuple(changed[:-1]),changed[-1],o-ko)
                    if lower:
                        gam=connection(ko,c,i,target)
                        if gam:parts.append(scale(times(gam,lower),-1))
        return plus(*parts)
    @lru_cache(None)
    def jet(w,a,o):
        n=len(w);assert n in (1,3,5) and 0<=o<=2
        if n<2*o+1:return F()
        return (-1)**((n-2*o-1)//2)*field(tuple(w),a,o).get(ZERO,F())
    @lru_cache(None)
    def gauge(w,a,b,o):return jet(w+(a,),b,o)+jet(w+(b,),a,o)
    @lru_cache(None)
    def symmetric(w,a,b,o):
        words=set(permutations(w))
        return sum((gauge(t,a,b,o) for t in words),F())/len(words)
    return jet,gauge,symmetric

def einstein_gauge(gauge,w,a,b,o):
    """Covariant derivative word w of E G(v); no use of target zero."""
    h=lambda t,i,j,k:gauge(w+t,i,j,k)
    E=-sum(h((i,i),a,b,o) for i in range(4))
    if a==b:E+=sum(h((i,i),m,m,o) for i in range(4) for m in range(4))/2
    E+=sum(h((a,m),m,b,o)+h((b,m),m,a,o) for m in range(4))
    E-=sum(h((a,b),m,m,o)+h((b,a),m,m,o) for m in range(4))/2
    if a==b:
        E-=sum(h((l,m),m,l,o) for l in range(4) for m in range(4))
        E+=sum(h((l,l),m,m,o) for l in range(4) for m in range(4))/2
    if o:
        E+=2*h((),a,b,o-1)
        if a==b:E+=sum(h((),m,m,o-1) for m in range(4))
    return E

def loop_gauge(symmetric,flat,first,second,o):
    j=symmetric;c1,c2,c3,c4,c5=flat;d1,d2,d3,_,d4=first;out=[]
    for a in range(4):
        row=[]
        for b in range(4):
            value=c1*sum(j((i,i,k,k),a,b,o) for i in range(4) for k in range(4))
            if a==b:value+=c2*sum(j((i,i,k,k),m,m,o) for i in range(4) for k in range(4) for m in range(4))
            value+=c3*sum(j((a,b,i,i),m,m,o) for i in range(4) for m in range(4))
            if a==b:value+=c3*sum(j((i,k,m,m),i,k,o) for i in range(4) for k in range(4))
            value+=c4/2*sum(j((a,i,k,k),i,b,o)+j((b,i,k,k),i,a,o) for i in range(4) for k in range(4))
            value+=c5*sum(j((a,b,i,k),i,k,o) for i in range(4) for k in range(4))
            if o>=1:
                value-=d1*sum(j((i,i),a,b,o-1) for i in range(4))
                if a==b:value-=d2*sum(j((i,i),m,m,o-1) for i in range(4) for m in range(4))
                value-=d3*sum(j((a,b),m,m,o-1) for m in range(4))
                if a==b:value-=d3*sum(j((i,k),i,k,o-1) for i in range(4) for k in range(4))
                value-=d4/2*sum(j((a,i),i,b,o-1)+j((b,i),i,a,o-1) for i in range(4))
            if o>=2:
                value+=second[0]*j((),a,b,o-2)
                if a==b:value+=second[1]*sum(j((),m,m,o-2) for m in range(4))
            row.append(value)
        out.append(row)
    return out
