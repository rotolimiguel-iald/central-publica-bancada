"""Source h-star/c bubble: external ghost IBP before anchoring Y.

Coordinate components, first curvature. Common propagator constants stripped.
Only the singular kernels are present. No extension/Fourier or tadpole.
"""
from functools import lru_cache
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E

class SourcePoint:
    def __init__(self,point):
        self.point=tuple(point);self.z=sum(t*t for t in point)
        assert self.z>0
        self.xmap=dict(zip(B.x,point))
    @lru_cache(None)
    def jet(self,kind,o,ids,xi=-1,yi=-1,extra_y=-1):
        f=E.xyjet(kind,o,ids,() if yi<0 else (yi,),xi)
        if extra_y>=0:f=B.derivative(f,'Y',extra_y)
        return s.expand(B.anchored(f).subs(self.xmap).subs(B.w,self.z))
    def hj(self,o,a,b,mu,nu,xi=-1,yi=-1,extra_y=-1):
        f=self.jet('metric',o,(a,b,mu,nu),xi,yi,extra_y)
        # Trace reversal at Y. Metric/inverse metric have zero first Y jet
        # at Y=0, so their extra partial_Y contribution is zero here.
        if mu==nu:f-=sum(self.jet('metric',o,(a,b,t,t),xi,yi,extra_y) for t in range(4))/2
        return f
    @lru_cache(None)
    def component(self,o,a,b,r):
        """A_ab,r - partial_Yj B^j_ab,r at Y=0, c^r external."""
        ans=0
        for go in range(o+1):
            ho=o-go
            for m in range(4):
                for mu in range(4):
                    for nu in range(4):
                        # Lie_c h = c^m D_m h_ab+h_am D_b c^m+h_bm D_a c^m.
                        for c,e,xi,gxi in [(a,b,m,-1),(a,m,-1,b),(b,m,-1,a)]:
                            g=self.jet('ghost',go,(m,nu),gxi,mu)
                            ans-=g*self.hj(ho,c,e,mu,nu,xi,r)
                            # B^j multiplies D_j c^r and carries the same overall minus.
                            for j in range(4):
                                def hcomb(extra=-1):
                                    v=0
                                    if j==mu:v+=self.jet('metric',ho,(c,e,r,nu),xi,-1,extra)
                                    if j==nu:v+=self.jet('metric',ho,(c,e,mu,r),xi,-1,extra)
                                    if mu==nu:v-=self.jet('metric',ho,(c,e,j,r),xi,-1,extra)
                                    return v
                                gj=self.jet('ghost',go,(m,nu),gxi,mu,j)
                                ans+=gj*hcomb()+g*hcomb(j)
        return s.expand(ans)
