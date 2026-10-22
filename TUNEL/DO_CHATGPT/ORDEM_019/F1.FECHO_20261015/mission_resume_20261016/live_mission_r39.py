"""Fresh mission reads and compact receipts; never replay a cached read as live."""
from pathlib import Path
import datetime
import json
import os
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
CORE = Path(r'C:\IALD\MEMORIA_IALD')
REFERENCE = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}


def save_new(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.stat().st_size != len(raw):
        raise RuntimeError('Receipt size mismatch')
    # On Windows rename refuses an existing destination. No original is replaced.
    os.rename(temporary, path)


def call(cli, payload, name):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    prefix = ROOT / ('LIVE_' + name + '_' + stamp + '_' + uuid.uuid4().hex[:8])
    save_new(prefix.with_name(prefix.name + '_REQUEST.json'), payload)
    process = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CORE / cli)],
                             input=json.dumps(payload, ensure_ascii=False), text=True,
                             encoding='utf-8', capture_output=True)
    try:
        response = json.loads(process.stdout)
    except json.JSONDecodeError:
        response = {'ok': False, 'stdout': process.stdout, 'stderr': process.stderr}
    receipt = prefix.with_name(prefix.name + '_RECEIPT.json')
    save_new(receipt, response)
    if process.returncode or not response.get('ok'):
        raise RuntimeError(f'Mission call refused; receipt: {receipt}')
    return response['result'], receipt


def project():
    return call('mission_cli.py', {'operation': 'project', 'reference': str(REFERENCE),
                                  'max_chars': 100000}, 'PROJECT')


def main():
    operation = sys.argv[1] if len(sys.argv) > 1 else 'project'
    if operation not in {'project', 'check', 'handoff'}:
        raise ValueError('Only project, check and handoff are allowed')
    current, receipt = project()
    projection = current['projection']
    output = {'revision': current['receipt']['revision'], 'project_receipt': str(receipt),
              'settled': [item['id'] for item in projection['settled']],
              'active': [{key: item[key] for key in ('id', 'status', 'ready')}
                         for item in projection['active']],
              'unresolved_handles': [{key: item.get(key) for key in ('id', 'status')}
                                     for item in projection['unresolved_handles']]}
    if operation != 'project':
        task_id = sys.argv[2]
        task = next(item for item in projection['active'] if item['id'] == task_id)
        if task['lease'] is None or task['lease']['owner'] != ACTOR['id']:
            raise RuntimeError('No current own lease')
        payload = {'operation': 'check', 'reference': str(REFERENCE), 'actor': ACTOR,
                   'task_id': task_id, 'lease_id': task['lease']['id'],
                   'expected_revision': current['receipt']['revision'],
                   'projection_sha256': current['projection_sha256']}
        _, checked = call('mission_cli.py', payload, 'CHECK_' + task_id)
        output.update(task_id=task_id, preflight_receipt=str(checked))
        if operation == 'handoff':
            payload.update(operation='handoff', max_chars=100000)
            _, handed = call('mission_cli.py', payload, 'HANDOFF_' + task_id)
            output['handoff_receipt'] = str(handed)
    print(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    main()
