"""Directed ghost pair with explicit endpoint derivatives before anchoring.

Pointwise off-diagonal first-K calculation; no distribution extension or
Fourier transform. Vertex matrices retain their existing normalization.
"""
from functools import lru_cache
from fractions import Fraction as F
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E
import ghost_direct_position_engine as G
from position_metric_bubble_engine import empty,transpose,frob,sandwich,BASIS,LABELS

def frame2(i,j,a,b):
    return F(2*int(i==j)*int(a==b)-int(a==i)*int(b==j)-int(a==j)*int(b==i),6)

class PointJets:
    def __init__(self,point):
        self.point=tuple(point);self.z=sum(t*t for t in point)
        assert self.z>0
        self.xmap=dict(zip(B.x,point))
        self.get=self._get_cache()
    def _get_cache(self):
        @lru_cache(None)
        def coord(order,a,b,xi,yi,word):
            yw=() if yi<0 else (yi,)
            # Covariant derivatives of the propagator at X/Y belong to internal legs.
            f=E.xyjet('ghost',order,(a,b),yw,xi).subs(self.xmap)
            # These additional derivatives differentiate the whole frame components.
            for j in reversed(word):
                f=s.expand(s.diff(f,B.y[j])-2*(self.point[j]-B.y[j])*(s.diff(f,B.w)+s.diff(f,B.L)/B.w))
            f=s.expand(B.anchored(f).subs(B.w,self.z))
            return f
        @lru_cache(None)
        def framed(order,a,b,xi,yi,word):
            f=coord(order,a,b,xi,yi,word)
            if order:
                # Upper X ghost vector transforms by the coframe, with a minus sign.
                for c in range(4):
                    f-=F(self.z*int(a==c)-self.point[a]*self.point[c],6)*coord(0,c,b,xi,yi,word)
                    if xi>=0:
                        f+=F(self.z*int(xi==c)-self.point[xi]*self.point[c],6)*coord(0,a,b,c,yi,word)
                # First derivatives of the radial inverse frame vanish at Y=0.
                if len(word)==2:
                    i,j=word
                    for c in range(4):
                        f+=frame2(i,j,b,c)*coord(0,a,c,xi,yi,())
                        if yi>=0:f+=frame2(i,j,yi,c)*coord(0,a,b,xi,c,())
            f=s.expand(f)
            assert s.diff(f,B.L,2)==0
            return tuple(F(f.coeff(B.L,k)) for k in (0,1))
        return framed
    @lru_cache(None)
    def matrix(self,order,word=()):
        mats=[empty(20),empty(20)]
        for i in range(20):
            xi=i//4-1;a=i%4
            for j in range(20):
                yi=j//4-1;b=j%4
                values=self.get(order,a,b,xi,yi,tuple(word))
                for ell,v in enumerate(values):
                    if v:mats[ell][i][j]=v
        return tuple(mats)

def multiplicity(a,b):return 1 if a==b else 2
def tensor(a,b):return tuple(int((i==a and j==b) or (i==b and j==a)) for i in range(4) for j in range(4))

def ghost_ward_point(point,T,progress=None,jets=None):
    """Coefficient of undifferentiated c_b, with only h_X present, Dh_X=0.

    T specifies the local orthonormal tensor jet at X. No global extension
    of that test is inferred. Results are (K order,b,log power) coefficients.
    """
    J=jets if jets is not None else PointJets(point)
    assert J.point==tuple(point)
    AX=G.vertex(tuple(T))[0]
    def C(order,word,BY):
        # Derivatives of G^T AX G by the full product rule.
        parts=[]
        if not word:parts=[((),())]
        elif len(word)==1:parts=[(word,()),((),word)]
        else:
            a,b=word;parts=[(word,()),((a,),(b,)),((b,),(a,)),((),word)]
        out=[F(),F()]
        for u,v in parts:
            for r in range(order+1):
                U=J.matrix(r,u);V=J.matrix(order-r,v)
                for ell in range(2):
                    for e in range(ell+1):
                        out[ell]+=frob(sandwich(U[e],AX,V[ell-e]),transpose(BY))
        return out
    @lru_cache(None)
    def Bval(n,j,a,b):
        h=tensor(a,b);v=G.vertex(h)
        return v[0] if n==0 else v[1][j]
    def d2vertex(i,j,k,a,b):
        h=tensor(a,b);D=[[frame2(i,j,u,v) for v in range(4)] for u in range(4)]
        changed=tuple(sum(D[u][r]*h[4*r+v]+h[4*u+r]*D[v][r] for r in range(4)) for u in range(4) for v in range(4))
        out=G.vertex(changed)[1][k]
        from position_metric_bubble_engine import lincomb
        return lincomb((F(1),out),*[(D[l][k],G.vertex(h)[1][l]) for l in range(4)])
    result=[]
    for order in (0,1):
        rows=[]
        for b in range(4):
            out=[F(),F()]
            for a in range(4):
                m=multiplicity(a,b)
                val=C(order,(a,),Bval(0,-1,a,b))
                for ell in range(2):out[ell]-=2*val[ell]/m
                for j in range(4):
                    val=C(order,(a,j),Bval(1,j,a,b))
                    for ell in range(2):out[ell]+=2*val[ell]/m
                    if order:
                        val=C(0,(),d2vertex(a,j,j,a,b))
                        for ell in range(2):out[ell]+=2*val[ell]/m
                if order:
                    v1=C(0,(),Bval(1,a,a,b));v2=C(0,(),Bval(1,b,a,a))
                    for ell in range(2):out[ell]+=F(8,3)*v1[ell]/m-F(2,3)*v2[ell]
            rows.append(tuple(out))
            if progress:progress(order,b,rows[-1])
        result.append(tuple(rows))
    return tuple(result),J
