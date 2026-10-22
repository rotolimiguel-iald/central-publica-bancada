"""Freeze a source-based reuse inventory and a conditional wiring candidate.
Writes only new files beside this script. No compilation or production writes.
"""
from pathlib import Path
import datetime, hashlib, json, os, re

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
NET = ROOT / 'F1.REDE'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
K = KERNEL / 'TGLExt'

def save(name, data):
    data = data.encode('utf-8') if isinstance(data, str) else data
    with (BASE/name).open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert (BASE/name).read_bytes() == data

def record(path, anchors, classification, consumption, residue):
    data=path.read_bytes(); lines=data.decode('utf-8').splitlines()
    refs=[]
    for anchor in anchors:
        hits=[i+1 for i,line in enumerate(lines) if anchor in line]
        if not hits: raise ValueError((path,anchor))
        refs.append({'needle':anchor,'lines':hits})
    return {'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),
            'anchors':refs,'classification':classification,'consumption':consumption,'precise_residue':residue}

entries=[
 record(K/'PoincareGroup.lean',['structure PoincareGroup','theorem poincare_faithful'],
  'EXISTE_LIGADO','Grupo e ação afim usados em PoincareWitness; no fecho de imports QGSolutionComplete.',
  'Não identifica essa ação com a representação fotônica canônica em H1.'),
 record(K/'PoincareWitness.lean',['def thePoincareWitness','theorem proper_sector_fibers_blind'],
  'EXISTE_LIGADO','Habitante FullWitnessData; covariância e sensibilidade à paridade.',
  'O setor próprio age trivialmente nas fibras deste habitante, como teorema.'),
 record(K/'WedgeNet.lean',['def wedgeNet','def theSpecificAQFTWitness','Hilbert (U ≡ 1)'],
  'EXISTE_LIGADO','Rede concreta não abeliana, vácuo cíclico/separante; fecho QG.',
  'Translações triviais nesta realização; não identificar com lightNet.'),
 record(K/'WedgeNetFiniteDiamond.lean',['theorem finite_diamond_has_scalar_algebra'],
  'EXISTE_NAO_LIGADO_A_REDE_FOTONICA','Controle de alcance da rede WedgeNet.',
  'Diamantes limitados têm álgebra escalar nesta rede específica.'),
 record(K/'V350L2CharacterMultiplier.lean',['theorem characterMultiplier_weyl'],
  'EXISTE_LIGADO','Weyl entre multiplicador de caracteres e translação no Hilbert regular.',
  'Não é por identidade de nome a família W(f) do Fock canônico.'),
 record(K/'TheImportedSecondQuantization.lean',['structure FockCertificate','def lightNet','theorem light_kms','def lightH3','theorem qg_formalized_by_citation'],
  'EXISTE_LIGADO_CONDICIONAL_KNOWN','Weyl/localidade, Tomita/KMS e core estão tipados como campos citados; consumidores existentes.',
  'Realização simultânea dos campos ainda importados sobre o mesmo Fock; não alegar teoremas ausentes.'),
 record(K/'MaxwellLiteratureBridge.lean',['structure MaxwellQuadraticForm','def toStress','def toCertificate'],
  'EXISTE_LIGADO','Extensão por zero paga a passagem de forma no domínio a tensor total; consumida pela v375/v376.',
  'Forma Q e hipóteses charge_link/nontrivial da realização específica continuam explícitas.'),
 record(K/'TheWholeIsOne.lean',['(Q : TGLExt.MaxwellBridge.MaxwellQuadraticForm C)'],
  'EXISTE_LIGADO','Consumo formal da ponte Maxwell no teorema da v376.',
  'As hipóteses do mesmo par físico não desaparecem pelo consumo.'),
 record(K/'O16/MaxwellPolynomial_v2.lean',['theorem maxwell_symmetric','theorem maxwell_null_flux_nonnegative'],
  'EXISTE_NAO_LIGADO_A_EXPECTATIVA_WICK','Tensor clássico polinomial, cinco identidades já construídas na ORDEM016.',
  'Não identifica expectativa de Wick no domínio do Fock.'),
 record(NET/'light_ray/ConcreteLightRayNet.lean',['def halfline','theorem halfline_antitone','theorem no_four_dimensional_promotion'],
  'EXISTE_NAO_LIGADO_A_CERTIFICADO_GLOBAL','Rede de semirretas concretas padrão e não nulas, usando O16.',
  'Hilbert escalar da reta não é automaticamente H1 orbital nem rede4D.'),
 record(NET/'modular_wedge/CanonicalOutput.lean',['def spectralOutput','theorem spectralOutput_nonzero','theorem delta_is_SdagS'],
  'EXISTE_NAO_LIGADO_A_CERTIFICADO_GLOBAL','Habitante concreto do contrato D1a3 no H1 canônico.',
  'Glue da rede global ao KWR concreto deve ser fornecido explicitamente.'),
 record(NET/'fock_construction/BosonicFock.lean',['abbrev F :=','def gamma','def oneParticle','theorem infinite_dimensional'],
  'EXISTE_NAO_LIGADO_A_CERTIFICADO_COMPLETO','Fock concreto, vácuo, Γ funtorial, inclusão H1; campos cinemáticos pagos.',
  'Fiação desses campos ao FockCertificate é o alvo desta candidata.'),
 record(NET/'fock_construction/BosonicFockContinuity.lean',['theorem gamma_strong','theorem boosts_strong'],
  'EXISTE_NAO_LIGADO_A_CERTIFICADO_COMPLETO','Continuidade forte para parâmetros gerais, inclusive ℝ e ℝ4.',
  'Não reintroduzir continuidade como campo importado.'),
 record(NET/'CONSTRUCAO_CONTINUA_R1.md',['Defina K(gW_R)=U(g)K(W_R).','defina A(O)={W(f):f∈K(O)}'],
  'KNOWN_DERIVED_DOCUMENTAL','Construção analítica por Wigner/BGL, com referências e revisão.',
  'Formalização integral e identificação de dispositivo constituem alvos diferentes.'),
 record(NET/'MATRIZ_CONTRATO_FOCK_R2.json',['OPEN_CONSTRUCTION_KNOWN_LITERATURE','Correspondentes concretos de campos'],
  'OPEN_CONSTRUCAO_ESPECIFICA_KNOWN_LITERATURA','Matriz dos campos pagos versus importados.',
  'Residuo apenas no mesmo Fock; não é ausência da teoria conhecida.'),
 record(NET/'orchestration_r3/HANDOFF_SUBMITTED_R3_20261014.json',['fock_exponential_vectors_totality_r3','fock_antiunitary_second_quantization_r3'],
  'MISSOES_EXISTENTES_NAO_DUPLICAR','MiMo: exponenciais/totalidade; DeepSeek: Γ(J). IDs preservados.',
  'Este trabalho não constrói esses alvos nem despacha novamente.'),
]
inventory={'unit':'F1.FECHO_20261015','claim':845,'author':'codex-gerente-tgl / subagent atrator_lean',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'method':'Leitura das fontes + inventário da bancada + Nós Vivo + rotas; presença no fecho de imports não equivale a consumo na prova.',
 'consulted_indices':[r'C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.md',r'C:\IALD\MAPA_DE_ROTAS\MAPA_DE_ROTAS.json',r'C:\IALD\NOS_VIVO\nos_vivo.sqlite3'],
 'sources':entries,'production_modified':False,'external_calls':False}
save('INVENTARIO_REAPROVEITAMENTO_R1.json',json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
rows=['# Rede: inventário de reaproveitamento R1','',
 '[REAL — leitura de fontes; não é nova auditoria Lean]. Unidade F1.FECHO_20261015, reivindicação845. Nenhum original alterado.',
 'O nome da classe sempre se refere ao consumidor descrito; importação transitiva não prova identificação entre realizações.','']
for e in entries:
 rows += [f"## {Path(e['path']).name}",f"- Classe: {e['classification']}",f"- Fonte: `{e['path']}`; SHA256 `{e['sha256']}`.",
          '- Âncoras: '+ '; '.join(f"{a['needle']} — linhas {a['lines']}" for a in e['anchors']),
          '- Consumo: '+e['consumption'],'- Resíduo: '+e['precise_residue'],'']
save('INVENTARIO_REAPROVEITAMENTO_R1.md','\n'.join(rows))

raw=(K/'TheImportedSecondQuantization.lean').read_text(encoding='utf-8')
rest=raw[raw.index('  /-- a condição espectral é preservada'):raw.index('\nattribute [instance] FockCertificate.instN')].rstrip()
rest=rest[:rest.rfind('  equal_halves')]+rest[rest.rfind('  equal_halves'):].splitlines()[0]+'\n'
# Replace only the existing concrete kinematic objects in the remaining fields.
rest=re.sub(r'(?<![\w])Γ(?![\w])','F1Rede.BosonicFock.gamma',rest)
rest=re.sub(r'(?<![\w])Ω(?![\w])','F1Rede.BosonicFock.vacuum',rest)
fields=re.findall(r'^  ([\w]+)\s*:',rest,re.M)
instance_fields=re.findall(r'^  \[([\w]+)\s*:',rest,re.M)
source='''import BosonicFockContinuity
import BosonicFockGroupActions
import CanonicalOutput
import ConcreteLightRayNet
import TGLExt.QGSolutionComplete
import TGLExt.MaxwellLiteratureBridge

/-!+Concrete wiring, not a claim that the remaining imported fields are inhabited.
The canonical H1, standard wedge and bosonic Fock are reused without rebuilding.
Only genuinely remaining Fock fields are inputs. The scalar light-ray net is
retained as a separately typed construction; no scalar-to-4D identification is
claimed. Gamma(J) and exponential-vector totality belong to preexisting jobs.
No new axiom, no physical H3 derivation, no global solution or device equivalence.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.NetworkReuse
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open TGLExt.ContratoQGv32 TGLExt.ImportedSQ TGLExt.QGSolution
open F1Rede.BosonicFock

structure CanonicalNetInput extends LightNetData where
  wedge_glue : toLightNetData.K rightWedge =
    F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule.toSubmodule

def CanonicalNetInput.toStandardWedge (D : CanonicalNetInput) :
    AuditF13v31.LightNetStandardWedgeDataBGL where
  toLightNetData := D.toLightNetData
  out := F1Rede.CanonicalWedge.spectralOutput
  wedge_glue := D.wedge_glue

theorem canonical_wedge_nonzero (D : CanonicalNetInput) :
    ∃ f : H1, f ∈ D.K rightWedge ∧ f ≠ 0 := by
  obtain ⟨f,hf,hn⟩ := F1Rede.CanonicalWedge.spectralOutput_nonzero
  refine ⟨f,?_,hn⟩
  rw [D.wedge_glue]
  exact hf

theorem zero_wedge_refused (D : CanonicalNetInput) : D.K rightWedge ≠ ⊥ := by
  intro h
  obtain ⟨f,hf,hn⟩ := canonical_wedge_nonzero D
  rw [h] at hf
  exact hn hf

def canonicalWedgeInFock : Submodule ℝ F :=
  F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule.toSubmodule.map
    (oneParticle.toLinearMap.restrictScalars ℝ)

theorem canonicalWedgeInFock_nonzero :
    ∃ f : F, f ∈ canonicalWedgeInFock ∧ f ≠ 0 := by
  obtain ⟨x,hx,hn⟩ := F1Rede.CanonicalWedge.spectralOutput_nonzero
  refine ⟨oneParticle x,⟨x,hx,rfl⟩,?_⟩
  intro hz
  apply hn
  apply oneParticle.injective
  simpa using hz

theorem concrete_kinematics_inhabited :
    ‖vacuum‖ = 1 ∧ ¬ FiniteDimensional ℂ F :=
  ⟨vacuum_norm,infinite_dimensional⟩

theorem scalar_halfline_still_nonzero (a : ℝ) :
    (F1Rede.LightRay.halfline a).toClosedSubmodule ≠ ⊥ :=
  F1Rede.LightRay.halfline_ne_bot a

/-- All fields below remain named inputs on the already constructed Fock.
This record has no asserted inhabitant. Kinematic fields are deliberately absent. -/
structure RemainingFockInput (L : LightOneParticle) where
'''.replace('/-!+','/-!\n')+rest+'\n'
source+='attribute [instance] '+ ' '.join('RemainingFockInput.'+n for n in instance_fields)+'\n\n'
source+='''def RemainingFockInput.toCertificate {L : LightOneParticle}
    (A : RemainingFockInput L) : FockCertificate L where
  F := F
  instN := inferInstance
  instI := inferInstance
  instC := inferInstance
  Ω := vacuum
  Ω_norm := vacuum_norm
  F_infinite := infinite_dimensional
  Γ := gamma
  Γ_refl := gamma_refl
  Γ_trans := gamma_trans
  Γ_vac := gamma_vacuum
  ι := oneParticle
  Γ_one_particle := gamma_oneParticle
  Γ_strong := gamma_strong_real
  Γ_strong4 := gamma_strong_spacetime
'''
source+=''.join(f'  {n} := A.{n}\n' for n in fields+instance_fields)
source+='''
theorem assembled_F_is_concrete {L : LightOneParticle} (A : RemainingFockInput L) :
    A.toCertificate.F = F := rfl
theorem assembled_gamma_is_concrete {L : LightOneParticle} (A : RemainingFockInput L) :
    A.toCertificate.Γ = gamma := rfl
theorem assembled_inclusion_is_concrete {L : LightOneParticle} (A : RemainingFockInput L) :
    A.toCertificate.ι = oneParticle := rfl
theorem assembled_boost_is_concrete {L : LightOneParticle} (A : RemainingFockInput L)
    (s : ℝ) (f : F) : (lightBoost A.toCertificate).V s f = gamma (B0 s) f := rfl
theorem assembled_modular_parameter {L : LightOneParticle} (A : RemainingFockInput L)
    (t : ℝ) : lightDelta A.toCertificate t = gamma (B0 (-(2*Real.pi*t))) := rfl

/-- Existing H2/H3 consumer instantiated on this concrete kinematic Fock.
Maxwell and the remaining analytic fields stay explicit hypotheses. -/
theorem canonical_contract_from_named_imports (D : CanonicalNetInput)
    (A : RemainingFockInput D.toLightNetData.toLightOneParticle)
    (M : MaxwellCertificate A.toCertificate) (N : KillingNormalization)
    (G : ℝ) (hG : 0 < G) :
    ∃ h2 : ContratoH2v32 (lightNet A.toCertificate) (lightRealization A.toCertificate) N,
      Nonempty (ContratoImportH3v32 (lightNet A.toCertificate) (lightRealization A.toCertificate)
        N (lightBoost A.toCertificate) M.T h2) :=
  qg_contract_from_the_cited_net D.toLightNetData A.toCertificate M N G hG

end F1Fecho.NetworkReuse

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if `F1Fecho.NetworkReuse.isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\\t" ++ n.toString ++ "\\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
'''
source=source.replace('`F1Fecho.NetworkReuse.isPrefixOf n','(`F1Fecho.NetworkReuse).isPrefixOf n')
save('CanonicalFockAssemblyR1.lean',source)
save('SCOPE_R1.json',json.dumps({'kinematic_fields_consumed':['F','Ω','Ω_norm','F_infinite','Γ','Γ_refl','Γ_trans','Γ_vac','ι','Γ_one_particle','Γ_strong','Γ_strong4'],
 'remaining_fields':fields+instance_fields,'concrete_global_net_claimed':False,'remaining_input_inhabitant_claimed':False,
 'overlap_avoided':['MiMo exponential vectors/totality','DeepSeek antiunitary Gamma(J)'],
 'new_wiring':'Concrete canonical standard wedge embedded in the one-particle sector of the concrete bosonic Fock; conditional assembly into the existing certificate and H2/H3 consumer.',
 'light_ray_scope':'Separate scalar StandardSubspace net retained; no unjustified identification with orbital H1.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'inventory_sources':len(entries),'remaining_fields':len(fields)+len(instance_fields),'source':str(BASE/'CanonicalFockAssemblyR1.lean')},ensure_ascii=False))
