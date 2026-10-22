"""Metadata/AST packaging only; never import or execute the candidate."""
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUEST = ROOT / 'F9_PRECISION_SERVICES_PREPARATION_REQUEST.json'
REQUEST_ID = 'f820203f-b83c-420a-87ec-7816f3179139'


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def write_json(name, value):
    path = (HERE / name).resolve()
    if path.parent != HERE:
        raise ValueError('write outside preparation folder')
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if path.exists():
        old = path.read_bytes()
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as stream:
            stream.write(old)
        if backup.read_bytes() != old:
            raise ValueError('backup byte mismatch')
    temporary = path.with_name(path.name + '.tmp_' + str(os.getpid()))
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != data or not data:
        raise ValueError('temporary verification failed')
    os.replace(temporary, path)
    if path.read_bytes() != data:
        raise ValueError('written bytes differ')


def main():
    started = datetime.now(timezone.utc).isoformat()
    request_pin = pin(REQUEST)
    request = json.loads(REQUEST.read_text(encoding='utf-8-sig'))
    if request['request_id'] != REQUEST_ID or request['output_folder'] != HERE.name:
        raise ValueError('request identity mismatch')
    source_pins = []
    for expected in request['sources']:
        actual = pin(expected['path'])
        if any(actual[key] != expected[key] for key in ('bytes', 'sha256')):
            raise ValueError('pinned source changed: ' + actual['path'])
        source_pins.append(actual)

    source = (HERE / 'precision_services.py').read_text(encoding='utf-8-sig')
    tree = ast.parse(source, filename='precision_services.py')
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    expected_signatures = {
        'log_exp_quad_interval': (['A', 'h', 'L', 'U'],
                                 ['absolute_log_error_target', 'max_evaluations']),
        'positive_quad_1d': (['f', 'lower', 'upper'],
                            ['absolute_error_target', 'relative_error_target', 'max_evaluations'])}
    checked = []
    signatures = {}
    for name, (positional, keywords) in expected_signatures.items():
        node = functions[name]
        arguments = node.args
        if ([a.arg for a in arguments.args] != positional
                or [a.arg for a in arguments.kwonlyargs] != keywords
                or arguments.defaults or any(x is not None for x in arguments.kw_defaults)
                or arguments.vararg or arguments.kwarg or arguments.posonlyargs):
            raise ValueError('signature/default mismatch: ' + name)
        signatures[name] = {'positional': positional, 'keyword_only_required': keywords,
                            'line': node.lineno}
        returns = [r for r in ast.walk(node) if isinstance(r, ast.Return)
                   and isinstance(r.value, ast.Dict)]
        if len(returns) != 1:
            raise ValueError('receipt dictionary ambiguity: ' + name)
        keys = [ast.literal_eval(k) for k in returns[0].value.keys]
        expected_keys = ['service_id', 'status',
                         'log_value' if name == 'log_exp_quad_interval' else 'value',
                         'error_estimate', 'error_kind', 'converged', 'evaluations', 'method']
        if keys != expected_keys:
            raise ValueError('receipt key mismatch: ' + name)
        signatures[name]['receipt_keys'] = keys
        checked.append('exact signature and eight receipt keys: ' + name)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.extend(node.module + '.' + alias.name for alias in node.names)
    if sorted(imports) != ['fractions.Fraction', 'heapq', 'math']:
        raise ValueError('unexpected candidate import')
    forbidden_calls = {'open', 'eval', 'exec', 'compile', '__import__', 'input', 'breakpoint'}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in forbidden_calls:
                raise ValueError('forbidden candidate call: ' + node.func.id)
    for node in tree.body:
        if not isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                                 ast.ClassDef, ast.Assign, ast.Expr)):
            raise ValueError('unexpected module-level statement')
        if isinstance(node, ast.Expr) and not isinstance(node.value, ast.Constant):
            raise ValueError('module-level expression is not documentation')
        if isinstance(node, ast.Assign) and any(isinstance(n, ast.Call) for n in ast.walk(node)):
            raise ValueError('module-level call in assignment')
    checked.extend(['stdlib import allowlist', 'no forbidden direct I/O/evaluation builtin',
                    'no module-level candidate execution call'])
    constants = {target.id: ast.literal_eval(node.value) for node in tree.body
                 if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                 for target in node.targets if isinstance(target, ast.Name)}

    samples = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == '_Samples')
    at = next(n for n in samples.body if isinstance(n, ast.FunctionDef) and n.name == 'at')
    direct_callback_calls = [n for n in ast.walk(at) if isinstance(n, ast.Call)
                            and isinstance(n.func, ast.Attribute) and n.func.attr == 'callback']
    if len(direct_callback_calls) != 1:
        raise ValueError('callback call-site ambiguity')
    protected_callbacks = [n for guard in ast.walk(at) if isinstance(guard, ast.Try)
                           for n in ast.walk(guard) if n in direct_callback_calls]
    if protected_callbacks:
        raise ValueError('callback exception unexpectedly intercepted')
    callback_statement = next(i for i, n in enumerate(at.body)
                              if direct_callback_calls[0] in list(ast.walk(n)))
    counter = at.body[callback_statement - 1]
    if not (isinstance(counter, ast.AugAssign) and isinstance(counter.op, ast.Add)
            and ast.unparse(counter.target) == 'self.count'
            and ast.literal_eval(counter.value) == 1):
        raise ValueError('callback count must increment immediately before call')
    checked.append('single callback call site, counted before call and outside try/except')

    inherited_contract = json.loads(Path(source_pins[3]['path']).read_text(encoding='utf-8-sig'))
    inventory_path = ROOT / 'f9_engine_import_closure_repair_preparation' / 'RUNTIME_INVENTORY.json'
    inventory_pin = pin(inventory_path)
    inventory = json.loads(inventory_path.read_text(encoding='utf-8-sig'))
    recorded_paths = {item['path']: item for item in inventory['pins']}
    selected_paths = ['/usr/bin/python3.12', '/usr/lib/python3.12/heapq.py',
                      '/usr/lib/python3.12/fractions.py', '/usr/lib/python3.12/numbers.py',
                      '/usr/lib/python3.12/decimal.py']
    recorded_selection = [{'path': path, 'pin': recorded_paths.get(path),
                           'status': 'RECORDED_NOT_REHASHED' if path in recorded_paths else 'NOT_IN_SNAPSHOT'}
                          for path in selected_paths]
    for item in inventory['pins']:
        basename = item['path'].rsplit('/', 1)[-1]
        if basename.startswith(('math.', '_heapq.', '_decimal.')) and basename.endswith('.so'):
            recorded_selection.append({'path': item['path'], 'pin': item,
                                       'status': 'RECORDED_NOT_REHASHED'})
    win_paths = [Path(sys.executable), Path(sys.base_prefix) / 'Lib' / 'heapq.py',
                 Path(sys.base_prefix) / 'Lib' / 'fractions.py']
    runtime_metadata = {
        'schema': 'F9_PRECISION_STATIC_RUNTIME_METADATA_V1', 'created_utc': started,
        'metadata_process': {'executable': sys.executable, 'version': sys.version,
                             'flags': {'isolated': sys.flags.isolated, 'no_site': sys.flags.no_site,
                                       'dont_write_bytecode': sys.dont_write_bytecode},
                             'files_hashed_read_only': [pin(path) for path in win_paths]},
        'intended_runtime': {'interpreter': inventory['interpreter'],
                             'interpreter_target': inventory['interpreter_target'],
                             'inventory_pin': inventory_pin,
                             'inventory_pin_count': len(inventory['pins']),
                             'selected_recorded_pins': recorded_selection,
                             'runtime_not_started': True,
                             'not_a_complete_transitive_import_closure': True,
                             'rehash_loaded_runtime_required_by_future_caller': True},
        'candidate_imported': False, 'numerical_dependencies_imported': False,
        'limitation': 'Windows metadata execution only. Existing Linux pins are cited records, not freshly measured Linux files or dynamic qualification.'}
    write_json('RUNTIME_METADATA.json', runtime_metadata)
    write_json('CONTRATO_SERVICOS.json', {
        'schema': 'F9_PRECISION_SERVICES_PREPARATION_V1', 'request_id': REQUEST_ID,
        'status': 'PREPARATION_ONLY_NOT_NUMERICALLY_QUALIFIED',
        'module': pin(HERE / 'precision_services.py'), 'signatures': signatures,
        'service_ids': {k: constants[k] for k in ('LOG_SERVICE_ID', 'QUAD_SERVICE_ID')},
        'inherited_contract': source_pins[3],
        'inherited_service_contract': inherited_contract['services'],
        'inherited_scope': inherited_contract['scope'],
        'receipt_status': 'ENGINEERING_ESTIMATE',
        'error_kinds': ['ESTIMATED_NOT_CERTIFIED', 'UNASSESSED'],
        'minimum_budget': {'positive_quad_1d': 17, 'window_per_nonempty_side': 5},
        'maximum_budget_schema_cap': 1000000,
        'algorithm': 'shared positive adaptive Simpson; exact-float rational recentering, localized monotone sides and analytic tail envelope for quadratic window',
        'unbounded_errors': ['generic missed peaks', 'backend and theory errors',
                             'rounding without outward interval arithmetic'],
        'authorization': False, 'claim': False,
        'numerical_tests': 0, 'candidate_imports': 0, 'observed_reads': 0})
    write_json('SOURCE_LINEAGE.json', {
        'schema': 'F9_PRECISION_SOURCE_LINEAGE_V1', 'request_id': REQUEST_ID,
        'request': request_pin, 'required_sources_verified_now': source_pins,
        'additional_read_only_runtime_record': inventory_pin,
        'scope': 'pure implementation of two injected services; no source package modified',
        'independent_review': 'PENDING', 'df482_review_reconciliation': 'REQUIRED_BEFORE_CONSUMPTION'})
    # Recheck all immutable inputs after AST/metadata work, before claiming preservation.
    for original in [request_pin, *source_pins, inventory_pin]:
        if pin(original['path']) != original:
            raise ValueError('source changed during packaging: ' + original['path'])
    receipt = {
        'schema': 'F9_PRECISION_STATIC_PREPARATION_RECEIPT_V1',
        'request_id': REQUEST_ID, 'created_utc': started,
        'status': 'STATIC_CHECKS_PASSED_NOT_NUMERICALLY_QUALIFIED',
        'scope_of_checks': checked,
        'module_pin': pin(HERE / 'precision_services.py'),
        'audit_script_pin': pin(Path(__file__).resolve()),
        'source_pins_verified_and_preserved': len(source_pins),
        'candidate_imports': 0, 'numerical_controls': 0, 'solver_calls': 0,
        'observed_reads': 0, 'wsl_children': 0, 'provider_calls': 0,
        'authorization_files_created': False, 'claim_files_created': False,
        'independent_review': 'PENDING',
        'limits': ['AST agreement is not dynamic behavior verification or numerical accuracy',
                   'Engineering estimates are not certified global error bounds',
                   'Existing MM/V1 conditionality and all scientific gates unchanged']}
    write_json('STATIC_PREPARATION_RECEIPT.json', receipt)
    members = ['precision_services.py', 'API_CONTRATO.md', 'DERIVACAO.md', 'prepare_static.py',
               'CONTRATO_SERVICOS.json', 'RUNTIME_METADATA.json', 'SOURCE_LINEAGE.json',
               'STATIC_PREPARATION_RECEIPT.json']
    write_json('MANIFESTO_PREPARACAO.json', {
        'schema': 'F9_PRECISION_PREPARATION_MANIFEST_V1', 'request_id': REQUEST_ID,
        'created_utc': started, 'status': 'PREPARATION_ONLY_NO_AUTHORIZATION',
        'members': [pin(HERE / name) for name in members],
        'immediate_byte_backups': [pin(path) for path in sorted(HERE.glob('*.bak_*'))],
        'excluded_operational_files': ['MANIFESTO_PREPARACAO.json', 'RECIBO_COORDENACAO.json'],
        'no_import_no_numerical_execution': True})
    manifest_path = HERE / 'MANIFESTO_PREPARACAO.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for member in manifest['members'] + manifest['immediate_byte_backups']:
        if pin(member['path']) != member:
            raise ValueError('manifest member mismatch')
    print(json.dumps({'request_id': REQUEST_ID, 'manifest': pin(manifest_path),
                      'module': pin(HERE / 'precision_services.py'),
                      'static_checks': len(checked), 'members': len(members),
                      'status': receipt['status']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
