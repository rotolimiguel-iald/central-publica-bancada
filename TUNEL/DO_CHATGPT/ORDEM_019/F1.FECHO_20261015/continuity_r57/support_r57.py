"""Immutable R56 evidence and access to the existing scientific mission."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
CORE = Path(r'C:\IALD\MEMORIA_IALD')
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
REFERENCE = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}
TASK = 'R4'

def new(path, value):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = value if isinstance(value, bytes) else (value.encode('utf-8') if isinstance(value, str) else
          (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.read_bytes() != raw:
        raise RuntimeError('write verification failed')
    tmp.rename(path)
    return path

def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def call(cli, request, label):
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    prefix = 'receipts/' + label + '_' + stamp
    new(prefix + '_REQUEST.json', request)
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CORE / cli)],
                       input=json.dumps(request, ensure_ascii=False), capture_output=True,
                       text=True, encoding='utf-8')
    try:
        result = json.loads(p.stdout)
    except ValueError:
        result = {'stdout': p.stdout}
    out = new(prefix + '_RESULT.json', {'exit_code': p.returncode, 'result': result, 'stderr': p.stderr})
    if p.returncode or result.get('ok') is False:
        raise RuntimeError(str(out))
    return result['result'], out

def project():
    return call('mission_cli.py', {'operation':'project', 'reference':str(REFERENCE),
                                  'max_chars':400000}, 'PROJECT')[0]

def action(operation, event_id, **extra):
    p = project()
    return call('mission_cli.py', dict(operation=operation, event_id=event_id, reference=str(REFERENCE),
                actor=ACTOR, expected_revision=p['receipt']['revision'],
                projection_sha256=p['projection_sha256'], **extra), operation.upper())

def preflight():
    p = project()
    task = next(t for t in p['projection']['active'] if t['id'] == TASK)
    return call('mission_cli.py', dict(operation='check', reference=str(REFERENCE), actor=ACTOR,
        task_id=TASK, lease_id=task['lease']['id'], expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256']), 'PREFLIGHT')

def transition(event_id, records, next_action):
    snap, _ = call('session_memory.py', {'operation':'get','reference':str(REFERENCE)}, 'GET')
    return call('session_memory.py', dict(operation='transition', reference=str(REFERENCE),
        actor=ACTOR, expected_revision=snap['revision'], event_id=event_id,
        changes={'records':records,'flow':{'phase':'miguel_reading_reuse', 'next_action':next_action}}), 'TRANSITION')
