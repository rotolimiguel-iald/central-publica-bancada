"""Contract quartic Noether identity with arbitrary constant symmetric W fiber."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time
from metric_principal_vertices import gamma2,gauge_matrix,lie_matrix,eh_cubic_16k,clear_caches
from metric_quartic_vertices import second_coefficient_4
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'finite_smooth_tadpole_transport';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 p=D/n;assert not p.exists(),p
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();tmp=p.with_suffix('.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;tmp.replace(p)
inputs=[Path(__file__),H/'metric_principal_vertices.py',H/'metric_quartic_vertices.py',H/'finite_smooth_tadpole/results.json']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='General W0 tadpole Ward variation equals negative cubic reference-transport contraction',
 method='All55 symmetric W fibers,3 dense nonaxis external controls, direct quartic vs cubic identity',
 normalization='Quartic32k/16; cubic16k/8; no fitted coefficient',
 scope='Zero derivative jet of a constant metric W; flat, constant cutoff; no physical state claimed',
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
start=time.process_time();checks=0;nonzero=[];zero=(0,0,0,0)
fixtures=[(BASIS[0],(1,2,-1,1),(2,-1,1,3)),(BASIS[1],(2,-1,0,3),(1,2,0,-1)),
 ((2,1,-1,3,1,0,2,-2,-1,2,1,0,3,-2,0,-1),(1,-1,2,3),(0,2,-1,1))]
for i in range(10):
 for j in range(i,10):
  entries=[(i,j)]+([] if i==j else [(j,i)])
  for f,(A,p,v) in enumerate(fixtures):
   G=gauge_matrix(p,v);ga=gamma2(A,tuple(-z for z in p));gg=gamma2(G,p)
   left=F();right=F()
   for a,b in entries:
    Ea,Eb=BASIS[a],BASIS[b]
    left+=F(second_coefficient_4(Ea,Eb,ga,gg)+second_coefficient_4(Ea,Eb,gg,ga),16)
    La=lie_matrix(Ea,zero,p,v);Lb=lie_matrix(Eb,zero,p,v)
    right+=F(eh_cubic_16k(A,tuple(-z for z in p),La,p,Eb,zero)+
             eh_cubic_16k(A,tuple(-z for z in p),Ea,zero,Lb,p),8)
   assert left+right==0,(i,j,f,left,right);checks+=1
   if left:nonzero.append(dict(fiber=[i,j],fixture=f,tadpole_Ward=str(left),reference_transport=str(right)))
  clear_caches()
assert nonzero;checks+=1
r=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 fibers=55,fixtures_per_fiber=3,nonzero_count=len(nonzero),nonzero_controls=nonzero[:12],
 identity='T_W(A,Gc)=-1/8 sum W_ab [V3raw(A,Lie_c Ea,Eb)+V3raw(A,Ea,Lie_c Eb)]',
 interpretation='Fixed anisotropic reference contributes a transport term; isotropic cancellation is not universal',
 reference_selected=False,full_Q2=False,gate_changed=False)
save('results.json',r);save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(r))
