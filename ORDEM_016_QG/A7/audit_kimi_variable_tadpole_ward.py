"""Audit raw vertex factors, conservation domain, and fixed-covector differentiation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from fractions import Fraction as F
import sympy as s
from metric_principal_vertices import gauge_matrix,lie_matrix,eh_cubic_16k
from metric_quartic_vertices import eh_quartic_32k
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'kimi_variable_tadpole_ward_review';D.mkdir(exist_ok=False)
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923';OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,append=False):
 if p.exists():
  assert append;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);assert not bak.exists()
  bak.write_bytes(old);assert bak.read_bytes()==old;b=old+b
 tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(b);assert b and tmp.read_bytes()==b;tmp.replace(p)
def put(n,v):write(D/n,json.dumps(v,indent=2,ensure_ascii=False).encode('utf-8'))
source=BASE/'state/handoffs/84b2dbe3-95cb-4dea-8752-ed0c41783525_delivery.json'
data=json.loads(source.read_bytes());j=data['job'];e=j['execution'];result=e['result']
assert j['stage']=='completed' and result['model']=='kimi-code/k3'
write(D/'RECEIPT.json',source.read_bytes());write(D/'RESPONSE.md',result['text'].encode('utf-8'))
put('INTAKE.json',dict(at=now.isoformat(),job_id=j['id'],request_id=j['request_id'],execution_task_id=e['id'],source=str(source),sha256=sha(source),scientific_status='DECLARADO_PENDING_LOCAL_AUDIT'))
ledger=OUT/'LEDGER_016.jsonl'
assert not any(json.loads(l).get('execution_task_id')==e['id'] for l in ledger.read_text('utf-8').splitlines())
event=dict(at=now.isoformat(),event='KIMI_VARIABLE_TADPOLE_WARD_RECEIVED',provider='kimi',target='A7.b',
 job_id=j['id'],request_id=j['request_id'],execution_task_id=e['id'],usage=result['usage'],
 cost_estimate_usd=None,cost_status='SUBSCRIPTION_NOT_REPORTED_NOT_ZERO',provider_elapsed_seconds=result['elapsed_seconds'],
 receipt_sha256=sha(source),response_sha256=sha(D/'RESPONSE.md'),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),remote_call_by_this_script=False)
write(ledger,(json.dumps(event)+'\n').encode(),True)
start=time.process_time();checks=0
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
add=lambda a,b:tuple(x+y for x,y in zip(a,b))
def ward(A,p,U,r,V,ss,k,v):
 raw4=eh_quartic_32k((A,p),(gauge_matrix(k,v),k),(U,r),(V,ss))
 raw3=[eh_cubic_16k(lie_matrix(A,p,k,v),add(p,k),U,r,V,ss),
       eh_cubic_16k(A,p,lie_matrix(U,r,k,v),add(r,k),V,ss),
       eh_cubic_16k(A,p,U,r,lie_matrix(V,ss,k,v),add(ss,k))]
 return raw4,raw3
A,U,V=BASIS[0],BASIS[0],BASIS[1]
p=(1,2,-1,1);r=(0,1,0,0);ss=(1,0,-1,0);v=(2,-1,1,3)
k=tuple(-sum(xs) for xs in zip(p,r,ss))
q4,c3=ward(A,p,U,r,V,ss,k,v)
eq(q4+2*sum(c3),0)
assert q4+sum(c3)!=0;checks+=1
eq(F(q4,16)+sum(F(x,8) for x in c3),0)
bad_k=(1,0,0,0);off4,off3=ward(A,p,U,r,V,ss,bad_k,v)
assert off4+2*sum(off3)!=0;checks+=1

# With a constant metric M and a fixed covector v(x), Lie_(M^-1 v) M=G(v).
# Its second derivative in M is zero. Both inverse-metric orderings are needed.
AA=s.Matrix([[1,2,0,0],[2,0,0,0],[0,0,1,0],[0,0,0,0]])
BB=s.Matrix([[0,1,0,0],[1,3,0,0],[0,0,0,0],[0,0,0,1]])
vv=s.Matrix([1,2,1,0]);kk=s.Matrix([1,0,1,0])
GG=lambda w:kk*w.T+w*kk.T
quoted=-GG(AA*BB*vv)-GG(BB*AA*vv)+GG(BB*AA*vv)
correct=-GG(AA*BB*vv)-GG(BB*AA*vv)+GG((AA*BB+BB*AA)*vv)
eq(correct,s.zeros(4));assert quoted!=s.zeros(4);checks+=1

# Fixed BRST reference does not mean spatially constant. Explicit data distinguish them.
x,y=s.symbols('x y');W=1+x+y+x*y
eq(s.diff(W,x).subs({x:0,y:0}),1);eq(s.diff(W,y).subs({x:0,y:0}),1)
eq(s.diff(W.subs(y,x),x),2+2*x)
report=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 accepted=['Unscaled action identity S4(A,Gc,U,V)+sum S3(Lie slots)=0 under constant-cutoff integrated action assumptions',
  'Quartic GammaGamma has two differentiated slots; variable W activates internal derivative groups',
  'Constant-W gauge contraction cannot be extrapolated to a general varying reference'],
 corrections=['The raw stored vertices need Qraw+2*sum(Craw)=0, not Qraw+sum(Craw)=0',
  'The integrated Ward identity requires momentum conservation or an explicit boundary current; free independent momenta do not satisfy it pointwise',
  'Fixed-covector second differentiation needs both inverse-metric orderings',
  's0 W=0 is a BRST convention, not the condition W10=W01=0; diagonal derivative is W10+W01'],
 control=dict(raw_quartic=str(q4),raw_cubic_terms=list(map(str,c3)),quoted_residual=str(q4+sum(c3)),
  corrected_residual=str(q4+2*sum(c3)),off_conservation_residual=str(off4+2*sum(off3)),
  fixed_covector_quoted_second=[[str(v) for v in row] for row in quoted.tolist()]),
 conclusion='Broad Noether organization retained; raw formulas and proposed free-momentum test cannot be used as delivered. Existing local derivative-tadpole computation stays authoritative.',
 full_Q2=False,gate_changed=False)
put('local_audit.json',report);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',D/'INTAKE.json',D/'local_audit.json',H/'finite_smooth_tadpole_derivative_jets/results.json']]))
print(json.dumps(report,ensure_ascii=False))
