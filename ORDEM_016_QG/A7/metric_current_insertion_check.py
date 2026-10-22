"""Contract actual J_BV vertex and audit one flat current-insertion diagram."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
from metric_current_insertion_engine import CurrentInsertion,opword,x,z,dx,Q
from flat_loop_cutoff_engine import tensor
H=Path(__file__).resolve().parent;D=H/'metric_current_insertion';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'metric_current_insertion_engine.py',H/'classical_current_jets/manifest.json',H/'full_loop_extension_engine.py']
for row in json.loads(sources[2].read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Classical metric current at Y paired with cubic metric vertex at X, with full jets and cutoffs',
 convention='Jraw from cubic BV current; insertion -dchiY.J, raw metric pair normalization /16, NO diagram symmetry factor',
 tests='Symbolic raw kernel against numeric contraction then all adjoint derivatives; cutoff constant vanishes by construction, not a physical test',
 full_Q2=False,exclusions=['ghost current diagrams','overall Ward diagram coefficients not assembled','curvature','smooth remainder','higherarities','causality']))
start=time.process_time();checks=0;rows=json.loads((H/'classical_current_jets/results.json').read_bytes())['rows'];point=(1,2,-1,1);sub=dict(zip(x,point));sub[z]=7
result=[]
for label,lam,eta in [('Y_exp',(0,0,0,0),(1,0,0,0)),('XY_exp',(1,-1,0,0),(1,0,0,0))]:
 e=CurrentInsertion(tensor(1,1),lam,eta,rows);n=CurrentInsertion(tensor(1,1),lam,eta,rows,point)
 actual=0
 for kw in sorted({k[-1] for k in e.terms}):
  for ex in [-1,0,1,2,3]:
   f=e.raw(ex,kw)
   assert s.expand(f.subs(sub)-n.raw(ex,kw))==0;checks+=1
   for word,c in opword(kw,ex,lam,eta).items():
    v=f
    for i in word:v=dx(v,i)
    vn=s.expand(v.subs(sub));assert vn==n.raw(ex,kw,word);checks+=1
    actual+=c*vn
  print('CURRENT_PAIR',label,'kword',kw,'checks',checks,'cpu',time.process_time()-start,flush=True)
 assert s.expand(actual-n.off_diagonal())==0;checks+=1
 pol=e.extension_contact()
 row=dict(case=label,off_diagonal=str(actual),extension_contact=str(pol),contact_at2100=str(pol.subs(dict(zip(Q,(2,1,0,0))))))
 result.append(row);put(label+'.json',row)
 print('CURRENT_CONTACT',label,'cpu',time.process_time()-start,flush=True)
out=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,rows=result,full_Q2=False,
 scope='Single metric-current insertion, h11/c0, flat singular pair, two fixed cutoff configurations; no physical Ward total coefficient asserted')
put('results.json',out);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(out))
