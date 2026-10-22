"""Finite activation marker fixtures, no sealer execution or seed access."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,copy,hashlib,ast
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];CODE=B/'bis/e2_code'
sys.path.insert(0,str(CODE))
import registration_guard as g
root=HERE/'activation_mock_v2/R';base=root/'ORDEM_013_RINGDOWN'
(base/'bis').mkdir(parents=True,exist_ok=False);(base/'refeito').mkdir()
def dump(p,obj):
    raw=(json.dumps(obj)+'\n').encode();temp=p.with_name(p.name+'.test_pending')
    with temp.open('xb') as f:f.write(raw)
    temp.replace(p)
application_path=base/'bis/E2_REVIEW_APPLICATION_V1.json'
receipt_path=base/'bis/E2_REGISTRATION_RECEIPT.json'
sealer_path=base/'refeito/seal_e2_013bis.py';sealer_path.write_bytes(b'# inert mock sealer text\n')
evidence=base/'bis/MOCK_REVIEW.txt';evidence.write_bytes(b'inert mock evidence, not a real review\n')
note=base/'bis/MOCK_WITNESS.txt';note.write_bytes(b'inert mock witness\n')
digest=hashlib.sha256(b'mock registration').hexdigest()
candidate=hashlib.sha256(b'mock candidate').hexdigest()
application=dict(status='APPLY_EXISTING_GO_TO_REVIEWED_CANDIDATE',candidate_sha256=candidate,
  sealer_sha256=g.sha(sealer_path),created_utc='2026-09-22T19:06:32Z',
  reviews={role:dict(status='BLOCKERS_CLOSED',blocking_findings=[],files={'bis/MOCK_REVIEW.txt':g.sha(evidence)}) for role in ('PE','MAIN','E7','ACTIVATION')})
dump(application_path,application)
reg=dict(registered_utc='2026-09-22T19:06:33.802143Z',registration_provenance={'candidate_sha256':candidate},activation={
 'receipt_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/E2_REGISTRATION_RECEIPT.json',
 'review_application_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V1.json',
 'review_application_sha256':g.sha(application_path),
 'sealer_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py','sealer_sha256':g.sha(sealer_path)})
receipt=dict(status='E2_ACTIVATION_COMPLETE',registration_sha256=digest,witness_sha256=g.sha(note),
 review_application_sha256=reg['activation']['review_application_sha256'],sealer_sha256=g.sha(sealer_path),finished_utc=datetime.now(timezone.utc).isoformat())
old_contained=g.contained;old_base=g.BASE
g.BASE=base;g.contained=lambda name,root=root:old_contained(name,root=root)
checks=[]
def refused(label,rr=reg):
    try:g.check_activation(rr,digest,note)
    except (ValueError,FileNotFoundError,KeyError):checks.append(label)
    else:raise RuntimeError('Accepted invalid activation '+label)
try:
    refused('absent_marker')
    dump(receipt_path,receipt)
    if not g.check_activation(reg,digest,note):raise RuntimeError('Valid mock refused')
    checks.append('complete_mock_positive')
    for field,value in (('status','PREPARED'),('registration_sha256','0'*64),('witness_sha256','0'*64),
      ('review_application_sha256','0'*64),('sealer_sha256','0'*64),('finished_utc','2099-01-01T00:00:00Z'),
      ('finished_utc','2000-01-01T00:00:00Z')):
        bad=dict(receipt);bad[field]=value;dump(receipt_path,bad);refused('wrong_'+field+'_'+str(value)[:10])
    dump(receipt_path,receipt)
    for label,edit in (
      ('application_status',lambda a:a.update(status='PENDING')),
      ('candidate',lambda a:a.update(candidate_sha256='0'*64)),
      ('missing_role',lambda a:a['reviews'].pop('E7')),
      ('open_blocker',lambda a:a['reviews']['PE'].update(status='OPEN')),
      ('empty_files',lambda a:a['reviews']['MAIN'].update(files={})),
      ('bad_evidence_pin',lambda a:a['reviews']['E7'].update(files={'bis/MOCK_REVIEW.txt':'0'*64})),
      ('escaped_file',lambda a:a['reviews']['E7'].update(files={'../outside':'0'*64}))):
        app=copy.deepcopy(application);edit(app);dump(application_path,app)
        rr=copy.deepcopy(reg);rr['activation']['review_application_sha256']=g.sha(application_path)
        rc=dict(receipt,review_application_sha256=g.sha(application_path));dump(receipt_path,rc)
        refused(label,rr)
    dump(application_path,application);dump(receipt_path,receipt)
    bad=copy.deepcopy(reg);bad['activation']['sealer_sha256']='0'*64;refused('sealer_file_pin',bad)
    bad=copy.deepcopy(reg);bad['activation']['review_application_sha256']='0'*64;refused('application_file_pin',bad)
    # Incremental schema controls; all application/receipt hashes recomputed so
    # each negative exercises the semantic check, not an earlier stale hash.
    cases=[
      ('wrong_application_sealer',lambda a:a.update(sealer_sha256='0'*64)),
      ('missing_application_sealer',lambda a:a.pop('sealer_sha256')),
      ('application_after_registration',lambda a:a.update(created_utc='2026-09-22T19:06:34Z')),
      ('missing_application_date',lambda a:a.pop('created_utc')),
      ('naive_application_date',lambda a:a.update(created_utc='2026-09-22T19:06:32')),
      ('missing_activation_role',lambda a:a['reviews'].pop('ACTIVATION')),
      ('extra_role',lambda a:a['reviews'].update(EXTRA=copy.deepcopy(a['reviews']['PE']))),
    ]
    for role in ('PE','MAIN','E7','ACTIVATION'):
        cases.extend([
          ('blocking_findings_'+role,lambda a,r=role:a['reviews'][r].update(blocking_findings=['mock unresolved blocker'])),
          ('missing_blocking_findings_'+role,lambda a,r=role:a['reviews'][r].pop('blocking_findings')),
          ('wrong_type_blocking_findings_'+role,lambda a,r=role:a['reviews'][r].update(blocking_findings=None)),
        ])
    for label,edit in cases:
        app=copy.deepcopy(application);edit(app);dump(application_path,app)
        rr=copy.deepcopy(reg);rr['activation']['review_application_sha256']=g.sha(application_path)
        dump(receipt_path,dict(receipt,review_application_sha256=g.sha(application_path)))
        refused(label,rr)
    app=copy.deepcopy(application);app['created_utc']=reg['registered_utc']
    dump(application_path,app)
    rr=copy.deepcopy(reg);rr['activation']['review_application_sha256']=g.sha(application_path)
    dump(receipt_path,dict(receipt,review_application_sha256=g.sha(application_path)))
    if not g.check_activation(rr,digest,note):raise RuntimeError('Equal creation/registration boundary rejected')
    checks.append('application_equal_registration_positive')
    dump(application_path,application);dump(receipt_path,receipt)

finally:g.contained=old_contained;g.BASE=old_base
tree=ast.parse((CODE/'registration_guard.py').read_text())
function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='checked_registration')
calls=[(n.lineno,n.func.id) for n in ast.walk(function) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)]
if not max(line for line,name in calls if name=='check_witness')<min(line for line,name in calls if name=='check_activation'):
    raise RuntimeError('Activation guard ordering')
out=dict(status='FINITE_MOCKS_ONLY_NO_REGISTRATION',created_utc=datetime.now(timezone.utc).isoformat(),checks=checks,
  source_sha256={str(p):g.sha(p) for p in (Path(__file__),CODE/'registration_guard.py',B/'bis/e2_publication_census/E2_SEALER_INDEPENDENT_REVIEW.md')},
  files_written=[str(p.relative_to(HERE)) for p in (HERE/'activation_mock_v2').rglob('*') if p.is_file()],
  seed_access=False,production_registration_created=False)
g.publish_new(HERE/'ACTIVATION_MARKER_MOCKS_V2.json',out)
print(json.dumps(dict(checks=len(checks),all_passed=True,source_sha256=out['source_sha256']),indent=2))
