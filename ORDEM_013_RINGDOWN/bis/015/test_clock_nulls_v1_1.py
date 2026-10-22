"""Isolated R7 negative probes and null entry-point controls; no heavy simulation."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import ast,copy,hashlib,importlib.util,json,os,sys,time

B=Path(__file__).resolve().parents[2]
C=B/'bis/e2_code_v1_1'
D=B/'bis/015/t03/clock_nulls_tests_001'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.stat().st_size==len(raw)
    os.replace(temp,p)
def put(p,obj):write(p,(json.dumps(obj,sort_keys=True,allow_nan=False)+'\n').encode())

def main():
    wall=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False)
    sys.path.insert(0,str(C));import registration_guard as g
    root=D/'fixture';base=root/'ORDEM_013_RINGDOWN';notes=root/'TUNEL/DO_CHATGPT'
    notes.mkdir(parents=True);base.mkdir()
    g.BASE=base;g.ROOT=root
    def contained(name,root=None):
        rt=g.ROOT if root is None else root;p=(rt/name).resolve()
        if not p.is_relative_to(rt.resolve()):raise ValueError('Outside isolated fixture')
        return p
    g.contained=contained
    now=datetime.now(timezone.utc)
    issued=now-timedelta(minutes=20);release_time=now-timedelta(minutes=10);start=now-timedelta(minutes=5)
    first_note=notes/'ENTREGA_015_E2_REGISTRO_V1_1.md'
    first_path=base/'RINGDOWN_5SIGMA_V1_1.json'
    first=dict(registered_utc=issued.isoformat(),witness_relative_to_Chatgpt=first_note.relative_to(root).as_posix())
    put(first_path,first)
    def witness(p,digest,stamp,label):
        write(p,(label+': '+digest+'\nregistered_utc: '+stamp.isoformat()+'\n').encode())
        os.utime(p,(stamp.timestamp(),stamp.timestamp()))
    witness(first_note,sha(first_path),issued,'registro_sha256')
    source=base/'bis/FINAL_DELIVERY_RECEIPT.json';put(source,{'remaining_of_40_hours':35.01724298083333})
    free=root/'TUNEL/PARA_CHATGPT/RECIBO_015_MAQUINA_LIVRE.md'
    write(free,b'SYNTHETIC TEST ONLY; no authorization outside this fixture\n')
    os.utime(free,(release_time.timestamp(),release_time.timestamp()))
    budget=base/'bis/PART_015_BUDGET_START.json';note=notes/'ENTREGA_015_RELOGIO.md'
    rule=dict(budget_relative_to_Chatgpt=budget.relative_to(root).as_posix(),
        source_receipt_relative_to_Chatgpt=source.relative_to(root).as_posix(),source_receipt_sha256=sha(source),
        machine_free_receipt_relative_to_Chatgpt=free.relative_to(root).as_posix(),
        witness_relative_to_Chatgpt=note.relative_to(root).as_posix(),deadline_hours=168)
    reg=dict(budget_rule_v1_1=rule,budget_relative_to_Chatgpt=rule['budget_relative_to_Chatgpt'])
    clock=dict(start_utc=start.isoformat(),hard_deadline_utc=(start+timedelta(hours=168)).isoformat(),
        authorized_machine_hours=json.loads(source.read_bytes())['remaining_of_40_hours'],
        source_receipt_relative_to_Chatgpt=rule['source_receipt_relative_to_Chatgpt'],
        source_receipt_sha256=sha(source),recibo_maquina_livre_sha256=sha(free))
    results=[]
    def test(name,fn,refuse=False,expected=(ValueError,KeyError,FileNotFoundError,TimeoutError)):
        try:fn()
        except expected as e:
            if not refuse:raise
            results.append(dict(name=name,result='REFUSED',type=type(e).__name__,message=str(e)));return
        if refuse:raise AssertionError('Unexpected acceptance: '+name)
        results.append(dict(name=name,result='ACCEPTED'))
    def reset(obj=None):
        put(budget,clock if obj is None else obj)
        witness(note,sha(budget),now-timedelta(minutes=1),'budget_sha256')
    test('missing_clock',lambda:g.time_guard(reg),True)
    reset();test('valid_clock',lambda:g.time_guard(reg))
    mutated=copy.deepcopy(reg);mutated['registered_utc']=now.isoformat()
    test('later_subamendment_does_not_restart_clock',lambda:g.time_guard(mutated))
    for label,key,val in [
        ('extra_schema_field','extra',True),('bool_hours','authorized_machine_hours',True),
        ('increased_hours','authorized_machine_hours',36),('rounded_hours','authorized_machine_hours',35.017),
        ('wrong_source','source_receipt_relative_to_Chatgpt','elsewhere'),
        ('wrong_source_hash','source_receipt_sha256','0'*64),
        ('wrong_release_hash','recibo_maquina_livre_sha256','0'*64),
        ('wrong_deadline','hard_deadline_utc',(start+timedelta(hours=169)).isoformat()),
        ('future_start','start_utc',(now+timedelta(days=1)).isoformat()),
        ('start_before_release','start_utc',(release_time-timedelta(seconds=1)).isoformat()),
        ('timezone_absent','start_utc',start.replace(tzinfo=None).isoformat())]:
        m=copy.deepcopy(clock);m[key]=val;reset(m);test(label,lambda:g.time_guard(reg),True)
    reset();write(note,b'budget_sha256: '+b'0'*64+b'\nregistered_utc: '+now.isoformat().encode()+b'\n')
    test('witness_hash_changed',lambda:g.time_guard(reg),True)
    reset();write(note,note.read_bytes()+b'budget_sha256: '+sha(budget).encode()+b'\n')
    test('duplicate_witness_hash',lambda:g.time_guard(reg),True)
    reset();old=free.read_bytes();write(free,b'CHANGED');test('release_content_changed',lambda:g.time_guard(reg),True)
    write(free,old);os.utime(free,(release_time.timestamp(),release_time.timestamp()))
    original=source.read_bytes();put(source,{'remaining_of_40_hours':99});test('historical_source_changed',lambda:g.time_guard(reg),True);write(source,original)
    m=copy.deepcopy(reg);m['budget_sha256']='0'*64;test('premature_clock_hash',lambda:g.time_guard(m),True)
    m=copy.deepcopy(reg);m['budget_rule_v1_1']['deadline_hours']=169;test('different_deadline_rule',lambda:g.time_guard(m),True)
    m=copy.deepcopy(reg);m['budget_rule_v1_1']['budget_relative_to_Chatgpt']='ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json'
    test('V1_clock_not_reused',lambda:g.time_guard(m),True)
    opening=notes/'ENTREGA_TEST_ABERTURA.md';write(opening,b'SYNTHETIC OPERATOR LIMIT = 10 HOURS\n')
    m=copy.deepcopy(reg);m['budget_rule_v1_1']['operator_reduction']=dict(opening_relative_to_Chatgpt=opening.relative_to(root).as_posix(),opening_sha256=sha(opening),authorized_machine_hours=10)
    c=copy.deepcopy(clock);c.update(authorized_machine_hours=10,source_receipt_relative_to_Chatgpt=opening.relative_to(root).as_posix(),source_receipt_sha256=sha(opening))
    reset(c);test('explicit_pinned_lower_budget',lambda:g.time_guard(m))
    c['authorized_machine_hours']=35;reset(c);test('lower_budget_not_ignored',lambda:g.time_guard(m),True)
    reset()
    # Expiry is reached only after all provenance/chronology checks pass.
    ancient=now-timedelta(days=10);first['registered_utc']=ancient.isoformat();put(first_path,first);witness(first_note,sha(first_path),ancient,'registro_sha256')
    os.utime(free,(ancient.timestamp(),ancient.timestamp()))
    c=copy.deepcopy(clock);c['start_utc']=(ancient+timedelta(hours=1)).isoformat();c['hard_deadline_utc']=(ancient+timedelta(hours=169)).isoformat()
    reset(c);test('expired_clock',lambda:g.time_guard(reg),True,expected=(TimeoutError,))
    first['registered_utc']=issued.isoformat();put(first_path,first);witness(first_note,sha(first_path),issued,'registro_sha256');os.utime(free,(release_time.timestamp(),release_time.timestamp()));reset()
    nullreg={'nulls':{'cells':{'OLD_CELL':{}}},'nulls_v1_1':{'cells':{'NEW_CELL':{'draws':1}}}}
    test('new_null_id_allowed',lambda:g.new_null_cells(nullreg))
    for label,cells in [('old_null_id_refused',{'OLD_CELL':{}}),('null_path_escape',{'../bad':{}}),('null_wrong_container',[])]:
        m=copy.deepcopy(nullreg);m['nulls_v1_1']['cells']=cells;test(label,lambda:g.new_null_cells(m),True)
    # Import actual entry points in the pinned scientific interpreter, replacing authorization
    # only inside this fixture. No random draws, native waveforms, seed reads or subprocesses.
    import null_runner as runner
    runner.checked_registration=lambda:(nullreg,'a'*64);runner.BASE=base
    sys.argv=['null_runner.py','--cell','OLD_CELL']
    test('runner_old_id_before_simulation',runner.main,True)
    import null_campaign as campaign
    badreg=copy.deepcopy(nullreg);badreg['nulls_v1_1']['cells']['OLD_CELL']={}
    campaign.checked_registration=lambda:(badreg,'a'*64);campaign.BASE=base
    test('campaign_old_id_before_subprocess',campaign.main,True)
    # Structural proof only for versioned output location, not a campaign execution.
    text=(C/'null_campaign.py').read_text();assert 'RESULT_E2_NULL_CAMPAIGN_V1_1_' in text
    assert "out=BASE/'bis/RESULT_E2_NULL_CAMPAIGN.json'" not in text
    results.append(dict(name='campaign_receipt_new_version',result='AST_AND_SOURCE_CHECK'))
    frozen=json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())
    roots=[(B/'bis/e2_code',frozen['own_code_tree_sha256'])]
    roots += [(B.parent/x['relative_to_Chatgpt'],x['files_sha256']) for x in frozen['extra_code_roots']]
    for rt,pins in roots:assert {p.relative_to(rt).as_posix():sha(p) for p in rt.rglob('*.py')}==pins
    assert not (B/'bis/PART_015_BUDGET_START.json').exists()
    result=dict(status='R7_AND_NULL_ENTRY_CONTROLS_PASSED_NOT_REGISTERED',tests=results,
        files_sha256={n:sha(C/n) for n in ('registration_guard.py','null_runner.py','null_campaign.py')},
        old_code_roots_unchanged=True,real_clock_created=False,heavy_jobs=0,seed_read=False,
        wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
        scope='Fixture clock checks and refusal at actual null entry points; full activation/registration still pending')
    put(D/'RESULT.json',result)
    print(json.dumps({k:result[k] for k in ('status','wall_seconds','cpu_seconds','old_code_roots_unchanged')}|{'tests':len(results)}))

if __name__=='__main__':main()
