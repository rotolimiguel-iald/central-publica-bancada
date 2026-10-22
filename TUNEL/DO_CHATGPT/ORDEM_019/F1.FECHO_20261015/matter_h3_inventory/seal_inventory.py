"""Create a new, bounded reuse inventory; all output paths must be absent."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

BASE = Path(__file__).resolve().parent
UNIT = BASE.parent
ORDER = UNIT.parent
CHAT = ORDER.parents[2]
K = UNIT / 'candidate_r3/tgl_kernel/TGLExt'

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def new(name, value):
    p = BASE / name
    b = value.encode('utf-8') if isinstance(value, str) else (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    with p.open('xb') as f:
        f.write(b)
    return pin(p)

sources = [
    ('maxwell_bridge', K/'MaxwellLiteratureBridge.lean', [(37,53),(59,115),(120,136)]),
    ('imported_sq', K/'TheImportedSecondQuantization.lean', [(235,263),(498,516),(547,593)]),
    ('stress_v32', K/'ContratoQG_v32.lean', [(41,66)]),
    ('stress_v31', K/'ContratoQG_v31.lean', [(109,110),(178,183),(276,296)]),
    ('boost_energy', K/'O16/ModularBoostEnergyReuse_v2.lean', [(9,38)]),
    ('modular_charge', K/'O16/ModularChargeLink.lean', [(11,42)]),
    ('null_solution', K/'O16/TeleologicalNullSolution_v2.lean', [(9,48)]),
    ('null_consumer', K/'O16/NullSolutionConsumerReuse.lean', [(18,58)]),
    ('classical_maxwell', K/'O16/MaxwellPolynomial_v2.lean', [(1,49)]),
    ('zero_negative', ORDER/'F1.REDE/fock_construction/CertificateNegativeProbe.lean', [(1,40)]),
    ('curved_bridge', K/'LiganteLeiCampoCurvo.lean', [(32,97)]),
    ('curved_controls', K/'LiganteLeiCampoCurvoTestemunha.lean', [(32,57),(175,202),(265,295)]),
    ('horizon_reconstruction', K/'HorizonEinsteinReconstruction.lean', [(101,130)]),
    ('fock_obligations', ORDER/'F1.REDE/MATRIZ_CONTRATO_FOCK_R2.json', [(155,175)]),
    ('fock_construction', ORDER/'F1.REDE/CONSTRUCAO_CONTINUA_R1.md', [(140,158)]),
    ('new_network_assembly', UNIT/'network_reuse/CanonicalFockAssemblyR1.lean', [(1,45),(210,240)]),
    ('star_commutant', K/'V350DualFixedCore.lean', [(14,21)]),
    ('commutant', K/'Commutant.lean', [(22,30),(65,88)]),
    ('conjugation', K/'TheConjugationMapsCommutants.lean', [(49,80)]),
    ('biinverse_conjugation', K/'TheOathOnTheTower.lean', [(73,87)]),
]
source_rows = []
for label,p,ranges in sources:
    lines = p.read_text(encoding='utf-8-sig').splitlines()
    source_rows.append({'id':label, **pin(p), 'read_ranges':ranges,
        'excerpts':[{'first':a,'last':min(b,len(lines)), 'text':'\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,min(b,len(lines))))} for a,b in ranges]})
source_manifest = new('SOURCE_PINS_R1.json', {'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':source_rows,
    'source_status':'Source statements inspected locally; only the new adapter is compiled in this delivery. Prior audit/build status is not recreated by textual inspection.'})

roots = [ORDER, ORDER.parent/'FECHAMENTO_PARCIAL_016', CHAT/'ORDEM_016_QG']
pattern = re.compile(r'MaxwellQuadraticForm|MaxwellCertificate|charge_link|Q_conserved|NamedAtlasH3|modular_charge_of_boost_charge')
files = set()
for root in roots:
    run = subprocess.run(['rg','--files',str(root),'-g','*.lean','-g','!.lake/**'],capture_output=True,text=True,check=True,encoding='utf-8')
    files.update(Path(s) for s in run.stdout.splitlines() if s)
groups = {}
for p in sorted(files):
    if BASE in p.parents or '.lake' in p.parts:
        continue
    raw = p.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    found = [{'line':i+1,'text':s} for i,s in enumerate(lines) if pattern.search(s)]
    if not found:
        continue
    h = hashlib.sha256(raw).hexdigest()
    g = groups.setdefault(h,{'sha256':h,'bytes':len(raw),'aliases':[], 'matches':found})
    g['aliases'].append(str(p))
search_manifest = new('SEARCH_REUSE_R1.json', {'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'roots':list(map(str,roots)), 'file_filter':'*.lean; .lake and this new output folder excluded', 'pattern':pattern.pattern,
    'paths_scanned':len(files), 'matched_paths':sum(len(g['aliases']) for g in groups.values()), 'unique_bytes':len(groups),
    'groups':list(groups.values()), 'limit':'Bounded source inventory plus semantic inspection of cited definitions. No claim of absence in the entire scientific corpus or equivalence of uninspected textual matches.'})

receipts = sorted((BASE/'attempts').glob('*/BUILD_RECEIPT.json'))
passed = [(p,json.loads(p.read_text(encoding='utf-8'))) for p in receipts if json.loads(p.read_text(encoding='utf-8'))['passed']]
if not passed:
    raise RuntimeError('No successful adapter build; no delivery can be emitted')
build_path, build = passed[-1]
source = BASE/'src/TGLExt/MaxwellBoostChargeAssemblyR1.lean'
if pin(source)['sha256'] != build['source']['sha256']:
    raise RuntimeError('Draft differs from accepted build snapshot')

obligations = {
 'unit':'F1.FECHO_20261015','claim_event':845,'actor':'codex-gerente-tgl / delegated first_law_haja_luz',
 'verdict':'CONDITIONAL_WIRING_COMPILED__R8_R9_PHYSICAL_RESIDUES_RETAINED',
 'rows':[
 {'id':'R8_SYMMETRY_CONSERVATION','status':'EXISTS_AND_WIRED_CONDITIONALLY',
  'source':'maxwell_bridge:37-53,73-104; stress_v32:48-58',
  'finding':'MaxwellQuadraticForm already carries symmetry, test-integrability and weak distributional Minkowski conservation. toStress transfers them and preserves Q on its named domain; MaxwellCertificate.T uses the stronger local V32 type.',
  'remaining':'Prove these fields for the physical Wick tensor on the same concrete Fock/domain. Their presence in a structure is not their physical construction.'},
 {'id':'R8_PHYSICAL_Q','status':'OPEN_CONSTRUCTION_IN_INSPECTED_SOURCES',
  'source':'maxwell_bridge:37-53; classical_maxwell:12-47; zero_negative:9-40',
  'finding':'Classical polynomial Maxwell stress, symmetry, trace and null-square identities exist. The quantum interface itself does not enforce quadratic scaling or polarization; Wick provenance is documentary. A zero form inhabits that interface, while the full certificate rules out an everywhere-zero tensor.',
  'remaining':'Same-realization operator-valued field/Wick tensor, regular invariant domain, finite null-plane integral and an exhibited regular state with nonzero charge. No zero form is offered as a realization.'},
 {'id':'R8_CHARGE_LINK','status':'DERIVED_CONDITIONAL_ADAPTER_COMPILED',
  'source':'boost_energy:9-38; modular_charge:17-22; new_adapter:22-71',
  'finding':'Actual boost matrix-coefficient derivative equal to the integrated stress charge implies modular energy 2*pi times that charge. A regular nonzero charge then gives the nontrivial modular witness. assembleMaxwell consumes both and preserves the original Q on its domain.',
  'remaining':'BoostChargeIdentity and NonzeroChargeState are explicit physical inputs, not proven inhabitants. The adapter derives the modular conclusion; it does not assume charge_link itself.'},
 {'id':'R9_STANDARD_WEDGE','status':'EXISTS_AND_NEW_ADAPTER_CONSUMES',
  'source':'imported_sq:547-563; null_solution:23-48; null_consumer:18-58; stress_v31:109',
  'finding':'lightH3/lightH3v32 already construct H3 conditionally from MaxwellCertificate, via a teleological null solution, on the same standard boost/horizon and fixed nullDir=(1,1,0,0), at every basepoint. standardWedgeH3 composes the new Maxwell adapter with this existing consumer.',
  'remaining':'This is not all-null-direction curved H3; no new global Lorentz family is constructed here.'},
 {'id':'R9_ALL_DIRECTIONS_CURVED','status':'IMPLICATION_PROVEN_IN_EXISTING_SOURCE__ANTECEDENT_OPEN_PHYSICAL_IDENTIFICATION',
  'source':'curved_bridge:32-97; curved_controls:32-57,265-295; horizon_reconstruction:101-130',
  'finding':'NamedAtlasH3 quantifies over each chart, point and nonzero null vector. Together with covariant conservation and atlas compatibility it implies Einstein with unique Lambda and eta=(4G)^-1. s5_local identifies its null-Ricci content; s8_h3_is_load_bearing supplies a conserved-source countermodel without H3.',
  'remaining':'Identify the same physical Maxwell tensor with recordSource in a regular metric/atlas; transport the field/domain/state through the required Lorentz directions; establish the named all-direction closure. Flat distributional conservation is not automatically pointwise covariant conservation. Foundation passage is logically idle in this implication.'},
 {'id':'R7_SCOPE','status':'SEPARATE_OBLIGATION_RETAINED',
  'source':'imported_sq:235-263',
  'finding':'The certificate Core/trace is a reduced algebraic interface (trace:Core→ENNReal, traciality on all products and scaling). Filling it does not identify a concrete crossed product or a normal semifinite faithful weight with analytic positive-cone domain.',
  'remaining':'The concrete Takesaki/crossed-product/weight identification remains separate; this inventory neither audits it globally nor closes it.'},
 {'id':'WEYL_NET_ADAPTER','status':'GENERIC_INGREDIENTS_EXIST__SEPARATE_PARENT_WORK',
  'source':'star_commutant:14-21; commutant:65-88; conjugation:49-80; biinverse_conjugation:73-87',
  'finding':'starCommutantAlgebra, commutant antitonicity, bicommutant monotonicity and conjugation by a multiplicative bijection with inverse already exist. No assembled Weyl-to-net adapter was located in the inspected F1.REDE Lean. Parent is constructing the generic adapter separately.',
  'remaining':'Actual W on concrete Fock, its star relation/Weyl commutation and covariance. Star commutant and ordinary commutant need the generator star-closure identification. W=I is not a physical substitute.'}
 ],
 'compile':pin(build_path),
 'nonvacuity_limit':'The new result is a conditional adapter. It supplies no physical Q, complete C, BoostChargeIdentity or NonzeroChargeState inhabitant. It retains nonzero charge as an explicit obligation and uses it nontrivially.',
 'new_adapter_dependencies':[pin(Path(build['LEAN_PATH'].split(';')[0])/'TGLExt'/name) for name in ['MaxwellLiteratureBridge.olean','TheImportedSecondQuantization.olean','O16/ModularBoostEnergyReuse_v2.olean','O16/ModularChargeLink.olean']],
 'build_receipt_note':'The reusable TimeGraviton source pins in the generic build runner are incidental context, not Maxwell dependency claims; exact Maxwell imported olean pins are recorded above.',
 'source_manifest':source_manifest,'search_manifest':search_manifest,
 'no_changes':['canonic kernel','um.py','Bancada','memory','gate','observed data'],
 'providers_called':0,
}
obligation_manifest = new('OBLIGATIONS_R8_R9_R1.json', obligations)
byid = {s['id']:s for s in source_rows}
def short(label):
    return byid[label]['sha256'][:16]
report = [
 '# R8/R9 — reaproveitamento e fiação condicional (15/10/2026)',
 '[REAL local] Novo adaptador: EXIT 0, seis declarações no trio; Q físico e identidade boost–carga seguem hipóteses explícitas.',
 f'1. MaxwellLiteratureBridge.lean:37–53,73–104 ({short("maxwell_bridge")}): simetria/conservação distribucional plana já entram em StressTensorDataLocalV32; não refazer.',
 f'2. MaxwellPolynomial_v2.lean:12–47 ({short("classical_maxwell")}): tensor clássico e identidades algébricas existentes; não é construção Wick no Fock.',
 f'3. CertificateNegativeProbe.lean:9–40 ({short("zero_negative")}): forma zero passa pela interface fina, mas o certificado inteiro exclui tensor sempre zero.',
 f'4. ModularBoostEnergyReuse_v2.lean:9–38 ({short("boost_energy")}): derivada do boost → energia modular com 2π; composição nova constrói charge_link e testemunha não nula.',
 '5. MaxwellBoostChargeAssemblyR1.lean:22–71 preserva Q no domínio e entrega standardWedgeH3; não exibe habitante físico das hipóteses.',
 f'6. TheImportedSecondQuantization.lean:547–563 ({short("imported_sq")}): H3 da cunha padrão já construído via resposta nula; direção nullDir fixa, não todas as direções.',
 f'7. LiganteLeiCampoCurvo.lean:32–97 ({short("curved_bridge")}): H3 nomeado de toda direção + conservação covariante → Einstein/Λ único; passagem da Fundação ociosa.',
 f'8. LiganteLeiCampoCurvoTestemunha.lean:32–57,265–295 ({short("curved_controls")}): conteúdo Ricci nulo do H3 e contramodelo conservado mostram seu peso real.',
 '9. [OPEN] Construir Q/Wick e estado regular não nulo na realização comum; provar boost–carga; identificar recordSource/métrica e transportar para todas as direções.',
 '10. R7 separado: Core/trace do certificado é interface reduzida; preencher campos não identifica produto cruzado/peso analítico normal semifinito.',
 f'11. TheOathOnTheTower.lean:73–87 ({short("biinverse_conjugation")}): covariância genérica do comutante já existe; adaptador Weyl→R(K) fica com o pai.',
 'Busca delimitada, trechos e SHA256 completos: SOURCE_PINS_R1.json, SEARCH_REUSE_R1.json; obrigações tipadas: OBLIGATIONS_R8_R9_R1.json.',
 'R8/R9 não promovidas a fechadas. Sem mudança canônica, memória, produção, provedor, dado ou gate.',
]
report_pin = new('INVENTARIO_R8_R9_R1.md','\n'.join(report)+'\n')
delivery = {'unit':'F1.FECHO_20261015','claim_event':845,'verdict':obligations['verdict'],
 'source':pin(source),'builder':pin(BASE/'build_maxwell_wiring.py'),'sealing_script':pin(Path(__file__)),
 'accepted_build':pin(build_path),'attempts':[pin(p) for p in receipts],
 'artifacts':[source_manifest,search_manifest,obligation_manifest,report_pin],
 'summary':'Reusable tensor symmetry/conservation and standard-wedge H3 preserved; new boost-charge-to-Maxwell assembly checked. Physical Q, derivative identity, regular nonzero state and all-direction curved identification remain explicit.'}
p = new('DELIVERY_R1.json',delivery)
print(json.dumps(p,ensure_ascii=False))
