"""Register prepared work in the existing queue; never execute provider transitions."""
from pathlib import Path
from datetime import datetime, timezone
import json, subprocess, sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]/'IALD_ORQUESTRACAO_20260923'

def save(path, data):
    assert not path.exists(), path
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    tmp = path.with_name(path.name+'.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    tmp.rename(path)

for provider in ('kimi', 'mimo'):
    path = HERE/f'reuse_{provider}_submit_v2.json'
    payload = json.loads(path.read_text(encoding='utf-8'))
    result_path = HERE/f'reuse_{provider}_submission_result.json'
    assert not result_path.exists(), 'Inspect existing result; do not duplicate submission.'
    marker = HERE/f'reuse_{provider}_submission_started.json'
    assert not marker.exists(), 'Uncertain submission: recover the same request ID first.'
    save(marker, dict(request_id=payload['request_id'], utc=datetime.now(timezone.utc).isoformat()))
    completed = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(BASE/'transport_cli.py')],
                               input=json.dumps(payload,ensure_ascii=False), capture_output=True,
                               encoding='utf-8', timeout=120)
    if completed.returncode:
        save(result_path, dict(returncode=completed.returncode, stdout=completed.stdout, stderr=completed.stderr))
        raise RuntimeError(f'{provider}: submission failed; inspect receipt without new UUID.')
    result = json.loads(completed.stdout)
    save(result_path, result)
    print(json.dumps(dict(provider=provider, request_id=payload['request_id'],
                          response_keys=list(result), id=result.get('id'), job_id=result.get('job_id'),
                          stage=result.get('stage'), status=result.get('status')),ensure_ascii=False),flush=True)
