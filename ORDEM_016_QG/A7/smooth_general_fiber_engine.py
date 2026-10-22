"""Exact mixed contact for a general real coincident reference fiber."""
from fractions import Fraction as F
from functools import lru_cache
import sympy as s
import position_metric_ordered_operator_engine as M
import ghost_direct_position_engine as G
from position_metric_bubble_engine import empty,lincomb,frob,sandwich,transpose,LABELS,BASIS
from smooth_mixed_gradient_engine import fiber_metric

def delta(a,b):return int(a==b)
INDEX={v:a for a,v in enumerate(LABELS)}
def idx(a,b):return INDEX[tuple(sorted((a,b)))]
def metric_fiber_basis(left,right):
    return tuple(F(int((a==left and b==right) or (a==right and b==left)))
                 for a in range(10) for b in range(10))

@lru_cache(None)
def mixed_tensor(fiber,metric=True):
    n=10 if metric else 4
    assert len(fiber)==n*n
    W=empty(5*n);J=empty(5*n)
    for a in range(n):
        for b in range(n):
            w=fiber[n*a+b]
            if w:W[a][b]=w
            if metric:
                i,j=LABELS[a];k,l=LABELS[b]
                f=F(delta(i,k)*delta(j,l)+delta(i,l)*delta(j,k)-delta(i,j)*delta(k,l),2)
            else:f=F(delta(a,b))
            if f:
                for i in range(4):J[n*(i+1)+a][n*(i+1)+b]=f/4
    vertices=[(M.vertex_data(v) if metric else G.vertex(v)) for v in BASIS]
    mixed={}
    for a in range(10):
        for i in range(4):
            V=vertices[a][1][i]
            mixed[a,i]=lincomb((1,sandwich(J,V,W)),(1,sandwich(W,V,J)))
    out={};factor=F(-1,32) if metric else F(1)
    for b in range(10):
        for j in range(4):
            V=vertices[b][1][j]
            if not metric:V=transpose(V)
            for a in range(10):
                for i in range(4):
                    v=factor*frob(mixed[a,i],V)
                    if v:out[a,b,i,j]=v
    return out

def general_source(fiber,c,w,x):
    """Reference W=f(center)*constant symmetric fiber, including first Y jet."""
    def W(a,b,c,e):return s.Rational(fiber[10*idx(a,b)+idx(c,e)])
    S=s.Matrix(4,4,lambda a,r:sum(W(a,m,r,m) for m in range(4)))
    trace=s.Matrix(4,4,lambda a,b:sum(W(a,b,m,m) for m in range(4)))
    out=s.zeros(4)
    for a in range(4):
        for b in range(4):
            out[a,b]=-w*sum((delta(j,b)*S[a,r]+delta(j,a)*S[b,r]
                   +W(a,j,b,r)+W(b,j,a,r)-2*W(a,b,j,r))*s.diff(c[r],x[j])
                   for j in range(4) for r in range(4))/4
            out[a,b]-=(S[a,b]+S[b,a]-trace[a,b])*sum(c[r]*s.diff(w,x[r]) for r in range(4))/8
    return out.applyfunc(s.expand)

def general_hessian(fiber,h,w,x):
    T=mixed_tensor(fiber);hv=[h[a,b] for a,b in LABELS];out=s.zeros(4)
    for a,(u,v) in enumerate(LABELS):
        value=-sum(s.Rational(co)*s.diff(w*s.diff(hv[b],x[j]),x[i])
                    for (aa,b,i,j),co in T.items() if aa==a)/fiber_metric(a)
        out[u,v]=out[v,u]=s.expand(value)
    return out

def general_current(fiber,h,k,w,x):
    T=mixed_tensor(fiber);hv=[h[a,b] for a,b in LABELS];kv=[k[a,b] for a,b in LABELS]
    return [s.expand(sum(w*s.Rational(co)*(-hv[a]*s.diff(kv[b],x[j])+kv[a]*s.diff(hv[b],x[j]))
            for (a,b,u,j),co in T.items() if u==i)) for i in range(4)]
