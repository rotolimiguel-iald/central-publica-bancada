"""Exact radial-log coefficient of scalar principal one-loop momentum kernels.

Euclidean angular algebra only. No finite renormalization, Wick factors, tensor
fiber contractions, ghost signs, or BRST anomaly are inferred by this module.
"""
from functools import lru_cache
import sympy as s

q=s.symbols('q0:4')
n=s.symbols('n0:4')
ANGULAR_FACTOR=s.Rational(1,8)/s.pi**2  # area(S3)/(2pi)^4, not a fitted parameter

@lru_cache(None)
def sphere_average_monomial(exponents):
    if any(a % 2 for a in exponents):return s.S.Zero
    total=sum(exponents)//2
    numerator=s.prod(s.factorial2(a-1) for a in exponents)
    denominator=s.prod(4+2*j for j in range(total))
    return numerator/denominator

def sphere_average(expr):
    poly=s.Poly(s.expand(expr),*n)
    return s.expand(sum(c*sphere_average_monomial(exps) for exps,c in poly.terms()))

def log_coefficient(numerator, shifts, masses_squared):
    """Return coefficient of log(Lambda) for d4q/(2pi)^4 N/prod D_e.

    D_e=(q+p_e)^2+m_e^2; all data are commuting polynomials independent of q.
    This is a UV asymptotic coefficient and does not evaluate the loop integral.
    """
    if len(shifts)!=len(masses_squared) or not shifts:
        raise ValueError('One shift and mass squared per denominator required')
    for p in shifts:
        if len(p)!=4:raise ValueError('Four Euclidean components required')
    data=[s.sympify(v) for p in shifts for v in p]+list(map(s.sympify,masses_squared))
    if any(set(q)&x.free_symbols for x in data):
        raise ValueError('Denominator data must not depend on loop momentum')
    poly=s.Poly(s.expand(numerator),*q)
    terms=poly.terms()
    maximum=max((sum(exps) for exps,_ in terms),default=0)+4-2*len(shifts)
    if maximum<0:return s.S.Zero
    # Recurrence of 1/(1+u*t+v*t²), t=1/r, with n on the unit sphere.
    product=[s.S.One]+[s.S.Zero]*maximum
    for p,m2 in zip(shifts,masses_squared):
        u=2*sum(n[j]*p[j] for j in range(4))
        v=sum(s.sympify(x)**2 for x in p)+m2
        den=[s.S.One]
        for k in range(1,maximum+1):
            den.append(s.expand(-u*den[k-1]-(v*den[k-2] if k>=2 else 0)))
        product=[s.expand(sum(product[j]*den[k-j] for j in range(k+1)))
                 for k in range(maximum+1)]
    radial=0
    for exps,c in terms:
        order=sum(exps)+4-2*len(shifts)
        if order>=0:
            radial+=c*s.prod(n[j]**exps[j] for j in range(4))*product[order]
    return s.factor(ANGULAR_FACTOR*sphere_average(radial))
