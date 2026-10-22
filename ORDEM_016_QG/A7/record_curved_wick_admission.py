"""Record official admission without taking over queue transitions."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, uuid

H=Path(__file__).resolve().parent
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
source=BASE/'state/handoffs/a7_curved_wick_defect_pending_submissions.json'
receipt=json.loads(source.read_bytes())
unit=next(v for v in receipt['units'] if v['request_id']=='87d118f3-08c3-49c3-bc24-fa78ff10d0c9')
payload=Path(unit['payload'])
assert hashlib.sha256(payload.read_bytes()).hexdigest()==unit['payload_sha256']
assert unit['status']=='REGISTERED_WAITING_FRESH_WORKER' and unit['job_id']
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')

def atomic(p, data):
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp)
        assert not b.exists();b.write_bytes(old);assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(data)
    assert t.read_bytes()==data;t.replace(p)

d=H/'curved_defect_descent_review_delivery/ADMISSION_RECEIPT.json'
assert not d.exists()
record=dict(at=now.isoformat(),source=str(source),
    source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),unit=unit,
    worker_owned_by='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',new_executor_calls=0)
atomic(d,json.dumps(record,ensure_ascii=False,indent=2).encode('utf-8'))
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
state['pending_orchestration']='MiMoa46 running last observed; MiMo87d admitted awaiting fresh audited worker after drain; Kimi e710/51c/709 waiting and d3 staging due five-hour quota; DeepSeek6309 complete/audited'
state['latest_verified_orchestration']['mimo_next']=unit
state['latest_verified_orchestration']['admission_receipt']=str(d)
atomic(p,json.dumps(state,ensure_ascii=False,indent=2).encode('utf-8'))
p=OUT/'LEDGER_016.jsonl'
event=dict(at=now.isoformat(),event='ORCHESTRATION_UNIT_ADMITTED',target='A7.b',
    provider='mimo',request_id=unit['request_id'],job_id=unit['job_id'],
    status=unit['status'],receipt_sha256=hashlib.sha256(d.read_bytes()).hexdigest(),
    new_executor_calls=0)
atomic(p,p.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode('utf-8'))
p=OUT/'ENTREGA_016_PROGRESSO.md'
atomic(p,p.read_bytes()+f'\n{now.isoformat()} MiMo87d admitido job{unit["job_id"]}; aguarda worker auditado após a46. Nenhuma nova chamada de executor nesta admissão.\n'.encode('utf-8'))
print(json.dumps(event,ensure_ascii=False))
