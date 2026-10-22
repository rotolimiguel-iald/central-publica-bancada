"""Regulator-only endpoint Y defects; pure code, first curvature.

Return coefficients of a,a² and L^0,L^1 with the common rho^(2a) stripped.
The geometric correction to the Hessian of log rho² is also returned
separately, allowing comparison with the coordinate-distance completion.
"""
from fractions import Fraction as F
from functools import lru_cache
import sympy as s
import bilocal_ghost_external_jets as BG
import bilocal_metric_external_jets as BM
import ghost_direct_position_engine as G
import position_metric_ordered_operator_engine as M
from position_metric_bubble_engine import empty,transpose,frob,sandwich,lincomb
from bilocal_source_divergence_engine import SourcePoint

def loop_defect_point(kind,point,T,derivative_index=None,jets=None):
    metric=kind=='metric';size=50 if metric else 20
    J=jets if jets is not None else (BM.MetricPointJets(point) if metric else BG.PointJets(point))
    z=J.z;x=J.point
    if metric:
        data=M.vertex_data(tuple(T))
        AX=[data[0],lincomb((F(-1),M.potential(tuple(T))))] if derivative_index is None else [data[1][derivative_index],empty(size)]
    else:
        data=G.vertex(tuple(T))
        AX=[data[0] if derivative_index is None else data[1][derivative_index]]
    def contraction(o,word,BY):
        if o<0:return [F(),F()]
        parts=[((),())] if not word else [(word,()),((),word)]
        assert len(word)<=1
        out=[F(),F()]
        for ex in range(min(o,len(AX)-1)+1):
            for u,v in parts:
                for r in range(o-ex+1):
                    U=J.matrix(r,u);V=J.matrix(o-ex-r,v)
                    for ell in (0,1):
                        for e in range(ell+1):
                            val=frob(sandwich(U[e],AX[ex],V[ell-e]),BY if metric else transpose(BY))
                            out[ell]+=F(val,16) if metric else val
        return out
    @lru_cache(None)
    def vertex(n,j,a,b):
        h=BG.tensor(a,b)
        val=M.vertex_data(h) if metric else G.vertex(h)
        return val[0] if n==0 else val[1][j]
    def f(i):return F(-2*x[i],z)
    def h0(i,j):return F(2*int(i==j),z)-F(4*x[i]*x[j],z*z)
    def h1(i,j):return F(-2,3)*(int(i==j)-F(x[i]*x[j],z))
    result=[];geometric=[]
    for o in (0,1):
        rows=[];grows=[]
        for b in range(4):
            out=[[F(),F()],[F(),F()]];geom=[F(),F()]
            for a in range(4):
                mult=F(2,BG.multiplicity(a,b))
                c=contraction(o,(),vertex(0,-1,a,b))
                if metric and o:
                    pot=contraction(0,(),lincomb((F(-1),M.potential(BG.tensor(a,b)))))
                    c=[v+w for v,w in zip(c,pot)]
                for ell in (0,1):out[0][ell]-=mult*f(a)*c[ell]
                for j in range(4):
                    V=vertex(1,j,a,b)
                    c=contraction(o,(),V)
                    ca=contraction(o,(a,),V) if f(j) else [F(),F()]
                    cj=contraction(o,(j,),V) if f(a) else [F(),F()]
                    flat=contraction(0,(),V) if o and h1(a,j) else [F(),F()]
                    for ell in (0,1):
                        g=mult*h1(a,j)*flat[ell] if o else F()
                        geom[ell]+=g
                        out[0][ell]+=mult*(f(a)*cj[ell]+f(j)*ca[ell]+h0(a,j)*c[ell])+g
                        out[1][ell]+=mult*f(a)*f(j)*c[ell]
            rows.append(out);grows.append(geom)
        result.append(rows);geometric.append(grows)
    return result,geometric,J

class SourceYDefect(SourcePoint):
    @lru_cache(None)
    def regulator_coefficient(self,o,a,b,r):
        """Coefficient of a in -dY(log rho²) B; first Y jet is common to both completions."""
        ans=0
        for go in range(o+1):
            ho=o-go
            for m in range(4):
                for mu in range(4):
                    for nu in range(4):
                        for c,e,xi,gxi in [(a,b,m,-1),(a,m,-1,b),(b,m,-1,a)]:
                            g=self.jet('ghost',go,(m,nu),gxi,mu)
                            for j in range(4):
                                if not self.point[j]:continue
                                h=0
                                if j==mu:h+=self.jet('metric',ho,(c,e,r,nu),xi)
                                if j==nu:h+=self.jet('metric',ho,(c,e,mu,r),xi)
                                if mu==nu:h-=self.jet('metric',ho,(c,e,j,r),xi)
                                ans-=s.Rational(2*self.point[j],self.z)*g*h
        return s.expand(ans)
