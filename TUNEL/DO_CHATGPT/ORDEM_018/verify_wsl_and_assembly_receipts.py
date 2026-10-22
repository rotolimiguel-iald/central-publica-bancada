"""Read and seal existing receipts only; never launch or import candidates."""
import json
from pathlib import Path
from datetime import datetime, timezone
from audit_inputs import file_info, save_json

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'preregistros/conjunto_d/guard_wsl_corrected_transport_preparation'
REQUEST = '5b67deb6-fec2-43d6-af61-347f1a3e5b83'

def read(path):
    return json.loads(Path(path).read_bytes())

def verify_pin(entry, base=None):
    path = Path(entry.get('path', entry.get('relative_path', '')))
    if not path.is_absolute():
        path = base / path
    actual = file_info(path)
    assert all(actual[k] == entry[k] for k in ('bytes', 'sha256')), path
    return actual

def main():
    output = ROOT / 'RECIBO_ROOT_WSL_CORRIGIDO_PASS.json'
    review_output = ROOT / 'RECIBO_ROOT_REVISAO_FIVE_MODEL_ASSEMBLY.json'
    assert not output.exists() and not review_output.exists()
    manifest = read(PACKAGE / 'MANIFESTO_TRANSPORTE_CORRIGIDO.json')
    verified = [verify_pin(x, PACKAGE) for x in manifest['artifacts']]
    contract = read(PACKAGE / 'CONTRATO_WSL.json')
    verified += [verify_pin(x, PACKAGE) for x in contract['local_pins']]
    result = read(PACKAGE / 'RESULT.json')
    claim = read(PACKAGE / 'CLAIM.json')
    auth = read(PACKAGE / 'AUTORIZACAO_ROOT.json')
    assert auth['authorized'] is True and auth['review_accepted'] is True
    assert all(x['request_id'] == REQUEST for x in (manifest, contract, result, claim, auth))
    assert claim['authorization_sha256'] == file_info(PACKAGE / 'AUTORIZACAO_ROOT.json')['sha256']
    assert claim['contract_sha256'] == auth['contract_sha256'] == file_info(PACKAGE / 'CONTRATO_WSL.json')['sha256']
    assert auth['review_sha256'] == file_info(PACKAGE / 'REVISAO_ROOT.json')['sha256']
    assert result['status'] == 'PASS_WSL_STDLIB_INTEGRATION_ONCE'
    assert result['primary_returncode'] == result['cleanup_returncode'] == 0
    assert result['error'] is None and result['retry_allowed'] is False
    assert result['scientific_calls'] == 0 and result['D_read'] is False
    assert result['pid'] == claim['pid'] and result['nonce'] == claim['nonce']
    nonce = result['nonce']
    linux, cleanup = result['linux'], result['cleanup']
    child = linux['child']
    assert linux == read(PACKAGE / 'RUN/LINUX_RESULT.json')
    assert cleanup == read(PACKAGE / 'RUN/CLEANUP_RESULT.json')
    assert child == read(PACKAGE / 'RUN/CASE/CASE_RESULT.json')
    for stream, receipt in [('primary', 'LINUX_RESULT.json'), ('cleanup', 'CLEANUP_RESULT.json')]:
        assert (PACKAGE / f'RUN/{stream}_stdout.bin').read_bytes() == (PACKAGE / f'RUN/{receipt}').read_bytes()
        assert (PACKAGE / f'RUN/{stream}_stderr.bin').read_bytes() == b''
        capture = result['capture_state'][stream]
        assert capture['all_readers_terminated'] and not capture['overflow']
        assert all(capture['eof'].values()) and all(v is None for v in capture['errors'].values())
        assert capture['retained_bytes']['stdout'] == (PACKAGE / f'RUN/{stream}_stdout.bin').stat().st_size
        assert capture['retained_bytes']['stderr'] == 0
    assert (PACKAGE / 'RUN/stdout.bin').read_bytes() == (PACKAGE / 'RUN/CASE/CASE_RESULT.json').read_bytes()
    assert (PACKAGE / 'RUN/stderr.bin').read_bytes() == b''
    for role, node, label in [('--supervisor', linux, 'SUPERVISOR'), ('--child', child, 'CHILD'), ('--cleanup', cleanup, 'CLEANUP')]:
        argv = read(PACKAGE / f'RUN/ARGV_{label}.json')
        assert node['argv_transport'] == argv
        assert argv['request_id'] == node['request_id'] == REQUEST and argv['nonce'] == node['nonce'] == nonce
        assert argv['role'] == role
        expected = [contract['runtime']['executable'], *contract['runtime']['flags'], contract['argv_transport']['linux_root'] + '/' + contract['argv_transport']['scripts'][role], role, REQUEST, nonce]
        assert len(expected) == 10
        assert argv['expected_process_argv'] == argv['received_process_argv'] == argv['process']['argv'] == expected
        assert argv['expected_script_argv'] == argv['received_script_argv'] == expected[6:]
        assert argv['script_argv_matches'] and argv['process_argv_matches']
        if 'process' in node:
            assert node['process'] == argv['process']
    assert child['process']['ppid'] == child['parent_pid'] == linux['process']['pid']
    assert child['process']['boot_id'] == linux['process']['boot_id'] == cleanup['argv_transport']['process']['boot_id']
    assert linux['child_returncode'] == 0 and linux['child_reaped'] is True
    assert child['status'] == 'PASS_EXPECTED_LATCHED' and child['error'] is None
    assert child['callbacks'] == child['new_children'] == child['scientific_calls'] == child['scientific_imports'] == 0
    assert child['next_blocked'] and child['final_blocked'] and child['import_returned_normally']
    assert child['unexpected_operations'] == []
    audit = child['audit_snapshot']
    journal = PACKAGE / 'RUN/CASE/journal.jsonl'
    jpin = file_info(journal)
    assert all(jpin[k] == child['journal'][k] for k in ('bytes', 'sha256'))
    entries = [json.loads(line) for line in journal.read_bytes().splitlines()]
    assert entries == audit['events'] == [audit['first_event']]
    assert audit['denial_count'] == 1 and audit['first_event']['sequence'] == 1
    assert audit['first_event']['reason'] == 'EXPECTED_CACHE_PROBE'
    assert audit['first_event']['likelihood_calls_at_event'] == audit['first_event']['native_attempts_completed_at_event'] == 0
    assert audit['latched'] and audit['journal_error'] is None and audit['interrupted_exceptions'] == []
    assert child['profile_real_os_calls'] == {k: {'c_call': 1, 'c_return': 1, 'c_exception': 0} for k in ('write', 'fsync')}
    assert cleanup['status'] == 'NO_LIVE_CONTROLLED_PROCESSES_VERIFIED' and cleanup['error'] is None
    assert cleanup['launch_fence_persistent'] and cleanup['stopped'] == []
    assert cleanup['control_runs'] == cleanup['scientific_calls'] == 0
    assert (PACKAGE / 'RUN/STOP.json').is_file()
    external = {'tool': 'exec_command', 'chunk_id': 'c2d091', 'exit_code': 0, 'wall_time_seconds': 0.8604963,
                'source': 'Actual tool return retained by coordinator; displayed output truncated, not represented as full stdout.',
                'scope': 'Process exit and elapsed time observed externally; nested physical receipts and captured streams independently checked here.'}
    assert external['wall_time_seconds'] < contract['limits']['nominal_total_s']
    evidence = [file_info(p) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and (p.parent.name == 'RUN' or 'RUN' in p.parts or p.name in ['RESULT.json','CLAIM.json','AUTORIZACAO_ROOT.json','REVISAO_ROOT.json','CONTRATO_WSL.json','MANIFESTO_TRANSPORTE_CORRIGIDO.json'])]
    save_json(output, {'at': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_WSL_STDLIB_INTEGRATION_ONCE_VERIFIED_BY_ROOT',
        'request_id': REQUEST, 'execution_consumed_once': True, 'repeat_allowed': False, 'external_execution': external,
        'verified_preparation_pins': verified, 'evidence': evidence, 'observed_result': result,
        'limitations': contract['acceptance']['not_proved'], 'orphan_absence_scope': contract['identity_and_claims']['absence_scope'],
        'new_execution_or_WSL_invocations_in_this_verification': 0, 'observed_data_read': False, 'scientific_execution': False})
    review_dir = ROOT / 'proveniencia/revisao_five_model_assembly'
    review_manifest = read(review_dir / 'MANIFESTO_REVISAO.json')
    review_pins = [verify_pin(e, review_dir) for e in review_manifest['files']]
    assembly_dir = ROOT / 'f9_five_model_assembly_preparation'
    assembly_manifest = read(assembly_dir / 'MANIFESTO_ENTREGA.json')
    assembly_pins = [verify_pin(e, assembly_dir) for e in assembly_manifest['files']]
    save_json(review_output, {'at': datetime.now(timezone.utc).isoformat(), 'status': 'LIMITED_STATIC_ACCEPTANCE_NOT_EXECUTION',
        'request_id': '8e017d91-f3bb-4ec6-9236-5b2c327d1b98', 'map_sequence': 548,
        'review_manifest': file_info(review_dir / 'MANIFESTO_REVISAO.json'), 'review_pins': review_pins,
        'assembly_manifest': file_info(assembly_dir / 'MANIFESTO_ENTREGA.json'), 'assembly_pins': assembly_pins,
        'review_read_completely': True, 'integration_request': file_info(ROOT / 'F9_ENGINE_ASSEMBLY_INTEGRATION_REQUEST.json'),
        'integration_obligations': ['z=0 plus seven BAO redshifts', 'Consumer Ty and TCT^T', 'Admission runtime and execution evidence checked outside passive assembly', 'MM candidate remains conditional and unratified'],
        'new_authorization': False, 'scientific_execution': False, 'observed_centers_read': False})
    print(json.dumps({'wsl_receipt': file_info(output), 'assembly_review_receipt': file_info(review_output), 'checks_passed': True}, ensure_ascii=False))

if __name__ == '__main__':
    main()
