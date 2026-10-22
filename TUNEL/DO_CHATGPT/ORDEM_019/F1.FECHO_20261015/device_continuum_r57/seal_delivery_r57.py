"""Seal local scientific delivery from actual sources and completed receipts."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
from mission_r57 import ROOT, REFERENCE, ACTOR, pin, save, check

OUT=ROOT.parent
NET=OUT.parent/'F1.REDE'
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
NAMES=['TowerBoostObstructionR2','CompactPacketRefinementR1','ComplexPacketLimitR1']

def pinned(path):
    p=Path(path)
    return {**pin(p),'bytes':p.stat().st_size}

def anchor(path, terms):
    p=Path(path); lines=p.read_text(encoding='utf-8').splitlines()
    found={term:next((i+1 for i,l in enumerate(lines) if term in l),None) for term in terms}
    assert all(v is not None for v in found.values()), (str(p), found)
    return {**pinned(p),'anchors':found}

def component(name):
    source=ROOT/(name+'.lean')
    good=[]
    for p in ROOT.glob('attempts/*/RECEIPT.json'):
        r=json.loads(p.read_bytes())
        if Path(r['source']['path']).name==source.name and r['exit_code']==0:
            assert r['source']['sha256']==pin(source)['sha256']
            good.append((p,r))
    assert len(good)==1,(name,len(good))
    receipt,r=good[0]
    for x in r['dependencies']+r['artifacts']+[r['source_original']]:
        assert pinned(x['path'])['sha256']==x['sha256'],x['path']
    log=(receipt.parent/'AXIOMS.txt').read_text(encoding='utf-8')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log,re.S)
    assert 'sorryAx' not in log and 'error:' not in log
    assert len(reports)==source.read_text(encoding='utf-8').count('#print axioms')
    parsed=[{'declaration':n,'axioms':[a.strip() for a in ax.split(',') if a.strip()]} for n,ax in reports]
    assert all(set(x['axioms']) <= {'propext','Classical.choice','Quot.sound'} for x in parsed)
    return dict(name=name,statute='REAL Lean compiled component; independent review pending',
        source=pinned(source),snapshot=pinned(Path(r['source']['path'])),
        olean=pinned(receipt.parent/(name+'.olean')),receipt=pinned(receipt),
        build_log=pinned(receipt.parent/'BUILD.log'),axioms=pinned(receipt.parent/'AXIOMS.txt'),
        exit_code=r['exit_code'],seconds=r['seconds'],memory_limit_mb=r['memory_limit_mb'],
        dependency_pins_rechecked=len(r['dependencies']),artifact_pins_rechecked=len(r['artifacts']),
        source_unchanged=r['source_unchanged'],readonly_dependencies_unchanged=r['readonly_dependencies_unchanged'],
        reports=parsed,trio_only=True,
        warnings=[line for line in log.splitlines() if ': warning:' in line],
        low_residual='Unused simp argument in ComplexPacketLimitR1:89, preserved; no mathematical defect or new repair/build.')

components=[component(n) for n in NAMES]
candidate=json.loads((ROOT/'PACKET_CANDIDATE_R1.json').read_bytes())
assert candidate['source']['sha256']==components[1]['source']['sha256']==components[1]['snapshot']['sha256']
chain={'candidate_manifest':pinned(ROOT/'PACKET_CANDIDATE_R1.json'),
       'candidate_current_snapshot_identical':True,'measured_bytes':components[1]['source']['bytes'],
       'measured_sha256':components[1]['source']['sha256'],
       'historical_8332_bytes':{'statute':'DECLARADO coordinator observation of source in motion before freeze',
           'preserved_artifact_located':False,'sha256':None,
           'note':'No fabricated retrospective custody. Additive movePacket_mono/packetMove_refinement and prints were edited before PACKET_CANDIDATE_R1 freeze and before the successful build.'}}
chain_path=ROOT/'PACKET_CHAIN_R57_R1.json'
if chain_path.exists():
    assert json.loads(chain_path.read_bytes())==chain
else:
    save(chain_path,chain)

sources=[
 anchor(KERNEL/'TGLExt/ModularFlowSpectrum.lean',['theorem modularFlow_eigenvector','theorem localEigenvectors_total']),
 anchor(KERNEL/'TGLExt/ModularFlowLevel.lean',['def modularPhase','theorem modularPhase_norm']),
 anchor(KERNEL/'TGLExt/TowerHilbert.lean',['abbrev TowerHilbert','theorem hOmega_norm']),
 anchor(KERNEL/'TGLExt/TowerDefinite.lean',['structure SiteProfile','def TowerPre']),
 anchor(KERNEL/'TGLExt/TheImportedSecondQuantization.lean',['abbrev H1','theorem B0_no_eigen']),
 anchor(OUT/'orbital_rotation/PhysicalCanonicalNetCompleteR1.lean',['theorem compactLocalized_rightWedge_eq','def physicalCanonicalNet']),
 anchor(OUT/'orbital_rotation/PhysicalCompactNetCovarianceR1.lean',['def compactSupportedGenerators','def compactLocalized','theorem compact_translated_generator','theorem compact_lorentz_generator']),
 anchor(OUT/'orbital_rotation/PhysicalCanonicalWedgeEqualityR3.lean',['theorem physical_right_wedge_complex_dense']),
 anchor(OUT/'orbital_rotation/LorentzFutureRepresentationR1.lean',['abbrev FutureLorentz','def futureToGenerated']),
 anchor(OUT/'orbital_rotation/PhysicalFockSpacetimeCovarianceR2.lean',['theorem frameUnitary_eq_helicityPoincare','theorem spacetimeNet_future_lorentz']),
 anchor(NET/'CONTRATO_REDE_R2.md',['## 7.','## 10.']),
 anchor(Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\RESPOSTA_Q6_MORADA_PACOTE_HILBERT.md'),['### Isotonia','\\mathscr D_{\\mathcal O_2}\\iota_{21}']),
 pinned(NET/'sources/MQC_DESCRITIVO_EXTRACT_R1.txt'),
 pinned(OUT/'CONFERENCIA_PONTE_DISPOSITIVO_R55.json'),
 pinned(OUT/'CONFERENCIA_PONTE_DISPOSITIVO_R55.txt'),
 pinned(OUT/'global_net_inventory/R53/DEVICE_CONTINUUM_SOURCE_AUDIT_R1.txt'),
 pinned(OUT/'continuity_r57/REUSE_PACKAGE_R57.json'),
 pinned(OUT/'continuity_r57/NOS_VIVO_QUERY_R57.json'),
 pinned(OUT/'continuity_r57/SOURCE_JAN09_CUSTODY_R57.json'),
 pinned(OUT/'continuity_r57/sources/SUPERCONDUTOR_JAN09_EXTRACT_R57.txt'),
]
p,pr,c,cr=check()
task=next(x for x in p['projection']['active'] if x['id']=='R5')
delivery={
 'schema':'R57_DEVICE_CONTINUUM_COMPONENT_DELIVERY_R1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'author':ACTOR['id'],'reference':pinned(REFERENCE),'task_id':'R5','criterion_literal':task['criterion'],
 'requirement_satisfied':False,'full_physical_device_realization':False,'independent_review':'PENDING',
 'final_sync':{'revision':p['receipt']['revision'],'projection':pinned(pr),'preflight':pinned(cr),'lease':task['lease']},
 'components':components,
 'targets':[
  {'id':'1_product_tower_obstruction','statute':'REAL Lean theorem',
   'statement':'For every SiteProfile P, clock : real -> real and bounded complex-linear V : TowerHilbert P -> H1, (forall s x, V(modularFlow P (clock s) x)=B0 s(Vx)) implies V=0.',
   'proof':'Existing total local eigenfamily + unit-modulus modularPhase + existing B0_no_eigen; density extends zero to the whole source.',
   'nonvacuity':'hOmega has norm1; hence no isometric intertwiner of the stated orientation.',
   'scope':'Only the existing product-tower modularFlow; not a general device no-go, not the Fock action, not a claim that MQC equals a binary product tower.'},
  {'id':'2_existing_net_packet_target','statute':'REAL Lean construction',
   'statement':'Finite compact-smear lists define directed finite-dimensional real packet subspaces of the SAME H1, literal isometric inclusions, exact local closure=compactLocalized, translations/Lorentz moving packets and commuting refinement diagrams. Complexified packet union is dense directly in the SAME H1.',
   'scope':'Target approximation family; no cell-to-packet map, microscopic state, dynamic or device refinement has been invented. Real localization is kept separate from global complexification.'},
  {'id':'3_physical_residual','statute':'OPEN',
   'statement':'MQC cell, Supercondutor dynamics and Psi-NET protocol remain complementary. Derive cell field labels, two-point state forms, compatible maps into actual tensor smears, dense/scaling-limit correlation control, physical Poincare/reflection action and localization intertwining.',
   'q6':'Exact D_O2 iota = iota D_O1 for regional isotony is distinct from strong convergence of dynamics along refinements; neither was silently weakened.'}],
 'criterion_matrix':[
  {'item':'Canonical global Maxwell net on H1','status':'REAL preexisting, reused','new_device_claim':False},
  {'item':'Finite directed target packets with exact recovery/density','status':'REAL newly compiled','new_device_claim':False},
  {'item':'Canonical Poincare/localization structure','status':'REAL preexisting; packet covariance for translation/future Lorentz/boost constructed','new_device_claim':False},
  {'item':'Microscopic cells/refinements and compatible positive states from sources','status':'OPEN'},
  {'item':'Unitary physical-sector identification and all required intertwining including reflection','status':'OPEN'},
  {'item':'R5 integral','status':'OPEN; requirement_satisfied=false'}],
 'source_custody':sources,'packet_chain':pinned(ROOT/'PACKET_CHAIN_R57_R1.json'),
 'residual_contract':pinned(ROOT/'RESIDUAL_TYPED_CONTRACT_R1.txt'),
 'recovery':pinned(ROOT/'RECOVERY_VERIFICATION_R1.json'),
 'lease_recovery':pinned(ROOT/'RESUME_LEASE_R57_R1.json'),
 'launcher':pinned(ROOT/'build_r57_r2.py'),'sealer':pinned(Path(__file__)),
 'failed_history':{'source':pinned(ROOT/'TowerBoostObstructionR1.lean'),
   'receipt':pinned(ROOT/'attempts/20261017T091654_656547Z/RECEIPT.json'),
   'reason':'ext descended to Lp ae equality; explicit ContinuousLinearMap.ext repaired in R2. Failed R1 contains sorryAx and is not accepted.',
   'prelaunch_resolver_correction':pinned(ROOT/'BUILD_PREFLIGHT_CORRECTION_R1.json')},
 'restrictions':{'production_modified':False,'originals_modified':False,'provider_calls':0,'kernel_builds':0,
   'existing_green_builds_repeated':False,'canonical_memory_written':False,'R5_accepted':False},
}
save(ROOT/'DELIVERY_R57.json',delivery)
print(json.dumps({'delivery':pinned(ROOT/'DELIVERY_R57.json'),'reports':sum(len(x['reports']) for x in components),
 'revision':p['receipt']['revision'],'requirement_satisfied':False},ensure_ascii=False))
