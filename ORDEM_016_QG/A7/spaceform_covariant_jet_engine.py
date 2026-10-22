"""Independent normal-chart covariant-derivative recursion, to first/second K."""
from functools import lru_cache
from fractions import Fraction as Q
from collections import defaultdict
from ghost_covariant_word_engine import gamma

def first_curvature_recursive(H,p):
 @lru_cache(None)
 def flat(w,a,b):
  r=Q(H[a][b])
  for i in w:r*=p[i]
  return r
 @lru_cache(None)
 def field(w,a,b):
  if not w:return Q(0),(Q(0),)*4
  i,rest=w[0],w[1:];c,L=field(rest,a,b)
  const=p[i]*c+L[i];linear=[p[i]*v for v in L]
  indices=list(rest)+( [a,b] )
  for slot,target in enumerate(indices):
   for k in range(4):
    changed=indices.copy();changed[slot]=k
    f=flat(tuple(changed[:-2]),changed[-2],changed[-1])
    if not f:continue
    for j in range(4):linear[j]-=gamma(k,i,target,j)*f
  return const,tuple(linear)
 def jet(w,a,b):
  if len(w)<2:return Q(0)
  return (-1)**((len(w)-2)//2)*field(tuple(w),a,b)[0]
 return jet

ZERO=(0,0,0,0)
def mono(indices,c=1):
 e=[0]*4
 for i in indices:e[i]+=1
 return {tuple(e):Q(c)}
def plus(*ps):
 out=defaultdict(Q)
 for p in ps:
  for e,c in p.items():out[e]+=c
 return {e:c for e,c in out.items() if c}
def times(p,q):
 out=defaultdict(Q)
 for e,c in p.items():
  for f,d in q.items():out[tuple(a+b for a,b in zip(e,f))]+=c*d
 return {e:c for e,c in out.items() if c}
def deriv(p,i):
 out={}
 for e,c in p.items():
  if e[i]:
   f=list(e);f[i]-=1;out[tuple(f)]=c*e[i]
 return out
@lru_cache(None)
def connection(order,a,b,c):
 if order==1:return {(tuple(int(k==j) for k in range(4))):gamma(a,b,c,j) for j in range(4) if gamma(a,b,c,j)}
 # Exact spaceform normal metric: a(z)=(sin(sqrt(Kz))/sqrt(Kz))².
 # Gamma2 = -z(x_b delta_ac+x_c delta_ab)/45
 #          -2z x_a delta_bc/15+8x_a x_b x_c/45.
 terms=[]
 for j in range(4):
  if a==c:terms.append(mono((j,j,b),Q(-1,45)))
  if a==b:terms.append(mono((j,j,c),Q(-1,45)))
  if b==c:terms.append(mono((j,j,a),Q(-2,15)))
 terms.append(mono((a,b,c),Q(8,45)))
 return plus(*terms)

def second_curvature_constant(H):
 @lru_cache(None)
 def field(w,a,b,order):
  if not w:return {ZERO:Q(H[a][b])} if order==0 and H[a][b] else {}
  i,rest=w[0],w[1:];parts=[deriv(field(rest,a,b,order),i)]
  indices=list(rest)+[a,b]
  for slot,target in enumerate(indices):
   for k in range(4):
    changed=indices.copy();changed[slot]=k
    for ko in range(1,order+1):
     f=field(tuple(changed[:-2]),changed[-2],changed[-1],order-ko)
     if not f:continue
     g=connection(ko,k,i,target)
     if g:parts.append({e:-v for e,v in times(g,f).items()})
  return plus(*parts)
 def jet(w,a,b,order):return field(tuple(w),a,b,order).get(ZERO,Q(0))
 return jet
