"""Independent E6 contract probes. Dummy metadata only; never calls producer main.

All writes below this review directory. Real sources are hashed, never decoded
except the preparation contracts/code. No scientific baseline is assembled.
"""
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace
import ast
import copy
import hashlib
import json
import os
import sys

HERE = Path(__file__).resolve().parent
PREP = HERE.parent / 'e6_prepare_v2'
ROOT = HERE.parents[2]
OUT = HERE / 'fixture_v2'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_new(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode() if not isinstance(value, bytes) else value
    temp = p.with_name(p.name + '.pending')
    with temp.open('xb') as stream:
        stream.write(data)
    if temp.read_bytes() != data:
        raise RuntimeError('Fixture write mismatch')
    os.link(temp, p)
    temp.unlink()
    return {'path': p.relative_to(OUT if p.is_relative_to(OUT) else HERE).as_posix(), 'sha256': digest(p)}


def producer_namespace():
    tree = ast.parse((PREP / 'generate_reach_table.py').read_bytes())
    allowed = {'require', 'sha', 'load', 'pinned', 'utc', 'pointer', 'missing',
               'copy_metric', 'new_scenario', 'check_metric', 'check_timeline', 'activate',
               'assemble_baselines', 'append_reviewed', 'render'}
    constants = {'LIMIT', 'ROUTES', 'GROUPS', 'METRICS', 'GATE_FIELDS', 'STAGES', 'PAID_FLAGS', 'SEMANTIC_UNITS', 'FUTURE_GROUPS', 'EVIDENCE_VERDICTS'}
    nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))
             or isinstance(n, ast.FunctionDef) and n.name in allowed
             or isinstance(n, ast.Assign) and all(isinstance(t, ast.Name) and t.id in constants for t in n.targets)]
    namespace = {'__name__': 'independent_ast_fixture'}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(PREP / 'generate_reach_table.py'), 'exec'), namespace)
    namespace.update(ROOT=OUT, BASE=OUT / 'ORDEM_DUMMY', HERE=OUT / 'ORDEM_DUMMY/bis/prepare')
    return namespace


def main():
    if OUT.exists():
        raise RuntimeError('Exclusive fixture; preserve prior evidence')
    n = producer_namespace()
    contract = json.loads((PREP / 'CONTRACT.json').read_text(encoding='utf-8-sig'))
    source_pins = json.loads((PREP / 'SOURCE_PINS.json').read_text(encoding='utf-8-sig'))
    manifest = json.loads((PREP / 'PREPARATION_MANIFEST_V2.json').read_text(encoding='utf-8-sig'))
    evidence = {'schema': 'E6_INDEPENDENT_CLOSING_PROBES_V2', 'created_utc': datetime.now(timezone.utc).isoformat(),
                'scope': 'AST-selected functions on dummy metadata only; no producer main, real stages, posterior, seeds, strain, PE, MC or E6 outputs',
                'preparation_pins': {}, 'source_pin_checks': [], 'cases': []}
    for p in sorted(PREP.iterdir()):
        if p.is_file():
            evidence['preparation_pins'][p.name] = {'sha256': digest(p), 'bytes': p.stat().st_size}
    evidence['manifest_matches'] = all({'sha256': digest(PREP / k), 'bytes': (PREP / k).stat().st_size} == v for k, v in manifest['artifacts'].items())
    for section in ('sources', 'document_pins'):
        for alias, ref in source_pins[section].items():
            p = (ROOT / ref['path']).resolve()
            if not p.is_relative_to(ROOT.resolve()) or p.suffix not in ('.json', '.md') or any(t.upper() == 'E2_PRIVATE' for t in p.parts):
                raise RuntimeError('Unexpected source path')
            actual = digest(p)
            evidence['source_pin_checks'].append({'alias': alias, 'path': ref['path'], 'expected': ref['sha256'], 'actual': actual, 'match': actual == ref['sha256'], 'access': 'byte hash only'})

    def probe(name, expected_rejection, action):
        try:
            result = action()
            rejected = False
            detail = result if isinstance(result, (str, int, bool, dict)) else 'accepted'
        except Exception as exc:
            rejected = isinstance(exc, ValueError)
            detail = type(exc).__name__ + ': ' + str(exc)
        evidence['cases'].append({'id': name, 'expected_rejection': expected_rejection,
                                  'rejected': rejected, 'expectation_met': rejected == expected_rejection, 'detail': detail})

    # Actual byte-pinned fixture receipts; all paths are confined to fixture_v1.
    ph = n['HERE']
    write_new(ph / 'generate_reach_table.py', b'# DUMMY PACKAGE IDENTITY ONLY\n')
    write_new(ph / 'CONTRACT.json', {'readings': contract['readings']})
    write_new(ph / 'OUTPUT_SCHEMA.json', {'dummy': True})
    reg = {'status': 'REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST', 'registered_utc': '2020-01-01T00:00:00Z',
           'readings': contract['readings'], 'witness_relative_to_Chatgpt': 'TUNEL/DO_CHATGPT/DUMMY.md',
           'activation': {'receipt_relative_to_Chatgpt': 'ORDEM_DUMMY/activation.json', 'review_application_sha256': hashlib.sha256(b'dummy application').hexdigest()}}
    regref = write_new(n['BASE'] / 'RINGDOWN_5SIGMA_V1.json', reg)
    witness = write_new(OUT / reg['witness_relative_to_Chatgpt'], ('registro_sha256: ' + regref['sha256'] + '\n').encode())
    activation = write_new(OUT / reg['activation']['receipt_relative_to_Chatgpt'], {
        'status': 'E2_ACTIVATION_COMPLETE', 'registration_sha256': regref['sha256'], 'witness_sha256': witness['sha256'],
        'review_application_sha256': reg['activation']['review_application_sha256'], 'finished_utc': '2020-01-01T00:10:00Z'})
    write_new(ph / 'SOURCE_PINS.json', {'sources': {'E2': regref, 'E2_ACTIVATION': activation}})
    package = {f: digest(ph / f) for f in ('generate_reach_table.py', 'CONTRACT.json', 'SOURCE_PINS.json', 'OUTPUT_SCHEMA.json')}

    def activation_case(label, times=None, review_mutator=None, auth_mutator=None, wall=False, activity_mutator=None, predecessor_mutator=None):
        times = times or ['2020-01-01T00:20:00Z', '2020-01-01T00:30:00Z', '2020-01-01T00:40:00Z']
        refs = {}
        evidence_refs = {}
        for stage, stamp in zip(n['STAGES'], times):
            d = OUT / label / stage
            artifact = write_new(d / 'artifact.json', {'dummy': True})
            index = n['STAGES'].index(stage)
            predecessor = activation if index == 0 else refs[n['STAGES'][index-1]]
            outcome = 'BLOCKED' if wall else 'COMPLETED'
            activity = {'authorized': '2019-12-31T23:00:00Z', 'start': stamp, 'finish': stamp,
                        'recorded': stamp, 'reason': 'DUMMY_NO_EXECUTION_WALL',
                        'predecessor': evidence_refs[n['STAGES'][index-1]]['sha256'] if index else activation['sha256']}
            if activity_mutator:
                activity_mutator(stage, activity)
            eref = write_new(d / 'timeline_evidence.json', activity)
            evidence_refs[stage] = eref
            timeline = {'evidence': eref, 'kind': 'NO_EXECUTION' if wall else ('ALLOCATION_REGISTERED' if stage == 'E3.2' else 'EXECUTED'),
                        'authorized_utc_pointer': '/authorized', 'started_utc_pointer': '/start', 'finished_utc_pointer': '/finish',
                        'recorded_utc_pointer': '/recorded', 'reason_pointer': '/reason', 'predecessor_evidence_sha256_pointer': '/predecessor'}
            if predecessor_mutator:
                predecessor = predecessor_mutator(stage, copy.deepcopy(predecessor))
            review = {'status': 'ACCEPTED_FOR_E6_MAPPING', 'stage': stage, 'registration_sha256': regref['sha256'],
                      'artifact_sha256': artifact['sha256'], 'blocking_findings': [], 'reviewed_utc': stamp,
                      'bindings': [], 'outcome': outcome, 'reviewer': 'DUMMY_INDEPENDENT_REVIEWER', 'timeline': timeline, 'predecessor': predecessor}
            if review_mutator:
                review_mutator(review)
            revref = write_new(d / 'review.json', review)
            refs[stage] = write_new(d / 'receipt.json', {'schema': 'E6_REVIEWED_STAGE_V2', 'stage': stage,
                'registration_sha256': regref['sha256'], 'outcome': outcome, 'issued_utc': stamp, 'timeline': timeline, 'predecessor': predecessor,
                'artifact': artifact, 'review': revref, 'bindings': []})
        auth = {'status': 'AUTHORIZED_E6_ASSEMBLY_AFTER_REVIEWED_E3_AND_TEST', 'new_scientific_computation_allowed': False,
                'package_sha256': package, 'registration': regref, 'witness': witness, 'issued_utc': '2020-01-01T01:00:00Z',
                'reviewed_stages': refs, 'run_id': 'dummy_' + label}
        if auth_mutator:
            auth_mutator(auth)
        path = OUT / label / 'authorization.json'
        pin = write_new(path, auth)
        n['activate'](SimpleNamespace(execute=True, authorization=path, authorization_sha256=pin['sha256']))
        return 'accepted by activate; no assembly or output invoked'

    probe('valid_dummy_activation', False, lambda: activation_case('valid'))
    probe('stage_before_E2_activation', True, lambda: activation_case('early', ['2020-01-01T00:05:00Z', '2020-01-01T00:30:00Z', '2020-01-01T00:40:00Z']))
    probe('TEST_before_allocation_and_calibration', True, lambda: activation_case('reversed', ['2020-01-01T00:40:00Z', '2020-01-01T00:30:00Z', '2020-01-01T00:20:00Z']))
    probe('review_before_receipt', True, lambda: activation_case('reviewearly', review_mutator=lambda r: r.update(reviewed_utc='2020-01-01T00:11:00Z')))
    probe('review_wrong_artifact_hash', True, lambda: activation_case('wronghash', review_mutator=lambda r: r.update(artifact_sha256=hashlib.sha256(b'wrong artifact').hexdigest())))
    probe('review_blocking_findings', True, lambda: activation_case('blocker', review_mutator=lambda r: r.update(blocking_findings=['DUMMY_OPEN'])))
    probe('review_wrong_binding', True, lambda: activation_case('binding', review_mutator=lambda r: r.update(bindings=[{'dummy': 'different'}])))
    probe('missing_TEST_stage', True, lambda: activation_case('missing', auth_mutator=lambda a: a['reviewed_stages'].pop('TEST')))
    probe('changed_package', True, lambda: activation_case('package', auth_mutator=lambda a: a['package_sha256'].update({'generate_reach_table.py': hashlib.sha256(b'wrong package').hexdigest()})))
    # Restore local dictionary altered in the last deliberate negative.
    package['generate_reach_table.py'] = digest(ph / 'generate_reach_table.py')

    def binding_case(color='green', physical=True, gate_ratio=None, verdict='NOT_FALSIFIED_POWERED',
                     data=True, paid=True, units=None, group='O4_CEGO', wrongcal=False, incomplete=False, route='TAU220_POPULATION', conditional=False, cal_ratio=None, insufficient=True):
        key = (route, 'R-B', group)
        is_iv = route == 'DF220_POPULATION_WIDTH_IV'
        unit = units or ('fractional_dtau440' if route == 'TAU440_FIXED_SOURCE_FISHER' else 'fractional_dtau220')
        cells = {key: {'scenarios': []}}
        gate = {'color': color, 'status': 'DUMMY_ONLY', 'decision_reviewed': True,
                **{f: paid for f in n['PAID_FLAGS']},
                'sigma_c_calibrated': None if is_iv else 0.001, 'floor5_INPUT': None if is_iv else 0.01, 'floor15_sensitivity': None if is_iv else 0.003,
                'sigma_sys_df': 0.001 if is_iv else None, 'sigma_jit_recovered': 0.002 if is_iv else None, 'correction_over_sigma_physical': None,
                'units': {f: (units or 'width_fractional_df220') if f in ('sigma_sys_df','sigma_jit_recovered') else (unit if f != 'correction_over_sigma_physical' else 'dimensionless') for f in n['GATE_FIELDS']}}
        summary = {'verdict': verdict, 'test_data_present': data, 'unblinding_authorized': True,
                   'population_checks_passed': True, 'decision_rule_paid': True, 'reading_multiplicity_paid': True,
                   'relative_exclusion_rule_paid': True, 'power_assessment': 'INSUFFICIENT_REVIEWED' if insufficient else 'UNREVIEWED'}
        sources, stages = {}, {}
        for stage in n['STAGES']:
            # These are dummy in-memory bindings: refs identify deterministic dummy bytes.
            ref = {'path': 'DUMMY_' + stage + '.json', 'sha256': hashlib.sha256(('DUMMY_' + stage).encode()).hexdigest()}
            obj = {'gate': copy.deepcopy(gate), 'summary': summary, 'value': 0.2}
            obj['gate']['correction_over_sigma_physical'] = gate_ratio if stage == 'TEST' else cal_ratio
            bindings = []
            if stage != 'E3.2':
                binding = dict(route=key[0], reading=key[1], data_group=key[2], scenario_id='dummy', scope='DUMMY_FIXTURE_NOT_SCIENCE', metrics={}, gate_pointer='/gate')
                if stage == 'TEST':
                    binding.update(test_summary_pointer='/summary', calibration_scenario_id='dummy', calibration_receipt_sha256=stages['E3.3'][1]['sha256'])
                    if wrongcal:
                        binding['calibration_receipt_sha256'] = hashlib.sha256(b'wrong calibration').hexdigest()
                    if conditional:
                        binding['metrics']['correction_over_sigma'] = {'pointer': '/value', 'unit': 'dimensionless'}
                    if physical:
                        binding['metrics']['z_physical'] = {'pointer': '/value', 'unit': 'dimensionless'}
                bindings = [binding]
            receipt = {'bindings': bindings, 'outcome': 'PARTIAL' if incomplete else 'COMPLETED', 'review': ref, 'artifact': ref}
            stages[stage] = (receipt, ref)
            sources['STAGE_' + stage] = (ref, obj)
        n['append_reviewed'](cells, sources, stages, contract['readings'], contract['permitted_verdicts'])
        row = cells[key]['scenarios'][-1]
        for name, item in row['metrics'].items():
            n['check_metric'](name, item, route)
        return {'gate': row['gate']['color'], 'verdict': row['verdict'], 'physical_ratio': row['gate']['correction_over_sigma_physical']['value'], 'group': group, 'z_physical_dummy': row['metrics']['z_physical']['value'], 'conditional_ratio': row['metrics']['correction_over_sigma']['value']}

    probe('valid_green_dummy_binding', False, lambda: binding_case())
    probe('red_z_physical', True, lambda: binding_case(color='red'))
    probe('wrong_calibration_receipt', True, lambda: binding_case(wrongcal=True))
    probe('unpaid_physical_readout', True, lambda: binding_case(paid=False))
    probe('partial_physical_readout', True, lambda: binding_case(incomplete=True))
    probe('red_gate_physical_ratio', True, lambda: binding_case(color='red', physical=False, gate_ratio=6.0, verdict='INCONCLUSIVE_SYSTEMATICS'))
    probe('red_data_AWAITING_DATA', True, lambda: binding_case(color='red', physical=False, verdict='AWAITING_DATA'))
    probe('unpaid_partial_NOT_FALSIFIED_UNDERPOWERED', True, lambda: binding_case(physical=False, verdict='NOT_FALSIFIED_UNDERPOWERED', paid=False, incomplete=True))
    probe('green_tau_gate_in_Hz', True, lambda: binding_case(units='Hz'))
    probe('future_ET_physical_test', True, lambda: binding_case(group='ET'))
    probe('no_data_falsified', True, lambda: binding_case(data=False, physical=False, verdict='FALSIFIED_IN_READING'))
    probe('no_data_OPEN', False, lambda: binding_case(color='OPEN', data=False, physical=False, verdict='AWAITING_DATA'))

    probe('valid_underpowered_z_below_5', False, lambda: binding_case(verdict='NOT_FALSIFIED_UNDERPOWERED'))
    probe('underpowered_no_power_review', True, lambda: binding_case(verdict='NOT_FALSIFIED_UNDERPOWERED', insufficient=False))
    probe('red_conditional_ratio_allowed', False, lambda: binding_case(color='red', physical=False, verdict='INCONCLUSIVE_SYSTEMATICS', conditional=True))
    probe('calibration_physical_ratio_forbidden', True, lambda: binding_case(cal_ratio=0.2))
    probe('valid_TEST_physical_ratio_calibration_null', False, lambda: binding_case(physical=False, gate_ratio=0.2))
    probe('valid_tau440_binding', False, lambda: binding_case(route='TAU440_FIXED_SOURCE_FISHER'))
    probe('valid_IV_binding', False, lambda: binding_case(route='DF220_POPULATION_WIDTH_IV'))
    probe('wrong_tau440_channel', True, lambda: binding_case(route='TAU440_FIXED_SOURCE_FISHER', units='fractional_dtau220'))
    probe('wrong_IV_channel', True, lambda: binding_case(route='DF220_POPULATION_WIDTH_IV', units='fractional_dtau220'))
    probe('red_present_INCONCLUSIVE', False, lambda: binding_case(color='red', physical=False, verdict='INCONCLUSIVE_SYSTEMATICS'))
    probe('green_present_AWAITING_DATA', True, lambda: binding_case(physical=False, verdict='AWAITING_DATA'))
    for group in n['FUTURE_GROUPS']:
        probe('future_'+group+'_physical_forbidden', True, lambda group=group: binding_case(group=group))
        probe('future_'+group+'_conditional_allowed', False, lambda group=group: binding_case(group=group, color='OPEN', physical=False, verdict='AWAITING_DATA', data=False, conditional=True))
    probe('valid_documented_no_execution_walls', False, lambda: activation_case('walls', wall=True))
    probe('source_activity_before_activation', True, lambda: activation_case('activityearly', activity_mutator=lambda stage,a: a.update(start='2020-01-01T00:05:00Z') if stage=='E3.2' else None))
    probe('source_TEST_before_calibration_finish', True, lambda: activation_case('activityreverse', activity_mutator=lambda stage,a: a.update(start='2020-01-01T00:21:00Z') if stage=='TEST' else None))
    probe('source_GO_after_activity', True, lambda: activation_case('golate', activity_mutator=lambda stage,a: a.update(authorized='2020-01-01T00:59:00Z')))
    probe('source_predecessor_evidence_hash_wrong', True, lambda: activation_case('predsource', activity_mutator=lambda stage,a: a.update(predecessor=hashlib.sha256(b'wrong predecessor source').hexdigest()) if stage=='TEST' else None))
    probe('adapter_predecessor_hash_wrong', True, lambda: activation_case('predreceipt', predecessor_mutator=lambda stage,p: dict(p,sha256=hashlib.sha256(b'wrong predecessor receipt').hexdigest()) if stage=='TEST' else p))
    probe('review_timeline_not_exact', True, lambda: activation_case('reviewtimeline', review_mutator=lambda r:r.update(timeline={})))

    dummy_ref = {'path': 'DUMMY.json', 'sha256': hashlib.sha256(b'DUMMY').hexdigest()}
    dummy_sources = {'E0': (dummy_ref, {'planning_targets': [], 'all_calibration_combinations': {},
        'conditional_rates_scenarios': {'forecasts': [], 'rates': []}, 'threeG_fixed_anchor_calculations': [], 'systematic_conditions': []}),
        'E4_RESULT': (dummy_ref, {'E4_fisher': [], 'E5_information': []}), 'E2': (dummy_ref, {'route_IV': {'targets': []}})}
    cells = n['assemble_baselines'](contract, dummy_sources)
    evidence['empty_dummy_grid'] = {'cells': len(cells), 'unique_readings': len({k[1] for k in cells}),
                                  'scenarios': sum(len(v['scenarios']) for v in cells.values()), 'retained_all': len(cells) == 180}
    def historical_o5_dummy():
        fixture_sources = copy.deepcopy(dummy_sources)
        fixture_sources['E0'][1]['conditional_rates_scenarios']['forecasts'] = [{
            'reading': 'R-B', 'gain_label': 'DUMMY', 'gain': 1, 'exposure_status': 'DUMMY_ONLY',
            'reference_population': 'DUMMY', 'rate_population': 'DUMMY', 'scope': 'DUMMY_NOT_SCIENCE',
            'z_optimistic_same_source_quality_plus_volume': 0.2,
            'N90_at_fixed_source_improved_sigma': 10, 'operational_information_target': 100,
            'z_optimistic_CI90_rate_only': [0.1, 0.3], 'z_detection_threshold_quality_invariant_control': 0.2}]
        grid = n['assemble_baselines'](contract, fixture_sources)
        row = grid[('TAU220_POPULATION', 'R-B', 'O5_BANDA')]['scenarios'][0]
        for name, metric in row['metrics'].items():
            n['check_metric'](name, metric, 'TAU220_POPULATION')
        return {'information_unit': row['metrics']['N90_information_target']['unit'], 'physical_z': row['metrics']['z_physical']['value']}
    probe('R3_existing_O5_mapping_nonnull_information_dummy', False, historical_o5_dummy)
    evidence['producer_files_unchanged'] = all(digest(PREP / k) == v['sha256'] for k, v in evidence['preparation_pins'].items())
    evidence['semantic_units_match_contract'] = json.loads(json.dumps(n['SEMANTIC_UNITS'])) == contract['semantic_units']
    evidence['producer_main_called'] = False
    evidence['science_output_created'] = False
    evidence['E6_assembly_authorized'] = False
    evidence['expectations_met'] = sum(c['expectation_met'] for c in evidence['cases'])
    evidence['negative_accepted'] = [c['id'] for c in evidence['cases'] if c['expected_rejection'] and not c['rejected']]
    write_new(HERE / 'E6_INDEPENDENT_FIXTURE_EVIDENCE_V2.json', evidence)
    print(json.dumps({'cases': len(evidence['cases']), 'expectations_met': evidence['expectations_met'],
                      'negative_accepted': evidence['negative_accepted'], 'pins_all_match': all(x['match'] for x in evidence['source_pin_checks']),
                      'manifest_matches': evidence['manifest_matches'], 'grid': evidence['empty_dummy_grid']}, indent=2))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
