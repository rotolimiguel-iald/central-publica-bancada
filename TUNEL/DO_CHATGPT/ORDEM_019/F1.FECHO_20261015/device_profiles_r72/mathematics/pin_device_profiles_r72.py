from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
specs=[
 (BASE/'maxwell_global/PhysicalSchwartzMaxwellR1.lean',['def physicalFourierCLM','def physicalSmearCLM','theorem physicalSmear_ae']),
 (BASE/'maxwell_global/SchwartzMaxwellCoefficientR5.lean',['def globalCoefficient (','theorem globalCoefficient_sq_bound']),
 (BASE/'orbital_rotation/PhysicalSmearTranslationR2.lean',['def circularSmear (']),
 (BASE/'maxwell_global/CircularPhysicalFieldTransportR1.lean',['def unitaryFourierFieldAmplitude :','def normalizedCircularSmearCLM :']),
 (BASE/'orbital_rotation/PhysicalCompactNetCovarianceR1.lean',['def compactSupportedGenerators','def compactLocalized (']),
 (BASE/'network_bundle_r7/src/TGLExt/F1Fecho394/FieldWeylR3.lean',['def W (f :','theorem W_mem_R (']),
 (BASE/'maxwell_global/RegularMaxwellEnergyR2.lean',['def EnergySquareProfile (','theorem coefficient_square_moment_density_bound','theorem physicalSmear_strongRegular','theorem strongRegular_finite_energy']),
 (BASE/'orbital_rotation/RegularCoefficientBoundaryR3.lean',['theorem circularSmear_energySquare']),
 (BASE/'maxwell_global/SchwartzRestrictionSquareMomentsR1.lean',['theorem energy_moment_square_restriction_integrable']),
 (BASE/'maxwell_global/MaxwellShellGeometryR3.lean',['def shellEnergy (','theorem shellEnergy_sq']),
 (BASE/'local_error_r71/locality/BOGOLIUBOV_CAVITY_R71.md',['## 2. Implementação','## 4. Transporte']),
 (BASE/'reservoir_bridge_r66/BOSONIC_CONTINUUM_R66.txt',['h_0=','J=A+B=','6. Ponte ao Fock']),
 (BASE/'reservoir_bridge_r66/JOINT_RESERVOIR_CONTINUUM_LIMIT_R66.txt',['Fixe as taxas','É uma realização construída']),
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
d={'schema':'r72-device-profile-mathematics-pins/v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Analytic candidate, NOT_LEAN, no numerical campaign or observed data',
 'mission':{'reference':r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json','revision':506,'task_id':'R5','lease_id':'ec98434f-b7cf-4bfb-b311-a6810dda408b','preflight_ready':True,'projection_sha256':'595f20ae8c350997097203e17512451211f1aef13547cb7068eb203dbabe52fb'},
 'sources':sources,'report':pin(ROOT/'DEVICE_PROFILE_BRIDGE_R72.md'),'script':pin(Path(__file__).resolve())}
with (ROOT/'SOURCE_PINS_DEVICE_PROFILE_R72.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'sources':len(sources),'report':d['report']},ensure_ascii=False))
