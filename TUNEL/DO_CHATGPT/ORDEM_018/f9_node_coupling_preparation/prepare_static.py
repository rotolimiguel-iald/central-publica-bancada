"""Prepare source pins, API metadata and AST evidence only. No candidate imports."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUEST = ROOT / 'F9_NODE_COUPLING_PREPARATION_REQUEST.json'
REQUEST_ID = '1fe78df6-efb2-4c57-93bd-499ad85d8b15'


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write(name, data):
    path = (HERE / name).resolve()
    if path.parent != HERE or not data:
        raise ValueError('invalid preparation output')
    if path.exists():
        old = path.read_bytes()
        if old == data:
            return
        backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:
            stream.write(old)
        if backup.read_bytes() != old:
            raise ValueError('backup byte mismatch')
    temporary = path.with_name(path.name + '.tmp_' + str(os.getpid()))
    with temporary.open('xb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    if temporary.read_bytes() != data:
        raise ValueError('temporary mismatch')
    os.replace(temporary, path)
    if path.read_bytes() != data:
        raise ValueError('output mismatch')


def save(name, doc):
    write(name, (json.dumps(doc, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def literal(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError('literal assignment not found: ' + name)


def main():
    request_pin = pin(REQUEST)
    if request_pin['bytes'] != 7063 or request_pin['sha256'] != '14a68f1002150f4e9a0ced510e5601663e4ba0c7d9037dbce8e0f1fadf7b66e0':
        raise ValueError('request changed')
    request = json.loads(REQUEST.read_text(encoding='utf-8-sig'))
    if request['request_id'] != REQUEST_ID or Path(request['output_folder']).resolve() != HERE:
        raise ValueError('request identity/folder')
    identity_path = HERE / 'PREPARATION_IDENTITY.json'
    identity_pin = pin(identity_path)
    identity = json.loads(identity_path.read_text(encoding='utf-8-sig'))
    if identity['request_id'] != REQUEST_ID or identity['request'] != request_pin:
        raise ValueError('pre-code preparation identity missing or wrong')
    aliases = ['dependency_board', 'assembler', 'consumer', 'consumer_contract', 'prior',
               'prior_contract', 'precision', 'theta', 'profile', 'layout', 'design',
               'precision_theta_review', 'background_execution_review']
    if len(aliases) != len(request['sources']):
        raise ValueError('source catalog length')
    sources = {}
    for name, expected in zip(aliases, request['sources']):
        actual = pin(expected['path'])
        if any(actual[k] != expected[k] for k in ('bytes', 'sha256')):
            raise ValueError('frozen source changed: ' + actual['path'])
        sources[name] = actual
    review_path = ROOT / 'RECIBO_ROOT_REVISAO_PERFIS_F9.json'
    review_pin = pin(review_path)
    if review_pin['bytes'] != 4567 or review_pin['sha256'] != '5cd2edb8192b6db76e6998d8c12f6003db54b0d182b92852f0933a33409e073e':
        raise ValueError('profile review update changed')
    sources['profile_review'] = review_pin
    sources['supplier_receipt_schema_reference'] = pin(ROOT / 'f9_engine_import_closure_repair_preparation' / 'worker.py')
    assembler_tree = ast.parse(Path(sources['assembler']['path']).read_text(encoding='utf-8-sig'))
    expected_engine = literal(assembler_tree, 'SOURCE_PINS')['background_engine']
    sources['background_engine_reference'] = pin(expected_engine['path'])
    if sources['background_engine_reference'] != expected_engine:
        raise ValueError('engine reference changed')
    path = HERE / 'node_adapter.py'
    source = path.read_text(encoding='utf-8-sig')
    pins = literal(ast.parse(source), 'SOURCE_PINS')
    if pins not in ({}, sources):
        raise ValueError('nonempty pins differ; silent repin prohibited')
    if not pins:
        start, end = '# BEGIN SOURCE PINS', '# END SOURCE PINS'
        if source.count(start) != 1 or source.count(end) != 1:
            raise ValueError('pin markers')
        prefix, rest = source.split(start)
        _, suffix = rest.split(end)
        write('node_adapter.py', (prefix + start + '\nSOURCE_PINS = ' + repr(sources) + '\n' + end + suffix).encode('utf-8'))
    trees = {name: ast.parse((HERE / name).read_text(encoding='utf-8-sig'), filename=name)
             for name in ('node_adapter.py', 'durable_nodes.py')}
    core, store = trees['node_adapter.py'], trees['durable_nodes.py']
    if literal(core, 'SOURCE_PINS') != sources:
        raise ValueError('candidate source pins')
    calls = {name: [node for node in ast.walk(tree) if isinstance(node, ast.Call)] for name, tree in trees.items()}
    api = {}
    for filename, tree in trees.items():
        if any(isinstance(n, ast.While) for n in ast.walk(tree)):
            raise ValueError('unexpected retry/iteration loop')
        for node in tree.body:
            if not isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.Expr, ast.ClassDef, ast.FunctionDef)):
                raise ValueError('module-level execution statement')
            if isinstance(node, ast.Expr) and not isinstance(node.value, ast.Constant):
                raise ValueError('module-level call')
            if isinstance(node, ast.Assign) and any(isinstance(n, ast.Call) for n in ast.walk(node)):
                raise ValueError('module-level call in assignment')
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(a.name.split('.')[0] in
                    ('subprocess','socket','requests','numpy','scipy','camb','importlib') for a in node.names):
                raise ValueError('forbidden direct dependency')
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            api[cls.name] = {n.name: {'positional': [a.arg for a in n.args.args],
                                    'keyword_only': [a.arg for a in n.args.kwonlyargs],
                                    'keyword_defaults': [None if d is None else ast.unparse(d) for d in n.args.kw_defaults],
                                    'line': n.lineno}
                             for n in cls.body if isinstance(n, ast.FunctionDef)}
        for call in calls[filename]:
            if isinstance(call.func, ast.Name) and call.func.id in ('eval','exec','compile','__import__','input'):
                raise ValueError('dynamic execution forbidden')
            if isinstance(call.func, ast.Attribute) and call.func.attr in ('run','get_background','prediction_worker','minimize','svd','pinv'):
                raise ValueError('unexpected solver/integration launcher call')
    core_calls = [ast.unparse(n.func) for n in calls['node_adapter.py']]
    if core_calls.count('self.a.assemble_five') != 1 or core_calls.count('self.p.integrate_at_fixed_theta') != 1:
        raise ValueError('core must reuse each existing API once per computation')
    if core_calls.count('self.t.canonical_conditional_sha256') != 1 or 'self._validator()._accept' not in core_calls:
        raise ValueError('typed conditional hash/envelope validation reuse missing')
    store_calls = [n for n in calls['durable_nodes.py'] if ast.unparse(n.func) == 'self.supplier']
    if len(store_calls) != 1:
        raise ValueError('exactly one supplier call site required')
    supplier_line = store_calls[0].lineno
    guards = {ast.literal_eval(n.args[0]): n.lineno for n in calls['durable_nodes.py']
              if ast.unparse(n.func) == 'self._guard'}
    if not (guards['NODE_ACCESS'] < guards['BACKGROUND_EXECUTION'] < supplier_line < guards['BACKGROUND_ACCEPTANCE']):
        raise ValueError('guard ordering')
    callback_cls = next(n for n in store.body if isinstance(n, ast.ClassDef) and n.name == 'DurableNodeCallback')
    callback = next(n for n in callback_cls.body if isinstance(n, ast.FunctionDef) and n.name == '__call__')
    cache_branch = next(n for n in callback.body if isinstance(n, ast.If)
                        and ast.unparse(n.test) == "not node['created']")
    cache_calls = [ast.unparse(n.func) for n in ast.walk(cache_branch) if isinstance(n, ast.Call)]
    if 'self.supplier' in cache_calls or 'ctx.compute' in cache_calls or 'store.acquire' in cache_calls:
        raise ValueError('cache must not launch new computation or claim')
    attributes = {n.attr for n in ast.walk(store) if isinstance(n, ast.Attribute)}
    if not {'O_EXCL','O_NOFOLLOW','O_DIRECTORY','fsync','link'} <= attributes:
        raise ValueError('durable exclusive publication primitives missing')
    if any(n.attr in ('replace','rename','unlink','remove') for n in ast.walk(store) if isinstance(n, ast.Attribute)):
        raise ValueError('runtime store must not overwrite/remove history')
    checks = ['preparation identity exists and is linked to exact request before code packaging',
              'thirteen requested source pins plus three explicit documentary/receipt references verified',
              'AST-only inspection: no imports/constructors/callback execution of candidates',
              'one assemble_five and one integrate_at_fixed_theta call site, shared context',
              'existing typed conditional digest and exact ThetaIntegrator._accept reused',
              'one supplier call site with access/execution/terminal-acceptance guards in order',
              'cache branch has no supplier/computation/new-claim call',
              'exclusive claim, fsync and no-overwrite publication primitives present; no unlink/retry loop']
    save('CONTRATO_API.json', {
        'schema': 'F9_NODE_COUPLING_PREPARATION_CONTRACT_V1', 'request_id': REQUEST_ID,
        'status': 'PREPARATION_ONLY_NOT_EXECUTED', 'source_pins': sources, 'api': api,
        'callback_envelope_exact_keys': ['conditional_result','receipt'],
        'conditional_hash': 'theta_integrator.canonical_conditional_sha256',
        'supplier_result_exact_keys': ['packet_json','result_json','receipt_json'],
        'supplier_calls_per_owned_background_claim_maximum': 1,
        'cache_new_scientific_calls': 0,
        'receipt_current_usage': {'new': {'background_origin':'NEW_EXECUTION','background_calls_this_callback':1},
                                 'cache': {'background_origin':'VERIFIED_DURABLE_CACHE','background_calls_this_callback':0}},
        'original_successful_solver_receipt_counts': {'attempted':1,'returned':1},
        'guards': ['NODE_ACCESS','BACKGROUND_EXECUTION','BACKGROUND_ACCEPTANCE'],
        'guard_return': 'None after external checks or exception; no boolean authorization substitute',
        'profile': 'Explicit opt-in, reviewed I05, separate stored typed profile_json; no envelope extension',
        'durability_scope': 'qualified protected POSIX local filesystem only; actual filesystem/runtime qualification external',
        'uncertain_or_failed': 'terminal/no automatic retry, no rename, no zero likelihood fallback',
        'background_scope': 'theta/config/runtime/engine/protocol/supplier under same explicit execution scope, independent of scenario',
        'coupling_scope': 'node descriptor + coupling admission hash + theta plan hash',
        'runtime_controller_not_implemented': ['background supplier/executor','authorization and terminal-audit guard','global resource/ledger enforcement'],
        'scientific_claims_created_now': 0, 'candidate_imports':0, 'numerical_execution':0,
        'MM':'CONDITIONAL_UNRATIFIED','V1':'NOT_RATIFIED','AUTH':False,'CLAIM':False})
    save('SOURCE_LINEAGE.json', {
        'schema':'F9_NODE_COUPLING_LINEAGE_V1','request_id':REQUEST_ID,'request':request_pin,
        'pre_code_identity':identity_pin,'sources':sources,
        'scope':'thin local adapter plus separate durable store; no new Gaussian/physics/numerical solver',
        'profile_review_update':review_pin,'review_state':'INDEPENDENT_COUPLING_REVIEW_PENDING',
        'metadata_process':{'executable':pin(sys.executable),'version':sys.version,
                            'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,'dont_write_bytecode':sys.dont_write_bytecode}})
    for original in [request_pin,identity_pin,*sources.values()]:
        if pin(original['path']) != original:
            raise ValueError('input changed during packaging')
    save('STATIC_PREPARATION_RECEIPT.json', {
        'schema':'F9_NODE_COUPLING_STATIC_RECEIPT_V1','request_id':REQUEST_ID,
        'at':datetime.now(timezone.utc).isoformat(),'status':'STATIC_CHECKS_PASSED_NOT_RUNTIME_QUALIFIED',
        'checks':checks,'source_count_verified_and_preserved':len(sources),
        'module_pins':[pin(HERE/name) for name in trees], 'packaging_script':pin(Path(__file__).resolve()),
        'candidate_imports':0,'numerical_execution':0,'scientific_claims_created':0,
        'AUTH_created':False,'observed_reads':0,'WSL_children':0,'provider_calls':0,
        'claim_cache_store_instantiated':False,'independent_review':'PENDING',
        'limits':'AST order is not crash/concurrency/runtime testing; all external guards/supplier/resource qualifications remain required before consumption.'})
    members = ['PREPARATION_IDENTITY.json','node_adapter.py','durable_nodes.py','API_DERIVACAO.md',
               'prepare_static.py','CONTRATO_API.json','SOURCE_LINEAGE.json','STATIC_PREPARATION_RECEIPT.json']
    save('MANIFESTO_PREPARACAO.json', {'schema':'F9_NODE_COUPLING_MANIFEST_V1','request_id':REQUEST_ID,
        'status':'PREPARATION_ONLY_NO_AUTHORIZATION','members':[pin(HERE/name) for name in members],
        'immediate_byte_backups':[pin(p) for p in sorted(HERE.glob('*.bak_*'))],
        'excluded_operational_files':['MANIFESTO_PREPARACAO.json','RECIBO_COORDENACAO.json'],
        'no_runtime_or_scientific_consumption':True})
    manifest_path=HERE/'MANIFESTO_PREPARACAO.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for member in manifest['members']+manifest['immediate_byte_backups']:
        if pin(member['path']) != member:
            raise ValueError('member pin mismatch')
    print(json.dumps({'request_id':REQUEST_ID,'manifest':pin(manifest_path),'members':len(members),
        'sources_verified':len(sources),'checks':len(checks),'status':'STATIC_CHECKS_PASSED_NOT_RUNTIME_QUALIFIED'},ensure_ascii=False))


if __name__=='__main__':
    main()
