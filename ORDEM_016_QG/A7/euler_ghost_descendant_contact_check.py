"""Calculate ordered two-ghost descendant under a labeled insertion family."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from euler_ghost_descendant_contact_engine import Q,TAU,euler_line_contact,ordered_descendant,weighted_defect
H=Path(__file__).resolve().parent;D=H/'euler_ghost_descendant_contact';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Raw ordered I_E,X Vghost,Y contact, two external ghosts',
 insertion_family='Split radial regulator parameter tau; not selected as the physical normalization',
 excluded='No fitted tau, no overall effective-action sign, no automatic exchange factor, no full Q2',
 engine_sha256=sha(H/'euler_ghost_descendant_contact_engine.py')))
start=time.process_time();checks=0
def eq(a,b):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
q2=sum(q*q for q in Q)
eq(euler_line_contact((),()),TAU*q2/8)
for j in range(4):
 eq(euler_line_contact((),(j,)),TAU*Q[j]*q2/24)
 eq(euler_line_contact((j,),()),TAU*Q[j]*q2/12)
lam=(1,-1,0,0);eta=(1,0,0,0);L=tuple(x+y for x,y in zip(lam,eta))
B,count=ordered_descendant(lam,eta);defect=weighted_defect(B,L)
zero,zero_count=ordered_descendant((0,0,0,0),eta)
assert zero==s.zeros(4) and zero_count==0;checks+=1
for value in B:
 eq(value.subs(TAU,0),0)
 eq(value,TAU*value.subs(TAU,1))
for value in weighted_defect(defect,L)-2*defect:eq(value,0)
# Independent constant/cutoff bookkeeping control: exchanging labels is a different ordered insertion.
reverse,nreverse=ordered_descendant(eta,lam)
assert reverse!=B;checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 lambda_x=lam,eta_y=eta,ordered_terms=count,reverse_ordered_terms=nreverse,
 B=[[str(v) for v in row] for row in B.tolist()],
 weighted_antisymmetric_part=[[str(v) for v in row] for row in defect.tolist()],
 reverse_B=[[str(v) for v in row] for row in reverse.tolist()],
 defect_01_at_q_zero=str(defect[0,1].subs(dict.fromkeys(Q,0))),
 normalization='Raw ordered Euler insertion times Vghost; CE=-4pi² suppressed, tau symbolic',
 conclusion='Explicit candidate descendant for the declared insertion family, still requiring its normalization and global Ward weight to be derived; no tau selected by matching',
 full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'euler_ghost_descendant_contact_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ['B','reverse_B','weighted_antisymmetric_part']}))
