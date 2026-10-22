"""Preserve completed scientific answer without executing its pseudocode."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;D=H/'kimi_curved_antifield_audit';D.mkdir(exist_ok=True)
p=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/3043848f-1e12-45b4-a5aa-127e2e3887fd_delivery.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
    if isinstance(b,str):b=b.encode()
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
d=json.loads(p.read_bytes());r=d['result'];put(D/'ANSWER.md',r['text'])
receipt=dict(at=datetime.now(timezone.utc).isoformat(),job_id=d['job_id'],source=str(p),source_sha256=sha(p),
 answer_sha256=sha(D/'ANSWER.md'),usage=r['usage'],model=r['model'],status='DECLARADO_PENDING_LOCAL_AUDIT',
 provider_code_executed=False)
put(D/'RECEIPT.json',json.dumps(receipt,ensure_ascii=False,indent=2))
print(json.dumps(dict(saved=True,chars=len(r['text']),lines=len(r['text'].splitlines()),usage=r['usage'])))
