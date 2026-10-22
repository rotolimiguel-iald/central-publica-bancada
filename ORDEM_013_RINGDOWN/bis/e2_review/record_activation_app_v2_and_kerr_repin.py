"""Record the authorized one-string guard delta and cold Kerr manifest v3."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast,copy,os
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
KERR=B/'bis/e3_pyring_preparation'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for raw in iter(lambda:f.read(1024*1024),b''):h.update(raw)
    return h.hexdigest()
def publish(path,value):
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    temp=path.with_name(path.name+'.pending')
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(raw):raise OSError('Incomplete output')
    os.link(temp,path);temp.unlink()

def main():
    guard=B/'bis/e2_code/registration_guard.py'
    snapshot=HERE/'activation_app_v2_path_snapshot/registration_guard.py'
    before=b'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V1.json'
    after=b'ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V2.json'
    oldbytes=snapshot.read_bytes()
    if oldbytes.count(before)!=1 or oldbytes.replace(before,after)!=guard.read_bytes():raise ValueError('Unexpected source delta')
    ast.parse(guard.read_text())
    tests_path=HERE/'ACTIVATION_APP_V2_PATH_TESTS.json'
    tests=json.loads(tests_path.read_bytes())
    if len(tests['checks'])!=40 or tests['source_sha256'][str(guard)]!=sha(guard):raise ValueError('Focused tests/source mismatch')
    predecessor=KERR/'MANIFEST_v2.json';old=json.loads(predecessor.read_bytes())
    key=guard.relative_to(ROOT).as_posix()
    # Refuse unrelated drift. No source/config is silently re-pinned.
    pins=dict(old['source_and_config_pins'])
    for path,pin in pins.items():
        if path!=key and sha(ROOT/path)!=pin:raise ValueError('Unrelated dependency drift '+path)
    actual_code={p.name:sha(p) for p in KERR.glob('*.py')}
    if actual_code!=old['code_sha256']:raise ValueError('Kerr source code changed since v2')
    guard_receipt_path=HERE/'ACTIVATION_APP_V2_PATH_RECEIPT.json'
    created=[HERE/'prepare_activation_app_v2_path_tests.py',HERE/'test_activation_app_v2_path.py',tests_path,
      Path(__file__),snapshot]
    created.extend(p for p in (HERE/'activation_app_v2_path_mock').rglob('*') if p.is_file())
    receipt=dict(status='PATH_V2_ONLY_GUARD_FROZEN_FOR_REVIEW',created_utc=datetime.now(timezone.utc).isoformat(),
      modified_source=key,old_sha256=sha(snapshot),new_sha256=sha(guard),
      fixed_application_path=after.decode(),exact_single_byte_string_replacement=True,
      finite_checks=40,prior_cases=38,focused_new_cases=2,test_receipt_sha256=sha(tests_path),
      old_receipts_modified=False,other_production_sources_modified=False,
      execution_policy_modified_or_bypassed=False,real_sealer_executed=False,science_executed=False,
      files_created_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(created)},
      receipt_itself=guard_receipt_path.relative_to(ROOT).as_posix())
    publish(guard_receipt_path,receipt)
    pins[key]=sha(guard)
    note=KERR/'MANIFEST_V3_NOTE.md'
    for p in (predecessor,note,guard_receipt_path):pins[p.relative_to(ROOT).as_posix()]=sha(p)
    manifest=copy.deepcopy(old)
    successor=KERR/'MANIFEST_v3.json'
    manifest.update(created_utc=datetime.now(timezone.utc).isoformat(),revision='V3_APPLICATION_V2_FIXED_PATH_REPIN',
      predecessor={'relative_to_Chatgpt':predecessor.relative_to(ROOT).as_posix(),'sha256':sha(predecessor)},
      source_and_config_pins=pins,authorization_manifest_filename='MANIFEST_v3.json',
      code_change_since_predecessor=False,
      changed_existing_dependency_pins={key:{'old':old['source_and_config_pins'][key],'new':sha(guard)}},
      checks=old['checks']+['Kerr code tree identical to v2','Guard changes exactly one application path literal','40 finite mock guard checks passed'],
      activation_scope='COLD_ONLY; principal execution after B review and B2/F0-stop; no policy bypass')
    publish(successor,manifest)
    closing_path=KERR/'MANIFEST_V3_REPIN_RECEIPT.json'
    written=created+[guard_receipt_path,note,successor,closing_path]
    final=dict(status='COLD_V3_READY_FOR_B_REVIEW',created_utc=datetime.now(timezone.utc).isoformat(),
      predecessor_path=predecessor.relative_to(ROOT).as_posix(),predecessor_sha256=sha(predecessor),
      successor_path=successor.relative_to(ROOT).as_posix(),successor_sha256=sha(successor),
      guard_sha256=sha(guard),guard_receipt_sha256=sha(guard_receipt_path),Kerr_code_files_unchanged=len(actual_code),
      sources_modified=[key],files_created=[p.relative_to(ROOT).as_posix() for p in written],
      scientific_execution=False,activation_created=False)
    publish(closing_path,final)
    for path,pin in pins.items():
        if sha(ROOT/path)!=pin:raise ValueError('Post-write dependency drift '+path)
    print(json.dumps(dict(guard_sha256=sha(guard),guard_receipt_sha256=sha(guard_receipt_path),
      successor_sha256=sha(successor),repin_receipt_sha256=sha(closing_path),
      Kerr_code_files_unchanged=len(actual_code),checks=40,status=final['status']),indent=2))

if __name__=='__main__':main()
