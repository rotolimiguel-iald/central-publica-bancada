"""Unintegrated first-external-derivative tensor of flat mixed contacts."""
from fractions import Fraction as F
from functools import lru_cache
import position_metric_ordered_operator_engine as M
import ghost_direct_position_engine as G
from position_metric_bubble_engine import empty,lincomb,frob,sandwich,transpose,LABELS,BASIS

def delta(a,b):return int(a==b)
@lru_cache(None)
def gradient_tensor(sector):
    metric=sector in ('metric_I','metric_T');n=10 if metric else 4
    W=empty(5*n);J=empty(5*n)
    for a in range(n):
        for b in range(n):
            if metric:
                i,j=LABELS[a];k,l=LABELS[b]
                identity=F(delta(i,k)*delta(j,l)+delta(i,l)*delta(j,k),2)
                trace=delta(i,j)*delta(k,l);fiber=identity-F(trace,2)
                w=identity if sector=='metric_I' else trace
            else:fiber=delta(a,b);w=fiber
            if w:W[a][b]=w
            for i in range(4):
                if fiber:J[n*(i+1)+a][n*(i+1)+b]=F(fiber,4)
    vertices=[(M.vertex_data(v) if metric else G.vertex(v)) for v in BASIS]
    factor=F(-1,32) if metric else F(1)
    mixed={}
    for a in range(10):
        for i in range(4):
            V=vertices[a][1][i]
            mixed[a,i]=lincomb((1,sandwich(J,V,W)),(1,sandwich(W,V,J)))
    out={}
    for b in range(10):
        for j in range(4):
            V=vertices[b][1][j]
            if not metric:V=transpose(V)
            for a in range(10):
                for i in range(4):
                    value=factor*frob(mixed[a,i],V)
                    if value:out[a,b,i,j]=value
    return out

def fiber_metric(a):
    i,j=LABELS[a]
    return 1 if i==j else 2

def variable_hessian_component(T,a,h,w,x):
    """N_w=-partial_i(w T_ij partial_j), converted from bilinear to tensor."""
    import sympy as s
    return s.expand(-sum(s.Rational(co)*s.diff(w*s.diff(h[b],x[j]),x[i])
        for (aa,b,i,j),co in T.items() if aa==a)/fiber_metric(a))
