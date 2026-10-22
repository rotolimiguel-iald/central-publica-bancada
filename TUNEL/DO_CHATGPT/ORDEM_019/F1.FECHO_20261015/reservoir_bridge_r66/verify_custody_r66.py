"""Verify R66 delivered bytes and append-only memory custody, read-only except receipt."""
from pathlib import Path
import json
import support_r66 as s

def verify_rows(rows):
 count=0
 for row in rows:
  assert s.pin(row['path'])['sha256']==row['sha256'],row['path']
  count+=1
 return count

def main():
 counts={}
 for name,key in [('DELIVERY_INTEGRATED_R66.json','evidence'),('construction/DELIVERY_CONSTRUCTION_R66.json','files'),('sources/DELIVERY_R66.json','artifacts'),('FINAL_REVIEW_R66.json','evidence')]:
  d=json.loads((s.ROOT/name).read_text(encoding='utf-8'));counts[name]=verify_rows(d[key])
 memory=json.loads((s.ROOT/'MEMORY_APPLIED_R66.json').read_text())
 for row in memory['surfaces']:
  before=Path(row['backup']['path']).read_bytes();after=Path(row['after']['path']).read_bytes();extra=Path(row['append']['path']).read_bytes()
  assert after==before+extra and s.pin(row['backup']['path'])['sha256']==row['before']['sha256']
  assert s.pin(row['after']['path'])==row['after'] and s.pin(row['append']['path'])==row['append']
 for row in json.loads((s.ROOT/'CANONICAL_PINS_R66.json').read_text())['checks']:assert s.pin(row['expected']['path'])==row['expected']
 m=s.project('FINAL_CUSTODY_PROJECT_R66')
 assert not m['projection']['flow']['handles']
 for t in m['projection']['active']:
  if t['id'] in ['R4','R5']:assert t['status']=='open' and t['lease'] is None
 result={'status':'PASS_CUSTODY','manifests_verified':counts,'memory_surfaces':len(memory['surfaces']),'canonical_pins_unchanged':5,'revision':m['receipt']['revision'],'R4_R5':'open_leases_released','registration':s.pin(s.ROOT/'REGISTRATION_R66.json')}
 s.new('FINAL_CUSTODY_R66.json',result);print(json.dumps(result))
if __name__=='__main__':main()
