import ContractGroupI_v3

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CONTRATO v3.1 — OS TEOREMAS (leem os campos do tipo `ContratoQG_v31`)
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, RODADA 2, 23/09/2026; scratchpad; NÃO cunha nome reservado]

  §A  unitariedade das translações.
  §B  o que a v2 pedia como campo e a v3/v3.1 DERIVA (Δit fixa Ω; BW geométrico; Poincaré; não-trivial).
  §C  ★★★ COERÊNCIA ESPECTRAL: todo habitante tem Δ^{it} SEM autovetor fora de ℂΩ (oposto da v2).
  §C' ★ as paredes do cético 1 transpostas (T1–T4): U transversal, boost trivial, torre, momento nulo discreto.
  §C''★ os certificados de sinal do cético 2 transpostos: inclusão semilateral, forma de Borchers, orientação.
  §D  ★★ κ: Unruh como relação KMS (β_Killing·κ = 2π); κ = 1/ρ(N); κ FIXO dado N; (W,R) NÃO fixa κ.
  §E  o implementador é ÚNICO.
  §F  as energias: K = 2πB; ★ a energia BILATERAL não tem termo de 1ª ordem (cético 2, transposto).
  §G  o frame.
  §H  ★★★ H3 v3.1: a lei local ao longo do gerador; BH/Clausius/8πG como teoremas de JANELA (integração
      exata); a energia nula não se anula; a expansão não é constante; G NÃO é predito (Jacobson).
  §I  as paredes no par legado e contra translações que comutam com Δit.
  §J  o import indexado.
  β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt.ContratoQGv31

open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace ComplexConjugate

noncomputable section

/-! ## §I — as paredes -/

theorem contratoH2_empty_of_unfaithful (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization)
    (h : ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ W.U a = 1) : IsEmpty (ContratoH2 W R N) :=
  ⟨fun C => by
    obtain ⟨a, ha, hU⟩ := h
    exact ha (C.translations_faithful a hU)⟩

theorem contratoH2_empty_on_legacy (N : KillingNormalization) :
    IsEmpty (ContratoH2 theSpecificAQFTWitness regularModularRealization N) :=
  contratoH2_empty_of_unfaithful _ _ N ⟨nullDir, by
    intro h; have := congrFun h 0; simp [nullDir] at this, rfl⟩

theorem contratoH3_empty_on_legacy (N : KillingNormalization)
    (T : StressTensorData theSpecificAQFTWitness) :
    IsEmpty (ContratoH3 theSpecificAQFTWitness regularModularRealization N T) :=
  ⟨fun C => (contratoH2_empty_on_legacy N).false C.H2⟩

theorem ContratoH2.commuting_translations_excluded {W : TGLSpecificAQFTWitness}
    {R : TGLModularRealization W} {N : KillingNormalization} (C : ContratoH2 W R N) :
    ¬ ∀ (t : ℝ) (a : Fin 4 → ℝ), (C.Δit t).conjStarAlgEquiv (W.U a) = W.U a := by
  intro hcomm
  set m : Fin 4 → ℝ := (Real.exp (-(2 * Real.pi)) - 1) • nullDir with hm
  have hm0 : m ≠ 0 := by
    intro h0
    have h := congrFun h0 0
    have hlt : Real.exp (-(2 * Real.pi)) < 1 := by
      have := Real.exp_lt_exp.mpr (show -(2 * Real.pi) < 0 by
        have := Real.pi_pos; linarith)
      simpa using this
    simp [hm, nullDir] at h
    linarith
  apply hm0
  apply C.translations_faithful
  have hB := C.poincare_relation 1 nullDir
  rw [hcomm, wedgeBoostMap_nullDir, mul_one] at hB
  have hsplit : Real.exp (-(2 * Real.pi)) • nullDir = nullDir + m := by
    rw [hm, sub_smul, one_smul]; abel
  rw [hsplit, W.U_add] at hB
  have hinv : W.U (-nullDir) * W.U nullDir = 1 := by
    rw [← W.U_add, neg_add_cancel, W.U_zero]
  calc W.U m = (W.U (-nullDir) * W.U nullDir) * W.U m := by rw [hinv, one_mul]
    _ = W.U (-nullDir) * (W.U nullDir * W.U m) := by rw [mul_assoc]
    _ = W.U (-nullDir) * W.U nullDir := by rw [← hB]
    _ = 1 := hinv

/-- [DERIVED] ★ o sinal de BW é load-bearing: nenhum habitante satisfaz também Δ^{it} = V(+2πt). -/
theorem ContratoH2.bw_sign_matters {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} (C : ContratoH2 W R N) :
    ¬ ∀ t : ℝ, C.Δit t = C.boost.V (2 * Real.pi * t) := by
  intro hflip
  apply C.trivial_boost_excluded
  intro s
  have hpi : (4 * Real.pi) ≠ 0 := by positivity
  have h1 := hflip (s / (4 * Real.pi))
  rw [C.bw] at h1
  -- V(−s/2) = V(s/2) ⟹ V(s) = V(s/2 + s/2) = V(s/2)∘V(s/2) = V(s/2)∘V(−s/2) = 1
  have e1 : -(2 * Real.pi * (s / (4 * Real.pi))) = -(s / 2) := by field_simp; ring
  have e2 : 2 * Real.pi * (s / (4 * Real.pi)) = s / 2 := by field_simp; ring
  rw [e1, e2] at h1
  have hsum : C.boost.V s = (C.boost.V (s / 2)).trans (C.boost.V (s / 2)) := by
    rw [← C.boost.V_add]; congr 1; ring
  have hzero : (C.boost.V (-(s / 2))).trans (C.boost.V (s / 2)) = LinearIsometryEquiv.refl ℂ W.H := by
    rw [← C.boost.V_add, add_neg_cancel, C.boost.V_zero]
  rw [hsum]
  rw [← h1] at hzero ⊢
  exact hzero

/-! ## §J — o import indexado -/

theorem ContratoImportH3.nonvacuous {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} {T : StressTensorData W}
    {h2 : ContratoH2 W R N} (I : ContratoImportH3 W R N T h2) : Nonempty (ContratoH3 W R N T) :=
  ⟨I.produce h2⟩

theorem ContratoImportH3.same_horizon_data {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} {T : StressTensorData W}
    {h2 : ContratoH2 W R N} (I : ContratoImportH3 W R N T h2) :
    (I.produce h2).H2.kappa = h2.kappa ∧ (I.produce h2).H2.Δit = h2.Δit ∧
      (I.produce h2).H2.boost = h2.boost := by
  rw [I.same_horizon h2]
  exact ⟨rfl, rfl, rfl⟩

theorem no_import_on_legacy (N : KillingNormalization) (T : StressTensorData theSpecificAQFTWitness) :
    ¬ ∃ h2 : ContratoH2 theSpecificAQFTWitness regularModularRealization N,
        Nonempty (ContratoImportH3 theSpecificAQFTWitness regularModularRealization N T h2) :=
  fun ⟨h2, _⟩ => (contratoH2_empty_on_legacy N).false h2


end
end TGLExt.ContratoQGv31

#print axioms TGLExt.ContratoQGv31.contratoH2_empty_of_unfaithful
#print axioms TGLExt.ContratoQGv31.contratoH2_empty_on_legacy
#print axioms TGLExt.ContratoQGv31.contratoH3_empty_on_legacy
#print axioms TGLExt.ContratoQGv31.ContratoH2.commuting_translations_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH2.bw_sign_matters
#print axioms TGLExt.ContratoQGv31.ContratoImportH3.nonvacuous
#print axioms TGLExt.ContratoQGv31.ContratoImportH3.same_horizon_data
#print axioms TGLExt.ContratoQGv31.no_import_on_legacy
