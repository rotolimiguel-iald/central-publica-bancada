"""Change in the actual five current diagrams and source diagram under R_bal."""
import ast
from functools import lru_cache
import sympy as s
from balanced_tensor_transport_engine import atom,delta_expression,correction,Q
from metric_current_insertion_engine_v3 import CurrentInsertion,opword
from mixed_b_h_current_engine_v3 import MixedCurrentInsertion
from ghost_current_insertion_engine import GhostCurrentInsertion
from opposite_endpoint_current_engine import OppositeEndpointCurrent,external_adjoint
from current_distributional_descendant_probe import rows_for
from position_metric_bubble_engine import BASIS
import localized_source_boundary_engine as source
from pathlib import Path

class FormalScalar:
    @lru_cache(None)
    def scalar(self,word):return atom(tuple(sorted(word)))
class FormalMetric(FormalScalar,CurrentInsertion):pass
class FormalMixed(FormalScalar,MixedCurrentInsertion):pass
class FormalGhost(FormalScalar,GhostCurrentInsertion):pass

def shift(f,lam):return s.expand(f.subs({Q[i]:Q[i]-lam[i] for i in range(4)},simultaneous=True))
def current_delta(engine):
    out=0
    for kw in sorted({key[-1] for key in engine.terms}):
        for ex in [-1,0,1,2,3]:
            f=engine.raw(ex,kw)
            value=delta_expression(f)
            for word,c in opword(kw,ex,engine.lam,engine.eta).items():
                out+=c*s.prod(Q[i] for i in word)*value
    return shift(out,engine.lam)

def opposite_delta(engine,kind):
    out=0
    for (pw,cw,hw,kw),v in getattr(engine,kind).items():
        local=correction(hw,kw)
        for word,c in external_adjoint(pw,cw,engine.lam,engine.eta).items():
            out+=v*c*s.prod(Q[i] for i in word)*local
    return shift(out,engine.lam)

def all_currents(a,r,lam,eta):
    t=BASIS[a];m=FormalMetric(t,lam,eta,rows_for(r))
    b=FormalMixed(t,r,lam,eta);g=FormalGhost(t,r,lam,eta)
    op=OppositeEndpointCurrent(a,r,lam,eta)
    out=dict(Ymetric=current_delta(m)/2,Ymixed=current_delta(b),Yghost=current_delta(g),
             Xmetric=opposite_delta(op,'metric'),Xmixed=opposite_delta(op,'mixed'))
    for e in [m,b,g]:
        e.raw.cache_clear()
        if hasattr(e,'raw_component'):e.raw_component.cache_clear()
        for name in ['column','h_column','b_column']:
            if hasattr(e,name):getattr(e,name).cache_clear()
    return {k:s.expand(v) for k,v in out.items()}

_source=Path(source.__file__)
_nodes=[n for n in ast.parse(_source.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='source_coefficients']
_ns=dict(vars(source));_ns['propagator_derivative']=lambda w:atom(tuple(sorted(w)))
exec(compile(ast.Module(body=_nodes,type_ignores=[]),str(_source),'exec'),_ns)
formal_source_coefficients=_ns['source_coefficients']

@lru_cache(None)
def source_delta(r,lam,eta):
    def component(u,v):
        A,B=formal_source_coefficients(u,v,r,eta)
        return delta_expression(A)+sum((Q[j]-eta[j])*delta_expression(B[j]) for j in range(4))
    h=s.Matrix(4,4,component).applyfunc(lambda f:shift(f,lam))
    return source.einstein(h,lambda f,i:Q[i]*f)
