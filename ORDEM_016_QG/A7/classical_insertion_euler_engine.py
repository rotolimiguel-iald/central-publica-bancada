"""Actual Euler contractions between qV_af and the field part of q0V_chi."""
from functools import lru_cache
from collections import defaultdict
from fractions import Fraction as F
import sympy as s
from balanced_tensor_transport_engine import balanced_euler_line,Q
from classical_current_jet_engine import current_coefficients,split_word
from mixed_b_h_current_engine_v3 import current_terms
from ghost_current_insertion_engine import current_monomials
from metric_coincident_jet_engine_v2 import metric_fiber
from position_metric_bubble_engine import LABELS

INDEX={p:i for i,p in enumerate(LABELS)}
def index(i,j):return INDEX[tuple(sorted((i,j)))]

def z_pieces(A,r):
    i,j=LABELS[A]
    return [(A,(r,),()),(index(i,r),(),(j,)),(index(j,r),(),(i,))]

def odd_pair_sign(pairs):
    slots=list(range(6));sign=1
    for a,b in pairs:
        i,j=slots.index(a),slots.index(b);assert i<j
        sign*=(-1)**(j-i-1);slots.remove(a);slots.remove(b)
    return sign

def build_terms(eta):
    """The X vertex is qVaf; Y is q0V field current. Both are odd."""
    out={k:defaultdict(F) for k in ['metric','mixed','ghost']};S=metric_fiber()['S0']
    def add(kind,rx,ry,ew,hw,ex,ey,value):
        key=(rx,ry,tuple(sorted(ew)),tuple(sorted(hw)),tuple(sorted(ex)),tuple(sorted(ey)))
        out[kind][key]+=F(value)
    # I_metric = +(d chi) Jraw/(16 kappa); its internal Hessian carries 1/2.
    # qVaf has E_A Z_A; one ordinary metric line is -4 kappa S.
    # The two matchings remove the 1/2, giving -Jraw*S/4.
    for ry in range(4):
        for A in range(10):
            for B in range(10):
                for mon,vector in current_coefficients(A,B,ry).items():
                    value=sum(F(eta[i])*vector[i] for i in range(4))
                    if not value:continue
                    pw,qw,kw=split_word(mon)
                    for rx in range(4):
                        for C,internal_h,external_c in z_pieces(A,rx):
                            sf=S[C,B]
                            if sf:
                                add('metric',rx,ry,pw,internal_h+qw,external_c,kw,
                                    -value*F(sf)*(-1)**(len(pw)+len(qw))/4)
        # I_mixed = (d chi)_mu b_nu Zbar^(mu,nu).
        for (nu,A,pw,kw),value in current_terms(ry,eta).items():
            for rx in range(4):
                for C,internal_h,external_c in z_pieces(A,rx):
                    i,j=LABELS[C]
                    for derivative,mult in [(i,int(j==nu)),(j,int(i==nu))]:
                        if mult:
                            add('mixed',rx,ry,pw,internal_h+(derivative,),external_c,kw,
                                value*mult*(-1)**len(pw))
    # (-Qbarc_i)c^j d_j c^i at X and (barc,c,c) current at Y.
    # The minus vertex and the oriented barc_X--c_Y covariance cancel.
    for value,(bar,first,second) in current_monomials(eta):
        for i in range(4):
            for j in range(4):
                xfields=[(j,()),(i,(j,))];yfields=[first,second]
                for xcontract in range(2):
                    if xfields[xcontract][0]!=bar[0]:continue
                    for ycontract in range(2):
                        if yfields[ycontract][0]!=i:continue
                        rx,ex=xfields[1-xcontract];ry,ey=yfields[1-ycontract]
                        ew=yfields[ycontract][1];hw=xfields[xcontract][1]+bar[1]
                        sign=odd_pair_sign([(0,4+ycontract),(1+xcontract,3)])
                        add('ghost',rx,ry,ew,hw,ex,ey,
                            value*sign*(-1)**(len(ew)+len(bar[1])))
    return {kind:{k:v for k,v in terms.items() if v} for kind,terms in out.items()}

def calculate(lam,eta):
    """Return c_X B(D)c_Y after integration, with switching exponential jets."""
    terms=build_terms(tuple(eta));L=tuple(a+b for a,b in zip(lam,eta))
    @lru_cache(None)
    def local(ew,hw):
        return balanced_euler_line(ew,hw).subs({Q[i]:Q[i]+eta[i] for i in range(4)},simultaneous=True)
    result={}
    for kind,entries in terms.items():
        B=s.zeros(4)
        for (rx,ry,ew,hw,ex,ey),v in entries.items():
            B[rx,ry]+=s.Rational(v)*local(ew,hw)*s.prod(-Q[i]-L[i] for i in ex)*s.prod(Q[i] for i in ey)
        result[kind]=B.applyfunc(s.expand)
    return result,{k:len(v) for k,v in terms.items()}
