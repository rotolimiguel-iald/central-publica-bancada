"""Selected local controls on the received DeepSeek scope/series statements."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import einstein_test_field_engine as E
H=Path(__file__).resolve().parent;D=H/'deepseek_adjoint_review';D.mkdir(exist_ok=True)
receipt=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/25292039-6bed-4b01-a788-cef4e7bfe55e_delivery.json'
data=json.loads(receipt.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=v.encode() if isinstance(v,str) else json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('RESPONSE.md',data['result']['text'])
put('RECEIPT.json',dict(at=data['at'],job_id=data['job_id'],execution_task_id=data['execution_task_id'],
    usage=data['result']['usage'],cost_estimate_usd=data['result']['cost_estimate_usd'],
    cost_status=data['result']['cost_status'],receipt_sha256=sha(receipt),response_sha256=sha(D/'RESPONSE.md')))
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Density series, trace of test versus metric correction; anchored smooth off-diagonal counterexample',
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'einstein_test_field_engine.py',D/'RESPONSE.md']],
    excludes='No new proof of full Einstein formal selfadjointness'))
cpu=time.process_time();K=s.Symbol('K');h0=s.Matrix(4,4,lambda i,j:s.Symbol('h'+str(min(i,j))+str(max(i,j))))
h1=s.eye(4);checks=[]
inv=s.eye(4)+K*E.inv1
expanded=((1-K*E.Z/2)*inv*(h0+K*h1)*inv).applyfunc(s.expand)
actual=E.density([h0,h1])
for o in (0,1):
    for i in range(4):
        for j in range(4):
            assert s.expand(expanded[i,j].coeff(K,o)-actual[o][i,j])==0
            checks.append([o,i,j])
assert s.expand(s.trace(E.g1)+E.Z)==0;checks.append('trace_metric_correction')
assert s.trace(s.eye(4))==4 and s.trace(s.eye(4))!=-E.Z
checks.append('arbitrary_test_trace_not_metric_trace')
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-cpu,
    status='SELECTED_DENSITY_SERIES_CHECKED_REVIEW_SCOPE_CORRECTED',
    corrected=['[E0,E1] is a formal K series, not K=1; adding a second K would double count',
               'tr(g1)=-X², not tr(h)=-X² for arbitrary test h',
               'Y=0 anchoring leaves X dependence; 1/X² is nonzero on neighborhoods away from X=0 and is not a contact'],
    original_task_unfulfilled_by_provider='Formal selfadjointness derivation and requested controls were not supplied',
    accepted='Need to distinguish cutoff, R, source orientation, smooth W and full Q2',
    full_Q2=False,whole_operator_certified=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'einstein_test_field_engine.py',D/'RESPONSE.md',D/'RECEIPT.json',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
