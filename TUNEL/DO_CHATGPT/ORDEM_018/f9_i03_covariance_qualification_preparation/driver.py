"""One future supervised I03 covariance-join control. Preparation is not authorization."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import types
import uuid

ROOT=Path(__file__).resolve().parent
RID='27c6d5e9-df9f-4566-bd5d-4857683936d8'
UNIT='I03_COVARIANCE_CONSUMER_JOIN'

def need(ok,label):
    if not ok: raise RuntimeError(label)

def sha(raw): return hashlib.sha256(raw).hexdigest()

def encode(doc): return (json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def read(path):
    b=path.read_bytes(); return json.loads(b),b

def checked(rec):
    b=Path(rec['path']).read_bytes()
    need(len(b)==rec['bytes'] and sha(b)==rec['sha256'],'PIN_MISMATCH:'+rec['path'])
    return b

def exclusive(path,doc):
    b=encode(doc)
    fd=os.open(str(path),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,'wb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    need(path.read_bytes()==b,'EXCLUSIVE_WRITE_FAILED')
    return sha(b)

def new_json(path,doc):
    need(not path.exists(),'NO_OVERWRITE:'+str(path))
    tmp=path.with_name(path.name+'.tmp')
    digest=exclusive(tmp,doc)
    need(not path.exists(),'TARGET_ALREADY_EXISTS')
    os.replace(tmp,path)
    need(sha(path.read_bytes())==digest,'READBACK_FAILED')
    return digest

def validate(decision_sha):
    need(ROOT.name=='f9_i03_covariance_qualification_preparation','FIXED_ROOT_NAME')
    identity,_=read(ROOT/'IDENTIDADE_PREPARACAO.json')
    need(identity['request_id']==RID,'IDENTITY')
    manifest,mb=read(ROOT/'MANIFESTO_PREPARACAO.json')
    need(manifest['request_id']==RID and manifest['unit']==UNIT,'MANIFEST_ID')
    need(manifest['status']=='PREPARATION_ONLY_PENDING_INDEPENDENT_REVIEW_AND_ROOT_DECISION','MANIFEST_STATUS')
    decision,db=read(ROOT/'ROOT_DECISION.json')
    need(sha(db)==decision_sha,'DECISION_SHA')
    need(set(decision)=={'schema','request_id','unit','authorize_single_execution','manifest_sha256','review_reference','scope'},'DECISION_FIELDS')
    need(decision['schema']=='I03_COVARIANCE_ROOT_DECISION_V1' and decision['request_id']==RID and decision['unit']==UNIT
        and decision['authorize_single_execution'] is True and decision['manifest_sha256']==sha(mb)
        and decision['scope']=='SIX_SYNTHETIC_COVARIANCE_JOIN_CASES_ONLY','ROOT_DECISION_REQUIRED')
    rr=decision['review_reference']
    need(type(rr) is dict and set(rr)=={'id','sha256'} and isinstance(rr['id'],str) and rr['id']
         and isinstance(rr['sha256'],str) and len(rr['sha256'])==64
         and all(c in '0123456789abcdef' for c in rr['sha256']),'INDEPENDENT_REVIEW')
    names=[]
    for rec in manifest['members']:
        p=Path(rec['path']).resolve()
        need(p.parent==ROOT and p.name not in names,'MANIFEST_PATH');names.append(p.name);checked(rec)
    need({'driver.py','cases.py','CONTROL_CONTRACT.json','SOURCE_LINEAGE.json','RUNTIME_INVENTORY.json',
          'STATIC_PREPARATION_RECEIPT.json','REFERENCIAS_E_COMANDO.md'}<=set(names),'MANIFEST_MEMBERS')
    contract,_=read(ROOT/'CONTROL_CONTRACT.json')
    need(contract['request_id']==RID and contract['case_order']==['V01','V02','V03','V04','V05','V06'],'CONTRACT_SCOPE')
    lineage=json.loads(checked(contract['lineage']))
    runtime=json.loads(checked(contract['runtime']))
    need(sys.version_info[:2]==(3,12) and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'PY312_-I_-S_-B_REQUIRED')
    need(Path(sys.executable).resolve()==Path(runtime['interpreter']['path']).resolve(),'INTERPRETER_IDENTITY')
    checked(runtime['interpreter'])
    for rec in list(contract['sources'].values())+lineage['inherited']:checked(rec)
    for rec in runtime['files']: checked(rec)
    return contract,lineage,runtime,sha(mb),decision_sha

def load_module(name,rec,attestation):
    data=checked(rec); module=types.ModuleType(name)
    module.__file__=rec['path'];sys.modules[name]=module
    code=compile(data,rec['path'],'exec',dont_inherit=True,optimize=0)
    exec(code,module.__dict__)
    need(sha(Path(rec['path']).read_bytes())==rec['sha256'],'SOURCE_CHANGED_WHILE_LOADING')
    attestation[name]={'source':rec,'loader':'compile exact checked bytes, optimize=0; no pycache',
                       'module_file':module.__file__,'cross_process_marshal_identity_claimed':False}
    return module

def audit_loaded(runtime):
    allowed={str(Path(r['path']).resolve()).casefold():r for r in runtime['files']}
    loaded=[]
    for name,module in sorted(sys.modules.items()):
        if not name.startswith('numpy'):continue
        filename=getattr(module,'__file__',None)
        need(filename is not None,'NUMPY_MODULE_WITHOUT_ORIGIN:'+name)
        p=Path(filename).resolve()
        need(str(p).casefold() in allowed,'UNPINNED_NUMPY_MODULE:'+name)
        rec=allowed[str(p).casefold()];checked(rec)
        loaded.append({'module':name,'path':str(p),'sha256':rec['sha256']})
    need(bool(loaded),'NUMPY_NOT_LOADED')
    return {'python_numpy_module_origins':loaded,
            'native_dependency_closure':'NOT_FULLY_ESTABLISHED; numpy.libs bytes pinned, Windows system DLLs not pinned'}

def worker(args):
    import ast
    contract,lineage,runtime,msha,dsha=validate(args.decision_sha256)
    out=ROOT/'execution_once';claim,_=read(ROOT/'RUN_CLAIM.json')
    need(claim['nonce']==args.nonce and claim['supervisor_pid']==os.getppid() and claim['request_id']==RID,'WORKER_PARENT_CLAIM')
    need(claim['manifest_sha256']==msha and claim['decision_sha256']==dsha,'WORKER_CLAIM_PINS')
    exclusive(out/'WORKER_STARTED.json',{'request_id':RID,'pid':os.getpid(),'ppid':os.getppid(),'nonce':args.nonce})
    start=time.monotonic();deadline=start+contract['budgets']['worker_cooperative_seconds']
    need(not any(n=='numpy' or n.startswith('numpy.') for n in sys.modules),'EARLY_NUMPY_IMPORT')
    sys.path.append(runtime['site'])
    dll_handle=os.add_dll_directory(str(Path(runtime['site'])/'numpy.libs'))
    attestation={}
    try:
        import numpy as np
        need(np.__version__==runtime['numpy_version_metadata'],'NUMPY_VERSION')
        need(Path(np.__file__).resolve()==Path(runtime['site'])/'numpy/__init__.py','NUMPY_LOCATION')
        sources=contract['sources']
        support=load_module('singular_gaussian_v2',sources['support'],attestation)
        linear=load_module('linear_gaussian',sources['backend'],attestation)
        consumer=load_module('f9_i03_consumer',sources['consumer'],attestation)
        builder=load_module('f9_i03_builder',sources['builder'],attestation)
        helpers=load_module('f9_i03_fixture_helpers',sources['helpers'],attestation)
        # Reuse the exact original callable body without importing its old main
        # module, sys.path side effect, audit_inputs or historical error inputs.
        prim=types.ModuleType('f9_stellar_primitive');prim.__file__=sources['primitive']['path'];prim.np=np
        sys.modules[prim.__name__]=prim
        tree=ast.parse(checked(sources['primitive']),filename=prim.__file__)
        definitions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='block_correlation']
        need(len(definitions)==1 and not definitions[0].decorator_list,'PRIMITIVE_AST_SELECTION')
        projection=ast.Module(body=definitions,type_ignores=[])
        exec(compile(projection,prim.__file__,'exec',dont_inherit=True,optimize=0),prim.__dict__)
        need(prim.block_correlation.__globals__['np'] is np and linear.np is np and support.np is np
             and linear.SupportGaussian is support.SupportGaussian,'INJECTED_RUNTIME_BINDINGS')
        attestation[prim.__name__]={'source':sources['primitive'],'loader':'AST projection of original block_correlation only; original line numbers retained',
              'first_line':definitions[0].lineno,'last_line':definitions[0].end_lineno,
              'original_top_level_executed':False,'original_main_executed':False,'numpy_global_identity':True}
        manifest,_=read(ROOT/'MANIFESTO_PREPARACAO.json')
        case_pin=next(r for r in manifest['members'] if Path(r['path']).name=='cases.py')
        cases=load_module('f9_i03_cases',case_pin,attestation)
        need(builder.REQUEST_ID=='f200dee1-0ecf-4a51-9b38-4c32d7eb0696'
             and consumer.REQUEST_ID=='a9874f79-9d71-48f5-824c-d51d6d819534','CANDIDATE_IDENTITIES')
        need(builder.METADATA_SHA256==sources['metadata']['sha256'],'BUILDER_METADATA_IDENTITY')
        meta=json.loads(checked(sources['metadata']));layout=json.loads(checked(sources['layout']));design=json.loads(checked(sources['design']))
        new_json(out/'LOADED_SOURCE_ATTESTATION.json',{'request_id':RID,'python_version':sys.version,
             'sources':attestation,'runtime_inventory_sha256':contract['runtime']['sha256'],
             'numpy_import':audit_loaded(runtime),'cross_process_marshal_identity_claimed':False,
             'helper_scope':['structure_from_documents','make_packet','serialization helpers'],'old_run_called':False})
        def emit(name,record):
            need(time.monotonic()<deadline,'COOPERATIVE_DEADLINE')
            need(name in {c+s for c in contract['case_order'] for s in ('_STARTED','_RESULT')},'OUTPUT_NAME')
            return new_json(out/(name+'.json'),record)
        result=cases.run(np,builder,prim.block_correlation,consumer,linear.FlatNuisanceGaussian,helpers,
            contract,meta,layout,design,{'artifact_sha256':contract['runtime']['sha256'],
            'clause':RID+'/runtime-bytes-rechecked','status':'SYNTHETIC_FIXTURE'},emit,deadline)
        need(result['status']=='PASS' and len(result['cases'])==6,'CASE_COMPLETENESS')
        for rec in list(contract['sources'].values())+lineage['inherited']:checked(rec)
        new_json(out/'LOADED_ORIGINS_AFTER.json',audit_loaded(runtime))
        result.update(manifest_sha256=msha,decision_sha256=dsha,worker_seconds=time.monotonic()-start)
        need(time.monotonic()<deadline,'WORKER_DEADLINE_AT_COMMIT')
        new_json(out/'RESULT.json',result)
    finally:dll_handle.close()


def fail(out,exc,detail=None):
    if not out.exists():return
    try:
        if not (out/'FAILURE.json').exists():
            new_json(out/'FAILURE.json',{'request_id':RID,'status':'FAIL','type':type(exc).__name__,
                  'detail':str(exc)[:4000],'extra':detail,'retry_allowed':False})
    except BaseException: pass

def supervise(args,start):
    contract,lineage,runtime,msha,dsha=validate(args.decision_sha256)
    need(time.monotonic()-start<15,'PRECLAIM_VALIDATION_TIME_EXCEEDED')
    out=ROOT/'execution_once'
    need(not out.exists(),'OUTPUT_EXISTS_NO_RETRY')
    nonce=str(uuid.uuid4())
    exclusive(ROOT/'RUN_CLAIM.json',{'request_id':RID,'unit':UNIT,'manifest_sha256':msha,'decision_sha256':dsha,
       'nonce':nonce,'supervisor_pid':os.getpid(),'retry_allowed':False})
    out.mkdir(exist_ok=False)
    child=None
    try:
        command=[runtime['interpreter']['path'],'-I','-S','-B','-X','utf8',str(ROOT/'driver.py'),
                 '--decision-sha256',dsha,'--worker','--nonce',nonce]
        env=os.environ.copy()
        for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[key]='1'
        env['PYTHONDONTWRITEBYTECODE']='1'
        with (out/'stdout.log').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:
            child=subprocess.Popen(command,cwd=str(ROOT),stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                 shell=False,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
            new_json(out/'CHILD_IDENTITY.json',{'pid':child.pid,'supervisor_pid':os.getpid(),'nonce':nonce,'command':command})
            child.wait(timeout=contract['budgets']['wait_seconds'])
        need(child.returncode==0,'WORKER_EXIT:'+str(child.returncode))
        need(not (out/'FAILURE.json').exists(),'FAILURE_PRESENT')
        for name in ('stdout.log','stderr.log'):
            need((out/name).stat().st_size<=contract['budgets']['output_acceptance_bytes_per_stream'],'STREAM_ACCEPTANCE_CAP')
        result,rbytes=read(out/'RESULT.json')
        need(result['status']=='PASS' and result['request_id']==RID and result['manifest_sha256']==msha and result['decision_sha256']==dsha,'RESULT_PINS')
        need([c['case'] for c in result['cases']]==contract['case_order'] and all(c['status']=='PASS' for c in result['cases']),'ALL_CASES_REQUIRED')
        for case in contract['case_order']:
            saved,_=read(out/(case+'_RESULT.json')); need(saved==next(c for c in result['cases'] if c['case']==case),'CASE_READBACK')
            need((out/(case+'_STARTED.json')).exists(),'MISSING_CASE_START')
        validate(dsha) # source/runtime inventory still unchanged, after child
        elapsed=time.monotonic()-start
        need(elapsed<contract['budgets']['seconds_nominal'],'NOMINAL_TOTAL_TIME_EXCEEDED')
        terminal={'request_id':RID,'unit':UNIT,'status':'PASS','manifest_sha256':msha,'decision_sha256':dsha,
                  'result_sha256':sha(rbytes),'worker_exit':child.returncode,'seconds_before_terminal_io':elapsed,
                  'acceptance_requires_external_supervisor_exit_zero':True,'physical_sigma':None}
        thash=new_json(out/'TERMINAL_RECEIPT.json',terminal)
        need(time.monotonic()-start<contract['budgets']['seconds_nominal'],'FINAL_TIME_EXCEEDED')
        print(json.dumps({'request_id':RID,'status':'PASS','terminal_sha256':thash}))
    except BaseException as exc:
        extra=None
        if child is not None and child.poll() is None:
            child.kill()
            try: child.wait(timeout=5)
            except subprocess.TimeoutExpired:extra='CHILD_REAP_UNCERTAIN'
        fail(out,exc,extra)
        raise

def main():
    start=time.monotonic();parser=argparse.ArgumentParser()
    parser.add_argument('--decision-sha256',required=True)
    parser.add_argument('--worker',action='store_true');parser.add_argument('--nonce')
    args=parser.parse_args()
    try:
        if args.worker:worker(args)
        else:supervise(args,start)
    except BaseException as exc:
        fail(ROOT/'execution_once',exc)
        raise

if __name__=='__main__':main()
