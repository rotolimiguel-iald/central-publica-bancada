# Joint-symbol successor; predecessor SHA256 248aca63ee15567f3f4c73f3ec16b266714dd1cc9dd0752c28861f9accb15224
"""Actual -Qbarc.c.dc x Vghost graph using the previously checked dual Euler.

The external ghost is a parallel vector at X, the metric jet is at Y.
Two Wick matchings have opposite signs; no temporal graph weight.
"""
from functools import lru_cache
import sympy as s
import labelled_ghost_dual as D
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T
from smooth_line_compatibility_check_v2 import multiply
from mixed_b_h_current_engine_v3 import current_terms
from position_metric_bubble_engine import LABELS
from balanced_tensor_transport_engine import balanced_euler_line,Q
R=s.symbols("R0:4")


@lru_cache(None)
def kernel(i,r,t,bar,kw,xw,mu,order):
    return s.expand(sum(L.pair(D.euler(j,(i,r),kw),(),M.cov('ghost',order-j,(t,bar),xw,(mu,)),()) for j in range(order+1)))


@lru_cache(None)
def external_vector(pol):
    X=s.Matrix(T.x);P1=(T.xx*s.eye(4)-X*X.T)/6
    b=s.eye(4)[:,pol];b1=P1[:,pol]
    grad={(t,u):s.expand(s.diff(b1[u],T.x[t])+T.gamma(T.x,u,t,pol)) for t in range(4) for u in range(4)}
    return b,b1,grad


def component(label,pol,order,joint=False):
    b,b1,grad=external_vector(pol);out=0;terms=0
    flip=lambda q:q.subs({v:-v for v in Q},simultaneous=True)
    for r in range(4):
        for mu in range(4):
            unit=tuple(int(i==mu) for i in range(4))
            for (bar,A,hw,kw),zcoef in current_terms(r,unit).items():
                if A!=label:continue
                hfactor=s.prod(-(R if joint else Q)[k] for k in hw)
                for u in range(4):
                    for t in range(4):
                        # First matching: Ebarc_u--cY_r, cX_t--barcY_bar,
                        # leaving (nabla_t c^u)_X. Wick sign +.
                        # Second matching: Ebarc_t--cY_r, nabla_u cX_t--barcY_bar,
                        # leaving cX_u. Wick sign -.
                        cases=[(u,(),Q[t],b[u],b1[u],1),
                               (t,(u,),s.S.One,b[u],b1[u],-1)]
                        if order:cases.append((u,(),s.S.One,s.S.Zero,grad[t,u],1))
                        for first,xw,external_derivative,c0,c1,sign in cases:
                            for m,coefficient in enumerate((c0,) if order==0 else (c0,c1)):
                                if coefficient==0:continue
                                k=kernel(first,r,t,bar,kw,xw,mu,order-m)
                                if k==0:continue
                                # Multiplication differentiates the parallel coefficient;
                                # Q->-Q evaluates the distribution on the +ip X wave.
                                out-=s.Rational(zcoef)*sign*hfactor*external_derivative*flip(multiply(coefficient,k))
                                terms+=1
    return s.expand(out),terms


def flat_reference(label,pol):
    out=0
    for r in range(4):
        for mu in range(4):
            unit=tuple(int(i==mu) for i in range(4))
            for (bar,A,hw,kw),zcoef in current_terms(r,unit).items():
                if A!=label:continue
                cases=[(r,(bar,),(),1)]
                if r==bar:cases += [(j,(),(j,),-1) for j in range(4)]
                for u,external_c,internal_c,sign in cases:
                    if u!=pol:continue
                    bw=(mu,)
                    k=balanced_euler_line(tuple(sorted(kw)),tuple(sorted(internal_c+bw)))
                    v=-s.Rational(zcoef)*sign*(-1)**(len(kw)+len(bw))*k*s.prod(-Q[j] for j in external_c)*s.prod(Q[j] for j in hw)
                    out+=v.subs({q:-q for q in Q},simultaneous=True)
    return s.expand(out)
