"""Actual Eh Lie_c h x Vghost contact, with the metric leg read in a parallel frame.

Constant cutoff, first curvature. Coordinate-delta polynomial Q is evaluated
on an X wave exp(-ip.x); the Y ghost jet uses +ip. No temporal graph weight.
"""
from functools import lru_cache
from itertools import product
import sympy as s
import labelled_nonminimal_metric_euler_v2 as N
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L
import tensor_euler_zerojet as T
from smooth_line_compatibility_check_v2 import multiply
from mixed_b_h_current_engine_v3 import current_terms
from position_metric_bubble_engine import LABELS,BASIS
from balanced_tensor_transport_engine import balanced_euler_line,Q


@lru_cache(None)
def upper_euler(order,ind,yword):
    a,b,c,d=ind;terms=list(N.euler(order,ind,yword))
    if order:
        for j in range(4):
            terms.extend(N.scaled(N.euler(0,(j,b,c,d),yword),-T.B.gX1[a,j]))
            terms.extend(N.scaled(N.euler(0,(a,j,c,d),yword),-T.B.gX1[b,j]))
    return L.clean(terms)


@lru_cache(None)
def line_pair(a,b,internal_h,t,hw,xw,mu,order):
    c,d=LABELS[internal_h]
    return s.expand(sum(L.pair(upper_euler(j,(a,b,c,d),hw),(),M.cov('ghost',order-j,(t,mu[0]),xw,(mu[1],)),()) for j in range(order+1)))


@lru_cache(None)
def external_metric(label):
    B=s.Matrix(4,4,[s.Rational(v) for v in BASIS[label]])
    X=s.Matrix(T.x);P1=-(T.xx*s.eye(4)-X*X.T)/6
    B1=(P1*B+B*P1.T).applyfunc(s.expand)
    grad={}
    for r,a,b in product(range(4),repeat=3):
        grad[r,a,b]=s.expand(s.diff(B1[a,b],T.x[r])-sum(T.gamma(T.x,j,r,a)*B[j,b]+T.gamma(T.x,j,r,b)*B[a,j] for j in range(4)))
    return B,B1,grad


def component(label,r,order):
    B,B1,grad=external_metric(label);out=0;terms=0
    for mu in range(4):
        unit=tuple(int(i==mu) for i in range(4))
        for (bar,A,hw,kw),zcoef in current_terms(r,unit).items():
            yfactor=s.prod(Q[k] for k in kw)
            for a,b in LABELS:
                multiplicity=1 if a==b else 2
                for t in range(4):
                    # Three Lie derivative pieces; external coefficients can carry K.
                    pieces=[((),-Q[t],B[a,b],B1[a,b]),
                            ((a,),s.S.One,B[t,b],B1[t,b]),
                            ((b,),s.S.One,B[a,t],B1[a,t])]
                    if order:pieces.append(((),s.S.One,s.S.Zero,grad[t,a,b]))
                    for xw,external_derivative,c0,c1 in pieces:
                        coefficients=(c0,) if order==0 else (c0,c1)
                        for m,coefficient in enumerate(coefficients):
                            if coefficient==0:continue
                            kernel=line_pair(a,b,A,t,hw,xw,(bar,mu),order-m)
                            if kernel==0:continue
                            out-=s.Rational(zcoef)*multiplicity*yfactor*external_derivative*multiply(coefficient,kernel)
                            terms+=1
    return s.expand(out),terms


def flat_reference(label,r):
    # Original flat contraction, restricted to the requested external component.
    out=0;index=lambda i,j:LABELS.index(tuple(sorted((i,j))))
    for mu in range(4):
        unit=tuple(int(i==mu) for i in range(4))
        for (bar,A,hw,kw),zcoef in current_terms(r,unit).items():
            i,j=LABELS[A]
            pieces=[(A,(bar,),()),(index(i,bar),(),(j,)),(index(j,bar),(),(i,))]
            for B,external_h,internal_c in pieces:
                if B!=label:continue
                bw=(mu,)
                kernel=balanced_euler_line(tuple(sorted(hw)),tuple(sorted(internal_c+bw)))
                out-=s.Rational(zcoef)*(-1)**(len(hw)+len(bw))*kernel*s.prod(-Q[k] for k in external_h)*s.prod(Q[k] for k in kw)
    return s.expand(out)
