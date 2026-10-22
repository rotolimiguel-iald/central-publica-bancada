"""Restore dchi terms when localizing the original ghost divergence operator.

Integral chi*barc*div Z = -Integral (chi*dbarc+dchi*barc)*Z.
The existing directed ghost vertex stores -dbarc*Z. Derivative columns
therefore give its boundary correction without new coupling or refitting.
"""
from functools import lru_cache
from fractions import Fraction as F
import ghost_direct_position_engine as G
from flat_loop_cutoff_engine import FlatLoop,tensor
from full_eh_localized_loop_engine import FullEHLoop
from localized_eh_cubic_engine import AXES
from position_metric_bubble_engine import empty,lincomb,frob,transpose

@lru_cache(None)
def ghost_boundary_data(A,gradient):
    v=G.vertex(A)
    def restore(W):
        out=empty(20)
        for i,row in enumerate(W):
            for j,value in row.items():
                mu,nu=j//4-1,j%4
                assert mu>=0
                if gradient[mu]:out[i][nu]=out[i].get(nu,F())+gradient[mu]*value
        return out
    return restore(v[0]),[restore(w) for w in v[1]]

def ghost_localized_data(A,value,gradient):
    b=G.vertex(A);d=ghost_boundary_data(A,tuple(gradient))
    return lincomb((value,b[0]),(F(1),d[0])),[lincomb((value,b[1][i]),(F(1),d[1][i])) for i in range(4)]

class FullGhostLoop(FullEHLoop):
    def __init__(self,point,T):FlatLoop.__init__(self,'ghost',point,T)

    @lru_cache(None)
    def data(self,T,variant):
        return G.vertex(T) if variant<0 else ghost_boundary_data(T,AXES[variant])

    @lru_cache(None)
    def full_raw(self,lx,ly,ex,word,y_index,a,b):
        data=self.data(tensor(a,b),ly);by=data[0] if y_index<0 else data[1][y_index]
        return F(frob(self.full_paired(lx,ex,tuple(sorted(word))),transpose(by)))
