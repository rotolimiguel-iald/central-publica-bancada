"""Quadratic internal/external jet coefficients of the cubic BV current.

No modification of the EH density. The Green-current representative is
the previously checked one. Momenta are derivative markers with i stripped.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import combinations_with_replacement
from localized_brst_flux_engine import v2,green_current,add,lie_matrix
from position_metric_bubble_engine import BASIS

ZERO=(0,)*4
MONOMIALS=tuple(combinations_with_replacement(range(12),2))
def current(U,p,V,q,r,k):
 c=tuple(int(i==r) for i in range(4));LU=lie_matrix(U,p,k,c);LV=lie_matrix(V,q,k,c)
 a=green_current(LU,add(p,k),V,q);b=green_current(LV,add(q,k),U,p)
 return tuple(2*c[i]*v2(U,p,V,q)-2*a[i]-2*b[i] for i in range(4))
@lru_cache(None)
def current_coefficients(a,b,r):
 if b<a:
  swap=lambda i:i+4 if i<4 else i-4 if i<8 else i
  return {tuple(sorted((swap(i),swap(j)))):v for (i,j),v in current_coefficients(b,a,r).items()}
 U,V=BASIS[a],BASIS[b]
 def value(v):return current(U,v[:4],V,v[4:8],r,v[8:])
 assert value((0,)*12)==(0,)*4
 diagonal={};out={}
 for i in range(12):
  p=tuple(int(i==j) for j in range(12));diagonal[i]=value(p)
  assert diagonal[i]==value(tuple(-v for v in p))
  if any(diagonal[i]):out[(i,i)]=diagonal[i]
 for i,j in combinations_with_replacement(range(12),2):
  if i==j:continue
  p=tuple(int(t==i)+int(t==j) for t in range(12));v=value(p)
  c=tuple(v[t]-diagonal[i][t]-diagonal[j][t] for t in range(4))
  if any(c):out[(i,j)]=c
 return out
def evaluate(coeff,p,q,k):
 v=p+q+k
 return tuple(sum(c[t]*v[i]*v[j] for (i,j),c in coeff.items()) for t in range(4))
def split_word(monomial):
 return (tuple(i for i in monomial if i<4),tuple(i-4 for i in monomial if 4<=i<8),tuple(i-8 for i in monomial if i>=8))
