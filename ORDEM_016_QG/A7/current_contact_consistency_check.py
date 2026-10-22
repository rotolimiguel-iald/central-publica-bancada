"""Distinguish invariant highest-order contact from cutoff-dependent descent."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from full_loop_extension_engine import Q
from position_metric_bubble_engine import LABELS
H=Path(__file__).resolve().parent;D=H/'current_contact_consistency';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
start=time.process_time();checks=0
data=json.loads((H/'full_current_contact_matrix/results.json').read_bytes());A={};top={}
locals={str(q):q for q in Q};q2=sum(q*q for q in Q)
for row in data['rows']:
 f=s.sympify(row['polynomial'],locals=locals);key=row['a'],row['c'];A[key]=f
 top[key]=s.expand(sum(co*s.prod(q**p for q,p in zip(Q,powers)) for powers,co in s.Poly(f,*Q).terms() if sum(powers)==5))
a,b,c=s.symbols('a b c');equations=[]
for (index,r),f in top.items():
 i,j=LABELS[index];m=1 if i==j else 2
 ansatz=m*(a*int(i==j)*Q[r]*q2**2+b*Q[i]*Q[j]*Q[r]*q2+c*(int(i==r)*Q[j]+int(j==r)*Q[i])*q2**2)
 equations.extend(s.Poly(s.expand(f-ansatz),*Q).coeffs())
solutions=s.solve(equations,[a,b,c],dict=True);assert len(solutions)==1;checks+=1
sol=solutions[0]
assert sol[a]==-s.Rational(139,1920) and sol[b]==s.Rational(217,960);checks+=2
B=s.zeros(4)
for (index,r),f in top.items():
 i,j=LABELS[index];B[j,r]-=Q[i]*f;B[i,r]-=Q[j]*f
B=B.applyfunc(s.expand)
adj=B.T.applyfunc(lambda f:s.expand(f.subs({q:-q for q in Q},simultaneous=True)))
for f in B-adj:assert f==0;checks+=1

# The full prescribed localized representative is not a cocycle in h/c alone.
defect=s.Matrix([[s.sympify(v,locals=locals) for v in row] for row in data['graded_adjoint_defect']])
nonzero=sum(f!=0 for f in defect);assert nonzero;checks+=1
L=tuple(x+y for x,y in zip(data['lambda_x'],data['eta_y']))
star=defect.T.applyfunc(lambda f:s.expand(f.subs({Q[i]:-Q[i]-L[i] for i in range(4)},simultaneous=True)))
for f in (defect+star).applyfunc(s.expand):assert f==0;checks+=1
# No degree6 term survives: the inconsistency measured here is lower differential order.
for f in defect:assert s.Poly(f,*Q).total_degree()<=5;checks+=1
control=defect[0,1].subs(dict(zip(Q,(0,0,0,0))))
assert control!=0;checks+=1

result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 highest_order_coefficients={str(k):str(v) for k,v in sol.items()},
 highest_order_wz_defect_zero=True,full_localized_h_c_defect_nonzero_entries=nonzero,
 defect_01_at_q_zero=str(control),weighted_formal_adjoint_antisymmetry_verified=True,
 interpretation='Highest-order flat bulk recovers invariant contact and closes; localized h-c representative alone requires remaining descent/normalization before a cohomology class can be assigned',
 full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'full_current_contact_matrix/results.json',D/'results.json']]))
print(json.dumps(result))
