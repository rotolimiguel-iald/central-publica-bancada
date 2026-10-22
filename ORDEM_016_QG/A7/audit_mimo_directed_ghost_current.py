"""Audit received ghost-current response against chain rule and graded contractions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from ghost_current_insertion_engine import GhostCurrentInsertion
from position_metric_bubble_engine import BASIS,LABELS
H=Path(__file__).resolve().parent;D=H/'mimo_directed_ghost_current_review';D.mkdir(exist_ok=False)
OUT=H.parents[1]/'TUNEL/DO_CHATGPT';BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,append=False):
 if p.exists():
  assert append;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);assert not bak.exists()
  bak.write_bytes(old);assert bak.read_bytes()==old;b=old+b
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def put(n,v):write(D/n,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
source=BASE/'state/handoffs/224bfef0-2105-46fe-9c26-4be72014769e_delivery.json'
data=json.loads(source.read_bytes());j=data['job'];e=j['execution'];r=e['result']
assert j['stage']=='completed' and r['model']=='mimo-v2.6-pro'
write(D/'RECEIPT.json',source.read_bytes());write(D/'RESPONSE.md',r['text'].encode('utf-8'))
put('INTAKE.json',dict(at=now.isoformat(),job_id=j['id'],request_id=j['request_id'],
 execution_task_id=e['id'],scientific_status='DECLARADO_PENDING_LOCAL_AUDIT',source=str(source),sha256=sha(source)))
ledger=OUT/'LEDGER_016.jsonl'
assert not any(json.loads(l).get('execution_task_id')==e['id'] for l in ledger.read_text('utf-8').splitlines())
event=dict(at=now.isoformat(),event='MIMO_DIRECTED_GHOST_CURRENT_RECEIVED',provider='mimo',target='A7.b',
 job_id=j['id'],request_id=j['request_id'],execution_task_id=e['id'],usage=r['usage'],
 cost_estimate_usd=r['cost_estimate_usd'],cost_status=r['cost_status'],provider_elapsed_seconds=r['elapsed_seconds'],
 receipt_sha256=sha(source),response_sha256=sha(D/'RESPONSE.md'),
 prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),remote_call_by_this_script=False)
write(ledger,(json.dumps(event)+'\n').encode(),True)
start=time.process_time();checks=0
def eq(a,b):
 global checks
 assert s.simplify(a-b)==0,(a,b);checks+=1
X=s.symbols('X0:4');Y=s.symbols('Y0:4')
forward=1/sum((X[i]-Y[i])**2 for i in range(4))
reverse=1/sum((Y[i]-X[i])**2 for i in range(4))
for i in range(4):
 eq(s.diff(forward,X[i]),s.diff(reverse,X[i]))
 assert s.diff(forward,X[i])!=-s.diff(reverse,X[i]);checks+=1
eq(-1+s.Rational(1,2)+1-s.Rational(1,2),0)
assert s.Integer(0)!=-s.Rational(1,2);checks+=1

def derivative(poly,i):
 out={}
 for word,value in poly.items():
  if i in word:
   n=word.index(i);key=word[:n]+word[n+1:]
   out[key]=out.get(key,0)+(-1)**n*value
 return out
def gamma(poly,cov):
 out={}
 for (i,j),coef in cov.items():
  for word,v in derivative(derivative(poly,i),j).items():out[word]=out.get(word,0)+coef*v
 return out
u,v,w=s.symbols('u v w');poly={(0,1,2,3,4):s.Integer(1)}
cov={(0,3):-u,(0,4):-v,(1,2):w}
out=gamma(gamma(poly,cov),cov)
eq(out[(4,)]/2,-u*w);eq(out[(3,)]/2,v*w)

T=BASIS[LABELS.index((1,1))];point=(1,2,-1,1);lam=(0,0,0,0);eta=(1,0,0,0)
whole=GhostCurrentInsertion(T,0,lam,eta,point).off_diagonal()
first=GhostCurrentInsertion(T,0,lam,eta,point,omit=1).off_diagonal()
second=GhostCurrentInsertion(T,0,lam,eta,point,omit=0).off_diagonal()
eq(first+second,whole);assert whole!=0;checks+=1
# The real vertex is Lie_c h with ghost jets, not trace-reversed h alone.
h=s.diag(0,1,0,0);c=s.zeros(4,1)
Lie=s.zeros(4);trace_reversed=h-s.eye(4)*s.trace(h)/2
assert Lie==s.zeros(4) and trace_reversed!=s.zeros(4);checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 rejected_claims=['Both directed Wick signs negative; exact signs are minus and plus in supplied ordering',
  'd_X f(Y-X)=-d_X f(X-Y); since f is even these derivatives are equal',
  'Replace trace-reversed Lie_c h by trace-reversed h, losing the ghost and its derivatives',
  'The rational coefficient sum -1+1/2+1-1/2=-1/2; it equals zero',
  'Both directed contractions sum to zero in the supplied nonzero-cutoff control'],
 control=dict(h='h11',c=0,point=point,lambda_x=lam,eta_y=eta,first=str(first),second=str(second),sum=str(whole)),
 scientific_status='REJECTED_IN_THIS_REPRESENTATIVE_AFTER_EXACT_COUNTEREXAMPLES',
 full_Q2=False,gate_changed=False)
put('local_audit.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',D/'INTAKE.json',D/'local_audit.json']]))
print(json.dumps(result,ensure_ascii=False))
