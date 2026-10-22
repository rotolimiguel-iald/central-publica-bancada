"""Record blocked egress and a running local proof, without touching payloads."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
R=Path(__file__).resolve().parents[1];D=R/'D6';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha
now=datetime.now(timezone.utc).isoformat()
catalog=json.loads((D/'orchestration/connections_catalog.json').read_bytes())
result=dict(at=now,status='AUTO_REVIEW_REJECTED_PENDING_SPECIFIC_EGRESS_CONSENT',external_calls_made=False,
 request_ids=[x['request_id'] for x in catalog],catalog_sha256=sha(D/'orchestration/connections_catalog.json'),
 reason='Automatic review requires specific approval for the new scientific payloads and MiMo/DeepSeek/Gemini destinations. Async question pending; no alternative route attempted.',
 kimi_separate=dict(status='RUNNING_AS_REPORTED_BY_OFFICIAL_COORDINATOR',request_id='abb30fb0-3a32-409e-85dc-4fd96d5dd602',job_id='634022b1-7544-4c1e-9a34-57e551e1047f',execution_id='f12e7df1-c4cb-4966-933a-41a4cecc32b4',usage=None,cost=None))
save(D/'orchestration/CONNECTIONS_APPROVAL_PENDING.json',result)
p=OUT/'LEDGER_016.jsonl';old=p.read_bytes()
entry=dict(at=now,event='NEW_THREE_PAYLOADS_AUTO_REVIEW_REJECTED',branch='D6',external_call_made=False,cost_usd=None,request_ids=result['request_ids'],receipt_sha256=sha(D/'orchestration/CONNECTIONS_APPROVAL_PENDING.json'))
write(p,old+(json.dumps(entry,ensure_ascii=False)+'\n').encode(),True)
p=R/'A7/CONTINUIDADE.json';st=json.loads(p.read_bytes());st.update(at=now,own_live_process={'session_id':1693,'source':str(D/'RecognitionModular.lean'),'label':'modular_01','started':'2026-09-26T12:07:02Z'},D6_pending_dispatch=str(D/'orchestration/CONNECTIONS_APPROVAL_PENDING.json'),next='Poll compiler session1693, do not restart. Kimi graph critic RUNNING (official coordinator job634022b1); three new connections payloads NOT SUBMITTED after automatic review rejection, explicit user egress question pending. Source RecognitionModular composes existing root/imaginary-power lemmas under independent analytic graph realizations. D6 still priority; B unregistered.');save(p,st,True)
print(json.dumps(dict(status=result['status'],pending_requests=len(catalog),compiler_session=1693)))
