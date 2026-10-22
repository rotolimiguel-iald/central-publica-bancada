"""Verify custody and exact additive writes without rerunning scientific work."""
from support_r88 import ROOT, new, pin
from pathlib import Path
import json

delivery=json.loads((ROOT/'DELIVERY_R88.json').read_text(encoding='utf-8'))
for evidence in delivery['evidence']:
    assert pin(evidence['path'])==evidence, evidence['path']
result=json.loads((ROOT/'RESULTADO_R88.json').read_text(encoding='utf-8'))
for evidence in result['evidence']:
    assert pin(evidence['path'])==evidence, evidence['path']
applied=json.loads((ROOT/'MEMORY_APPLIED_R88.json').read_text(encoding='utf-8'))
extra=(ROOT/'MEMORY_APPEND_R88.txt').read_bytes()
assert len(applied['surfaces'])==8
for row in applied['surfaces']:
    assert pin(row['after']['path'])==row['after']
    assert pin(row['backup']['path'])==row['backup']
    assert row['before']['sha256']==row['backup']['sha256']
    assert Path(row['after']['path']).read_bytes()==Path(row['backup']['path']).read_bytes()+extra
transition=json.loads((ROOT/'FINAL_TRANSITION_RESULT.json').read_text(encoding='utf-8'))
assert transition['exit_code']==0 and transition['response']['ok']
for name in ['MAP_REGISTER_RESULT.json','BOARD_REGISTER_RESULT.json']:
    assert json.loads((ROOT/name).read_text(encoding='utf-8'))['exit_code']==0
out={'status':'PASS','delivery_pins':len(delivery['evidence']),
     'scientific_pins':len(result['evidence']),'pure_appends_and_byte_backups':8,
     'goal_complete':False,'H3_universal_proved':False,'scientific_reruns':0,
     'delivery':pin(ROOT/'DELIVERY_R88.json'),'registration':pin(ROOT/'REGISTRATION_R88.json'),
     'transition':pin(ROOT/'FINAL_TRANSITION_RESULT.json')}
new('VERIFIED_DELIVERY_R88.json',out)
print(json.dumps(out,ensure_ascii=False))
