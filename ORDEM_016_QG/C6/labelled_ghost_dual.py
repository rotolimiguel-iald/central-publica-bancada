"""Metric dual of the existing ghost bitensor, preserving radial line labels.

Input H^a_b has X contravariant / Y covariant slots. The dual H_a^b
is gX_ac H^c_d gY^{db}. Metric compatibility permits dualization AFTER
covariant differentiation, but BEFORE pairing/distribution extension.
No covariance or Grassmann sign is assigned here.
"""
from functools import lru_cache
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T


def dualize(fetch, order, ind):
    assert order in (0,1)
    a,b=ind
    terms=list(fetch(order,ind))
    if order:
        for j in range(4):
            terms.extend((T.B.gX1[a,j]*v,p,w) for v,p,w in fetch(0,(j,b)))
            terms.extend((-T.B.gY1[j,b]*v,p,w) for v,p,w in fetch(0,(a,j)))
    return L.clean(terms)


@lru_cache(None)
def cov(order, ind, xword=(), yword=()):
    return dualize(lambda o,ids:M.cov('ghost',o,ids,xword,yword),order,ind)


@lru_cache(None)
def euler(order, ind, yword=()):
    return dualize(lambda o,ids:M.euler('ghost',o,ids,yword),order,ind)


def pair_contact(ind1, kind2, ind2, xword2=(), yword1=(), yword2=(), order=1):
    return sum(L.pair(euler(j,ind1,yword1),(),M.cov(kind2,order-j,ind2,xword2,yword2),()) for j in range(order+1))
