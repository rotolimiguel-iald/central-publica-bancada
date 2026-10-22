"""Exact integer vertices of the two-derivative Einstein-Hilbert principal part.

Euclidean index contractions; Fourier exp(+ipx). Metric perturbations are
covariant and linear, g=delta+h. Cubic output is 16*kappa times the vertex.
The Gamma-Gamma action is used only modulo its total derivative (constant cutoff).
"""
from functools import lru_cache
from itertools import permutations

I=tuple(int(i==j) for i in range(4) for j in range(4))
def trace(H):return sum(H[4*i+i] for i in range(4))
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def mv(H,p):return tuple(sum(H[4*i+j]*p[j] for j in range(4)) for i in range(4))
def inner(H,J):return sum(a*b for a,b in zip(H,J))
def basis(i,j):return tuple(int((a,b)==(i,j) or (a,b)==(j,i)) for a in range(4) for b in range(4))
def c2(H,p):
    hp=mv(H,p);tr=trace(H)
    return tuple(2*hp[i]-p[i]*tr for i in range(4))
@lru_cache(None)
def gamma2(H,p):
    # gamma = i/2 * gamma2, indices [rho,mu,nu].
    return tuple(p[mu]*H[4*nu+rho]+p[nu]*H[4*mu+rho]-p[rho]*H[4*mu+nu]
                 for rho in range(4) for mu in range(4) for nu in range(4))
@lru_cache(None)
def upper_product(H,G):
    return tuple(sum(H[4*rho+a]*G[16*a+4*mu+nu] for a in range(4))
                 for rho in range(4) for mu in range(4) for nu in range(4))
@lru_cache(None)
def contraction(W,G,H):
    """W^mu,nu (G^rho_mu,sigma H^sigma_nu,rho - G^rho_mu,nu H^sigma_rho,sigma)."""
    ht=[sum(H[16*a+4*rho+a] for a in range(4)) for rho in range(4)]
    result=0
    for mu in range(4):
        for nu in range(4):
            w=W[4*mu+nu]
            if w:
                b=sum(G[16*rho+4*mu+sigma]*H[16*sigma+4*nu+rho]
                      for rho in range(4) for sigma in range(4))
                b-=sum(G[16*rho+4*mu+nu]*ht[rho] for rho in range(4))
                result+=w*b
    return result
def eh_quadratic_8k(H,p,J,q):
    G,L=gamma2(H,tuple(p)),gamma2(J,tuple(q))
    return contraction(I,G,L)+contraction(I,L,G)
def gauge_fixed_quadratic_8k(H,p,J,q):
    return eh_quadratic_8k(H,p,J,q)-dot(c2(H,p),c2(J,q))
def eh_cubic_16k(H,p,J,q,L,r):
    fields=[(H,tuple(p)),(J,tuple(q)),(L,tuple(r))]
    gs=[gamma2(*f) for f in fields]
    result=0
    for i,j,k in permutations(range(3)):
        A=fields[i][0];G,T=gs[j],gs[k]
        result+=trace(A)*contraction(I,G,T)-2*contraction(A,G,T)
        result-=2*contraction(I,upper_product(A,G),T)
        result-=2*contraction(I,G,upper_product(A,T))
    return result
def gauge_matrix(p,v):
    return tuple(p[a]*v[b]+p[b]*v[a] for a in range(4) for b in range(4))
def lie_matrix(H,p,k,v):
    hv=mv(H,v);vp=dot(v,p)
    return tuple(vp*H[4*a+b]+k[a]*hv[b]+k[b]*hv[a] for a in range(4) for b in range(4))
def clear_caches():
    gamma2.cache_clear();upper_product.cache_clear();contraction.cache_clear()
