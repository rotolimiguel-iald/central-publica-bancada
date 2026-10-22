"""Finite fake hash-chain checks with copied frozen guard, no real activation or fetch."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,importlib.util,json,os

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
RESULTS=[]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write((json.dumps(value,sort_keys=True)+'\n').encode())


def check(name,fn,reject=False):
    error=None;result=None
    try:result=fn()
    except Exception as e:error=type(e).__name__+': '+str(e)
    RESULTS.append(dict(id=name,passed=(error is not None) if reject else (error is None and result is not False),error=error))


def main():
    root=HERE/'phase_fixture_001/Chatgpt';base=root/'ORDEM_013_RINGDOWN';code=base/'bis/e2_code'
    code.mkdir(parents=True,exist_ok=False)
    original=BASE/'bis/e2_code/registration_guard.py';copy=code/'registration_guard.py';copy.write_bytes(original.read_bytes())
    spec=importlib.util.spec_from_file_location('fake_guard',copy);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    now=datetime.now(timezone.utc);stamp=lambda n:(now+timedelta(seconds=n)).isoformat()
    parent=hashlib.sha256(b'FAKE_PARENT_NOT_REAL_E2').hexdigest()
    reg=dict(registered_utc=stamp(-100),pe_jobs={'FAKE_STATIC':{'mode':'calibration'}},downloads={},
        allocation_policy={'relative_to_Chatgpt':'ORDEM_013_RINGDOWN/ORCAMENTO_40H.json','max_job_wall_seconds':28800},
        calibration_event_ids=['FAKE_CAL'],test_candidates={'FAKE_HELD':dict(eligible=True,
            published_deformation_at_registration=False,publication_census_scope='FAKE_SCOPE',data_quality_hold=True)})
    license=base/'FAKE_LICENSE.json';write(license,{'scope':'FAKE_ONLY'})
    recipe={'event':'FAKE_HELD','mode':'blind_test','license_receipt_relative_to_Chatgpt':license.relative_to(root).as_posix(),
            'license_receipt_sha256':sha(license)}
    a=base/'JOBS_A_IMMUTABLE.json';write(a,dict(schema_version='E2_PE_JOBS_V2',parent_registration_sha256=parent,jobs={},downloads={'FAKE_RECIPE':recipe}))
    witnessA=root/'TUNEL/DO_CHATGPT/FAKE_A.md'
    aa=base/'ALLOCATION_A_IMMUTABLE.json';write(aa,dict(parent_registration_sha256=parent,registered_utc=stamp(-50),
        witness_relative_to_Chatgpt=witnessA.relative_to(root).as_posix(),jobs_relative_to_Chatgpt=a.relative_to(root).as_posix(),jobs_sha256=sha(a)))
    active=base/'ORCAMENTO_40H.json';active.write_bytes(aa.read_bytes())
    check('phaseA_without_witness_refused',lambda:g.load_authorized_configuration(reg,parent),True)
    witnessA.parent.mkdir(parents=True);witnessA.write_text('allocation_sha256: '+sha(aa)+'\nregistered_utc: '+stamp(0)+'\n')
    check('phaseA_downloads_only_keeps_static_job',lambda:set(g.load_authorized_configuration(reg,parent)['pe_jobs'])=={'FAKE_STATIC'})
    check('phaseA_held_recipe_not_job_reviewed',lambda:'FAKE_RECIPE' in g.load_authorized_configuration(reg,parent)['downloads'])
    check('fetch_classification_is_not_hold_clearance',lambda:g.authorize_event(reg,'FAKE_HELD','blind_test'))
    phaseAhash={p.name:sha(p) for p in (a,aa,witnessA)}
    b=base/'JOBS_B_IMMUTABLE.json';write(b,dict(schema_version='E2_PE_JOBS_V2',parent_registration_sha256=parent,jobs={},downloads={}))
    witnessB=root/'TUNEL/DO_CHATGPT/FAKE_B.md'
    ab=base/'ALLOCATION_B_IMMUTABLE.json';write(ab,dict(parent_registration_sha256=parent,registered_utc=stamp(0),
        witness_relative_to_Chatgpt=witnessB.relative_to(root).as_posix(),jobs_relative_to_Chatgpt=b.relative_to(root).as_posix(),jobs_sha256=sha(b),
        lineage_INPUT={'previous_sha256':sha(aa)}))
    active.write_bytes(ab.read_bytes())
    check('phaseB_switch_without_new_witness_refused',lambda:g.load_authorized_configuration(reg,parent),True)
    witnessB.write_text('allocation_sha256: '+sha(ab)+'\nregistered_utc: '+datetime.now(timezone.utc).isoformat()+'\n')
    check('phaseB_no_automatic_download_accumulation',lambda:g.load_authorized_configuration(reg,parent)['downloads']=={})
    check('phaseA_versioned_bytes_preserved',lambda:phaseAhash=={p.name:sha(p) for p in (a,aa,witnessA)})
    corrupt=json.loads(ab.read_bytes());corrupt['lineage_INPUT']['previous_sha256']='0'*64
    active.write_text(json.dumps(corrupt));witnessB.write_text('allocation_sha256: '+sha(active)+'\nregistered_utc: '+datetime.now(timezone.utc).isoformat()+'\n')
    check('lineage_extra_field_not_core_gate',lambda:g.load_authorized_configuration(reg,parent)['downloads']=={})
    c=base/'JOBS_C_HELD.json';write(c,dict(schema_version='E2_PE_JOBS_V2',parent_registration_sha256=parent,downloads={},
        jobs={'FAKE_NEW_JOB':dict(event='FAKE_HELD',mode='blind_test',wall_budget_seconds=1,publication_metadata_review={})}))
    corrupt['jobs_relative_to_Chatgpt']=c.relative_to(root).as_posix();corrupt['jobs_sha256']=sha(c)
    active.write_text(json.dumps(corrupt));witnessB.write_text('allocation_sha256: '+sha(active)+'\nregistered_utc: '+datetime.now(timezone.utc).isoformat()+'\n')
    check('actual_job_missing_publication_review_refused',lambda:g.load_authorized_configuration(reg,parent),True)
    if sha(original)!=sha(copy):raise ValueError('Frozen guard changed')
    result=dict(status='FINITE_FAKE_PHASE_CONTRACT_ONLY',cases=RESULTS,total=len(RESULTS),passed=sum(x['passed'] for x in RESULTS),
        frozen_guard_sha256=sha(copy),script_sha256=sha(Path(__file__)),mock_witness=False,
        real_E2_activated=False,fetch_called=False,network=False,scientific_data_read=False,admission=False,
        scope='Exact load_authorized_configuration on own fake files; real check_witness within fake root, no checked_registration/launch')
    write(HERE/'PHASE_CONTRACT_RESULTS_V1.json',result)
    print(json.dumps(dict(total=len(RESULTS),passed=result['passed'])))


if __name__=='__main__':main()
