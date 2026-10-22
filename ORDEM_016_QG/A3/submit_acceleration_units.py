from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys

HERE = Path(__file__).resolve().parent
DEST = HERE / 'acceleration_20260924'
BASE = HERE.parents[1] / 'IALD_ORQUESTRACAO_20260923'
OUT = HERE.parents[1] / 'TUNEL/DO_CHATGPT'
stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')

def save(path, raw):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        old = path.read_bytes()
        with path.with_name(path.name + '.bak_' + stamp).open('xb') as f: f.write(old)
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as f: f.write(raw)
    assert temp.read_bytes() == raw and raw
    temp.replace(path)

results = []
for unit in json.loads((DEST / 'prepared_units.json').read_text(encoding='utf-8')):
    slug = unit['slug']
    payload = json.loads((DEST / (slug + '_submit.json')).read_text(encoding='utf-8'))
    preview = json.loads((DEST / (slug + '_preview.json')).read_text(encoding='utf-8'))
    assert preview['selected'] == unit['provider']
    marker = DEST / (slug + '_submission_started.json')
    if marker.exists():
        saved = json.loads((DEST / (slug + '_submission_raw.json')).read_text(encoding='utf-8'))
        assert saved['rc'] == 0, 'Uncertain submission; no automatic retry'
        result = json.loads(saved['stdout'])
    else:
        save(marker, json.dumps({'request_id':payload['request_id'], 'utc':stamp}).encode())
        call = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(BASE / 'transport_cli.py')],
            input=json.dumps(payload, ensure_ascii=False), text=True, encoding='utf-8', capture_output=True, timeout=120)
        save(DEST / (slug + '_submission_raw.json'), json.dumps({'rc':call.returncode, 'stdout':call.stdout,'stderr':call.stderr}, ensure_ascii=False).encode())
        assert call.returncode == 0, 'Submission failed; inspect saved receipt'
        result = json.loads(call.stdout)
    receipt_path = DEST / (slug + '_receipt.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update(job_id=result['id'], status=result['stage'], registered_at=result['created_at'])
    save(receipt_path, json.dumps(receipt, ensure_ascii=False, indent=2).encode())
    event = dict(ts=result['created_at'], event='coordination_registered', alvo='A-3',
        ramo=unit['slug'], provedor=unit['provider'], request_id=payload['request_id'],
        job_id=result['id'], question_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
        answer_sha256=None, provider_calls_observed=0, custo_usd=None, desfecho=result['stage'])
    ledger = OUT / 'LEDGER_016.jsonl'
    previous = ledger.read_bytes()
    if not any(json.loads(line).get('job_id') == result['id'] for line in previous.decode('utf-8').splitlines() if line.strip()):
        save(ledger, previous + (json.dumps(event, ensure_ascii=False)+'\n').encode())
    results.append(receipt)
save(DEST / 'registered_units.json', json.dumps(results, ensure_ascii=False, indent=2).encode())
print(json.dumps([{k:r[k] for k in ('provider','branch','request_id','job_id','status')} for r in results], ensure_ascii=False))
