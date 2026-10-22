"""Final hashes after requested vector predictions; metadata only."""
from pathlib import Path
import hashlib,json,os
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parents[1]; BASE=OUT.parents[1]; ROOT=BASE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):
    p=OUT/name; tmp=p.with_suffix(p.suffix+'.pending')
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.stat().st_size==len(raw)
    os.link(tmp,p);tmp.unlink()
include=json.loads((OUT/'E2_INCLUDE_FINAL.json').read_bytes())
tree={p.name:sha(p) for p in (OUT/'producer').glob('*.py')}
include['e7']['producer_tree_sha256']=tree
include['extra_code_roots'][0]['files_sha256']=tree
guard=BASE/'bis/e2_code/registration_guard.py'
include['e7']['guard_sha256']=sha(guard)
include['observed_guard_sha256']=sha(guard)
source=BASE/'tgl_ringdown_prediction.py'
include['e7']['prediction_source_path']=source.relative_to(ROOT).as_posix()
include['e7']['prediction_source_sha256']=sha(source)
include['input_pins_relative_to_Chatgpt'][source.relative_to(ROOT).as_posix()]=sha(source)
include['input_pins_relative_to_Chatgpt'][(OUT/'HANDOFF_FINAL_v2.md').relative_to(ROOT).as_posix()]=sha(OUT/'HANDOFF_FINAL_v2.md')
include['supersedes']='E2_INCLUDE_FINAL.json'
write('E2_INCLUDE_FINAL_v2.json',include)
files={p.relative_to(OUT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size}
       for p in sorted(OUT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
write('MANIFEST_FINAL_v2.json',{'status':'E7_OPERATIONAL_CONDITIONAL_MODULE_PREPARED_NOT_PHYSICAL_TEST_PAID',
      'created_utc':datetime.now(timezone.utc).isoformat(),'files':files,'producer_tree_sha256':tree,
      'tests':{'count':31,'status':'PASS_DETERMINISTIC_SYNTHETIC','log':'UNIT_TESTS_READINGS_FINAL.log'},
      'prediction_source_sha256':sha(source),'real_extraction_executed':False,
      'independent_review':'PENDING','guard_final_pin_recheck_required':True,
      'supersedes':'MANIFEST_FINAL.json'})
print(json.dumps({'producer_sha256':tree,'prediction_source_sha256':sha(source),
      'include_sha256':sha(OUT/'E2_INCLUDE_FINAL_v2.json'),
      'manifest_sha256':sha(OUT/'MANIFEST_FINAL_v2.json')},indent=2))
