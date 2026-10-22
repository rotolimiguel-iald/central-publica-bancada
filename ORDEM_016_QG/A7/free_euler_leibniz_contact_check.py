"""Check total Leibniz contact against the fixed pair-extension engine."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from logarithmic_contact_engine import contact,residue,Q
H=Path(__file__).resolve().parent;D=H/'free_euler_leibniz_contact';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
start=time.process_time();checks=0
def eq(a,b):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
a,t=s.symbols('a tau');q2=sum(q*q for q in Q)
first=4*t*a*(t*a-1);second=4*(1-t)*a*((1-t)*a-1)
cross=8*(t*a-1)*((1-t)*a-1)
total=4*(a-2)*(a-1)
eq(first+second+cross,total)
res=residue(3,(0,0,0,0),(1,1,1,1))
def correction(co):return s.expand(s.diff(co,a).subs(a,0)*res)
euler=correction(first+second);cross_correction=correction(cross)
fixed=-sum(contact(2,0,(i,i)) for i in range(4))
eq(euler,q2/8);eq(cross_correction,q2/4)
eq(euler+cross_correction,correction(total));eq(correction(total),fixed)
eq(fixed,3*q2/8)
for value in [s.Integer(0),s.Rational(1,2),s.Integer(1),s.Rational(2,3)]:
 eq(correction(first).subs(t,value)+correction(second).subs(t,value)+cross_correction,fixed)
source=json.loads((H/'free_euler_insertion_contact/results.json').read_bytes())
locals={str(q):q for q in Q};locals['tau']=t
eq(s.sympify(source['scalar_contacts']['sum'],locals=locals),euler)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 identity='box(f_a*g_a)=(box f_a)g_a+2 grad f_a.grad g_a+f_a(box g_a)',
 total_contact_normalized=str(fixed),sum_euler_contacts=str(euler),
 cross_gradient_contact=str(cross_correction),allocation_independent_total=True,
 interpretation='The first-line allocation dependence does not alter the existing ordinary pair extension; total Leibniz agrees exactly with its contact engine.',
 scope='Scalar rational simple-pole sector only, not a choice of time-ordered EOM axiom or a complete gravitational loop',
 full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'logarithmic_contact_engine.py',H/'free_euler_insertion_contact/results.json',D/'results.json']]))
print(json.dumps(result))
