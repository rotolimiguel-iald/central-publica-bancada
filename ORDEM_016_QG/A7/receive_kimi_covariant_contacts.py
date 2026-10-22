"""Recover one existing completed review, without execution or transition."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,uuid
H=Path(__file__).resolve().parent;CHAT=H.parents[1];DEST=H/'received_reviews'
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
def sha(b):return hashlib.sha256(b).hexdigest()
def fresh(p,b):
    if p.exists():assert p.read_bytes()==b;return
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(b)
    assert q.read_bytes()==b;q.replace(p)
job='b9d7e1a5-06fd-4f6d-8ed8-e82084aff2e8'
d=Coordination(Runtime(recover=False)).get(job);ex=d['execution']
assert d['execution_constraints']['required_provider']=='kimi' and ex['status']=='result_ready'
assert d['request_id']=='aed4b3f3-d9f7-4922-9f7a-f5cd4b1a8100'
res=ex['result'];body=res['text'].encode();path=DEST/(job+'.md');fresh(path,body)
receipt=dict(job_id=job,request_id=d['request_id'],execution_id=ex['id'],provider='kimi',
    response_sha256=sha(body),prompt_sha256=sha(d['prompt'].encode()),
    result_metadata={k:v for k,v in res.items() if k!='text'},scope='DECLARADO_PENDING_LOCAL_REVIEW')
fresh(DEST/(job+'.json'),json.dumps(receipt,ensure_ascii=False,indent=2).encode())
ledger=CHAT/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_KIMI_COVARIANT_CONTACTS_RECEIVED'
if marker.encode() not in raw:
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    fresh(ledger.with_name(ledger.name+'.bak_'+stamp),raw)
    event=dict(event=marker,at=datetime.now(timezone.utc).isoformat(),provider='kimi',target='A-7.b',
        job_id=job,request_id=d['request_id'],execution_id=ex['id'],prompt_sha256=receipt['prompt_sha256'],
        response_sha256=receipt['response_sha256'],usage=res.get('usage'),cost_estimate_usd=res.get('cost_estimate_usd'),
        new_external_execution=False,statute='DECLARADO_PENDING_LOCAL_REVIEW')
    q=ledger.with_name(ledger.name+'.tmp_'+stamp);fresh(q,raw+(json.dumps(event,ensure_ascii=False)+'\n').encode());q.replace(ledger)
print(json.dumps(dict(response=str(path),bytes=len(body),usage=res.get('usage'),execution_id=ex['id']),ensure_ascii=False))
