import ContratoQG_v3_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# ProbeAjusteH3v3 — A LIBERDADE RESIDUAL de H3 v3, medida   [DIAGNÓSTICO POSITIVO; DEVE COMPILAR]
  Frente contrato_v3, 23/09/2026. Resposta ao cético final de W2 («BH e Clausius AJUSTÁVEIS dado um H2»).

  Na v3, dado um H2: Clausius é teorema (não se ajusta); G é fixo antes da perturbação e a razão
  energia : resposta de área é UNIVERSAL (`area_response_proportional`); o balanço vazio é recusado
  (`ProbeTrivialH3v3`, falha só em `admissible_nontrivial`). O QUE SOBRA — e este arquivo mede, COMPILANDO —
  é a RESPOSTA GEOMÉTRICA: com UMA perturbação ψ₁ e UM horizonte, se houver um frame E₁ com δA = 8πG·b₁ e um
  tensor T₁ com calor κ·b₁, o contrato é habitado. A dívida de H3 é, portanto, EXATAMENTE: a resposta
  geométrica tem de ser a métrica do estado (não um frame escolhido por perturbação) para TODOS os
  horizontes locais — o que, pelo argumento de Jacobson, é a equação de Einstein [OPEN, não formalizado].
-/

namespace TGLExt.ContratoQGv3.ProbeAjuste

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Complex
open scoped InnerProductSpace Classical

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

theorem boostEnergy_unique {V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {ψ : W.H} {b b' : ℝ}
    (h : HasBoostEnergy V ψ b) (h' : HasBoostEnergy V ψ b') : b = b' := by
  have hu := h.unique h'
  have : (b : ℂ) = b' := mul_left_cancel₀ Complex.I_ne_zero hu
  exact_mod_cast this

/-- [DERIVED] ★ A LIBERDADE RESIDUAL, como construção: uma perturbação, um horizonte, a geometria escolhida. -/
def residualH3 (C2 : ContratoH2 W R) (G : ℝ) (hG : 0 < G)
    (ψ₁ : W.H) (hψ₁ : ‖ψ₁‖ = 1) (hne : ψ₁ ≠ W.vac)
    (b₁ : ℝ) (hb₁ : HasBoostEnergy C2.boost.V ψ₁ b₁) (hb0 : b₁ ≠ 0)
    (E₁ : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (hE₁ : ∀ x ∈ rightWedge, IsUnit (E₁ x).det)
    (hd₀ : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0)
    (hd₁ : DifferentiableAt ℝ (fun l => screenAreaOf E₁ (Set.Icc 0 1) 1 l) 0)
    (harea : deltaArea C2.E E₁ (Set.Icc 0 1) 1 = 8 * Real.pi * G * b₁)
    (T₁ : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ)
    (hheat : horizonHeatK C2.kappa (Set.Icc 0 1) 1 (-1 / 4) T₁ = C2.kappa * b₁) :
    ContratoH3 W R where
  H2 := C2
  G := G
  G_pos := hG
  screen := Set.Icc 0 1
  screen_measurable := measurableSet_Icc
  screen_pos := by rw [Real.volume_Icc_pi]; simp
  screen_finite := by rw [Real.volume_Icc_pi]; simp
  eps := 1
  eps_pos := one_pos
  lam0 := -1 / 4
  lam0_neg := by norm_num
  lam0_in_wedge := by norm_num
  admissible := {W.vac, ψ₁}
  admissible_unit := by
    intro ψ hψ
    rcases hψ with h | h
    · rw [h]; exact W.vac_norm
    · rw [Set.mem_singleton_iff.mp h]; exact hψ₁
  vac_admissible := Set.mem_insert _ _
  admissible_energy := by
    intro ψ hψ
    rcases hψ with h | h
    · rw [h]; exact ⟨0, C2.vac_boostEnergy⟩
    · rw [Set.mem_singleton_iff.mp h]; exact ⟨b₁, hb₁⟩
  admissible_nontrivial := ⟨ψ₁, Set.mem_insert_of_mem _ rfl, b₁, hb₁, hb0⟩
  response := fun ψ => if ψ = ψ₁ then E₁ else C2.E
  response_vac := by simp [hne.symm]
  response_det_unit_on := by
    intro ψ hψ x hx
    by_cases h : ψ = ψ₁
    · simp only [h, if_true]; exact hE₁ x hx
    · simp only [h, if_false]; exact C2.det_unit_on x hx
  area_differentiable := by
    intro ψ hψ
    by_cases h : ψ = ψ₁
    · simp only [h, if_true]; exact hd₁
    · simp only [h, if_false]; exact hd₀
  matter := fun ψ => if ψ = ψ₁ then T₁ else fun _ => 0
  matter_is_state := by
    intro ψ hψ b hb
    rcases hψ with h | h
    · subst h
      have hb0' : b = 0 := boostEnergy_unique hb C2.vac_boostEnergy
      simp only [hne.symm, if_false]
      rw [hb0', mul_zero]
      simp [horizonHeatK, pairing]
    · rw [Set.mem_singleton_iff.mp h] at hb ⊢
      have : b = b₁ := boostEnergy_unique hb hb₁
      simp only [if_true]
      rw [this]
      exact hheat
  area_law := by
    intro ψ hψ k hk
    rcases hψ with h | h
    · subst h
      have hk0 : k = 0 := ContratoH2.modularEnergy_unique hk C2.vac_modularEnergy
      simp [hne.symm, deltaArea, hk0]
    · rw [Set.mem_singleton_iff.mp h] at hk ⊢
      have hk1 : k = 2 * Real.pi * b₁ :=
        ContratoH2.modularEnergy_unique hk (C2.modularEnergy_of_boostEnergy hb₁)
      simp only [if_true]
      rw [harea, hk1]
      field_simp
      ring

/-- [DERIVED] a leitura: com UM estado e UM horizonte, H3 v3 reduz-se à EXISTÊNCIA da resposta geométrica. -/
theorem H3_reduces_to_geometric_response (C2 : ContratoH2 W R) (G : ℝ) (hG : 0 < G)
    (ψ₁ : W.H) (hψ₁ : ‖ψ₁‖ = 1) (hne : ψ₁ ≠ W.vac)
    (b₁ : ℝ) (hb₁ : HasBoostEnergy C2.boost.V ψ₁ b₁) (hb0 : b₁ ≠ 0)
    (hd₀ : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0)
    (hresp : ∃ E₁ : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ, (∀ x ∈ rightWedge, IsUnit (E₁ x).det) ∧
      DifferentiableAt ℝ (fun l => screenAreaOf E₁ (Set.Icc 0 1) 1 l) 0 ∧
      deltaArea C2.E E₁ (Set.Icc 0 1) 1 = 8 * Real.pi * G * b₁)
    (hmat : ∃ T₁ : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ,
      horizonHeatK C2.kappa (Set.Icc 0 1) 1 (-1 / 4) T₁ = C2.kappa * b₁) :
    Nonempty (ContratoH3 W R) := by
  obtain ⟨E₁, hE₁, hd₁, harea⟩ := hresp
  obtain ⟨T₁, hheat⟩ := hmat
  exact ⟨residualH3 C2 G hG ψ₁ hψ₁ hne b₁ hb₁ hb0 E₁ hE₁ hd₀ hd₁ harea T₁ hheat⟩

#print axioms boostEnergy_unique
#print axioms residualH3
#print axioms H3_reduces_to_geometric_response

end

end TGLExt.ContratoQGv3.ProbeAjuste
