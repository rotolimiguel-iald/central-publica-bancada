"""Wess-Zumino consistency of measured linear contact sectors, not full Q2."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations
import hashlib,json,time
import sympy as s
from smooth_general_fiber_engine import general_hessian,general_source
from smooth_variable_ward_engine import gauge,einstein,source
H=Path(__file__).resolve().parent;D=H/'assembled_contact_wz';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 p=D/n;assert not p.exists(),p
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
inputs=[Path(__file__),H/'smooth_general_fiber_engine.py',H/'smooth_variable_ward_engine.py',
 H/'bilocal_curved_contact_primitive/results.json',H/'smooth_general_fiber/DERIVACAO.md',
 H/'fourth_order_cutoff_bridge/results.json']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Assemble singular and general smooth contacts with cutoff; test antisymmetric two-ghost coefficient',
 scope='Flat 4D differential operators with compact C5 one-coordinate polynomial profiles; abstract graded proof separate',
 controls='Drop cutoff commutator and detect failure; verify free Einstein gauge identity',
 exclusions=['Full Q2','Higher arities','Lorentzian normalization','Choice of reference state'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
start=time.process_time();checks=0
def eq(a,b=0):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
x=s.symbols('x0:4',real=True);u=x[0];bump=(1-u*u)**6;chi=bump*(1+u+u*u)
ghosts=[s.Matrix([bump,u*bump,0,0]),s.Matrix([u*u*bump,0,bump,0]),s.Matrix([u*bump,bump,u*u*bump,bump])]
w=1+u+2*u*u;wg=2-u
fiber=tuple((i+1)*(j+1) for i in range(10) for j in range(10))
families=json.loads((H/'bilocal_curved_contact_primitive/results.json').read_bytes())['families']
b,c,t=s.symbols('b c t')
co=[s.sympify(v,locals={'b':b,'c':c,'t':t}).subs({b:0,c:0,t:0}) for v in families['geodesic']['flat']]
def singular(h):
 a1,a2,a3,a4,a5=co;z=h.applyfunc(lambda f:s.diff(f,u,4));tr=s.trace(z)
 e=s.Matrix([1,0,0,0]);col=z*e
 return (a1*z+a2*tr*s.eye(4)+a3*(e*e.T*tr+s.eye(4)*z[0,0])+
         a4*(e*col.T+col*e.T)/2+a5*e*e.T*z[0,0]).applyfunc(s.expand)
def N(h):return singular(h)+general_hessian(fiber,h,w,x)
def integrate(f):
 p=s.Poly(s.expand(f),u)
 return sum(co*s.Rational(2,n[0]+1) for n,co in p.terms() if n[0]%2==0)
def pair(h,k):return integrate(s.trace(h*k))
gs=[gauge(v,x) for v in ghosts];proper=[];wrong=[]
for v,g in zip(ghosts,gs):
 eg=einstein(g,x)
 for z in eg:eq(z)
 nh=N(g);nch=N(chi*g)
 rw=general_source(fiber,v,w,x)+source('ghost_I',v,wg,x)
 er=einstein(chi*rw,x)
 proper.append(((chi*nh+nch)/2+er).applyfunc(s.expand))
 wrong.append((chi*nh+er).applyfunc(s.expand))
neg=[];rows=[]
for i,j in combinations(range(len(gs)),2):
 value=pair(gs[i],proper[j])-pair(gs[j],proper[i]);eq(value)
 defect=pair(gs[i],wrong[j])-pair(gs[j],wrong[i])
 rows.append(dict(i=i,j=j,antisymmetric_ghost_coefficient=str(value),omitted_cutoff_defect=str(defect)))
 if defect!=0:neg.append([i,j,str(defect)])
assert neg,'Negative control must detect missing cutoff';checks+=1
r=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 ghost_pairs=rows,negative_controls=neg,free_parameters='b=c=t=0 only for this control; no physical selection',
 identity='Achi/CE=<h,Mchi Gc+E(chi R_W c)>; s0Achi=0 using Mchi*=Mchi and EG=0',
 scope='Contact sectors already measured, assembled together; smooth reference formal, not a state',
 full_Q2=False,quantum_consistency_all_arities=False,gate_changed=False)
save('results.json',r);save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(r))
