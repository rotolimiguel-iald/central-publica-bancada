"""Verify stored artifacts, append prefixes and final mission state without rerunning science."""
from pathlib import Path
import hashlib,json
import support_r64 as s

def verify(rows):
    for row in rows:assert s.pin(row['path'])['sha256']==row['sha256']
    return len(rows)

d=json.loads((s.ROOT/'DELIVERY_INTEGRATED_R64.json').read_text());counts={'delivery':verify(d['evidence'])}
for file,key in [('output/DELIVERY_OUTPUT_R64.json','evidence'),('sources/DELIVERY_R1.json','files'),('output/FREEZE_R64.json','files'),('FINAL_REVIEW_R64.json','evidence')]:
    counts[file]=verify(json.loads((s.ROOT/file).read_text())[key])
m=json.loads((s.ROOT/'MEMORY_APPLIED_R64.json').read_text())
for row in m['surfaces']:
    verify([row['after'],row['backup'],row['append']])
    old=Path(row['backup']['path']).read_bytes();now=Path(row['after']['path']).read_bytes();extra=Path(row['append']['path']).read_bytes()
    assert now==old+extra and hashlib.sha256(old).hexdigest()==row['before']['sha256']
counts['memory_surfaces']=len(m['surfaces'])
for row in json.loads((s.ROOT/'CANONICAL_PINS_R64.json').read_text())['checks']:verify([row['expected']])
p=s.project('FINAL_PROJECT_R64')
assert not any(h['id'].startswith('r64-') for h in p['projection']['flow']['handles'])
s.new('FINAL_CUSTODY_R64.json',{'status':'PASS_CUSTODY','counts':counts,'canonical_pins_unchanged':5,
 'mission_revision':p['receipt']['revision'],'delivery':s.pin(s.ROOT/'DELIVERY_INTEGRATED_R64.json'),
 'registration':s.pin(s.ROOT/'REGISTRATION_R64.json'),'active':[{'id':t['id'],'status':t['status']} for t in p['projection']['active']],
 'new_scientific_execution':False,'all_memory_backups_prefix_verified':True})
print(json.dumps({'status':'PASS_CUSTODY','counts':counts,'revision':p['receipt']['revision']}))

