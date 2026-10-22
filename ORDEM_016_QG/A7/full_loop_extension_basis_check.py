"""Complete the flat symmetric tensor basis, reusing already computed entries."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
from full_loop_extension_engine import SymbolicRawLoop,loop_contact,Q
from flat_loop_cutoff_engine import tensor
from position_metric_bubble_engine import LABELS

H=Path(__file__).resolve().parent;D=H/'full_loop_extension_basis';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'full_loop_extension_engine.py',H/'full_loop_extension/manifest.json',H/'bilocal_XY_extension_contact/results.json',H/'source_two_cutoff_assembly/manifest.json']
for folder in ['full_loop_extension','source_two_cutoff_assembly']:
 for row in json.loads((H/folder/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],target='All10 symmetric polarizations and4 ghosts,3 exponential-cutoff configurations',
 exclusions=['curvature','full localized source','classical-current insertion','tadpoles','higherarities','causal continuation'],full_Q2=False))
start=time.process_time();checks=0;q2=sum(q*q for q in Q);parse=lambda t:s.sympify(t,locals={str(q):q for q in Q})
old=json.loads((H/'bilocal_XY_extension_contact/results.json').read_bytes())['coefficients_over_C_E']
print('OLD_KEYS',list(old),flush=True)
# Flat coefficients agree for both already declared completions.
c0=list(map(s.Rational,old['geodesic'][0]));assert c0==list(map(s.Rational,old['coordinate'][0]));checks+=1
# Recover source invariant coefficients from previously computed r=0 data.
source=json.loads((H/'source_two_cutoff_assembly/results.json').read_bytes())['values'];lam=s.Symbol('lam')
u,v,w=s.symbols('u v w')
def form(co,a,b,r):
 return co[0]*int(a==b)*Q[r]*q2**2+co[1]*(int(a==r)*Q[b]+int(b==r)*Q[a])*q2**2+co[2]*Q[a]*Q[b]*Q[r]*q2
eqs=[]
for a,b in [(1,1),(0,1),(0,0)]:
 val=s.sympify(source[str((-1,a,b))],locals={'lam':lam,**{str(q):q for q in Q}}).subs(lam,0)
 eqs+=s.Poly(s.expand(form([u,v,w],a,b,0)-val),*Q).coeffs()
sol=s.solve(eqs,(u,v,w),dict=True);assert len(sol)==1;sc=[sol[0][a] for a in (u,v,w)]
for a in range(4):
 for b in range(4):
  val=s.sympify(source[str((-1,a,b))],locals={'lam':lam,**{str(q):q for q in Q}}).subs(lam,0)
  assert s.expand(val-form(sc,a,b,0))==0;checks+=1
put('source_invariant_check.json',dict(coefficients=list(map(str,sc)),checks=16,rotation_basis='O4 invariant flat prescription'))
rows=[];nonzero=0
for label,lx,ly in [('constant',(0,0,0,0),(0,0,0,0)),('Y_exp',(0,0,0,0),(1,0,0,0)),('XY_exp',(1,-1,0,0),(1,0,0,0))]:
 for a,b in LABELS:
  engines={kind:SymbolicRawLoop(kind,tensor(a,b),lx,ly) for kind in ['ghost','metric']}
  for r in range(4):
   p={}
   for kind,e in engines.items():
    if (a,b,r)==(1,1,0):p[kind]=parse(json.loads((H/'full_loop_extension'/(label+'_'+kind+'.json')).read_bytes())['polynomial'])
    else:p[kind]=loop_contact(e,r)/(1 if a==b else 2)
   combo=s.expand(p['ghost']-p['metric']/2)
   if label=='constant':assert s.expand(combo+form(sc,a,b,r)-form(c0,a,b,r))==0,(a,b,r,combo);checks+=1
   assert s.Poly(combo,*Q).total_degree()<=5;checks+=1
   if combo!=0:nonzero+=1
   row=dict(case=label,a=a,b=b,r=r,ghost=str(s.expand(p['ghost'])),metric=str(s.expand(p['metric'])),combined=str(combo),value2100=str(combo.subs(dict(zip(Q,(2,1,0,0))))))
   rows.append(row)
  put(label+'_'+str(a)+str(b)+'.json',dict(rows=rows[-4:],cpu_cumulative=time.process_time()-start))
  print('BASIS',label,a,b,'checks',checks,'cpu',time.process_time()-start,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,components=len(rows),nonzero=nonzero,rows=rows,
 full_Q2=False,scope='Complete10x4 flat pair tensor basis for3 fixed exponential-cutoff jets; not arbitrary lambda/eta or all quantum diagrams')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'source_invariant_check.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,cpu_seconds=result['cpu_seconds'],components=len(rows),nonzero=nonzero)))
