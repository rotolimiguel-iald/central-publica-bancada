"""Recover a completed review without any execution transition."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1]
DEST=HERE.parent/'A6_EQUACAO_DA_VERDADE/received_reviews'
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
def sha(b):return hashlib.sha256(b).hexdigest()
def new(p,b):
    if p.exists():assert p.read_bytes()==b;return
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
job='99bbefc3-504b-4c4c-a361-80efb8ba1e42'
d=Coordination(Runtime(recover=False)).get(job);ex=d['execution']
assert d['execution_constraints']['required_provider']=='mimo' and ex['status']=='result_ready'
res=ex['result'];body=res['text'].encode();path=DEST/(job+'.md');new(path,body)
receipt=dict(job_id=job,request_id=d['request_id'],execution_id=ex['id'],provider='mimo',
    response_sha256=sha(body),prompt_sha256=sha(d['prompt'].encode()),
    result_metadata={k:v for k,v in res.items() if k!='text'},scope='DECLARADO_PENDING_LOCAL_REVIEW')
new(DEST/(job+'.json'),json.dumps(receipt,ensure_ascii=False,indent=2).encode())
ledger=CHAT/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A6_MIMO_C2_RESULT_RECOVERED'
if marker.encode() not in raw:
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(ledger.with_name(ledger.name+'.bak_'+stamp),raw)
    event=dict(event=marker,at=datetime.now(timezone.utc).isoformat(),provider='mimo',target='A-6.C',
        job_id=job,request_id=d['request_id'],execution_id=ex['id'],prompt_sha256=receipt['prompt_sha256'],
        response_sha256=receipt['response_sha256'],usage=res.get('usage'),cost_estimate_usd=res.get('cost_estimate_usd'),
        new_external_execution=False,statute='DECLARADO_PENDING_LOCAL_REVIEW')
    t=ledger.with_name(ledger.name+'.tmp_'+stamp);new(t,raw+(json.dumps(event,ensure_ascii=False)+'\n').encode());t.replace(ledger)
print(json.dumps(dict(response=str(path),bytes=len(body),usage=res.get('usage'),execution_id=ex['id']),ensure_ascii=False))
