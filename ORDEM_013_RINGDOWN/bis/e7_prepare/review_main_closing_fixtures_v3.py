"""Only changed main boundaries; deterministic mocks, no science/network."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
from unittest.mock import patch
import ast,base64,copy,hashlib,io,json,os,sys,tempfile,types,contextlib,subprocess
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;BASE=OUT.parents[1];CODE=BASE/'bis/e2_code'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    p=OUT/name;t=p.with_suffix(p.suffix+'.pending');raw=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert t.stat().st_size==len(raw)
    os.link(t,p);t.unlink()
names=[p.relative_to(BASE).as_posix() for p in sorted(CODE.glob('*.py'))]+['bis/E2_DESIGN_DRAFT_003.json']
snapshot={}
for name in names:
    raw=(BASE/name).read_bytes();snapshot[name]=dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),bytes_base64=base64.b64encode(raw).decode())
helper_raw=(OUT/'review_main_negative_fixtures_v2.py').read_bytes()
save('MAIN_CODE_REVIEW_SNAPSHOT_V3.json',dict(status='FROZEN_BYTES_FOR_CHANGED_BOUNDARIES',
 created_utc=datetime.now(timezone.utc).isoformat(),files=snapshot,
 fixture_helper_sha256=hashlib.sha256(helper_raw).hexdigest()))
def module(name):
    m=types.ModuleType(name);m.__file__=str(CODE/(name+'.py'));sys.modules[name]=m
    exec(compile(base64.b64decode(snapshot['bis/e2_code/'+name+'.py']['bytes_base64']),m.__file__,'exec'),m.__dict__)
    return m
guard=module('registration_guard');campaign=module('null_campaign');fetch=module('fetch_registered');pe=module('pe_runner')
draft=json.loads(base64.b64decode(snapshot['bis/E2_DESIGN_DRAFT_003.json']['bytes_base64']))
results=[]
def record(name,passed,detail):results.append(dict(name=name,passed=bool(passed),detail=detail))
# Reuse ONLY this prior function, never execute the old script or its campaign.
node=next(n for n in ast.parse(helper_raw).body if isinstance(n,ast.FunctionDef) and n.name=='campaign_case')
exec(compile(ast.Module(body=[node],type_ignores=[]),'<pinned prior campaign helper>','exec'))
campaign_case('changed_campaign_deadline_exception_receipt','guard_error')
campaign_case('changed_campaign_bad_receipt_exception_receipt','bad_receipt')
campaign_case('changed_campaign_timeout_bytes_receipt','timeout')

with tempfile.TemporaryDirectory(dir=OUT) as tmp:
    root=Path(tmp);(root/'evidence.txt').write_bytes(b'SYNTHETIC_METADATA_ONLY')
    now=datetime.now(timezone.utc).isoformat()
    review=dict(relative_to_Chatgpt='evidence.txt',sha256=sha(root/'evidence.txt'),reviewed_utc=now,
                review_passed=True,scope='SYNTHETIC_SCOPE',method='SYNTHETIC_METHOD')
    holds=[e for e,v in draft['test_candidates'].items() if v.get('data_quality_hold')]
    def check_job(event,variant,dynamic=False):
        job=dict(event=event,mode='blind_test',publication_metadata_review=copy.deepcopy(review),wall_budget_seconds=1)
        if variant!='missing':job['data_quality_resolution']=copy.deepcopy(review)
        if variant=='failed':job['data_quality_resolution']['review_passed']=False
        if variant=='wrong_pin':job['data_quality_resolution']['sha256']='0'*64
        reg=copy.deepcopy(draft);reg['registered_utc']='2026-01-01T00:00:00+00:00';reg['allocation_policy']=None
        reg['pe_jobs']={'FIXTURE':job}
        if dynamic:
            reg['pe_jobs']={};reg['allocation_policy']=dict(relative_to_Chatgpt='allocation.json',max_job_wall_seconds=2)
            raw=json.dumps(dict(parent_registration_sha256='a'*64,schema_version='E2_PE_JOBS_V2',jobs={'FIXTURE':job})).encode()
            (root/'jobs.json').write_bytes(raw)
            (root/'allocation.json').write_text(json.dumps(dict(parent_registration_sha256='a'*64,
                witness_relative_to_Chatgpt='unused',registered_utc=now,jobs_relative_to_Chatgpt='jobs.json',
                jobs_sha256=sha(root/'jobs.json'))))
        error=None
        with patch.object(guard,'contained',lambda p:root/p),patch.object(guard,'check_witness',lambda *a:None):
            try:guard.load_jobs(reg,'a'*64)
            except (ValueError,KeyError) as exc:error=type(exc).__name__+': '+str(exc)
        record(('dynamic_' if dynamic else 'registered_')+'quality_hold_'+variant+'_'+event,
               (error is None) if variant=='valid' else (error is not None),
               dict(error=error,boundary='load_jobs; witness mocked, evidence SHA/time/review checks real'))
    for event in holds:check_job(event,'missing')
    for variant in ('failed','wrong_pin','valid'):check_job(holds[0],variant)
    for variant in ('missing','wrong_pin','valid'):check_job(holds[0],variant,True)

# No real timer is installed: exercise handler and cleanup deterministically.
installed={};timer_calls=[];previous=object()
def set_handler(sig,value):installed['handler']=value
def interrupted(*args):installed['handler'](None,None)
with patch.object(fetch,'time_guard',lambda r:datetime.now(timezone.utc)+timedelta(seconds=60)),\
     patch.object(fetch.signal,'getitimer',lambda *a:(0.,0.)),\
     patch.object(fetch.signal,'getsignal',lambda *a:previous),\
     patch.object(fetch.signal,'signal',set_handler),\
     patch.object(fetch.signal,'setitimer',lambda *a:timer_calls.append(a)),\
     patch.object(fetch,'_fetch',interrupted):
    try:fetch.fetch({},'a'*64,'fixture',{});record('fetch_wall_handler_interrupt',False,'returned')
    except TimeoutError as e:
        record('fetch_wall_handler_interrupt',str(e)=='Registered download wall deadline reached',str(e))
record('fetch_wall_cleanup_restores_timer_and_handler',len(timer_calls)==2 and timer_calls[-1][1]==0. and installed['handler'] is previous,
       'Mock timer only; no live socket, transfer, signal or timing benchmark')
with patch.object(fetch.signal,'getitimer',lambda *a:(1.,0.)),patch.object(fetch,'_fetch',side_effect=AssertionError('boundary crossed')):
    try:fetch.fetch({},'a'*64,'fixture',{});record('fetch_existing_timer_refused',False,'returned')
    except RuntimeError as e:record('fetch_existing_timer_refused','existing wall timer' in str(e),str(e))

cfg=draft['pe_jobs']['GW250114_PILOT']
try:
    pe.validate_config(cfg)
    record('draft003_16s_window_static_contract',cfg['duration_s']==16 and cfg['segment_start_GPS']==1420878129,
           dict(duration_s=cfg['duration_s'],segment_start_GPS=cfg['segment_start_GPS'],scope='validate_config only'))
except Exception as e:record('draft003_16s_window_static_contract',False,str(e))
record('draft003_GPS_anchor_matches_pilot',draft.get('event_reference_GPS',{}).get(cfg['event'])==cfg['event_GPS'],
       dict(event=cfg['event'],anchor=draft.get('event_reference_GPS',{}).get(cfg['event']),event_GPS=cfg['event_GPS']))
record('draft003_exactly_25_registered_null_cells',len(draft['nulls']['cells'])==25,len(draft['nulls']['cells']))
source=base64.b64decode(snapshot['bis/e2_code/pe_runner.py']['bytes_base64']).decode()
record('remnant_bridge_present_static_only','from remnant_conversion import derive' in source and
       'derived,remnant_receipt=derive(columns,cfg,lambda:time_guard(reg))' in source and
       "'PRIVATE_REMNANT_CONVERSION.json'" in source,'Presence check only, not PE execution or numerical fit')
value=dict(status='CHANGED_BOUNDARIES_REVIEW_V3',snapshot='MAIN_CODE_REVIEW_SNAPSHOT_V3.json',
 snapshot_sha256=sha(OUT/'MAIN_CODE_REVIEW_SNAPSHOT_V3.json'),fixtures=results,
 passed=sum(r['passed'] for r in results),failed=sum(not r['passed'] for r in results),
 changed_live_since_snapshot=[n for n,v in snapshot.items() if sha(BASE/n)!=v['sha256']],
 no_real_MC_PE_waveform_strain_network=True,
 correction_to_v2='authorize_event classifies identity; load_jobs enforces pinned hold-resolution before launch. Four v2 authorize_event probes alone did not establish a launch bypass.')
save('MAIN_CODE_REVIEW_FIXTURES_V3.json',value)
print(json.dumps(value,ensure_ascii=False,indent=2))
