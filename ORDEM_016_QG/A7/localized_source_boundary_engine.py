"""Flat source coefficients with the pre-IBP ghost boundary restored.

No evaluation, I/O or choice of quantum normalization at import time.
Cutoff Y has exponential jets eta; source cutoff X is treated separately.
"""
from functools import lru_cache
from itertools import product
import sympy as s
from full_loop_extension_engine import x,z,Q,propagator_derivative,dx,contact
import logarithmic_contact_engine as R

def delta(i,j):return s.Integer(i==j)
def metric(c,e,mu,nu):
 return (delta(c,mu)*delta(e,nu)+delta(c,nu)*delta(e,mu)-delta(c,e)*delta(mu,nu))/2
def trace_reversed(c,e,mu,nu):
 return (delta(c,mu)*delta(e,nu)+delta(c,nu)*delta(e,mu))/2
def hcomb(c,e,j,r,mu,m):
 return delta(j,mu)*metric(c,e,r,m)+delta(j,m)*metric(c,e,mu,r)-delta(mu,m)*metric(c,e,j,r)

@lru_cache(None)
def source_coefficients(u,v,r,eta):
 A=0;B=[0]*4
 for m,mu in product(range(4),repeat=2):
  for c,e,xi,gxi in [(u,v,m,-1),(u,m,-1,v),(v,m,-1,u)]:
   gw=() if gxi<0 else (gxi,);hw=() if xi<0 else (xi,)
   # The contraction delta_(m,nu) fixes nu=m. Restore dchi*barc
   # by replacing the single derivative on the internal Y antighost.
   g=-propagator_derivative(tuple(sorted(gw+(mu,))))+eta[mu]*propagator_derivative(gw)
   hY=-propagator_derivative(tuple(sorted(hw+(r,))))
   A-=g*hY*trace_reversed(c,e,mu,m)
   for j in range(4):B[j]-=g*propagator_derivative(hw)*hcomb(c,e,j,r,mu,m)
 return s.expand(A),tuple(s.expand(t) for t in B)

def source_reduced(u,v,r,eta):
 A,B=source_coefficients(u,v,r,eta)
 return s.expand(A+sum(dx(B[j],j)-eta[j]*B[j] for j in range(4)))

def einstein(h,derivative):
 tr=s.trace(h)
 dd=lambda f,i,j:derivative(derivative(f,j),i)
 boxtr=sum(dd(tr,i,i) for i in range(4))
 ddh=sum(dd(h[i,j],i,j) for i,j in product(range(4),repeat=2))
 return s.Matrix(4,4,lambda u,v:s.expand(-sum(dd(h[u,v],i,i) for i in range(4))-dd(tr,u,v)
  +sum(dd(h[i,v],u,i)+dd(h[i,u],v,i) for i in range(4))+delta(u,v)*(boxtr-ddh)))

def einstein_contact(h,lam):
 # C_E(exp(lambda.X)h)/exp(lambda.X), before moving multiplier
 # onto the diagonal. Zero-order lambda_i lambda_j terms commute.
 tr=s.trace(h)
 def dd(f,i,j):return contact(f,(i,j))+lam[i]*contact(f,(j,))+lam[j]*contact(f,(i,))
 return s.Matrix(4,4,lambda u,v:s.expand(-sum(dd(h[u,v],i,i) for i in range(4))-dd(tr,u,v)
  +sum(dd(h[i,v],u,i)+dd(h[i,u],v,i) for i in range(4))
  +delta(u,v)*(sum(dd(tr,i,i) for i in range(4))-sum(dd(h[i,j],i,j) for i,j in product(range(4),repeat=2)))))

def source_extension(r,lam,eta):
 h=s.Matrix(4,4,lambda u,v:source_reduced(u,v,r,eta))
 # C_divY(B)=-sum C_dj(Bj), after factoring exp(eta.Y).
 DY=s.Matrix(4,4,lambda u,v:-sum(contact(source_coefficients(u,v,r,eta)[1][j],(j,)) for j in range(4)))
 shift=lambda f:s.expand(f.subs({Q[i]:Q[i]-lam[i] for i in range(4)},simultaneous=True))
 ec=einstein_contact(h,lam).applyfunc(shift)
 dy=DY.applyfunc(shift)
 # E acts after shifting delta polynomial: it multiplies by Q, not Q+lambda.
 eY=einstein(dy,lambda f,i:s.expand(Q[i]*f))
 return (-ec+eY).applyfunc(s.expand)
