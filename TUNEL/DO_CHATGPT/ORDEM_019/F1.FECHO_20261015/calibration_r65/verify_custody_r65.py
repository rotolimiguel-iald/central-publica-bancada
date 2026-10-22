"""Verify stored evidence and byte backups, without executing scientific code."""
from pathlib import Path
import hashlib,json
import support_r65 as s

def verify(rows):
 for x in rows:assert s.pin(x['path'])['sha256']==x['sha256']
 return len(rows)
counts={}
for filename,key in [('DELIVERY_INTEGRATED_R65.json','evidence'),('sources/DELIVERY_R1.json','artifacts'),('calibration/DELIVERY_CALIBRATION_R65.json','evidence'),('FINAL_REVIEW_R65.json','evidence')]:
 d=json.loads((s.ROOT/filename).read_text());rows=d.get(key,d.get('artifacts',d.get('files',[])));assert rows;counts[filename]=verify(rows)
m=json.loads((s.ROOT/'MEMORY_APPLIED_R65.json').read_text())
for row in m['surfaces']:
 verify([row['backup'],row['after'],row['append']])
 old=Path(row['backup']['path']).read_bytes();now=Path(row['after']['path']).read_bytes();extra=Path(row['append']['path']).read_bytes()
 assert now==old+extra and hashlib.sha256(old).hexdigest()==row['before']['sha256']
counts['memory_surfaces']=len(m['surfaces'])
for row in json.loads((s.ROOT/'CANONICAL_PINS_R65.json').read_text())['checks']:verify([row['expected']])
p=s.project('FINAL_PROJECT_R65')
assert not any(h['id'].startswith('r65-') for h in p['projection']['flow']['handles'])
s.new('FINAL_CUSTODY_R65.json',{'status':'PASS_CUSTODY','counts':counts,'canonical_pins_unchanged':5,
 'mission_revision':p['receipt']['revision'],'delivery':s.pin(s.ROOT/'DELIVERY_INTEGRATED_R65.json'),
 'registration':s.pin(s.ROOT/'REGISTRATION_R65.json'),'active':[{'id':t['id'],'status':t['status']} for t in p['projection']['active']],
 'new_scientific_execution':False,'all_memory_backups_prefix_verified':True})
print(json.dumps({'status':'PASS_CUSTODY','counts':counts,'revision':p['receipt']['revision']}))

