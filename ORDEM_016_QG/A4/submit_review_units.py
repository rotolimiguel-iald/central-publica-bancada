from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
DEST = HERE / 'orchestration_reviews_20260924'
BASE = HERE.parents[1] / 'IALD_ORQUESTRACAO_20260923'
OUT = HERE.parents[1] / 'TUNEL/DO_CHATGPT'

def save(path, raw):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as stream:
            stream.write(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert raw and temp.read_bytes() == raw
    temp.replace(path)

def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')

registered = []
for unit in json.loads((DEST / 'prepared_units.json').read_bytes()):
    slug = unit['slug']
    payload = json.loads((DEST / (slug + '_submit.json')).read_bytes())
    preview = json.loads((DEST / (slug + '_preview.json')).read_bytes())
    assert preview['selected'] == unit['provider']
    marker = DEST / (slug + '_submission_started.json')
    raw_path = DEST / (slug + '_submission_raw.json')
    if marker.exists():
        if not raw_path.exists():
            raise RuntimeError('Uncertain registration: inspect before any retry')
        raw_result = json.loads(raw_path.read_bytes())
        assert raw_result['rc'] == 0, 'No automatic retry of failed registration'
    else:
        save(marker, encode(dict(request_id=payload['request_id'],
                                at=datetime.now(timezone.utc).isoformat())))
        proc = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(BASE/'transport_cli.py')],
            input=json.dumps(payload, ensure_ascii=False), text=True, encoding='utf-8',
            capture_output=True, timeout=120)
        raw_result = dict(rc=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
        save(raw_path, encode(raw_result))
        assert proc.returncode == 0, 'Registration failed; inspect retained output'
    result = json.loads(raw_result['stdout'])
    receipt_path = DEST / (slug + '_receipt.json')
    receipt = json.loads(receipt_path.read_bytes())
    receipt.update(job_id=result['id'], status=result['stage'], registered_at=result['created_at'])
    save(receipt_path, encode(receipt))
    ledger = OUT / 'LEDGER_016.jsonl'
    previous = ledger.read_bytes()
    events = [json.loads(line) for line in previous.decode('utf-8-sig').splitlines() if line.strip()]
    if not any(event.get('job_id') == result['id'] for event in events):
        event = dict(ts=result['created_at'], event='coordination_registered', alvo='A-4',
            ramo=unit['branch'], lemma_id=slug, provedor=unit['provider'],
            request_id=payload['request_id'], job_id=result['id'],
            question_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
            answer_sha256=None, provider_calls_observed=0, custo_usd=None,
            desfecho=result['stage'])
        save(ledger, previous + (json.dumps(event, ensure_ascii=False)+'\n').encode('utf-8'))
    registered.append(receipt)
save(DEST / 'registered_units.json', encode(registered))
print(json.dumps([{key: row[key] for key in ('provider','branch','request_id','job_id','status')}
                  for row in registered], ensure_ascii=False))
