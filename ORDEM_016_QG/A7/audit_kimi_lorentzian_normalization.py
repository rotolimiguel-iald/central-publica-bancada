"""Audit algebraic identities in a received response; no boundary-value theorem claimed."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s
from logarithmic_contact_engine import contact

H=Path(__file__).resolve().parent
D=H/'kimi_lorentzian_normalization_review'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
stamp=now.strftime('%Y%m%d_%H%M%S_%f')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,append=False):
    assert b
    if p.exists():
        assert append,p
        old=p.read_bytes(); bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
        b=old+b
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(b);assert tmp.read_bytes()==b;tmp.replace(p)
def put(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))

D.mkdir(exist_ok=False)
receipt=BASE/'state/handoffs/23034d1b-28b1-4a40-8410-c33b79a0f209_delivery.json'
data=json.loads(receipt.read_bytes());job=data['job'];execution=job['execution'];result=execution['result']
assert job['stage']=='completed' and result['model']=='kimi-code/k3'
write(D/'RECEIPT.json',receipt.read_bytes())
write(D/'RESPONSE.md',result['text'].encode('utf-8'))
put(D/'INTAKE.json',dict(at=now.isoformat(),source=str(receipt),sha256=sha(receipt),
    request_id=job['request_id'],job_id=job['id'],execution_task_id=execution['id'],
    status='DECLARADO_PENDING_LOCAL_AUDIT',usage=result['usage'],new_provider_call=False))
ledger=OUT/'LEDGER_016.jsonl'
old_events=[json.loads(x) for x in ledger.read_text('utf-8').splitlines()]
assert not any(e.get('execution_task_id')==execution['id'] for e in old_events)
event=dict(at=now.isoformat(),event='KIMI_LORENTZIAN_NORMALIZATION_RECEIVED',provider='kimi',target='A7.b',
    job_id=job['id'],request_id=job['request_id'],execution_task_id=execution['id'],
    usage=result['usage'],provider_elapsed_seconds=result['elapsed_seconds'],cost_estimate_usd=None,
    cost_status='SUBSCRIPTION_COST_NOT_REPORTED_NOT_ZERO',receipt_sha256=sha(receipt),
    response_sha256=sha(D/'RESPONSE.md'),prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),
    scientific_status='DECLARADO_PENDING_LOCAL_AUDIT',remote_call_by_this_script=False)
write(ledger,(json.dumps(event,ensure_ascii=False)+'\n').encode('utf-8'),append=True)

start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert s.simplify(a-b)==0,(a,b);checks+=1
x=s.symbols('x0:4',real=True);z=sum(t*t for t in x)
for i in range(4):
    for j in range(4):
        derivative=s.diff(1/z,x[i],x[j])
        expected=-2*int(i==j)/z**2+8*x[i]*x[j]/z**3
        eq(derivative,expected)
        quoted=-2*int(i==j)/z**2+4*x[i]*x[j]/z**3
        eq(derivative-quoted,4*x[i]*x[j]/z**3)
eps=s.symbols('eps',positive=True);sigma=s.symbols('sigma',real=True)
eq(1/(eps+s.I*sigma),-s.I/(sigma-s.I*eps))
wrong=s.simplify(1/(eps+s.I*sigma)+s.I/(sigma+s.I*eps))
assert wrong!=0;checks+=1
eq(wrong,2*eps/(sigma**2+eps**2))
metric=(-1,1,1,1);sigma_x=sum(g*y*y for g,y in zip(metric,x))
box=sum(g*s.diff(1/(sigma_x+s.I*eps),y,2) for g,y in zip(metric,x))
eq(box,-8*s.I*eps/(sigma_x+s.I*eps)**3)
assert s.simplify(box-8*s.I*eps/(sigma_x+s.I*eps)**3)!=0;checks+=1
for i in range(4):eq(contact(1,0,(i,i)),-s.Rational(1,4))
eq(sum(contact(1,0,(i,i)) for i in range(4)),-1)

audit=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    corrections=[
      'Euclidean Hessian coefficient of x_i*x_j/z^3 is 8, not 4.',
      '(eps+i*sigma)^(-1)=-i/(sigma-i*eps); the response identifies it with the opposite branch.',
      'For eps>0, box(1/(sigma+i*eps))=-8*i*eps/(sigma+i*eps)^3, not positive.',
      'Same-endpoint (R D_i D_j-D_i D_j R)/C_E has diagonal -1/4; the quoted +1/4 belongs to opposite-endpoint derivatives.'
    ],finite_epsilon_wrong_branch_difference=str(wrong),
    rejected_scope='The proposed Lorentzian normalization and transfer are not validated by this response.',
    unverified=['Distributional boundary-value normalization','Global cone decomposition','All-order poles and curvature continuation'],
    scope='Exact rational differentiation and comparison with the already fixed Euclidean prescription only.',
    full_Q2=False,gate_changed=False)
put(D/'local_audit.json',audit)
put(D/'manifest.json',dict(opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',D/'INTAKE.json',D/'local_audit.json']],
    remote_calls=0,gate_changed=False))
print(json.dumps(audit,ensure_ascii=False))
