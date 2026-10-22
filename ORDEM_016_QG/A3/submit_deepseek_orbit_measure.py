from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def write(p,data):
    if p.exists():
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp)
    with tmp.open('xb') as f:f.write(data)
    assert tmp.read_bytes()==data and data
    tmp.replace(p);assert p.read_bytes()==data
payload=json.loads((HERE/'deepseek_orbit_submit.json').read_text(encoding='utf8'))
marker=HERE/'deepseek_orbit_submission_started.json'
assert not marker.exists(), 'Recover existing request; do not repeat an uncertain unit.'
write(marker,json.dumps(dict(request_id=payload['request_id'],utc=stamp)).encode())
call=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],
                    input=json.dumps(payload,ensure_ascii=False),capture_output=True,encoding='utf8',timeout=120)
assert call.returncode==0,call.stderr
result=json.loads(call.stdout)
write(HERE/'deepseek_orbit_submission_result.json',json.dumps(result,ensure_ascii=False,indent=2).encode())
receipt=json.loads((HERE/'deepseek_orbit_receipt.json').read_text(encoding='utf8'))
receipt.update(job_id=result['id'],status=result['stage'],registered_at=result['created_at'])
write(HERE/'deepseek_orbit_receipt.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
write(BASE/'state/session_requests'/f'{payload["request_id"]}.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
ledger=OUT/'LEDGER_016.jsonl'
event=dict(ts=result['created_at'],event='coordination_registered',alvo='A-3',ramo='A-3.4',
           provedor='deepseek',request_id=payload['request_id'],job_id=result['id'],
           question_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),answer_sha256=None,
           provider_calls_observed=0,custo_usd=None,desfecho=result['stage'],execution_constraints=payload['execution_constraints'])
write(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
print(json.dumps(dict(request_id=payload['request_id'],job_id=result['id'],stage=result['stage']),ensure_ascii=False))
