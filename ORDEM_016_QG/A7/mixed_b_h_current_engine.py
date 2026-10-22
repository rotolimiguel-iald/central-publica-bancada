"""Ordered mixed b-h/current contraction; no global Ward diagram weight."""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
import sympy as s
from position_metric_bubble_engine import BASIS,LABELS
from localized_eh_cubic_engine import localized_vertex_data
from full_loop_extension_engine import x,z,Q,propagator_derivative,contact
from metric_current_insertion_engine_v2 import fiber,opword

def current_terms(r,eta):
    """Coefficient of b_nu h_A c_r and their jets in eta_mu b_nu Zbar_mu,nu."""
    out={}
    def add(nu,a,pw,kw,c):
        key=(nu,a,pw,kw);out[key]=out.get(key,F())+F(c)
    for mu in range(4):
        for nu in range(4):
            for a,H in enumerate(BASIS):
                h=lambda i,j:H[4*i+j]
                tr=sum(h(i,i) for i in range(4))
                add(nu,a,(r,),(),eta[mu]*(F(h(mu,nu))-F(mu==nu,2)*tr))
                add(nu,a,(),(mu,),eta[mu]*h(r,nu))
                add(nu,a,(),(nu,),eta[mu]*h(mu,r))
                for j in range(4):add(nu,a,(),(j,),-eta[mu]*int(mu==nu)*h(r,j))
    return {key:c for key,c in out.items() if c}

class MixedCurrentInsertion:
    """One ordered contraction, physical scales relative to the shared scalar GQ.

    Raw V3=16*kappa V3physical, GD=-4*kappa*S*GQ and Ghb=G*GQ.
    Their product gives -1/4 for this diagram's one metric line.
    exchange=False/True are kept distinct; expansion factorials not inserted.
    """
    def __init__(self,T,r,lam,eta,point=None):
        self.lam=tuple(lam);self.eta=tuple(eta);self.point=point
        self.AX=localized_vertex_data(tuple(T),1,self.lam)
        self.terms=current_terms(r,self.eta)
    @lru_cache(None)
    def scalar(self,word):
        value=propagator_derivative(tuple(sorted(word)))
        if self.point is None:return value
        return F(value.subs(dict(zip(x,self.point))).subs(z,sum(t*t for t in self.point)))
    @lru_cache(None)
    def h_column(self,a,pw,extra):
        out={}
        for row in range(50):
            fr=fiber(row%10,a)
            if not fr:continue
            w=(() if row<10 else (row//10-1,))+pw+extra
            v=fr*(-1)**len(pw)*self.scalar(w)
            if v:out[row]=v
        return out
    @lru_cache(None)
    def b_column(self,nu,extra):
        out={}
        for row in range(50):
            a,b=LABELS[row%10];w=(() if row<10 else (row//10-1,))+extra
            v=int(b==nu)*self.scalar(w+(a,))+int(a==nu)*self.scalar(w+(b,))
            if v:out[row]=v
        return out
    @lru_cache(None)
    def raw_component(self,ex,nu,a,pw,word=(),exchange=False):
        W=self.AX[0] if ex<0 else self.AX[1][ex];ans=0
        for mask in product((0,1),repeat=len(word)):
            u=tuple(word[i] for i,t in enumerate(mask) if not t)
            v=tuple(word[i] for i,t in enumerate(mask) if t)
            left=self.b_column(nu,u);right=self.h_column(a,pw,v)
            if exchange:left,right=right,left
            for i,l in left.items():
                for j,c in W[i].items():
                    if j in right:ans+=l*c*right[j]
        return s.expand(-s.Rational(1,4)*ans) if self.point is None else -F(ans,4)
    @lru_cache(None)
    def raw(self,ex,kw,word=(),exchange=False):
        ans=sum(c*self.raw_component(ex,nu,a,pw,word,exchange)
                for (nu,a,pw,k),c in self.terms.items() if k==kw)
        return s.expand(ans) if self.point is None else ans
    def off_diagonal(self,exchange=False):
        return s.expand(sum(c*self.raw(ex,kw,w,exchange)
            for kw in sorted({key[-1] for key in self.terms})
            for ex in [-1,0,1,2,3]
            for w,c in opword(kw,ex,self.lam,self.eta).items()))
    def extension_contact(self):
        assert self.point is None
        ans=0
        for kw in sorted({key[-1] for key in self.terms}):
            for ex in [-1,0,1,2,3]:
                f=self.raw(ex,kw)
                for word,c in opword(kw,ex,self.lam,self.eta).items():
                    if word:ans-=c*contact(f,word)
        return s.expand(ans.subs({Q[i]:Q[i]-self.lam[i] for i in range(4)},simultaneous=True))
