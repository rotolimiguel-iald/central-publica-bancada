"""Receive exactly one completed scientific result; ledger usage once."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT=H.parents[1]/'TUNEL/DO_CHATGPT';D=H/'mimo_source_preibp_review';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,b,existing=False):
    if p.exists():
        assert existing;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b==t.read_bytes();t.replace(p)
p=BASE/'state/handoffs/c7ee8599-9976-46ef-b4ad-6b128f79d3b4_delivery.json';raw=p.read_bytes()
j=json.loads(raw)['job'];e=j['execution'];r=e['result'];assert j['stage']=='completed'
write(D/'RECEIPT.json',raw);write(D/'RESPONSE.md',r['text'].encode('utf-8'))
event=dict(at=now.isoformat(),event='MIMO_SOURCE_PREIBP_RECEIVED',provider='mimo',target='A7.b',
    job_id=j['id'],request_id=j['request_id'],execution_task_id=e['id'],usage=r['usage'],
    cost_estimate_usd=r['cost_estimate_usd'],cost_status=r['cost_status'],provider_elapsed_seconds=r['elapsed_seconds'],
    receipt_sha256=sha(raw),response_sha256=sha(r['text'].encode('utf-8')),
    prompt_sha256=sha(j['prompt'].encode('utf-8')),scientific_status='DECLARADO_PENDING_LOCAL_AUDIT',remote_call_by_this_script=False)
write(D/'INTAKE.json',json.dumps(event,indent=2).encode())
ledger=OUT/'LEDGER_016.jsonl';rows=[json.loads(line) for line in ledger.read_text('utf-8').splitlines()]
if not any(row.get('execution_task_id')==e['id'] for row in rows):
    write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
print(json.dumps(event))
