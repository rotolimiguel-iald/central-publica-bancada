"""Metadata/AST only. No tests or producer scientific calls."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os
OUT=Path(__file__).resolve().parents[1];BASE=OUT.parents[1];ROOT=BASE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();p=OUT/name;t=p.with_suffix(p.suffix+'.pending')
    with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if t.stat().st_size!=len(raw):raise IOError('Short write')
    os.link(t,p);t.unlink()
backup=OUT/'snapshot_v3_before_F3_fix';old=json.loads((backup/'MANIFEST_FINAL_v3.json').read_bytes())
for name,item in old['files'].items():
    if sha(backup/name)!=item['sha256']:raise ValueError('Snapshot differs: '+name)
def functions(path):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_bytes()).body if isinstance(n,ast.FunctionDef)}
a=functions(backup/'producer/tgl_ringdown_ampliacao.py');b=functions(OUT/'producer/tgl_ringdown_ampliacao.py')
changed=[n for n in set(a)|set(b) if a.get(n)!=b.get(n)]
if changed!=['checked_authorization']:raise ValueError(changed)
if sha(OUT/'producer/extrai_posteriores_pseob.py')!=sha(backup/'producer/extrai_posteriores_pseob.py'):raise ValueError('Extractor changed')
tree={p.name:sha(p) for p in sorted((OUT/'producer').glob('*.py'))}
save('UNIT_TESTS_F3_V4.json',dict(status='PASS_FOCUSED_DETERMINISTIC_AUTHORIZATION',count=7,failures=0,
 log='UNIT_TESTS_F3_V4.log',log_sha256=sha(OUT/'UNIT_TESTS_F3_V4.log'),producer_tree_sha256=tree,
 AST_changed_functions=changed,scientific_functions_AST_unchanged=True,extractor_bytes_unchanged=True,
 previous_v3_tests=46,previous_v3_tests_rerun=False,real_data_access=False))
include=json.loads((OUT/'E2_INCLUDE_FINAL_v3.json').read_bytes());guard=BASE/'bis/e2_code/registration_guard.py';gs=sha(guard)
include['e7']['producer_tree_sha256']=tree;include['extra_code_roots'][0]['files_sha256']=tree
include['e7']['guard_sha256']=gs;include['observed_guard_sha256']=gs
include['e7']['guard_pin_status']='OBSERVED_V4_PRINCIPAL_REHASH_AUTHORIZED_AT_PRE_E2_ASSEMBLY_WITH_PROVENANCE'
include['supersedes']='E2_INCLUDE_FINAL_v3.json'
include['assembly_fragment_source_relative_to_Chatgpt']=(OUT/'E2_INCLUDE_FINAL_v4.json').relative_to(ROOT).as_posix()
pins=include['input_pins_relative_to_Chatgpt']
for key in list(pins):
    if key.endswith('HANDOFF_FINAL_v3.md'):del pins[key]
for p in (OUT/'HANDOFF_FINAL_v4.md',BASE/'bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V3.md'):
    pins[p.relative_to(ROOT).as_posix()]=sha(p)
for name,digest in pins.items():
    if sha(ROOT/name)!=digest:raise ValueError('Changed input: '+name)
save('E2_INCLUDE_FINAL_v4.json',include)
names=['producer/'+n for n in tree]+['E2_INCLUDE_FINAL_v4.json','HANDOFF_FINAL_v4.md','EXTRACTION_PLAN.json',
 'UNIT_TESTS_F3_V4.json','UNIT_TESTS_F3_V4.log','tests/test_authorization_v4.py','tests/finalize_F3_v4.py']
save('MANIFEST_FINAL_v4.json',dict(status='F3_FIXED_AWAITING_INDEPENDENT_CLOSE_NOT_REGISTRATION',
 created_utc=datetime.now(timezone.utc).isoformat(),files={n:dict(sha256=sha(OUT/n),bytes=(OUT/n).stat().st_size) for n in names},
 producer_tree_sha256=tree,guard_sha256=gs,supersedes='MANIFEST_FINAL_v3.json',
 snapshot_v3_manifest_sha256=sha(backup/'MANIFEST_FINAL_v3.json'),independent_review='PENDING_RUSSELL_F3_V4',
 science_AST_unchanged_from_v3=True,real_extraction_executed=False))
save('E7_ASSEMBLY_V4.json',dict(status='PREPARED_NOT_REGISTERED',
 fragment_source_relative_to_Chatgpt=(OUT/'E2_INCLUDE_FINAL_v4.json').relative_to(ROOT).as_posix(),
 fragment_sha256=sha(OUT/'E2_INCLUDE_FINAL_v4.json'),manifest_relative_to_Chatgpt=(OUT/'MANIFEST_FINAL_v4.json').relative_to(ROOT).as_posix(),
 manifest_sha256=sha(OUT/'MANIFEST_FINAL_v4.json'),observed_guard_sha256=gs,
 merge_fields=['e7','extra_code_roots','input_pins_relative_to_Chatgpt'],supersedes='E7_ASSEMBLY_V3.json',
 integration='Update source field to v4; principal may rehash final reviewed guard before E2, keeping explicit fragment provenance; F3 independent close pending'))
print(json.dumps(dict(producer_tree_sha256=tree,fragment_sha256=sha(OUT/'E2_INCLUDE_FINAL_v4.json'),
 manifest_sha256=sha(OUT/'MANIFEST_FINAL_v4.json'),assembly_sha256=sha(OUT/'E7_ASSEMBLY_V4.json'),observed_guard_sha256=gs),indent=2))
