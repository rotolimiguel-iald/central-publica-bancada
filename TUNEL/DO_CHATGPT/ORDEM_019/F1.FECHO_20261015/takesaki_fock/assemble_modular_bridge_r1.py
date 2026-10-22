"""Join four not-yet-compiled consumers, preserving all proof bodies and prints."""
from pathlib import Path
import datetime, hashlib, json, os, re
BASE=Path(__file__).resolve().parent
NAMES=['CanonicalFockCoefficientFlowR13','CanonicalFockCoefficientGraphEqualityR9',
       'CanonicalFockModularIdentificationR9','CanonicalFockWeightPolarR2']
TARGET=BASE/'CanonicalFockModularBridgeR1.lean'
assert not TARGET.exists()
imports=[];bodies=[];pins=[]
def pin(p):
 b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
for name in NAMES:
 p=BASE/(name+'.lean')
 assert not list((BASE/'attempts').glob('*/'+name+'.lean')),name
 s=p.read_text(encoding='utf-8')
 pins.append(pin(p))
 for m in re.findall(r'^import\s+(\S+)',s,re.M):
  if m not in NAMES and m not in imports:imports.append(m)
 body=re.sub(r'^import[^\n]*\n','',s,flags=re.M)
 bodies.append('-- BEGIN EXACT BODY '+name+'\n'+body+'\n-- END EXACT BODY '+name+'\n')
data=('\n'.join('import '+m for m in imports)+'\n\n'+''.join(bodies)).encode('utf-8')
with TARGET.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert TARGET.read_bytes()==data
for p in pins:assert pin(Path(p['path']))==p
receipt={'unit':'F1.FECHO_20261015','claim':845,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'SOURCE_ASSEMBLED_NOT_YET_COMPILED','method':'Preserved complete source bodies, proof terms and all #print axioms; deduplicated imports and removed only imports internal to this join.',
 'inputs':pins,'output':pin(TARGET),'imports':imports,'script':pin(Path(__file__)),
 'namespaces_unchanged':True,'running_sources_repeated':False,'production_modified':False,'gate_modified':False}
with (BASE/'MODULAR_BRIDGE_ASSEMBLY_R1.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
print(json.dumps({'output':pin(TARGET),'receipt':pin(BASE/'MODULAR_BRIDGE_ASSEMBLY_R1.json')}))
