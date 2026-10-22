"""Real covariant polynomial jets and the measured quadratic Ward primitive.

Pure code. Series coefficients are in K, with no Fourier phase removed.
The normal connection is the existing spaceform connection through K^2.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from spaceform_covariant_jet_engine import ZERO, mono, plus, times, deriv, connection


def scale(p, c):
    return {e: c*v for e, v in p.items() if c*v}


def splits(word):
    for mask in range(1 << len(word)):
        yield (tuple(x for i, x in enumerate(word) if mask & (1 << i)),
               tuple(x for i, x in enumerate(word) if not mask & (1 << i)))


def polynomial_jet(initial, rank):
    @lru_cache(None)
    def field(word, indices, order):
        if not word:
            return initial(indices, order)
        i, rest = word[0], word[1:]
        terms = [deriv(field(rest, indices, order), i)]
        all_indices = rest + indices
        for slot, target in enumerate(all_indices):
            for a in range(4):
                changed = all_indices[:slot] + (a,) + all_indices[slot+1:]
                for ko in range(1, order+1):
                    lower = field(changed[:-rank], changed[-rank:], order-ko) if rank else field(changed, (), order-ko)
                    if lower:
                        terms.append(scale(times(connection(ko, a, i, target), lower), -1))
        return plus(*terms)

    @lru_cache(None)
    def jet(word, indices, order):
        return field(tuple(word), tuple(indices), order).get(ZERO, F())
    return jet


def spaceform_metric_initial(indices, order):
    a, b = indices
    z = plus(*(mono((i, i)) for i in range(4)))
    N = plus(scale(z, int(a == b)), mono((a, b), -1))
    if order == 0:
        return {ZERO: F(int(a == b))} if a == b else {}
    return scale(N, F(-1, 3)) if order == 1 else scale(times(z, N), F(2, 45))


def lower_vector_initial(vector):
    def initial(indices, order):
        return plus(*(times(spaceform_metric_initial((indices[0], b), order), vector[b]) for b in range(4)))
    return initial


def scalar_product(chi, tensor):
    @lru_cache(None)
    def jet(word, indices, order):
        return sum((chi(u, (), k)*tensor(v, indices, order-k)
                    for u, v in splits(word) for k in range(order+1)), F())
    return jet


def pair_product(left, li, right, ri, word, order):
    return sum((left(u, li, k)*right(v, ri, order-k)
                for u, v in splits(word) for k in range(order+1)), F())


def lie_tensor(vector, tensor):
    @lru_cache(None)
    def jet(word, indices, order):
        a, b = indices
        total = F()
        for u, v in splits(word):
            for k in range(order+1):
                for r in range(4):
                    total += vector(u, (r,), k)*tensor(v+(r,), (a, b), order-k)
                    total += tensor(u, (r, b), k)*vector(v+(a,), (r,), order-k)
                    total += tensor(u, (a, r), k)*vector(v+(b,), (r,), order-k)
        return total
    return jet


def vector_bracket(left, right):
    @lru_cache(None)
    def jet(word, indices, order):
        b = indices[0]
        return sum((left(u, (r,), k)*right(v+(r,), (b,), order-k)
                    -right(u, (r,), k)*left(v+(r,), (b,), order-k)
                    for u, v in splits(word) for k in range(order+1) for r in range(4)), F())
    return jet


def ward_operator(tensor, parameter):
    """deltaH_t in real covariant derivatives; coefficients from prior fit."""
    t = F(parameter)
    d1, d2, d3, d4 = F(1,2)-t/2, F(9,4)+t/2, -1-t/2, t
    e1, e2 = t+F(7,3), -t-F(22,3)

    @lru_cache(None)
    def jet(word, indices, order):
        a, b = indices
        def h(w, i, j, k):
            return tensor(word+w, (i, j), k)
        def sym(i, j, a, b, k):
            return (h((i,j), a,b,k)+h((j,i), a,b,k))/2
        total = F()
        if order:
            k = order-1
            total -= d1*sum(h((i,i),a,b,k) for i in range(4))
            if a == b:
                total -= d2*sum(h((i,i),m,m,k) for i in range(4) for m in range(4))
            total -= d3*sum(sym(a,b,m,m,k) for m in range(4))
            if a == b:
                total -= d3*sum(sym(i,j,i,j,k) for i in range(4) for j in range(4))
            total -= d4/2*sum(sym(a,i,i,b,k)+sym(b,i,i,a,k) for i in range(4))
        if order >= 2:
            total += e1*h((),a,b,order-2)
            if a == b:
                total += e2*sum(h((),m,m,order-2) for m in range(4))
        return total
    return jet


def localized_operator(chi, tensor, parameter):
    left = scalar_product(chi, ward_operator(tensor, parameter))
    right = ward_operator(scalar_product(chi, tensor), parameter)
    @lru_cache(None)
    def jet(word, indices, order):
        return (left(word, indices, order)+right(word, indices, order))/2
    return jet
