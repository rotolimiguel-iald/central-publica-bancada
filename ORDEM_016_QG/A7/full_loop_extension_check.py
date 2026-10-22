"""Compare raw loop extension with saved uncut contact and localized kernels."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from fractions import Fraction as F
from full_loop_extension_engine import SymbolicRawLoop,loop_contact,contact,x,z,Q
from flat_loop_cutoff_engine import FlatLoop,tensor
from full_eh_localized_loop_engine import FullEHLoop
from localized_ghost_boundary_engine import FullGhostLoop
import logarithmic_contact_engine as R

H=Path(__file__).resolve().parent;D=H/'full_loop_extension';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'full_loop_extension_engine.py',H/'logarithmic_contact_engine.py',H/'bilocal_XY_extension_contact/results.json',H/'source_two_cutoff_assembly/results.json',H/'full_localized_vertices_delivery/manifest.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],target='Pair derivative-extension commutator from full raw localized kernels',
 cutoff='Exponential jets near diagonal; compact realization possible',scope='Flat singular pair only; no classical current insertion/source boundary completion or fullQ2',full_Q2=False))
start=time.process_time();checks=0;rows=[];point=(1,2,-1,1);sub=dict(zip(x,point));sub[z]=sum(v*v for v in point)
def eq(a,b):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
for n in range(1,4):
 for word in [(0,),(0,0),(0,1),(0,0,1)]:eq(contact(z**(-n),word),R.contact(n,0,word))
q2=sum(q*q for q in Q)
for label,lx,ly in [('constant',(0,0,0,0),(0,0,0,0)),('Y_exp',(0,0,0,0),(1,0,0,0)),('XY_exp',(1,-1,0,0),(1,0,0,0))]:
    pols={}
    for kind in ['ghost','metric']:
        e=SymbolicRawLoop(kind,tensor(1,1),lx,ly)
        numeric=(FullGhostLoop if kind=='ghost' else FullEHLoop)(point,tensor(1,1))
        # Raw contraction comparison checks vertex/propagator normalizations
        # before derivative-extension contact, including nonzero boundary jets.
        for ex in [-1,0,1]:
          for a,r,j in [(0,0,-1),(1,0,0),(1,0,1),(2,0,2)]:
            actual=e.raw_expression(ex,j,a,r).subs(sub)
            expected=0
            for vx in [-1,0,1,2,3]:
              cx=1 if vx<0 else lx[vx]
              for vy in [-1,0,1,2,3]:
                cy=1 if vy<0 else ly[vy]
                if cx*cy:expected+=cx*cy*numeric.full_raw(vx,vy,ex,(),j,a,r)
            eq(actual,expected)
        pol=loop_contact(e,0);pols[kind]=pol
        put(label+'_'+kind+'.json',dict(polynomial=str(pol),cpu_cumulative=time.process_time()-start))
        print('CONTACT',label,kind,'cpu',time.process_time()-start,flush=True)
    combined=s.expand(pols['ghost']-pols['metric']/2)
    row=dict(case=label,lambdaX=lx,etaY=ly,component=[1,1,0],loop_polynomial=str(combined),at_q_2100=str(combined.subs(dict(zip(Q,(2,1,0,0))))))
    if label=='constant':
      # The old total adds the already computed Einstein/source contact.
      source=json.loads((H/'source_two_cutoff_assembly/results.json').read_bytes())['controls'][0]['at_constant_X']
      src=s.sympify(source,locals={str(q):q for q in Q})
      old=(-s.Rational(139,1920)*Q[0]*q2**2+s.Rational(217,960)*Q[1]**2*Q[0]*q2)
      eq(combined+src,old);row['old_pair_plus_source_recovered']=True
    rows.append(row);put(label+'_combined.json',row)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,rows=rows,full_Q2=False,
 scope='One tensor component of exact raw flat singular pair contact with fullEH/ghost cutoff vertices; not all tensors,curvature,source,current or arities')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
