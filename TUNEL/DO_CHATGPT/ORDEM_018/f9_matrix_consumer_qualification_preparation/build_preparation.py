"""Metadata and AST only. Does not import a candidate, NumPy, or the bundle."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
BUNDLE = Path(r'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python')
RID = json.loads((ROOT/'IDENTIDADE_PREPARACAO.json').read_bytes())['request_id']

def pin(p):
    p = Path(p).resolve()
    raw = p.read_bytes()
    return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def write(name, doc):
    p = ROOT/name
    raw = (json.dumps(doc, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == raw and len(raw)>0
    os.replace(temp,p)
    assert p.read_bytes() == raw

def constants(path, wanted):
    tree = ast.parse(path.read_bytes(), filename=str(path))
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    out[target.id] = ast.literal_eval(node.value)
    assert set(out)==set(wanted)
    return out

def main():
    request=BASE/'F9_MATRIX_JOIN_PREPARATION_REQUEST.json'
    doc=json.loads(request.read_bytes())
    assert doc['request_id']=='29981416-d6fe-4d68-acff-46f88e8819fb'
    assert pin(doc['basis']['path'])==doc['basis']
    source_names={
      'consumer':'f9_likelihood_consumer_preparation/likelihood_consumer.py',
      'prior':'f9_physical_prior_preparation/physical_prior.py',
      'precision':'f9_precision_services_preparation/precision_services.py',
      'backend':'covariance_support/linear_gaussian.py',
      'support':'covariance_support/singular_gaussian_v2.py',
      'layout':'f9_structural_layout_preparation/LAYOUT_ESTRUTURAL_3CMB_13BAO.json',
      'design':'h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json'}
    sources={k:pin(BASE/v) for k,v in source_names.items()}
    cm=constants(Path(sources['consumer']['path']),['SOURCE_PINS','ASSEMBLY_SOURCE_PINS','STRUCTURAL_IDENTITY_PINS'])
    pm=constants(Path(sources['prior']['path']),['SOURCE_PINS'])
    fm=constants(Path(sources['precision']['path']),['LOG_SERVICE_ID','QUAD_SERVICE_ID'])
    inherited={}
    for group in (cm['SOURCE_PINS'],cm['ASSEMBLY_SOURCE_PINS'],pm['SOURCE_PINS']):
        for rec in group.values():
            assert pin(rec['path'])==rec
            inherited[rec['path']]=rec
    declarations={}
    for key in ('consumer','prior','precision','backend','support'):
        tree=ast.parse(Path(sources[key]['path']).read_bytes())
        declarations[key]=[{ 'name':n.name,'line':n.lineno,'kind':type(n).__name__}
                           for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
    site=BUNDLE/'Lib/site-packages'
    metadata=site/'numpy-2.3.5.dist-info/METADATA'
    wheel=site/'numpy-2.3.5.dist-info/WHEEL'
    assert 'Version: 2.3.5' in metadata.read_text(encoding='utf-8')
    assert 'cp312-cp312-win_amd64' in wheel.read_text(encoding='utf-8')
    files=set()
    for p in BUNDLE.iterdir():
        if p.is_file(): files.add(p)
    for folder in (BUNDLE/'DLLs',BUNDLE/'Lib'):
        for p in folder.rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts: continue
            if folder.name=='Lib' and 'site-packages' in p.relative_to(folder).parts: continue
            if p.suffix not in ('.pyc','.pyo'): files.add(p)
    for folder in (site/'numpy',site/'numpy.libs',site/'numpy-2.3.5.dist-info'):
        assert folder.is_dir(), str(folder)
        for p in folder.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.pyo'):
                files.add(p)
    assert not any(p.is_symlink() for p in files)
    runtime={
       'status':'BYTES_INVENTORIED_NOT_IMPORTED_OR_EXECUTED',
       'interpreter':pin(BUNDLE/'python.exe'), 'root':str(BUNDLE), 'site':str(site),
       'numpy_version_metadata':'2.3.5','abi_metadata':'cp312-cp312-win_amd64',
       'files':[pin(p) for p in sorted(files)],
       'excluded':['__pycache__','other site packages','Windows system DLL closure','OS loader state'],
       'library_loadability':'UNVERIFIED_UNTIL_DISTINCT_AUTHORIZED_EXECUTION',
       'metadata_collector_interpreter':pin(Path(os.sys.executable)),
       'bootstrap_python314_has_numpy':False,
       'search_scope':'C:/Python314 site-packages contains pip only; bundled runtime returned by load_workspace_dependencies inspected by bytes; no global absence claim',
       'wsl_alternative':'Existing /opt/lal_env receipt is historical; not launched or re-pinned here'}
    write('RUNTIME_INVENTORY.json',runtime)
    write('SOURCE_LINEAGE.json',dict(request_id=RID,parent_request=pin(request),basis=doc['basis'],
         direct=sources,inherited=list(inherited.values()),declarations=declarations,
         consumer_constants=cm,prior_constants=pm,precision_constants=fm))
    contract={
      'schema':'Q01_MATRIX_CONSUMER_PREPARATION_V1','request_id':RID,'unit':'Q01_MATRIX_CONSUMER_JOIN',
      'status':'PREPARATION_ONLY_PENDING_INDEPENDENT_REVIEW_AND_ROOT_DECISION',
      'sources':sources,'lineage':pin(ROOT/'SOURCE_LINEAGE.json'),'runtime':pin(ROOT/'RUNTIME_INVENTORY.json'),
      'case_order':['J01','J02','J03','J04','J05'],
      'scopes':['fixed original X and row layout','native Ty/TCTt/Torigin exactly once',
                'full support 283 and affine support 282','prepare_joint/evaluate_five/integrate_at_fixed_theta original bytes',
                'all five models and original full extra-prior domains at one synthetic theta'],
      'budgets':{'cases':5,'prepare_attempts':4,'backend_constructors':3,'evaluate_attempts':7,
                 'integration_calls':3,'curve_constructors':9,'real_precision_calls':6,
                 'service_evaluations':24586,'curve_log_calls':8200,'h5_reference_evaluations':1026,
                 'seconds_nominal':120,'worker_cooperative_seconds':80,'wait_seconds':90,
                 'output_acceptance_bytes_per_stream':131072,'max_reference_fraction_bits':16384},
      'precision':{'window_cap':4098,'quadrature_cap':4097,'absolute_log_error_target':1e-9,
                   'absolute_scaled_error_target':1e-10,'relative_scaled_error_target':1e-9},
      'acceptance':{'pointwise_log_absolute_tolerance':2e-7,'integrated_log_base_tolerance':1e-6,
                    'coefficient_absolute_tolerance':2e-6,'coefficient_relative_tolerance':2e-8,
                    'array_absolute_tolerance':2e-12,'array_relative_tolerance':2e-12,
                    'h5_reference_panels':512,'h5_reference_roundoff_allowance':5e-11,
                    'uniform_certificate':False},
      'decision_schema':{'schema':'Q01_MATRIX_CONSUMER_ROOT_DECISION_V1','request_id':RID,
        'unit':'Q01_MATRIX_CONSUMER_JOIN','authorize_single_execution':'FUTURE_BOOLEAN_NOT_AUTHORIZATION',
        'manifest_sha256':'FUTURE_HASH','review_reference':'FUTURE_REFERENCE',
        'scope':'FIVE_SYNTHETIC_MATRIX_JOIN_CASES_ONLY'},
      'resource_limit_scope':'Fixed shapes/callbacks and one child; nominal timeout. No hard RAM, disk or native-thread enforcement claimed.',
      'not_covered':['assembler or cosmological solver','actual observations or covariance','I02 guard/filesystem',
        'theta integration or entire Q01','Q02/Q03','uniform or interval accuracy','physical sigma',
        'cross-process marshal identity','complete Windows DLL security boundary']}
    write('CONTROL_CONTRACT.json',contract)
    for name in ('cases.py','driver.py','build_preparation.py'):
        ast.parse((ROOT/name).read_bytes(),filename=str(ROOT/name))
    for name in ('ROOT_DECISION.json','AUTH.json','CLAIM.json','RUN_CLAIM.json','execution_once'):
        assert not (ROOT/name).exists(),name
    # Read-back only; never run a case to populate this receipt.
    write('STATIC_PREPARATION_RECEIPT.json',dict(request_id=RID,status='AST_AND_BYTES_ONLY',
       imports_candidate=0,imports_numpy=0,numerical_execution=0,observed_reads=0,
       runtime_files=len(runtime['files']),runtime_bytes=sum(r['bytes'] for r in runtime['files']),
       direct_sources=len(sources),inherited_sources=len(inherited),
       case_count=5,checks=['parent/basis pins','inherited bytes','actual NumPy METADATA/WHEEL',
       'runtime hash inventory','AST parsing only','no decision/claim/output','sources unchanged'],
       review='PENDING',runtime_execution='NOT_AUTHORIZED'))
    for rec in list(sources.values())+list(inherited.values()): assert pin(rec['path'])==rec
    names=['IDENTIDADE_PREPARACAO.json','cases.py','driver.py','build_preparation.py',
           'CONTROL_CONTRACT.json','SOURCE_LINEAGE.json','RUNTIME_INVENTORY.json',
           'STATIC_PREPARATION_RECEIPT.json','REFERENCIAS_E_COMANDO.md']
    write('MANIFESTO_PREPARACAO.json',dict(request_id=RID,unit='Q01_MATRIX_CONSUMER_JOIN',
       status=contract['status'],members=[pin(ROOT/name) for name in names],
       backups=[pin(p) for p in sorted(ROOT.glob('*.bak_*'))],
       excludes=['MANIFESTO_PREPARACAO.json','RECIBO_COORDENACAO.json'],
       authorization_created=False,execution_created=False))
    print(json.dumps({'manifest':pin(ROOT/'MANIFESTO_PREPARACAO.json'),
                      'runtime_files':len(runtime['files']),'status':'PREPARATION_ONLY'}))

if __name__=='__main__': main()
