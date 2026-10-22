import ContractGroupD

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

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem modular_is_boost_at_two_pi (C : ContratoH2 W R N) :
    (fun t => C.Δit (-t)) = (fun t => C.boost.V (2 * Real.pi * t)) := by
  funext t
  rw [C.bw]
  ring_nf

/-- [DERIVED] ★ UNRUH COMO RELAÇÃO KMS: o fluxo de Killing τ ↦ V(κτ) é KMS a β = 2π/κ. ⚠ (rodada 2) isto fixa
    o PRODUTO β_Killing·κ = 2π — NÃO o valor de κ (cético 1, `kms_product_is_two_pi`). -/
theorem unruh_is_kms (C : ContratoH2 W R N) :
    KMSAt W C.killingFlow (2 * Real.pi / C.kappa) := by
  have h1 : KMSAt W (fun t => C.boost.V (2 * Real.pi * t)) 1 := by
    have := C.kms
    rwa [modular_is_boost_at_two_pi] at this
  have hc : 0 < C.kappa / (2 * Real.pi) := div_pos C.kappa_pos (by positivity)
  have h2 := KMSAt.rescale h1 hc
  have hfun : (fun τ => (fun t => C.boost.V (2 * Real.pi * t)) (C.kappa / (2 * Real.pi) * τ))
      = C.killingFlow := by
    funext τ
    unfold ContratoH2.killingFlow
    field_simp
  have hβ : (1 : ℝ) / (C.kappa / (2 * Real.pi)) = 2 * Real.pi / C.kappa := by
    field_simp
  rw [hfun, hβ] at h2
  exact h2

theorem unruh_is_kms_temperature (C : ContratoH2 W R N) :
    KMSAt W C.killingFlow (1 / C.unruhTemperature) := by
  have h := unruh_is_kms C
  have : (1 : ℝ) / C.unruhTemperature = 2 * Real.pi / C.kappa := by
    unfold ContratoH2.unruhTemperature
    have := C.kappa_pos.ne'
    field_simp
  rw [this]; exact h

/-- [DERIVED] a relação que o tipo fixa: β_Killing·κ = 2π (a do cético 1). -/
theorem kms_product_is_two_pi (C : ContratoH2 W R N) :
    (2 * Real.pi / C.kappa) * C.kappa = 2 * Real.pi := by
  have := C.kappa_pos.ne'
  field_simp

/-- o raio de Rindler do relógio de N. -/
def refRadius (N : KillingNormalization) : ℝ := Real.sqrt (N.point 1 ^ 2 - N.point 0 ^ 2)

theorem refRadius_pos (N : KillingNormalization) : 0 < refRadius N := by
  have hx : |N.point 0| < N.point 1 := N.point_in_wedge
  obtain ⟨h1, h2⟩ := abs_lt.mp hx
  unfold refRadius
  apply Real.sqrt_pos.mpr
  nlinarith

/-- [DERIVED] κ·ρ(N) = 1. -/
theorem kappa_mul_radius (C : ContratoH2 W R N) : C.kappa * refRadius N = 1 := by
  have h := C.observer_unit
  simp [minkowskiSq, killingField] at h
  have hk : C.kappa ^ 2 * (N.point 1 ^ 2 - N.point 0 ^ 2) = 1 := by
    linear_combination h
  unfold refRadius
  rw [← Real.sqrt_sq C.kappa_pos.le, ← Real.sqrt_mul (sq_nonneg _), hk, Real.sqrt_one]

/-- [DERIVED] ★ κ = 1/ρ(N): o VALOR de κ é o do relógio externo. -/
theorem kappa_eq_inv_radius (C : ContratoH2 W R N) : C.kappa = 1 / refRadius N := by
  have h := kappa_mul_radius C
  have hne := (refRadius_pos N).ne'
  field_simp
  linarith [h]

/-- [DERIVED] ★★ κ FIXO DADO N: dois habitantes de `ContratoH2 W R N` têm o MESMO κ (o `rekappa` do cético 1 e
    o `regauge` do cético 2 NÃO habitam o mesmo tipo indexado). -/
theorem kappa_fixed (C C' : ContratoH2 W R N) : C.kappa = C'.kappa := by
  rw [kappa_eq_inv_radius C, kappa_eq_inv_radius C']

theorem no_rekappa (C : ContratoH2 W R N) {κ' : ℝ} (h : κ' ≠ C.kappa) :
    ¬ ∃ C' : ContratoH2 W R N, C'.kappa = κ' :=
  fun ⟨C', hC'⟩ => h (hC' ▸ kappa_fixed C' C)

/-- a unidade do Killing no relógio de N' com κ' = 1/ρ(N'). -/
theorem observer_unit_of_index (N' : KillingNormalization) :
    minkowskiSq (killingField (1 / refRadius N') N'.point) = 1 := by
  have hr := refRadius_pos N'
  have hsq : refRadius N' ^ 2 = N'.point 1 ^ 2 - N'.point 0 ^ 2 := by
    unfold refRadius
    have hx : |N'.point 0| < N'.point 1 := N'.point_in_wedge
    obtain ⟨h1, h2⟩ := abs_lt.mp hx
    rw [Real.sq_sqrt (by nlinarith)]
  simp [minkowskiSq, killingField]
  field_simp
  linarith [hsq]

/-- ★ RE-INDEXAR: de um habitante sobre N, outro sobre QUALQUER N' (mesmo Δit, boost, frame, bloco (P)). -/
def reindex (C : ContratoH2 W R N) (N' : KillingNormalization) : ContratoH2 W R N' where
  kappa := 1 / refRadius N'
  kappa_pos := by have := refRadius_pos N'; positivity
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer_unit := observer_unit_of_index N'
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := by
    intro x hx
    obtain ⟨c, hc, h⟩ := C.fiducial_is_modular x hx
    have hk := C.kappa_pos
    have hr := refRadius_pos N'
    refine ⟨c * C.kappa * refRadius N', by positivity, ?_⟩
    rw [h]
    funext i
    simp only [killingField, Pi.smul_apply, smul_eq_mul]
    field_simp

/-- [DERIVED] ★★ HONESTO: o par (W, R) NÃO fixa κ — se há habitante sobre algum N, há sobre TODO N'. O valor
    de κ é o [INPUT] N; a v3.1 NÃO «fixa o parâmetro espectral» a partir do par. -/
theorem kappa_is_input (h : Nonempty (ContratoH2 W R N)) (N' : KillingNormalization) :
    Nonempty (ContratoH2 W R N') :=
  ⟨reindex h.some N'⟩

theorem killingFlow_add (C : ContratoH2 W R N) (τ σ : ℝ) :
    C.killingFlow (τ + σ) = (C.killingFlow σ).trans (C.killingFlow τ) := by
  unfold ContratoH2.killingFlow
  rw [mul_add, C.boost.V_add]

theorem killingFlow_zero (C : ContratoH2 W R N) :
    C.killingFlow 0 = LinearIsometryEquiv.refl ℂ W.H := by
  unfold ContratoH2.killingFlow
  rw [mul_zero, C.boost.V_zero]

/-! ## §F — as energias -/

theorem modularEnergy_of_boostEnergy (C : ContratoH2 W R N) {ψ : W.H} {b : ℝ}
    (h : HasBoostEnergy C.boost.V ψ b) : HasModularEnergy C.Δit ψ (2 * Real.pi * b) := by
  unfold HasBoostEnergy at h
  unfold HasModularEnergy
  have hg : HasDerivAt (fun t : ℝ => -(2 * Real.pi * t)) (-(2 * Real.pi)) 0 := by
    have h0 := (hasDerivAt_id (0:ℝ)).const_mul (-(2 * Real.pi))
    have e : (fun t : ℝ => -(2 * Real.pi * t)) = (fun y : ℝ => -(2 * Real.pi) * id y) := by
      funext t; simp [id]
    rw [e]
    exact h0.congr_deriv (by ring)
  have h' : HasDerivAt (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) (I * (b : ℂ)) (-(2 * Real.pi * 0)) := by
    simpa using h
  have hc := h'.scomp (0:ℝ) hg
  have hfun : (fun t : ℝ => ⟪ψ, C.Δit t ψ⟫_ℂ)
      = (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) ∘ (fun t : ℝ => -(2 * Real.pi * t)) := by
    funext t
    simp only [Function.comp, C.bw]
  rw [hfun]
  refine hc.congr_deriv ?_
  rw [Complex.real_smul]
  push_cast
  ring

theorem modularEnergy_unique {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {D : ℝ → (H ≃ₗᵢ[ℂ] H)} {ψ : H} {k k' : ℝ}
    (h : HasModularEnergy D ψ k) (h' : HasModularEnergy D ψ k') : k = k' := by
  have hu := h.unique h'
  have hI : I * (k : ℂ) = I * (k' : ℂ) := neg_inj.mp hu
  have : (k : ℂ) = k' := mul_left_cancel₀ Complex.I_ne_zero hI
  exact_mod_cast this

theorem vac_modularEnergy (C : ContratoH2 W R N) : HasModularEnergy C.Δit W.vac 0 := by
  unfold HasModularEnergy
  have : (fun t : ℝ => ⟪W.vac, C.Δit t W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext t; rw [Δit_vac]
  rw [this]
  simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)

theorem vac_boostEnergy (C : ContratoH2 W R N) : HasBoostEnergy C.boost.V W.vac 0 := by
  unfold HasBoostEnergy
  have : (fun s : ℝ => ⟪W.vac, C.boost.V s W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext s; rw [C.boost.V_vac]
  rw [this]
  simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)

theorem inner_vac_Δit (C : ContratoH2 W R N) (t : ℝ) (φ : W.H) :
    ⟪W.vac, C.Δit t φ⟫_ℂ = ⟪W.vac, φ⟫_ℂ := by
  have h := (C.Δit t).inner_map_map W.vac φ
  rw [Δit_vac] at h
  exact h

/-- [DERIVED] ★★ (cético 2, CeticoFirstLaw.lean 39e2508fdde98aef, transposto) a energia modular BILATERAL da
    perturbação Ω + εφ é ε²·k_φ: SEM termo de 1ª ordem. É por isso que o δS de H3 v3.1 NÃO é esta energia,
    e sim a carga UNILATERAL do corte nulo (`windowEntropy`). -/
theorem bilateral_no_first_order (C : ContratoH2 W R N) {φ : W.H} {k : ℝ}
    (hk : HasModularEnergy C.Δit φ k) (ε : ℝ) :
    HasModularEnergy C.Δit (W.vac + (ε : ℂ) • φ) (ε ^ 2 * k) := by
  unfold HasModularEnergy at hk ⊢
  have hfun : (fun t : ℝ => ⟪W.vac + (ε : ℂ) • φ, C.Δit t (W.vac + (ε : ℂ) • φ)⟫_ℂ)
      = fun t : ℝ => (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
          + ((ε : ℂ) ^ 2) * ⟪φ, C.Δit t φ⟫_ℂ := by
    funext t
    rw [map_add, map_smul, Δit_vac, inner_add_left, inner_add_right, inner_add_right,
      inner_smul_left, inner_smul_left, inner_smul_right, inner_smul_right, inner_vac_Δit]
    simp only [Complex.conj_ofReal]
    ring
  rw [hfun]
  have h2 := (hk.const_mul ((ε : ℂ) ^ 2)).const_add
    (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
  refine h2.congr_deriv ?_
  push_cast
  ring

end ContratoH2

end
end TGLExt.ContratoQGv31
