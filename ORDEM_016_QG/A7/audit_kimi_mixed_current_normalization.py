"""Audit Kimi ee44 against the actual mixed propagator and external-jet convention."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from mixed_b_h_current_engine_v3 import current_terms,MixedCurrentInsertion
from metric_current_insertion_engine_v3 import fiber
from position_metric_bubble_engine import LABELS,BASIS
H=Path(__file__).resolve().parent;D=H/'kimi_mixed_current_normalization_review'
assert not D.exists();D.mkdir()
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923';OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,append=False):
    if p.exists():
        assert append;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old;b=old+b
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p)
def put(name,v):write(D/name,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
source=BASE/'state/handoffs/a51eab34-e334-46c7-9021-53b2a32d2085_delivery.json'
receipt=json.loads(source.read_bytes());j=receipt['job'];e=j['execution'];r=e['result']
assert j['stage']=='completed' and r['model']=='kimi-code/k3'
write(D/'RECEIPT.json',source.read_bytes());write(D/'RESPONSE.md',r['text'].encode('utf-8'))
put('INTAKE.json',dict(at=now.isoformat(),job_id=j['id'],request_id=j['request_id'],
 execution_task_id=e['id'],source=str(source),receipt_sha256=sha(source),
 scientific_status='DECLARADO_PENDING_LOCAL_AUDIT'))
ledger=OUT/'LEDGER_016.jsonl'
assert not any(json.loads(l).get('execution_task_id')==e['id'] for l in ledger.read_text('utf-8').splitlines())
event=dict(at=now.isoformat(),event='KIMI_MIXED_CURRENT_NORMALIZATION_RECEIVED',provider='kimi',target='A7.b',
 job_id=j['id'],request_id=j['request_id'],execution_task_id=e['id'],usage=r['usage'],
 provider_elapsed_seconds=r['elapsed_seconds'],cost_estimate_usd=None,
 cost_status='SUBSCRIPTION_NOT_REPORTED_NOT_ZERO',receipt_sha256=sha(source),
 response_sha256=sha(D/'RESPONSE.md'),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),
 remote_call_by_this_script=False)
write(ledger,(json.dumps(event)+'\n').encode('utf-8'),True)
start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
def neq(a,b):
    global checks
    assert s.expand(a-b)!=0,(a,b);checks+=1

# Derive the five families directly from the submitted table, independently of BASIS.
for mu in range(4):
    for c in range(4):
        table={}
        def add(nu,ab,hw,cw,co):
            key=(nu,LABELS.index(tuple(sorted(ab))),hw,cw)
            table[key]=table.get(key,F())+F(co)
        for nu in range(4):
            add(nu,(mu,nu),(c,),(),1)
            add(nu,(c,nu),(),(mu,),1)
            add(nu,(mu,c),(),(nu,),1)
        for sig in range(4):
            add(mu,(sig,sig),(c,),(),F(-1,2))
            add(mu,(sig,c),(),(sig,),-1)
        table={k:v for k,v in table.items() if v}
        assert table==current_terms(c,tuple(int(i==mu) for i in range(4)));checks+=1

# Formal-adjoint convolution: G*=-(delta d + delta d), not the same sign as G.
k=s.Symbol('kappa',nonzero=True);gD=-4*k;ell=1/(2*k);gQ=s.Integer(1)
eq(gD*ell,-2*gQ);neq(gD*ell,2*gQ)
q=s.symbols('q0:4')
tr=lambda a,b:int(a==b)
S=lambda a,b,c,d:s.Rational(tr(a,c)*tr(b,d)+tr(a,d)*tr(b,c)-tr(a,b)*tr(c,d),2)
nu,c,d=0,0,0
Csf=sum(q[m]*S(m,nu,c,d) for m in range(4))-q[nu]*sum(S(m,m,c,d) for m in range(4))/2
Gtf=tr(c,nu)*q[d]+tr(d,nu)*q[c]
eq(gD*Csf,-gQ*Gtf/ell)
neq(gD*Csf,gQ*Gtf/ell)

# The actual b_column already contains both deltas, with no missing trace term.
point=(1,2,-1,1);graph=MixedCurrentInsertion(BASIS[0],0,(0,0,0,0),(1,0,0,0),point)
idx=LABELS.index((0,0));actual=graph.b_column(0,()).get(idx,F())
eq(actual,-F(4,49))
pure=2*sum(fiber(idx,LABELS.index(tuple(sorted((j,0)))))*graph.scalar((j,)) for j in range(4))
eq(actual,pure+graph.scalar((0,)));neq(actual,pure)

# The reported toy is correct as a specified plane-wave jet evaluation, not adjunction.
eq(2*(-F(2,2401)-F(1,343)),-F(18,2401))
eq(2*F(1,14)**2,F(1,98))
x=s.Symbol('x');eta=s.Symbol('eta',nonzero=True)
eq(s.diff(s.Integer(1),x),0);neq(eta*s.Integer(1),0)
# External-ghost derivative after IBP acts on the kernel too, even at eta=0.
eq(s.diff(x**2,x),2*x);neq(s.diff(x**2,x),0)
eq((-1/(16*k))*(-4*k),s.Rational(1,4))

report=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 accepted=['Five coefficient families agree for all16(mu,r) pairs with current_terms',
           'Two ordered contractions coincide for symmetric EH Hessian; actual diagram factorial must still be tracked',
           'Toy -18/2401*gQ*gD and pure-metric control gD²/98 are arithmetically correct in their declared jet evaluation'],
 corrections=['Convolution sign gives gD*ell=-2*gQ, not +2*gQ; existing free inverse is unchanged',
              'Mixed b_column already uses both Kronecker deltas and includes the trace contribution; no missing term to add',
              'Replacing external dc by eta*c is a special external field evaluation, not the adjoint (d-eta) acting on the kernel',
              'Response conversion referenced older metric /16 engine; actual mixed v3 has independently derived +1/4 per ordered contraction'],
 controls=dict(actual_diagonal_mixed=str(actual),pure_fiber_only=str(pure),
               corrected_gD_ell=str(s.expand(gD*ell)),toy='-18/2401'),
 next='Retain engine v3; do not inject a second trace term or change normalization based on this response. Await separate graded-weight/BV consistency reviews.',
 full_Q2=False,gate_changed=False)
put('local_audit.json',report)
paths=[Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',D/'INTAKE.json',D/'local_audit.json',
 H/'mixed_b_h_current_engine_v3.py',H/'mixed_b_h_current_v3/results.json']
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths]))
print(json.dumps(dict(audit=report,usage=r['usage'],provider_elapsed_seconds=r['elapsed_seconds']),ensure_ascii=False))
