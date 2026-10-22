"""Final read-only checks plus an additive pin bundle; no scientific imports."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import sys

O = Path(__file__).resolve().parent
B = O.parents[1]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read(name):
    return json.loads((O/name).read_text(encoding='utf-8'))


def main():
    target = O/'PIN_BUNDLE.json'
    require(not target.exists(), 'Preserve existing pin bundle')
    manifest, plan, receipt = read('INPUT_MANIFEST.json'), read('PLAN.json'), read('STATIC_RECEIPT.json')
    for entry in manifest['files']:
        path = B/entry['path']
        require(path.stat().st_size == entry['bytes'] and sha(path) == entry['sha256'], 'Input changed: '+entry['path'])
    for name, info in receipt['outputs'].items():
        require(sha(O/name) == info['sha256'], 'Output changed: '+name)
    for name, digest in receipt['scripts'].items():
        require(sha(O/name) == digest, 'Code changed: '+name)
    require(plan['input_manifest_sha256'] == sha(O/'INPUT_MANIFEST.json'), 'Plan pin')
    tree = ast.parse((O/'deterministic_e4_e5.py').read_text(encoding='utf-8'))
    compile(tree, 'deterministic_e4_e5.py', 'exec', optimize=1)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    main_body = functions['main'].body
    gate_position = next(i for i,n in enumerate(main_body) if isinstance(n, ast.Assign) and
                         isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id == 'gate')
    import_positions = [i for i,n in enumerate(main_body) if isinstance(n, (ast.Import, ast.ImportFrom))]
    require(all(i > gate_position for i in import_positions), 'Scientific import before gate')
    for n in ast.walk(tree):
        require(not isinstance(n, ast.Assert), 'Optimization-unsafe assert')
        if isinstance(n, ast.Attribute):
            require(n.attr not in ['default_rng', 'random', 'sample', 'rvs'], 'Stochastic execution introduced')
    forecast = ast.get_source_segment((O/'deterministic_e4_e5.py').read_text(encoding='utf-8'), functions['forecast'])
    require('+.5 * d * (1 / zm**2 + 1 / zp**2)' in forecast, 'Derivative sign')
    require("'AMPLITUDE_FIXA_INPUT'" in forecast and 'norm / norm_o4' in forecast, 'Fixed amplitude route')
    require('cfg[\'operational_delta_min\']' in forecast and "cfg['normal_90_quantile']" in forecast, 'Power/subresolution contract')
    meta = read('METADATA_AND_HIGH_SNR.json')
    rows = meta['rows']
    require(len(rows) == len({r['event'] for r in rows}) == 114, 'Metadata uniqueness')
    require(sum(r['eligibility_INPUT'] is True for r in rows) == 69, 'Eligibility count')
    require(sum(r['eligibility_INPUT'] is None for r in rows) == 11, 'Missing count')
    require(meta['GW250207_status']['eligibility_INPUT'] is None, 'Missing GR promoted')
    require(not (O/'runs').exists(), 'Unexpected scientific run')
    pins = {n: sha(O/n) for n in ['PLAN.json','INPUT_MANIFEST.json','SCHEMA.json','deterministic_e4_e5.py']}
    result = {'status': 'READY_FOR_PRINCIPAL_PIN_NOT_AUTHORIZATION', 'utc': datetime.now(timezone.utc).isoformat(),
              'e4_e5_preparation_pins': pins, 'python_optimize': sys.flags.optimize,
              'validation_script_sha256': sha(Path(__file__)), 'static_receipt_sha256': sha(O/'STATIC_RECEIPT.json'),
              'checked_input_files': len(manifest['files']), 'metadata_unique_ge12': 114,
              'eligible_INPUT': 69, 'awaiting_GR_metadata': 11, 'prepared_fisher_matrix_rows': 1920,
              'scientific_execution': False, 'HDF_values_read': False, 'all_pins_rechecked': True,
              'limits': 'AST/source and metadata checks only, not derivative finite-difference, Fisher, density or runtime numerical validation',
              'activation_template_NOT_AUTHORIZED': {
                  'status': 'TEMPLATE_NOT_AUTHORIZED', 'allowed_task': 'E4_E5_DETERMINISTIC_ARCHIVED_CALIBRATION_ONLY',
                  'new_test_data_allowed': False, 'package_sha256': pins,
                  'E2_registration_path': None, 'E2_registration_sha256': None,
                  'E2_tunnel_witness_path': None, 'E2_tunnel_witness_sha256': None,
                  'run_id': 'principal_authorized_001'}}
    with target.open('xb') as stream:
        stream.write((json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8'))
    print(json.dumps({'status': result['status'], 'plan_sha256': pins['PLAN.json'], 'bundle_sha256': sha(target)}))


if __name__ == '__main__':
    main()
