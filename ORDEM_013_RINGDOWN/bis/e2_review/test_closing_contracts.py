"""Finite metadata and syntax checks; reuse already measured scalar bounds."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,copy,ast
HERE=Path(__file__).resolve().parent
B=HERE.parents[1];CODE=B/'bis/e2_code'
sys.path.insert(0,str(CODE))
import registration_guard as g
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
source=HERE/'TEMPORAL_REMNANT_SCALAR_TEST.json'
measured=json.loads(source.read_text())
rows=measured['temporal']['rows']
start=1420878129.;duration=16.
margins=dict(start_GPS=start,duration_s=duration,left_margin_s=min(r['earliest_GPS']-(start+.2) for r in rows),right_margin_s=min(start+duration-.2-r['latest_GPS'] for r in rows))
if min(margins['left_margin_s'],margins['right_margin_s'])<=0:raise RuntimeError('Proposed window fails measured corners')
now=datetime.now(timezone.utc).isoformat();issued='2026-09-22T19:06:33.802143+00:00'
evidence={'relative_to_Chatgpt':str(source),'sha256':sha(source),'reviewed_utc':now,'review_passed':True}
reg={'registered_utc':issued,'calibration_event_ids':[], 'test_candidates':{'MOCK':dict(eligible=True,published_deformation_at_registration=False,publication_census_scope='Mock only',data_quality_hold=True)}}
job={'mode':'blind_test','event':'MOCK','publication_metadata_review':dict(evidence,scope='Mock only'),'data_quality_resolution':dict(evidence,method='Synthetic gate plumbing; not an actual DQ resolution')}
checks=[]
g.validate_job_reviews(reg,job);checks.append('held_with_valid_mock_resolution_passes')
for label,mutate in (
 ('missing_resolution',lambda j:j.pop('data_quality_resolution')),
 ('false_review',lambda j:j['data_quality_resolution'].update(review_passed=False)),
 ('blank_method',lambda j:j['data_quality_resolution'].update(method=' ')),
 ('wrong_source_pin',lambda j:j['data_quality_resolution'].update(sha256='0'*64)),
 ('future_review',lambda j:j['data_quality_resolution'].update(reviewed_utc='2099-01-01T00:00:00Z')),
 ('missing_publication',lambda j:j.pop('publication_metadata_review'))):
    bad=copy.deepcopy(job);mutate(bad)
    try:g.validate_job_reviews(reg,bad)
    except (ValueError,KeyError):checks.append(label+'_refused')
    else:raise RuntimeError('Invalid review accepted '+label)
clean=copy.deepcopy(reg);clean['test_candidates']['MOCK']['data_quality_hold']=False
cleanjob=copy.deepcopy(job);cleanjob.pop('data_quality_resolution')
g.validate_job_reviews(clean,cleanjob);checks.append('clean_without_resolution_passes')
for p in CODE.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
tree=ast.parse((CODE/'pe_runner.py').read_text())
# Inspect actual integration, no execution of main or paired science outputs.
text=(CODE/'pe_runner.py').read_text()
if 'for k in PHYSICAL+DERIVED_PHYSICAL' not in text or 'derive(columns,cfg,lambda:time_guard(reg))' not in text:
    raise RuntimeError('Paired integration missing')
checks.append('paired_runner_integration_static_only')
out={'created_utc':now,'status':'FINITE_CONTRACT_TESTS_ONLY','candidate_window':margins,
 'checks':checks,'source_sha256':{str(p):sha(p) for p in (Path(__file__),source,CODE/'pe_runner.py',CODE/'pseob_source.py',CODE/'registration_guard.py',CODE/'remnant_conversion.py')},
 'limits':'Corners only, not exhaustive support proof or generated waveform validation. Metadata evidence is mock, no real candidate hold resolved.'}
g.publish_new(HERE/'CLOSING_CONTRACTS.json',out)
print(json.dumps(out))
