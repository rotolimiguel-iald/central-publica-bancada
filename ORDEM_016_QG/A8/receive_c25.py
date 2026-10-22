"""Custody and single accounting only; scientific audit belongs to Part C3."""
from pathlib import Path
import sys,json,hashlib
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append
D=H.parent/'ADENDO_002_CRITICAS/C25_RECEIVED';D.mkdir(exist_ok=False)
src=BASE/'state/handoffs/7bcb6868-f9ce-456c-b42e-f8d5dd6041c3_delivery.json'
j=json.loads(src.read_bytes())['job'];e=j['execution'];r=e['result'];assert e['status']=='result_ready'
now=datetime.now(timezone.utc).isoformat()
write(D/'KIMI_ORIGINAL.md',r['text'].encode())
data=dict(at=now,statute='DECLARADO_UNREVIEWED',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],
    source_sha256=sha(src),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),response_sha256=sha(D/'KIMI_ORIGINAL.md'),
    usage=r['usage'],cost_estimate_usd=r.get('cost_estimate_usd'),cost_unknown_not_zero=r.get('cost_estimate_usd') is None,
    scientific_audit='PENDING_PART_C3',canonical_memory=r.get('canonical_memory'))
put(D/'RECEIPT.json',data)
ledger=OUT/'LEDGER_016.jsonl';rows=[json.loads(x) for x in ledger.read_text('utf-8').splitlines() if x.strip()]
assert not any(e['id'] in json.dumps(v) and 'completion_tokens' in json.dumps(v) for v in rows)
append(ledger,json.dumps(dict(data,event='C25_RECEIVED_PENDING_C3_AUDIT',target='ADENDO002.C2.5',provider='kimi'))+'\n')
print(json.dumps({k:data[k] for k in ['at','usage','scientific_audit','response_sha256']}))
