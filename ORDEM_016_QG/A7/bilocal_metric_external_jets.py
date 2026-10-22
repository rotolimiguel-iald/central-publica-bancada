"""Metric pair with explicit endpoint jets and curvature vertices, first K."""
from functools import lru_cache
from fractions import Fraction as F
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E
from bilocal_ghost_pair_engine import PointJets,frame2,tensor,multiplicity
import position_metric_ordered_operator_engine as M
from position_metric_bubble_engine import empty,frob,sandwich,lincomb,LABELS

class MetricPointJets(PointJets):
    def _get_cache(self):
        @lru_cache(None)
        def coord(order,indices,xi,yi,word):
            f=E.xyjet('metric',order,indices,() if yi<0 else (yi,),xi).subs(self.xmap)
            for j in reversed(word):
                f=s.expand(s.diff(f,B.y[j])-2*(self.point[j]-B.y[j])*(s.diff(f,B.w)+s.diff(f,B.L)/B.w))
            return s.expand(B.anchored(f).subs(B.w,self.z))
        @lru_cache(None)
        def framed(order,indices,xi,yi,word):
            f=coord(order,indices,xi,yi,word)
            if order:
                for pos in (0,1):
                    a=indices[pos]
                    for c in range(4):
                        ids=indices[:pos]+(c,)+indices[pos+1:]
                        f+=F(self.z*int(a==c)-self.point[a]*self.point[c],6)*coord(0,ids,xi,yi,word)
                if xi>=0:
                    for c in range(4):
                        f+=F(self.z*int(xi==c)-self.point[xi]*self.point[c],6)*coord(0,indices,c,yi,word)
                if len(word)==2:
                    i,j=word
                    for pos in (2,3):
                        a=indices[pos]
                        for c in range(4):
                            ids=indices[:pos]+(c,)+indices[pos+1:]
                            f+=frame2(i,j,a,c)*coord(0,ids,xi,yi,())
                    if yi>=0:
                        for c in range(4):f+=frame2(i,j,yi,c)*coord(0,indices,xi,c,())
            f=s.expand(f);assert s.diff(f,B.L,2)==0
            return tuple(F(f.coeff(B.L,k)) for k in (0,1))
        return framed
    @lru_cache(None)
    def matrix(self,order,word=()):
        out=[empty(50),empty(50)]
        for i in range(50):
            xi=i//10-1;a,b=LABELS[i%10]
            for j in range(50):
                yi=j//10-1;c,d=LABELS[j%10]
                for ell,v in enumerate(self.get(order,(a,b,c,d),xi,yi,tuple(word))):
                    if v:out[ell][i][j]=v
        return tuple(out)

def metric_ward_point(point,T,progress=None,jets=None,derivative_index=None):
    J=jets if jets is not None else MetricPointJets(point)
    assert J.point==tuple(point)
    # The EH principal vertex was stored in its Fourier convention; relative
    # position-space sign of the algebraic curvature vertex is negative.
    AX=([M.vertex_data(tuple(T))[0],lincomb((F(-1),M.potential(tuple(T))))] if derivative_index is None else [M.vertex_data(tuple(T))[1][derivative_index],empty(50)])
    def C(order,word,BY):
        if not word:parts=[((),())]
        elif len(word)==1:parts=[(word,()),((),word)]
        else:
            a,b=word;parts=[(word,()),((a,),(b,)),((b,),(a,)),((),word)]
        out=[F(),F()]
        for ex in range(order+1):
            for u,v in parts:
                for r in range(order-ex+1):
                    U=J.matrix(r,u);V=J.matrix(order-ex-r,v)
                    for ell in (0,1):
                        for e in range(ell+1):out[ell]+=F(frob(sandwich(U[e],AX[ex],V[ell-e]),BY),16)
        return out
    @lru_cache(None)
    def BY(n,j,a,b):
        h=tensor(a,b)
        return M.vertex_data(h)[0] if n==0 else M.vertex_data(h)[1][j]
    def d2vertex(i,j,k,a,b):
        h=tensor(a,b);D=[[frame2(i,j,u,v) for v in range(4)] for u in range(4)]
        changed=tuple(sum(D[u][r]*h[4*r+v]+h[4*u+r]*D[v][r] for r in range(4)) for u in range(4) for v in range(4))
        return lincomb((F(1),M.vertex_data(changed)[1][k]),
                       *[(D[l][k],M.vertex_data(h)[1][l]) for l in range(4)])
    result=[]
    for order in (0,1):
        rows=[]
        for b in range(4):
            out=[F(),F()]
            for a in range(4):
                m=multiplicity(a,b);val=C(order,(a,),BY(0,-1,a,b))
                if order:
                    pot=C(0,(a,),lincomb((F(-1),M.potential(tensor(a,b)))))
                    val=[v+p for v,p in zip(val,pot)]
                for ell in (0,1):out[ell]-=2*val[ell]/m
                for j in range(4):
                    val=C(order,(a,j),BY(1,j,a,b))
                    for ell in (0,1):out[ell]+=2*val[ell]/m
                    if order:
                        val=C(0,(),d2vertex(a,j,j,a,b))
                        for ell in (0,1):out[ell]+=2*val[ell]/m
                if order:
                    v1=C(0,(),BY(1,a,a,b));v2=C(0,(),BY(1,b,a,a))
                    for ell in (0,1):out[ell]+=F(8,3)*v1[ell]/m-F(2,3)*v2[ell]
            rows.append(tuple(out))
            if progress:progress(order,b,rows[-1])
        result.append(tuple(rows))
    return tuple(result),J
