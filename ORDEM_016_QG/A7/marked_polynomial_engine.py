"""Sparse-polynomial principal BV algebra, no IO and no fitted tensor ansatz.

q0..q3 are loop/direction variables; a,b,c parametrize p=a e0,r=b e0+c e1.
Fiber sums are contracted by Itr on symmetric tensors, independently of the
ten-coordinate contraction in marked_vertex_engine.
"""
from fractions import Fraction
from sympy.polys.rings import ring
from sympy.polys.domains import QQ

R,*VARS=ring('q0,q1,q2,q3,a,b,c',QQ)
q=VARS[:4];a,b,c=VARS[4:]
ZERO=R.zero;ONE=R.one
I=[[ONE if i==j else ZERO for j in range(4)] for i in range(4)]
axes=[[ONE if i==j else ZERO for j in range(4)] for i in range(4)]
P=[a,ZERO,ZERO,ZERO];Q=[b,c,ZERO,ZERO]
def add(x,y):return [u+v for u,v in zip(x,y)]
def scale(x,t):return [v*t for v in x]
def dot(x,y):return sum((u*v for u,v in zip(x,y)),ZERO)
def trace(H):return sum((H[i][i] for i in range(4)),ZERO)
def madd(A,B):return [[A[i][j]+B[i][j] for j in range(4)] for i in range(4)]
def mscale(A,t):return [[v*t for v in row] for row in A]
def inner(A,B):return sum((A[i][j]*B[i][j] for i in range(4) for j in range(4)),ZERO)
def mv(H,v):return [dot(row,v) for row in H]
def outer(x,y):return [[u*v for v in y] for u in x]
def sym(x,y):return mscale(madd(outer(x,y),outer(y,x)),QQ(1,2))
def itr(H):return madd(H,mscale(I,-trace(H)/2))
def gauge(k,u):return madd(outer(k,u),outer(u,k))
def lie(H,p,k,u):return madd(mscale(H,dot(p,u)),gauge(k,mv(H,u)))
def C(H,p):return add(mv(H,p),scale(p,-trace(H)/2))
def bracket(p,v,r,w):return add(scale(w,dot(v,r)),scale(v,-dot(w,p)))
def R0(p,v):
    return madd(mscale(gauge(p,v),-QQ(3,8)*dot(p,p)),mscale(outer(p,p),dot(p,v)/2))
def source_duals(T,k,l):
    t=mv(T,l)
    return [madd(mscale(T,k[m]),gauge(axes[m],t)) for m in range(4)]
def ghost_duals(k,l,v):
    """B_n with tr(B_n H)=[V(H,k,l)v]_n, independent index derivation."""
    r=add(k,l);kv=dot(k,v);rl=dot(r,l)
    result=[]
    for n in range(4):
        B=madd(mscale(sym(axes[n],r),kv),mscale(sym(axes[n],v),rl))
        B=madd(B,mscale(sym(v,r),l[n]))
        B=madd(B,mscale(I,-r[n]*kv/2))
        B=madd(B,mscale(sym(v,l),-r[n]))
        result.append(mscale(B,-1))
    return result
def ghost_matrix(H,k,l):
    cols=[list(map(lambda B:inner(B,H),ghost_duals(k,l,e))) for e in axes]
    return [[cols[j][i] for j in range(4)] for i in range(4)]
def eh2(A,B,p):return dot(p,p)*inner(A,itr(B))-2*dot(C(A,p),C(B,p))
def cubic_gauge(A,pa,B,pb,k,v):
    """16kappa V3(K_k v,A,B) from classical diffeomorphism Ward identity."""
    return -4*(eh2(lie(A,pa,k,v),B,pb)+eh2(A,lie(B,pb,k,v),pa))

def marked_numerators(T,k,u,r,v):
    """h*(T,-k-r), metric(K_k u,k), ghost(v,r)."""
    l=add(add(k,r),scale(q,-1))
    us=[itr(A) for A in source_duals(T,q,l)]
    ghostvertex=ghost_matrix(gauge(k,u),k,add(r,scale(q,-1)))
    end=ghost_duals(scale(q,-1),r,v)
    ng=sum((ghostvertex[m][n]*inner(us[m],end[n]) for m in range(4) for n in range(4)),ZERO)
    other=[itr(B) for B in ghost_duals(add(k,scale(q,-1)),r,v)]
    nm=sum((cubic_gauge(us[m],scale(q,-1),other[m],add(q,scale(k,-1)),k,u)
            for m in range(4)),ZERO)
    return ng,nm

def triangle_numerator(T,p,v,r,w):
    Y=scale(mv(T,add(p,r)),2);k=add(q,p);l=add(r,scale(q,-1))
    aa=ghost_duals(q,p,v);bb=ghost_duals(scale(q,-1),r,w)
    def contract(ds,x):
        return [[sum((x[m]*ds[m][i][j] for m in range(4)),ZERO) for j in range(4)] for i in range(4)]
    return inner(itr(contract(aa,l)),contract(bb,Y))-inner(itr(contract(aa,Y)),contract(bb,k))

def angular(exps):
    if any(x%2 for x in exps):return QQ.zero
    out=Fraction(1)
    for x in exps:
        for f in range(1,x,2):out*=f
    for j in range(sum(exps)//2):out/=4+2*j
    return QQ(out.numerator,out.denominator)

class UV:
    def __init__(self,shifts,maximum=4):
        self.m=len(shifts);self.product=[ONE]+[ZERO]*maximum
        for shift in shifts:
            u=2*dot(q,shift);v=dot(shift,shift);den=[ONE]
            for j in range(1,maximum+1):den.append(-u*den[j-1]-(v*den[j-2] if j>=2 else ZERO))
            self.product=[sum((self.product[i]*den[j-i] for i in range(j+1)),ZERO)
                          for j in range(maximum+1)]
    def extract(self,num):
        grouped={}
        for exps,coef in num.items():
            order=sum(exps[:4])+4-2*self.m
            if order>=0:
                assert order<len(self.product)
                grouped.setdefault(order,{})[exps]=coef
        radial=sum((R.from_dict(terms)*self.product[order] for order,terms in grouped.items()),ZERO)
        out={}
        for exps,coef in radial.items():
            av=angular(exps[:4])
            if av:
                key=(0,0,0,0)+exps[4:]
                out[key]=out.get(key,QQ.zero)+coef*av
        return R.from_dict({k:v for k,v in out.items() if v})

ZERO4=[ZERO]*4
UVLG=UV([ZERO4,scale(P,-1),scale(add(P,Q),-1)])
UVLM=UV([ZERO4,scale(Q,-1),scale(add(P,Q),-1)])
UVRG=UVLM
UVRM=UVLG
UVTRI=UV([ZERO4,P,scale(Q,-1)])

def ward(T,v,w):
    ln,lmn=marked_numerators(T,Q,w,P,v)
    rn,rmn=marked_numerators(T,P,v,Q,w)
    lg,lm=UVLG.extract(ln),UVLM.extract(lmn)
    rg,rm=UVRG.extract(rn),UVRM.extract(rmn)
    tri=UVTRI.extract(triangle_numerator(T,P,v,Q,w))
    free=inner(T,madd(madd(R0(add(P,Q),bracket(P,v,Q,w)),
                    mscale(lie(R0(Q,w),Q,P,v),-1)),lie(R0(P,v),P,Q,w)))
    return tri+free-lg+lm/4+rg-rm/4,(tri,free,lg,lm,rg,rm)
