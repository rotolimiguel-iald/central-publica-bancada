"""Full Schur Euler hh block through K, retaining labelled radial words.

HD=-4*kappa*P; ell=1/(2*kappa); P=H_h I_tr.
S=ell C HD-HQ Kstar=-2 C P-HQ Kstar.
PH_hh=I_tr Lh P-Cstar S; density is applied once at X.
All four free tensor slots are covariant. No graph/Grassmann weights here.
"""
from functools import lru_cache
from itertools import product
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T


def scaled(terms, coeff):
    return tuple((coeff*v,p,w) for v,p,w in terms)


@lru_cache(None)
def mixed_ward(order, nu, c, d, xword=()):
    terms=[]
    # Metric compatibility keeps inverse metric outside all differentiated contractions.
    for a,b in product(range(4),repeat=2):
        for m in range(order+1):
            coefficient=T.delta(a,b) if m==0 else -T.B.gX1[a,b]
            terms.extend(scaled(M.cov('metric',order-m,(b,nu,c,d),xword+(a,),()),-2*coefficient))
            terms.extend(scaled(M.cov('metric',order-m,(a,b,c,d),xword+(nu,),()),coefficient))
    # The kernel of HQ Kstar is the positive Y symmetrized derivative,
    # after integrating Kstar=-2 div by parts. Lower its X vector index.
    for j in range(4):
        for m in range(order+1):
            coefficient=T.delta(nu,j) if m==0 else T.B.gX1[nu,j]
            terms.extend(scaled(M.cov('ghost',order-m,(j,d),xword,(c,)),-coefficient))
            terms.extend(scaled(M.cov('ghost',order-m,(j,c),xword,(d,)),-coefficient))
    return L.clean(terms)


@lru_cache(None)
def cstar_mixed(order, ind):
    a,b,c,d=ind
    terms=list(scaled(mixed_ward(order,b,c,d,(a,)),-T.s.Rational(1,2)))
    terms.extend(scaled(mixed_ward(order,a,c,d,(b,)),-T.s.Rational(1,2)))
    for i,j in product(range(4),repeat=2):
        for m in range(order+1):
            coefficient=T.delta(a,b)*T.delta(i,j) if m==0 else T.B.gX1[a,b]*T.delta(i,j)-T.delta(a,b)*T.B.gX1[i,j]
            terms.extend(scaled(mixed_ward(order-m,j,c,d,(i,)),coefficient/2))
    return L.clean(terms)


@lru_cache(None)
def euler(order, ind):
    a,b,c,d=ind
    terms=list(M.euler('metric',order,ind))
    # Trace reverse the OUTPUT of Lh P, including the first metric jets.
    for i,j in product(range(4),repeat=2):
        for m in range(order+1):
            coefficient=T.delta(a,b)*T.delta(i,j) if m==0 else T.B.gX1[a,b]*T.delta(i,j)-T.delta(a,b)*T.B.gX1[i,j]
            terms.extend(scaled(M.euler('metric',order-m,(i,j,c,d)),-coefficient/2))
    terms.extend(scaled(cstar_mixed(order,ind),-1))
    if order:terms.extend(scaled(cstar_mixed(0,ind),T.xx/2))
    return L.clean(terms)


def pair_contact(ind1, kind2, ind2, xword2=(), yword2=(), order=1):
    return T.s.expand(sum(L.pair(euler(j,ind1),(),M.cov(kind2,order-j,ind2,xword2,yword2),()) for j in range(order+1)))
