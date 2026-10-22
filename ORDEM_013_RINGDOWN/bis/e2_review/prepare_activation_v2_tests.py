"""Create an additive finite-test revision; preserve old scripts/receipts."""
from pathlib import Path
import ast
HERE=Path(__file__).resolve().parent
text=(HERE/'test_activation_marker.py').read_text()
def replace_once(old,new):
    global text
    if text.count(old)!=1:raise ValueError('Ambiguous test revision anchor')
    text=text.replace(old,new)
replace_once("root=HERE/'activation_mock/R'","root=HERE/'activation_mock_v2/R'")
replace_once("application=dict(status='APPLY_EXISTING_GO_TO_REVIEWED_CANDIDATE',candidate_sha256=candidate,\n  reviews={role:dict(status='BLOCKERS_CLOSED',files={'bis/MOCK_REVIEW.txt':g.sha(evidence)}) for role in ('PE','MAIN','E7')})",
"application=dict(status='APPLY_EXISTING_GO_TO_REVIEWED_CANDIDATE',candidate_sha256=candidate,\n  sealer_sha256=g.sha(sealer_path),created_utc='2026-09-22T19:06:32Z',\n  reviews={role:dict(status='BLOCKERS_CLOSED',blocking_findings=[],files={'bis/MOCK_REVIEW.txt':g.sha(evidence)}) for role in ('PE','MAIN','E7','ACTIVATION')})")
anchor="    bad=copy.deepcopy(reg);bad['activation']['review_application_sha256']='0'*64;refused('application_file_pin',bad)"
additional="""
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
"""
replace_once(anchor,anchor+additional)
replace_once("(HERE/'activation_mock').rglob('*')","(HERE/'activation_mock_v2').rglob('*')")
replace_once("HERE/'ACTIVATION_MARKER_MOCKS.json'","HERE/'ACTIVATION_MARKER_MOCKS_V2.json'")
ast.parse(text)
with (HERE/'test_activation_marker_v2.py').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
print('Created additive test_activation_marker_v2.py; prior test and receipt untouched')
