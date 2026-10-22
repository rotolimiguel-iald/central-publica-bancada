"""Two directed Wick contractions of the three-odd-field cutoff current."""
from functools import lru_cache
from itertools import product
from fractions import Fraction as F
import sympy as s
from localized_ghost_boundary_engine import ghost_localized_data
from full_loop_extension_engine import x,z,Q,propagator_derivative,contact
from metric_current_insertion_engine_v2 import opword

def current_monomials(eta):
    """Ordered fields (barc_nu, c_rho, c_nu), each as (component, derivative word)."""
    for mu,nu,rho in product(range(4),repeat=3):
        if not eta[mu]:continue
        yield F(eta[mu]),((nu,(mu,)),(rho,()),(nu,(rho,)))
        yield -F(eta[mu]),((nu,()),(rho,(mu,)),(nu,(rho,)))
        yield -F(eta[mu]),((nu,()),(rho,()),(nu,tuple(sorted((mu,rho)))))

def contraction_terms(r,eta,omit=None):
    """Key: (barYcomp,barYword,cYcontractcomp,cYcontractword,external_c_word).

    In the ordered product (barX,cX,barY,cYA,cYB), contracting barX with
    cYA has Wick sign+, covariance sign-; with cYB signs- and-.
    Thus total signs are respectively -,+ before endpoint derivatives.
    """
    out={}
    for coefficient,(bar,first,second) in current_monomials(eta):
        for option,contracted,external,sign in [(0,first,second,-1),(1,second,first,1)]:
            if option==omit or external[0]!=r:continue
            key=bar+contracted+(external[1],)
            out[key]=out.get(key,F())+sign*coefficient
    return {key:c for key,c in out.items() if c}

class GhostCurrentInsertion:
    def __init__(self,T,r,lam,eta,point=None,omit=None):
        self.lam=tuple(lam);self.eta=tuple(eta);self.point=point
        self.AX=ghost_localized_data(tuple(T),F(1),self.lam)
        self.terms=contraction_terms(r,self.eta,omit)
    @lru_cache(None)
    def scalar(self,word):
        value=propagator_derivative(tuple(sorted(word)))
        if self.point is None:return value
        return F(value.subs(dict(zip(x,self.point))).subs(z,sum(t*t for t in self.point)))
    @lru_cache(None)
    def raw(self,ex,kw,word=()):
        W=self.AX[0] if ex<0 else self.AX[1][ex];ans=0
        for (nu,bw,rho,cw,k),coefficient in self.terms.items():
            if k!=kw:continue
            for i,row in enumerate(W):
                if i%4!=nu:continue
                iw=() if i<4 else (i//4-1,)
                for j,v in row.items():
                    if j%4!=rho:continue
                    jw=() if j<4 else (j//4-1,)
                    for mask in product((0,1),repeat=len(word)):
                        u=tuple(word[a] for a,t in enumerate(mask) if not t)
                        t=tuple(word[a] for a,b in enumerate(mask) if b)
                        ans+=coefficient*v*(-1)**(len(bw)+len(cw))*self.scalar(iw+bw+u)*self.scalar(jw+cw+t)
        return s.expand(ans) if self.point is None else ans
    def off_diagonal(self):
        return s.expand(sum(c*self.raw(ex,kw,w)
            for kw in sorted({key[-1] for key in self.terms})
            for ex in [-1,0,1,2,3]
            for w,c in opword(kw,ex,self.lam,self.eta).items()))
    def extension_contact(self):
        assert self.point is None
        ans=s.Integer(0)
        for kw in sorted({key[-1] for key in self.terms}):
            for ex in [-1,0,1,2,3]:
                f=self.raw(ex,kw)
                for word,c in opword(kw,ex,self.lam,self.eta).items():
                    if word:ans-=c*contact(f,word)
        return s.expand(ans.subs({Q[i]:Q[i]-self.lam[i] for i in range(4)},simultaneous=True))
