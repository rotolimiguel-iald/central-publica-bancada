"""Derivative/extension contacts for current-X graphs in the fixed prescription."""
from functools import lru_cache
import sympy as s
from opposite_endpoint_current_engine import OppositeEndpointCurrent,external_adjoint
from full_loop_extension_engine import Q,propagator_derivative,contact

class OppositeEndpointContact(OppositeEndpointCurrent):
    @lru_cache(None)
    def raw_blocks(self,kind):
        blocks={}
        for (pw,cw,hw,kw),v in getattr(self,kind).items():
            blocks[pw,cw]=blocks.get((pw,cw),s.Integer(0))+v*propagator_derivative(hw)*propagator_derivative(kw)
        return {key:s.expand(f) for key,f in blocks.items()}

    def extension_contact(self,kind):
        assert self.point is None
        result=s.Integer(0)
        for (pw,cw),f in self.raw_blocks(kind).items():
            for word,v in external_adjoint(pw,cw,self.lam,self.eta).items():
                if word:result-=v*contact(f,word)
        return s.expand(result.subs({Q[i]:Q[i]-self.lam[i] for i in range(4)},simultaneous=True))
