from pathlib import Path
from datetime import datetime, timezone
import json, subprocess, sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def save(p,raw):
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)
rp=HERE/'deepseek_orbit_receipt.json';r=json.loads(rp.read_text(encoding='utf8'))
call=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'bridge.py')],input=json.dumps(dict(operation='get',job_id=r['job_id'])),capture_output=True,encoding='utf8',timeout=60)
assert call.returncode==0
j=json.loads(call.stdout)
assert j['stage']=='cancelled' and j.get('execution_task_id') is None
e=dict(ts=now.isoformat(),event='coordination_cancelled_before_execution',provedor='deepseek',request_id=r['request_id'],job_id=r['job_id'],desfecho=j['stage'],execution_task_id=None,provider_calls_observed=0,custo_usd='0',reason='Previous automatic review rejected dispatch authorization for this new package; preserved cancelled, no retry. Current operator asks distribution to Kimi/MiMo.')
save(HERE/'deepseek_orbit_cancellation.json',json.dumps(e,ensure_ascii=False,indent=2).encode())
r.update(status='cancelled',execution_task_id=None,cancellation_receipt='deepseek_orbit_cancellation.json')
raw=json.dumps(r,ensure_ascii=False,indent=2).encode();save(rp,raw)
save(BASE/'state/session_requests'/f'{r["request_id"]}.json',raw)
ledger=OUT/'LEDGER_016.jsonl'
save(ledger,ledger.read_bytes()+(json.dumps(e,ensure_ascii=False)+'\n').encode())
print(json.dumps(e,ensure_ascii=False))
