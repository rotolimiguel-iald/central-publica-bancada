import ContratoQG_v3

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CONTRATO v3 — OS TEOREMAS (leem os campos do tipo `ContratoQG_v3`)
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, 23/09/2026; scratchpad; NÃO cunha nome reservado]

  §A  unitariedade das translações de uma testemunha qualquer (lida de U_add/U_star/U_zero).
  §B  o que a v2 pedia como campo e a v3 DERIVA: Δit fixa o vácuo; BW geométrico sobre a rede (B1);
      a relação de Poincaré (B3); translações não-triviais (B2).
  §C  ★★★ COERÊNCIA ESPECTRAL (item 7): todo habitante da v3 tem Δ^{it} SEM autovetores fora de ℂΩ —
      o OPOSTO exato de `W5Final.Espectral.contratoH2_forces_point_spectrum` (v2).
  §D  ★★ κ AMARRADO (item 3): o fluxo de Killing τ ↦ V(κτ) é KMS a β = 2π/κ (Unruh como TEOREMA);
      κ = 1/ρ do observador fiducial.
  §E  ★ o implementador é ÚNICO (lido de R e da ciclicidade do vácuo): Δit não é escolha.
  §F  as energias: K = 2πB (de BW), vácuo com energia modular 0, unicidade.
  §G  o frame (como na v2) e as exclusões de `theCurvedFrame`.
  §H  ★★ H3: Clausius DERIVADO; BH com G fixo; a razão δS:δA é universal (G não se ajusta por
      perturbação); o balanço não é vazio; κ cancela em δS; alimenta o teorema mestre.
  §I  as paredes no par legado (U = 1) e contra translações que comutam com Δit (o dente de W5).
  §J  o import indexado: não-vacuidade por tipo.
  β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt.ContratoQGv3

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace ComplexConjugate

noncomputable section

/-! ## §A — as translações de qualquer testemunha são unitárias -/

section Unitarity

variable (W : TGLSpecificAQFTWitness)

theorem U_neg_mul (a : Fin 4 → ℝ) : W.U (-a) * W.U a = 1 := by
  rw [← W.U_add, neg_add_cancel, W.U_zero]

theorem U_neg_apply (a : Fin 4 → ℝ) (x : W.H) : W.U (-a) (W.U a x) = x := by
  have h := congrArg (fun T : W.H →L[ℂ] W.H => T x) (U_neg_mul W a)
  exact h

theorem U_inner_adj (a : Fin 4 → ℝ) (x y : W.H) : ⟪W.U a x, y⟫_ℂ = ⟪x, W.U (-a) y⟫_ℂ := by
  rw [← W.U_star a, ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_right]

theorem U_norm (a : Fin 4 → ℝ) (x : W.H) : ‖W.U a x‖ = ‖x‖ := by
  have h : ⟪W.U a x, W.U a x⟫_ℂ = ⟪x, x⟫_ℂ := by
    rw [U_inner_adj, U_neg_apply]
  rw [inner_self_eq_norm_sq_to_K, inner_self_eq_norm_sq_to_K] at h
  have h2 : ‖W.U a x‖ ^ 2 = ‖x‖ ^ 2 := by exact_mod_cast h
  have := norm_nonneg (W.U a x)
  have := norm_nonneg x
  nlinarith [sq_nonneg (‖W.U a x‖ - ‖x‖), sq_nonneg (‖W.U a x‖ + ‖x‖)]

end Unitarity

/-! ## §B — o que a v2 pedia como CAMPO e a v3 DERIVA -/

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- [DERIVED] Δ^{it} fixa o vácuo (de `bw` + `V_vac`). -/
theorem Δit_vac (C : ContratoH2 W R) (t : ℝ) : C.Δit t W.vac = W.vac := by
  rw [C.bw]; exact C.boost.V_vac _

/-- [DERIVED] (B1 da v2, agora teorema) Ad(Δ^{it}) é GEOMÉTRICO na rede: net(O) ↦ net(Λ(−2πt)O). -/
theorem bw_covariance (C : ContratoH2 W R) (t : ℝ) (O : Set (Fin 4 → ℝ)) (T : W.H →L[ℂ] W.H)
    (hT : T ∈ W.net O) :
    (C.Δit t).conjStarAlgEquiv T ∈ W.net (wedgeBoostMap (-(2 * Real.pi * t)) '' O) := by
  rw [C.bw]; exact C.boost.V_net _ O T hT

/-- [DERIVED] (B3 da v2, agora teorema) Δ^{it} U(a) Δ^{−it} = U(Λ(−2πt)a). -/
theorem poincare_relation (C : ContratoH2 W R) (t : ℝ) (a : Fin 4 → ℝ) :
    (C.Δit t).conjStarAlgEquiv (W.U a) = W.U (wedgeBoostMap (-(2 * Real.pi * t)) a) := by
  rw [C.bw]; exact C.boost.V_translations _ a

/-- [DERIVED] (B2 da v2, agora teorema, pela fidelidade) as translações não são triviais. -/
theorem translates (C : ContratoH2 W R) : ∃ a : Fin 4 → ℝ, W.U a ≠ 1 := by
  refine ⟨nullDir, fun h => ?_⟩
  have h0 := congrFun (C.translations_faithful _ h) 0
  simp [nullDir] at h0

/-! ## §C — ★★★ COERÊNCIA ESPECTRAL: nenhum autovetor de Δ^{it} fora de ℂΩ -/

/-- [DERIVED] ★ a função de correlação nula g(λ) = ⟪ψ, U(λn)ψ⟫ de um autovetor de Δ^{it} é invariante por
    dilatação: g(λ·e^{−2πt}) = g(λ) (de BW + covariância do boost nas translações + |fase| = 1). -/
theorem eigen_null_correlation_dilation (C : ContratoH2 W R) {ψ : W.H} {r : ℝ}
    (hψ : ∀ t : ℝ, C.Δit t ψ = ChatgptAudit.modularPhase t r • ψ) (t l : ℝ) :
    ⟪ψ, W.U ((l * Real.exp (-(2 * Real.pi * t))) • nullDir) ψ⟫_ℂ
      = ⟪ψ, W.U (l • nullDir) ψ⟫_ℂ := by
  set p : ℂ := ChatgptAudit.modularPhase t r with hpdef
  have hp : ‖p‖ = 1 := by
    rw [hpdef]
    unfold ChatgptAudit.modularPhase
    exact Complex.norm_exp_ofReal_mul_I _
  have hp0 : p ≠ 0 := by
    intro h; rw [h, norm_zero] at hp; exact zero_ne_one hp
  have hsymm : (C.Δit t).symm ψ = p⁻¹ • ψ := by
    apply (C.Δit t).injective
    rw [LinearIsometryEquiv.apply_symm_apply, LinearIsometryEquiv.map_smul, hψ t, smul_smul,
      inv_mul_cancel₀ hp0, one_smul]
  have hrel := congrArg (fun T : W.H →L[ℂ] W.H => T ψ) (C.poincare_relation t (l • nullDir))
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply] at hrel
  rw [wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul] at hrel
  rw [← hrel]
  have hin : ⟪ψ, C.Δit t (W.U (l • nullDir) ((C.Δit t).symm ψ))⟫_ℂ
      = ⟪(C.Δit t).symm ψ, W.U (l • nullDir) ((C.Δit t).symm ψ)⟫_ℂ := by
    have h := (C.Δit t).inner_map_map ((C.Δit t).symm ψ)
      (W.U (l • nullDir) ((C.Δit t).symm ψ))
    rw [LinearIsometryEquiv.apply_symm_apply] at h
    exact h
  rw [hin, hsymm, map_smul, inner_smul_left, inner_smul_right, ← mul_assoc]
  have hq : (starRingEnd ℂ) p⁻¹ * p⁻¹ = 1 := by
    rw [Complex.conj_mul', norm_inv, hp, inv_one]
    simp
  rw [hq, one_mul]

/-- [DERIVED] ★★★ O TEOREMA DE COERÊNCIA (item 7): em QUALQUER habitante da v3, Δ^{it} não tem autovetor
    fora de ℂ·Ω. Prova: a correlação nula de um autovetor é invariante por dilatação (lema acima), contínua
    em 0 (`translations_continuous`), logo constante = ‖ψ‖²; então U(λn)ψ = ψ (igualdade na norma), e a
    ergodicidade nula (`null_ergodic`) põe ψ em ℂΩ. Não usa energia positiva nem KMS.
    É o OPOSTO de `contratoH2_forces_point_spectrum` (v2): lá TODO habitante tinha autovetor fora de ℂΩ. -/
theorem no_point_spectrum (C : ContratoH2 W R) : NoEigenOutsideVacuum W C.Δit := by
  intro ψ r hψ
  apply C.null_ergodic
  set g : ℝ → ℂ := fun l => ⟪ψ, W.U (l • nullDir) ψ⟫_ℂ with hg
  have hcont : Continuous g := by
    have h1 : Continuous (fun l : ℝ => W.U (l • nullDir) ψ) :=
      (C.translations_continuous ψ).comp (continuous_id.smul continuous_const)
    exact continuous_const.inner h1
  have hdil : ∀ l μ : ℝ, 0 < μ → g (l * μ) = g l := by
    intro l μ hμ
    have h := eigen_null_correlation_dilation C hψ (-(Real.log μ) / (2 * Real.pi)) l
    have hpi : (2 * Real.pi) ≠ 0 := by positivity
    have he : Real.exp (-(2 * Real.pi * (-(Real.log μ) / (2 * Real.pi)))) = μ := by
      have : -(2 * Real.pi * (-(Real.log μ) / (2 * Real.pi))) = Real.log μ := by
        field_simp
      rw [this, Real.exp_log hμ]
    rw [he] at h
    exact h
  have hconst : ∀ l : ℝ, g l = g 0 := by
    intro l
    have hlim : Tendsto (fun μ : ℝ => g (l * μ)) (𝓝[>] 0) (𝓝 (g 0)) := by
      have h0 : Tendsto (fun μ : ℝ => l * μ) (𝓝[>] (0:ℝ)) (𝓝 0) := by
        have h : Tendsto (fun μ : ℝ => l * μ) (𝓝 (0:ℝ)) (𝓝 (l * 0)) :=
          (continuous_const_mul l).tendsto 0
        rw [mul_zero] at h
        exact h.mono_left nhdsWithin_le_nhds
      exact (hcont.tendsto 0).comp h0
    have hlim' : Tendsto (fun μ : ℝ => g (l * μ)) (𝓝[>] 0) (𝓝 (g l)) := by
      apply tendsto_const_nhds.congr'
      filter_upwards [self_mem_nhdsWithin] with μ hμ
      exact (hdil l μ hμ).symm
    exact tendsto_nhds_unique hlim' hlim
  have hg0 : g 0 = ⟪ψ, ψ⟫_ℂ := by
    simp only [hg, zero_smul, W.U_zero]
    rfl
  intro l
  have hgl : ⟪ψ, W.U (l • nullDir) ψ⟫_ℂ = ⟪ψ, ψ⟫_ℂ := by
    have := hconst l
    rw [hg0] at this
    exact this
  have hre : RCLike.re ⟪W.U (l • nullDir) ψ, ψ⟫_ℂ = ‖ψ‖ ^ 2 := by
    rw [inner_re_symm, hgl, inner_self_eq_norm_sq_to_K]
    norm_cast
  have hn := @norm_sub_sq ℂ W.H _ _ _ (W.U (l • nullDir) ψ) ψ
  rw [hre, U_norm] at hn
  have hz : ‖W.U (l • nullDir) ψ - ψ‖ ^ 2 = 0 := by rw [hn]; ring
  have hz' : ‖W.U (l • nullDir) ψ - ψ‖ = 0 := by
    exact (pow_eq_zero_iff two_ne_zero).mp hz
  exact sub_eq_zero.mp (norm_eq_zero.mp hz')

/-! ## §D — ★★ κ AMARRADO: Unruh como TEOREMA KMS; κ = 1/ρ do observador -/

end ContratoH2

/-- [DERIVED] ★ REESCALA DO KMS: se α é KMS a β, então τ ↦ α(λτ) (λ > 0) é KMS a β/λ. Puro cálculo de faixas
    (a F nova é z ↦ F(λz)). -/
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

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- [DERIVED] o fluxo modular, lido em rapidez, é o boost à taxa 2π: Δit(−t) = V(2πt). -/
theorem modular_is_boost_at_two_pi (C : ContratoH2 W R) :
    (fun t => C.Δit (-t)) = (fun t => C.boost.V (2 * Real.pi * t)) := by
  funext t
  rw [C.bw]
  ring_nf

/-- [DERIVED] ★★★ UNRUH COMO TEOREMA (item 3): o fluxo de Killing τ ↦ V(κτ) do MESMO κ é KMS a β = 2π/κ,
    i.e. a temperatura de Unruh T = κ/2π é a temperatura KMS do fluxo de Killing — lida dos campos `kms`
    (Δit é o fluxo modular) e `bw` (Δ^{it} = V(−2πt)). Na v2 era definição (`kappa_eq_two_pi_temperature`). -/
theorem unruh_is_kms (C : ContratoH2 W R) :
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

/-- [DERIVED] a leitura em temperatura: β_Killing = 1/T_Unruh. -/
theorem unruh_is_kms_temperature (C : ContratoH2 W R) :
    KMSAt W C.killingFlow (1 / C.unruhTemperature) := by
  have h := unruh_is_kms C
  have : (1 : ℝ) / C.unruhTemperature = 2 * Real.pi / C.kappa := by
    unfold ContratoH2.unruhTemperature
    have := C.kappa_pos.ne'
    field_simp
  rw [this]; exact h

/-- [DERIVED] ★ κ DETERMINADO PELO OBSERVADOR: κ·ρ_obs = 1, com ρ_obs = √(x¹² − x⁰²) o raio de Rindler do
    observador fiducial (na sua órbita |ξ_κ| = 1; κ é a sua aceleração própria [KNOWN, cinemática]). -/
theorem kappa_mul_radius (C : ContratoH2 W R) :
    C.kappa * Real.sqrt (C.observer 1 ^ 2 - C.observer 0 ^ 2) = 1 := by
  have h := C.observer_unit
  have hx : |C.observer 0| < C.observer 1 := C.observer_in_wedge
  simp [minkowskiSq, killingField] at h
  have hk : C.kappa ^ 2 * (C.observer 1 ^ 2 - C.observer 0 ^ 2) = 1 := by
    linear_combination h
  rw [← Real.sqrt_sq C.kappa_pos.le, ← Real.sqrt_mul (sq_nonneg _), hk, Real.sqrt_one]

theorem kappa_eq_inv_radius (C : ContratoH2 W R) :
    C.kappa = 1 / Real.sqrt (C.observer 1 ^ 2 - C.observer 0 ^ 2) := by
  have h := kappa_mul_radius C
  have hne : Real.sqrt (C.observer 1 ^ 2 - C.observer 0 ^ 2) ≠ 0 := by
    intro h0; rw [h0, mul_zero] at h; exact zero_ne_one h
  field_simp
  linarith [h]

/-- [DERIVED] o fluxo de Killing é grupo (V_zero, V_add) — a mesma lei de grupo de `boostMat_add`. -/
theorem killingFlow_add (C : ContratoH2 W R) (τ σ : ℝ) :
    C.killingFlow (τ + σ) = (C.killingFlow σ).trans (C.killingFlow τ) := by
  unfold ContratoH2.killingFlow
  rw [mul_add, C.boost.V_add]

theorem killingFlow_zero (C : ContratoH2 W R) :
    C.killingFlow 0 = LinearIsometryEquiv.refl ℂ W.H := by
  unfold ContratoH2.killingFlow
  rw [mul_zero, C.boost.V_zero]

/-- [DERIVED] o campo de Killing é o JATO da ação geométrica do fluxo de Killing: d/dτ|₀ Λ(κτ)x = ξ_κ(x). -/
theorem killingField_is_the_jet (κ : ℝ) (x : Fin 4 → ℝ) :
    HasDerivAt (fun s : ℝ => wedgeBoostMap (κ * s) x) (killingField κ x) 0 := by
  have hl : HasDerivAt (fun s : ℝ => κ * s) κ 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).const_mul κ
  have h0 : HasDerivAt (fun s : ℝ => Real.cosh (κ * s) * x 0 + Real.sinh (κ * s) * x 1)
      (κ * x 1) 0 := by
    refine (((hl.cosh).mul_const (x 0)).add ((hl.sinh).mul_const (x 1))).congr_deriv ?_
    simp
  have h1 : HasDerivAt (fun s : ℝ => Real.sinh (κ * s) * x 0 + Real.cosh (κ * s) * x 1)
      (κ * x 0) 0 := by
    refine (((hl.sinh).mul_const (x 0)).add ((hl.cosh).mul_const (x 1))).congr_deriv ?_
    simp
  have hw : ∀ s : ℝ, wedgeBoostMap s x = ![Real.cosh s * x 0 + Real.sinh s * x 1,
      Real.sinh s * x 0 + Real.cosh s * x 1, x 2, x 3] := by
    intro s
    funext i
    fin_cases i <;> simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]
  rw [hasDerivAt_pi]
  intro i
  fin_cases i
  · simpa [hw, killingField] using h0
  · simpa [hw, killingField] using h1
  · simpa [hw, killingField] using hasDerivAt_const (0 : ℝ) (x 2)
  · simpa [hw, killingField] using hasDerivAt_const (0 : ℝ) (x 3)

/-! ## §F — as energias: K = 2πB -/

/-- [DERIVED] ★ K = 2πB: se ψ tem energia de boost b, tem energia modular 2πb (de `bw`, regra da cadeia). -/
theorem modularEnergy_of_boostEnergy (C : ContratoH2 W R) {ψ : W.H} {b : ℝ}
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

/-- [DERIVED] a energia modular é única (derivada única). -/
theorem modularEnergy_unique {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {D : ℝ → (H ≃ₗᵢ[ℂ] H)} {ψ : H} {k k' : ℝ}
    (h : HasModularEnergy D ψ k) (h' : HasModularEnergy D ψ k') : k = k' := by
  have hu := h.unique h'
  have hI : I * (k : ℂ) = I * (k' : ℂ) := neg_inj.mp hu
  have : (k : ℂ) = k' := mul_left_cancel₀ Complex.I_ne_zero hI
  exact_mod_cast this

/-- [DERIVED] o vácuo tem energia modular zero (⟨K⟩_Ω = 0; de Δit_vac). -/
theorem vac_modularEnergy (C : ContratoH2 W R) : HasModularEnergy C.Δit W.vac 0 := by
  unfold HasModularEnergy
  have : (fun t : ℝ => ⟪W.vac, C.Δit t W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext t; rw [Δit_vac]
  rw [this]
  simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)

/-- [DERIVED] o vácuo tem energia de boost zero. -/
theorem vac_boostEnergy (C : ContratoH2 W R) : HasBoostEnergy C.boost.V W.vac 0 := by
  unfold HasBoostEnergy
  have : (fun s : ℝ => ⟪W.vac, C.boost.V s W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext s; rw [C.boost.V_vac]
  rw [this]
  simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)

end ContratoH2

/-! ## §E — ★ o implementador é ÚNICO -/

/-- [DERIVED] ★ dois unitários que fixam o vácuo e implementam o MESMO fluxo de R coincidem (o vácuo é
    cíclico para a cunha — campo da testemunha W). Logo Δit não é escolha: é lido de R. -/
theorem implementer_unique {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    (D₁ D₂ : ℝ → (W.H ≃ₗᵢ[ℂ] W.H))
    (h₁v : ∀ t, D₁ t W.vac = W.vac) (h₂v : ∀ t, D₂ t W.vac = W.vac)
    (h₁ : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
      ((R.modular.modularFlow t) a).val = (D₁ t).conjStarAlgEquiv a.val)
    (h₂ : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
      ((R.modular.modularFlow t) a).val = (D₂ t).conjStarAlgEquiv a.val)
    (t : ℝ) : D₁ t = D₂ t := by
  have hpt : ∀ T ∈ W.net rightWedge, D₁ t (T W.vac) = D₂ t (T W.vac) := by
    intro T hT
    have hmem : T ∈ R.modular.wedgeAlgebra.toStarSubalgebra := by
      show T ∈ R.modular.wedgeAlgebra
      rw [R.modular.wedgeAlgebra_eq]; exact hT
    have e1 := congrArg (fun X : W.H →L[ℂ] W.H => X W.vac) (h₁ t ⟨T, hmem⟩)
    have e2 := congrArg (fun X : W.H →L[ℂ] W.H => X W.vac) (h₂ t ⟨T, hmem⟩)
    simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply] at e1 e2
    have s1 : (D₁ t).symm W.vac = W.vac := by
      apply (D₁ t).injective
      rw [LinearIsometryEquiv.apply_symm_apply, h₁v]
    have s2 : (D₂ t).symm W.vac = W.vac := by
      apply (D₂ t).injective
      rw [LinearIsometryEquiv.apply_symm_apply, h₂v]
    rw [s1] at e1
    rw [s2] at e2
    rw [← e1, ← e2]
  have hspan : ∀ x ∈ Submodule.span ℂ
      ((fun T : W.H →L[ℂ] W.H => T W.vac) '' (W.net rightWedge : Set (W.H →L[ℂ] W.H))),
      D₁ t x = D₂ t x := by
    intro x hx
    induction hx using Submodule.span_induction with
    | mem x hx =>
      obtain ⟨T, hT, rfl⟩ := hx
      exact hpt T hT
    | zero => simp
    | add x y _ _ hx hy => rw [map_add, map_add, hx, hy]
    | smul c x _ hx => rw [map_smul, map_smul, hx]
  have hfun : (fun x => D₁ t x) = (fun x => D₂ t x) :=
    Continuous.ext_on W.vac_cyclic_wedge (D₁ t).continuous (D₂ t).continuous hspan
  ext x
  exact congrFun hfun x

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- [DERIVED] dois contratos v3 no MESMO par têm o MESMO Δit (unicidade do implementador). -/
theorem Δit_determined (C C' : ContratoH2 W R) (t : ℝ) : C.Δit t = C'.Δit t :=
  implementer_unique C.Δit C'.Δit C.Δit_vac C'.Δit_vac C.flow_implemented C'.flow_implemented t

/-! ## §G — o frame (como na v2) -/

/-- [DERIVED] o determinante do boost é unidade (da condição de Lorentz). -/
theorem boostMat_det_isUnit (s : ℝ) : IsUnit (boostMat s).det := by
  have h := congrArg Matrix.det (boostMat_isLorentz s)
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose] at h
  have hη : eta4.det ≠ 0 := by
    unfold eta4
    rw [Matrix.det_diagonal, Fin.prod_univ_four]
    norm_num [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
      Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail]
  have hsq : (boostMat s).det * (boostMat s).det = 1 := by
    have h' : ((boostMat s).det * (boostMat s).det - 1) * eta4.det = 0 := by
      linear_combination h
    rcases mul_eq_zero.mp h' with h1 | h1
    · linarith
    · exact absurd h1 hη
  refine isUnit_iff_ne_zero.mpr ?_
  intro h0
  rw [h0, mul_zero] at hsq
  exact zero_ne_one hsq

/-- [DERIVED] o contrato alimenta a face finita de H2 (coframe + métrica lorentziana em cada ponto). -/
theorem feeds_finite_face (C : ContratoH2 W R) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    (C.E x)⁻¹ * C.E x = 1 ∧ LorentzByCongruence (solderMetric4 (C.E x)⁻¹) :=
  four_frame_gives_lorentz_metric (C.E x) (C.det_unit_on x hx)

/-- [DERIVED] o arrasto propaga a inversibilidade ao longo da órbita. -/
theorem det_unit_along_orbit (C : ContratoH2 W R) (s : ℝ) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    IsUnit (C.E (wedgeBoostMap s x)).det := by
  rw [C.dragged s x hx, Matrix.det_mul]
  exact (boostMat_det_isUnit s).mul (C.det_unit_on x hx)

end ContratoH2

/-- [DERIVED] `theCurvedFrame` não é arrastado pelo boost (entrada (1,0), x = (0,1,0,0), s = 1). -/
theorem curvedFrame_not_dragged :
    ¬ ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
        theCurvedFrame.E (wedgeBoostMap s x) = boostMat s * theCurvedFrame.E x := by
  intro h
  have hx : (![0, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp
  have h10 := congrFun (congrFun (h 1 _ hx) 1) 0
  rw [curvedFrame_E_apply, curvedFrame_E_apply] at h10
  simp [Matrix.mul_apply, boostMat, Fin.sum_univ_four, profileFn] at h10
  exact (Real.sinh_pos_iff.mpr one_pos).ne' h10.symm

/-- [DERIVED] a fiducial de `theCurvedFrame` não é a direção modular, para todo κ. -/
theorem curvedFrame_fiducial_not_modular (κ : ℝ) :
    ¬ ∀ x ∈ rightWedge, ∃ c : ℝ, 0 < c ∧
        (fun i => theCurvedFrame.E x i 0) = c • killingField κ x := by
  intro h
  have hx : (![1/2, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp; norm_num
  obtain ⟨c, hc, hE⟩ := h _ hx
  have h0 := congrFun hE 0
  have h1 := congrFun hE 1
  simp [curvedFrame_E_apply, killingField, profileFn] at h0 h1
  rcases h1 with h1 | h1
  · exact hc.ne' h1
  · rw [h1, mul_zero] at h0
    norm_num at h0

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- [DERIVED] (lê `dragged`) o frame de um contrato não é `theCurvedFrame`. -/
theorem frame_ne_curvedFrame_by_drag (C : ContratoH2 W R) : C.E ≠ theCurvedFrame.E := by
  intro hE
  apply curvedFrame_not_dragged
  intro s x hx
  have h := C.dragged s x hx
  rw [hE] at h
  exact h

/-- [DERIVED] (lê `fiducial_is_modular`) idem, pela fiducial. -/
theorem frame_ne_curvedFrame_by_fiducial (C : ContratoH2 W R) : C.E ≠ theCurvedFrame.E := by
  intro hE
  apply curvedFrame_fiducial_not_modular C.kappa
  intro x hx
  have h := C.fiducial_is_modular x hx
  rw [hE] at h
  exact h

end ContratoH2

/-! ## §H — ★★ H3: Clausius DERIVADO, BH com G fixo, razão universal -/

namespace ContratoH3

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- a variação de entropia de uma perturbação: δS := δ⟨K⟩ (primeira lei do emaranhamento) — DEFINIDA
    como a energia modular, relativa ao vácuo (⟨K⟩_Ω = 0, `vac_modularEnergy`). -/
def entropyVariation (C : ContratoH3 W R) (b : ℝ) : ℝ := 2 * Real.pi * b

/-- o calor de uma perturbação: o calor de Jacobson do tensor de matéria DO ESTADO. -/
def heat (C : ContratoH3 W R) (ψ : W.H) : ℝ :=
  horizonHeatK C.H2.kappa C.screen C.eps C.lam0 (C.matter ψ)

/-- [DERIVED] ★ a primeira lei lida: a energia modular de uma perturbação admissível é 2π × a de boost. -/
theorem first_law_value (C : ContratoH3 W R) {ψ : W.H} {b k : ℝ}
    (hb : HasBoostEnergy C.H2.boost.V ψ b) (hk : HasModularEnergy C.H2.Δit ψ k) :
    k = 2 * Real.pi * b :=
  ContratoH2.modularEnergy_unique hk (C.H2.modularEnergy_of_boostEnergy hb)

/-- [DERIVED] ★★★ CLAUSIUS COMO TEOREMA: δQ = T_Unruh · δS para TODA perturbação admissível — com δQ o
    calor da matéria DO ESTADO (`matter_is_state`), δS = δ⟨K⟩ (primeira lei) e T = κ/2π do MESMO κ.
    Na v2 era campo (`clausius`), ajustável dado um H2. -/
theorem clausius (C : ContratoH3 W R) {ψ : W.H} (hψ : ψ ∈ C.admissible) {b : ℝ}
    (hb : HasBoostEnergy C.H2.boost.V ψ b) :
    C.heat ψ = C.H2.unruhTemperature * (2 * Real.pi * b) := by
  unfold heat ContratoH2.unruhTemperature
  rw [C.matter_is_state ψ hψ b hb]
  field_simp

/-- [DERIVED] ★ Bekenstein–Hawking lida: δS = δA/(4G) com o G FIXO do contrato. -/
theorem bekenstein_hawking (C : ContratoH3 W R) {ψ : W.H} (hψ : ψ ∈ C.admissible) {b : ℝ}
    (hb : HasBoostEnergy C.H2.boost.V ψ b) :
    2 * Real.pi * b = deltaArea C.H2.E (C.response ψ) C.screen C.eps / (4 * C.G) :=
  C.area_law ψ hψ _ (C.H2.modularEnergy_of_boostEnergy hb)

/-- [DERIVED] ★ o 8πG: δQ = κ·δA/(8πG), para toda perturbação admissível. -/
theorem einstein_coefficient (C : ContratoH3 W R) {ψ : W.H} (hψ : ψ ∈ C.admissible) {b : ℝ}
    (hb : HasBoostEnergy C.H2.boost.V ψ b) :
    C.heat ψ = C.H2.kappa * deltaArea C.H2.E (C.response ψ) C.screen C.eps / (8 * Real.pi * C.G) := by
  rw [clausius C hψ hb, bekenstein_hawking C hψ hb]
  unfold ContratoH2.unruhTemperature
  exact einstein_coefficient_from_clausius _ _ _ C.G_pos.ne'

/-- [DERIVED] ★★ G NÃO SE AJUSTA POR PERTURBAÇÃO: para duas perturbações admissíveis quaisquer,
    b₁·δA₂ = b₂·δA₁ — a razão energia : resposta de área é UNIVERSAL (= 1/(8πG)). -/
theorem area_response_proportional (C : ContratoH3 W R) {ψ₁ ψ₂ : W.H}
    (h₁ : ψ₁ ∈ C.admissible) (h₂ : ψ₂ ∈ C.admissible) {b₁ b₂ : ℝ}
    (hb₁ : HasBoostEnergy C.H2.boost.V ψ₁ b₁) (hb₂ : HasBoostEnergy C.H2.boost.V ψ₂ b₂) :
    b₁ * deltaArea C.H2.E (C.response ψ₂) C.screen C.eps
      = b₂ * deltaArea C.H2.E (C.response ψ₁) C.screen C.eps := by
  have e1 := bekenstein_hawking C h₁ hb₁
  have e2 := bekenstein_hawking C h₂ hb₂
  have hG := C.G_pos
  have hpi : 0 < Real.pi := Real.pi_pos
  set A₁ := deltaArea C.H2.E (C.response ψ₁) C.screen C.eps
  set A₂ := deltaArea C.H2.E (C.response ψ₂) C.screen C.eps
  have f1 : A₁ = 8 * Real.pi * C.G * b₁ := by
    field_simp at e1; linarith
  have f2 : A₂ = 8 * Real.pi * C.G * b₂ := by
    field_simp at e2; linarith
  rw [f1, f2]; ring

/-- [DERIVED] ★ O BALANÇO NÃO É VAZIO: existe perturbação admissível com resposta de área ≠ 0
    (de `admissible_nontrivial` + `area_law` + G > 0). Substitui o `dA_ne` solto da v2. -/
theorem nontrivial_area_response (C : ContratoH3 W R) :
    ∃ ψ ∈ C.admissible, deltaArea C.H2.E (C.response ψ) C.screen C.eps ≠ 0 := by
  obtain ⟨ψ, hψ, b, hb, hb0⟩ := C.admissible_nontrivial
  refine ⟨ψ, hψ, fun h0 => ?_⟩
  have e := bekenstein_hawking C hψ hb
  rw [h0, zero_div] at e
  have : b = 0 := by
    have hpi : (2 * Real.pi) ≠ 0 := by positivity
    rcases mul_eq_zero.mp e with h | h
    · exact absurd h hpi
    · exact h
  exact hb0 this

/-- [DERIVED] no vácuo a resposta é nula e a lei de área vale trivialmente (consistência de
    `response_vac` com `area_law`). -/
theorem vacuum_balance (C : ContratoH3 W R) :
    deltaArea C.H2.E (C.response W.vac) C.screen C.eps = 0 := by
  unfold deltaArea
  rw [C.response_vac, sub_self]

/-- [DERIVED] ★ κ CANCELA em δS: δQ/T_Unruh = 2πb, independentemente da normalização κ (o que a v3 fixa
    não é o valor de κ — é o 2π de BW; κ é lido do observador). -/
theorem kappa_cancels (C : ContratoH3 W R) {ψ : W.H} (hψ : ψ ∈ C.admissible) {b : ℝ}
    (hb : HasBoostEnergy C.H2.boost.V ψ b) :
    C.heat ψ / C.H2.unruhTemperature = 2 * Real.pi * b := by
  rw [clausius C hψ hb]
  have hT : C.H2.unruhTemperature ≠ 0 := by
    unfold ContratoH2.unruhTemperature
    exact div_ne_zero C.H2.kappa_pos.ne' (by positivity)
  field_simp

/-- [DERIVED] o segmento do horizonte esticado vive na cunha. -/
theorem segment_in_wedge (C : ContratoH3 W R) {l : ℝ} (hl : C.lam0 ≤ l) (hl0 : l ≤ 0)
    (y : Fin 2 → ℝ) : horizonPoint C.eps l y ∈ rightWedge :=
  horizonPoint_mem_rightWedge C.eps_pos (lt_of_lt_of_le C.lam0_in_wedge hl) y

/-- a PROJEÇÃO no consumidor legado `HorizonEquilibriumData`, na perturbação não-trivial escolhida:
    os cinco números são CALCULADOS (κ do fluxo, δA da resposta, δS = 2πb, δQ = calor do estado). -/
def toHorizonData (C : ContratoH3 W R) : HorizonEquilibriumData :=
  let ψ := Classical.choose C.admissible_nontrivial
  let hψ := Classical.choose_spec C.admissible_nontrivial
  let b := Classical.choose hψ.2
  let hb := Classical.choose_spec hψ.2
  { kappa := C.H2.kappa
    G := C.G
    G_pos := C.G_pos
    dA := deltaArea C.H2.E (C.response ψ) C.screen C.eps
    dS := 2 * Real.pi * b
    dQ := C.heat ψ
    area_entropy := bekenstein_hawking C hψ.1 hb.1
    clausius := by
      have := clausius C hψ.1 hb.1
      unfold ContratoH2.unruhTemperature at this
      exact this }

/-- [DERIVED] o δA projetado é NÃO-NULO (o balanço projetado não é 0 = 0). -/
theorem toHorizonData_dA_ne (C : ContratoH3 W R) : C.toHorizonData.dA ≠ 0 := by
  let ψ := Classical.choose C.admissible_nontrivial
  let hψ := Classical.choose_spec C.admissible_nontrivial
  let b := Classical.choose hψ.2
  let hb := Classical.choose_spec hψ.2
  intro h0
  have e := bekenstein_hawking C hψ.1 hb.1
  change deltaArea C.H2.E (C.response ψ) C.screen C.eps = 0 at h0
  rw [h0, zero_div] at e
  have hpi : (2 * Real.pi) ≠ 0 := by positivity
  rcases mul_eq_zero.mp e with h | h
  · exact hpi h
  · exact hb.2 h

/-- [DERIVED] ★★ o contrato ALIMENTA o teorema mestre completo (v74), com o frame de H2 num ponto da cunha. -/
theorem feeds_the_master (C : ContratoH3 W R)
    {L : Type} [Lattice L] [BoundedOrder L] {T : SubadditiveTraceData L}
    (S : SusyRelativeData L T) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    (0 < T.tau S.ker ∧ T.tau S.ker < ⊤) ∧
      T.tau S.ker / T.tau S.ker = 1 ∧
      ((C.H2.E x)⁻¹ * C.H2.E x = 1 ∧ LorentzByCongruence (solderMetric4 (C.H2.E x)⁻¹)) ∧
      C.toHorizonData.dQ = C.toHorizonData.kappa * C.toHorizonData.dA
        / (8 * Real.pi * C.toHorizonData.G) :=
  emergence_master_full_triad S (C.H2.E x) (C.H2.det_unit_on x hx) C.toHorizonData

end ContratoH3

/-! ## §I — as paredes -/

/-- [DERIVED] ★★ A PAREDE DA FIDELIDADE: se alguma translação NÃO nula age trivialmente, o contrato é vazio. -/
theorem contratoH2_empty_of_unfaithful (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (h : ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ W.U a = 1) : IsEmpty (ContratoH2 W R) :=
  ⟨fun C => by
    obtain ⟨a, ha, hU⟩ := h
    exact ha (C.translations_faithful a hU)⟩

/-- [DERIVED] ★★ no PAR LEGADO (U = 1) a v3 é VAZIA. -/
theorem contratoH2_empty_on_legacy :
    IsEmpty (ContratoH2 theSpecificAQFTWitness regularModularRealization) :=
  contratoH2_empty_of_unfaithful _ _ ⟨nullDir, by
    intro h; have := congrFun h 0; simp [nullDir] at this, rfl⟩

theorem ratifying_the_legacy_pair_ratifies_the_void (F : FullTGLWitness)
    (h : F = regularFullWitness) : IsEmpty (ContratoH2 F.1 F.2) := by
  subst h
  exact contratoH2_empty_on_legacy

theorem contratoH3_empty_on_legacy :
    IsEmpty (ContratoH3 theSpecificAQFTWitness regularModularRealization) :=
  ⟨fun C => contratoH2_empty_on_legacy.false C.H2⟩

/-- [DERIVED] ★ (o dente de W5, na v3) translações que comutam com Δ^{it} são excluídas: pela relação de
    Poincaré no vetor nulo, U((e^{−2π}−1)n) = 1, contra a fidelidade. -/
theorem ContratoH2.commuting_translations_excluded {W : TGLSpecificAQFTWitness}
    {R : TGLModularRealization W} (C : ContratoH2 W R) :
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

/-! ## §J — o import indexado -/

/-- [DERIVED] ★ o import é NÃO-VAZIO por tipo: o índice é um H2 real, logo há H3 no par. -/
theorem ContratoImportH3.nonvacuous {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {h2 : ContratoH2 W R} (I : ContratoImportH3 W R h2) : Nonempty (ContratoH3 W R) :=
  ⟨I.produce h2⟩

/-- [DERIVED] ★ com o import indexado, o trio reduz-se a H1 SOZINHO: o próprio tipo do import já porta o H2. -/
theorem ContratoImportH3.makes_the_trio_H1 {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {h2 : ContratoH2 W R} (I : ContratoImportH3 W R h2) {H1 P : Prop}
    (master : H1 ∧ Nonempty (ContratoH2 W R) ∧ Nonempty (ContratoH3 W R) → P) : H1 → P :=
  fun h1 => master ⟨h1, ⟨h2⟩, I.nonvacuous⟩

/-- [DERIVED] ★ no par legado NÃO há import algum: nem o índice existe. -/
theorem no_import_on_legacy :
    ¬ ∃ h2 : ContratoH2 theSpecificAQFTWitness regularModularRealization,
        Nonempty (ContratoImportH3 theSpecificAQFTWitness regularModularRealization h2) :=
  fun ⟨h2, _⟩ => contratoH2_empty_on_legacy.false h2

/-! ## Os `#print axioms` -/

#print axioms U_norm
#print axioms ContratoH2.Δit_vac
#print axioms ContratoH2.bw_covariance
#print axioms ContratoH2.poincare_relation
#print axioms ContratoH2.translates
#print axioms ContratoH2.eigen_null_correlation_dilation
#print axioms ContratoH2.no_point_spectrum
#print axioms KMSAt.rescale
#print axioms ContratoH2.modular_is_boost_at_two_pi
#print axioms ContratoH2.unruh_is_kms
#print axioms ContratoH2.unruh_is_kms_temperature
#print axioms ContratoH2.kappa_mul_radius
#print axioms ContratoH2.kappa_eq_inv_radius
#print axioms ContratoH2.killingFlow_add
#print axioms ContratoH2.killingFlow_zero
#print axioms ContratoH2.killingField_is_the_jet
#print axioms ContratoH2.modularEnergy_of_boostEnergy
#print axioms ContratoH2.modularEnergy_unique
#print axioms ContratoH2.vac_modularEnergy
#print axioms ContratoH2.vac_boostEnergy
#print axioms implementer_unique
#print axioms ContratoH2.Δit_determined
#print axioms ContratoH2.boostMat_det_isUnit
#print axioms ContratoH2.feeds_finite_face
#print axioms ContratoH2.det_unit_along_orbit
#print axioms curvedFrame_not_dragged
#print axioms curvedFrame_fiducial_not_modular
#print axioms ContratoH2.frame_ne_curvedFrame_by_drag
#print axioms ContratoH2.frame_ne_curvedFrame_by_fiducial
#print axioms ContratoH3.first_law_value
#print axioms ContratoH3.clausius
#print axioms ContratoH3.bekenstein_hawking
#print axioms ContratoH3.einstein_coefficient
#print axioms ContratoH3.area_response_proportional
#print axioms ContratoH3.nontrivial_area_response
#print axioms ContratoH3.vacuum_balance
#print axioms ContratoH3.kappa_cancels
#print axioms ContratoH3.segment_in_wedge
#print axioms ContratoH3.toHorizonData_dA_ne
#print axioms ContratoH3.feeds_the_master
#print axioms contratoH2_empty_of_unfaithful
#print axioms contratoH2_empty_on_legacy
#print axioms ratifying_the_legacy_pair_ratifies_the_void
#print axioms contratoH3_empty_on_legacy
#print axioms ContratoH2.commuting_translations_excluded
#print axioms ContratoImportH3.nonvacuous
#print axioms ContratoImportH3.makes_the_trio_H1
#print axioms no_import_on_legacy

end

end TGLExt.ContratoQGv3
