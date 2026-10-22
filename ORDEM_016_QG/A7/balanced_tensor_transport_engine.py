"""Preserve two derivative words until applying the declared balanced extension."""
from functools import lru_cache
import sympy as s
from balanced_pair_normalization_check_v2 import correction
from full_loop_extension_engine import SymbolicRawLoop,propagator_derivative,Q,differential_operator

WORDS={}
@lru_cache(None)
def atom(word):
    word=tuple(sorted(word));name='g_'+(''.join(map(str,word)) or 'empty')
    obj=s.Symbol(name);WORDS[obj]=word;return obj

@lru_cache(None)
def delta_expression(expr):
    """R_bal-R_raw for homogeneous degree-two formal line derivatives, divided by CE."""
    out=0
    for term in s.Add.make_args(s.expand(expr)):
        if not term:continue
        c,factors=term.as_coeff_Mul();words=[]
        assert c.is_Rational,(term,c)
        for v,n in factors.as_powers_dict().items():
            assert v in WORDS and n.is_Integer and n>0,(term,v,n)
            words.extend([WORDS[v]]*int(n))
        assert len(words)==2,(term,words)
        out+=c*correction(*words)
    return s.expand(out)

def realize(expr):
    return s.expand(expr.subs({a:propagator_derivative(w) for a,w in WORDS.items()},simultaneous=True))

class FormalPairLoop(SymbolicRawLoop):
    @lru_cache(None)
    def scalar(self,word):return atom(tuple(sorted(word)))

def loop_ward_delta(engine,r):
    """Y Ward adjunction of the change in the h-h pair; not complete A2."""
    out=0;terms=0
    for ex in [-1,0,1,2,3]:
        for a in range(4):
            for j in [-1,0,1,2,3]:
                formal=engine.raw_expression(ex,j,a,r)
                change=delta_expression(formal)
                op=differential_operator(ex,j,a,engine.lx,engine.ly)
                out+=s.Rational(2,1 if a==r else 2)*sum(c*s.prod(Q[i] for i in w)*change for w,c in op.items())
                terms+=int(formal!=0)
    return s.expand(out.subs({Q[i]:Q[i]-engine.lx[i] for i in range(4)},simultaneous=True)),terms

@lru_cache(None)
def balanced_euler_line(euler_word,ghost_word):
    """The pointwise Euler sum is zero; its balanced composite extension need not be."""
    return s.expand(sum(correction(tuple(sorted(euler_word+(i,i))),tuple(sorted(ghost_word))) for i in range(4)))
