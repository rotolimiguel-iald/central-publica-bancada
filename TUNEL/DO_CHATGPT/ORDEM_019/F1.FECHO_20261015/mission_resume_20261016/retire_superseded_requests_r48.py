"""Retire two never-dispatched requests superseded by accepted local R6 evidence.

The normal get/act path currently assembles an incompatible canonical generation.
Use the existing transactional transition, solely for cancellation from the
confirmed initial state. No payload, constraint, generation or provider changes.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path
import live_mission_r39 as live

OUT = Path(__file__).resolve().parents[1]
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
JOBS = {
    '1e2c2f25-f6bf-4451-aad2-052ba9a1897d': 'fock_antiunitary_second_quantization_r3',
    '67df5266-7d17-4f33-a003-da2494c9bdc2': 'fock_exponential_vectors_totality_r3',
}


def pin(path):
    return {'path': str(path), 'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest()}


def main():
    result_path = OUT / 'QUEUE_RETIREMENT_R48.json'
    if result_path.exists():
        raise RuntimeError('Immutable receipt exists; recover rather than repeat.')
    current, projected = live.project()
    accepted = next(x for x in current['projection']['settled'] if x['id'] == 'R6')
    assert accepted['status'] == 'satisfied' and accepted['reviewed_by'] != live.ACTOR['id']
    for evidence in accepted['evidence'] + accepted['review_evidence']:
        assert pin(evidence['path'])['sha256'] == evidence['sha256']
    sys.path.insert(0, str(BASE))
    from iald_orchestrator.coordination import Coordination
    coordinator = Coordination()
    receipts = []
    for job_id, handle_id in JOBS.items():
        with coordinator.runtime.db() as db:
            before = dict(db.execute('SELECT * FROM coordination_jobs WHERE id=?', (job_id,)).fetchone())
            events = list(db.execute('SELECT id FROM coordination_events WHERE job_id=?', (job_id,)))
        assert before['stage'] == 'awaiting_dispatch' and before['version'] == 0
        assert before['execution_task_id'] is None and before['thread_id'] is None and not events
        constraints = before['execution_constraints']
        payload_digest = hashlib.sha256(before['prompt'].encode('utf-8')).hexdigest()
        after = coordinator._change(job_id, {'awaiting_dispatch'}, 'cancelled', 'cancel',
            error='Retirado sem envio: objetivo atendido localmente por R6 aceito, evidência pinada em QUEUE_RETIREMENT_R48.json; sem repetição.')
        assert after['stage'] == 'cancelled' and after['execution_task_id'] is None
        with coordinator.runtime.db() as db:
            row = dict(db.execute('SELECT * FROM coordination_jobs WHERE id=?', (job_id,)).fetchone())
        assert row['execution_constraints'] == constraints
        assert hashlib.sha256(row['prompt'].encode('utf-8')).hexdigest() == payload_digest
        receipt = OUT / ('QUEUE_RETIREMENT_R48_' + job_id + '.json')
        live.save_new(receipt, {'job_id': job_id, 'handle_id': handle_id,
            'before': {k: before[k] for k in ('stage', 'version', 'request_id', 'execution_task_id', 'thread_id')},
            'after': {k: row[k] for k in ('stage', 'version', 'request_id', 'execution_task_id', 'thread_id')},
            'prompt_sha256': payload_digest, 'constraints_preserved': True,
            'providers_called': False, 'accepted_evidence': accepted['evidence'] + accepted['review_evidence']})
        receipts.append(pin(receipt))
    live.save_new(result_path, {'statute': 'REAL', 'reason': 'Accepted local R6 supersedes never-dispatched requests',
        'project_receipt': pin(projected), 'jobs': receipts, 'providers_called': False,
        'production_science_modified': False, 'gate_moved': False})
    state, _ = live.call('session_memory.py', {'operation': 'get', 'reference': str(live.REFERENCE)}, 'R48_QUEUE_FINAL_GET')
    handles = copy.deepcopy(state['p']['handles'])
    for h in handles:
        if h['id'] in JOBS.values():
            assert h['status'] == 'awaiting_dispatch'
            h.update(status='cancelled', receipt=pin(result_path), no_repeat=True,
                     reason='Superseded by accepted local R6, never dispatched; queue cancellation verified.')
    result, receipt = live.call('session_memory.py', {'operation': 'transition', 'reference': str(live.REFERENCE),
        'actor': live.ACTOR, 'expected_revision': state['revision'], 'event_id': 'r48-superseded-requests-retired',
        'changes': {'flow': {'handles': handles}}}, 'R48_QUEUE_RETIRED')
    print(json.dumps({'result': pin(result_path), 'revision': result['revision'], 'receipt': str(receipt)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
