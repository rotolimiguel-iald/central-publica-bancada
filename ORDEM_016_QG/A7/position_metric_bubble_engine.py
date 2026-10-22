"""Sparse, exact position-space contraction of the differentiated metric bubble.

Vertices act on (undifferentiated field, four differentiated fields) x ten
symmetric tensor components. All I/O stays in runners. K^1 expressions are
radial-frame profiles; no integrated covariant Hessian is inferred here.
"""
from functools import lru_cache
from itertools import permutations
from math import factorial
from fractions import Fraction as F
from metric_principal_vertices import (I,basis,gamma2,contraction,upper_product,
                                       trace,eh_cubic_16k,clear_caches)
from metric_coincident_jet_engine_v2 import metric_fiber

SIZE=50
ZERO4=(0,0,0,0)
AXES=[tuple(int(i==j) for i in range(4)) for j in range(4)]
LABELS=[(i,j) for i in range(4) for j in range(i,4)]
BASIS=[basis(i,j) for i,j in LABELS]
def empty(n=SIZE):return [{} for _ in range(n)]
def transpose(A):
    out=empty(len(A))
    for i,row in enumerate(A):
        for j,x in row.items():out[j][i]=x
    return out
def mul(A,B):
    out=empty(len(A))
    for i,row in enumerate(A):
        dst=out[i]
        for k,a in row.items():
            for j,b in B[k].items():dst[j]=dst.get(j,0)+a*b
        out[i]={j:v for j,v in dst.items() if v}
    return out
def lincomb(*terms):
    out=empty(len(terms[0][1]))
    for c,A in terms:
        if not c:continue
        for i,row in enumerate(A):
            for j,v in row.items():out[i][j]=out[i].get(j,0)+c*v
    return [{j:v for j,v in row.items() if v} for row in out]
def frob(A,B):return sum(v*A[i].get(j,0) for i,row in enumerate(B) for j,v in row.items())
def sandwich(G,A,Q=None):return mul(mul(transpose(G),A),G if Q is None else Q)
def sparse(M):return [{j:int(M[i,j]) for j in range(M.cols) if M[i,j]} for i in range(M.rows)]
def block(out,i,j,M,c=1):
    for a,row in enumerate(M):
        for b,v in row.items():
            if v:out[10*i+a][10*j+b]=out[10*i+a].get(10*j+b,0)+c*v

@lru_cache(None)
def fiber_data():
    f=metric_fiber()
    S2=sparse(2*f['S0']);gg=sparse(f['g']*f['g'].T)
    oms={key:sparse(M) for key,M in f['omega'].items()}
    return S2,gg,oms

def green_integer(x):
    """Numerators G0/(2z³), G1/(24z²), G1_L/(24z²)."""
    x=tuple(x);z=sum(v*v for v in x);S2,gg,oms=fiber_data()
    A2=[lincomb(*[(x[j],oms[j,i]) for j in range(4)]) for i in range(4)]
    AS=[mul(A,S2) for A in A2]
    G0,G1,GL=empty(),empty(),empty()
    block(G0,0,0,S2,z*z);block(G1,0,0,S2,3*z*z);block(GL,0,0,gg,12*z*z)
    for i in range(4):
        block(G0,i+1,0,S2,-2*x[i]*z);block(G0,0,i+1,S2,2*x[i]*z)
        block(G1,i+1,0,lincomb((6*z,AS[i]),(24*z*x[i],gg)))
        block(G1,0,i+1,lincomb((6*z,AS[i]),(-24*z*x[i],gg)))
        for j in range(4):
            delta=int(i==j);n=z*delta-x[i]*x[j]
            block(G0,i+1,j+1,S2,2*delta*z-8*x[i]*x[j])
            part=lincomb((4*n,S2),(6*z,mul(oms[i,j],S2)),
                (-12*x[i],AS[j]),(12*x[j],AS[i]),(24*(-delta*z+2*x[i]*x[j]),gg))
            block(G1,i+1,j+1,part)
    return G0,G1,GL,2*z**3,24*z*z

def cubic_from_gammas(fields,gs):
    result=0
    for i,j,k in permutations(range(3)):
        A=fields[i];G,T=gs[j],gs[k]
        result+=trace(A)*contraction(I,G,T)-2*contraction(A,G,T)
        result-=2*contraction(I,upper_product(A,G),T)
        result-=2*contraction(I,G,upper_product(A,T))
    return result
def gamma_gradient(grad):
    return tuple(grad[mu][4*nu+rho]+grad[nu][4*mu+rho]-grad[rho][4*mu+nu]
                 for rho in range(4) for mu in range(4) for nu in range(4))

@lru_cache(None)
def vertex_data(A):
    """W2, four W1 momentum coefficients, four twice-W1 connection coefficients."""
    W2=empty();W1=[empty() for _ in range(4)];WC2=[empty() for _ in range(4)]
    # Two internally differentiated legs, external derivative absent.
    for i in range(4):
        for a,Ea in enumerate(BASIS):
            ia=10*(i+1)+a
            for j in range(4):
                for b,Eb in enumerate(BASIS):
                    jb=10*(j+1)+b
                    if jb<ia:continue
                    v=eh_cubic_16k(A,ZERO4,Ea,AXES[i],Eb,AXES[j])
                    if v:W2[ia][jb]=v;W2[jb][ia]=v
    f=metric_fiber();avec=[A[4*i+j] for i,j in LABELS]
    cg=[]
    for j in range(4):
        grad=[]
        for i in range(4):
            D=f['omega'][j,i]
            values=[sum(int(D[a,b])*avec[b] for b in range(10)) for a in range(10)]
            lookup={pair:v for pair,v in zip(LABELS,values)}
            grad.append(tuple(lookup[min(a,b),max(a,b)] for a in range(4) for b in range(4)))
        cg.append(gamma_gradient(grad))
    zg=(0,)*64
    for j in range(4):
        for i in range(4):
            for a,Ea in enumerate(BASIS):
                ia=10*(i+1)+a
                for b,Eb in enumerate(BASIS):
                    v=eh_cubic_16k(A,AXES[j],Ea,AXES[i],Eb,ZERO4)
                    c=cubic_from_gammas([A,Ea,Eb],[cg[j],gamma2(Ea,AXES[i]),zg])
                    if v:W1[j][ia][b]=v;W1[j][b][ia]=v
                    if c:WC2[j][ia][b]=c;WC2[j][b][ia]=c
    clear_caches()
    return W2,W1,WC2

def contracted_node(A,B,p,x,curved=True):
    """Return flat, K-constant and K-log profiles before angular averaging /16."""
    x=tuple(x);p=tuple(p);z=sum(v*v for v in x);px=sum(a*b for a,b in zip(p,x))
    G0,G1,GL,d0,d1=green_integer(x)
    a2,a1,ac=vertex_data(tuple(A));b2,b1,_=vertex_data(tuple(B))
    VX={1:lincomb(*[(-p[i],a1[i]) for i in range(4)]),2:a2}
    VY={1:lincomb(*[(p[i],b1[i]) for i in range(4)]),2:b2}
    flat=F();curve=F();log=F()
    for nx in (1,2):
        C0=sandwich(G0,VX[nx])
        C1=lincomb((1,sandwich(G0,VX[nx],G1)),(1,sandwich(G1,VX[nx],G0))) if curved else None
        CL=lincomb((1,sandwich(G0,VX[nx],GL)),(1,sandwich(GL,VX[nx],G0))) if curved else None
        for ny in (1,2):
            n=nx+ny;c0=frob(C0,VY[ny])
            flat+=F((-1)**n*px**n*c0,factorial(n)*d0*d0)
            if curved:
                factor=F((-1)**(n-1)*px**(n-2),factorial(n-2))
                curve+=factor*(F(frob(C1,VY[ny]),d0*d1)-F(z*c0,2*d0*d0))
                log+=factor*F(frob(CL,VY[ny]),d0*d1)
    if curved:
        # Six times the external coframe momentum correction: -(z*p-x(px)).
        wp6=lincomb(*[(-(z*p[i]-x[i]*px),a1[i]) for i in range(4)])
        # Twice the external connection correction, excluding its -i.
        wc2=lincomb(*[(x[i],ac[i]) for i in range(4)])
        CP=sandwich(G0,wp6);CC=sandwich(G0,wc2)
        for ny in (1,2):
            n=1+ny
            curve+=F((-1)**(n-1)*px**(n-2)*frob(CP,VY[ny]),factorial(n-2)*6*d0*d0)
            curve+=F((-1)**n*px**(n-1)*frob(CC,VY[ny]),factorial(n-1)*2*d0*d0)
    return tuple(value*z*z/16 for value in (flat,curve,log))
