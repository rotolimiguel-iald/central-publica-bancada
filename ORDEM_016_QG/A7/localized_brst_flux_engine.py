"""Classical cubic BV boundary flux in the existing stripped Fourier convention.

Build the Green current from the full quadratic EH density, retaining its
second derivatives. The current is a chosen polynomial representative;
only its divergence is fixed, up to divergence-free improvements.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import combinations
from metric_principal_vertices import eh_quadratic_8k,eh_cubic_16k,gauge_matrix,lie_matrix
from metric_boundary_current_engine import eh_boundary_vertex_raw

ZERO=(0,)*4
AXES=tuple(tuple(int(i==j) for i in range(4)) for j in range(4))
def add(*vs):return tuple(sum(x) for x in zip(*vs))
def neg(v):return tuple(-x for x in v)
def dot(a,b):return sum(u*v for u,v in zip(a,b))
def v2(A,p,B,q):return eh_quadratic_8k(A,p,B,q)+eh_boundary_vertex_raw((A,p),(B,q))
def v3(A,p,B,q,C,r):return eh_cubic_16k(A,p,B,q,C,r)+eh_boundary_vertex_raw((A,p),(B,q),(C,r))

@lru_cache(None)
def green_coefficients(A,B,q):
    """V2(A,Q-q,B,q)-V2(A,-q,B,q) = Q.L + Q.M.Q."""
    base=v2(A,neg(q),B,q)
    def D(Q):return v2(A,add(Q,neg(q)),B,q)-base
    assert D(ZERO)==0
    plus=[D(e) for e in AXES];minus=[D(neg(e)) for e in AXES]
    L=[F(p-m,2) for p,m in zip(plus,minus)]
    M=[[F() for _ in range(4)] for _ in range(4)]
    for i in range(4):M[i][i]=F(plus[i]+minus[i],2)
    for i,j in combinations(range(4),2):
        M[i][j]=M[j][i]=F(D(add(AXES[i],AXES[j]))-plus[i]-plus[j],2)
    return tuple(L),tuple(tuple(row) for row in M)

def green_current(A,p,B,q):
    Q=add(p,q);L,M=green_coefficients(tuple(A),tuple(B),tuple(q))
    return tuple(L[i]+sum(M[i][j]*Q[j] for j in range(4)) for i in range(4))

def cubic_bv_flux(U,p,V,q,c,k):
    Q=add(p,q,k);LU=lie_matrix(U,p,k,c);LV=lie_matrix(V,q,k,c)
    jU=green_current(LU,add(p,k),V,q)
    jV=green_current(LV,add(q,k),U,p)
    current=tuple(2*c[i]*v2(U,p,V,q)-2*jU[i]-2*jV[i] for i in range(4))
    # Only derivatives of the untouched field enter the Euler-Lagrange pairing.
    euler=v2(LU,neg(q),V,q)+v2(LV,neg(p),U,p)
    cubic=v3(gauge_matrix(k,c),k,U,p,V,q)
    return dict(total=Q,current=current,divergence=dot(Q,current),
                cubic=cubic,euler=2*euler,ward_lhs=cubic+2*euler,
                density_flux=2*dot(Q,c)*v2(U,p,V,q),green_currents=(jU,jV))
