"""S3 projectors for local harmonic-reference contact, same fixed R.

No raw graph, Wick weight, Taylor factorial or Ward assumption enters here.
Coefficients multiply C times derivatives of delta, with q denoting d/dx.
"""
from functools import lru_cache
from fractions import Fraction
import sympy as s
from finite_harmonic_extension_engine_v2 import radial_inverse, harmonic_contact
from curved_source_jet_engine import x, z
from logarithmic_contact_engine import Q

@lru_cache(None)
def coefficient(m, degree, log_power):
    assert m >= 0 and 0 <= degree <= m and (m-degree) % 2 == 0
    base = (m+4-degree)//2
    harmonic = s.expand((x[0]+s.I*x[1])**degree)
    weights = radial_inverse(degree, base, log_power)
    local = s.expand(sum(w*harmonic_contact(harmonic, base, r)
                         for r, w in enumerate(weights)))
    value = s.simplify(local.subs(dict(zip(Q, (1, 0, 0, 0)))))
    expected = value*sum(q*q for q in Q)**((m-degree)//2)*(Q[0]+s.I*Q[1])**degree
    assert s.expand(local-expected) == 0
    assert value.is_Rational
    return value

@lru_cache(None)
def projector_polynomial(m, log_power):
    """Degree m polynomial in x,q; z remains formal x.x until node evaluation."""
    nq = sum(a*b for a,b in zip(x,Q))
    q2 = sum(q*q for q in Q)
    zonal = [s.Integer(1), 4*nq, 12*nq**2-3*z*q2,
             32*nq**3-16*z*q2*nq,
             80*nq**4-60*z*q2*nq**2+5*z*z*q2*q2]
    assert 0 <= m <= 4
    return s.expand(sum(coefficient(m,l,log_power)*(z*q2)**((m-l)//2)*zonal[l]
                        for l in range(m%2,m+1,2)))

@lru_cache(None)
def weight_terms(m, log_power):
    out = []
    for qp, val in s.Poly(projector_polynomial(m,log_power), *Q).terms():
        word = tuple(i for i,n in enumerate(qp) for _ in range(n))
        terms = []
        for powers, c in s.Poly(val,*x,z).terms():
            terms.append((powers, Fraction(int(s.numer(c)),int(s.denom(c)))))
        out.append((word,tuple(terms)))
    return tuple(out)

def node_weights(m, log_power, node):
    """Return q-word coefficients. Contract against symmetric jets, not /I!."""
    coordinates = tuple(map(Fraction,node))
    variables = coordinates+(sum(a*a for a in coordinates),)
    out = {}
    for word, terms in weight_terms(m,log_power):
        total = Fraction(0)
        for powers, c in terms:
            for a,n in zip(variables,powers):
                c *= a**n
            total += c
        if total:
            out[word] = total
    return out
