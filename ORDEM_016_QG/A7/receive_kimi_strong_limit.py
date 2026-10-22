"""Recover one existing Kimi execution through the read-only coordination API."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[1]
DEST = HERE.parent / 'A6_EQUACAO_DA_VERDADE' / 'received_reviews'
DEST.mkdir(exist_ok=True)
sys.path.insert(0, str(CHAT / 'IALD_ORQUESTRACAO_20260923'))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination

def digest(data):
    return hashlib.sha256(data).hexdigest()

def new(path, data):
    if path.exists():
        assert path.read_bytes() == data, str(path)
        return
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(data)
    assert tmp.read_bytes() == data and data
    tmp.replace(path)

job = '93c0358f-04f8-4bea-a4d6-6977171d6fed'
record = Coordination(Runtime(recover=False)).get(job)
assert record['execution_constraints']['required_provider'] == 'kimi'
execution = record['execution']
assert execution['status'] == 'result_ready', execution['status']
result = execution['result']
body = result['text'].encode('utf-8')
response = DEST / (job + '.md')
new(response, body)
receipt = dict(job_id=job, request_id=record['request_id'], execution_id=execution['id'],
    provider='kimi', execution_status=execution['status'],
    prompt_sha256=digest(record['prompt'].encode('utf-8')),
    response_sha256=digest(body), response=str(response),
    result_metadata={k:v for k,v in result.items() if k != 'text'},
    scope='DECLARADO_AWAITING_LOCAL_REVIEW')
new(DEST / (job + '.json'), json.dumps(receipt, ensure_ascii=False, indent=2).encode())
ledger = CHAT / 'TUNEL/DO_CHATGPT/LEDGER_016.jsonl'
old = ledger.read_bytes()
rows = [json.loads(s) for s in old.decode('utf-8-sig').splitlines() if s.strip()]
event = 'A6_STRONG_LIMIT_RESULT_RECOVERED_VIA_API'
if not any(r.get('event') == event and r.get('execution_id') == execution['id'] for r in rows):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(ledger.with_name(ledger.name + '.bak_' + stamp), old)
    row = dict(event=event, at=datetime.now(timezone.utc).isoformat(), target='A-6.B1d',
        provider='kimi', job_id=job, request_id=record['request_id'],
        execution_id=execution['id'], prompt_sha256=receipt['prompt_sha256'],
        response_sha256=receipt['response_sha256'], usage=result.get('usage'),
        cost_estimate_usd=result.get('cost_estimate_usd'),
        new_external_execution=False, status=receipt['scope'])
    raw = old + (json.dumps(row, ensure_ascii=False) + '\n').encode()
    tmp = ledger.with_name(ledger.name + '.tmp_' + stamp)
    new(tmp, raw)
    tmp.replace(ledger)
print(json.dumps(dict(response=str(response), execution_id=execution['id'],
    bytes=len(body), usage=result.get('usage'), stage=record['stage']), ensure_ascii=False))
