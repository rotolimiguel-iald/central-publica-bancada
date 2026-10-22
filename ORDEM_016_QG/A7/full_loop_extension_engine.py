"""Flat localized loop derivative/extension contacts from unreduced kernels.

Analytic pair extension R=FP[(1-a)mu^(2a)z^a .]. Cutoffs have local
exponential jets lambda and eta. No log amplitudes or curved corrections.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
import sympy as s
from flat_loop_cutoff_engine import FlatLoop,tensor
from localized_eh_cubic_engine import localized_vertex_data
from localized_ghost_boundary_engine import ghost_localized_data
from position_metric_bubble_engine import transpose,frob
import logarithmic_contact_engine as R

x=s.symbols('x0:4');z=s.Symbol('z');Q=R.Q
def dx(f,i):return s.expand(s.diff(f,x[i])+2*x[i]*s.diff(f,z))
@lru_cache(None)
def propagator_derivative(word):
    return 1/z if not word else dx(propagator_derivative(word[:-1]),word[-1])

class SymbolicRawLoop(FlatLoop):
    def __init__(self,kind,T,lambda_x,eta_y):
        super().__init__(kind,(1,0,0,0),T)
        self.lx=tuple(lambda_x);self.ly=tuple(eta_y)
        self.local_vertex=localized_vertex_data if kind=='metric' else ghost_localized_data
        self.AX=self.local_vertex(self.T,F(1),self.lx)

    @lru_cache(None)
    def scalar(self,word):return propagator_derivative(word)

    @lru_cache(None)
    def raw_expression(self,ex,y_index,a,b):
        by=self.local_vertex(tensor(a,b),F(1),self.ly)
        by=by[0] if y_index<0 else by[1][y_index]
        if self.kind=='ghost':by=transpose(by)
        value=frob(self.paired(ex,()),by)
        return s.expand(value/(16 if self.kind=='metric' else 1))

@lru_cache(None)
def terms(f):
    out=[]
    for term in s.expand(f).as_ordered_terms():
        if not term:continue
        power=term.as_powers_dict().get(z,0);n=-int(power)
        assert n>=0 and n==-power
        for powers,c in s.Poly(term*z**n,*x).terms():
            assert c.is_Rational
            out.append((n,powers,c))
    return tuple(out)

@lru_cache(None)
def monomial_contact(n,powers,word):
    """Leibniz expansion; smooth monomials commute with R, derivatives do not."""
    out=0
    for mask in product((0,1),repeat=len(word)):
        remaining=list(powers);c=s.Integer(1);rest=[]
        for i,on_monomial in zip(word,mask):
            if on_monomial:
                c*=remaining[i];remaining[i]-=1
                if c==0:break
            else:rest.append(i)
        if c==0 or not rest:continue
        v=R.contact(n,0,tuple(rest))
        for i,m in enumerate(remaining):v=(-1)**m*s.diff(v,Q[i],m)
        out+=c*v
    return s.expand(out)

def contact(f,word):
    return s.expand(sum(c*monomial_contact(n,p,tuple(sorted(word))) for n,p,c in terms(f)))

def differential_operator(ex,y_index,a,lx,ly):
    # -dYa for hY, +dYa dYj for dYj hY; dY on kernels = -d_x.
    if y_index<0:op={():-ly[a],(a,):1}
    else:
        j=y_index;op={}
        for w,c in [((),ly[a]*ly[j]),((j,),-ly[a]),((a,),-ly[j]),(tuple(sorted((a,j))),1)]:
            op[w]=op.get(w,0)+c
    if ex<0:return {w:c for w,c in op.items() if c}
    out={}
    for w,c in op.items():
        out[w]=out.get(w,0)-lx[ex]*c
        v=tuple(sorted(w+(ex,)));out[v]=out.get(v,0)-c
    return {w:c for w,c in out.items() if c}

def loop_contact(engine,r):
    out=0
    for ex in [-1,0,1,2,3]:
        for a in range(4):
            for j in [-1,0,1,2,3]:
                f=engine.raw_expression(ex,j,a,r)
                op=differential_operator(ex,j,a,engine.lx,engine.ly)
                # P=O R(f), Q=R(O f), hence P-Q=-C_O(f).
                out-=s.Rational(2,1 if a==r else 2)*sum(c*contact(f,w) for w,c in op.items() if w)
    # Remove chiX(X) to the diagonal using all its jets, not its value alone.
    return s.expand(out.subs({Q[i]:Q[i]-engine.lx[i] for i in range(4)},simultaneous=True))
