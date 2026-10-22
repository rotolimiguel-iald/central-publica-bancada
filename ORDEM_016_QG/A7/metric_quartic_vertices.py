"""Quartic derivative EH vertex: integer 32*kappa*V4, modulo divergence.

Fixed background orthonormal frame. Derivative momenta include the same
Fourier factors as metric_principal_vertices. Polarization is not divided
by 4!, and undifferentiated matrices are never assumed to commute.
"""
from itertools import combinations
from metric_principal_vertices import I, trace, inner, gamma2, upper_product, contraction

def mm(A,B):
    return tuple(sum(A[4*i+k]*B[4*k+j] for k in range(4))
                 for i in range(4) for j in range(4))

def second_coefficient_4(A,B,G,T):
    """Four times d_A d_B [sqrt(g) g^-1 (g^-1 G)(g^-1 T)]."""
    ta,tb=trace(A),trace(B)
    AB=tuple(a+b for a,b in zip(mm(A,B),mm(B,A)))
    WAB=tuple((ta*tb-2*inner(A,B))*e-2*ta*b-2*tb*a+4*ab
              for e,a,b,ab in zip(I,A,B,AB))
    WA=tuple(2*ta*e-4*a for e,a in zip(I,A))
    WB=tuple(2*tb*e-4*b for e,b in zip(I,B))
    AG,BG=upper_product(A,G),upper_product(B,G)
    AT,BT=upper_product(A,T),upper_product(B,T)
    return (contraction(WAB,G,T)
        -contraction(WA,BG,T)-contraction(WA,G,BT)
        -contraction(WB,AG,T)-contraction(WB,G,AT)
        +4*contraction(I,upper_product(AB,G),T)
        +4*contraction(I,G,upper_product(AB,T))
        +4*contraction(I,AG,BT)+4*contraction(I,BG,AT))

def eh_quartic_32k(*fields):
    """Fields are four (symmetric row-major tuple, momentum tuple) pairs."""
    assert len(fields)==4
    gammas=[gamma2(H,tuple(p)) for H,p in fields]
    answer=0
    for i,j in combinations(range(4),2):
        k,l=[a for a in range(4) if a not in (i,j)]
        A,B=fields[i][0],fields[j][0]
        answer+=second_coefficient_4(A,B,gammas[k],gammas[l])
        answer+=second_coefficient_4(A,B,gammas[l],gammas[k])
    return answer
