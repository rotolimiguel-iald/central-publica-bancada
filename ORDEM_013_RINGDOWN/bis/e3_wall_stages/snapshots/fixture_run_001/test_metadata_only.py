"""Finite dummy metadata tests; never reads active allocation or science data."""
from pathlib import Path
from datetime import datetime,timezone
from types import SimpleNamespace
import ast,copy,hashlib,json,os

HERE=Path(__file__).resolve().parent
OUT=HERE/'fixtures_001'
E6=HERE.parent/'e6_prepare_v3'
CASES=[]


def write(p,obj):
    raw=obj if isinstance(obj,bytes) else (json.dumps(obj,indent=2,allow_nan=False)+'\n').encode()
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
    return p


def namespace(path):
    tree=ast.parse(path.read_bytes())
    nodes=[n for n in tree.body if not isinstance(n,ast.If)]
    ns={'__name__':'metadata_fixture_only','__file__':str(path)}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
    return ns


def check(name,fn,reject=False):
    error=None
    try:fn()
    except Exception as e:error=type(e).__name__+': '+str(e)
    CASES.append(dict(name=name,expected_rejection=reject,passed=(error is not None)==reject,error=error))


def ensure(value):
    if not value:raise ValueError('Fixture expectation failed')


def fixture(label):
    root=OUT/label;h=namespace(HERE/'wall_stage_adapter.py')
    h.update(ROOT=root,BASE=root/'ORDEM_DUMMY',HERE=root/'ORDEM_DUMMY/bis/wall')
    def put(rel,obj):return h['pin'](write(root/rel,obj))
    stamp='2020-01-01T00:00:00+00:00'
    contract=json.loads((E6/'CONTRACT.json').read_bytes())
    cp=put('contract.json',contract)
    e0={'systematic_conditions':[dict(reading=r,floor5_INPUT=0.01,floor15_INPUT=0.003) for r in contract['readings']]}
    ep=put('e0_dummy.json',e0)
    put('ORDEM_DUMMY/bis/wall/PREPARATION_PINS.json',dict(E0=ep,E6_contract=cp))
    reg=put('ORDEM_DUMMY/RINGDOWN_5SIGMA_V1.json',dict(status='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST',
        readings=contract['readings'],activation={'receipt_relative_to_Chatgpt':'activation_dummy.json'},
        allocation_policy={'relative_to_Chatgpt':'budget_dummy.json'}))
    act=put('activation_dummy.json',dict(status='E2_ACTIVATION_COMPLETE',registration_sha256=reg['sha256'],finished_utc=stamp))
    jobs=put('jobs_dummy.json',dict(schema_version='E2_PE_JOBS_V2',parent_registration_sha256=reg['sha256'],jobs={}))
    budget=put('budget_dummy.json',dict(parent_registration_sha256=reg['sha256'],registered_utc=stamp,
        jobs_relative_to_Chatgpt=jobs['path'],jobs_sha256=jobs['sha256'],witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/witness_dummy.md'))
    witness=put('TUNEL/DO_CHATGPT/witness_dummy.md',('allocation_sha256: '+budget['sha256']+'\nregistered_utc: '+stamp+'\n').encode())
    timeline=dict(kind='ALLOCATION_REGISTERED',evidence=budget,authorized_utc_pointer='/registered_utc',
        started_utc_pointer='/registered_utc',finished_utc_pointer='/registered_utc')
    receipt=dict(schema='E6_REVIEWED_STAGE_V2',stage='E3.2',registration_sha256=reg['sha256'],outcome='COMPLETED',
        issued_utc=stamp,artifact=budget,predecessor=act,timeline=timeline,bindings=[])
    review=dict(status='ACCEPTED_FOR_E6_MAPPING',stage='E3.2',registration_sha256=reg['sha256'],artifact_sha256=budget['sha256'],
        blocking_findings=[],reviewed_utc=stamp,reviewer='DUMMY_NOT_REAL_REVIEW',bindings=[],timeline=timeline,predecessor=act,outcome='COMPLETED')
    receipt['review']=put('prior_review_dummy.json',review);pred=put('prior_receipt_dummy.json',receipt)
    notes=put('note_dummy.md',b'DUMMY ONLY: no real instrument execution or authorization.\n')
    auth=dict(status='AUTHORIZED_WALL_STAGE_CANDIDATE_AFTER_BUDGET',stage='E3.3',helper_sha256=h['sha'](HERE/'wall_stage_adapter.py'),
        test_posterior_available=False,new_PE_allowed=False,new_injections_allowed=False,cost_per_converged_PE=None,
        outcome='UNAVAILABLE',reason='DUMMY_NO_EXECUTION_ONLY',registration=reg,E2_activation=act,budget=budget,budget_witness=witness,
        issued_utc=stamp,E6_contract=cp,E0=ep,principal_notes=[notes],predecessor=pred,run_id='wall_dummy')
    return h,auth,put,contract,e0


def run_prepare(h,auth,put,name):
    p=put(name,auth)
    h['prepare'](SimpleNamespace(execute=True,authorization=h['ROOT']/p['path'],authorization_sha256=p['sha256']))
    folder=h['HERE']/'candidates'/auth['run_id']
    return folder


def run_finalize(h,folder,put,name,mutate=None):
    request=folder/'ADAPTER_REVIEW_REQUEST.json';draft=h['load'](request)['draft']
    review={k:copy.deepcopy(draft[k]) for k in ('stage','registration_sha256','bindings','timeline','predecessor','outcome')}
    review.update(status='ACCEPTED_FOR_E6_MAPPING',blocking_findings=[],artifact_sha256=draft['artifact']['sha256'],
        request_sha256=h['sha'](request),reviewer='DUMMY_NOT_REAL_REVIEW',reviewed_utc=datetime.now(timezone.utc).isoformat())
    if mutate:mutate(review)
    rp=put(name,review)
    h['finalize'](SimpleNamespace(execute=True,request=request,request_sha256=h['sha'](request),
        review=h['ROOT']/rp['path'],review_sha256=rp['sha256']))
    return h['pin'](folder/'ADAPTER_REVIEWED.json')


def main():
    ensure(not OUT.exists());OUT.mkdir()
    h,a,put,c,e0=fixture('positive')
    a.update(stage='E3.2',predecessor=a['E2_activation'],outcome='COMPLETED',run_id='allocation_dummy')
    allocationfolder=run_prepare(h,a,put,'authorize_allocation_dummy.json')
    allocationref=run_finalize(h,allocationfolder,put,'review_allocation_dummy.json')
    allocation=h['load'](allocationfolder/'ADAPTER_REVIEWED.json')
    check('E3.2_artifact_actual_dummy_budget_empty_bindings',lambda:ensure(allocation['artifact']==a['budget'] and allocation['bindings']==[]
        and allocation['predecessor']==a['E2_activation'] and not (allocationfolder/'WALL_SOURCE.json').exists()))
    check('E3.2_single_documentary_registration_instant',lambda:ensure(all(allocation['timeline'][k]=='/registered_utc'
        for k in ('authorized_utc_pointer','started_utc_pointer','finished_utc_pointer'))))
    a.update(stage='E3.3',predecessor=allocationref,outcome='UNAVAILABLE',run_id='wall_dummy',issued_utc=datetime.now(timezone.utc).isoformat())
    folder=run_prepare(h,a,put,'authorize_dummy.json')
    check('E3.3_empty_bindings_wall',lambda:ensure(h['load'](folder/'ADAPTER_REVIEW_REQUEST.json')['draft']['bindings']==[]))
    pred=run_finalize(h,folder,put,'review_calibration_dummy.json')
    a.update(stage='TEST',predecessor=pred,run_id='test_dummy',issued_utc=datetime.now(timezone.utc).isoformat())
    testfolder=run_prepare(h,a,put,'authorize_test_dummy.json')
    testref=run_finalize(h,testfolder,put,'review_test_dummy.json')
    artifact=h['load'](testfolder/'WALL_SOURCE.json');receipt=h['load'](testfolder/'ADAPTER_REVIEWED.json')
    check('TEST_180_unique_cells',lambda:ensure(len(receipt['bindings'])==len({(b['route'],b['reading'],b['data_group']) for b in receipt['bindings']})==180))
    check('all_TEST_AWAITING_DATA_and_null_physical',lambda:ensure(all(r['summary']==dict(test_data_present=False,verdict='AWAITING_DATA')
        and all(v is None for v in r['metrics'].values()) and r['gate']['correction_over_sigma_physical'] is None for r in artifact['rows'])))
    check('E0_floors_only_220_INPUT',lambda:ensure(all(r['gate']['floor5_INPUT']==(0.01 if r['route']=='TAU220_POPULATION' else None)
        and r['gate']['sigma_c_calibrated'] is None and not any(r['gate'][f] for f in h['FLAGS']) for r in artifact['rows'])))
    check('no_fake_cost_or_execution',lambda:ensure(artifact['cost_per_converged_PE'] is None and artifact['status']=='NO_EXECUTION'
        and h['load'](testfolder/'FINALIZATION_RECEIPT.json')['E6_executed'] is False))
    # Exercise frozen E6 mapping functions only on in-memory dummy cells; no activate/main/baselines.
    e=namespace(E6/'generate_reach_table.py');cells={(r,reading,g):{'scenarios':[]} for r in h['ROUTES'] for reading in c['readings'] for g in h['GROUPS']}
    stages={};sources={}
    for stage,ref in [('E3.2',h['load'](folder/'ADAPTER_REVIEWED.json')['predecessor']),('E3.3',pred),('TEST',testref)]:
        rr=h['load'](h['checked'](ref));stages[stage]=(rr,ref);sources['STAGE_'+stage]=(rr['artifact'],h['load'](h['checked'](rr['artifact'])))
    def mapped(data):
        target=copy.deepcopy(cells);e['append_reviewed'](target,data,stages,c['readings'],c['permitted_verdicts']);return target
    check('frozen_E6_accepts_empty_E3.3_and_TEST180',lambda:ensure(sum(len(x['scenarios']) for x in mapped(sources).values())==180))
    for label,change in [('physical_z',lambda r:r['metrics'].update(z_physical=1)),
        ('physical_ratio',lambda r:r['gate'].update(correction_over_sigma_physical=1)),
        ('red_present_AWAITING',lambda r:r['summary'].update(test_data_present=True)),
        ('wrong_floor_unit',lambda r:r['gate']['units'].update(floor5_INPUT='fractional_dtau440'))]:
        data=copy.deepcopy(sources);change(data['STAGE_TEST'][1]['rows'][0])
        check('reject_'+label,lambda data=data:mapped(data),True)
    # No overwrite: real code must refuse reuse of a candidate or finalized receipt.
    check('reject_candidate_replacement',lambda:run_prepare(h,a,put,'second_auth_dummy.json'),True)
    check('reject_final_receipt_replacement',lambda:run_finalize(h,testfolder,put,'second_review_dummy.json'),True)
    for label,change in [('future',lambda a:a.update(issued_utc='2100-01-01T00:00:00Z')),
        ('naive',lambda a:a.update(issued_utc='2020-01-01T00:00:00')),
        ('malformed',lambda a:a.update(issued_utc='NOT_A_TIME')),
        ('helper_pin',lambda a:a.update(helper_sha256='0'*64)),
        ('cost_zero',lambda a:a.update(cost_per_converged_PE=0)),
        ('posterior_present',lambda a:a.update(test_posterior_available=True)),
        ('completed_wall',lambda a:a.update(outcome='COMPLETED')),
        ('budget_pin',lambda a:a['budget'].update(sha256='0'*64)),
        ('new_PE',lambda a:a.update(new_PE_allowed=True))]:
        nn,aa,pp,_,_=fixture(label);change(aa)
        check('reject_'+label,lambda nn=nn,aa=aa,pp=pp:run_prepare(nn,aa,pp,'authorize_dummy.json'),True)
        check('no_candidate_after_'+label,lambda nn=nn:ensure(not (nn['HERE']/'candidates').exists()))
    for label,raw in [('duplicate',b'{"a":1,"a":2}'),('overflow',b'{"a":1e999}'),('nan',b'{"a":NaN}')]:
        p=write(OUT/(label+'.json'),raw);check('reject_json_'+label,lambda p=p:h['load'](p),True)
    check('no_activation_without_execute',lambda:h['prepare'](SimpleNamespace(execute=False)),True)
    e0bad=copy.deepcopy(e0);e0bad['systematic_conditions'].append(e0bad['systematic_conditions'][0])
    check('reject_duplicate_floor',lambda:h['rows_and_bindings'](c,e0bad,a['E0'],'TEST'),True)
    for label,change in [('not_accepted',lambda r:r.update(status='PENDING')),('request_hash',lambda r:r.update(request_sha256='0'*64)),
        ('review_future',lambda r:r.update(reviewed_utc='2100-01-01T00:00:00Z'))]:
        nn,aa,pp,_,_=fixture(label);ff=run_prepare(nn,aa,pp,'authorize_dummy.json')
        check('reject_'+label,lambda nn=nn,ff=ff,pp=pp,change=change:run_finalize(nn,ff,pp,'bad_review_dummy.json',change),True)
        check('no_final_after_'+label,lambda ff=ff:ensure(not (ff/'ADAPTER_REVIEWED.json').exists()))
    result=dict(scope='DUMMY_METADATA_ONLY_NOT_ACTUAL_STAGE_CREATION',science_executed=False,actual_receipts_created=False,
        code_sha256=h['sha'](HERE/'wall_stage_adapter.py'),E6_code_sha256=h['sha'](E6/'generate_reach_table.py'),
        total=len(CASES),passed=sum(x['passed'] for x in CASES),cases=CASES)
    write(HERE/'FIXTURE_RESULTS_V1.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
    if result['passed']!=result['total']:raise SystemExit(1)


if __name__=='__main__':main()
