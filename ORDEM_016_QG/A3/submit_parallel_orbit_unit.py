from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
provider=sys.argv[1]
assert provider in ('mimo','kimi')
def save(p,raw):
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw and raw
    t.replace(p)
payload=json.loads((HERE/f'{provider}_parallel_orbit_submit.json').read_text(encoding='utf8'))
sys.path.insert(0,str(BASE))
from iald_orchestrator.runtime import Runtime
preview=Runtime(recover=False).preview(payload['prompt'],payload['execution_constraints'])
save(HERE/f'{provider}_parallel_orbit_pre_submit.json',json.dumps(preview,ensure_ascii=False,indent=2).encode())
assert preview.get('selected')==provider, 'ROTA_NAO_DISPONIVEL; no submission'
marker=HERE/f'{provider}_parallel_orbit_submission_started.json'
assert not marker.exists(), 'Existing attempt; recover same ID, do not repeat'
save(marker,json.dumps(dict(request_id=payload['request_id'],utc=stamp)).encode())
call=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(payload,ensure_ascii=False),capture_output=True,encoding='utf8',timeout=120)
assert call.returncode==0,call.stderr
result=json.loads(call.stdout)
save(HERE/f'{provider}_parallel_orbit_submission_result.json',json.dumps(result,ensure_ascii=False,indent=2).encode())
rp=HERE/f'{provider}_parallel_orbit_receipt.json'
receipt=json.loads(rp.read_text(encoding='utf8'))
receipt.update(job_id=result['id'],status=result['stage'],registered_at=result['created_at'])
raw=json.dumps(receipt,ensure_ascii=False,indent=2).encode()
save(rp,raw);save(BASE/'state/session_requests'/f'{payload["request_id"]}.json',raw)
event=dict(ts=result['created_at'],event='coordination_registered',alvo='A-3',ramo=payload['execution_constraints']['branch_id'],provedor=provider,request_id=payload['request_id'],job_id=result['id'],question_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),answer_sha256=None,provider_calls_observed=0,custo_usd=None,desfecho=result['stage'],execution_constraints=payload['execution_constraints'])
ledger=OUT/'LEDGER_016.jsonl'
save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
print(json.dumps(dict(provider=provider,request_id=payload['request_id'],job_id=result['id'],stage=result['stage']),ensure_ascii=False))
