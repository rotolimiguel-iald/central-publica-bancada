"""Direct nonminimal ghost bubble after one exact integration by parts.

Vertex = -(nabla_mu barc_nu) [c^rho nabla_rho h_mu_nu
 +h_rho_nu nabla_mu c^rho+h_mu_rho nabla_nu c^rho
 -.5g_mu_nu(c^rho nabla_rho trh+2h_rho_lambda nabla_lambda c^rho)].
No determinant factorization. Auxiliary Euclidean spaceform, first K.
"""
from position_metric_bubble_engine import empty,lincomb,mul,frob,sandwich,LABELS,BASIS
from position_metric_ordered_operator_engine import external_jets
from functools import lru_cache
from fractions import Fraction as F

SIZE=20
def green(x):
    z=sum(a*a for a in x);G0=empty(SIZE);G1=empty(SIZE);GL=empty(SIZE)
    def omega(i,j,a,b):return int(a==i and b==j)-int(a==j and b==i)
    def A(i,a,b):return sum(x[j]*omega(j,i,a,b) for j in range(4))
    for a in range(4):
        G0[a][a]=z*z;G1[a][a]=3*z*z;GL[a][a]=-15*z*z
        for i in range(4):
            G0[4*(i+1)+a][a]=-2*x[i]*z;G0[a][4*(i+1)+a]=2*x[i]*z
            for b in range(4):
                d=int(a==b)
                v=6*z*A(i,a,b)-30*z*x[i]*d
                if v:G1[4*(i+1)+a][b]=v
                v=6*z*A(i,a,b)+30*z*x[i]*d
                if v:G1[a][4*(i+1)+b]=v
                for j in range(4):
                    if d:G0[4*(i+1)+a][4*(j+1)+b]=2*int(i==j)*z-8*x[i]*x[j]
                    N=z*int(i==j)-x[i]*x[j]
                    v=4*N*d+6*z*omega(i,j,a,b)-12*x[i]*A(j,a,b)+12*x[j]*A(i,a,b)
                    v+=30*(int(i==j)*z-2*x[i]*x[j])*d
                    if v:G1[4*(i+1)+a][4*(j+1)+b]=v
    return G0,G1,GL,z**3,12*z*z

@lru_cache(None)
def vertex(A):
    h=lambda a,b:A[4*a+b];t=sum(h(i,i) for i in range(4))
    W2=empty(SIZE);W1=[empty(SIZE) for _ in range(4)]
    for rho in range(4):
        for nu in range(4):
            for mu in range(4):
                b=4*(mu+1)+nu
                v=-h(mu,nu)+F(1,2)*int(mu==nu)*t
                if v:W1[rho][rho][b]=v
                for lam in range(4):
                    a=4*(lam+1)+rho
                    v=-(int(lam==mu)*h(rho,nu)+int(lam==nu)*h(mu,rho)-int(mu==nu)*h(lam,rho))
                    if v:W2[a][b]=v
    return W2,W1

def weighted(vec,n,i):
    terms=[]
    for a,c in enumerate(vec):
        if c:terms.append((c,vertex(BASIS[a])[0] if n==2 else vertex(BASIS[a])[1][i]))
    return lincomb(*terms) if terms else empty(SIZE)

def direct_node(A,B,p,x,order):
    G0,G1,GL,d0,d1=green(x);z=sum(a*a for a in x);b2,b1=vertex(B)
    specs=[(2,-1)]+[(1,i) for i in range(4)];value=F();log=F()
    # Directed ghost contraction uses the transpose of the second vertex.
    from position_metric_bubble_engine import transpose
    for nx,xi in specs:
        for ny,yj in specs:
            BY=transpose(b2 if ny==2 else b1[yj]);sign=-1 if ny==1 else 1
            for r in range(order+1):
                n=nx+ny-2*r;o=order-r
                jets=external_jets(A,p,o,n,xi,yj)
                vec=[F() for _ in range(10)]
                for w,den,v in jets:
                    fac=F(1,den)
                    for i in w:fac*=x[i]
                    for a in range(10):vec[a]+=fac*v[a]
                if not any(vec):continue
                WX=weighted(vec,nx,xi)
                c0=F(frob(sandwich(G0,WX),BY),d0*d0)
                if r==0:c=c0;l=F()
                else:
                    c=F(frob(sandwich(G0,WX,G1),BY)+frob(sandwich(G1,WX,G0),BY),d0*d1)-F(z,2)*c0
                    l=F(frob(sandwich(G0,WX,GL),BY)+frob(sandwich(GL,WX,G0),BY),d0*d1)
                value+=sign*z*z*c;log+=sign*z*z*l
    return value,log
