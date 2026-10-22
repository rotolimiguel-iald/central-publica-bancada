import ContractGroupA_v2

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

/-! ## §B — o que a v2 pedia como CAMPO e a v3.1 DERIVA -/

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- [DERIVED] Δ^{it} fixa o vácuo (de `bw` + `V_vac`). -/
theorem Δit_vac (C : ContratoH2 W R N) (t : ℝ) : C.Δit t W.vac = W.vac := by
  rw [C.bw]; exact C.boost.V_vac _

/-- [DERIVED] Ad(Δ^{it}) é GEOMÉTRICO na rede: net(O) ↦ net(Λ(−2πt)O). -/
theorem bw_covariance (C : ContratoH2 W R N) (t : ℝ) (O : Set (Fin 4 → ℝ)) (T : W.H →L[ℂ] W.H)
    (hT : T ∈ W.net O) :
    (C.Δit t).conjStarAlgEquiv T ∈ W.net (wedgeBoostMap (-(2 * Real.pi * t)) '' O) := by
  rw [C.bw]; exact C.boost.V_net _ O T hT

/-- [DERIVED] Δ^{it} U(a) Δ^{−it} = U(Λ(−2πt)a). -/
theorem poincare_relation (C : ContratoH2 W R N) (t : ℝ) (a : Fin 4 → ℝ) :
    (C.Δit t).conjStarAlgEquiv (W.U a) = W.U (wedgeBoostMap (-(2 * Real.pi * t)) a) := by
  rw [C.bw]; exact C.boost.V_translations _ a

/-- [DERIVED] as translações não são triviais (fidelidade). -/
theorem translates (C : ContratoH2 W R N) : ∃ a : Fin 4 → ℝ, W.U a ≠ 1 := by
  refine ⟨nullDir, fun h => ?_⟩
  have h0 := congrFun (C.translations_faithful _ h) 0
  simp [nullDir] at h0

/-! ## §C — ★★★ COERÊNCIA ESPECTRAL -/

theorem eigen_null_correlation_dilation (C : ContratoH2 W R N) {ψ : W.H} {r : ℝ}
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

/-- [DERIVED] ★★★ O TEOREMA DE COERÊNCIA: em QUALQUER habitante da v3.1, Δ^{it} não tem autovetor fora
    de ℂ·Ω (o OPOSTO de `contratoH2_forces_point_spectrum`, v2). Não usa energia positiva nem KMS. -/
theorem no_point_spectrum (C : ContratoH2 W R N) : NoEigenOutsideVacuum W C.Δit := by
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


end ContratoH2

end
end TGLExt.ContratoQGv31

#print axioms TGLExt.ContratoQGv31.ContratoH2.Δit_vac
#print axioms TGLExt.ContratoQGv31.ContratoH2.bw_covariance
#print axioms TGLExt.ContratoQGv31.ContratoH2.poincare_relation
#print axioms TGLExt.ContratoQGv31.ContratoH2.translates
#print axioms TGLExt.ContratoQGv31.ContratoH2.eigen_null_correlation_dilation
#print axioms TGLExt.ContratoQGv31.ContratoH2.no_point_spectrum
