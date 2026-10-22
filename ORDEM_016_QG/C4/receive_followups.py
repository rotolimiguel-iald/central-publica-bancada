"""Receive completed/failed scientific units exactly once; never dispatch."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C4/orchestration'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,write,append
events=[]
for provider,jid,label in [('kimi','d2d79420-27a5-4d4f-bd2e-ac37bed55bb8','KIMI_AE_FAILURE'),('deepseek','3197e661-7f22-4af8-87c8-78e5105a17c0','DEEPSEEK_KMS')]:
    p=BASE/'state/handoffs'/(jid+'_delivery.json');j=json.loads(p.read_bytes())['job'];e=j['execution'];r=e['result']
    event=dict(at=datetime.now(timezone.utc).isoformat(),event='C4_FOLLOWUP_RECEIVED',target=label,provider=provider,request_id=j['request_id'],job_id=jid,
        execution_task_id=e['id'],source_receipt=str(p),source_receipt_sha256=sha(p),status=e['status'],
        prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),retry=False,scientific_status='DECLARADO_PENDING_LOCAL_CHECK')
    if r:
        assert e['status']=='result_ready'
        write(D/(label+'_ORIGINAL.md'),r['text'].encode())
        event.update(response_sha256=sha(D/(label+'_ORIGINAL.md')),usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],canonical_memory=r.get('canonical_memory'))
    else:
        assert e['status']=='failed'
        event.update(error=e['error'],usage=None,cost_estimate_usd=None,unknown_is_not_zero=True)
    put(D/(label+'_RECEIPT.json'),event);events.append(event)
append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in events))
print(json.dumps([dict(provider=x['provider'],status=x['status'],cost=x['cost_estimate_usd']) for x in events]))
