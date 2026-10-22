"""Flat metric bubble with a classical BV current at its Y vertex.

This computes only the indicated diagram, with /16 metric normalization
and no diagram symmetry factor. It is not the full quantum Ward identity.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import sympy as s
from localized_eh_cubic_engine import localized_vertex_data
from position_metric_bubble_engine import LABELS
from full_loop_extension_engine import propagator_derivative,x,z,dx,contact,Q
from classical_current_jet_engine import split_word

def fiber(a,b):
 i,j=LABELS[a];k,l=LABELS[b]
 return F(int(i==k and j==l)+int(i==l and j==k)-int(i==j and k==l),2)

def current_terms(rows,eta):
 out={}
 for row in rows:
  a,b=row['a'],row['b']
  for item in row['coefficients']:
   coeff=-sum(F(t)*g for t,g in zip(item['current'],eta))
   if not coeff:continue
   pw,qw,kw=tuple(item['pword']),tuple(item['qword']),tuple(item['kword'])
   out[a,b,pw,qw,kw]=coeff
   if a!=b:out[b,a,qw,pw,kw]=coeff
 return out

def opword(kword,ex,lam,eta):
 out={():s.Integer(1)}
 for i in kword:
  tmp={}
  for word,c in out.items():
   tmp[word]=tmp.get(word,0)-eta[i]*c
   w=tuple(sorted(word+(i,)));tmp[w]=tmp.get(w,0)+c
  out=tmp
 if ex>=0:
  tmp={}
  for word,c in out.items():
   tmp[word]=tmp.get(word,0)-lam[ex]*c
   w=tuple(sorted(word+(ex,)));tmp[w]=tmp.get(w,0)-c
  out=tmp
 return {k:v for k,v in out.items() if v}

class CurrentInsertion:
 def __init__(self,T,lam,eta,rows,point=None):
  self.lam=tuple(lam);self.eta=tuple(eta);self.AX=localized_vertex_data(tuple(T),1,self.lam)
  self.terms=current_terms(rows,self.eta);self.point=point
 @lru_cache(None)
 def scalar(self,word):
  v=propagator_derivative(word)
  if self.point is None:return v
  return F(v.subs(dict(zip(x,self.point))).subs(z,sum(t*t for t in self.point)))
 @lru_cache(None)
 def column(self,a,pword,extra=()):
  out={}
  for row in range(50):
   fr=fiber(row%10,a)
   if not fr:continue
   w=(() if row<10 else (row//10-1,))+pword+extra
   v=fr*(-1)**len(pword)*self.scalar(tuple(sorted(w)))
   if v:out[row]=v
  return out
 @lru_cache(None)
 def raw_component(self,ex,a,b,pw,qw,word=()):
  W=self.AX[0] if ex<0 else self.AX[1][ex];ans=0
  for mask in product((0,1),repeat=len(word)):
   u=tuple(word[i] for i,t in enumerate(mask) if not t);v=tuple(word[i] for i,t in enumerate(mask) if t)
   left=self.column(a,pw,u);right=self.column(b,qw,v)
   for i,l in left.items():
    for j,c in W[i].items():
     if j in right:ans+=l*c*right[j]
  return s.expand(s.Rational(1,16)*ans) if self.point is None else F(ans,16)
 @lru_cache(None)
 def raw(self,ex,kw,word=()):
  out=sum(c*self.raw_component(ex,a,b,pw,qw,word) for (a,b,pw,qw,k),c in self.terms.items() if k==kw)
  return s.expand(out) if self.point is None else out
 def off_diagonal(self):
  ans=0
  for kw in sorted({k[-1] for k in self.terms}):
   for ex in [-1,0,1,2,3]:
    for w,c in opword(kw,ex,self.lam,self.eta).items():ans+=c*self.raw(ex,kw,w)
  return s.expand(ans)
 def extension_contact(self):
  assert self.point is None
  out=0
  for kw in sorted({k[-1] for k in self.terms}):
   for ex in [-1,0,1,2,3]:
    f=self.raw(ex,kw)
    for word,c in opword(kw,ex,self.lam,self.eta).items():
     if word:out-=c*contact(f,word)
  return s.expand(out.subs({Q[i]:Q[i]-self.lam[i] for i in range(4)},simultaneous=True))
