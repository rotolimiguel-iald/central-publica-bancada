"""Metadata-only v3 delivery. Never run extraction or tests from here."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
OUT=Path(__file__).resolve().parents[1];BASE=OUT.parents[1];ROOT=BASE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    p=OUT/name;temp=p.with_suffix(p.suffix+'.pending')
    raw=(json.dumps(obj,ensure_ascii=False,allow_nan=False,indent=2)+'\n').encode()
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.stat().st_size==len(raw)
    os.link(temp,p);temp.unlink()
backup=OUT/'snapshot_v2_before_review_fixes'
old=json.loads((backup/'MANIFEST_FINAL_v2.json').read_bytes())
assert all(sha(backup/n)==v['sha256'] for n,v in old['files'].items())
assert sha(backup/'MANIFEST_FINAL_v2.json')==sha(OUT/'MANIFEST_FINAL_v2.json')
tree={p.name:sha(p) for p in sorted((OUT/'producer').glob('*.py'))}
guard=BASE/'bis/e2_code/registration_guard.py';guard_sha=sha(guard)
save('UNIT_TESTS_V3.json',dict(status='PASS_DETERMINISTIC_SYNTHETIC',count=46,failures=0,
    execution_exit_code=0,suite_seconds=1.608,producer_tree_sha256=tree,
    command="/opt/lal_env/bin/python -B -m unittest discover -s e7_prepare/tests -p 'test*.py' -v",
    evidence='Observed execution in this session; 31 original + 15 new methods with subcases',
    real_extraction=False,PE=False,MC=False,waveforms=False,strain=False,network=False))
include=json.loads((OUT/'E2_INCLUDE_FINAL_v2.json').read_bytes())
include['e7']['producer_tree_sha256']=tree
include['extra_code_roots'][0]['files_sha256']=tree
include['e7']['guard_sha256']=guard_sha
include['e7']['guard_pin_status']='OBSERVED_V3_RECHECK_AT_PRINCIPAL_FREEZE'
include['observed_guard_sha256']=guard_sha
pins=include['input_pins_relative_to_Chatgpt']
for key in list(pins):
    if key.endswith(('HANDOFF_FINAL_v2.md','E2_DESIGN_DRAFT_001.json')):del pins[key]
for p in (OUT/'HANDOFF_FINAL_v3.md',BASE/'bis/E2_DESIGN_DRAFT_003.json',
          BASE/'bis/e2_publication_census/E7_INDEPENDENT_REVIEW.md'):
    pins[p.relative_to(ROOT).as_posix()]=sha(p)
for path,digest in pins.items():assert sha(ROOT/path)==digest,path
include['supersedes']='E2_INCLUDE_FINAL_v2.json'
include['assembly_fragment_source_relative_to_Chatgpt']=(OUT/'E2_INCLUDE_FINAL_v3.json').relative_to(ROOT).as_posix()
include['consumer_authorization_contract']='Independent principal receipt path and SHA256 required with posterior'
save('E2_INCLUDE_FINAL_v3.json',include)
names=['producer/'+n for n in tree]+['HANDOFF_FINAL_v3.md','E2_INCLUDE_FINAL_v3.json',
 'UNIT_TESTS_V3.json','EXTRACTION_PLAN.json','tests/test_e7.py','tests/test_review_fixes_v3.py','tests/finalize_review_v3.py']
save('MANIFEST_FINAL_v3.json',dict(status='E7_REVIEW_FIXES_PREPARED_PENDING_INDEPENDENT_CLOSE',
 created_utc=datetime.now(timezone.utc).isoformat(),supersedes='MANIFEST_FINAL_v2.json',
 producer_tree_sha256=tree,guard_sha256=guard_sha,
 files={n:dict(sha256=sha(OUT/n),bytes=(OUT/n).stat().st_size) for n in names},
 snapshot_v2=dict(directory=backup.name,manifest_sha256=sha(backup/'MANIFEST_FINAL_v2.json'),all_files_verified=True),
 real_extraction_executed=False,independent_review='PENDING_RUSSELL_V3',guard_final_pin_recheck_required=True))
save('E7_ASSEMBLY_V3.json',dict(status='PREPARED_NOT_REGISTERED',
 fragment_source_relative_to_Chatgpt=(OUT/'E2_INCLUDE_FINAL_v3.json').relative_to(ROOT).as_posix(),
 fragment_sha256=sha(OUT/'E2_INCLUDE_FINAL_v3.json'),manifest_relative_to_Chatgpt=(OUT/'MANIFEST_FINAL_v3.json').relative_to(ROOT).as_posix(),
 manifest_sha256=sha(OUT/'MANIFEST_FINAL_v3.json'),guard_sha256=guard_sha,
 merge_fields=['e7','extra_code_roots','input_pins_relative_to_Chatgpt'],
 requirement='Replace assembly source v2 with v3; preserve other roots; independent close pending; do not register on stale guard hash'))
assert sha(guard)==guard_sha,'Guard changed during finalization'
print(json.dumps(dict(producer_tree_sha256=tree,guard_sha256=guard_sha,
 fragment_sha256=sha(OUT/'E2_INCLUDE_FINAL_v3.json'),manifest_sha256=sha(OUT/'MANIFEST_FINAL_v3.json'),
 assembly_sha256=sha(OUT/'E7_ASSEMBLY_V3.json')),indent=2))
