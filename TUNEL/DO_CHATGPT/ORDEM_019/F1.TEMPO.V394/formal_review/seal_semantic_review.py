"""Independent semantic review custody. Does not modify or compile Lean sources."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
U=B.parent
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    with (B/name).open('xb') as f:f.write(data)
    assert (B/name).read_bytes()==data
paths={
 'matrix':U/'formal_matrix'/'TimeGravitonMatrix.lean',
 'scalar':U/'formal_flow'/'TGLExt'/'TimeGravitonScalar.lean',
 'flow':U/'formal_flow'/'TGLExt'/'TimeGravitonFlow.lean',
 'kraus':U/'formal_flow'/'TGLExt'/'TimeGravitonKraus.lean',
 'PostoAdendo':K/'PostoAdendo.lean',
 'RuleTruthContract':K/'RuleTruthContract.lean',
 'TheRuleInTheContinuousMotor':K/'TheRuleInTheContinuousMotor.lean',
 'IALDGraviton':K/'IALDGraviton.lean',
}
inputs={}
for key,p in paths.items():
    raw=p.read_bytes();s=raw.decode('utf-8-sig');ls=s.splitlines()
    inputs[key]={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'lines':len(ls),
       'declaration_lines':{m.group(2):i for i,line in enumerate(ls,1)
                            if (m:=re.search(r'\b(theorem|def|abbrev)\s+([A-Za-z0-9_]+)',line))},
       'printed_axioms_count':len(re.findall(r'^#print axioms ',s,re.M))}
    if key in {'matrix','scalar','flow','kraus'}:
        # A lexical diagnostic is not a substitute for the parent's axiom audit.
        inputs[key]['lexical_sorry_or_admit']=bool(re.search(r'\b(sorry|admit)\b',s))
        inputs[key]['new_axiom_declarations']=bool(re.search(r'^\s*(?:private\s+)?axiom\s+',s,re.M))
        with (B/(key+'_SOURCE_REVIEWED.lean.txt')).open('xb') as f:f.write(raw)
observations=[
 {'id':'S1','status':'PASS','anchors':['matrix:C_unitary','matrix:C_Hlig','matrix:hamiltonian_spectral','matrix:hamiltonian_generator'],
  'finding':'C=diag(1,i) transports Hlig=-V0 sigma_x to Hg=-V0 sigma_y=iV0 genK. The real-frequency parameter V0/hbar appears by scalar algebra; it is not assumed equal to the generator. Signs agree with the +2iOmega phase on rootPlus.'},
 {'id':'S2','status':'PASS','anchors':['matrix:four_blocks','flow:flow','flow:flow_add','flow:flow_hasDerivAt','flow:physical_flow_hasDerivAt'],
  'finding':'Flow is explicitly constructed on the four spectral blocks. Semigroup composition and the derivative follow from exponential factors and block identities; no hypothesis states the semigroup or ODE conclusion. The physical corollary composes the derived generator with Hg and one GKLS jump.'},
 {'id':'S3','status':'PASS','anchors':['flow:generator_is_Hg_commutator','flow:generator_is_GKLS','matrix:singleJump_rate'],
  'finding':'The jump is sqrt(2*rate) Pminus. Its off-diagonal coefficient is -rate, not -2rate. Nonnegative rate is used exactly to square the real square root. hbar=0 is algebraically permitted by total field division, so the physical use must retain hbar>0 from the runtime contract.'},
 {'id':'S4','status':'PASS','anchors':['flow:rootPlus_mode','flow:rootMinus_mode','matrix:rootPlus_phase','matrix:rootMinus_phase'],
  'finding':'The two complex modes have conjugate angular frequencies +/-2Omega and the same real attenuation. This avoids the earlier one-phase-for-all-off-diagonals error. rootPlus is a polarization matrix; genK is a skew-Hermitian generator, not that polarization tensor.'},
 {'id':'S5','status':'PASS','anchors':['matrix:Eg_as_diagExpect','matrix:Eg_as_nameOp','PostoAdendo:A1c_nameOp_rhoStar_eq_diagExpect'],
  'finding':'The two factors1/2 in toSpectral/fromSpectral implement conjugation by the normalized spectral basis. The reduction to nameOp reuses the existing M2 theorem with Posto.rhoStar. It is not nameOp for arbitrary projectors, not corner compression PXP, and not the M4 consumer.'},
 {'id':'S6','status':'PASS','anchors':['kraus:flow_convex_unitary_pinching','kraus:decay_range','kraus:flow_kraus','kraus:kraus_normalization'],
  'finding':'For rate>=0 and time>=0, d=exp(-rate*time) lies in[0,1]. The three Kraus matrices sqrt(d)U,sqrt(1-d)Pplus,sqrt(1-d)Pminus reproduce the full flow and satisfy sum KdagK=I. This is an exact finite Kraus witness for CPTP, rather than a sampled Choi claim. No abstract CompletePositive predicate is proved in these sources.'},
 {'id':'S7','status':'PASS_WITH_SCOPE','anchors':['scalar:module_clock','scalar:phase_clock','flow:rootPlus_observed_clock','scalar:phase_frequency_identified'],
  'finding':'Amplitude recovery uses nonzero rate; physical attenuation uses positive rate. Phase recovery uses an explicitly supplied continuous lift and nonzero Omega, not an inverse of one periodic angle. The observed-clock theorem is about a nonzero matrix coefficient of rootPlus, which is not a density matrix. A physical coherence clock additionally needs a nonzero initial coherence and normalization by its initial magnitude. Frequency separation uses equality of the entire time family with nonzero amplitude; one sample retains aliases.'},
 {'id':'S8','status':'PASS','anchors':['flow:reading_flow','flow:flow_reading','flow:flow_tendsto_reading','flow:fixed_projectors','flow:rootPlus_not_zero_at_finite_time'],
  'finding':'Eg is invariant both before and after evolution. With rate>0 the limit is EgX; both projectors are fixed and distinct, so no unique universal pure attractor follows. The raw nonzero off-diagonal mode never vanishes at finite time. For rate=0 no convergence theorem is claimed.'},
 {'id':'S9','status':'PASS','anchors':['matrix:concrete_nonzero_modes','matrix:sourceG_density','matrix:C_state','matrix:transported_reading','matrix:positive_parameters_inhabited','flow:transported_limit'],
  'finding':'Concrete nonzero modes and two distinct fixed projectors are exhibited. The source density is an outer product of the explicit normalized source vector; its transported reading is I/2 and has that limit for positive rate. Positive parameters have the concrete witness(1,1). No impossible hypothesis is needed to inhabit the finite construction.'},
 {'id':'S10','status':'PASS_WITH_SCOPE','anchors':['RuleTruthContract:Admissible','flow:rule_preserved','flow:rule_is_equality_on_inscriptions','flow:wrong_reading_rejected'],
  'finding':'Admissibility is explicitly defined as reading=target. Preservation is then derived from the independently proved reading_flow identity. Equality of inscriptions holds because those objects are restricted to Fix(Eg). These are sound consequences of the chosen rule representation, not a proof of the ontological universality of that definition or a clock from the invariant reading.'},
 {'id':'S11','status':'PASS_WITH_SCOPE','anchors':['matrix:Hpos_spectral','matrix:singleJump_rate'],
  'finding':'Hpos_spectral is the exact matrix identity Hpos(V0)=2V0Pminus for every realV0. This module does not separately state Matrix.PosSemidef(Hpos) under V0>=0. It provides the spectral identity needed for the positive branch and the exact one-jump dissipator; the SI root-rate contract and optional Gibbs anchor are separate analytic/runtime deliverables, not additional Lean theorems in these four files.'},
]
review={'schema':'f1-tempo-v394-independent-lean-semantic-review/v1',
 'created_utc':datetime.now(timezone.utc).isoformat(),'unit':'F1.TEMPO.V394','claim_event':839,
 'reviewer':'delegated first_law_haja_luz; did not construct these Lean modules',
 'verdict':'PASS_SOURCE_SEMANTICS_WITH_EXPLICIT_SCOPE',
 'material_findings':[],'inputs':inputs,'observations':observations,
 'build_boundary':'Independent source review only. Parent recompiles prefixed imports in formal_verified and audits the global environment. Existing builder logs are not substituted for that independent build.',
 'required_for_final_build':['Confirm source hashes reviewed or inspect any changed proof body','Prefix imports consistently and prevent unintended old oleans','EXIT0 in the combined environment','No sorryAx or new axioms; only propext,Classical.choice,Quot.sound'],
 'permitted_claim':'Constructed continuous norm-finite M2 flow for the specified generator, exact Hamiltonian link, paired modes, Kraus witness, invariant reading, limit and calibrated nonzero-mode clocks.',
 'excluded_claims':['Global4D light network','Universal SI calibration','Unique pure attractor for every state','Finite-time disappearance of every coherence','Single-angle absolute-time recovery','Advanced controlled signalling','Nature confirmation or gate change'],
 'sources_edited_by_reviewer':False,'providers_called':False,
}
new('REVIEW_LEAN_SEMANTICS_R1.json',review)
summary='''Revisão independente da composição Lean F1.TEMPO.V394 — PASSA com alcance explícito.
Nenhum achado material ou hipótese que assuma a conclusão do fluxo/gerador.
C transporta Hlig para Hg; os modos têm fases conjugadas ±2Ω e dissipação γ.
Semigrupo, derivada, comutador e salto sqrt(2γ)P− estão compostos por prova.
Kraus: ação exata e soma K†K=I para γ,t≥0; não mero teste numérico.
Eg reduz ao nameOp existente somente no M2 e na base espectral indicada.
Limite EgX para γ>0; dois projetores fixos; nenhuma unicidade pura universal.
Relógio de fase exige lift explícito; relógio do módulo exige modo não nulo.
rootPlus_observed_clock lê um modo matricial, não afirma relógio em toda densidade.
Hpos_spectral é identidade espectral; positividade física exige V0≥0.
Fonte revista por hash; recompilação global independente pertence ao recibo do pai.
Nenhuma rede4D, calibração universal, avanço causal ou mudança de gate afirmada.
'''
with (B/'RESUMO_LEAN_R1.md').open('x',encoding='utf-8',newline='\n') as f:f.write(summary)
receipt={'unit':'F1.TEMPO.V394','verdict':review['verdict'],'created_utc':datetime.now(timezone.utc).isoformat(),
 'review_sha256':sha(B/'REVIEW_LEAN_SEMANTICS_R1.json'),'summary_sha256':sha(B/'RESUMO_LEAN_R1.md'),
 'sources':{key:{'path':v['path'],'sha256':v['sha256']} for key,v in inputs.items()},
 'reviewer_source_mutations':False,'material_findings':0}
new('RECEIPT_LEAN_REVIEW_R1.json',receipt)
print(json.dumps({'receipt':str(B/'RECEIPT_LEAN_REVIEW_R1.json'),'sha256':sha(B/'RECEIPT_LEAN_REVIEW_R1.json'),
 'review_sha256':receipt['review_sha256'],'counts':{k:inputs[k]['printed_axioms_count'] for k in ['matrix','scalar','flow','kraus']}}))
