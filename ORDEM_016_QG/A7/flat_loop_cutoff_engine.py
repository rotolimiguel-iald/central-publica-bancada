"""Unreduced flat loop kernels with independent endpoint cutoff jets.

Gamma-Gamma metric vertices only. No distribution extension, EH boundary
vertex completion, curvature, or claim about the full quantum anomaly.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
import sympy as s
import ghost_direct_position_engine as G
import position_metric_ordered_operator_engine as M
from position_metric_bubble_engine import empty, lincomb, frob, sandwich, transpose, LABELS

x = s.symbols('x0:4')
z = sum(v*v for v in x)

@lru_cache(None)
def scalar_derivative(word):
    if not word:
        return 1/z
    return s.diff(scalar_derivative(word[:-1]), x[word[-1]])

def tensor(a, b):
    return tuple(int((i==a and j==b) or (i==b and j==a))
                 for i in range(4) for j in range(4))

class FlatLoop:
    def __init__(self, kind, point, external_tensor):
        assert kind in ('metric', 'ghost') and sum(t*t for t in point)>0
        self.kind = kind
        self.point = tuple(point)
        self.T = tuple(external_tensor)
        self.size = 50 if kind == 'metric' else 20
        self.width = 10 if kind == 'metric' else 4
        self.vertex = M.vertex_data if kind == 'metric' else G.vertex
        self.AX = self.vertex(self.T)

    @lru_cache(None)
    def matrix(self, word):
        out = empty(self.size)
        for i,j in product(range(self.size),repeat=2):
            xi,yi = i//self.width-1,j//self.width-1
            if self.kind == 'ghost':
                fiber = F(int(i%4 == j%4))
            else:
                a,b=LABELS[i%10];c,d=LABELS[j%10]
                fiber=F(int(a==c and b==d)+int(a==d and b==c)-int(a==b and c==d),2)
            if not fiber:
                continue
            w=tuple(sorted(word+(() if xi<0 else (xi,))+(() if yi<0 else (yi,))))
            v=self.scalar(w)*((-1)**(len(word)+int(yi>=0)))*fiber
            if v:out[i][j]=v
        return out

    @lru_cache(None)
    def scalar(self, word):
        return F(scalar_derivative(word).subs(dict(zip(x,self.point))))

    @lru_cache(None)
    def paired(self, external_index, word):
        ax=self.AX[0] if external_index<0 else self.AX[1][external_index]
        parts=[]
        for mask in product((0,1),repeat=len(word)):
            u=tuple(word[k] for k,t in enumerate(mask) if not t)
            v=tuple(word[k] for k,t in enumerate(mask) if t)
            parts.append((F(1),sandwich(self.matrix(u),ax,self.matrix(v))))
        return lincomb(*parts)

    @lru_cache(None)
    def raw(self, external_index, word, y_index, a, b):
        by=self.vertex(tensor(a,b))
        by=by[0] if y_index<0 else by[1][y_index]
        if self.kind=='ghost':by=transpose(by)
        scale=F(1,16) if self.kind=='metric' else F(1)
        return scale*frob(self.paired(external_index,tuple(sorted(word))),by)

    def y_ward(self, external_index, r, value, gradient, hessian, extra_word=()):
        """Y-adjoint with cutoff; extra_word differentiates only kernels in Y."""
        out=F()
        for a in range(4):
            w=lambda word,j:self.raw(external_index,extra_word+word,j,a,r)
            term=-value*w((a,),-1)-gradient[a]*w((),-1)
            for j in range(4):
                term+=value*w((a,j),j)+gradient[a]*w((j,),j)
                term+=gradient[j]*w((a,),j)+hessian[a][j]*w((),j)
            out+=F(2,1 if a==r else 2)*term
        return out

    def localized(self,r,x_value,x_gradient,y_value,y_gradient,y_hessian):
        out=x_value*self.y_ward(-1,r,y_value,y_gradient,y_hessian)
        for i in range(4):
            out-=x_gradient[i]*self.y_ward(i,r,y_value,y_gradient,y_hessian)
            # Translation invariant flat raw kernels: dX_i=-dY_i, not on chiY.
            out+=x_value*self.y_ward(i,r,y_value,y_gradient,y_hessian,(i,))
        return out
