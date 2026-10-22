"""Recover existing finite-gap review only; no new provider call/transitions."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1]
DEST=HERE.parent/'A6_EQUACAO_DA_VERDADE/received_reviews'
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
def digest(b):return hashlib.sha256(b).hexdigest()
def new(p,b):
    if p.exists():assert p.read_bytes()==b;return
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and b;t.replace(p)
job='46bc7f7d-0b2c-4238-892e-e9280a95cfd3'
record=Coordination(Runtime(recover=False)).get(job)
assert record['execution_constraints']['required_provider']=='kimi'
execution=record['execution'];assert execution['status']=='result_ready'
result=execution['result'];body=result['text'].encode('utf-8')
response=DEST/(job+'.md');new(response,body)
receipt=dict(job_id=job,request_id=record['request_id'],execution_id=execution['id'],
    provider='kimi',execution_status=execution['status'],response=str(response),
    prompt_sha256=digest(record['prompt'].encode()),response_sha256=digest(body),
    result_metadata={k:v for k,v in result.items() if k!='text'},scope='DECLARADO_AWAITING_LOCAL_REVIEW')
new(DEST/(job+'.json'),json.dumps(receipt,ensure_ascii=False,indent=2).encode())
ledger=CHAT/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl';old=ledger.read_bytes()
marker='A6_FINITE_GAP_RESULT_RECOVERED_VIA_API'
if marker.encode() not in old:
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(ledger.with_name(ledger.name+'.bak_'+stamp),old)
    event=dict(event=marker,at=datetime.now(timezone.utc).isoformat(),target='A-6.B1b',
        provider='kimi',job_id=job,request_id=record['request_id'],execution_id=execution['id'],
        prompt_sha256=receipt['prompt_sha256'],response_sha256=receipt['response_sha256'],
        usage=result.get('usage'),cost_estimate_usd=result.get('cost_estimate_usd'),
        new_external_execution=False,status=receipt['scope'])
    raw=old+(json.dumps(event,ensure_ascii=False)+'\n').encode()
    tmp=ledger.with_name(ledger.name+'.tmp_'+stamp);new(tmp,raw);tmp.replace(ledger)
print(json.dumps(dict(response=str(response),bytes=len(body),usage=result.get('usage'),
    execution_id=execution['id'],stage=record['stage']),ensure_ascii=False))
