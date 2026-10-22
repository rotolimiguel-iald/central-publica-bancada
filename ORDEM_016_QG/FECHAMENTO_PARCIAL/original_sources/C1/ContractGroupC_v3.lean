import ContractGroupB_v3

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

namespace ContratoH2
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}
/-! ## §C' — as paredes do CÉTICO 1 (BrinqH2Paredes.lean, 957f5ac79142a327), transpostas à v3.1 -/

/-- (T2, cético 1) grupo de boosts trivial não habita. -/
theorem trivial_boost_excluded (C : ContratoH2 W R N)
    (hV : ∀ s : ℝ, C.boost.V s = LinearIsometryEquiv.refl ℂ W.H) : False := by
  have hm0 : (Real.exp (-(2 * Real.pi)) - 1) • nullDir ≠ 0 := by
    intro h0
    have h := congrFun h0 0
    have hlt : Real.exp (-(2 * Real.pi)) < 1 := by
      have := Real.exp_lt_exp.mpr (show -(2 * Real.pi) < 0 by
        have := Real.pi_pos; linarith)
      simpa using this
    simp [nullDir] at h
    linarith
  apply hm0
  apply C.translations_faithful
  have hB := C.poincare_relation 1 nullDir
  rw [C.bw, hV] at hB
  have hid : (LinearIsometryEquiv.refl ℂ W.H).conjStarAlgEquiv (W.U nullDir) = W.U nullDir := by
    ext x; simp
  rw [hid, wedgeBoostMap_nullDir, mul_one] at hB
  have hsplit : Real.exp (-(2 * Real.pi)) • nullDir
      = nullDir + (Real.exp (-(2 * Real.pi)) - 1) • nullDir := by
    rw [sub_smul, one_smul]; abel
  rw [hsplit, W.U_add] at hB
  have hinv : W.U (-nullDir) * W.U nullDir = 1 := by
    rw [← W.U_add, neg_add_cancel, W.U_zero]
  calc W.U ((Real.exp (-(2 * Real.pi)) - 1) • nullDir)
      = (W.U (-nullDir) * W.U nullDir) * W.U ((Real.exp (-(2 * Real.pi)) - 1) • nullDir) := by
        rw [hinv, one_mul]
    _ = W.U (-nullDir) * (W.U nullDir * W.U ((Real.exp (-(2 * Real.pi)) - 1) • nullDir)) := by
        rw [mul_assoc]
    _ = W.U (-nullDir) * W.U nullDir := by rw [← hB]
    _ = 1 := hinv

theorem boost_moves_null_eigen (C : ContratoH2 W R N) (ψ : W.H) (ω : ℝ)
    (h : ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ) (s l : ℝ) :
    W.U (l • nullDir) (C.boost.V s ψ)
      = Complex.exp (((l * (Real.exp (-s) * ω) : ℝ) : ℂ) * I) • C.boost.V s ψ := by
  have hrel := congrArg (fun T : W.H →L[ℂ] W.H => T (C.boost.V s ψ))
    (C.boost.V_translations s ((l * Real.exp (-s)) • nullDir))
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    LinearIsometryEquiv.symm_apply_apply] at hrel
  rw [wedgeBoostMap_smul, wedgeBoostMap_nullDir, smul_smul] at hrel
  have he : l * Real.exp (-s) * Real.exp s = l := by
    rw [mul_assoc, ← Real.exp_add]; simp
  rw [he] at hrel
  rw [← hrel, h, LinearIsometryEquiv.map_smul]
  congr 2
  push_cast
  ring

theorem null_eigen_orth (ψ φ : W.H) (ω ω' : ℝ) (hne : ω' - ω ≠ 0)
    (hψ : ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ)
    (hφ : ∀ l : ℝ, W.U (l • nullDir) φ = Complex.exp (((l * ω' : ℝ) : ℂ) * I) • φ) :
    ⟪ψ, φ⟫_ℂ = 0 := by
  set l : ℝ := Real.pi / (ω' - ω) with hl
  have hinv : ⟪ψ, φ⟫_ℂ = ⟪W.U (l • nullDir) ψ, W.U (l • nullDir) φ⟫_ℂ := by
    rw [U_inner_adj W, U_neg_apply W]
  rw [hψ l, hφ l, inner_smul_left, inner_smul_right, ← mul_assoc] at hinv
  have hlω : l * ω' - l * ω = Real.pi := by
    rw [hl]; field_simp
  have hphase : (starRingEnd ℂ) (Complex.exp (((l * ω : ℝ) : ℂ) * I))
      * Complex.exp (((l * ω' : ℝ) : ℂ) * I) = -1 := by
    rw [← Complex.exp_conj, map_mul, Complex.conj_ofReal, Complex.conj_I, ← Complex.exp_add]
    have hc : ((l * ω' - l * ω : ℝ) : ℂ) = (Real.pi : ℂ) := by exact_mod_cast hlω
    have : ((l * ω : ℝ) : ℂ) * -I + ((l * ω' : ℝ) : ℂ) * I = (Real.pi : ℂ) * I := by
      push_cast at hc ⊢
      linear_combination hc * I
    rw [this, Complex.exp_pi_mul_I]
  rw [hphase] at hinv
  linear_combination (1 / 2 : ℂ) * hinv

/-- (T4, cético 1) ★★ num habitante, todo autovetor das translações nulas está em ℂΩ (exclui U de momento
    discreto — «de dimensão finita» ou de torre). Primeiro consumidor de `V_continuous`. -/
theorem null_point_spectrum_excluded (C : ContratoH2 W R N) (ψ : W.H) (ω : ℝ)
    (h : ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ) :
    ψ ∈ (ℂ ∙ W.vac) := by
  by_cases hω : ω = 0
  · apply C.null_ergodic
    intro l
    rw [h l, hω]
    simp
  · suffices hψ : ψ = 0 by rw [hψ]; exact Submodule.zero_mem _
    have horth : ∀ s : ℝ, s ≠ 0 → ⟪ψ, C.boost.V s ψ⟫_ℂ = 0 := by
      intro s hs
      have hne : Real.exp (-s) * ω - ω ≠ 0 := by
        intro h0
        have h1 : (Real.exp (-s) - 1) * ω = 0 := by linarith [h0]
        rcases mul_eq_zero.mp h1 with h2 | h2
        · have h3 : Real.exp (-s) = 1 := by linarith
          have h4 : -s = 0 := Real.exp_eq_one_iff (-s) |>.mp h3
          exact hs (by linarith)
        · exact hω h2
      exact null_eigen_orth ψ (C.boost.V s ψ) ω (Real.exp (-s) * ω) hne h
        (boost_moves_null_eigen C ψ ω h s)
    have hcont : Continuous (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) :=
      continuous_const.inner (C.boost.V_continuous ψ)
    have hlim : Tendsto (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) (𝓝[≠] 0) (𝓝 0) := by
      apply tendsto_const_nhds.congr'
      filter_upwards [self_mem_nhdsWithin] with s hs
      exact (horth s hs).symm
    have hlim2 : Tendsto (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) (𝓝[≠] 0)
        (𝓝 ⟪ψ, C.boost.V 0 ψ⟫_ℂ) :=
      (hcont.tendsto 0).mono_left nhdsWithin_le_nhds
    have h0 : ⟪ψ, C.boost.V 0 ψ⟫_ℂ = 0 := tendsto_nhds_unique hlim2 hlim
    rw [C.boost.V_zero] at h0
    change ⟪ψ, ψ⟫_ℂ = 0 at h0
    exact inner_self_eq_zero.mp h0

end ContratoH2

/-- (T1, cético 1) U que só lê as coordenadas transversais não habita. -/
theorem transverse_U_excluded {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization}
    (hU : ∀ a : Fin 4 → ℝ, W.U a = W.U ![0, 0, a 2, a 3]) : IsEmpty (ContratoH2 W R N) := by
  refine ⟨fun C => ?_⟩
  have h0 := C.translations_faithful nullDir (by
    rw [hU]
    have : (![0, 0, nullDir 2, nullDir 3] : Fin 4 → ℝ) = 0 := by
      funext i; fin_cases i <;> simp [nullDir]
    rw [this, W.U_zero])
  have := congrFun h0 0
  simp [nullDir] at this

/-- (T4', cético 1) U de momento nulo discreto ⟹ vazio. -/
theorem discrete_null_momentum_excluded {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization}
    (hpt : ∃ (ψ : W.H) (ω : ℝ), ψ ∉ (ℂ ∙ W.vac) ∧
      ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ) :
    IsEmpty (ContratoH2 W R N) := by
  refine ⟨fun C => ?_⟩
  obtain ⟨ψ, ω, hψ, h⟩ := hpt
  exact hψ (C.null_point_spectrum_excluded ψ ω h)


end
end TGLExt.ContratoQGv31

#print axioms TGLExt.ContratoQGv31.ContratoH2.trivial_boost_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH2.boost_moves_null_eigen
#print axioms TGLExt.ContratoQGv31.ContratoH2.null_eigen_orth
#print axioms TGLExt.ContratoQGv31.ContratoH2.null_point_spectrum_excluded
#print axioms TGLExt.ContratoQGv31.transverse_U_excluded
#print axioms TGLExt.ContratoQGv31.discrete_null_momentum_excluded
