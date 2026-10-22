"""Resolve the smooth-reference jets supplied by the full EH divergence."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from itertools import combinations_with_replacement
import hashlib,json,time,uuid
from metric_boundary_current_engine import boundary_current,eh_boundary_vertex_raw
from metric_quartic_vertices import eh_quartic_32k
from metric_principal_vertices import clear_caches
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'localized_tadpole_boundary_jets';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,obj):
 p=D/n;assert not p.exists();b=json.dumps(obj,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'metric_boundary_current_engine.py',H/'metric_quartic_vertices.py',H/'metric_boundary_current/DERIVACAO.md',H/'finite_smooth_tadpole_derivative_jets/DERIVACAO.md']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),target='Second jets on a single internal leg in the localized full EH quartic tadpole',
 conventions='flat Euclidean auxiliary,exp(+ipx),W=(U(X)V(Y)+V(X)U(Y))/2; full density before IBP versus cutoff-current after IBP',
 tests='55 independent symmetric internal fibers,2 external pairs; independently interpolate momentum powers and compare current placement; zero-cutoff-momentum control',
 prescription_changed=False,full_Q2=False,sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=0;nonzero20=0;controls=[];Z=(0,)*4
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def add(*vs):return tuple(sum(xs) for xs in zip(*vs))
def scale(c,v):return tuple(c*x for x in v)
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
p=(1,2,-1,1);q=(2,-1,0,3);r=(0,1,1,0);sp=(-1,0,2,1)
for external in [(0,4),(1,8)]:
 A,B=(BASIS[i] for i in external)
 for u,v in combinations_with_replacement(range(10),2):
  U,V=BASIS[u],BASIS[v];matrices=(A,B,U,V);momenta=(p,q,r,sp)
  bs=[]
  for leg in range(4):bs.append(boundary_current(*[(matrices[i],momenta[i] if i==leg else Z) for i in range(4)]))
  pe=add(p,q);be=add(bs[0],bs[1]);bu,bv=bs[2:]
  coeff={(0,0):dot(pe,be),(1,0):dot(pe,bu)+dot(r,be),(0,1):dot(pe,bv)+dot(sp,be),
         (2,0):dot(r,bu),(1,1):dot(r,bv)+dot(sp,bu),(0,2):dot(sp,bv)}
  def fields(a,b):return ((A,p),(B,q),(U,scale(a,r)),(V,scale(b,sp)))
  def full(a,b):return (eh_quartic_32k(*fields(a,b))+eh_boundary_vertex_raw(*fields(a,b)))/16
  def gg(a,b):return eh_quartic_32k(*fields(a,b))/16
  for a,b in [(0,0),(1,0),(-1,0),(0,1),(0,-1),(2,-3)]:
   predicted=sum(value*F(a)**i*F(b)**j for (i,j),value in coeff.items())
   eq(full(a,b)-gg(a,b),predicted)
  eq((full(1,0)+full(-1,0))/2-full(0,0),coeff[2,0])
  eq((full(0,1)+full(0,-1))/2-full(0,0),coeff[0,2])
  eq((gg(1,0)+gg(-1,0))/2-gg(0,0),0)
  eq((gg(0,1)+gg(0,-1))/2-gg(0,0),0)
  # Moving the total derivative onto chi supplies exactly -ell.B,
  # where ell=-(p+q+r+s), without constraining the internal jets.
  Q=add(p,q,r,sp);ell=scale(-1,Q);bc=boundary_current(*fields(1,1))
  eq(full(1,1)-gg(1,1),-dot(ell,bc))
  qzero=scale(-1,add(p,r,sp))
  eq(eh_boundary_vertex_raw((A,p),(B,qzero),(U,r),(V,sp)),0)
  if coeff[2,0] or coeff[0,2]:
   nonzero20+=1
   if len(controls)<5:controls.append(dict(external=external,internal=[u,v],coefficients={str(k):str(value) for k,value in coeff.items()},omit_boundary_defect=str(full(1,1)-gg(1,1))))
  clear_caches()
assert nonzero20>0;checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,
 nonzero_same_leg_second_jet_fibers=nonzero20,controls=controls,
 conclusion='FULL_LOCAL_DENSITY_HAS_W20_W02; CUTOFF_CURRENT_REPRESENTATION_TRADES_THEM_BY_IBP',
 full_Q2=False,gate_changed=False)
save('results.json',result);save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
