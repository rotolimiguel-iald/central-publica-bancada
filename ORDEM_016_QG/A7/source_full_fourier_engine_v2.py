"""Candidate full source symbol from the ordered covariant Taylor prescription.

Includes singular A/B kernels and source density correction through first K.
No curved Einstein composition, tadpole, smooth W or complete Ward claim.
Flat source functional uses exp(-ipX) on its tensor test and +ip on c(Y).
The source Taylor displacement is -x: P_j(-x)=(-1)^j P_j(x).
This cancels the j-dependent Fourier phase. Curved adjunction still requires audit.
"""
from fractions import Fraction as F
from functools import lru_cache
import sympy as s
import curved_source_jet_engine as E
from first_curvature_gauge_generating_engine import oneform_generator,AXES
from curved_harmonic_fourier_engine import node_weights

def pack(expr):
    terms=[]
    for powers,c in s.Poly(s.expand(expr),*E.x,E.z,E.L).terms():
        terms.append((powers[:4],powers[4],powers[5],F(c)))
    return tuple(terms)

def rational_pack(expr):
    expr=s.expand(expr)
    shift=max([0]+[-int(t.as_powers_dict().get(E.z,0)) for t in s.Add.make_args(expr)])
    return tuple((xs,zp-shift,ell,c) for xs,zp,ell,c in pack(s.expand(expr*E.z**shift)))

@lru_cache(None)
def kernels(T,order):
    T=s.Matrix(4,4,T);X=s.Matrix(E.x)
    dT=-E.z*T/6-(X*X.T*T+T*X*X.T)/6
    out=[]
    for r in range(4):
        v=s.eye(4)[:,r]
        a,_=E.kernel(T,v,s.zeros(4,1),order)
        if order:a+=E.kernel(dT,v,s.zeros(4,1),0)[0]
        out.append((r,-1,rational_pack(a)))
        for k in range(4):
            _,b=E.kernel(T,v,s.eye(4)[:,k],order)
            if order:b+=E.kernel(dT,v,s.eye(4)[:,k],0)[1]
            out.append((r,k,rational_pack(b)))
    return tuple(out)

def at_node(terms,x):
    z=sum(F(q*q) for q in x);values=[F(),F()]
    for powers,zp,ell,c in terms:
        assert ell in (0,1)
        value=c*z**zp
        for q,n in zip(x,powers):value*=q**n
        values[ell]+=value
    return values

def source_node(T,p,v,x,order):
    T=tuple(T);p=tuple(p);v=tuple(v);x=tuple(x)
    total=[F(),F(),F()]
    for rorder in range(order+1):
        o=order-rorder
        for r,k,raw in kernels(T,rorder):
            if not raw:continue
            suffix=(AXES[k],) if k>=0 else ()
            external=oneform_generator((),suffix,AXES[r],p,v,x,o)
            values=at_node(raw,x)
            m=(2 if k>=0 else 3)-2*rorder
            for j,c in enumerate(external):
                if not c:continue
                assert m-j>=0,(r,k,rorder,o,j)
                for ell,value in enumerate(values):
                    if not value:continue
                    weights=node_weights(m-j,ell,x,p,6)
                    for n in range(3):total[n]+=(-1)**(1-order+m)*c*value*weights[n]
    return tuple(total)
