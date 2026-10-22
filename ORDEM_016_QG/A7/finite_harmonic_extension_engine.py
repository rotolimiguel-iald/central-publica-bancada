"""Harmonic differential representation of actual homogeneous pair kernels.

The analytic extension stays R=FP[(1-a)mu^(2a)z^a .]. A differential
representation is only a computational reference; its local difference is
computed, not adopted as a new prescription.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
import sympy as s
from logarithmic_contact_engine import contact,Q,A
from curved_source_jet_engine import x,z,L
q2=sum(v*v for v in x)
def lap(p):return s.expand(sum(s.diff(p,v,2) for v in x))

def harmonic_split(p):
    """p=sum (x.x)^j H_(m-2j), H harmonic; exact Fischer decomposition."""
    p=s.expand(p)
    if p==0:return []
    m=s.Poly(p,*x).total_degree()
    assert all(sum(k)==m for k,c in s.Poly(p,*x).terms())
    h=p;term=p;coefficient=s.Integer(1)
    for j in range(1,m//2+1):
        term=lap(term);coefficient=-coefficient/(4*j*(m-j+1))
        h+=coefficient*q2**j*term
    h=s.expand(h);assert lap(h)==0
    quotient,remainder=s.div(s.expand(p-h),q2,*x)
    assert remainder==0
    rows=[(0,h)] if h!=0 else []
    return rows+[(j+1,H) for j,H in harmonic_split(quotient)]

@lru_cache(None)
def radial_inverse(degree,b,log_power):
    """H_d(partial) z^(a-b)=c(a) H_d(x) z^(a-b-d)."""
    c=s.Integer(2)**degree*s.prod(A-b-j for j in range(degree))
    zero=s.expand(c).subs(A,0)==0
    maximum=log_power+int(zero)
    variables=s.symbols('v0:'+str(maximum+1))
    output=sum(variables[r]*sum(s.binomial(r,k)*s.diff(c,A,k).subs(A,0)*L**(r-k)
                               for k in range(r+1)) for r in range(maximum+1))
    equations=s.Poly(s.expand(output-L**log_power),L).all_coeffs()
    if zero:equations.append(variables[0]) # derivative of z^-b vanishes here
    solutions=s.solve(equations,variables,dict=True);assert len(solutions)==1
    values=tuple(solutions[0][v] for v in variables)
    assert s.expand(output.subs(solutions[0])-L**log_power)==0
    return values

@lru_cache(None)
def harmonic_contact(H,b,log_power):
    output=0
    for powers,coef in s.Poly(H,*x).terms():
        inds=tuple(i for i,k in enumerate(powers) for _ in range(k))
        output+=coef*contact(b,log_power,inds)
    return s.expand(output)

def represent(kernel):
    """Return explicit H(partial)R(U_b L^r) plus C*local(delta)."""
    kernel=s.expand(kernel);rows=[];local=0;reconstruction=0
    maxlog=s.Poly(kernel,L).degree() if kernel!=0 else 0
    for ell in range(maxlog+1):
        f=s.expand(kernel.coeff(L,ell))
        if f==0:continue
        denominator=max(-term.as_powers_dict().get(z,0) for term in s.Add.make_args(f))
        denominator=int(denominator)
        numerator=s.expand((f*z**denominator).subs(z,q2))
        assert not numerator.has(z)
        for power,H in harmonic_split(numerator):
            degree=s.Poly(H,*x).total_degree();N=denominator-power;b=N-degree
            inverse=radial_inverse(degree,b,ell)
            correction=sum(v*harmonic_contact(H,b,r) for r,v in enumerate(inverse))
            local+=correction
            reconstruction+=H*q2**power*L**ell
            rows.append(dict(degree=degree,power=N,base_power=b,target_log=ell,
                             harmonic=H,derivative_radial_coefficients=inverse,local=s.expand(correction)))
        rebuilt=sum(H*q2**power for power,H in harmonic_split(numerator))
        assert s.expand(rebuilt-numerator)==0
    return rows,s.expand(local)
