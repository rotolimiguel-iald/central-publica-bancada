"""Exact finite-dimensional tests of the old frame and its radial correction."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C4'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import sha,put,write,OUT,append
start=time.process_time();checks=[]
r=s.symbols('r',positive=True);a,b,t,u=s.symbols('a b t u',real=True)
eta=s.diag(1,-1,-1,-1);k=s.Matrix([1,0,1,0])
def B(x):return s.Matrix([[s.cosh(x),s.sinh(x),0,0],[s.sinh(x),s.cosh(x),0,0],[0,0,1,0],[0,0,0,1]])
R=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,a,-b],[0,0,b,a]])
c=(r+1/r)/2;h=(r-1/r)/2
Y=s.Matrix([[c,0,h,0],[0,1,0,0],[h,0,c,0],[0,0,0,1]])
def zero(x):return s.simplify(s.expand_trig(s.expand(x))).subs(a*a,1-b*b).simplify()
def check(name,x):
    assert zero(x)==0,(name,x,zero(x));checks.append(name)
def mat(name,X):
    for i,x in enumerate(X):check(name+':'+str(i),x)
L=B(t)*R*Y; old=R*B(t);p=r*s.Matrix([s.cosh(t),s.sinh(t),a,b])
mat('corrected_L_maps_reference_to_actual_p',L*k-p)
mat('old_L_maps_only_to_p_over_r',old*k-p/r)
mat('corrected_L_is_Lorentz',L.T*eta*L-eta)
check('corrected_L_det_one',L.det()-1)
mat('boost_equivariance_of_corrected_section',B(u)*L-L.subs(t,t+u))
mat('null_momentum',s.Matrix([(p.T*eta*p)[0]]))
assert (old*k-p).subs({r:2,a:1,b:0,t:0})!=s.zeros(4,1)
checks.append('old_section_fails_actual_reference_at_r2')
check('correct_inverse_at_xi_log2',s.asinh(s.Rational(3,4)).rewrite(s.log)-s.log(2))
assert s.simplify(s.atanh(s.Rational(3,4))-s.log(2))!=0
checks.append('atanh_p1_over_r_is_wrong_at_xi_log2')
# A fixed spacetime rotation around y does not commute with the x boost.
phi=s.symbols('phi',real=True)
Ry=s.Matrix([[1,0,0,0],[0,s.cos(phi),0,s.sin(phi)],[0,0,1,0],[0,-s.sin(phi),0,s.cos(phi)]])
comm=B(u)*Ry-Ry*B(u)
assert s.simplify(comm[0,3])==s.sin(phi)*s.sinh(u)
checks.append('fixed_y_rotation_does_not_commute_with_x_boost')
raw=ROOT/'A5/63b4e640-2b1a-4f7e-8213-76b2eb94d3e5_received_response.json'
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),names=checks,cpu_seconds=time.process_time()-start,
    old_response=str(raw),old_response_sha256=sha(raw),status='EXACT_CAS_SECTION_AND_OLD_RESPONSE_CORRECTIONS',
    assumptions=['r>0','a,b real','a^2+b^2=1','auxiliary flat Minkowski signature +---'],
    corrected_section='L(q,xi)=Bx(xi) Rx(a,b) By(log r), a=q0/r,b=q1/r',
    exact_test='By(log r) represented by (r+r^-1)/2 and (r-r^-1)/2',
    conclusions=['Lk=p, not merely p/r','Lorentz and det1','Bx(s)L(q,xi)=L(q,xi+s)','inverse rapidity is arsinh(p1/r)',
        'constant internal little-group character is not a fixed global spacetime Ry subgroup commuting with Bx'],
    exclusions=['No global induced representation built','No arbitrary Lorentz cocycle integrated on L2','No regional modular witness','CAS is not Lean'],gate_changed=False)
put(D/'SECTION_CAS.json',result)
rows=[('mimo','46fca62c-b3fa-44f9-90e0-20da44607d6e','2372eee7-6542-4ba0-81b0-695206dad41f','ab8fb940-b160-4514-855f-f5db6c1b887f'),
('kimi','8c777290-e8fa-491d-9a52-4c047643e5bb','d2d79420-27a5-4d4f-bd2e-ac37bed55bb8','e07d5379-4c38-463e-af72-453eff8c9967'),
('deepseek','aa091239-5a5e-4bd0-a466-7839d37dc19e','3197e661-7f22-4af8-87c8-78e5105a17c0','080b7322-bd26-4539-80f5-ea1354610484')]
events=[dict(at=result['at'],event='C4_UNITS_RUNNING_OFFICIAL_COORDINATOR',provider=pr,request_id=rid,job_id=jid,execution_task_id=eid,
    status='RUNNING_REPORTED_BY_OFFICIAL_COORDINATOR',usage=None,cost_estimate_usd=None) for pr,rid,jid,eid in rows]
put(D/'orchestration/RUNNING_IDS.json',events)
append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(x)+'\n' for x in events))
print(json.dumps(dict(checks=len(checks),cpu_seconds=result['cpu_seconds'])))
