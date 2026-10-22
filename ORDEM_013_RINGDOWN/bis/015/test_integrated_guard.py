"""Exercise actual activation and allocation readers with isolated synthetic witnesses."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,copy,hashlib,os,sys,time
B=Path(__file__).resolve().parents[2];C=B/'bis/e2_code_v1_1';D=B/'bis/015/t03/guard_integration_tests_001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,obj):
    raw=obj if isinstance(obj,bytes) else (json.dumps(obj,sort_keys=True,allow_nan=False)+'\n').encode()
    p.parent.mkdir(parents=True,exist_ok=True);temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.stat().st_size==len(raw);os.replace(temp,p)
def main():
    begin=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False)
    sys.path.insert(0,str(C));import registration_guard as g
    root=D/'fixture';base=root/'ORDEM_013_RINGDOWN';notes=root/'TUNEL/DO_CHATGPT';notes.mkdir(parents=True);base.mkdir()
    g.BASE=base;g.ROOT=root
    def contained(name,root=None):
        rt=g.ROOT if root is None else root;p=(rt/name).resolve()
        if not p.is_relative_to(rt.resolve()):raise ValueError('Outside fixture')
        return p
    g.contained=contained
    now=datetime.now(timezone.utc);t0=(now-timedelta(minutes=20)).isoformat();t1=(now-timedelta(minutes=10)).isoformat();t2=(now-timedelta(minutes=5)).isoformat();t3=(now-timedelta(minutes=2)).isoformat()
    def witness(p,digest,issued,label='registro_sha256'):
        put(p,(label+': '+digest+'\nregistered_utc: '+issued+'\n').encode());stamp=datetime.fromisoformat(issued).timestamp();os.utime(p,(stamp,stamp))
    original=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    orig=copy.deepcopy(original);orig['registered_utc']=t0;orig['witness_relative_to_Chatgpt']='TUNEL/DO_CHATGPT/TEST_V1.md'
    op=base/'RINGDOWN_5SIGMA_V1.json';on=notes/'TEST_V1.md';put(op,orig);witness(on,sha(op),t0);g.V1_PIN=sha(op);g.V1_WITNESS_PIN=sha(on)
    reg=copy.deepcopy(orig)
    reg.update(parent_registration_sha256=sha(op),v1_witness_sha256=sha(on),
        registration_id='SYNTHETIC_V1_1',registered_utc=t1,
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_E2_REGISTRO_V1_1.md',
        statistical_subobject_sha256=g.statistical_digest(orig),nulls_v1_1={'cells':{'NEW':{}}},
        pe_jobs={'NEW_JOB':{'mode':'calibration','wall_budget_seconds':100}},test_candidates_amendments=[],
        allocation_policy={'pattern':'ORCAMENTO_015_v*.json','max_job_wall_seconds':28800},
        own_code_tree_sha256={p.relative_to(C).as_posix():sha(p) for p in C.rglob('*.py')},extra_code_roots=[],
        input_pins_relative_to_Chatgpt={})
    a=base/'bis/015';source=B/'bis/015/t03';target=a/'source';target.mkdir(parents=True)
    for name in ('R5/INPUT_MANIFEST.json','R5/CONFIG_2048_INPUT.json','R5/CONFIG_4096_RESERVED_INPUT.json','R5/ITEMS.json','R5/generation_4096/RESULT.json','R5_SOURCE_CLOSING.json'):
        put(target/name,(source/name).read_bytes())
    r5=target/'R5/generation_4096/RESULT.json';scope=target/'R5_SOURCE_CLOSING.json';manifest=target/'R5/INPUT_MANIFEST.json'
    probes=a/'PROBES_FIXTURE.json';receipt=a/'E2_V1_1_REGISTRATION_RECEIPT.json';cp=base/'RINGDOWN_5SIGMA_V1_1.json';cn=notes/'ENTREGA_015_E2_REGISTRO_V1_1.md'
    reg['activation_v1_1']=dict(receipt_relative_to_Chatgpt=receipt.relative_to(root).as_posix(),probes_result_relative_to_Chatgpt=probes.relative_to(root).as_posix(),
        qualification_R5_relative_to_Chatgpt=r5.relative_to(root).as_posix(),qualification_scope_relative_to_Chatgpt=scope.relative_to(root).as_posix(),
        qualification_scope_sha256=sha(scope),qualification_inputs_relative_to_Chatgpt=manifest.relative_to(root).as_posix())
    # Only this fixture substitutes synthetic probe evidence to test the reader.
    proof=dict(status='V1_1_GUARD_PROBES_PASSED',own_code_tree_sha256=reg['own_code_tree_sha256'],statistical_subobject_sha256=reg['statistical_subobject_sha256'],
        tests=[{'passed':True,'name':'SYNTHETIC reader fixture, not a production attestation'}],finished_utc=t0)
    put(probes,proof)
    runtime=B.parent/original['runtime_manifest_relative_to_Chatgpt'];runtime_copy=a/'RUNTIME.json';put(runtime_copy,runtime.read_bytes())
    reg['runtime_manifest_relative_to_Chatgpt']=runtime_copy.relative_to(root).as_posix();reg['runtime_manifest_sha256']=sha(runtime_copy)
    reg['budget_relative_to_Chatgpt']='ORDEM_013_RINGDOWN/bis/PART_015_BUDGET_START.json';reg.pop('budget_sha256',None)
    budget_source=base/'bis/FINAL_DELIVERY_RECEIPT.json';put(budget_source,(B/'bis/FINAL_DELIVERY_RECEIPT.json').read_bytes())
    reg['budget_rule_v1_1']=dict(budget_relative_to_Chatgpt=reg['budget_relative_to_Chatgpt'],source_receipt_relative_to_Chatgpt=budget_source.relative_to(root).as_posix(),
        source_receipt_sha256=sha(budget_source),machine_free_receipt_relative_to_Chatgpt='TUNEL/PARA_CHATGPT/RECIBO_015_MAQUINA_LIVRE.md',
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_RELOGIO.md',deadline_hours=168)
    def publish(current=None):
        value=reg if current is None else current;put(cp,value);witness(cn,sha(cp),value['registered_utc'])
        marker=dict(status='E2_V1_1_REGISTERED',registration_sha256=sha(cp),witness_sha256=sha(cn),probes_result_sha256=sha(probes),qualification_R5_sha256=sha(r5))
        put(receipt,marker);return marker
    marker=publish();tests=[]
    def check(name,fn,refuse=False,types=(ValueError,KeyError,FileNotFoundError)):
        try:fn()
        except types as e:
            if not refuse:raise
            tests.append(dict(name=name,passed=True,observed='REFUSED',exception=type(e).__name__,message=str(e)));return
        if refuse:raise AssertionError('Unexpected acceptance: '+name)
        tests.append(dict(name=name,passed=True,observed='ACCEPTED'))
    check('valid_activation_bound_to_code_and_R5',lambda:g.check_activation_v1_1(reg,sha(cp),cn))
    for label,key,val in [('wrong_registration','registration_sha256','0'*64),('wrong_witness','witness_sha256','0'*64),
                          ('wrong_probes','probes_result_sha256','0'*64),('wrong_R5','qualification_R5_sha256','0'*64),('wrong_status','status','E2_ACTIVATION_COMPLETE')]:
        m=copy.deepcopy(marker);m[key]=val;put(receipt,m);check(label,lambda:g.check_activation_v1_1(reg,sha(cp),cn),True)
    put(receipt,marker)
    for label,key,val in [('probes_failed','tests',[{'passed':False}]),('probes_empty','tests',[]),('probes_other_tree','own_code_tree_sha256',{}),
                         ('probes_after_registration','finished_utc',t2),('probes_different_statistics','statistical_subobject_sha256','0'*64)]:
        m=copy.deepcopy(proof);m[key]=val;put(probes,m);publish();check(label,lambda:g.check_activation_v1_1(reg,sha(cp),cn),True)
    put(probes,proof);marker=publish()
    original_r5=r5.read_bytes();q=json.loads(original_r5);q['status_counts']={'FINITE_WAVEFORM':1014,'DOMAIN_NONE':1};put(r5,q);publish()
    check('R5_EDOM_not_qualified',lambda:g.check_activation_v1_1(reg,sha(cp),cn),True);put(r5,original_r5);marker=publish()
    old_scope=scope.read_bytes();q=json.loads(old_scope);q['source_path_function_hashes']['pe_runner.py:build_priors']='0'*64;put(scope,q)
    m=copy.deepcopy(reg);m['activation_v1_1']['qualification_scope_sha256']=sha(scope);publish(m)
    check('R5_build_priors_changed',lambda:g.check_activation_v1_1(m,sha(cp),cn),True);put(scope,old_scope);marker=publish()
    m=copy.deepcopy(reg);m['status']='DRAFT';publish(m);check('inactive_amendment',g.load_registration_chain_v1_1,True);publish()
    check('full_entry_reaches_missing_R7_after_pinned_runtime',g.checked_registration,True,types=(FileNotFoundError,))
    # Complete synthetic R7, still never creating the real clock.
    release=contained(reg['budget_rule_v1_1']['machine_free_receipt_relative_to_Chatgpt']);put(release,b'SYNTHETIC machine free\n')
    stamp=datetime.fromisoformat(t2).timestamp();os.utime(release,(stamp,stamp))
    budget=contained(reg['budget_relative_to_Chatgpt']);clock=dict(start_utc=t3,hard_deadline_utc=(datetime.fromisoformat(t3)+timedelta(hours=168)).isoformat(),
        authorized_machine_hours=json.loads(budget_source.read_bytes())['remaining_of_40_hours'],source_receipt_relative_to_Chatgpt=budget_source.relative_to(root).as_posix(),
        source_receipt_sha256=sha(budget_source),recibo_maquina_livre_sha256=sha(release))
    put(budget,clock);witness(notes/'ENTREGA_015_RELOGIO.md',sha(budget),t3,'budget_sha256')
    check('full_checked_registration_pinned_runtime_fixture',g.checked_registration)
    check('missing_external_blind_review',lambda:g.check_blind_activation(reg),True)
    review=root/'TUNEL/PARA_CHATGPT/RECIBO_015_V1_1_AUDITADA.md';put(review,('registro_sha256: '+sha(cp)+'\n').encode())
    check('external_blind_receipt_matches_registration',lambda:g.check_blind_activation(reg))
    put(review,('registro_sha256: '+'0'*64+'\n').encode());check('external_receipt_other_registration',lambda:g.check_blind_activation(reg),True)
    # Allocation chain uses real guard code. Only calibration job stubs are used here.
    digest=sha(cp)
    check('empty_allocation_chain',lambda:g.load_jobs(reg,digest))
    one=base/'ORCAMENTO_015_v1.json';two=base/'ORCAMENTO_015_v2.json'
    config1=a/'ALLOCATION1.json';config2=a/'ALLOCATION2.json'
    extra1=dict(schema_version='E2_PE_JOBS_V2',parent_registration_sha256=digest,jobs={'CAL2':{'mode':'calibration','wall_budget_seconds':200}},downloads={})
    put(config1,extra1)
    alloc1=dict(supersedes_sha256=None,parent_registration_sha256=digest,registered_utc=t2,
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v1.md',jobs_relative_to_Chatgpt=config1.relative_to(root).as_posix(),jobs_sha256=sha(config1))
    def alloc(path,obj):
        put(path,obj);witness(contained(obj['witness_relative_to_Chatgpt']),sha(path),obj['registered_utc'],'allocation_sha256')
    alloc(one,alloc1);check('one_allocation_adds_job',lambda:assert_jobs(g.load_jobs(reg,digest),{'NEW_JOB','CAL2'}))
    extra2=copy.deepcopy(extra1);extra2['jobs']['CAL3']={'mode':'calibration','wall_budget_seconds':300};put(config2,extra2)
    alloc2=dict(supersedes_sha256=sha(one),parent_registration_sha256=digest,registered_utc=t3,
        witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v2.md',jobs_relative_to_Chatgpt=config2.relative_to(root).as_posix(),jobs_sha256=sha(config2))
    alloc(two,alloc2);check('latest_cumulative_allocation',lambda:assert_jobs(g.load_jobs(reg,digest),{'NEW_JOB','CAL2','CAL3'}))
    for label,key,val in [('allocation_bad_parent','supersedes_sha256','0'*64),('allocation_unknown_registration','parent_registration_sha256','0'*64),
                          ('allocation_bad_config_hash','jobs_sha256','0'*64),('allocation_reversed_time','registered_utc',t0)]:
        m=copy.deepcopy(alloc2);m[key]=val;alloc(two,m);check(label,lambda:g.load_jobs(reg,digest),True)
    alloc(two,alloc2)
    for label,modify in [
      ('allocated_job_replaced',lambda x:x['jobs']['CAL2'].update(wall_budget_seconds=201)),
      ('allocated_job_removed',lambda x:x['jobs'].pop('CAL2')),
      ('eight_hour_cap',lambda x:x['jobs']['CAL3'].update(wall_budget_seconds=28801)),
      ('historical_job_reused',lambda x:x['jobs'].update({next(iter(orig['pe_jobs'])):{'mode':'calibration','wall_budget_seconds':100}})),
      ('unlicensed_download',lambda x:x['downloads'].update({'NEW_DOWNLOAD':{'url':'fixture'}}))]:
        m=copy.deepcopy(extra2);modify(m);put(config2,m);a2=copy.deepcopy(alloc2);a2['jobs_sha256']=sha(config2);alloc(two,a2)
        check(label,lambda:g.load_jobs(reg,digest),True)
    put(config2,extra2);alloc(two,alloc2)
    gap=base/'ORCAMENTO_015_v3.json';two.rename(gap);check('allocation_gap',lambda:g.load_jobs(reg,digest),True);gap.rename(two)
    # Reading after a subsequent registration still recognizes an earlier witnessed allocation.
    sp=base/'RINGDOWN_5SIGMA_V1_1_1.json';sn=notes/'ENTREGA_015_E2_REGISTRO_V1_1_1.md'
    r2=copy.deepcopy(reg);r2.update(parent_registration_sha256=digest,registered_utc=t2,witness_relative_to_Chatgpt=sn.relative_to(root).as_posix())
    put(sp,r2);witness(sn,sha(sp),t2)
    check('allocation_ancestor_retained_after_amendment',lambda:assert_jobs(g.load_jobs(r2,sha(sp)),{'NEW_JOB','CAL2','CAL3'}))
    check('allocation_caller_stale',lambda:g.load_jobs(reg,digest),True)
    assert not (B/'bis/PART_015_BUDGET_START.json').exists()
    real=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    for rt,pins in [(B/'bis/e2_code',real['own_code_tree_sha256'])]+[(B.parent/x['relative_to_Chatgpt'],x['files_sha256']) for x in real['extra_code_roots']]:
        assert {p.relative_to(rt).as_posix():sha(p) for p in rt.rglob('*.py')}==pins
    result=dict(status='INTEGRATED_GUARD_CONTROLS_PASSED_SYNTHETIC_FIXTURE_ONLY',tests=tests,guard_sha256=sha(C/'registration_guard.py'),
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-begin,real_registration_activated=False,seed_read=False,heavy_jobs=0,
        scope='Actual entry, pinned runtime, R5 source artifacts, synthetic registration/witness/probes/clock; allocation and management receipt refusal tests')
    put(D/'RESULT.json',result);print(json.dumps({k:result[k] for k in ('status','cpu_seconds','wall_seconds')}|{'tests':len(tests)}))
def assert_jobs(jobs,names):assert set(jobs)==names
if __name__=='__main__':main()
