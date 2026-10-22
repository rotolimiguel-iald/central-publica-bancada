"""Check the symmetric cutoff polarization without choosing weights from results."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from full_loop_extension_engine import Q
H=Path(__file__).resolve().parent;D=H/'polarized_current_contact';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
start=time.process_time();checks=0
left=H/'full_current_contact_matrix/results.json';right=H/'full_current_contact_matrix_swapped/results.json'
l=json.loads(left.read_bytes());r=json.loads(right.read_bytes());symbols={str(q):q for q in Q}
assert l['lambda_x']==r['eta_y'] and l['eta_y']==r['lambda_x'];checks+=1
dl=s.Matrix([[s.sympify(f,locals=symbols) for f in row] for row in l['graded_adjoint_defect']])
dr=s.Matrix([[s.sympify(f,locals=symbols) for f in row] for row in r['graded_adjoint_defect']])
# Plus, fixed by polarization of the two even interactions, not fitted.
combined=((dl+dr)/2).applyfunc(s.expand)
L=tuple(x+y for x,y in zip(l['lambda_x'],l['eta_y']))
adj=combined.T.applyfunc(lambda f:s.expand(f.subs({Q[i]:-Q[i]-L[i] for i in range(4)},simultaneous=True)))
for value in (combined+adj).applyfunc(s.expand):assert value==0;checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 cutoff_polarization='(A(lambda,eta)+A(eta,lambda))/2, fixed plus sign',
 combined_wz_defect=[[str(v) for v in row] for row in combined.tolist()],
 combined_defect_nonzero_entries=sum(v!=0 for v in combined),
 defect_01_at_q_zero=str(combined[0,1].subs(dict.fromkeys(Q,0))),
 h_c_alone_closed=combined==s.zeros(4),full_Q2=False,gate_changed=False,
 scope='Tests whether missing symmetric cutoff polarization explains previous h-c diagnostic; does not substitute this sector for full BV complex')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),left,right,D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='combined_wz_defect'}))
