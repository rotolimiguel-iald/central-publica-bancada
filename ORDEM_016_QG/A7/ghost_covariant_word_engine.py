"""Covariant derivative words and a first-curvature normal-chart evaluator.

All h indices and derivative indices are covariant. At the origin g=delta.
No path writes, script imports, external calls or numeric fits on import.
"""
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction as Q

def term(word,a,b,c=1):return {(tuple(word),min(a,b),max(a,b)):Q(c)}
def add(*parts):
 r=defaultdict(Q)
 for part in parts:
  for k,c in part.items():r[k]+=c
 return {k:c for k,c in r.items() if c}
def scale(a,c):return {k:v*Q(c) for k,v in a.items() if v*c}
def derivative(a,i):return {((i,)+w,j,k):c for (w,j,k),c in a.items()}
def trh(word=()):return add(*(term(word,a,a) for a in range(4)))
def divergence(nu):return add(*(term((a,),a,nu) for a in range(4)))
def C(nu):return add(divergence(nu),scale(derivative(trh(),nu),Q(-1,2)))
@lru_cache(None)
def A(mu,nu,rho):
 return add(term((rho,),mu,nu),term((mu,),rho,nu),term((nu,),mu,rho,-1),C(rho) if mu==nu else {})
def B(nu,rho):return derivative(C(nu),rho)
def box(a,b):return add(*(term((i,i),a,b) for i in range(4)))
def D(nu,rho):return add(B(nu,rho),scale(box(nu,rho),-1))
@lru_cache(None)
def F(mu,nu,a,b):return add(derivative(A(nu,a,b),mu),scale(derivative(A(mu,a,b),nu),-1))

def hessian_terms(reference=False):
 """Map (explicit K power, T_ab, H_cd, derivative word on H) -> rational."""
 result=defaultdict(Q)
 def quad(left,right,coefficient,order=0):
  for (u,a,b),v in left.items():
   for (w,c,d),z in right.items():
    fac=Q(coefficient)*v*z
    result[(order,a,b,c,d,tuple(reversed(u))+w)]+=(-1)**len(u)*fac
    result[(order,c,d,a,b,tuple(reversed(w))+u)]+=(-1)**len(w)*fac
 if reference:
  for a in range(4):
   for b in range(4):quad(box(a,b),box(a,b),Q(1,24))
  bt=add(*(box(a,a) for a in range(4)))
  du=add(*(derivative(divergence(a),a) for a in range(4)))
  quad(bt,bt,Q(7,96));quad(du,bt,Q(-1,8));quad(du,du,Q(1,12))
  for a in range(4):
   for b in range(4):quad(derivative(divergence(a),b),derivative(divergence(a),b),Q(-1,24))
 else:
  for a in range(4):
   for b in range(4):
    quad(term((),a,b),B(b,a),-5,1)
    quad(D(a,b),D(b,a),Q(1,8))
    for m in range(4):quad(A(m,a,b),A(m,b,a),Q(-5,4),1)
    for m in range(4):
     for n in range(4):quad(F(m,n,a,b),F(m,n,b,a),Q(1,48))
  # Omega^a_b,mn/K=delta_am delta_bn-delta_an delta_bm.
  # tr Omega[A_m,A_n] = ([A_m,A_n])_n,m - ([A_m,A_n])_m,n.
  for m in range(4):
   for n in range(4):
    for k in range(4):
     quad(A(m,n,k),A(n,k,m),Q(1,24),1)
     quad(A(n,n,k),A(m,k,m),Q(-1,24),1)
     quad(A(m,m,k),A(n,k,n),Q(-1,24),1)
     quad(A(n,m,k),A(m,k,n),Q(1,24),1)
 return {k:c for k,c in result.items() if c}

def curvature_gradient_terms():
 """First-K integrated correction inferred from the word calculation."""
 result=defaultdict(Q)
 def quad(left,right,coefficient):
  for (u,a,b),v in left.items():
   for (w,c,d),z in right.items():
    f=Q(coefficient)*v*z
    result[(1,a,b,c,d,tuple(reversed(u))+w)]+=(-1)**len(u)*f
    result[(1,c,d,a,b,tuple(reversed(w))+u)]+=(-1)**len(w)*f
 for m in range(4):
  for a in range(4):
   for b in range(4):quad(term((m,),a,b),term((m,),a,b),Q(7,12))
  quad(derivative(trh(),m),derivative(trh(),m),Q(-17,12))
  quad(divergence(m),derivative(trh(),m),Q(7,2))
  quad(divergence(m),divergence(m),Q(-79,24))
 return {k:c for k,c in result.items() if c}

def gamma(a,b,c,j):
 return -Q(int(a==c)*int(b==j)+int(a==b)*int(c==j)-2*int(b==c)*int(a==j),3)

def jet(word,a,b,H,p,order):
 """D_word h_ab at zero, h_ab(x)=H_ab exp(i p.x); coefficient of K^order.

 For first K, exactly one Christoffel symbol is differentiated exactly once.
 Gamma vanishes at the origin and has no higher derivative at order K.
 """
 n=len(word)
 assert n%2==0
 if order==0:
  value=Q(H[a][b])*(-1)**(n//2)
  for i in word:value*=p[i]
  return value
 if n<2:return Q(0)
 value=Q(0)
 for k in range(1,n):
  for j in range(k):
   for slot in range(k+1,n+2):
    target=word[slot] if slot<n else (a if slot==n else b)
    for c in range(4):
     coeff=-gamma(c,word[k],target,word[j])
     if not coeff:continue
     indices=list(word);aa,bb=a,b
     if slot<n:indices[slot]=c
     elif slot==n:aa=c
     else:bb=c
     coeff*=Q(H[aa][bb])*(-1)**((n-2)//2)
     for pos,i in enumerate(indices):
      if pos not in (j,k):coeff*=p[i]
     value+=coeff
 return value

def evaluate(operator,T,H,p,order):
 @lru_cache(None)
 def j(w,a,b,o):return jet(w,a,b,H,p,o)
 return sum((c*Q(T[a][b])*j(w,u,v,order-ko)
   for (ko,a,b,u,v,w),c in operator.items() if ko<=order and T[a][b]),Q(0))

def matrix_unit(a,b):
 H=[[0]*4 for _ in range(4)];H[a][b]=H[b][a]=1;return H
