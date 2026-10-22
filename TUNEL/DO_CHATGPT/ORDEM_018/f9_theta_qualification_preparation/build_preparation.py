"""Metadata/AST packager only. Never imports or executes candidate/cases/driver."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
RID = '4e9a80ad-dac3-4c6c-8ec5-b7927a9c056d'
UNIT = 'Q01_THETA_COLLECTION'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    raw=path.read_bytes()
    return {'path':str(path),'bytes':len(raw),'sha256':digest(raw)}


def save(path, raw):
    if path.exists():
        old=path.read_bytes()
        if old==raw:
            return
        backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as out:out.write(old)
        assert backup.read_bytes()==old
    temporary=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with temporary.open('xb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
    assert temporary.read_bytes()==raw and raw
    os.replace(temporary,path)
    assert path.read_bytes()==raw


def save_json(name,obj):
    save(ROOT/name,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))


identity=json.loads((ROOT/'IDENTIDADE_PREPARACAO.json').read_bytes())
assert identity['request_id']==RID
request=BASE/'F9_NEXT_USEFUL_UNIT_REQUEST.json'
assert pin(request)==identity['request_source']
request_doc=json.loads(request.read_bytes())
for rec in request_doc['basis']:assert pin(Path(rec['path']))==rec
candidate=BASE/'f9_theta_integration_preparation'/'theta_integrator.py'
assert pin(candidate)['sha256']=='9de620190aaf4987cd1abf00772737721945926054d80d99bb1f540184ca2682'
tree=ast.parse(candidate.read_bytes(),filename=str(candidate))
literal={}
for node in tree.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        if node.targets[0].id in ('SOURCE_PINS','PRIOR_SOURCE_PINS','REQUEST_ID','PRIOR_REQUEST_ID'):
            literal[node.targets[0].id]=ast.literal_eval(node.value)
sources={str(request):pin(request),str(candidate):pin(candidate)}
for group in ('SOURCE_PINS','PRIOR_SOURCE_PINS'):
    for rec in literal[group].values():
        assert pin(Path(rec['path']))==rec
        sources[rec['path']]=rec
for rec in request_doc['basis']:sources[rec['path']]=rec
for name in ('RECIBO_ROOT_REVISOES_PRECISAO_THETA_F9.json',
             'preregistros/f9_completion_dependencies/QUADRO_F9_ATE_V1.md',
             'f9_precision_qualification_preparation/driver.py'):
    rec=pin(BASE/name);sources[rec['path']]=rec
old_driver=BASE/'f9_precision_qualification_preparation'/'driver.py'
assert pin(old_driver)['sha256']=='348926e9c5d45a570984ab1cc93bcaa387bc18d2fd9c97c7cc993e6cdde88fe2'
driver=old_driver.read_text(encoding='utf-8')
# Reuse the consumed supervisor's design in a NEW preparation. No old call is run.
replacements={
 'f9_precision_qualification_preparation':'f9_theta_qualification_preparation',
 'd8aac6d3-7061-42fb-ae33-6e8b834b3de8':RID,
 'f820203f-b83c-420a-87ec-7816f3179139':literal['REQUEST_ID'],
 'f9_precision_services_preparation':'f9_theta_integration_preparation',
 'precision_services.py':'theta_integrator.py',
 '"Q01"':'"Q01_THETA_COLLECTION"',
 'F9_Q01_ROOT_DECISION_V1':'F9_Q01_THETA_ROOT_DECISION_V1',
 'ONLY_NINE_PINNED_PRECISION_CASES_NO_OBSERVED':'ONLY_FIFTEEN_SYNTHETIC_THETA_CASES_NO_OBSERVED',
 'ENGINEERING_QUALIFICATION_OF_NINE_PINNED_CASES_ONLY':'ENGINEERING_QUALIFICATION_OF_FIFTEEN_SYNTHETIC_THETA_CASES_ONLY',
 'maximum_service_calls':'maximum_constructor_attempts',
 'service_invocations':'constructor_attempts',
 '16433':'765',
 'q01_f820_pinned_candidate':'q01_theta_pinned_candidate',
 'q01_cases_pinned':'q01_theta_cases_pinned',
 '"case_count"] == 9':'"case_count"] == 15',
 '"maximum_constructor_attempts"] == 9':'"maximum_constructor_attempts"] == 15',
 '"constructor_attempts"] == 9':'"constructor_attempts"] == 15',
 'len(results) == 9 and total_invocations == 9':'len(results) == 15 and total_invocations == 15 and total_runs == 16',
 'import heapq\n        import fractions':'import itertools',
 'for name in ("log_exp_quad_interval", "positive_quad_1d"):\n            fn = getattr(candidate, name)':
     'for name in ("run", "_accept", "_evaluate", "_level_result"):\n            fn = getattr(candidate.ThetaIntegrator, name)',
 'results, total_evaluations, total_invocations = [], 0, 0':'results, total_evaluations, total_invocations, total_runs = [], 0, 0, 0',
 'cases.run_case(candidate, case, str(source), deadline)':'cases.run_case(candidate, case, str(source), deadline, contract)',
 'total_invocations += result["constructor_attempts"]':'total_invocations += result["constructor_attempts"]\n            total_runs += result["run_attempts"]\n            need(total_runs <= contract["maximum_run_attempts"], "TOTAL_RUN_CAP")',
 '"constructor_attempts": total_invocations,':'"constructor_attempts": total_invocations, "run_attempts": total_runs,',
 }
for before,after in replacements.items():
    assert before in driver,repr(before)
    driver=driver.replace(before,after)
order=['T01','T02','T03','T04','T05','T06','N01','N02','N03','N04','N05','N06','N07','N08','N09']
driver=driver.replace('["W01", "W02", "W03", "W04", "W05", "P01", "P02", "N01", "N02"]',repr(order))
driver=driver.replace('Prepared Q01 supervisor and one pure worker.',
    'Prepared Q01-THETA supervisor and one pure synthetic worker; derived from pinned Q01 supervisor.')
driver=driver.replace('and result["observed_total_evaluations"] <= 765,',
    'and result["run_attempts"] == 16 and result["observed_total_evaluations"] == 765,')
save(ROOT/'driver.py',driver.encode('utf-8'))
cases=[]
for cid,purpose in [
 ('T01','Constant five-model integrals; prior normalization, quality counters and post-success reentry refusal'),
 ('T02','Tensor cubic: integral (5/4)(4/3)(3/2)=5/2 for every scale'),
 ('T03','Same tensor cubic with common log offset +1000; no exp(1000) needed'),
 ('T04','Same tensor cubic with common log offset -1000; no absolute underflow'),
 ('T05','One hypothesis has legitimate zero sampled support everywhere; complete family fails after full box'),
 ('T06','Compact triangular peak between all nodes: sampled rule1 versus true integral2; no certificate promotion')]:
    rec={'id':cid,'purpose':purpose,'expected_callbacks':125,'expected_completed':125,
         'absolute_log_tolerance':3e-10 if cid in ('T03','T04') else 1e-11}
    if cid=='T05':rec['expected_exception_code']='NO_POSITIVE_SAMPLED_MASS'
    cases.append(rec)
for cid,calls,done,code,purpose in [
 ('N01',0,0,'BUDGET_ERROR','124 callbacks cannot cover125 nodes: pre-callback refusal'),
 ('N02',3,2,None,'Same sentinel exception at callback3; post-failure reentry rejected without new callback'),
 ('N03',2,1,'MEASURE_CHANGED','Nuisance normalization changes at node2'),
 ('N04',2,1,'PIN_ERROR','Wrong conditional-result hash at node2'),
 ('N05',1,0,'DENSITY_ERROR','Minus infinity without corresponding zero-support status'),
 ('N06',2,1,'SCHEMA_ERROR','Fifth model missing at node2'),
 ('N07',2,1,'BACKGROUND_ERROR','Same synthetic background hash at different theta'),
 ('N08',1,0,'PRIOR_ERROR','Base theta prior already applied in callback'),
 ('N09',2,1,'IDENTITY_ERROR','Callback theta differs from requested theta')]:
    cases.append({'id':cid,'purpose':purpose,'expected_callbacks':calls,
                  'expected_completed':done,'expected_exception_code':code})
assert [x['id'] for x in cases]==order and sum(x['expected_callbacks'] for x in cases)==765
contract={'schema':'F9_Q01_THETA_CONTROL_CONTRACT_V1','request_id':RID,'unit':UNIT,
          'parent_request_id':identity['parent_request_id'],'source_request':literal['REQUEST_ID'],
          'prior_request':literal['PRIOR_REQUEST_ID'],'candidate':pin(candidate),
          'case_order':order,'cases':cases,'case_count':15,
          'maximum_constructor_attempts':15,'maximum_run_attempts':16,
          'maximum_total_evaluations':765,'exact_expected_total_callbacks':765,
          'maximum_unique_nodes_per_instance':125,'theta_source_pins':literal['SOURCE_PINS'],
          'prior_source_pins':literal['PRIOR_SOURCE_PINS'],
          'case_source_sha256':pin(ROOT/'cases.py')['sha256'],
          'driver_source_sha256':pin(ROOT/'driver.py')['sha256'],
          'runtime':{'interpreter':pin(Path(sys.executable)), 'required_major_minor':[3,14],
                     'flags':['-I','-S','-B','-X','utf8'],
                     'stdlib_dll_closure':'Not pinned in full; exact candidate/cases bytes and functions attested; interpreter executable pinned'},
          'sources':list(sources.values()),
          'limits':{'total_nominal_seconds':30,'worker_cooperative_seconds':23,
                    'worker_wait_seconds':25,'reaping_reserve_seconds':4,'maximum_children':1,
                    'parallel_cases':1,'threads':1,'RAM_hard_limit_bytes':None,
                    'RAM_scope':'Bounded125-node stdlib fixtures; no OS job-object RAM cap or benchmark claimed',
                    'stream_acceptance_bytes':65536,'output_hard_disk_quota':None,
                    'scope':'Nominal deadline after main; not hard realtime; known pinned worker has no descendants'},
          'authorization_created':False,'execution_claim_created':False,
          'candidate_imports':0,'numerical_controls_executed':0,
          'external_provider_preview':{'performed':False,'reason':'Local stdlib qualification; remote stack ineligible, no dispatch needed'},
          'excluded':['real joint/observations/covariance','assembler/physical_prior/profile execution',
                      'precision-service replay','I02 POSIX store/guard qualification','WSL/CAMB/NumPy/SciPy',
                      'network/providers','physical Q02/Q03 precision','new numerical method or uniform certificate'],
          'I02_remaining_preflight':"joint._admission['prediction_admission_sha256'] == plan['assembly_admission_sha256'] before any future background",
          'decision_schema_description':{'schema':'F9_Q01_THETA_ROOT_DECISION_V1','request_id':RID,'unit':UNIT,
              'authorize_single_execution':'MUST_BE_TRUE_ONLY_IN_FUTURE_ROOT_FILE',
              'manifest_sha256':'FUTURE_VERIFIED_MANIFEST_HASH','review_reference':{'id':'FUTURE_REVIEW','sha256':'FUTURE_HASH'},
              'scope':'ONLY_FIFTEEN_SYNTHETIC_THETA_CASES_NO_OBSERVED'}}
save_json('CONTROL_CONTRACT.json',contract)
trees={name:ast.parse((ROOT/name).read_bytes(),filename=str(ROOT/name)) for name in ('cases.py','driver.py')}
assert not any(isinstance(n,ast.Import) and any(a.name.split('.')[0] in ('numpy','scipy','camb') for a in n.names) for tr in trees.values() for n in ast.walk(tr))
assert ast.literal_eval(next(n.value for n in trees['cases.py'].body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CASE_IDS' for t in n.targets)))==tuple(order)
assert 'total_runs == 16' in driver and 'observed_total_evaluations"] == 765' in driver
assert '16' in driver and 'ROOT_DECISION.json' in driver and 'RUN_CLAIM.json' in driver
assert not any((ROOT/n).exists() for n in ('ROOT_DECISION.json','RUN_CLAIM.json','AUTH.json','CLAIM.json','execution_once'))
for rec in sources.values():assert pin(Path(rec['path']))==rec
save_json('SOURCE_LINEAGE.json',{'request_id':RID,'sources':list(sources.values()),'runtime':contract['runtime'],
                               'driver_derived_from':pin(old_driver),'source_changes':0,'sources_verified':len(sources)})
save_json('STATIC_PREPARATION_RECEIPT.json',{'request_id':RID,'status':'STATIC_PREPARATION_ONLY_NOT_EXECUTED',
    'checks':['request/basis byte pins','candidate and inherited source pins','AST candidate/cases/driver parsed only',
              '15 case identities and765 callback caps','16 maximum run attempts including2 intentional no-callback reentries',
              'driver source and fixture bindings','no scientific imports in prepared modules','no AUTH/claim/execution output',
              'all source bytes unchanged'], 'candidate_imports':0,'numerical_execution':0,'source_count':len(sources),
    'case_count':15,'candidate_module_copied':False,'driver_only_copied_and_adapted':True,
    'independent_review':'PENDING','runtime_qualification':'PENDING','solver_calls':0,'observed_reads':0})
names=('IDENTIDADE_PREPARACAO.json','cases.py','driver.py','build_preparation.py','CONTROL_CONTRACT.json',
       'REFERENCIAS_E_COMANDO.md','SOURCE_LINEAGE.json','STATIC_PREPARATION_RECEIPT.json')
members=[pin(ROOT/name) for name in names]
backups=[pin(p) for p in sorted(ROOT.glob('*.bak_*'))]
save_json('MANIFESTO_PREPARACAO.json',{'request_id':RID,'unit':UNIT,
    'status':'PREPARATION_ONLY_PENDING_INDEPENDENT_REVIEW_AND_ROOT_DECISION','members':members,
    'backups':backups,'authorization_created':False,'execution_created':False,
    'excludes':['MANIFESTO_PREPARACAO.json','RECIBO_COORDENACAO.json']})
for rec in members:assert pin(Path(rec['path']))==rec
print(json.dumps({'request_id':RID,'manifest':pin(ROOT/'MANIFESTO_PREPARACAO.json'),
                  'members':len(members),'sources':len(sources),'cases':15,'max_callbacks':765,
                  'numerical_execution':0},ensure_ascii=False))
