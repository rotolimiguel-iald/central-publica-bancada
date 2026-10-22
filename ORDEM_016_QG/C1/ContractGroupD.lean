import ContractGroupC

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

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace ComplexConjugate

noncomputable section

/-! ## §C'' — os certificados de sinal do CÉTICO 2 (CeticoKappaGauge.lean §2, 333a662a8fde1b51), transpostos -/

theorem translate_null_subset (l : ℝ) (hl : 0 ≤ l) :
    TGL.SpecificAQFT.translate (l • nullDir) rightWedge ⊆ rightWedge := by
  rintro _ ⟨x, hx, rfl⟩
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1, h2⟩ := abs_lt.mp hx'
  show |(x + l • nullDir) 0| < (x + l • nullDir) 1
  simp only [Pi.add_apply, Pi.smul_apply, nullDir, smul_eq_mul, Matrix.cons_val_zero,
    Matrix.cons_val_one, mul_one]
  rw [abs_lt]
  constructor <;> linarith

/-- [DERIVED] ★ (a) A INCLUSÃO SEMILATERAL, da covariância e da isotonia do kernel. -/
theorem halfsided_inclusion (W : TGLSpecificAQFTWitness) (l : ℝ) (hl : 0 ≤ l)
    (T : W.H →L[ℂ] W.H) (hT : T ∈ W.net rightWedge) :
    W.U (l • nullDir) * T * W.U (-(l • nullDir)) ∈ W.net rightWedge := by
  have h := (W.covariance (l • nullDir) rightWedge T).mp hT
  exact W.isotony _ _ (translate_null_subset l hl) h

/-- [DERIVED] ★ (b) A FORMA DE BORCHERS no contrato: Δ^{it} U(λn) Δ^{−it} = U(e^{−2πt}·λ·n). -/
theorem ContratoH2.contract_borchers_form {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} (C : ContratoH2 W R N) (t l : ℝ) :
    (C.Δit t).conjStarAlgEquiv (W.U (l • nullDir))
      = W.U ((Real.exp (-(2 * Real.pi * t)) * l) • nullDir) := by
  rw [C.poincare_relation, wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul, mul_comm l]

/-- [DERIVED] (c) a orientação de `PositiveEnergy`: z ↦ e^{izλ} (λ ≥ 0) é limitada no semiplano superior. -/
theorem positiveEnergy_orientation (lam : ℝ) (hlam : 0 ≤ lam) (z : ℂ) (hz : 0 ≤ z.im) :
    ‖Complex.exp (I * z * lam)‖ ≤ 1 := by
  rw [Complex.norm_exp]
  have : (I * z * (lam : ℂ)).re = -(z.im * lam) := by
    simp [Complex.mul_re, Complex.mul_im]
  rw [this, Real.exp_le_one_iff]
  have := mul_nonneg hz hlam
  linarith

/-! ## §D — ★★ κ: Unruh como RELAÇÃO KMS; κ fixo DADO N; (W,R) não fixa κ -/

/-- [DERIVED] REESCALA DO KMS: α KMS a β ⟹ τ ↦ α(cτ) KMS a β/c. -/
theorem KMSAt.rescale {W : TGLSpecificAQFTWitness} {α : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {β : ℝ}
    (h : KMSAt W α β) {c : ℝ} (hc : 0 < c) :
    KMSAt W (fun τ => α (c * τ)) (β / c) := by
  intro A hA B hB
  obtain ⟨F, hF, ⟨M, hM⟩, h1, h2⟩ := h A hA B hB
  have him : ∀ w : ℂ, ((c : ℂ) * w).im = c * w.im := by
    intro w; simp [Complex.mul_im]
  refine ⟨fun w => F ((c : ℂ) * w), ?_, ⟨M, ?_⟩, ?_, ?_⟩
  · have hg : DiffContOnCl ℂ (fun w : ℂ => (c : ℂ) * w) (kmsStrip (β / c)) :=
      (differentiable_id.const_mul _).diffContOnCl
    refine hF.comp hg ?_
    intro w hw
    simp only [kmsStrip, Set.mem_setOf_eq] at hw ⊢
    rw [him]
    refine ⟨mul_pos hc hw.1, ?_⟩
    calc c * w.im < c * (β / c) := mul_lt_mul_of_pos_left hw.2 hc
      _ = β := by field_simp
  · intro z hz0 hzβ
    apply hM
    · rw [him]; exact mul_nonneg hc.le hz0
    · rw [him]
      calc c * z.im ≤ c * (β / c) := mul_le_mul_of_nonneg_left hzβ hc.le
        _ = β := by field_simp
  · intro t
    have := h1 (c * t)
    simp only
    rw [← this]
    push_cast
    rfl
  · intro t
    have := h2 (c * t)
    have hc0 : (c : ℂ) ≠ 0 := by exact_mod_cast hc.ne'
    have harg : (c : ℂ) * ((t : ℂ) + ((β / c : ℝ) : ℂ) * I) = ((c * t : ℝ) : ℂ) + (β : ℂ) * I := by
      push_cast
      rw [mul_add, div_mul_eq_mul_div, mul_div_assoc', mul_div_cancel_left₀ _ hc0]
    simp only
    rw [harg, this]
    congr 3
    ring


end
end TGLExt.ContratoQGv31
