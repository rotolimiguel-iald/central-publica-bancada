"""Audit endpoint index typing and distributional scope of the Kimi reply."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E
from logarithmic_contact_engine import contact,direct_laurent_contact,Q
H=Path(__file__).resolve().parent;D=H/'kimi_bilocal_pair_review';D.mkdir(exist_ok=False)
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
receipt=BASE/'state/handoffs/3ceb40a7-8ef6-4f56-87b4-bf301e2a0337_delivery.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,value,raw=False):
 p=D/n;assert not p.exists();data=value if raw else json.dumps(value,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(data);assert t.read_bytes()==data;t.replace(p)
packet=json.loads(receipt.read_bytes());save('RECEIPT.json',receipt.read_bytes(),True);save('RESPONSE.md',packet['result']['text'].encode('utf-8'),True)
inputs=[Path(__file__),H/'bilocal_first_curvature_engine.py',H/'bilocal_covariant_jet_engine.py',
 H/'logarithmic_contact_engine.py',H/'transvection_endpoint_recurrence/DERIVACAO.md',D/'RESPONSE.md']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Verify explicit endpoint formulas; distinguish X upper and Y lower index; test contact extrapolation to two-line kernels',
 typing='ghost(o,a,b) has contravariant X slot a, covariant Y slot b; diverge on b at Y',
 reference='Existing exact engines unchanged, no provider retry',
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=0
def eq(a,b=0):
 global checks
 assert s.cancel(s.expand(a-b))==0,(a,b);checks+=1
for j in range(4):
 for a in range(4):
  for b in range(4):
   claimed=(B.r[j]*int(a==b)-2*int(a==j)*B.r[b]+B.r[a]*int(b==j))/3
   eq(B.derivative(B.P1[a,b],'X',j)+B.derivative(B.P1[a,b],'Y',j),claimed)
 eq(B.derivative(B.distance1,'X',j)+B.derivative(B.distance1,'Y',j),
    2*(B.x[j]*B.r.dot(B.Y)-B.y[j]*B.r.dot(B.X))/3)
rows=[]
for a in range(4):
 # Literal expression from the reply: wrong endpoint slot for a Y divergence.
 literal=E.anchor(sum(B.derivative(B.ghost(1,b,a),'Y',b) for b in range(4)))
 literal_naive=E.anchor(-sum(B.derivative(B.ghost(1,b,a),'X',b) for b in range(4)))
 eq(literal,B.x[a]/B.xx);eq(literal_naive,3*B.x[a]/B.xx)
 # Correct covariant Y divergence. At the anchor inverse metric is delta.
 actual=E.anchor(sum(E.yjet('ghost',1,(a,b),(b,)) for b in range(4)))
 naive=E.anchor(-sum(B.derivative(B.ghost(1,a,b),'X',b) for b in range(4)))
 eq(actual,4*B.x[a]/B.xx);eq(naive,3*B.x[a]/B.xx)
 eq(actual-naive,B.x[a]/B.xx)
 flat=E.anchor(sum(E.yjet('ghost',0,(a,b),(b,)) for b in range(4)))
 eq(flat,2*B.x[a]/B.xx**2)
 rows.append(dict(component=a,literal_row_sum=str(literal),literal_naive=str(literal_naive),
                  Y_slot_divergence=str(actual),naive_minus_X=str(naive),correct_defect=str(s.cancel(actual-naive))))
contacts=[]
for i in range(4):
 eq(contact(1,0,(i,)),0)
 measured=contact(2,0,(i,));eq(measured,-Q[i]/8)
 eq(measured,direct_laurent_contact(2,0,(i,)))
 contacts.append(dict(index=i,kernel='z^-2',contact_Rderivative_minus_derivativeR_over_CE=str(measured)))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,
 rows=rows,contacts=contacts,
 retained='Explicit coefficient rule and failure of naive -dX; literal coordinate row sum reproduced',
 corrected='Literal row sum is not the Y divergence of the typed ghost kernel; correct coefficient4 not1',
 rejected_scope='No-contact first derivative for z^-1 cannot be extrapolated to z^-2 two-line kernels',
 complete_pair_Ward_supplied=False,full_Q2=False,gate_changed=False)
save('results.json',result);save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'RECEIPT.json',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
