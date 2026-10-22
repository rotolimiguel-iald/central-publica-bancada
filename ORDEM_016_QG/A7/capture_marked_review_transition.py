"""Read authoritative mission jobs and register a terminal transport failure."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,uuid
H=Path(__file__).resolve().parent;CHAT=H.parents[1]
sys.path.insert(0,str(CHAT/'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,b):
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        backup=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
coord=Coordination(Runtime(recover=False));receipts=[]
for job in ['ab543117-b279-407c-8d0a-6d036b234b1b','f1293276-0c3a-4b5b-bbf6-b3585a862ad2']:
    d=coord.get(job);ex=d.get('execution') or {};res=ex.get('result') or {}
    receipt=dict(at=datetime.now(timezone.utc).isoformat(),job_id=job,request_id=d['request_id'],
        provider=d['execution_constraints']['required_provider'],status=d.get('status'),
        execution_id=ex.get('id'),execution_status=ex.get('status'),
        prompt_sha256=sha(d['prompt'].encode()),result_present=bool(res),
        usage=res.get('usage'),cost_estimate_usd=res.get('cost_estimate_usd'),
        new_external_execution=False)
    if job.startswith('ab54'):
        receipt.update(diagnostic='IncompleteRead per official coordinator notification; confirmed terminal API state',
            unknown_cost_not_zero=True,no_retry=True)
        assert ex.get('status')=='failed',receipt
        ledger=CHAT/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl';raw=ledger.read_bytes()
        marker='A7_MIMO_MARKED_WICK_TRANSPORT_FAILED'
        if marker.encode() not in raw:
            event=dict(receipt,event=marker,target='A-7.b')
            save(ledger,raw+(json.dumps(event,ensure_ascii=False)+'\n').encode())
    receipts.append(receipt)
path=H/'received_reviews'/'A7_transition_after_mimo_marked_failure.json'
save(path,json.dumps(receipts,ensure_ascii=False,indent=2).encode())
print(json.dumps(receipts,ensure_ascii=False))
