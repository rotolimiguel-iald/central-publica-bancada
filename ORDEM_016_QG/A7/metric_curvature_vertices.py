"""Algebraic curvature vertices of EH with fixed Einstein background.

Matrices use row-major tuples, same as metric_principal_vertices.
Potential density S=-3K/(2kappa)*P(h), P=sqrt(det(I+h))*(tr((I+h)^-1)-2).
No files written on import; returned multilinear coefficients include factorials.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
I=tuple(int(a==b) for a in range(4) for b in range(4))
def tr(A):return sum(A[5*i] for i in range(4))
def mul(A,B):return tuple(sum(A[4*i+k]*B[4*k+j] for k in range(4)) for i in range(4) for j in range(4))
def plus(*As):return tuple(sum(A[i] for A in As) for i in range(16))
def traceless(A):
 t=Q(tr(A),4);return tuple(Q(A[i])-t*I[i] for i in range(16))
def potential_polynomial(A,degree):
 t=tr(A);a2=mul(A,A);t2=tr(a2);t3=tr(mul(a2,A));t4=tr(mul(a2,a2))
 if degree==2:return t2/ Q(2)-t*t/Q(4)
 if degree==3:return -t**3/Q(12)+t*t2/Q(2)-2*t3/Q(3)
 if degree==4:return -t**4/Q(64)+3*t*t*t2/Q(16)-3*t2*t2/Q(16)-t*t3/Q(2)+3*t4/Q(4)
 raise ValueError('Only degrees2,3,4 are implemented')
def polarized(fields):
 n=len(fields);value=Q(0)
 for size in range(1,n+1):
  for subset in combinations(fields,size):value+=(-1)**(n-size)*potential_polynomial(plus(*subset),n)
 return value
@lru_cache(None)
def eh_cubic_potential_16k_over_K(A,B,C):
 # P3=-2/3 tr(h0^3); coefficient ABC=-4tr(A0 B0 C0) for symmetric matrices.
 a,b,c=traceless(A),traceless(B),traceless(C)
 return 96*tr(mul(mul(a,b),c))
