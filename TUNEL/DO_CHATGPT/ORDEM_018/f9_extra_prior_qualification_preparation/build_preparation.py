"""Byte/AST packaging only; no candidate/case/driver execution."""
import ast
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
RID='4f5a24b4-594d-4c6d-84f6-cd06dc4c6064'
UNIT='Q01_EXTRA_PRIOR_MEASURES'


def pin(path):
    raw=path.read_bytes()
    return {'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def save(path,raw):
    if path.exists():
        old=path.read_bytes()
        if old==raw:return
        b=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    temp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==raw and raw
    os.replace(temp,path);assert path.read_bytes()==raw


def js(name,doc):
    save(ROOT/name,(json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))


ident=json.loads((ROOT/'IDENTIDADE_PREPARACAO.json').read_bytes())
assert ident['request_id']==RID
request=BASE/'F9_NEXT_JOIN_QUALIFICATION_REQUEST.json'
assert pin(request)==ident['request_source']
req=json.loads(request.read_bytes());assert pin(Path(req['basis']['path']))==req['basis']
prior=BASE/'f9_physical_prior_preparation'/'physical_prior.py'
precision=BASE/'f9_precision_services_preparation'/'precision_services.py'
old_driver=BASE/'f9_precision_qualification_preparation'/'driver.py'
assert pin(prior)['sha256']=='4fbae1160282875c4ed61c242361c14db9434416a1886d41905c79f0a4f7a3f6'
assert pin(precision)['sha256']=='63f6adc987308cb14d986a07a9006610e0a304bb36d7d705f59e8c3874b7f278'
assert pin(old_driver)['sha256']=='348926e9c5d45a570984ab1cc93bcaa387bc18d2fd9c97c7cc993e6cdde88fe2'
sources={}
for p in (request,prior,precision,old_driver,Path(req['basis']['path']),
          BASE/'RECIBO_ROOT_Q01_PASS9.json',BASE/'RECIBO_ROOT_REVISOES_PRECISAO_THETA_F9.json',
          BASE/'RECIBO_ROOT_REVISAO_LIGACAO_F9.json',
          BASE/'preregistros/f9_completion_dependencies/QUADRO_F9_ATE_V1.md',
          BASE/'f9_physical_prior_preparation/CONTRATO_API.json'):
    sources[str(p)]=pin(p)
prior_tree=ast.parse(prior.read_bytes(),filename=str(prior))
source_request=None
for n in prior_tree.body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='REQUEST_ID' for t in n.targets):
        source_request=ast.literal_eval(n.value)
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCE_PINS' for t in n.targets):
        for rec in ast.literal_eval(n.value).values():
            assert pin(Path(rec['path']))==rec;sources[rec['path']]=rec
precision_ids={}
for n in ast.parse(precision.read_bytes(),filename=str(precision)).body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('LOG_SERVICE_ID','QUAD_SERVICE_ID'):
        precision_ids[n.targets[0].id]=ast.literal_eval(n.value)
assert set(precision_ids)=={'LOG_SERVICE_ID','QUAD_SERVICE_ID'}
order=['B01','B02','S01','R01','F01','F02','F03','Z01','N01','N02','N03']
driver=old_driver.read_text(encoding='utf-8')
changes={
 'f9_precision_qualification_preparation':'f9_extra_prior_qualification_preparation',
 'd8aac6d3-7061-42fb-ae33-6e8b834b3de8':RID,
 'f820203f-b83c-420a-87ec-7816f3179139':source_request,
 'f9_precision_services_preparation':'f9_physical_prior_preparation',
 'precision_services.py':'physical_prior.py',
 '"Q01"':'"Q01_EXTRA_PRIOR_MEASURES"',
 'F9_Q01_ROOT_DECISION_V1':'F9_Q01_EXTRA_PRIORS_ROOT_DECISION_V1',
 'ONLY_NINE_PINNED_PRECISION_CASES_NO_OBSERVED':'ONLY_ELEVEN_SCALAR_PRIOR_JOIN_CASES_NO_OBSERVED',
 'ENGINEERING_QUALIFICATION_OF_NINE_PINNED_CASES_ONLY':'ENGINEERING_QUALIFICATION_OF_ELEVEN_SCALAR_PRIOR_JOINS_ONLY',
 '16433':'16393',
 'q01_f820_pinned_candidate':'q01_df482_pinned_candidate',
 'q01_cases_pinned':'q01_extra_prior_cases_pinned',
 '"case_count"] == 9':'"case_count"] == 11',
 '"maximum_service_calls"] == 9':'"maximum_service_calls"] == 7',
 '"service_invocations"] == 9':'"service_invocations"] == 7',
 'len(results) == 9 and total_invocations == 9':'len(results) == 11 and total_invocations == 7',
 'cases.run_case(candidate, case, str(source), deadline)':'cases.run_case(candidate, case, str(source), deadline, precision)',
 'for name in ("log_exp_quad_interval", "positive_quad_1d"):\n            fn = getattr(candidate, name)':
   'for name in ("_analytic", "_rd_quadrature", "_Curve.peak"):\n            fn = candidate._Curve.peak if name == "_Curve.peak" else getattr(candidate, name)',
 }
for before,after in changes.items():
    assert before in driver,repr(before);driver=driver.replace(before,after)
driver=driver.replace('["W01", "W02", "W03", "W04", "W05", "P01", "P02", "N01", "N02"]',repr(order))
anchor='        case_record = next(x for x in manifest["members"] if Path(x["path"]).name == "cases.py")'
addition='''        precision_path = Path(contract["precision_service"]["path"])
        precision, precision_attest = load_bytes(precision_path, checked_bytes(contract["precision_service"]), "q01_f820_service_dependency")
        need(precision.LOG_SERVICE_ID == contract["precision_service_ids"]["LOG_SERVICE_ID"] and precision.QUAD_SERVICE_ID == contract["precision_service_ids"]["QUAD_SERVICE_ID"], "PRECISION_DEPENDENCY_IDENTITY")
        precision_functions = {}
        for service_name in ("log_exp_quad_interval", "positive_quad_1d"):
            service_fn = getattr(precision, service_name)
            need(service_fn.__globals__ is precision.__dict__ and service_fn.__code__.co_filename == str(precision_path), "LOADED_PRECISION_BINDING")
            precision_functions[service_name] = {"co_filename": service_fn.__code__.co_filename,
                "code_sha256": digest(marshal.dumps(service_fn.__code__))}
'''
assert anchor in driver;driver=driver.replace(anchor,addition+anchor)
driver=driver.replace('"functions": functions, "python_version": sys.version,',
    '"functions": functions, "precision_module": precision_attest, "precision_functions": precision_functions, "python_version": sys.version,')
anchor='        checked_bytes(case_record)\n        result = '
add='''        checked_bytes(case_record)
        checked_bytes(contract["precision_service"])
        need(sum(x["candidate_invocations"] for x in results) == 11, "PRIOR_ENTRY_COUNT")
        need(sum(x["real_service_invocations"] for x in results) == 4 and sum(x["synthetic_service_invocations"] for x in results) == 3, "REAL_VS_NEGATIVE_SERVICE_COUNTS")
        need(sum(x["curve_log_calls"] for x in results) <= 4105, "CURVE_WORK_CAP")
        need(sum((x["reference"] or {}).get("evaluations", 0) for x in results) == 257, "REFERENCE_WORK_COUNT")
        result = '''
assert anchor in driver;driver=driver.replace(anchor,add)
driver=driver.replace('"service_invocations": total_invocations,',
    '"service_invocations": total_invocations, "prior_entry_calls": 11, "real_f820_calls": 4, "synthetic_service_calls": 3,\n                  "curve_log_calls": sum(x["curve_log_calls"] for x in results), "reference_evaluations": 257,')
driver=driver.replace('Prepared Q01 supervisor and one pure worker.',
    'Prepared Q01 extra-prior supervisor; derived from pinned consumed Q01 runner, new scope only.')
save(ROOT/'driver.py',driver.encode('utf-8'))
cases=[]
for cid,route,a,center,offset,evaluations,logs,services,peaks in [
 ('B01','beta',400.0,0.01,0.0,4098,1,1,1),
 ('B02','beta',400.0,0.12,0.0,4098,1,1,1),
 ('S01','s',4.0,0.08,0.0,4098,1,1,1),
 ('R01','rd',1000000.0,None,0.0,4097,4098,1,1),
 ('F01','beta',0.0,0.0,2.0,0,0,0,0),
 ('F02','s',0.0,0.0,-3.0,0,0,0,0),
 ('F03','rd',0.0,None,5.0,0,0,0,0),
 ('Z01','beta',400.0,0.01,0.0,0,0,0,0),
 ('N01','beta',400.0,0.01,0.0,0,1,1,1),
 ('N02','rd',1000000.0,None,0.0,1,1,1,1),
 ('N03','rd',1000000.0,None,0.0,1,2,1,1)]:
    case={'id':cid,'route':route,'a':a,'center':center,'offset':offset,
          'maximum_evaluations':evaluations,'maximum_log_calls':logs,
          'expected_service_invocations':services,'expected_peak_calls':peaks,
          'comparison_absolute_log_tolerance':3e-8}
    if cid.startswith('N'):
        case['expected_evaluations']=evaluations
        case['expected_exception_code']={'N01':'SERVICE_ERROR','N02':'QUADRATURE_CALLBACK_FAILED',
                                        'N03':'QUADRATURE_ZERO_OR_UNDERFLOW'}[cid]
    cases.append(case)
assert [x['id'] for x in cases]==order
assert sum(x['maximum_evaluations'] for x in cases)==16393
assert sum(x['maximum_log_calls'] for x in cases)==4105
assert sum(x['expected_service_invocations'] for x in cases)==7
contract={'schema':'F9_Q01_EXTRA_PRIOR_CONTROL_CONTRACT_V1','request_id':RID,'unit':UNIT,
 'parent_request_id':ident['parent_request_id'],'source_request':source_request,
 'candidate':pin(prior),'precision_service':pin(precision),'precision_request_id':'f820203f-b83c-420a-87ec-7816f3179139',
 'precision_service_ids':precision_ids,
 'case_order':order,'cases':cases,'case_count':11,'maximum_service_calls':7,
 'maximum_total_evaluations':16393,'maximum_curve_log_evaluations':4105,
 'independent_reference_evaluations':257,'candidate_scalar_entries':11,
 'real_f820_service_calls':4,'negative_synthetic_service_calls':3,
 'scope':'Scalar _analytic/_rd_quadrature/_Curve.peak with explicit Gaussian restrictions; NOT _Curve construction or complete integrate_at_fixed_theta',
 'runtime':{'interpreter':pin(Path(sys.executable)),'flags':['-I','-S','-B','-X','utf8'],
            'loaded_code':'Exact bytes compile/exec plus source/code/function attestation; candidate+f820+harness',
            'stdlib_closure':'Executable pinned, full DLL/stdlib closure not pinned'},
 'limits':{'total_nominal_seconds':30,'worker_cooperative_seconds':23,'worker_outer_wait_seconds':25,
           'maximum_children':1,'case_parallelism':1,'threads':1,'retry':False,'fallback':False,
           'RAM_hard_limit_bytes':None,'disk_hard_quota_bytes':None,'stream_acceptance_bytes':65536,
           'timer_scope':'main entry through terminal readback; interpreter startup excluded, no hard realtime claim'},
 'sources':list(sources.values()),'candidate_imports':0,'numerical_controls_executed':0,
 'authorization_created':False,'execution_claim_created':False,
 'remote_preview':{'performed':False,'reason':'Local stdlib unit; source/generation divergence blocks remote stack'},
 'excluded':['matrix backend/NumPy','prepare_joint/evaluate_five/integrate_at_fixed_theta',
             'I02 guard/POSIX store','solver/WSL','real covariance/observations','Q02/Q03/uniform certificates',
             'rerun Q01scalar/Q01theta/c435/ffd6/NC02'],
 'I02_preflight_pending':"joint._admission['prediction_admission_sha256']==plan['assembly_admission_sha256'] before any background",
 'decision_schema_description':{'schema':'F9_Q01_EXTRA_PRIORS_ROOT_DECISION_V1','request_id':RID,'unit':UNIT,
        'authorize_single_execution':'REQUIRES_TRUE_IN_FUTURE_ROOT_FILE','manifest_sha256':'FUTURE_HASH',
        'review_reference':{'id':'FUTURE_REVIEW','sha256':'FUTURE_HASH'},
        'scope':'ONLY_ELEVEN_SCALAR_PRIOR_JOIN_CASES_NO_OBSERVED'}}
js('CONTROL_CONTRACT.json',contract)
trees={name:ast.parse((ROOT/name).read_bytes(),filename=str(ROOT/name)) for name in ('cases.py','driver.py')}
case_ids=next(n.value for n in trees['cases.py'].body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CASE_IDS' for t in n.targets))
assert ast.literal_eval(case_ids)==tuple(order)
assert not any(isinstance(n,ast.Import) and any(a.name.split('.')[0] in ('numpy','scipy','camb') for a in n.names) for t in trees.values() for n in ast.walk(t))
assert 'len(results) == 11 and total_invocations == 7' in driver
assert 'sum(x["curve_log_calls"] for x in results) <= 4105' in driver
assert not any((ROOT/n).exists() for n in ('ROOT_DECISION.json','RUN_CLAIM.json','AUTH.json','CLAIM.json','execution_once'))
for rec in sources.values():assert pin(Path(rec['path']))==rec
js('SOURCE_LINEAGE.json',{'request_id':RID,'sources':list(sources.values()),'runtime':contract['runtime'],
                         'driver_derived_from':pin(old_driver),'source_changes':0})
js('STATIC_PREPARATION_RECEIPT.json',{'request_id':RID,'status':'STATIC_PREPARATION_ONLY_NOT_EXECUTED',
 'checks':['request/basis pin','df482/f820 bytes and inherited pins','AST parsing only','11case identities',
           '16393 service evaluation cap/4105curve cap/257reference','4real+3negative services in11entries',
           'runtime/source bindings','no AUTH/CLAIM/output','all frozen source bytes unchanged'],
 'candidate_imports':0,'numerical_execution':0,'source_count':len(sources),'case_count':11,
 'independent_review':'PENDING','runtime_qualification':'PENDING','observed_reads':0,'solver_calls':0})
names=('IDENTIDADE_PREPARACAO.json','cases.py','driver.py','build_preparation.py','CONTROL_CONTRACT.json',
       'REFERENCIAS_E_COMANDO.md','SOURCE_LINEAGE.json','STATIC_PREPARATION_RECEIPT.json')
members=[pin(ROOT/n) for n in names]
js('MANIFESTO_PREPARACAO.json',{'request_id':RID,'unit':UNIT,
 'status':'PREPARATION_ONLY_PENDING_INDEPENDENT_REVIEW_AND_ROOT_DECISION','members':members,
 'backups':[pin(p) for p in sorted(ROOT.glob('*.bak_*'))],
 'authorization_created':False,'execution_created':False,
 'excludes':['MANIFESTO_PREPARACAO.json','RECIBO_COORDENACAO.json']})
for rec in members:assert pin(Path(rec['path']))==rec
print(json.dumps({'request_id':RID,'manifest':pin(ROOT/'MANIFESTO_PREPARACAO.json'),
                  'members':len(members),'sources':len(sources),'cases':11,
                  'max_service_evaluations':16393,'numerical_execution':0},ensure_ascii=False))
