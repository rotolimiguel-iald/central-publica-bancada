"""First-K Einstein operator on polynomial tensor fields in RNC.

Fields include exp(q.x); q is an arbitrary complex formal momentum.
All input/output tensor indices are covariant coordinate indices.
"""
import sympy as s
from curved_source_jet_engine import x,metric1,z as radial_z,L as radial_log
Z=sum(t*t for t in x)
I=s.eye(4)
g1=s.Matrix(4,4,lambda a,b:metric1(a,b).subs('z',Z))
inv1=-g1
def ex(a):return s.expand(a)
def gamma(c,a,b):return -(s.KroneckerDelta(c,b)*x[a]+s.KroneckerDelta(c,a)*x[b]-2*s.KroneckerDelta(a,b)*x[c])/3
def derivative(f,i,q):return ex(s.diff(f,x[i])+2*x[i]*(s.diff(f,radial_z)+s.diff(f,radial_log)/radial_z)+q[i]*f)
def gradient_tensor(h,q):
    out=[]
    for o in (0,1):
        out.append([s.Matrix(4,4,lambda a,b:ex(derivative(h[o][a,b],i,q)-
          (sum(gamma(c,i,a)*h[0][c,b]+gamma(c,i,b)*h[0][a,c] for c in range(4)) if o else 0))) for i in range(4)])
    return out
def scalar_box(f,q):
    flat=sum(derivative(derivative(f[0],i,q),i,q) for i in range(4))
    curve=sum(derivative(derivative(f[1],i,q),i,q)-sum(gamma(c,i,i)*derivative(f[0],c,q) for c in range(4)) for i in range(4))
    curve+=sum(inv1[i,j]*derivative(derivative(f[0],j,q),i,q) for i in range(4) for j in range(4))
    return [ex(flat),ex(curve)]
def gauge(v,q):
    return [s.Matrix(4,4,lambda a,b:ex(derivative(v[o][b],a,q)+derivative(v[o][a],b,q)-
       (2*sum(gamma(c,a,b)*v[0][c] for c in range(4)) if o else 0))) for o in (0,1)]
def einstein(h,q):
    dh=gradient_tensor(h,q)
    trace=[s.trace(h[0]),ex(s.trace(h[1])+s.trace(inv1*h[0]))]
    C=[]
    for o in (0,1):
        C.append([ex(sum(dh[o][i][i,b] for i in range(4))-
                    derivative(trace[o],b,q)/2+
                    (sum(inv1[i,j]*dh[0][i][j,b] for i in range(4) for j in range(4)) if o else 0)) for b in range(4)])
    GC=gauge(C,q)
    divC=[ex(sum(derivative(C[0][i],i,q) for i in range(4))),
      ex(sum(derivative(C[1][i],i,q)-sum(gamma(c,i,i)*C[0][c] for c in range(4)) for i in range(4))+
         sum(inv1[i,j]*derivative(C[0][j],i,q) for i in range(4) for j in range(4)))]
    bt=scalar_box(trace,q);boxes=[]
    for o in (0,1):
        def entry(a,b):
            val=sum(derivative(dh[o][i][a,b],i,q) for i in range(4))
            if o:
                val+=sum(inv1[i,j]*derivative(dh[0][j][a,b],i,q) for i in range(4) for j in range(4))
                val-=sum(gamma(c,i,i)*dh[0][c][a,b]+gamma(c,i,a)*dh[0][i][c,b]+gamma(c,i,b)*dh[0][i][a,c] for i in range(4) for c in range(4))
            return ex(val)
        boxes.append(s.Matrix(4,4,entry))
    return [(-boxes[0]+I*bt[0]/2+GC[0]-I*divC[0]).applyfunc(ex),
       (-boxes[1]+I*bt[1]/2+g1*bt[0]/2+GC[1]-I*divC[1]-g1*divC[0]+2*h[0]+I*trace[0]).applyfunc(ex)]
def parallel_tensor(T):
    X=s.Matrix(x)
    return [T,(-Z*T/3+(X*X.T*T+T*X*X.T)/6).applyfunc(ex)]
def density(h):
    return [h[0],(h[1]+inv1*h[0]+h[0]*inv1-Z*h[0]/2).applyfunc(ex)]
