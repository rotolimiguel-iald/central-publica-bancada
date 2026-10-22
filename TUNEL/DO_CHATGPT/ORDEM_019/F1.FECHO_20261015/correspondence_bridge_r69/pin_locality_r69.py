from pathlib import Path
import hashlib, json, datetime

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
specs = [
    (BASE/'orbital_rotation/PhysicalCompactNetCovarianceR1.lean', ['def compactSupportedGenerators', 'def compactLocalized', 'theorem compactLocalized_lorentz_iff']),
    (BASE/'orbital_rotation/PhysicalCompactNetLocalityR2.lean', ['theorem compactLocalized_locality']),
    (BASE/'orbital_rotation/PhysicalCompactNetAssemblyR1.lean', ['theorem compactPhysicalNet_local', 'theorem compactPhysicalNet_wedge_glue', 'def physicalCanonicalNet', 'theorem physical_canonical_net_nonzero']),
    (BASE/'network_bundle_r7/src/TGLExt/F1Fecho394/FieldWeylR3.lean', ['def rotate', 'def W (', 'def R (', 'theorem R_local', 'theorem W_mem_R']),
    (BASE/'network_bundle_r7/src/TGLExt/F1Fecho394/ConcreteWeylR1.lean', ['theorem W_ccr', 'theorem R_local']),
    (BASE/'segal_selfadjoint/CanonicalSegalEssentialR6.lean', ['def segalFlow', 'theorem segal_essentially_selfadjoint']),
    (KERNEL/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StandardSubspace.lean', ['structure StandardSubspace', '  IsSeparating : toClosedSubmodule ⊓ toClosedSubmodule.mulI = ⊥']),
    (BASE/'anchored_contour_r68/AnchoredNameContourR68R3.lean', ['theorem exact_correspondence_iff', 'theorem complementary_residual_is_invisible_to_projection', 'theorem projection_alone_does_not_determine_input']),
    (BASE/'reservoir_bridge_r66/BOSONIC_CONTINUUM_R66.txt', ['2. Estrutura', '3. Construção', '5. Aproximação', '6. Ponte', '7. Covariância']),
    (BASE/'reservoir_bridge_r66/JOINT_RESERVOIR_CONTINUUM_LIMIT_R66.txt', ['Para δ=t/n', 'O limite é dos']),
    (BASE/'physical_receiver_r63/receiver/DERIVACAO_RECEPTOR_R63.md', ['## 2.', '## 4.', '## 5.']),
    (BASE/'maxwell_global/RealSchwartzTestsR1.lean', ['def IsRealTest', 'theorem real_imag_decomposition']),
]
sources=[]
for path, markers in specs:
    raw=path.read_bytes()
    lines=raw.decode('utf-8-sig').splitlines()
    anchors=[]
    for marker in markers:
        hits=[i for i,line in enumerate(lines,1) if marker in line]
        if len(hits)!=1:
            raise RuntimeError((str(path), marker, hits))
        n=hits[0]
        anchors.append({'marker':marker,'line':n,'through':min(n+9,len(lines)),'excerpt':'\n'.join(lines[n-1:min(n+9,len(lines))])})
    sources.append({'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'lines':len(lines),'anchors':anchors})
report=ROOT/'LOCALITY_BRIDGE_R69.md'
raw=report.read_bytes()
record={'schema':'r69-locality-source-pins/v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Read-only source examination and new written derivation; no compilation or production change',
    'mission_revision_observed':491,'source_count':len(sources),'sources':sources,
    'report':{'path':str(report),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)},
    'script':{'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
with (ROOT/'SOURCE_PINS_R69_LOCALITY.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(record,f,ensure_ascii=False,indent=2)
    f.write('\n')
print(json.dumps({'source_count':len(sources),'report':record['report']},ensure_ascii=False))
