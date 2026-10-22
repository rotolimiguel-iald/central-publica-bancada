from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
specs=[
 (BASE/'local_interaction_r70/locality/LOCAL_INTERACTION_R70.md',['## 3. Teorema tangente','## 4. Interação','## 6. Diferença']),
 (BASE/'reservoir_bridge_r66/BOSONIC_CONTINUUM_R66.txt',['h_0=','L=(sqrt','J=A+B=','2. Estrutura','5. Aproximação']),
 (BASE/'reservoir_bridge_r66/construction/CONSTRUCTION_R66.md',['Todos os cinco canais','## 3. O bombeamento']),
 (BASE/'correspondence_bridge_r69/LOCALITY_BRIDGE_R69.md',['## 3. Passagem','## 4. Obstáculo']),
 (BASE/'network_bundle_r7/src/TGLExt/F1Fecho394/FieldWeylR3.lean',['theorem vacuum_characteristic','def W (']),
 (BASE/'physical_receiver_r63/receiver/DERIVACAO_RECEPTOR_R63.md',['## 2. A POVM','## 3. O decoder']),
]
sources=[]
for path,markers in specs:
 raw=path.read_bytes();lines=raw.decode('utf-8-sig').splitlines();anchors=[]
 for marker in markers:
  hits=[i for i,line in enumerate(lines,1) if marker in line]
  if len(hits)!=1:raise RuntimeError((str(path),marker,hits))
  n=hits[0];end=min(n+10,len(lines));anchors.append({'marker':marker,'line':n,'through':end,'excerpt':'\n'.join(lines[n-1:end])})
 sources.append({'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'anchors':anchors})
def pin(p):
 raw=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
d={'schema':'r71-energy-error-pins/v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Analytic derivation, no new numerical campaign or Lean compilation','mission_revision_observed':501,
 'projection_recovery':{'first_budget':400000,'first_result':'ProjectionOverflow','successful_budget':1000000,'same_reference':True},
 'sources':sources,'report':pin(ROOT/'ENERGY_ERROR_R71.md'),'script':pin(Path(__file__).resolve())}
with (ROOT/'SOURCE_PINS_ENERGY_ERROR_R71.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'sources':len(sources),'report':d['report']},ensure_ascii=False))
