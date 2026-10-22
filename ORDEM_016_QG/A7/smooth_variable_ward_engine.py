"""Flat variable-reference Ward operators, retaining the antifield source."""
import sympy as s
from position_metric_bubble_engine import LABELS
from smooth_mixed_gradient_engine import gradient_tensor,variable_hessian_component

def gauge(c,x):
    return s.Matrix(4,4,lambda a,b:s.diff(c[b],x[a])+s.diff(c[a],x[b]))

def einstein(h,x):
    def lap(f):return sum(s.diff(f,t,2) for t in x)
    tr=s.trace(h)
    C=s.Matrix([sum(s.diff(h[i,j],x[j]) for j in range(4))-s.diff(tr,x[i])/2 for i in range(4)])
    div=sum(s.diff(C[i],x[i]) for i in range(4))
    return s.Matrix(4,4,lambda a,b:s.expand(-lap(h[a,b])+int(a==b)*lap(tr)/2+
        s.diff(C[b],x[a])+s.diff(C[a],x[b])-int(a==b)*div))

def source(sector,c,w,x):
    dw=s.Matrix([s.diff(w,t) for t in x]);g=gauge(c,x)
    if sector=='metric_I':return -w*g/2-w*s.eye(4)*s.trace(g)/8-s.eye(4)*c.dot(dw)/2
    if sector=='metric_T':return -w*g/2+w*s.eye(4)*s.trace(g)/4+s.eye(4)*c.dot(dw)/4
    if sector=='ghost_I':return -(c*dw.T+dw*c.T)/16
    raise ValueError(sector)

def hessian(sector,h,w,x):
    T=gradient_tensor(sector);v=[h[a,b] for a,b in LABELS];out=s.zeros(4)
    for a,(i,j) in enumerate(LABELS):
        out[i,j]=out[j,i]=variable_hessian_component(T,a,v,w,x)
    return out

def green_current_N(sector,h,k,w,x):
    T=gradient_tensor(sector);hv=[h[a,b] for a,b in LABELS];kv=[k[a,b] for a,b in LABELS]
    current=[]
    for i in range(4):
        f=0
        for (a,b,u,j),value in T.items():
            if u==i:
                f+=s.Rational(value)*w*(-hv[a]*s.diff(kv[b],x[j])+kv[a]*s.diff(hv[b],x[j]))
        current.append(s.expand(f))
    return current

def einstein_coefficients():
    """Symmetric derivative coefficients C so E= C^ij partial_i partial_j."""
    p=s.Matrix(s.symbols('p0:4'));p2=p.dot(p);out={}
    for b,(u,v) in enumerate(LABELS):
        h=s.zeros(4);h[u,v]=h[v,u]=1
        C=h*p-p*s.trace(h)/2
        image=-p2*h+s.eye(4)*p2*s.trace(h)/2+p*C.T+C*p.T-s.eye(4)*p.dot(C)
        for a,(aa,bb) in enumerate(LABELS):
            weight=1 if aa==bb else 2
            for i in range(4):
                for j in range(4):
                    value=s.diff(image[aa,bb],p[i],p[j])/2
                    if value:out[a,b,i,j]=weight*value
    return out

def green_current_E(h,k,x):
    C=einstein_coefficients();hv=[h[a,b] for a,b in LABELS];kv=[k[a,b] for a,b in LABELS]
    current=[]
    for i in range(4):
        f=0
        for (a,b,u,j),value in C.items():
            if u==i:f+=value*(hv[a]*s.diff(kv[b],x[j])-kv[a]*s.diff(hv[b],x[j]))
        current.append(s.expand(f))
    return current
