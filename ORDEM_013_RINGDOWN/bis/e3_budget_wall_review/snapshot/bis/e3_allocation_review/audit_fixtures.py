"""Finite metadata-only audit. Copies under this review tree; no actual launch/data."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import copy
import hashlib
import importlib.util
import json
import os
import sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
PRODUCER=BASE/'bis/e3_allocation_prepare'
SNAP=HERE/'snapshot_001'
RESULTS=[]
LIMIT=25_000_000


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p,obj):
    raw=(json.dumps(obj,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n').encode()
    if len(raw)>LIMIT:raise ValueError('Review file cap')
    p.parent.mkdir(parents=True,exist_ok=True)
    pending=p.with_name(p.name+'.pending')
    with pending.open('xb') as f:f.write(raw)
    if pending.stat().st_size!=len(raw):raise ValueError('Short fixture write')
    os.link(pending,p);pending.unlink()


def module(p,name):
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def pin(p,root):return dict(relative_to_Chatgpt=p.relative_to(root).as_posix(),sha256=sha(p))


def setup(name,alter=None):
    folder=HERE/'fixtures_001'/name
    root=folder/'Chatgpt';base=root/'ORDEM_013_RINGDOWN';side=base/'bis/e3_allocation_prepare'
    side.mkdir(parents=True,exist_ok=False)
    for n in ('render_allocation_candidates.py','CONTRACT_SCHEMA.json'):
        (side/n).write_bytes((SNAP/n).read_bytes())
    now=datetime.now(timezone.utc);stamp=lambda sec:(now+timedelta(seconds=sec)).isoformat()
    schema=json.loads((side/'CONTRACT_SCHEMA.json').read_bytes())
    cfg={k:1 for k in schema['job_required']}
    cfg.update(event='FAKE_CAL',mode='calibration',privacy_mode='procedural_same_host',label='FAKE_ONLY',
        variant='220_plus_440_free',fixed_deformation_parameters={},output_directory_name='fake_new_output',
        event_GPS=1000,segment_start_GPS=990,duration_s=16,detectors=['FAKE_DETECTOR'],data={},
        wall_budget_seconds=30,
        priors={k:dict(kind='Uniform',minimum=0.1,maximum=0.9) for k in schema['prior_names_exact']},
        sampler=dict(nlive=10,walks=2,maxcall=100,workers=24,seed=0,dlogz=0.1,
                     minimum_posterior_samples=2,minimum_effective_samples=2,check_point=False,check_point_plot=False),
        remnant_conversion_INPUT={'fixture':'NO_COSMOLOGY_OR_DATA_READ'})
    reg=dict(status='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST',registered_utc=stamp(-300),
        budget_relative_to_Chatgpt='ORDEM_013_RINGDOWN/PART_B_BUDGET_START.json',
        pe_jobs={'fake_static_pilot':dict(mode='calibration',event='FAKE_CAL',output_directory_name='fake_static_output')},
        calibration_event_ids=['FAKE_CAL'],event_reference_GPS={'FAKE_CAL':1000},
        test_candidates={'FAKE_BLIND':dict(eligible=True,published_deformation_at_registration=False,
            data_quality_hold=True,publication_census_scope='FICTITIOUS_METADATA_ONLY')},
        allocation_policy=dict(relative_to_Chatgpt='ORDEM_013_RINGDOWN/ORCAMENTO_40H.json',max_job_wall_seconds=28800))
    budget=dict(hard_deadline_utc=stamp(7200))
    controller=dict(job='fake_static_pilot',blind=False,status='CHILD_COMPLETED_REQUIRES_REVIEW',returncode=0,
        cleanup={'group_absent':True},wall_seconds=20,started_utc=stamp(-100),finished_utc=stamp(-80))
    conv=dict(accepted_for_analysis=True,cost=dict(sampler_ncall=100,likelihood_calls=90,source_calls=80))
    proposal=dict(schema_version='E3_ALLOCATION_PROPOSAL_V1',slug='candidate_fake',allocation_registered_utc=stamp(-10),
        jobs_relative_to_Chatgpt='ORDEM_013_RINGDOWN/fake_future_jobs.json',
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/fake_future_witness.md',jobs={'fake_new':cfg},ordered_job_names=['fake_new'],
        global_reserve_seconds=60,decision_documentation=dict(five_alternatives=[{'id':i,'status':'OPEN_FAKE'} for i in range(1,6)],
            per_job_cost_and_information={'fake_new':{'cost':'FAKE_ONLY','information':None}},
            unpaid=['NO_SCIENCE'],stopping_rules='FAKE_METADATA',selection_rationale='NO_REAL_SELECTION',
            pilot_independent_review='FAKE_NOT_A_REAL_REVIEW',reserve_rationale='FIXTURE_ONLY'))
    state=dict(folder=folder,root=root,base=base,side=side,reg=reg,budget=budget,controller=controller,conv=conv,
               proposal=proposal,cfg=cfg,stamp=stamp)
    if alter:alter(state)
    write(base/'PART_B_BUDGET_START.json',budget);reg['budget_sha256']=sha(base/'PART_B_BUDGET_START.json')
    write(base/'RINGDOWN_5SIGMA_V1.json',reg);digest=sha(base/'RINGDOWN_5SIGMA_V1.json')
    controller['registration_sha256']=digest;conv['registration_sha256']=digest
    pilot=base/'fake_pilot_metadata'
    write(pilot/'CONTROLLER.json',controller);write(pilot/'PRIVATE_CONVERGENCE.json',conv)
    proposal.update(registration=pin(base/'RINGDOWN_5SIGMA_V1.json',root),
                    pilot_controller=pin(pilot/'CONTROLLER.json',root),
                    pilot_convergence=pin(pilot/'PRIVATE_CONVERGENCE.json',root))
    state.update(digest=digest,pilot=pilot)
    return state


def execute(state):
    proposal=state['side']/'PROPOSAL_FAKE.json';write(proposal,state['proposal'])
    mod=module(state['side']/'render_allocation_candidates.py','candidate_fixture')
    before=sys.argv;sys.argv=[str(mod.__file__),str(proposal)]
    try:mod.main()
    finally:sys.argv=before
    return mod


def run_case(name,alter=None,post=None,expect_reject=True,check=None):
    state=setup(name,alter)
    if post:post(state)
    error=None
    try:execute(state)
    except Exception as exc:error=type(exc).__name__+': '+str(exc)
    okay=(error is not None) if expect_reject else (error is None)
    detail={}
    if check:
        try:detail=check(state,error);okay=okay and detail.pop('ok',True)
        except Exception as exc:okay=False;detail={'check_error':repr(exc)}
    RESULTS.append(dict(id=name,expectation='REJECT' if expect_reject else 'ACCEPT_CANDIDATE_ONLY',
                        passed=okay,error=error,details=detail))
    return state


def baseline_check(s,error):
    dst=s['side']/'candidates/candidate_fake'
    jobs=dst/'JOBS_V2.CANDIDATE.json';allocation=json.loads((dst/'ORCAMENTO_40H.CANDIDATE.json').read_bytes())
    active=s['base']/'ORCAMENTO_40H.json';future=s['root']/s['proposal']['jobs_relative_to_Chatgpt']
    witness=s['root']/s['proposal']['witness_relative_to_Chatgpt']
    okay=allocation['jobs_sha256']==sha(jobs) and not any(p.exists() for p in (active,future,witness))
    return dict(ok=okay,jobs_pin_exact=allocation['jobs_sha256']==sha(jobs),active_destinations_absent=okay,
                serial_sum=allocation['preparation']['serial_job_ceilings_seconds'])


def guard_fixture(s):
    code=s['base']/'bis/e2_code';code.mkdir(parents=True)
    p=code/'registration_guard.py';p.write_bytes((SNAP/'registration_guard.py').read_bytes())
    return module(p,'fake_guard')


def guard_tests():
    s=setup('guard_chain');execute(s);guard=guard_fixture(s)
    def test(name,call,reject=False,validate=None):
        err=None;result=None
        try:result=call()
        except Exception as e:err=type(e).__name__+': '+str(e)
        RESULTS.append(dict(id=name,expectation='REJECT' if reject else 'SUCCESS',
            passed=(err is not None) if reject else (err is None and (validate(result) if validate else True)),error=err))
    test('guard_candidate_directory_not_active',lambda:guard.load_jobs(s['reg'],s['digest']),
         validate=lambda jobs:set(jobs)=={'fake_static_pilot'})
    dst=s['side']/'candidates/candidate_fake';active=s['base']/'ORCAMENTO_40H.json'
    active.write_bytes((dst/'ORCAMENTO_40H.CANDIDATE.json').read_bytes())
    test('guard_active_copy_without_witness_rejected',lambda:guard.load_jobs(s['reg'],s['digest']),True)
    future=s['root']/s['proposal']['jobs_relative_to_Chatgpt'];future.write_bytes((dst/'JOBS_V2.CANDIDATE.json').read_bytes())
    witness=s['root']/s['proposal']['witness_relative_to_Chatgpt'];witness.parent.mkdir(parents=True)
    stamp=datetime.now(timezone.utc).isoformat()
    def witness_write(hashvalue,extra=''):
        witness.write_text('allocation_sha256: '+hashvalue+'\nregistered_utc: '+stamp+'\n'+extra)
    witness_write('0'*64)
    test('guard_wrong_witness_hash',lambda:guard.load_jobs(s['reg'],s['digest']),True)
    witness_write(sha(active),'allocation_sha256: '+sha(active)+'\n')
    test('guard_duplicate_witness_hash',lambda:guard.load_jobs(s['reg'],s['digest']),True)
    witness_write(sha(active))
    test('guard_explicit_fake_promotion_status_is_not_gate',lambda:guard.load_jobs(s['reg'],s['digest']),
         validate=lambda jobs:set(jobs)=={'fake_static_pilot','fake_new'})
    original=future.read_bytes();future.write_bytes(original+b' ')
    test('guard_jobs_byte_pin_changed',lambda:guard.load_jobs(s['reg'],s['digest']),True)
    future.write_bytes(original)
    allocation=json.loads(active.read_bytes());extra=json.loads(original)
    extra['jobs']={'fake_static_pilot':extra['jobs']['fake_new']}
    future.write_text(json.dumps(extra));allocation['jobs_sha256']=sha(future)
    active.write_text(json.dumps(allocation));witness_write(sha(active))
    test('guard_jobs_no_static_replacement',lambda:guard.load_jobs(s['reg'],s['digest']),True)


def main():
    if SNAP.exists():raise FileExistsError('Immutable prior review snapshot exists')
    SNAP.mkdir(parents=True)
    sources={n:PRODUCER/n for n in ('render_allocation_candidates.py','CONTRACT_SCHEMA.json',
              'CONTRACT_AND_CHECKLIST.md','GENERATOR_INPUT.md','PREPARATION_RECEIPT.json')}
    sources.update({'registration_guard.py':BASE/'bis/e2_code/registration_guard.py',
        'E3_ALTERNATIVE5_METADATA_ONLY_V1.json':BASE/'bis/E3_ALTERNATIVE5_METADATA_ONLY_V1.json'})
    pins={}
    for n,p in sources.items():
        raw=p.read_bytes();(SNAP/n).write_bytes(raw)
        pins[n]=dict(source=str(p),sha256=sha(p),snapshot_sha256=sha(SNAP/n),bytes=len(raw))
    write(HERE/'SOURCE_SNAPSHOT_001.json',dict(status='READ_ONLY_REVIEW_SNAPSHOT',sources=pins,
        fixture_script_sha256=sha(Path(__file__)),scope='No actual activation, cost receipt, seed or scientific data reads'))
    run_case('success_single',expect_reject=False,check=baseline_check)
    def two(s):
        s['proposal']['jobs']['fake_second']=copy.deepcopy(s['cfg'])
        s['proposal']['jobs']['fake_second']['output_directory_name']='fake_second_output'
        s['proposal']['ordered_job_names'].append('fake_second')
        s['proposal']['decision_documentation']['per_job_cost_and_information']['fake_second']={}
    run_case('success_serial_two_jobs_24_workers_each',two,expect_reject=False,check=baseline_check)
    for name,key in [('registration_pin','registration'),('controller_pin','pilot_controller'),('convergence_pin','pilot_convergence')]:
        run_case(name,post=lambda s,k=key:s['proposal'][k].update(sha256='0'*64))
    run_case('budget_pin',post=lambda s:(s['base']/'PART_B_BUDGET_START.json').write_bytes(b'{}'))
    run_case('expired_deadline',lambda s:s['budget'].update(hard_deadline_utc='2000-01-01T00:00:00Z'))
    run_case('naive_deadline',lambda s:s['budget'].update(hard_deadline_utc='2100-01-01T00:00:00'))
    run_case('future_allocation',lambda s:s['proposal'].update(allocation_registered_utc='2100-01-01T00:00:00Z'))
    run_case('allocation_before_pilot_end',lambda s:s['proposal'].update(allocation_registered_utc=s['stamp'](-90)))
    run_case('serial_sum_over_deadline',lambda s:(s['cfg'].update(wall_budget_seconds=7200)))
    run_case('reserve_zero',lambda s:s['proposal'].update(global_reserve_seconds=0))
    run_case('wall_over_eight_hours',lambda s:s['cfg'].update(wall_budget_seconds=28801))
    run_case('stricter_registered_wall_cap',lambda s:s['reg']['allocation_policy'].update(max_job_wall_seconds=29))
    run_case('workers25',lambda s:s['cfg']['sampler'].update(workers=25))
    run_case('workers_bool',lambda s:s['cfg']['sampler'].update(workers=True))
    run_case('partial_pilot',lambda s:s['conv'].update(accepted_for_analysis=False))
    run_case('pilot_cleanup_unpaid',lambda s:s['controller']['cleanup'].update(group_absent=False))
    run_case('negative_cost_counter',lambda s:s['conv']['cost'].update(source_calls=-1))
    run_case('static_job_replacement',lambda s:(s['proposal'].update(jobs={'fake_static_pilot':s['cfg']},ordered_job_names=['fake_static_pilot'])))
    run_case('duplicate_job_order',lambda s:s['proposal'].update(ordered_job_names=['fake_new','fake_new']))
    run_case('witness_outside_tunnel',lambda s:s['proposal'].update(witness_relative_to_Chatgpt='ORDEM_013_RINGDOWN/fake.md'))
    run_case('jobs_escape_root',lambda s:s['proposal'].update(jobs_relative_to_Chatgpt='../escape.json'))
    run_case('jobs_inside_sidecar',lambda s:s['proposal'].update(jobs_relative_to_Chatgpt='ORDEM_013_RINGDOWN/bis/e3_allocation_prepare/x.json'))
    run_case('unsafe_slug',lambda s:s['proposal'].update(slug='../escape'))
    run_case('output_slug_static_reuse',lambda s:s['cfg'].update(output_directory_name='fake_static_output'))
    for name,pathkey in [('existing_jobs','jobs_relative_to_Chatgpt'),('existing_witness','witness_relative_to_Chatgpt')]:
        run_case(name,post=lambda s,k=pathkey:write(s['root']/s['proposal'][k],{'sentinel':'PRESERVE'}))
    run_case('existing_allocation',post=lambda s:write(s['base']/'ORCAMENTO_40H.json',{'sentinel':'PRESERVE'}))
    def blind(s):
        s['cfg'].update(mode='blind_test',event='FAKE_BLIND',publication_metadata_review={})
    run_case('blind_hold_missing_resolution',blind)
    run_case('blind_documents_deferred_to_guard',lambda s:(blind(s),s['cfg'].update(data_quality_resolution={})),
             expect_reject=False,check=baseline_check)
    def symlink(s):
        escaped=s['folder']/'escaped_sidecar';escaped.mkdir()
        (s['side']/'candidates').symlink_to(escaped,target_is_directory=True)
    def link_check(s,error):
        escaped=s['folder']/'escaped_sidecar/candidate_fake/CANDIDATE_RECEIPT.json'
        return dict(ok=escaped.exists(),observed_defect='Writes follow candidates symlink outside sidecar, still inside own fixture tree')
    run_case('finding_symlink_output_escape',post=symlink,expect_reject=False,check=link_check)
    s=setup('finding_serialization_size_cap')
    payload=[0]*40000
    for _ in range(400):payload=[payload]
    s['proposal']['decision_documentation']['unpaid']=payload
    p=s['side']/'PROPOSAL_FAKE.json';write(p,s['proposal'])
    mod=module(s['side']/'render_allocation_candidates.py','size_fixture');captured=[]
    mod.publish_exclusive=lambda path,raw:captured.append(dict(name=path.name,bytes=len(raw),exceeds_limit=len(raw)>mod.LIMIT))
    before=sys.argv;sys.argv=[str(mod.__file__),str(p)]
    try:mod.main()
    finally:sys.argv=before
    RESULTS.append(dict(id='finding_output_size_no_enforcement',expectation='REPRODUCE_DEFECT_WITHOUT_WRITING_OVERSIZE',
        passed=any(r['exceeds_limit'] for r in captured),details=dict(input_bytes=p.stat().st_size,serialized=captured,
        interception='Only publisher replaced; original renderer serialization unmodified; oversized bytes never written')))
    guard_tests()
    for n,p in sources.items():
        if sha(p)!=pins[n]['sha256']:raise ValueError('Producer/source changed during audit: '+n)
    for p in HERE.rglob('*'):
        if p.is_file() and p.stat().st_size>LIMIT:raise ValueError('Oversized review artifact')
    write(HERE/'FIXTURE_RESULTS_001.json',dict(status='FINITE_METADATA_FIXTURES_COMPLETED',
        finished_utc=datetime.now(timezone.utc).isoformat(),cases=RESULTS,
        total=len(RESULTS),passed=sum(r['passed'] for r in RESULTS),failed=sum(not r['passed'] for r in RESULTS),
        scientific_execution=False,real_activation_or_jobs_publication=False,seed_reads=False,
        guard_scope='Only load_jobs on isolated fake metadata, never checked_registration/validate_launch or real runtime',
        fixture_script_sha256=sha(Path(__file__)),snapshot_manifest_sha256=sha(HERE/'SOURCE_SNAPSHOT_001.json')))
    print(json.dumps(dict(total=len(RESULTS),passed=sum(r['passed'] for r in RESULTS),
        failed=[r['id'] for r in RESULTS if not r['passed']],results_sha256=sha(HERE/'FIXTURE_RESULTS_001.json'))))


if __name__=='__main__':main()
