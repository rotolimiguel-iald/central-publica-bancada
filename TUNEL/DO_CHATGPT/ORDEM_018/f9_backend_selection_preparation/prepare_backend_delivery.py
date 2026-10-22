"""Assemble documentary payload and custody; no candidate imports or arithmetic tests."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import os

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
RID = 'bf2a5692-1aff-423e-9345-7bfa256d5072'
checks = []


def check(name, ok):
    if not ok:
        raise RuntimeError(name)
    checks.append({'name':name,'passed':True})


def info(path):
    path=Path(path);raw=path.read_bytes()
    return {'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def write_new(name, data):
    p=BASE/name;check('new file '+name,not p.exists())
    raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    tmp=p.with_suffix(p.suffix+'.tmp')
    with tmp.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    check('temporary exact '+name,tmp.read_bytes()==raw)
    os.replace(tmp,p);check('written exact '+name,p.read_bytes()==raw)


meta=json.loads((BASE/'METADADOS_BACKENDS_LOCAIS.json').read_bytes())
check('metadata request',meta['request_id']==RID)
for pin in meta['local_pins']:
    now=info(pin['path'])
    check('source unchanged '+Path(pin['path']).name,now['bytes']==pin['bytes'] and now['sha256']==pin['sha256'])
check('zero candidate imports',meta['candidate_imports']==0)
check('zero control runs',meta['control_or_solver_runs']==0)
check('zero remote calls',meta['remote_model_calls']==0)
check('zero installs/downloads',meta['downloads']==meta['installations']==0)
check('two Windows scopes',len(meta['windows_inventory'])==2)
check('WSL metadata no candidate import',meta['wsl_inventory']['candidate_imports']==0)
check('source note exists',(BASE/'SELECAO_BACKEND_LOCAL.md').stat().st_size>0)

def rat(n,d='1'):
    # Data constructor only: no Fraction, conversion, reduction or evaluation.
    return {'numerator':n,'denominator':d}

dependency_names={'INTERFACE_CERTIFICADOS_F9.json','CONTRATO_NUMERICO_F9.md',
    'PLANO_SINTETICO_NUMERICO.json','PARECER_CERTIFICACAO_NUMERICA_F9.md',
    'RECIBO_ROOT_CONTROLES_TAIL_V2_PASS.json','tail_envelope.py','RUNTIME_PINS.json',
    'python.exe','python314.dll','fractions.py'}
dependencies=[p for p in meta['local_pins'] if Path(p['path']).name in dependency_names]
payload={
    'schema':'F9_NC02_RATIONAL_UNIT_PROPOSAL_V1',
    'preparation_request_id':RID,
    'proposed_unit_identity':RID+'::NC02-RAT-01',
    'status':'READY_FOR_IMPLEMENTATION_PREPARATION_NOT_EXECUTION',
    'execution_request_id':None,'claim_created':False,'worker_source_sha256':None,
    'execution_authorized':False,'canonical_F9_contract_changed':False,
    'target':'SYNTHETIC_NC02_ONLY_NOT_ANY_PHYSICAL_HYPOTHESIS',
    'objective':'Implement then independently review a single rational dual-lower/feasible-upper certificate fixture and one non-annihilating negative, before any execution.',
    'backend':'Pinned Windows Python integer arithmetic and Fraction over canonical integer pairs; no floating point',
    'codec_dependency':'Read-only pinned tail_envelope._rational, return(a,b); import/call allowed only in a later authorized unit. No tail_upper/aggregate/worker call.',
    'geometry':{'C':[[rat('1'),rat('0')],[rat('0'),rat('1')]],
        'X':[[rat('1')],[rat('1')]],'data_dimension':2,'nuisance_dimension':1,
        'support':'R^2','nuisance_domain':'R','no_numerical_rank_or_tolerance':True},
    'cell':{'coordinate':'u','closed_lower':rat('0'),'closed_upper':rat('1','2'),
        'b_constant':[rat('1'),rat('0')],'b_linear':[rat('0'),rat('1')],
        'cover':'this one closed interval is the entire toy domain'},
    'cases':[
        {'id':'NC02-RAT-01-POSITIVE','dual_v':[rat('1','4'),rat('-1','4')],
         'witness':{'u':rat('1','2'),'eta':rat('3','4')},
         'required_checks':['X^T v exactly zero','dual affine bound valid over whole toy cell','feasible witness residual norm squared'],
         'expected_analytic_not_run':{'status':'CERTIFIED_TOY_MINIMUM','lower':rat('1','8'),'upper':rat('1','8')}},
        {'id':'NC02-RAT-01-NEGATIVE-ANNIHILATION','dual_v':[rat('1','4'),rat('-255','1024')],
         'required_checks':['reject nonzero X^T v before issuing a certificate; never tolerance cutoff'],
         'expected_analytic_not_run':{'status':'INVALID_DUAL_ANNIHILATION','annihilation_residual':rat('1','1024'),'lower':None,'upper':None}}
    ],
    'builder_output_contract':['payload_sha256','dependency_hashes','case_id','exact_annihilation_witness',
        'dual_affine_coefficients','lower_on_entire_cell','feasible_point_and_eta','upper_from_residual','certificate_status'],
    'independent_verifier':'Recompute annihilation, affine endpoint lower, witness residual and integer comparisons from payload; never trust builder valid flag or hardcoded expected output.',
    'arithmetic_proof_reference':{'profile':'q(u)=(1-u)^2/2',
        'completion_of_square':'||b-X eta||^2 = 2*(eta-(1+u)/2)^2+(1-u)^2/2',
        'positive_dual':'2 v^T b-v^T C v=3/8-u/2>=1/8 for 0<=u<=1/2',
        'statute':'DERIVED_SYMBOLIC_EXPECTATION_NOT_EXECUTED'},
    'dependencies_pinned_now':dependencies,
    'metadata_receipt':info(BASE/'METADADOS_BACKENDS_LOCAIS.json'),
    'dependencies_to_freeze_after_implementation':['new builder/verifier/worker source hashes','complete actually used runtime imports','explicit execution identity and supervisor binding'],
    'resource_requirements_proposed':{'worker_wall_s':10,'total_through_persistence_s':30,'threads':1,
        'RSS_MiB':256,'output_KiB':128,'input_bits_max_from_existing_codec':512,
        'intermediate_bits_max_proposed':4096,'fixed_case_count':2,
        'hard_OS_limits_qualified':False,'do_not_claim_enforced_before_implementation':True},
    'forbidden':['observed inputs','CAMB','numpy/scipy/sympy/mpmath','exp/log/SF','quadrature','random sampling',
        'tail_upper','aggregate_bounds','old tail controls','C01-C08','INIT003','WSL4f5d replay',
        'provider call or metadata repair','kernel or gate change','new real F9 run','automatic retry'],
    'execution_sequence_proposed':['Prepare builder/verifier/worker in separately authorized output directory with old files read-only',
        'Freeze source/runtime/payload pins and obtain independent static review',
        'ROOT creates own execution request/claim if approved; one run of exactly two cases',
        'Review receipt and actual resource scope; no promotion to physical F9 certificates'],
    'actual_result':None,'actual_runs':0,'sigma':None}
check('two fixed cases',len(payload['cases'])==2)
check('worker not falsely existing',payload['worker_source_sha256'] is None)
check('no execution identity invented',payload['execution_request_id'] is None)
check('no authorization from proposal',payload['execution_authorized'] is False)
check('no computed result',payload['actual_result'] is None and payload['actual_runs']==0)
write_new('PAYLOAD_PROXIMA_UNIDADE_NC02.json',payload)

choice={'request_id':RID,'status':'DOCUMENTARY_BACKEND_SELECTION_NOT_IMPLEMENTATION_OR_EXECUTION',
    'selected':'Python integer/Fraction exact rational for NC02 subset only',
    'alternatives':[
        {'id':'A','name':'Exact rational','installed_evidence':'Windows stdlib sources/runtime and consumed tail integer-code receipt pinned',
         'scope':'rational operations on fixed small fixture; bounded resources','selected':True,
         'elementary_extensions':'Rational exp enclosure formula exists in admitted tail proposal; not implemented/qualified by tailV2 PASS'},
        {'id':'B','name':'mpmath.iv','installed_evidence':'mpmath1.3.0 METADATA in Windows user-site and WSL; local libmpi source',
         'scope':'interval mechanisms present; package docs warn about heuristic non-arithmetic directed rounding',
         'candidate_imported':False,'globally_qualified':False,'selected':False},
        {'id':'C','name':'Decimal adapter','installed_evidence':'decimal.py,_pydecimal.py and accelerated extension bytes present',
         'scope':'fallback exp/ln final HALF_EVEN visible; accelerated implementation and outward wrapper not qualified',
         'candidate_imported':False,'globally_qualified':False,'selected':False}],
    'not_found_scope':'No matching Arb/FLINT/GMPY2/MPFI/MPFR metadata in the three enumerated roots; no whole-computer absence claim',
    'next_unit_payload':info(BASE/'PAYLOAD_PROXIMA_UNIDADE_NC02.json'),
    'ready_for':'separate local implementation preparation and independent review',
    'not_ready_for':'automatic controls, scientific minima, quadrature or observed F9',
    'queue':'No remote call, repair, admission, repin or old Claude dispatch; current metadata/source mismatch preserved',
    'unchanged':['five physical models','prior domains','scenario family','alpha','V1','section6','originals','shared memories','gate']}
write_new('DECISAO_BACKEND_CANDIDATA.json',choice)
validation={'request_id':RID,'status':'PASS_DOCUMENTARY_CUSTODY_ONLY','checks_passed':len(checks),'checks':list(checks),
    'candidate_imports':0,'control_runs':0,'solver_runs':0,'observed_data_access':False,'remote_calls':0,
    'downloads':0,'installations':0,'symbolic_expected_values_are_not_run_results':True}
write_new('VALIDACAO_DOCUMENTAL.json',validation)
files=[]
for p in sorted(BASE.iterdir()):
    if p.is_file() and p.name not in ['MANIFESTO_ENTREGA.json','RECIBO_COORDENACAO.json']:
        x=info(p);x['path']=p.name;files.append(x)
write_new('MANIFESTO_ENTREGA.json',{'request_id':RID,'created_utc':datetime.now(timezone.utc).isoformat(),
    'status':'DOCUMENTARY_PREPARATION_COMPLETE_NOT_BACKEND_VALIDATION','files':files,
    'candidate_imports':0,'scientific_controls':0,'observed_reads':False,'remote_calls':0,
    'execution_authorization':False})
for n in ['SELECAO_BACKEND_LOCAL.md','PAYLOAD_PROXIMA_UNIDADE_NC02.json','MANIFESTO_ENTREGA.json']:
    print(json.dumps(info(BASE/n)))
print(json.dumps({'documentary_checks':validation['checks_passed'],'manifest_files':len(files),'local_sources_revalidated':len(meta['local_pins']),'synthetic_cases_planned':2,'executed':0}))
