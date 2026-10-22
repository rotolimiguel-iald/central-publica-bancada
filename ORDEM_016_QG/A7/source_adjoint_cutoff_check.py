"""Audit a received adjoint claim and compute the first cutoff jet of its contact."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import product
import json,hashlib,time,uuid
import sympy as s
import logarithmic_contact_engine as R
import einstein_radial_aux_engine as E
H=Path(__file__).resolve().parent;D=H/'source_adjoint_cutoff';D.mkdir(exist_ok=False)
src=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/9118ccb7-dd63-49b6-9340-773caa74812e_delivery.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,obj):
 p=D/n;assert not p.exists();b=obj if isinstance(obj,bytes) else json.dumps(obj,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
receipt=json.loads(src.read_bytes());put('RECEIPT.json',src.read_bytes());put('RESPONSE.md',receipt['result']['text'].encode())
sources=[Path(__file__),H/'logarithmic_contact_engine.py',H/'einstein_radial_aux_engine.py',H/'source_einstein_radial_aux/DERIVACAO.md',H/'covariant_source_density/DERIVACAO.md']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Exact distribution adjoint versus derivative/extension contact; first cutoff jet in E contact of known flat source',
 definition='C_D=R(Df)-D R(f); R=FP[(1-a)mu^(2a)z^a]',
 source='C_ab,r=-12delta_ab x_r/z4-30(delta_ar x_b+delta_br x_a)/z4+96x_a x_b x_r/z5',
 cutoff='chi=exp(lambda b.x) near diagonal, formal jet; b=e0,e1; r=0; compact cutoff can realize these jets',
 scope='X-side source commutator only, K0; no Y cutoff contribution, full pair or causal anomaly claim',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=0;x=E.x;z=E.radial_z;Q=R.Q;a,lam=s.symbols('a lam')
def delta(i,j):return s.Integer(i==j)
def eq(f,g=0):
 global checks
 assert s.expand(f-g)==0,(f,g);checks+=1
# The quoted 1/z second and third derivative contact table is valid
# in the D R-R D orientation, but logs acquire contact at fourth order.
for i,j in product(range(4),repeat=2):eq(R.contact(1,0,(i,j)),-delta(i,j)/4)
for i,j,k in product(range(4),repeat=3):
 eq(R.contact(1,0,(i,j,k)),-(delta(i,j)*Q[k]+delta(j,k)*Q[i]+delta(k,i)*Q[j])/6)
for word in product(range(4),repeat=4):
 i,j,k,l=word
 pred=-(delta(i,j)*delta(k,l)+delta(i,k)*delta(j,l)+delta(i,l)*delta(j,k))/6
 eq(R.contact(0,1,word),pred);eq(R.direct_laurent_contact(0,1,word),pred)
# Exact trace transport already specified by the source convention.
T=s.Matrix(4,4,lambda i,j:s.Integer(3*i+2*j+1));T=T+T.T
P=(s.eye(4)*z-s.Matrix(x)*s.Matrix(x).T)/6
eqmat=-z*T/2+P*T+T*P.T
expected=-(z*T+s.Matrix(x)*s.Matrix(x).T*T+T*s.Matrix(x)*s.Matrix(x).T)/6
for i,j in product(range(4),repeat=2):eq(eqmat[i,j],expected[i,j])
# Independent distribution adjoint example: integral r^-2 Delta e^-r².
rr=s.symbols('r',positive=True)
eq(s.integrate(rr*(4*rr**2-8)*s.exp(-rr**2),(rr,0,s.oo)),-2)

def dx(f,i,shift):return s.expand(s.diff(f,x[i])+2*x[i]*s.diff(f,z)+shift[i]*f)
def flat_e(h,shift):
 tr=s.trace(h)
 def dd(f,i,j):return dx(dx(f,j,shift),i,shift)
 boxtr=sum(dd(tr,i,i) for i in range(4))
 ddh=sum(dd(h[i,j],i,j) for i,j in product(range(4),repeat=2))
 return s.Matrix(4,4,lambda u,v:s.expand(-sum(dd(h[u,v],i,i) for i in range(4))-dd(tr,u,v)
       +sum(dd(h[i,v],u,i)+dd(h[i,u],v,i) for i in range(4))+delta(u,v)*(boxtr-ddh)))

@lru_cache(None)
def monomials(f):
 terms=[]
 for term in s.expand(f).as_ordered_terms():
  if not term:continue
  powz=term.as_powers_dict().get(z,s.Integer(0));assert powz.is_Integer and powz<=0
  for powers,co in s.Poly(term*z**(-powz),*x).terms():
   assert co.is_Rational,(co,term);terms.append((int(-powz),powers,co))
 return terms
def multiply_delta(pol,powers):
 for i,n in enumerate(powers):pol=(-1)**n*s.diff(pol,Q[i],n)
 return s.expand(pol)
def residue(f):return s.expand(sum(co*R.residue(n,powers,(1,1,1,1)) for n,powers,co in monomials(f)))
@lru_cache(None)
def first(f,i):return s.expand(sum(co*multiply_delta(R.contact(n,0,(i,)),powers) for n,powers,co in monomials(f)))
h=s.Matrix(4,4,lambda u,v:(-12*delta(u,v)*x[0]-30*(delta(u,0)*x[v]+delta(v,0)*x[u]))/z**4+96*x[u]*x[v]*x[0]/z**5)
reg=[2*a*xx/z for xx in x];baseline=flat_e(h,reg)
values={};nonzero=[]
for direction in (0,1):
 b=[delta(i,direction) for i in range(4)];shift=[reg[i]+lam*b[i] for i in range(4)]
 actual=flat_e(h,shift)-baseline
 for u,v in product(range(4),repeat=2):
  # For this rational kernel only the simple pole and coefficient a^1
  # contribute; sign follows C_E=R E-E R.
  linear=-residue(s.expand(actual[u,v]).coeff(a,1).coeff(lam,1))
  eq(s.expand(actual[u,v]).coeff(a,1).coeff(lam,2),0)
  tr=s.trace(h)
  predicted=-2*sum(b[i]*first(h[u,v],i) for i in range(4))-b[u]*first(tr,v)-b[v]*first(tr,u)
  predicted+=sum(b[u]*first(h[i,v],i)+b[i]*first(h[i,v],u)+b[v]*first(h[i,u],i)+b[i]*first(h[i,u],v) for i in range(4))
  predicted+=delta(u,v)*(2*sum(b[i]*first(tr,i) for i in range(4))-sum(b[i]*first(h[i,j],j)+b[j]*first(h[i,j],i) for i,j in product(range(4),repeat=2)))
  eq(linear,predicted)
  values[str((direction,u,v))]=str(linear)
  if linear!=0:nonzero.append((direction,u,v))
assert nonzero;checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,
 local_contact_over_C_E=values,nonzero_components=len(nonzero),
 control=dict(component=[0,1,1],value=values[str((0,1,1))]),
 adjoint='Exact on extended distributions; no extra contact in integration by parts',
 contact='Extra term belongs to R E-E R; localization adds first cutoff jet, no second cutoff jet in this commutator',
 full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'RECEIPT.json',D/'RESPONSE.md',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='local_contact_over_C_E'}))
