"""Fresh mission sync and one CAS acceptance after real independent R6 review."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

OUT = Path(__file__).resolve().parent
REF = r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json'
CLI = [r'C:\Python314\python.exe', '-B', '-X', 'utf8', r'C:\IALD\MEMORIA_IALD\mission_cli.py']

def save(name, obj):
    path = OUT / name
    assert not path.exists(), path
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, path)

def call(request):
    proc = subprocess.run(CLI, input=json.dumps(request, ensure_ascii=False).encode('utf-8'),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = json.loads(proc.stdout)
    return result

save('R6_ACCEPT_PRIOR_REFUSALS_R1.json', {
    'first': {'ok': False, 'error': 'IntegrityError', 'message': 'Memory transition failed closed'},
    'first_after_read': {'revision': 29, 'R6': 'review_pending'},
    'second': {'ok': False, 'error': 'MissionError', 'message': 'stale_revision_refresh_required'},
    'original_request': str(OUT / 'R6_ACCEPT_REQUEST_R1.json'),
    'interpretation': 'First error is the store sqlite3.Error wrapper; specific SQLite cause was not emitted. Second refusal explicitly requires fresh revision. No successful acceptance was reported.'
})
projection = call({'operation': 'project', 'reference': REF, 'max_chars': 60000})
save('R6_ACCEPT_PROJECT_R2.json', projection)
assert projection.get('ok'), projection
result = projection['result']
task = next(t for t in result['projection']['active'] if t['id'] == 'R6')
assert task['status'] == 'review_pending' and task['submitted_by'] == 'codex-gerente-tgl'
report_path = OUT / 'R6_REQUIREMENT_REVIEW_R1.json'
report = json.loads(report_path.read_bytes())
assert report['reviewer']['id'] == 'codex-fock-r6-review'
assert report['verdict'] == 'PASS_WITH_SCOPE' and not report['blocking_findings']
reviewed = {x['path']: x['sha256'] for x in [report['reviewed_delivery'], report['reviewed_source']]}
for evidence in task['evidence']:
    assert reviewed[evidence['path']] == evidence['sha256']
    assert hashlib.sha256(Path(evidence['path']).read_bytes()).hexdigest() == evidence['sha256']
assert not any(r.get('meta', {}).get('mission_event_id') == 'R6-physical-fock-r2-independent-accept-r1'
               for r in result['projection'].get('current_records', []))
request = json.loads((OUT / 'R6_ACCEPT_REQUEST_R1.json').read_bytes())
request['expected_revision'] = result['receipt']['revision']
request['projection_sha256'] = result['projection_sha256']
assert request['review_evidence'][0]['sha256'] == hashlib.sha256(report_path.read_bytes()).hexdigest()
save('R6_ACCEPT_REQUEST_R2.json', request)
accepted = call(request)
save('R6_ACCEPT_RECEIPT_R2.json', accepted)
assert accepted.get('ok'), accepted
after = call({'operation': 'project', 'reference': REF, 'max_chars': 60000})
save('R6_AFTER_ACCEPT_PROJECT_R2.json', after)
assert after.get('ok'), after
settled = next(t for t in after['result']['projection']['settled'] if t['id'] == 'R6')
assert settled['status'] == 'satisfied' and settled['reviewed_by'] == 'codex-fock-r6-review'
print(json.dumps({'ok': True, 'revision': after['result']['receipt']['revision'],
                  'R6': settled['status'], 'reviewer': settled['reviewed_by'],
                  'tetelestai': after['result']['projection']['tetelestai']}, ensure_ascii=False))
