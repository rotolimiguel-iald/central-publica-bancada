"""Full singular source evaluated on E(test), to first K.

Uses formal self-adjointness of E with compact test support. Computes the
bulk plane symbol; does not discard cutoff contacts or smooth W globally.
"""
import sympy as s
from curved_source_jet_engine import x,z,L,kernel
from finite_harmonic_extension_engine_v2 import harmonic_split
from curved_harmonic_fourier_engine import coefficients,L as FL
from einstein_test_field_engine import einstein,parallel_tensor,density

def fourier(expr,p):
    """Fourier exp(-ip.x)/C_E by exact homogeneous Fischer decomposition."""
    expr=s.expand(expr);total=0;p2=sum(q*q for q in p);X2=sum(q*q for q in x)
    for ell in (0,1):
        f=expr.coeff(L,ell)
        if f==0:continue
        N=max(0,max(-int(t.as_powers_dict().get(z,0)) for t in s.Add.make_args(f)))
        numerator=s.expand(s.expand(f*z**N).subs(z,X2));hom={}
        for powers,c in s.Poly(numerator,*x).terms():
            degree=sum(powers);term=c*s.prod(q**n for q,n in zip(x,powers))
            hom[degree]=hom.get(degree,0)+term
        for polynomial in hom.values():
            for radial,H in harmonic_split(s.expand(polynomial)):
                l=s.Poly(H,*x).total_degree();m=2*(N-radial)-l-4
                assert m>=0,(N,radial,l,m)
                coeff=sum(s.Rational(c)*FL**j for j,c in enumerate(coefficients(m,l,ell)))
                total+=(-s.I)**m*coeff*H.subs(dict(zip(x,p)),simultaneous=True)*p2**((m-l)//2)
    return s.expand(total)

def source_adjoint(T,p,v,order):
    """Return source(E T,c)/C_E/i; E acts before the fixed R extension."""
    p=s.Matrix(p);v=s.Matrix(v);test=density(einstein(parallel_tensor(T),-s.I*p))
    A=0;B=0
    for r in range(order+1):
        a,b=kernel(test[order-r],v,p,r);A+=a;B+=b
    result=s.simplify(s.expand(fourier(A,p)/s.I+fourier(B,p)))
    assert s.simplify(s.im(result.subs(FL,s.Symbol('realLog',real=True))))==0
    return [s.expand(result).coeff(FL,j) for j in range(3)]
