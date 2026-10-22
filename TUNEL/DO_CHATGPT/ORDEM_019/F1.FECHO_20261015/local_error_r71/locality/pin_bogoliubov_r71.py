from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
LEAN=BASE/'network_bundle_r7/src/TGLExt/F1Fecho394'
specs=[
 (LEAN/'OneParticleDualityR2.lean',['theorem Jcandidate_image_equals_symplectic :']),
 (LEAN/'WedgeNonisotropicR5.lean',['theorem KWR_inter_JKWR_zero','theorem KWR_not_isotropic :']),
 (LEAN/'FubiniL2.lean',['noncomputable def canonicalPartialFourier :']),
 (BASE/'orbital_rotation/PhysicalCompactNetCovarianceR1.lean',['def compactSupportedGenerators','def compactLocalized (']),
 (BASE/'orbital_rotation/PhysicalCompactNetAssemblyR1.lean',['theorem compactPhysicalNet_wedge_glue','def physicalCanonicalNet :']),
 (LEAN/'FieldWeylR3.lean',['def W (f :','def R (K :','theorem W_mem_R (']),
 (LEAN/'WedgeCyclicR3.lean',['theorem canonical_wedge_separating (']),
 (BASE/'segal_selfadjoint/CanonicalSegalEssentialR6.lean',['def segalFlow']),
 (BASE/'reservoir_bridge_r66/BOSONIC_CONTINUUM_R66.txt',['h_0=','3. Construção conservativa','4. Bombeamento','5. Aproximação finita','6. Ponte ao Fock']),
 (BASE/'reservoir_bridge_r66/JOINT_RESERVOIR_CONTINUUM_LIMIT_R66.txt',['Fixe as taxas','Assim, para qualquer precisão']),
 (BASE/'local_interaction_r70/locality/LOCAL_INTERACTION_R70.md',['## 3. Teorema tangente','## 6. Diferença']),
 (BASE/'correspondence_bridge_r69/LOCALITY_BRIDGE_R69.md',['## 3. Passagem']),
 (ROOT/'ENERGY_ERROR_R71.md',['# R71']),
]
sources=[]
for path,markers in specs:
 raw=path.read_bytes();lines=raw.decode('utf-8-sig').splitlines();anchors=[]
 for marker in markers:
  hits=[i for i,line in enumerate(lines,1) if marker in line]
  if len(hits)!=1:raise RuntimeError((str(path),marker,hits))
  n=hits[0];end=min(n+12,len(lines));anchors.append({'marker':marker,'line':n,'through':end,'excerpt':'\n'.join(lines[n-1:end])})
 sources.append({'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'anchors':anchors})
def pin(p):
 raw=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
d={'schema':'r71-local-bogoliubov-pins/v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Analytic derivation, NOT_LEAN; finite implementation constructed in text; no numerical or provider execution',
 'mission_revision_observed':501,'sources':sources,'report':pin(ROOT/'BOGOLIUBOV_CAVITY_R71.md'),'script':pin(Path(__file__).resolve())}
with (ROOT/'SOURCE_PINS_BOGOLIUBOV_R71.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'sources':len(sources),'report':d['report']},ensure_ascii=False))
