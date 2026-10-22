"""Verify jet realization of current before contracting it in a loop."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
from classical_current_jet_engine import current,current_coefficients,evaluate,split_word
from localized_brst_flux_engine import cubic_bv_flux,dot,add
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'classical_current_jets';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'classical_current_jet_engine.py',H/'localized_brst_flux_engine.py',H/'localized_brst_flux/manifest.json']
for row in json.loads(sources[-1].read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Polynomial representative J_BV(h,h,c0) on internal metric jets through order2 and external ghost jets through order2',
 proof='J is homogeneous degree2 in12 derivative markers: EH quadratic degree2,Lie degree1,Green degree1. Polarization reconstructs all78 coefficients, not a truncation fit.',
 tests='Two nonzero generic momenta per55 symmetric fiber pairs; compare current and Ward divergence; exchanged legs independently',full_Q2=False))
start=time.process_time();checks=0;rows=[];second_internal=0;second_ghost=0
points=[((1,2,-1,1),(2,-1,0,3),(0,1,1,0)),((-2,1,3,0),(0,1,-1,2),(2,0,-1,1))]
for a in range(10):
 for b in range(a,10):
  coeff=current_coefficients(a,b,0)
  for p,q,k in points:
   predicted=evaluate(coeff,p,q,k);direct=current(BASIS[a],p,BASIS[b],q,0,k)
   for u,v in zip(predicted,direct):assert u==v;checks+=1
   old=cubic_bv_flux(BASIS[a],p,BASIS[b],q,(1,0,0,0),k)
   assert dot(add(p,q,k),predicted)==old['ward_lhs'];checks+=1
   swapped=evaluate(current_coefficients(b,a,0),q,p,k)
   for u,v in zip(predicted,swapped):assert u==v;checks+=1
  data=[]
  for monomial,c in coeff.items():
   pw,qw,kw=split_word(monomial)
   if len(pw)==2 or len(qw)==2:second_internal+=1
   if len(kw)==2:second_ghost+=1
   data.append(dict(monomial=monomial,pword=pw,qword=qw,kword=kw,current=list(map(str,c))))
  rows.append(dict(a=a,b=b,coefficients=data))
 put('fibers_'+str(a)+'.json',dict(rows=[r for r in rows if r['a']==a],cpu_seconds=time.process_time()-start))
 print('CURRENT_JET',a,'checks',checks,'cpu',time.process_time()-start,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,rows=rows,
 internal_second_derivative_monomials=second_internal,external_ghost_second_derivative_monomials=second_ghost,
 ghost_component=0,full_Q2=False,scope='Classical metric BV current jet realization; no loop contraction or ghost-sector current yet')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
