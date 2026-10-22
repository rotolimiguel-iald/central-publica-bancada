"""Pinned finite negative fixtures. No network, MC, PE, waveform or strain."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
import base64, copy, hashlib, io, json, os, sys, tempfile, types, contextlib, subprocess
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent; BASE=OUT.parents[1]; CODE=BASE/'bis/e2_code'
def sha_bytes(raw):return hashlib.sha256(raw).hexdigest()
def sha(p):return sha_bytes(p.read_bytes())
def save(name,value):
    raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    p=OUT/name; tmp=p.with_suffix(p.suffix+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise IOError('short write')
    os.link(tmp,p);tmp.unlink()
names=[p.relative_to(BASE).as_posix() for p in sorted(CODE.glob('*.py'))]
names+=['bis/E2_DESIGN_DRAFT_002.json','bis/E2_REMNANT_BRIDGE_INPUT.json',
        'bis/e2_publication_census/PUBLICATION_CENSUS.json','refeito/prepare_e2_design_013bis.py']
snapshot={}
for name in names:
    raw=(BASE/name).read_bytes();snapshot[name]={'sha256':sha_bytes(raw),'bytes':len(raw),'bytes_base64':base64.b64encode(raw).decode()}
save('MAIN_CODE_REVIEW_SNAPSHOT_V2.json',{'status':'FROZEN_BYTES_FOR_NEGATIVE_FIXTURES',
     'created_utc':datetime.now(timezone.utc).isoformat(),'files':snapshot})
def read(name):return json.loads(base64.b64decode(snapshot[name]['bytes_base64']))
def module(name):
    m=types.ModuleType(name);m.__file__=str(CODE/(name+'.py'));sys.modules[name]=m
    exec(compile(base64.b64decode(snapshot['bis/e2_code/'+name+'.py']['bytes_base64']),m.__file__,'exec'),m.__dict__)
    return m
guard=module('registration_guard');source=module('pseob_source');inj=module('injection_design')
fetch=module('fetch_registered');rem=module('remnant_conversion');campaign=module('null_campaign');pe=module('pe_runner')
draft=read('bis/E2_DESIGN_DRAFT_002.json'); bridge=read('bis/E2_REMNANT_BRIDGE_INPUT.json')
results=[]
def record(name,passed,detail):results.append({'name':name,'passed':bool(passed),'detail':detail})
def reject(name,call,text=None):
    try:call();record(name,False,'ACCEPTED_UNEXPECTEDLY')
    except (ValueError,KeyError,TimeoutError) as e:
        record(name,text is None or text.lower() in str(e).lower(),type(e).__name__+': '+str(e))

# No waveform: the fake generator raises at its construction boundary.
class Boundary(Exception):pass
def boundary(**kw):raise Boundary('GENERATOR_BOUNDARY_ONLY_NO_WAVEFORM')
fake_bilby=types.SimpleNamespace(gw=types.SimpleNamespace(WaveformGenerator=boundary))
def ifo(start=100.,delay=0.):
    return types.SimpleNamespace(name='H1',strain_data=types.SimpleNamespace(start_time=start,time_within_data=lambda t:start<=t<start+8),
                                  time_delay_from_geocenter=lambda *a:delay)
cfg={'mode':'calibration','event':'FIXTURE','event_GPS':200.,'segment_start_GPS':100.,'duration_s':8.,
     'offsource_exclusion_s':16.,'onsource_roll_off_s':.2,'sample_rate_hz':4096,
     'minimum_frequency_hz':20.,'maximum_frequency_hz':1024.,'reference_frequency_hz':20.,
     'data':{'H1':{'onsource_path':'fixture','offsource_path':'fixture','onsource_sha256':'same','offsource_sha256':'same'}},
     'injection':{'family':'IMRPhenomXPHM','noise_kind':'REAL_OFFSOURCE','target_network_optimal_SNR':20,
                  'parameters':{'dtau220':0.,'dtau440':0.,'domega220':0.,'domega440':0.,'geocent_time':104.,
                                'luminosity_distance':400.,'ra':0.,'dec':0.}}}
reg={'calibration_event_ids':['FIXTURE'],'event_reference_GPS':{'FIXTURE':200.}}
with patch.dict(sys.modules,{'bilby':fake_bilby}):
    bad=copy.deepcopy(cfg);bad['event_GPS']=104.
    reject('injection_label_cannot_move_real_GPS',lambda:inj.inject_into_ifos([ifo()],bad,reg),'metadata anchor')
    bad=copy.deepcopy(cfg);bad['segment_start_GPS']=196.;bad['injection']['parameters']['geocent_time']=200.
    reject('injection_whole_window_real_event_overlap',lambda:inj.inject_into_ifos([ifo(196.)],bad,reg),'protected real-event')
    reject('injection_missing_GPS_anchor',lambda:inj.inject_into_ifos([ifo()],cfg,{'calibration_event_ids':['FIXTURE'],'event_reference_GPS':{}}),'metadata anchor')
    bad=copy.deepcopy(cfg);bad['offsource_exclusion_s']=0.
    reject('injection_nonpositive_exclusion',lambda:inj.inject_into_ifos([ifo()],bad,reg),'exclusion')
    reject('injection_detector_arrival_inside_taper',lambda:inj.inject_into_ifos([ifo(delay=3.9)],cfg,reg),'tapered')
    bad=copy.deepcopy(cfg);bad['injection']['parameters']['dtau220']=.01
    reject('second_family_non_GR_refused',lambda:inj.inject_into_ifos([ifo()],bad,reg),'non-GR XPHM')
    try:inj.inject_into_ifos([ifo()],cfg,reg);record('injection_disjoint_valid_reaches_boundary',False,'unexpected return')
    except Boundary:record('injection_disjoint_valid_reaches_boundary',True,'No generator or waveform constructed')

# Named Planck18 equality/hash failures before any remnant fit; fit traps prove this.
import lalsimulation as ls
columns={'mass_1':[40.,30.],'mass_2':[30.,5.],'chi_1':[.2,-.9],'chi_2':[-.1,-.9],'luminosity_distance':[400.,800.]}
with patch.object(ls,'SimIMREOBFinalMassSpin',side_effect=AssertionError('No real fit permitted in negative fixture')):
    bad=copy.deepcopy(bridge);bad['cosmology_parameters']['H0_km_s_Mpc']+=1
    reject('remnant_named_cosmology_wrong_parameters',lambda:rem.derive(columns,{'remnant_conversion_INPUT':bad},lambda:None),'Parameters do not match')
    bad=copy.deepcopy(bridge);bad['cosmology_source_sha256']='0'*64
    reject('remnant_cosmology_bad_pin',lambda:rem.derive(columns,{'remnant_conversion_INPUT':bad},lambda:None),'Cosmology input changed')
    badcols=copy.deepcopy(columns);badcols['mass_1'].pop()
    reject('remnant_unpaired_columns',lambda:rem.derive(badcols,{'remnant_conversion_INPUT':bridge},lambda:None),'paired')

# HTTP fixture. All transfers are three local bytes; no network object is opened.
class Response:
    def __init__(self,headers):self.headers=headers;self.used=False
    def __enter__(self):return self
    def __exit__(self,*a):pass
    def geturl(self):return 'https://gwosc.org/fixture'
    def read(self,n):
        if self.used:return b''
        self.used=True;return b'abc'
def download_case(name,headers,changes=None,mutate=None,accepted=False,dynamic=False):
    with tempfile.TemporaryDirectory(dir=OUT) as temp:
        root=Path(temp)
        cfg={'event':'FIXTURE','mode':'calibration','kind':'public_strain','url':'https://gwosc.org/fixture',
             'filename':'fixture.bin','maximum_bytes':100,'license_source':'SYNTHETIC','license_status':'INPUT',
             'provider_checksum':None,'provider_checksum_algorithm':None}
        cfg.update(changes or {})
        allocation_sha='a'*64 if dynamic else None
        jobs_sha='b'*64
        (root/'allocation.json').write_text(json.dumps({'jobs_sha256':jobs_sha}))
        freg={'allocation_policy':{'relative_to_Chatgpt':'allocation.json'}}
        calls=[]
        def view(*a):
            calls.append(1);v={'downloads':{'fixture':copy.deepcopy(cfg)},'_allocation_sha256':allocation_sha}
            if len(calls)>1 and mutate=='allocation':v['_allocation_sha256']='c'*64
            if len(calls)>1 and mutate=='recipe':v['downloads']['fixture']['maximum_bytes']=99
            if mutate=='initial':v['downloads']['fixture']['maximum_bytes']=99
            return v
        with patch.object(fetch,'time_guard',lambda r:datetime.now(timezone.utc)+timedelta(hours=1)),\
             patch.object(fetch,'authorize_event',lambda *a:True),patch.object(fetch,'output_path',lambda n:root/n),\
             patch.object(fetch,'contained',lambda n:root/n),patch.object(fetch,'load_authorized_configuration',view),\
             patch.object(fetch.urllib.request,'build_opener',lambda *a:types.SimpleNamespace(open=lambda *a,**k:Response(headers))):
            error=None
            try:fetch.fetch(freg,'d'*64,'fixture',{'fixture':cfg})
            except (ValueError,TimeoutError) as e:error=str(e)
        exists=(root/'fixture.bin').exists();partial=(root/'fixture.bin.partial').exists()
        detail={'error':error,'promoted':exists,'partial_retained':partial,'guard_calls':len(calls)}
        passed=(error is None and exists) if accepted else (error is not None and not exists)
        if exists:
            receipt=json.loads((root/'fixture.bin.receipt.json').read_bytes())
            expected_recipe=sha_bytes(json.dumps(cfg,sort_keys=True,allow_nan=False).encode())
            identity_ok=(receipt['recipe_sha256']==expected_recipe and receipt['allocation_sha256']==allocation_sha
                         and receipt['jobs_configuration_sha256']==(jobs_sha if dynamic else None))
            passed=passed and identity_ok;detail['receipt_identity_verified']=identity_ok
        record(name,passed,detail)
download_case('fetch_HTTP_truncation_refused',{'Content-Length':'10'})
download_case('fetch_metadata_size_mismatch_refused',{'Content-Length':'3'},{'expected_bytes':4})
download_case('fetch_wrong_checksum_refused',{'Content-Length':'3'},{'provider_checksum_algorithm':'sha256','provider_checksum':'0'*64})
download_case('fetch_no_completeness_check_keeps_partial',{})
download_case('fetch_encoded_payload_refused',{'Content-Length':'3','Content-Encoding':'gzip'})
download_case('fetch_recipe_must_match_active_view',{'Content-Length':'3'},mutate='initial')
download_case('fetch_allocation_changed_before_promotion',{'Content-Length':'3'},mutate='allocation',dynamic=True)
download_case('fetch_recipe_changed_before_promotion',{'Content-Length':'3'},mutate='recipe')
download_case('fetch_size_and_dynamic_receipt_identity',{'Content-Length':'3'},{'expected_bytes':3},accepted=True,dynamic=True)
download_case('fetch_checksum_only_complete_fallback',{}, {'provider_checksum_algorithm':'sha256','provider_checksum':sha_bytes(b'abc')},accepted=True)

# Coordinator runs with a subprocess stub ONLY. No child process can be launched.
def campaign_case(name,behavior):
    with tempfile.TemporaryDirectory(dir=OUT) as temp:
        root=Path(temp);(root/'bis').mkdir()
        fake={'nulls':{'cells':{'CELL_'+str(i):{'draws':2,'fixture':True} for i in range(25)}}}
        launched=[];guard_calls=[]
        def deadline(r):
            guard_calls.append(1)
            if behavior=='guard_error':raise TimeoutError('SYNTHETIC_DEADLINE')
            return datetime.now(timezone.utc)+timedelta(hours=1)
        def child(args,**kwargs):
            cell=args[-1];launched.append(cell)
            if behavior=='timeout':raise subprocess.TimeoutExpired(args,1,output=b'FIXTURE',stderr=b'TIMEOUT')
            if behavior=='nonzero':return types.SimpleNamespace(returncode=2,stdout='',stderr='FIXTURE_FAILURE')
            digest='x'*64 if behavior=='bad_receipt' else 'd'*64
            receipt={'registration_sha256':digest,'cell':fake['nulls']['cells'][cell],'result':{'draws':2},'wall_seconds':0.}
            guard.publish_new(root/'bis'/('RESULT_E2_NULL_'+cell+'.json'),receipt)
            return types.SimpleNamespace(returncode=0,stdout='FIXTURE\n',stderr='')
        error=None
        with patch.object(campaign,'BASE',root),patch.object(campaign,'checked_registration',lambda:(fake,'d'*64)),\
             patch.object(campaign,'time_guard',deadline),patch.object(campaign.subprocess,'run',child),contextlib.redirect_stdout(io.StringIO()):
            try:campaign.main()
            except (SystemExit,TimeoutError,ValueError) as e:error=type(e).__name__+': '+str(e)
        p=root/'bis/RESULT_E2_NULL_CAMPAIGN.json';receipt=json.loads(p.read_bytes()) if p.exists() else None
        detail={'launched_stub_calls':len(launched),'error':error,'aggregate_receipt':receipt is not None,
                'aggregate_status':receipt['status'] if receipt else None}
        if behavior=='success':passed=receipt is not None and len(receipt['completed'])==25 and len(set(launched))==25
        else:passed=receipt is not None and receipt['status']=='SYNTHETIC_NULL_CAMPAIGN_FAILED'
        record(name,passed,detail)
campaign_case('campaign_25_sequential_frozen_stub_receipts','success')
campaign_case('campaign_child_nonzero_failure_receipt','nonzero')
campaign_case('campaign_timeout_failure_receipt','timeout')
campaign_case('campaign_deadline_guard_failure_receipt','guard_error')
campaign_case('campaign_bad_cell_receipt_failure_receipt','bad_receipt')

# Draft integration, not activation of the draft or actual E2 witness.
try:pe.validate_config(draft['pe_jobs']['GW250114_PILOT']);record('draft002_pilot_static_contract',True,'validate_config only; no PE')
except Exception as e:record('draft002_pilot_static_contract',False,str(e))
census=read('bis/e2_publication_census/PUBLICATION_CENSUS.json')
scoped=[e for e,v in draft['test_candidates'].items() if v['published_deformation_at_registration'] is False]
holds=[e for e,v in draft['test_candidates'].items() if v.get('data_quality_hold')]
record('draft002_census_counts',len(draft['calibration_event_ids'])==48 and len(scoped)==14 and len(holds)==4,
       {'calibration':len(draft['calibration_event_ids']),'scoped':len(scoped),'quality_holds':len(holds),'total_candidates':len(draft['test_candidates'])})
for event in holds:
    try:guard.authorize_event(draft,event,'blind_test');record('quality_hold_admission_'+event,False,'Guard accepts held event; no job or data read')
    except ValueError as e:record('quality_hold_admission_'+event,True,str(e))
record('draft002_census_pin',draft['publication_census']['sha256']==snapshot['bis/e2_publication_census/PUBLICATION_CENSUS.json']['sha256'],draft['publication_census']['sha256'])
record('draft002_real_GPS_anchor_present','event_reference_GPS' in draft,{'present':'event_reference_GPS' in draft})
frozen=json.loads((OUT/'MANIFEST_FINAL_v2.json').read_bytes())
e7_ok=all(sha(OUT/'producer'/n)==h for n,h in frozen['producer_tree_sha256'].items())
record('E7_frozen_producers_unchanged',e7_ok,'Compared with existing final-v2 manifest')
changed=[n for n,v in snapshot.items() if sha(BASE/n)!=v['sha256']]
out={'status':'INDEPENDENT_NEGATIVE_FIXTURES_V2','snapshot':'MAIN_CODE_REVIEW_SNAPSHOT_V2.json',
     'snapshot_sha256':sha(OUT/'MAIN_CODE_REVIEW_SNAPSHOT_V2.json'),'fixtures':results,
     'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),
     'changed_live_since_snapshot':changed,'no_real_MC_PE_waveform_strain_network':True,
     'scope':'Modules compiled from snapshotted bytes; mock subprocess/HTTP/generator only. Failures are findings, never patched here.'}
save('MAIN_CODE_REVIEW_FIXTURES_V2.json',out)
print(json.dumps(out,indent=2,ensure_ascii=False))
