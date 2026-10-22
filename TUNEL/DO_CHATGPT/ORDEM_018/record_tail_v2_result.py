"""Validate the already consumed synthetic unit; never execute its code."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from audit_inputs import file_info, save_json

ROOT = Path(__file__).resolve().parent
P = ROOT / 'f9_tail_envelope_implementation_v2'

def read(name):
    return json.loads((P / name).read_bytes())

def main():
    output = ROOT / 'RECIBO_ROOT_CONTROLES_TAIL_V2_PASS.json'
    assert not output.exists()
    tool = read('EXEC_RESULT_OFFICIAL_TOOL.json')
    assert tool['exit_code'] == 0 and not tool.get('session_id')
    emitted = json.loads(tool['output'])
    receipt = read('TERMINAL_RECEIPT.json')
    assert emitted['provisional_receipt_sha256'] == file_info(P / 'TERMINAL_RECEIPT.json')['sha256']
    assert emitted['controls_status'] == receipt['controls_status'] == 'PASS'
    assert emitted['status'] == receipt['status'] == 'PENDING_FINAL_DEADLINE_CHECK'
    assert not (P / 'FINALIZATION_FAILURE.json').exists()
    claim, process, contract = read('CLAIM.json'), read('RUN/PROCESS_IDENTITY.json'), read('CONTROL_CONTRACT.json')
    inputs, auth, worker = read('EXECUTION_INPUTS.json'), read('AUTORIZACAO_ROOT.json'), receipt['worker']
    request = contract['request_id']
    assert all(x['request_id'] == request for x in (emitted, receipt, claim, process, inputs, auth, worker))
    assert receipt['authorization_sha256'] == claim['authorization_sha256'] == file_info(P / 'AUTORIZACAO_ROOT.json')['sha256']
    assert receipt['contract_sha256'] == claim['contract_sha256'] == auth['contract_sha256'] == file_info(P / 'CONTROL_CONTRACT.json')['sha256']
    assert receipt['execution_inputs_sha256'] == claim['inputs_sha256'] == auth['execution_inputs_sha256'] == file_info(P / 'EXECUTION_INPUTS.json')['sha256']
    assert receipt['supervisor_pid'] == worker['supervisor_pid'] == process['supervisor_pid'] == claim['supervisor_pid']
    assert receipt['worker_pid'] == worker['worker_pid'] == process['worker_pid']
    assert receipt['worker_returncode'] == 0 and worker['error'] is None
    assert process['argv'][process['argv'].index('--claim-token') + 1] == claim['claim_token']
    assert process['argv'][process['argv'].index('--request-id') + 1] == request
    assert process['execution_started_monotonic'] == receipt['execution_started_monotonic']
    assert abs(process['total_deadline_monotonic'] - process['execution_started_monotonic'] - 30) < 1e-8
    expected = contract['primary_function_order'] + contract['negative_function_order']
    assert [r['id'] for r in worker['results']] == expected
    assert len(expected) == 17 and all(r['status'] == 'PASS' for r in worker['results'])
    assert worker['audit_denied'] == [] and worker['observed_data'] is False and worker['physical_certification'] is False
    assert all(worker[k] == 0 for k in ('remote_calls', 'MC', 'CAMB'))
    assert receipt['stderr_excerpt'] == '' and receipt['stderr_sha256'] == hashlib.sha256(b'').hexdigest()
    assert 0 < emitted['observed_wall_through_persistence_seconds'] < 30
    verified = []
    for e in inputs['pins']:
        a = file_info(e['path'])
        assert all(a[k] == e[k] for k in ('bytes', 'sha256')), a['path']
        verified.append(a)
    evidence = [file_info(P / n) for n in ('EXEC_RESULT_OFFICIAL_TOOL.json', 'TERMINAL_RECEIPT.json', 'CLAIM.json', 'RUN/PROCESS_IDENTITY.json', 'AUTORIZACAO_ROOT.json', 'REVISAO_ROOT.json', 'CONTROL_CONTRACT.json', 'EXECUTION_INPUTS.json')]
    value = {
        'at': datetime.now(timezone.utc).isoformat(), 'request_id': request,
        'status': 'EIGHT_PRIMARY_AND_NINE_NEGATIVE_SYNTHETIC_GROUPS_PASSED_ONCE',
        'parent_exit_code_observed_by_exec_tool': tool['exit_code'], 'exec_command_wall_s': tool['wall_time_seconds'],
        'wall_through_terminal_persistence_s': emitted['observed_wall_through_persistence_seconds'],
        'worker_controls_wall_s': worker['wall_s'], 'nominal_total_s': 30,
        'supervisor_pid': receipt['supervisor_pid'], 'worker_pid': receipt['worker_pid'],
        'groups': [{'id': r['id'], 'status': r['status']} for r in worker['results']],
        'physical_certification': False, 'observed_data': False, 'remote_calls': 0,
        'scope': 'Fixed synthetic arithmetic, semantics, whole-family binding and finalization doubles; not physical F9 certificates, observed verdict, global optimization, or OS hard deadline.',
        'limitations': ['Output caps are post-collection acceptance caps.', 'Reported finalization duration precedes final stdout completion; external exit0 proves the pinned post-flush deadline check returned successfully.', 'No preserved raw worker stream file: stdout digest belongs to supervisor receipt; worker records were inspected there.'],
        'inputs_revalidated': verified, 'evidence': evidence, 'automatic_retry': False,
    }
    save_json(output, value)
    print(json.dumps({'receipt': file_info(output), 'groups': len(expected), 'inputs_revalidated': len(verified)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
