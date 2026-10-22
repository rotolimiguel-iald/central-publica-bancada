"""Flat scalar harmonic reference shift relative to derivatives of R(U2).

q is the differential symbol. No prescription is changed. High harmonics
l>m are excluded here only because the flat kernels used have l<=m.
"""
from functools import lru_cache
from fractions import Fraction
import sympy as s
from finite_angular_contact_engine import coefficient
from finite_harmonic_extension_engine_v2 import radial_inverse
from curved_source_jet_engine import x,z
from logarithmic_contact_engine import Q

@lru_cache(None)
def reference_coefficient(m,l):
    assert m>=0 and 0<=l<=m and (m-l)%2==0
    b=(m+4-l)//2
    inverse=radial_inverse(l,b,0)
    assert len(inverse)==1 and b>=2
    scalar=-(s.harmonic(b-1)+s.harmonic(b-2)-1)/(4**(b-1)*s.factorial(b-1)*s.factorial(b-2))
    return inverse[0]*scalar

def full_finite_coefficient(m,l):
    k=(m-l)//2;N=(m+4+l)//2
    # Schwinger/Gaussian transform, common [log(4mu²/p²)-2gamma] removed.
    return -(-1)**l*(s.harmonic(k)+s.harmonic(N-1)-1)/(2**(m+2)*s.factorial(k)*s.factorial(N-1))

@lru_cache(None)
def weight_terms(m):
    assert 0<=m<=4
    nq=sum(a*b for a,b in zip(x,Q));q2=sum(a*a for a in Q)
    zonal=[s.Integer(1),4*nq,12*nq**2-3*z*q2,
           32*nq**3-16*z*q2*nq,
           80*nq**4-60*z*q2*nq**2+5*z*z*q2*q2]
    poly=s.expand(sum(reference_coefficient(m,l)*(z*q2)**((m-l)//2)*zonal[l]
                      for l in range(m%2,m+1,2)))
    out=[]
    if poly==0:return tuple(out)
    for qp,val in s.Poly(poly,*Q).terms():
        word=tuple(i for i,n in enumerate(qp) for _ in range(n));terms=[]
        for powers,c in s.Poly(val,*x,z).terms():
            terms.append((powers,Fraction(int(s.numer(c)),int(s.denom(c)))))
        out.append((word,tuple(terms)))
    return tuple(out)

def node_weights(m,ell,node):
    assert ell==0,'This module is flat and log-free only'
    coordinates=tuple(map(Fraction,node));variables=coordinates+(sum(a*a for a in coordinates),)
    out={}
    for word,terms in weight_terms(m):
        value=Fraction()
        for powers,c in terms:
            for a,n in zip(variables,powers):c*=a**n
            value+=c
        if value:out[word]=value
    return out

def scalar_reference_local(rows):
    result=0
    for row in rows:
        assert row['target_log']==0 and row['base_power']>=2
        b=row['base_power'];inv=row['derivative_radial_coefficients']
        assert len(inv)==1
        shift=-(s.harmonic(b-1)+s.harmonic(b-2)-1)/(4**(b-1)*s.factorial(b-1)*s.factorial(b-2))
        result+=inv[0]*row['harmonic'].subs(dict(zip(x,Q)))*shift*sum(q*q for q in Q)**(b-2)
    return s.expand(result)
