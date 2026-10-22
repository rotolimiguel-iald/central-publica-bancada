"""AST/byte-only packaging; never import or call scientific candidates."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUEST = ROOT / 'F9_AFFINE_PROFILE_PREPARATION_REQUEST.json'
REQUEST_ID = '4eea0cfb-0a3e-4b38-abcd-37bddbf5bbe3'


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write(name, data):
    path = (HERE / name).resolve()
    if path.parent != HERE:
        raise ValueError('output outside preparation folder')
    if path.exists():
        old = path.read_bytes()
        if old == data:
            return
        backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:
            stream.write(old)
        if backup.read_bytes() != old:
            raise ValueError('backup differs from original bytes')
    temporary = path.with_name(path.name + '.tmp_' + str(os.getpid()))
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if not data or temporary.read_bytes() != data:
        raise ValueError('temporary verification failed')
    os.replace(temporary, path)
    if path.read_bytes() != data:
        raise ValueError('output verification failed')


def write_json(name, value):
    write(name, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def literal_assignment(tree, name):
    nodes = [node for node in tree.body if isinstance(node, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)]
    if len(nodes) != 1:
        raise ValueError('ambiguous literal assignment: ' + name)
    return ast.literal_eval(nodes[0].value)


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    request_pin = pin(REQUEST)
    if request_pin['bytes'] != 4111 or request_pin['sha256'] != 'd6daaf8d5e14e46419a4e72323a36ab17799f76bb5d2fb7c5a12de04c1082453':
        raise ValueError('request changed')
    request = json.loads(REQUEST.read_text(encoding='utf-8-sig'))
    if request['request_id'] != REQUEST_ID or Path(request['output_folder']).resolve() != HERE:
        raise ValueError('request/folder mismatch')
    aliases = ['dependency_board', 'physical_prior', 'prior_derivation', 'prior_api',
               'consumer', 'consumer_api', 'prior_review', 'certificate_interface']
    if len(request['sources']) != len(aliases):
        raise ValueError('unexpected source list')
    sources = {}
    for name, expected in zip(aliases, request['sources']):
        actual = pin(expected['path'])
        if any(actual[key] != expected[key] for key in ('bytes', 'sha256')):
            raise ValueError('source changed: ' + actual['path'])
        sources[name] = actual
    consumer_tree = ast.parse(Path(sources['consumer']['path']).read_text(encoding='utf-8-sig'))
    inherited_pins = literal_assignment(consumer_tree, 'SOURCE_PINS')
    for name, upstream in (('linear_gaussian', 'linear_gaussian'), ('singular_gaussian', 'support')):
        actual = pin(inherited_pins[upstream]['path'])
        if actual != inherited_pins[upstream]:
            raise ValueError('backend dependency changed')
        sources[name] = actual
    candidate = HERE / 'affine_profile.py'
    source = candidate.read_text(encoding='utf-8-sig')
    begin, end = '# BEGIN SOURCE PINS', '# END SOURCE PINS'
    if source.count(begin) != 1 or source.count(end) != 1:
        raise ValueError('pin markers missing or ambiguous')
    existing_tree = ast.parse(source)
    existing_pins = literal_assignment(existing_tree, 'SOURCE_PINS')
    if existing_pins not in ({}, sources):
        raise ValueError('nonempty candidate pins disagree; do not silently repin')
    if not existing_pins:
        before, rest = source.split(begin)
        _, after = rest.split(end)
        source = before + begin + '\nSOURCE_PINS = ' + repr(sources) + '\n' + end + after
        write('affine_profile.py', source.encode('utf-8'))
    tree = ast.parse(candidate.read_text(encoding='utf-8-sig'), filename='affine_profile.py')
    if literal_assignment(tree, 'SOURCE_PINS') != sources:
        raise ValueError('literal dependency pins mismatch')
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    entry = functions['profile_at_fixed_theta']
    args = entry.args
    expected_pos = ['joint', 'assembly_json']
    expected_kw = ['assembly_sha256', 'background_json', 'consumer_module',
                   'physical_prior_module', 'caller_verification_reference']
    if ([a.arg for a in args.args] != expected_pos or [a.arg for a in args.kwonlyargs] != expected_kw
            or args.defaults or any(x is not None for x in args.kw_defaults)
            or args.vararg or args.kwarg or args.posonlyargs):
        raise ValueError('entry signature mismatch')
    imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    if len(imports) != 1 or not isinstance(imports[0], ast.Import) or [a.name for a in imports[0].names] != ['math']:
        raise ValueError('unexpected candidate imports')
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    call_names = [ast.unparse(n.func) for n in calls]
    forbidden_names = {'open', 'eval', 'exec', 'compile', '__import__', 'input', 'breakpoint'}
    forbidden_attrs = {'svd', 'pinv', 'inv', 'solve', 'minimize', 'integrate_at_fixed_theta',
                       'positive_quad_1d', 'log_exp_quad_interval', 'assemble_five'}
    for call in calls:
        if (isinstance(call.func, ast.Name) and call.func.id in forbidden_names
                or isinstance(call.func, ast.Attribute) and call.func.attr in forbidden_attrs):
            raise ValueError('forbidden candidate call: ' + ast.unparse(call.func))
    peak = [n for n in calls if isinstance(n.func, ast.Attribute) and n.func.attr == 'peak']
    if len(peak) != 1 or peak[0].args or peak[0].keywords:
        raise ValueError('likelihood profile must call peak without prior shift')
    if call_names.count('p._Curve') != 3 or call_names.count('joint.evaluate_five') != 1:
        raise ValueError('existing geometry/five-model reuse mismatch')
    if any(isinstance(n, (ast.Try, ast.While)) for n in ast.walk(tree)):
        raise ValueError('candidate must not hide failures or launch iterative search')
    cert_return = functions['_unavailable_certificates'].body[0]
    if not isinstance(cert_return, ast.Return):
        raise ValueError('certificate defaults not literal')
    certificates = ast.literal_eval(cert_return.value)
    if certificates['conditional_minimum'] != {'status': 'UNAVAILABLE', 'lower': None,
            'upper': None, 'certificate': None, 'verified': False}:
        raise ValueError('conditional certificate not unavailable')
    if certificates['global_theta_minimum'] != {'status': 'NOT_SEARCHED', 'estimate': None,
            'lower': None, 'upper': None, 'certificate': None, 'verified': False}:
        raise ValueError('global minimum claim present')
    final_return = entry.body[-1]
    if not isinstance(final_return, ast.Return) or not isinstance(final_return.value, ast.Dict):
        raise ValueError('entry output structure')
    output_nodes = {ast.literal_eval(k): v for k, v in zip(final_return.value.keys, final_return.value.values)}
    for name in ('global_minima', 'relative_evidence', 'lnB', 'p', 'sigma', 'verdict'):
        if ast.literal_eval(output_nodes[name]) is not None:
            raise ValueError('unavailable scientific output populated: ' + name)
    for name in ('global_theta_search_performed', 'physical_extra_priors_applied'):
        if ast.literal_eval(output_nodes[name]) is not False:
            raise ValueError('unexpected integration/search claim')
    checks = ['ten source pins verified, eight requested and two inherited backend files',
              'exact entry signature; caller injection and no implicit data reads',
              'only math imported; no direct I/O/dynamic import/solver/optimization calls',
              'three reused df482 curves and one a987 evaluate_five call site',
              'peak called without prior shift; no physical-prior integral calls',
              'no try/except fallback or iterative while search',
              'literal unavailable conditional/global certificates',
              'global minima/evidence/p/sigma/verdict unavailable and priors not applied']
    write_json('CONTRATO_API.json', {
        'schema': 'F9_AFFINE_PROFILE_PREPARATION_CONTRACT_V1', 'request_id': REQUEST_ID,
        'status': 'PREPARATION_ONLY_NOT_EXECUTED', 'module': pin(candidate),
        'entry': 'profile_at_fixed_theta', 'positional': expected_pos, 'keyword_only_required': expected_kw,
        'source_pins': sources, 'models': literal_assignment(tree, 'MODELS'),
        'theta_names': literal_assignment(tree, 'THETA_NAMES'),
        'theta_bounds': literal_assignment(tree, 'THETA_BOUNDS'),
        'dependency_fields': {'consumer': ['PreparedJoint', 'evaluate_five', '_np', '_engine', '_y',
                                          '_origin', '_structure', '_admission_sha256'],
                              'physical_prior': ['_Curve', 'peak', 'mean', 'log_likelihood',
                                                 'BETA_LIMITS', 'S_LIMITS', 'RD_LIMITS'],
                              'backend': ['residualize', 'support.evaluate', 'log_integral']},
        'minimum_formula': 'xref+clip(B/A,[lo-xref,hi-xref]); flat only if projected direction zero',
        'prior_shift_in_profile': False, 'H4_inverse': 's=expm1(-(ln10/5)*delta)',
        'H5_coordinate': 'x=1/rd_Mpc; physical rd=1/x; BAO indices3:16 only',
        'roundtrip_policy': 'evaluate mean at forward coordinate of returned physical point; retain difference from chosen affine vertex',
        'source_method_reuse': 'df482 has no exported curve factory; only its argument construction is repeated; _Curve/R/support/log-integral reused',
        'certificate_defaults': certificates, 'external_certificate_checker_implemented': False,
        'scope': 'engineering feasible profile estimates at fixed theta; no global minimum',
        'MM': 'CONDITIONAL_UNRATIFIED', 'numerical_controls': 0, 'candidate_imports': 0,
        'observed_reads': 0, 'solver_calls': 0, 'AUTH': False, 'CLAIM': False})
    write_json('SOURCE_LINEAGE.json', {
        'schema': 'F9_AFFINE_PROFILE_LINEAGE_V1', 'request_id': REQUEST_ID,
        'request': request_pin, 'sources_verified_now': sources,
        'prior_review': sources['prior_review'], 'independent_profile_review': 'PENDING',
        'frozen_sources_modified': False,
        'metadata_runtime': {'version': sys.version, 'executable': pin(sys.executable),
                             'isolated': sys.flags.isolated, 'no_site': sys.flags.no_site,
                             'dont_write_bytecode': sys.dont_write_bytecode},
        'runtime_note': 'Only Windows stdlib AST/hash packaging ran. No target runtime or injected scientific modules were loaded.'})
    for original in [request_pin, *sources.values()]:
        if pin(original['path']) != original:
            raise ValueError('source changed during packaging')
    write_json('STATIC_PREPARATION_RECEIPT.json', {
        'schema': 'F9_AFFINE_PROFILE_STATIC_RECEIPT_V1', 'request_id': REQUEST_ID,
        'at': timestamp, 'status': 'STATIC_CHECKS_PASSED_NOT_NUMERICALLY_QUALIFIED',
        'module': pin(candidate), 'packaging_script': pin(Path(__file__).resolve()),
        'checks': checks, 'source_count_verified_and_preserved': len(sources),
        'candidate_imports': 0, 'numerical_execution': 0, 'controls': 0, 'solver_calls': 0,
        'observed_data_reads': 0, 'WSL_children': 0, 'provider_calls': 0,
        'AUTH_or_CLAIM_created': False, 'independent_review': 'PENDING',
        'manual_static_notes': [
            'B/A profile distinguished from B-lambda prior-integrand maximum',
            'H4/H5 monotone inverse domains and float roundtrip explicitly retained',
            'direct projected norm avoids D-B^2/A cancellation; no new Gaussian solver',
            'legitimate off-support zero retains source residual diagnosis, not a failure substitute',
            'no q estimate is promoted to certified lower/upper or global minimum'],
        'limits': 'AST/source analysis does not establish dynamic behavior, numerical precision, loaded-object authenticity or physical model adequacy.'})
    members = ['affine_profile.py', 'prepare_static.py', 'DERIVACAO.md', 'API_CONTRATO.md',
               'CONTRATO_API.json', 'SOURCE_LINEAGE.json', 'STATIC_PREPARATION_RECEIPT.json']
    write_json('MANIFESTO_PREPARACAO.json', {
        'schema': 'F9_AFFINE_PROFILE_PREPARATION_MANIFEST_V1', 'request_id': REQUEST_ID,
        'at': timestamp, 'status': 'PREPARATION_ONLY_NO_AUTHORIZATION',
        'members': [pin(HERE / name) for name in members],
        'immediate_byte_backups': [pin(path) for path in sorted(HERE.glob('*.bak_*'))],
        'excluded_operational_files': ['MANIFESTO_PREPARACAO.json', 'RECIBO_COORDENACAO.json'],
        'no_import_no_numerical_execution': True})
    manifest_path = HERE / 'MANIFESTO_PREPARACAO.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for member in manifest['members'] + manifest['immediate_byte_backups']:
        if pin(member['path']) != member:
            raise ValueError('manifest pin mismatch')
    print(json.dumps({'request_id': REQUEST_ID, 'manifest': pin(manifest_path),
                      'module': pin(candidate), 'members': len(members), 'checks': len(checks),
                      'status': 'STATIC_CHECKS_PASSED_NOT_NUMERICALLY_QUALIFIED'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
