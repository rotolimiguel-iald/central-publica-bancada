"""Record additive guard closure and preserve historical receipts; no science."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,ast
HERE=Path(__file__).resolve().parent;B=HERE.parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
snapshot=HERE/'activation_v2_snapshot'
for name in ('test_activation_marker.py','ACTIVATION_MARKER_MOCKS.json'):
    if (HERE/name).read_bytes()!=(snapshot/name).read_bytes():raise ValueError('Historical test/receipt changed')
source=B/'bis/e2_code/registration_guard.py'
ast.parse(source.read_text())
tests=json.loads((HERE/'ACTIVATION_MARKER_MOCKS_V2.json').read_bytes())
if len(tests['checks'])!=38:raise ValueError('Incomplete finite controls')
kerrpath=B/'bis/e3_pyring_preparation/MANIFEST.json'
kerr=json.loads(kerrpath.read_bytes())
oldpin=kerr['source_and_config_pins']['ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py']
created=[HERE/name for name in ('prepare_activation_v2_tests.py','test_activation_marker_v2.py','ACTIVATION_MARKER_MOCKS_V2.json','record_activation_v2.py')]
created+=list(p for directory in (snapshot,HERE/'activation_mock_v2') for p in directory.rglob('*') if p.is_file())
receipt=dict(status='GUARD_FROZEN_FOR_INDEPENDENT_REVIEW_NO_REGISTRATION',created_utc=datetime.now(timezone.utc).isoformat(),
 modified_source={'path':source.relative_to(B).as_posix(),'sha256':sha(source)},
 requirements={'exact_roles':['PE','MAIN','E7','ACTIVATION'],'application_sealer_matches_activation':True,
 'application_created_no_later_than_registration':True,'every_review_blocking_findings_empty_list':True},
 finite_checks=38,previous_cases=18,incremental_cases=20,old_test_and_receipt_byte_identical=True,
 historical_guard_sha256=sha(snapshot/'registration_guard.py'),
 sealer_read_only_sha256=sha(B/'refeito/seal_e2_013bis.py'),
 test_receipt_sha256=sha(HERE/'ACTIVATION_MARKER_MOCKS_V2.json'),
 files_created_sha256={p.relative_to(B).as_posix():sha(p) for p in sorted(created)},
 receipt_itself='bis/e2_review/ACTIVATION_V2_CLOSING_RECEIPT.json',
 kerr_dependency={'manifest_sha256':sha(kerrpath),'recorded_guard_sha256':oldpin,
 'current_guard_sha256':sha(source),'status':'REPIN_REQUIRED_BEFORE_EXECUTION' if oldpin!=sha(source) else 'MATCH'},
 limits='Only finite mocked activation checks. No real marker/application/sealer/seed/runtime-science executed. Other E2 sources unedited; independent review remains external.')
with (HERE/'ACTIVATION_V2_CLOSING_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'source_sha256':sha(source),'receipt_sha256':sha(HERE/'ACTIVATION_V2_CLOSING_RECEIPT.json'),'checks':38,'created_files':len(created)+1,'kerr_status':receipt['kerr_dependency']['status']}))
