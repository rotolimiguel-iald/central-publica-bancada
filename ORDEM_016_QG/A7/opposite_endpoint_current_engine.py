"""Current at X, ghost interaction at Y; external h(X), c(Y).

Only the connected two-contraction graph is constructed. The separate mean
current expansion sign is not included. No fitting to a Ward residual.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
import sympy as s
from classical_current_jet_engine import current_coefficients, split_word
from position_metric_bubble_engine import BASIS, LABELS
from localized_ghost_boundary_engine import ghost_localized_data
from metric_current_insertion_engine_v2 import fiber
from mixed_b_h_current_engine_v3 import current_terms
from full_loop_extension_engine import x, z, propagator_derivative, dx

def external_adjoint(hword, cword, lam, eta):
    """All external jets: prod[-(d+lambda)] prod[d-eta]."""
    out={():F(1)}
    for i,derivative,constant in [(i,-1,-lam[i]) for i in hword]+[(i,1,-eta[i]) for i in cword]:
        nxt={}
        for word,coefficient in out.items():
            w=tuple(sorted(word+(i,)))
            nxt[w]=nxt.get(w,F())+derivative*coefficient
            nxt[word]=nxt.get(word,F())+constant*coefficient
        out={w:c for w,c in nxt.items() if c}
    return out

def split_derivatives(word):
    for mask in product((0,1),repeat=len(word)):
        yield tuple(word[i] for i,b in enumerate(mask) if not b),tuple(word[i] for i,b in enumerate(mask) if b)

class OppositeEndpointCurrent:
    def __init__(self,external_h_index,r,lam,eta,point=None):
        self.lam=tuple(lam); self.eta=tuple(eta); self.point=point
        self.a=external_h_index; self.r=r
        self.Y=[ghost_localized_data(B,F(1),self.eta) for B in BASIS]
        self.metric={};self.mixed={}
        self._build()

    @staticmethod
    def add(out,hword,cword,line_h,line_c,value):
        key=tuple(sorted(hword)),tuple(sorted(cword)),tuple(sorted(line_h)),tuple(sorted(line_c))
        out[key]=out.get(key,F())+F(value)

    def ghost_slots(self,b,internal_c):
        W0,W1=self.Y[b][:2]
        for hjet in [-1,0,1,2,3]:
            W=W0 if hjet<0 else W1[hjet]
            hw=() if hjet<0 else (hjet,)
            for row,cols in enumerate(W):
                if row%4!=self.r:continue
                cw=() if row<4 else (row//4-1,)
                for col,v in cols.items():
                    if col%4!=internal_c:continue
                    bw=() if col<4 else (col//4-1,)
                    yield hw,cw,bw,v

    def _build(self):
        if not any(self.lam):return
        for internal_c in range(4):
            slots=[tuple(self.ghost_slots(b,internal_c)) for b in range(10)]
            for h_internal in range(10):
                coeff=current_coefficients(self.a,h_internal,internal_c)
                for monomial,vector in coeff.items():
                    current=sum(self.lam[mu]*vector[mu] for mu in range(4))
                    if not current:continue
                    pw,qw,kw=split_word(monomial)
                    for b in range(10):
                        sf=fiber(h_internal,b)
                        if not sf:continue
                        for hw,cw,bw,v in slots[b]:
                            # Cmetric_real=+Jraw/(16kappa); GD=-4kappa*S*f.
                            # Hessian 1/2 cancels the two choices of external h.
                            value=-F(1,4)*current*sf*v*(-1)**(len(hw)+len(bw))
                            self.add(self.metric,pw,cw,qw+hw,kw+bw,value)
            for (nu,a,pw,kw),current in current_terms(internal_c,self.lam).items():
                if a!=self.a:continue
                for b,(i,j) in enumerate(LABELS):
                    for hw,cw,bw,v in slots[b]:
                        for derivative,mult in [(i,int(j==nu)),(j,int(i==nu))]:
                            if not mult:continue
                            # <b(X)h(Y)>=-G^T(d)f; cX barY is positive.
                            value=-current*v*mult*(-1)**(len(hw)+len(bw))
                            self.add(self.mixed,pw,cw,hw+(derivative,),kw+bw,value)
        self.metric={k:v for k,v in self.metric.items() if v}
        self.mixed={k:v for k,v in self.mixed.items() if v}

    @lru_cache(None)
    def scalar(self,word):
        value=propagator_derivative(tuple(sorted(word)))
        if self.point is None:return value
        return F(value.subs(dict(zip(x,self.point))).subs(z,sum(v*v for v in self.point)))

    def off_diagonal(self,kind):
        ans=0
        for (pw,cw,hw,kw),value in getattr(self,kind).items():
            for word,adj in external_adjoint(pw,cw,self.lam,self.eta).items():
                for left,right in split_derivatives(word):
                    ans+=value*adj*self.scalar(tuple(sorted(hw+left)))*self.scalar(tuple(sorted(kw+right)))
        return s.expand(ans) if self.point is None else ans

    def symbolic_after_product(self,kind):
        """Independent adjunction applied after explicitly multiplying kernels."""
        blocks={}
        for (pw,cw,hw,kw),v in getattr(self,kind).items():
            blocks[pw,cw]=blocks.get((pw,cw),s.Integer(0))+v*propagator_derivative(hw)*propagator_derivative(kw)
        ans=s.Integer(0)
        for (pw,cw),f in blocks.items():
            f=s.expand(f)
            for i in pw:f=s.expand(-dx(f,i)-self.lam[i]*f)
            for i in cw:f=s.expand(dx(f,i)-self.eta[i]*f)
            ans+=f
        return s.expand(ans)
