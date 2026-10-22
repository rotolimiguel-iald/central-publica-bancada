from pathlib import Path
import hashlib, json, datetime

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
specs=[
 (BASE/'network_bundle_r7/src/TGLExt/F1Fecho394/WedgeCyclicR3.lean',['theorem vacuum_separating','theorem canonical_wedge_separating']),
 (BASE/'network_bundle_r7/src/TGLExt/F1Fecho394/WedgeNonisotropicR5.lean',['theorem KWR_not_isotropic']),
 (BASE/'network_bundle_r7/src/TGLExt/F1Fecho394/FieldWeylR3.lean',['def W (','theorem W_star','theorem W_ccr','def R (','theorem R_local','theorem W_mem_R']),
 (BASE/'orbital_rotation/PhysicalCompactNetAssemblyR1.lean',['theorem compactPhysicalNet_wedge_glue','def physicalCanonicalNet']),
 (BASE/'orbital_rotation/PhysicalCompactNetCovarianceR1.lean',['def compactLocalized','theorem compactLocalized_mono']),
 (BASE/'segal_selfadjoint/CanonicalSegalEssentialR6.lean',['def segalFlow','theorem segal_essentially_selfadjoint']),
 (KERNEL/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StandardSubspace.lean',['structure StandardSubspace','  IsSeparating : toClosedSubmodule ⊓ toClosedSubmodule.mulI = ⊥']),
 (BASE/'reservoir_bridge_r66/BOSONIC_CONTINUUM_R66.txt',['h_0=','L=(sqrt','J=A+B=','3. Construção','6. Ponte']),
 (BASE/'reservoir_bridge_r66/construction/CONSTRUCTION_R66.md',['## 1. Colisão','## 2. Vácuo','## 3. O bombeamento','## 4. Convergência']),
 (BASE/'reservoir_bridge_r66/JOINT_RESERVOIR_CONTINUUM_LIMIT_R66.txt',['Para δ=t/n','O limite é dos']),
 (BASE/'correspondence_bridge_r69/LOCALITY_BRIDGE_R69.md',['## 2. Composição','## 4. Obstáculo']),
]
sources=[]
for path,markers in specs:
 raw=path.read_bytes(); lines=raw.decode('utf-8-sig').splitlines(); anchors=[]
 for marker in markers:
  hits=[i for i,s in enumerate(lines,1) if marker in s]
  if len(hits)!=1: raise RuntimeError((str(path),marker,hits))
  n=hits[0]; end=min(n+10,len(lines))
  anchors.append({'marker':marker,'line':n,'through':end,'excerpt':'\n'.join(lines[n-1:end])})
 sources.append({'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'anchors':anchors})
def pin(path):
 raw=path.read_bytes();return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
data={'schema':'r70-locality-source-pins/v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'mission_revision_observed':496,'scope':'Analytic candidate and read-only source verification; no numerical campaign or Lean build',
 'sources':sources,'report':pin(ROOT/'LOCAL_INTERACTION_R70.md'),'script':pin(Path(__file__).resolve())}
with (ROOT/'SOURCE_PINS_LOCALITY_R70.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'source_count':len(sources),'report':data['report']},ensure_ascii=False))
