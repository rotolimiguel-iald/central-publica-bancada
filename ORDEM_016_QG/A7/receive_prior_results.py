"""Read-only provider receipt recovery via Coordination.get, without a new call."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[1]
DEST = HERE.parent/'A5'/'received_results'
DEST.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
coord = Coordination(Runtime(recover=False))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write_new(p,raw):
    if p.exists():
        assert p.read_bytes()==raw, p
        return
    t=p.with_suffix(p.suffix+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)

ledger=CHAT/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl'
events=[]
summary=[]
for job,provider in [('08addf0a-def3-4757-9140-958cb96b72fc','deepseek'),
                     ('51a28f15-0463-43f7-b2d0-ad712e390cd3','mimo')]:
    r=coord.get(job)
    ex=r['execution'];result=ex['result']
    assert r['stage']=='completed',r['stage']
    assert r['execution_constraints']['required_provider']==provider
    body=result['text'].encode('utf-8')
    response=DEST/(job+'.md')
    write_new(response,body)
    metadata={key:val for key,val in result.items() if key!='text'}
    receipt=dict(job_id=job,request_id=r['request_id'],execution_id=ex['id'],
                 provider=provider,stage=r['stage'],execution_status=ex['status'],
                 prompt_sha256=sha(r['prompt'].encode('utf-8')),
                 response_sha256=sha(body),response=str(response),
                 result_metadata=metadata,scope='DECLARADO_AWAITING_FULL_LOCAL_REVIEW')
    write_new(DEST/(job+'.json'),json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    event=dict(event='A5_RESULT_RECOVERED_VIA_API',at=datetime.now(timezone.utc).isoformat(),
               provider=provider,target='A-5',job_id=job,request_id=r['request_id'],
               execution_id=ex['id'],prompt_sha256=receipt['prompt_sha256'],
               response_sha256=receipt['response_sha256'],usage=result.get('usage'),
               cost_estimate_usd=result.get('cost_estimate_usd'),
               new_external_execution=False,status='DECLARADO_AWAITING_FULL_LOCAL_REVIEW')
    events.append(event)
    summary.append({key:receipt[key] for key in ('job_id','provider','response','stage')})
    summary[-1]['cost_estimate_usd']=result.get('cost_estimate_usd')
    summary[-1]['response_bytes']=len(body)
old=ledger.read_bytes()
existing=[json.loads(line) for line in old.decode('utf-8-sig').splitlines() if line.strip()]
events=[e for e in events if not any(x.get('event')==e['event'] and x.get('execution_id')==e['execution_id'] for x in existing)]
if events:
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    bak=ledger.with_name(ledger.name+'.bak_'+stamp)
    write_new(bak,old)
    raw=old+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode()
    temp=ledger.with_name(ledger.name+'.tmp_'+stamp)
    write_new(temp,raw)
    temp.replace(ledger)
print(json.dumps(summary,ensure_ascii=False,indent=2))
