"""Flat metric bubble with both full EH vertices and cutoff jets through order3."""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from flat_loop_cutoff_engine import FlatLoop,tensor
from localized_eh_cubic_engine import boundary_vertex_data,AXES
from position_metric_bubble_engine import lincomb,sandwich,frob

class FullEHLoop(FlatLoop):
    def __init__(self,point,T):super().__init__('metric',point,T)

    @lru_cache(None)
    def data(self,T,variant):
        return self.vertex(T) if variant<0 else boundary_vertex_data(T,AXES[variant])

    @lru_cache(None)
    def full_paired(self,variant,ex,word):
        data=self.data(self.T,variant);ax=data[0] if ex<0 else data[1][ex]
        terms=[]
        for mask in product((0,1),repeat=len(word)):
            u=tuple(word[k] for k,t in enumerate(mask) if not t)
            v=tuple(word[k] for k,t in enumerate(mask) if t)
            terms.append((F(1),sandwich(self.matrix(u),ax,self.matrix(v))))
        return lincomb(*terms)

    @lru_cache(None)
    def full_raw(self,lx,ly,ex,word,y_index,a,b):
        data=self.data(tensor(a,b),ly);by=data[0] if y_index<0 else data[1][y_index]
        return F(1,16)*frob(self.full_paired(lx,ex,tuple(sorted(word))),by)

    def full_y_ward(self,lx,ex,r,y_jets,extra_word=()):
        out=F()
        for ly in [-1,0,1,2,3]:
            prefix=() if ly<0 else (ly,)
            value=y_jets.get(tuple(sorted(prefix)),0)
            gradient=[y_jets.get(tuple(sorted(prefix+(j,))),0) for j in range(4)]
            hessian=[[y_jets.get(tuple(sorted(prefix+(a,j))),0) for j in range(4)] for a in range(4)]
            if not value and not any(gradient) and not any(v for row in hessian for v in row):continue
            for a in range(4):
                w=lambda word,j:self.full_raw(lx,ly,ex,extra_word+word,j,a,r)
                term=-value*w((a,),-1)-gradient[a]*w((),-1)
                for j in range(4):
                    term+=value*w((a,j),j)+gradient[a]*w((j,),j)
                    term+=gradient[j]*w((a,),j)+hessian[a][j]*w((),j)
                out+=F(2,1 if a==r else 2)*term
        return out

    def full_localized(self,r,x_jets,y_jets):
        out=F()
        for lx in [-1,0,1,2,3]:
            prefix=() if lx<0 else (lx,)
            v=x_jets.get(prefix,0)
            g=[x_jets.get(tuple(sorted(prefix+(i,))),0) for i in range(4)]
            if v:out+=v*self.full_y_ward(lx,-1,r,y_jets)
            for i in range(4):
                if g[i]:out-=g[i]*self.full_y_ward(lx,i,r,y_jets)
                if v:out+=v*self.full_y_ward(lx,i,r,y_jets,(i,))
        return out
