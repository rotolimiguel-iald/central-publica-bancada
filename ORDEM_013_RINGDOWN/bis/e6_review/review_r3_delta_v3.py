"""Focused independent E6 V3 review: one label delta and dummy unit probes.

No main/activation, real stage adapter, real baseline assembly or science call.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import copy
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
V2 = HERE.parent / 'e6_prepare_v2'
V3 = HERE.parent / 'e6_prepare_v3'
ROOT = HERE.parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def publish(path, obj):
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
    temporary = path.with_name(path.name + '.pending')
    with temporary.open('xb') as stream:
        stream.write(raw)
    if temporary.read_bytes() != raw:
        raise ValueError('Short review write')
    os.link(temporary, path)
    temporary.unlink()


def verify_manifest(folder, filename):
    manifest = json.loads((folder / filename).read_bytes())
    checked = {}
    for relative, expected in manifest['artifacts'].items():
        path = (folder / relative).resolve()
        if not path.is_relative_to(folder.resolve()):
            raise ValueError('Manifest escape')
        actual = {'sha256': sha(path), 'bytes': path.stat().st_size}
        if actual != expected:
            raise ValueError('Changed artifact: ' + relative)
        checked[relative] = actual
    return manifest, checked


def main():
    m2, files2 = verify_manifest(V2, 'PREPARATION_MANIFEST_V2.json')
    m3, files3 = verify_manifest(V3, 'PREPARATION_MANIFEST_V3.json')
    before = (V2 / 'generate_reach_table.py').read_bytes()
    after = (V3 / 'generate_reach_table.py').read_bytes()
    old = b"('N90_information_target','operational_information_target','source_declared_information')"
    new = b"('N90_information_target','operational_information_target','sum_inverse_variance_dtau')"
    if before.count(old) != 1 or before.replace(old, new) != after:
        raise ValueError('Delta exceeds reviewed single label')
    for name in ('CONTRACT.json', 'OUTPUT_SCHEMA.json', 'STAGE_RECEIPT_SCHEMA.json', 'SOURCE_PINS.json'):
        if (V2 / name).read_bytes() != (V3 / name).read_bytes():
            raise ValueError('Unexpected contract/schema/source change')
    if m3['predecessor_manifest_sha256'] != sha(V2 / 'PREPARATION_MANIFEST_V2.json'):
        raise ValueError('Wrong V2 predecessor')
    for name, pin in m3['activation_package_sha256'].items():
        if sha(V3 / name) != pin:
            raise ValueError('Wrong package pin')

    # Reuse only the reviewer's AST loader; never call either producer main.
    loader = HERE / 'review_fixtures_v2.py'
    tree = ast.parse(loader.read_bytes())
    allowed = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef))]
    namespace = {'__file__': str(loader), '__name__': 'independent_delta_loader'}
    exec(compile(ast.Module(body=allowed, type_ignores=[]), str(loader), 'exec'), namespace)
    namespace['PREP'] = V3
    namespace['OUT'] = HERE / 'UNUSED_DUMMY_V3_ROOT'
    n = namespace['producer_namespace']()
    contract = json.loads((V3 / 'CONTRACT.json').read_bytes())
    ref = {'path': 'DUMMY_MEMORY_ONLY.json', 'sha256': hashlib.sha256(b'DUMMY_NOT_SCIENCE').hexdigest()}
    fixture = {'E0': (ref, {'planning_targets': [], 'all_calibration_combinations': {},
        'conditional_rates_scenarios': {'forecasts': [], 'rates': []}, 'threeG_fixed_anchor_calculations': [], 'systematic_conditions': []}),
        'E4_RESULT': (ref, {'E4_fisher': [], 'E5_information': []}), 'E2': (ref, {'route_IV': {'targets': []}})}
    forecast = {'reading': 'R-B', 'gain_label': 'DUMMY', 'gain': 1, 'exposure_status': 'DUMMY',
        'reference_population': 'DUMMY', 'rate_population': 'DUMMY', 'scope': 'DUMMY_ONLY',
        'z_optimistic_same_source_quality_plus_volume': 0.2, 'N90_at_fixed_source_improved_sigma': 10,
        'operational_information_target': 100, 'z_optimistic_CI90_rate_only': [0.1, 0.3],
        'z_detection_threshold_quality_invariant_control': 0.2}
    cases = []

    def probe(label, expected_rejection, action):
        try:
            detail = action()
            rejected = False
        except ValueError as exc:
            detail, rejected = str(exc), True
        cases.append({'id': label, 'expected_rejection': expected_rejection, 'rejected': rejected,
                      'expectation_met': rejected == expected_rejection, 'detail': detail})

    def check_forecast(value):
        sources = copy.deepcopy(fixture)
        row_input = dict(forecast, operational_information_target=value)
        sources['E0'][1]['conditional_rates_scenarios']['forecasts'] = [row_input]
        cells = n['assemble_baselines'](contract, sources)
        row = cells[('TAU220_POPULATION', 'R-B', 'O5_BANDA')]['scenarios'][0]
        for name, metric in row['metrics'].items():
            n['check_metric'](name, metric, 'TAU220_POPULATION')
        metric = row['metrics']['N90_information_target']
        if metric['value'] != value or metric['source']['pointer'] != '/conditional_rates_scenarios/forecasts/0/operational_information_target':
            raise ValueError('Value/pointer changed')
        if row['metrics']['z_physical']['value'] is not None or row['verdict'] != 'AWAITING_DATA' or row['gate']['color'] != 'OPEN':
            raise ValueError('Projection promoted')
        if len(cells) != 180:
            raise ValueError('Lost grid cells')
        return {'unit': metric['unit'], 'status': metric['status'], 'value_and_pointer_preserved': True,
                'grid': 180, 'physical_z': None, 'verdict': row['verdict']}

    probe('R3_O5_nonnull_information_dummy', False, lambda: check_forecast(100))
    probe('R3_O5_null_remains_OPEN', False, lambda: check_forecast(None))
    for label in ('source_declared_information', 'Hz', 'event_count', 'sum_inverse_variance_dtau440'):
        def reject_unit(unit=label):
            metric = dict(value=100, status='INPUT_CONDITIONAL_COPIED', unit=unit,
                          source=dict(ref, pointer='/dummy'), reason='DUMMY_ONLY')
            n['check_metric']('N90_information_target', metric, 'TAU220_POPULATION')
            return 'accepted'
        probe('R3_incompatible_' + label, True, reject_unit)

    source_checks = []
    sources = json.loads((V3 / 'SOURCE_PINS.json').read_bytes())
    for section in ('sources', 'document_pins'):
        for alias, pin in sources[section].items():
            path = (ROOT / pin['path']).resolve()
            if not path.is_relative_to(ROOT.resolve()) or any(x.upper() == 'E2_PRIVATE' for x in path.parts):
                raise ValueError('Unexpected private/escaped source')
            actual = sha(path)
            source_checks.append({'alias': alias, **pin, 'actual_sha256': actual, 'match': actual == pin['sha256']})
    definitions = {}
    for relative, expected in m3['source_definition_pins'].items():
        actual = sha(ROOT / relative)
        definitions[relative] = {'expected': expected, 'actual': actual, 'match': actual == expected}
    e0 = json.loads((ROOT / sources['sources']['E0']['path']).read_bytes())
    rate_code = ROOT / 'ORDEM_013_RINGDOWN/refeito/e0_rate_and_o5_scenarios_013bis.py'
    seal_code = ROOT / 'ORDEM_013_RINGDOWN/refeito/seal_e0_gate_013bis.py'
    provenance = {'rate_code_matches_pinned_E0': sha(rate_code) == e0['conditional_rates_scenarios']['code_sha256'],
        'seal_code_matches_pinned_E0': sha(seal_code) == e0['code_sha256'],
        'rate_code_sha256': sha(rate_code), 'seal_code_sha256': sha(seal_code),
        'forecast_rows_metadata_only': len(e0['conditional_rates_scenarios']['forecasts']),
        'nonnull_information_fields_metadata_only': sum(x['operational_information_target'] is not None for x in e0['conditional_rates_scenarios']['forecasts']),
        'source_read_scope': 'Code declarations and field presence only; no source numerical values emitted or recomputed'}
    # Recheck the frozen trees at the end.
    verify_manifest(V2, 'PREPARATION_MANIFEST_V2.json')
    verify_manifest(V3, 'PREPARATION_MANIFEST_V3.json')
    evidence = {'schema': 'E6_INDEPENDENT_R3_DELTA_V3', 'reviewed_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'BLOCKERS_CLOSED_PREPARATION_ONLY' if all(c['expectation_met'] for c in cases) else 'BLOCKING_FINDINGS_OPEN',
        'cases': cases, 'case_count': len(cases), 'expectations_met': sum(c['expectation_met'] for c in cases),
        'delta_exactly_one_unit_label': True, 'V2_manifest_verified_artifacts': len(files2), 'V3_manifest_verified_artifacts': len(files3),
        'V2_preserved_at_final_check': True, 'contracts_schemas_unchanged': True,
        'manifest_V2_sha256': sha(V2 / 'PREPARATION_MANIFEST_V2.json'), 'manifest_V3_sha256': sha(V3 / 'PREPARATION_MANIFEST_V3.json'),
        'activation_package_sha256': m3['activation_package_sha256'], 'source_pin_checks': source_checks,
        'source_definition_pins': definitions, 'semantic_provenance': provenance,
        'carried_forward_evidence': {'path': 'E6_INDEPENDENT_FIXTURE_EVIDENCE_V2.json', 'sha256': sha(HERE / 'E6_INDEPENDENT_FIXTURE_EVIDENCE_V2.json'),
                                  'scope': 'R1/R2/R4/R5 and other R3 branches unchanged by exact byte delta; prior failed O5 case retained'},
        'harness_sha256': sha(Path(__file__)), 'reused_AST_loader_sha256': sha(loader),
        'actual_E6_executed': False, 'actual_stage_receipts_created': False, 'actual_activation_performed': False,
        'science_executed': False, 'E6_execution_authorized': False, 'order_completed': False}
    if not all(x['match'] for x in source_checks) or not all(x['match'] for x in definitions.values()) or not provenance['rate_code_matches_pinned_E0'] or not provenance['seal_code_matches_pinned_E0']:
        raise ValueError('Source identity/provenance mismatch')
    publish(HERE / 'E6_R3_DELTA_V3_EVIDENCE.json', evidence)
    print(json.dumps({'status': evidence['status'], 'cases': len(cases), 'passed': evidence['expectations_met'],
                      'manifest_V3_sha256': evidence['manifest_V3_sha256'], 'V2_preserved': True}))


if __name__ == '__main__':
    main()
