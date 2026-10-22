"""Read two completed Kimi results once; no execution transitions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,uuid
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];BASE=CHAT/'IALD_ORQUESTRACAO_20260923'
DEST=HERE/'received_reviews';DEST.mkdir(exist_ok=True)
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
def sha(b):return hashlib.sha256(b).hexdigest()
def new(path,b):
    if path.exists():assert path.read_bytes()==b;return
    t=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(path)
co=Coordination(Runtime(recover=False));ledger=CHAT/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl'
for job in ['ba337b71-5345-44e7-8481-04a24ba1569e','1cb94397-825d-4005-8dc1-933481d302c0']:
    d=co.get(job);ex=d['execution'];assert ex['status']=='result_ready'
    assert d['execution_constraints']['required_provider']=='kimi'
    res=ex['result'];body=res['text'].encode();path=DEST/(job+'.md');new(path,body)
    receipt=dict(job_id=job,request_id=d['request_id'],execution_id=ex['id'],provider='kimi',
        prompt_sha256=sha(d['prompt'].encode()),response_sha256=sha(body),
        result_metadata={k:v for k,v in res.items() if k!='text'},status='DECLARADO_PENDING_LOCAL_REVIEW')
    new(DEST/(job+'.json'),json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    raw=ledger.read_bytes();marker='A7_KIMI_RESULT_RECOVERED_'+job
    if marker.encode() not in raw:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
        new(ledger.with_name(ledger.name+'.bak_'+stamp),raw)
        event=dict(event=marker,at=datetime.now(timezone.utc).isoformat(),provider='kimi',target='A-7.b',
            job_id=job,request_id=d['request_id'],execution_id=ex['id'],prompt_sha256=receipt['prompt_sha256'],
            response_sha256=receipt['response_sha256'],usage=res.get('usage'),cost_estimate_usd=res.get('cost_estimate_usd'),
            new_external_execution=False,statute='DECLARADO_PENDING_LOCAL_REVIEW')
        t=ledger.with_name(ledger.name+'.tmp_'+stamp);new(t,raw+(json.dumps(event,ensure_ascii=False)+'\n').encode());t.replace(ledger)
    print(json.dumps(dict(job_id=job,path=str(path),bytes=len(body),usage=res.get('usage'),cost=res.get('cost_estimate_usd')),ensure_ascii=False))
