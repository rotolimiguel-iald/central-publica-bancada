import ContratoQG_v3_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 4000000

/-!
# BrinqH2Paredes — AS TENTATIVAS DE BRINQUEDO CONTRA H2 v3, como PAREDES   [CÉTICO 1; DEVE COMPILAR]
  Cético 1 do contrato v3, 23/09/2026. Scratchpad. NÃO cunha nome reservado; nada move o gate.

  Cada tentativa de habitar `ContratoH2 W R` por brinquedo é aqui convertida num teorema QUANTIFICADO sobre
  todo par (W, R) — mais forte que um probe de rc=1 num par só:

  (T1) U TRANSVERSAL (U só lê a², a³: comuta com o boost) ⟹ vazio (fidelidade).
  (T2) BOOST TRIVIAL (V = 1) ⟹ vazio (via `commuting_translations_excluded`).
  (T3) TORRE: se ALGUM implementador do fluxo de R que fixa o vácuo tem autovetor fora de ℂΩ, o contrato é
       vazio (unicidade do implementador + `no_point_spectrum`).
  (T4) ★ NOVA: ESPECTRO PONTUAL DAS TRANSLAÇÕES NULAS: num habitante, todo autovetor de λ ↦ U(λn) está em
       ℂΩ. Usa `V_translations`, `V_continuous` e `null_ergodic`. Exclui todo U «de dimensão finita» ou de
       torre (momento discreto) — e dá a `V_continuous` o PRIMEIRO consumidor em teorema.

  Estatutos: tudo [DERIVED]. Sem sorry, sem axiom.
-/

namespace TGLExt.ContratoQGv3.CeticoBrinquedo

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Complex Filter Topology
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- (T1) ★ U que só lê as coordenadas transversais não habita a v3. -/
theorem transverse_U_excluded
    (hU : ∀ a : Fin 4 → ℝ, W.U a = W.U ![0, 0, a 2, a 3]) : IsEmpty (ContratoH2 W R) := by
  refine contratoH2_empty_of_unfaithful W R ⟨nullDir, ?_, ?_⟩
  · intro h; have := congrFun h 0; simp [nullDir] at this
  · rw [hU]
    have : (![0, 0, nullDir 2, nullDir 3] : Fin 4 → ℝ) = 0 := by
      funext i; fin_cases i <;> simp [nullDir]
    rw [this, W.U_zero]

/-- (T2) ★ grupo de boosts trivial não habita a v3. -/
theorem trivial_boost_excluded (C : ContratoH2 W R)
    (hV : ∀ s : ℝ, C.boost.V s = LinearIsometryEquiv.refl ℂ W.H) : False := by
  apply C.commuting_translations_excluded
  intro t a
  rw [C.bw, hV]
  ext x
  simp

/-- (T3) ★ A TORRE: se um implementador do fluxo de R (fixando o vácuo) tem autovetor fora de ℂΩ, então
    NENHUM contrato v3 existe sobre (W, R). -/
theorem tower_excluded (D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (hDv : ∀ t, D t W.vac = W.vac)
    (hD : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
      ((R.modular.modularFlow t) a).val = (D t).conjStarAlgEquiv a.val)
    (hpt : ∃ (v : W.H) (r : ℝ), v ∉ (ℂ ∙ W.vac) ∧
      ∀ t : ℝ, D t v = ChatgptAudit.modularPhase t r • v) :
    IsEmpty (ContratoH2 W R) := by
  refine ⟨fun C => ?_⟩
  obtain ⟨v, r, hv, hvD⟩ := hpt
  apply hv
  apply C.no_point_spectrum v r
  intro t
  rw [implementer_unique C.Δit D C.Δit_vac hDv C.flow_implemented hD t]
  exact hvD t

/-! ## (T4) ★ espectro pontual das translações NULAS -/

theorem boost_moves_null_eigen (C : ContratoH2 W R) (ψ : W.H) (ω : ℝ)
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

/-- (T4) ★★ num habitante da v3, todo autovetor das translações nulas está em ℂΩ: o momento nulo não tem
    espectro pontual fora do vácuo. (Um U «de dimensão finita» ou de torre tem — logo é excluído.) -/
theorem null_point_spectrum_excluded (C : ContratoH2 W R) (ψ : W.H) (ω : ℝ)
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

/-- (T4') corolário: se ALGUM vetor fora de ℂΩ é autovetor das translações nulas (U de momento discreto),
    o contrato é vazio. -/
theorem discrete_null_momentum_excluded
    (hpt : ∃ (ψ : W.H) (ω : ℝ), ψ ∉ (ℂ ∙ W.vac) ∧
      ∀ l : ℝ, W.U (l • nullDir) ψ = Complex.exp (((l * ω : ℝ) : ℂ) * I) • ψ) :
    IsEmpty (ContratoH2 W R) := by
  refine ⟨fun C => ?_⟩
  obtain ⟨ψ, ω, hψ, h⟩ := hpt
  exact hψ (null_point_spectrum_excluded C ψ ω h)

#print axioms transverse_U_excluded
#print axioms trivial_boost_excluded
#print axioms tower_excluded
#print axioms boost_moves_null_eigen
#print axioms null_eigen_orth
#print axioms null_point_spectrum_excluded
#print axioms discrete_null_momentum_excluded

end

end TGLExt.ContratoQGv3.CeticoBrinquedo
