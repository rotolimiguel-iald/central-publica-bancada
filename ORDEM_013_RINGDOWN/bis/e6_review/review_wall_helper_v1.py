"""Finite wall-adapter probes on AST-selected functions and dummy metadata."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import copy
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'e3_wall_stages/wall_stage_adapter.py'
FIXTURE = HERE / 'wall_helper_fixture_001'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p, raw):
    if not isinstance(raw, bytes):
        raw = (json.dumps(raw, indent=2) + '\n').encode()
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_name(p.name + '.pending')
    with temp.open('xb') as f:
        f.write(raw)
    if temp.read_bytes() != raw:
        raise ValueError('Fixture write mismatch')
    os.link(temp, p)
    temp.unlink()
    return {'path': p.relative_to(FIXTURE).as_posix(), 'sha256': sha(p)}


def main():
    if FIXTURE.exists():
        raise ValueError('Do not overwrite fixture evidence')
    raw = SOURCE.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    write(FIXTURE / 'wall_stage_adapter_snapshot.py', raw)
    tree = ast.parse(raw)
    funcs = {'require', 'metadata_bytes', 'sha', 'load', 'pin', 'checked', 'utc', 'pointer', 'reviewed_predecessor', 'rows_and_bindings'}
    constants = {'LIMIT', 'ROUTES', 'GROUPS', 'METRICS', 'GATES', 'FLAGS'}
    nodes = [x for x in tree.body if isinstance(x, (ast.Import, ast.ImportFrom))
             or isinstance(x, ast.FunctionDef) and x.name in funcs
             or isinstance(x, ast.Assign) and all(isinstance(t, ast.Name) and t.id in constants for t in x.targets)]
    n = {'__name__': 'independent_wall_functions', '__file__': str(FIXTURE / 'wall_stage_adapter_snapshot.py')}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), 'exec'), n)
    n.update(ROOT=FIXTURE, HERE=FIXTURE, BASE=FIXTURE / 'ORDEM_DUMMY')
    contract_file = HERE.parent / 'e6_prepare_v3/CONTRACT.json'
    contract = json.loads(contract_file.read_bytes())
    floors = {'systematic_conditions': [{'reading': name, 'floor5_INPUT': 0.01, 'floor15_INPUT': 0.003} for name in contract['readings']]}
    floor_ref = write(FIXTURE / 'DUMMY_FLOORS.json', floors)
    rows, bindings = n['rows_and_bindings'](contract, floors, floor_ref, 'TEST')
    cases = []

    def test(name, expected_rejection, action):
        try:
            detail = action()
            rejected = False
        except ValueError as exc:
            detail, rejected = str(exc), True
        cases.append({'id': name, 'expected_rejection': expected_rejection, 'rejected': rejected,
                      'expectation_met': expected_rejection == rejected, 'detail': detail})

    def invariant(ok, message):
        if not ok:
            raise ValueError(message)
        return 'satisfied'

    test('allocation_has_no_scientific_bindings', False, lambda: invariant(n['rows_and_bindings'](contract, floors, floor_ref, 'E3.2') == ([], []), 'E3.2 fabricated results'))
    test('calibration_wall_has_no_scientific_bindings', False, lambda: invariant(n['rows_and_bindings'](contract, floors, floor_ref, 'E3.3') == ([], []), 'E3.3 fabricated calibration'))
    test('TEST_wall_has_no_test_data_physical_values_or_paid_flags', False, lambda: invariant(all(
        r['summary'] == {'test_data_present': False, 'verdict': 'AWAITING_DATA'}
        and r['gate']['color'] == 'red'
        and all(x is None for x in r['metrics'].values())
        and all(r['gate'][x] is False for x in n['FLAGS'])
        and all(r['gate'][x] is None for x in ('sigma_c_calibrated', 'sigma_sys_df', 'sigma_jit_recovered', 'correction_over_sigma_physical'))
        for r in rows), 'Wall promoted to science'))
    test('historical_tau220_floors_not_transplanted', False, lambda: invariant(all(
        (r['gate']['floor5_INPUT'] == 0.01 and r['historical_floor_context']['source'] == floor_ref)
        if r['route'] == 'TAU220_POPULATION' else
        (r['gate']['floor5_INPUT'] is None and r['gate']['floor15_sensitivity'] is None and r['historical_floor_context'] is None)
        for r in rows), 'Historical floor channel changed'))
    def validate_pointers():
        obj = {'rows': rows}
        for binding, row in zip(bindings, rows):
            if any(n['pointer'](obj, spec['pointer']) is not None for spec in binding['metrics'].values()):
                raise ValueError('Non-null wall metric')
            if n['pointer'](obj, binding['gate_pointer']) != row['gate'] or n['pointer'](obj, binding['test_summary_pointer']) != row['summary']:
                raise ValueError('Wrong row pointer')
        return {'bindings': len(bindings), 'all_literal_pointers_resolve': True}
    test('TEST_wall_literal_mappings_resolve', False, validate_pointers)

    def predecessor_case(label, kind='NO_EXECUTION', mutation=None):
        directory = FIXTURE / label
        evidence = {'recorded': '2020-01-01T00:10:00Z', 'finish': '2020-01-01T00:10:00Z', 'reason': 'DUMMY_WALL'}
        artifact = write(directory / 'evidence.json', evidence)
        stage = 'E3.2' if kind == 'ALLOCATION_REGISTERED' else 'E3.3'
        registration = hashlib.sha256(b'DUMMY_REGISTRATION').hexdigest()
        previous = write(directory / 'predecessor.json', {'dummy': 'identity only'})
        timeline = {'kind': kind, 'evidence': artifact, 'recorded_utc_pointer': '/recorded', 'finished_utc_pointer': '/finish'}
        receipt = {'schema': 'E6_REVIEWED_STAGE_V2', 'stage': stage, 'registration_sha256': registration,
                   'artifact': artifact, 'timeline': timeline, 'predecessor': previous,
                   'bindings': [], 'outcome': 'BLOCKED' if kind == 'NO_EXECUTION' else 'COMPLETED',
                   'issued_utc': '2020-01-01T00:11:00Z'}
        review = {'status': 'ACCEPTED_FOR_E6_MAPPING', 'blocking_findings': [], 'stage': stage,
                  'registration_sha256': registration, 'artifact_sha256': artifact['sha256'], 'reviewer': 'DUMMY_REVIEWER',
                  'bindings': [], 'timeline': copy.deepcopy(timeline), 'predecessor': previous,
                  'outcome': receipt['outcome'], 'reviewed_utc': '2020-01-01T00:12:00Z'}
        if mutation:
            mutation(review)
        receipt['review'] = write(directory / 'review.json', review)
        ref = write(directory / 'receipt.json', receipt)
        _, stamp = n['reviewed_predecessor'](ref, stage, registration)
        return {'documentary_time': stamp.isoformat(), 'kind': kind}
    test('NO_EXECUTION_predecessor_uses_recorded_time_only', False, lambda: predecessor_case('validwall'))
    test('allocation_predecessor_uses_registration_completion', False, lambda: predecessor_case('validallocation', kind='ALLOCATION_REGISTERED'))
    test('predecessor_open_review_rejected', True, lambda: predecessor_case('blockedreview', mutation=lambda r:r.update(blocking_findings=['DUMMY_OPEN'])))
    test('predecessor_wrong_artifact_rejected', True, lambda: predecessor_case('wrongartifact', mutation=lambda r:r.update(artifact_sha256=hashlib.sha256(b'wrong').hexdigest())))
    test('predecessor_changed_timeline_rejected', True, lambda: predecessor_case('wrongtimeline', mutation=lambda r:r.update(timeline={})))
    test('predecessor_early_review_rejected', True, lambda: predecessor_case('earlyreview', mutation=lambda r:r.update(reviewed_utc='2020-01-01T00:09:00Z')))
    evidence = {'schema': 'E3_WALL_HELPER_INDEPENDENT_FINITE_REVIEW_V1', 'reviewed_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Helper snapshot only, AST-selected pure mapping and dummy reviewed_predecessor; no real prepare/finalize/main invoked',
        'source_sha256': source_hash, 'source_unchanged_at_end': sha(SOURCE) == source_hash,
        'snapshot_sha256': sha(FIXTURE / 'wall_stage_adapter_snapshot.py'), 'harness_sha256': sha(Path(__file__)),
        'E6_contract_sha256': sha(contract_file), 'cases': cases, 'total': len(cases),
        'passed': sum(x['expectation_met'] for x in cases), 'actual_adapters_reviewed': [],
        'actual_stage_receipts_created': False, 'actual_E6_executed': False, 'E6_execution_authorized': False,
        'limitations': 'Does not replace review of actual authorization, draft, artifact, principal note, witness, timing, predecessors and finalization byte pins.'}
    write(FIXTURE / 'EVIDENCE.json', evidence)
    print(json.dumps({'total': evidence['total'], 'passed': evidence['passed'], 'source_sha256': source_hash,
                      'source_unchanged_at_end': evidence['source_unchanged_at_end']}))


if __name__ == '__main__':
    main()
