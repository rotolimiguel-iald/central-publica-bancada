"""Local contacts for derivatives of z^-n log(mu^2 z)^ell in the fixed one-pair prescription."""
from functools import lru_cache
import sympy as s
A=s.Symbol('a')
Q=s.symbols('q0:4')

@lru_cache(None)
def differentiated(n,indices,signature):
    terms={(n,(0,0,0,0)):s.Integer(1)}
    for i in indices:
        out={}
        for (power,xs),coef in terms.items():
            if xs[i]:
                powers=list(xs);powers[i]-=1;key=(power,tuple(powers))
                out[key]=out.get(key,0)+coef*xs[i]
            powers=list(xs);powers[i]+=1;key=(power+1,tuple(powers))
            out[key]=out.get(key,0)+2*signature[i]*(A-power)*coef
        terms={key:s.expand(coef) for key,coef in out.items() if coef!=0}
    return terms

@lru_cache(None)
def residue(n,powers,signature):
    if n<2:return s.Integer(0)
    f=s.expand(sum(signature[i]*Q[i]**2 for i in range(4))**(n-2))
    for i,p in enumerate(powers):f=(-1)**p*s.diff(f,Q[i],p)
    return -f/s.Integer(4**(n-1)*s.factorial(n-1)*s.factorial(n-2))

def contact(n,ell,indices,signature=(1,1,1,1)):
    """(R(D f)-D R(f))/C for f=z^-n L^ell, all L at the regulator scale."""
    value=0
    for (power,xs),coef in differentiated(n,tuple(indices),tuple(signature)).items():
        local=residue(power,xs,tuple(signature))
        factor=s.diff(coef,A,ell+1).subs(A,0)/s.Integer(ell+1)
        if ell:factor+=s.diff(coef,A,ell).subs(A,0)
        value-=factor*local
    return s.expand(value)

def direct_laurent_contact(n,ell,indices,signature=(1,1,1,1)):
    """Separate regulator and log derivatives, retaining all poles before finite part."""
    out=0
    for (power,xs),coef in differentiated(n,tuple(indices),tuple(signature)).items():
        res=residue(power,xs,tuple(signature))
        for t in range(ell+1):
            u=ell-t
            difference=s.diff(coef,A,u).subs(A,0)-s.diff(coef,A,u)
            meromorphic=(1-A)*s.binomial(ell,t)*difference*s.diff(res/A,A,t)
            out+=s.expand(meromorphic).coeff(A,0)
    return s.expand(out)

def lap(f,signature=(1,1,1,1)):
    return s.expand(sum(signature[i]*s.diff(f,Q[i],2) for i in range(4)))
