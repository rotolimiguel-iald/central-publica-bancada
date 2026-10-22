"""Finalize metadata and measured hashes only; never run producer extraction."""
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
include=json.loads((OUT/'E2_INCLUDE.json').read_bytes())
tree={p.name:sha(p) for p in (OUT/'producer').glob('*.py')}
include['e7']['producer_tree_sha256']=tree
include['extra_code_roots'][0]['files_sha256']=tree
guard=BASE/'bis/e2_code/registration_guard.py'
include['e7']['guard_sha256']=sha(guard)
draft=BASE/'bis/E2_DESIGN_DRAFT_001.json'
include['input_pins_relative_to_Chatgpt'][draft.relative_to(ROOT).as_posix()]=sha(draft)
include['draft_review_status']='DESIGN_REVIEW_ONLY_NO_REGISTERED_OR_PHYSICAL_PAID_CLAIM'
include['observed_guard_sha256']=sha(guard)
write('E2_INCLUDE_FINAL.json',include)
sources=json.loads((OUT/'SOURCE_PINS.json').read_bytes())
preview={'status':'PREPARATION_PREVIEW_NOT_REGISTERED_RESULT','registration_sha256':None,
         'nuisance_sha256':include['e7']['nuisance_sha256'],
         'test_events_added':0,'lnB':None,'z_physical':None,
         'matrix':[{'reading':r,'mode_variant':mode,'verdict':'AWAITING_DATA',
                    'N_target_information':None,'target_status':'OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED',
                    'systematic_gate':'red','lnB':None,'z_physical':None}
                   for r in include['e7']['readings'] for mode in ('220_only','220_plus_440_INPUT')],
         'note':'Static preparation preview from metadata; guarded producer not run; no extraction authorized'}
write('PREPARATION_PREVIEW.json',preview)
files={p.relative_to(OUT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size}
       for p in sorted(OUT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
write('MANIFEST_FINAL.json',{'status':'E7_PREPARED_NOT_ORDER_COMPLETED',
      'created_utc':datetime.now(timezone.utc).isoformat(),'files':files,
      'producer_tree_sha256':tree,'test_count':23,'tests':'PASS_SYNTHETIC_DETERMINISTIC_ONLY',
      'real_extraction_executed':False,'independent_review':'PENDING',
      'guard_final_pin_recheck_required':True})
print(json.dumps({'producer_sha256':tree,'include_sha256':sha(OUT/'E2_INCLUDE_FINAL.json'),
                  'manifest_sha256':sha(OUT/'MANIFEST_FINAL.json')},indent=2))
