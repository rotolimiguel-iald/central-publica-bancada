"""Custody and single accounting only; scientific audit belongs to Part C5."""
from pathlib import Path
import sys,json,hashlib
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append
D=H.parent/'ADENDO_002_CRITICAS/C24_RECEIVED';D.mkdir(exist_ok=False)
src=BASE/'state/handoffs/7f044602-7a5c-4c9a-8f59-7930175e4e93_delivery.json'
j=json.loads(src.read_bytes())['job'];e=j['execution'];r=e['result'];assert e['status']=='result_ready'
now=datetime.now(timezone.utc).isoformat()
write(D/'KIMI_ORIGINAL.md',r['text'].encode())
data=dict(at=now,statute='DECLARADO_UNREVIEWED',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],
    source_sha256=sha(src),prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),response_sha256=sha(D/'KIMI_ORIGINAL.md'),
    usage=r['usage'],cost_estimate_usd=r.get('cost_estimate_usd'),cost_unknown_not_zero=r.get('cost_estimate_usd') is None,
    scientific_audit='PENDING_PART_C5',canonical_memory=r.get('canonical_memory'))
put(D/'RECEIPT.json',data)
ledger=OUT/'LEDGER_016.jsonl';rows=[json.loads(x) for x in ledger.read_text('utf-8').splitlines() if x.strip()]
assert not any(e['id'] in json.dumps(v) and 'completion_tokens' in json.dumps(v) for v in rows)
append(ledger,json.dumps(dict(data,event='C24_RECEIVED_PENDING_C5_AUDIT',target='ADENDO002.C2.4',provider='kimi'))+'\n')
print(json.dumps({k:data[k] for k in ['at','usage','scientific_audit','response_sha256']}))
