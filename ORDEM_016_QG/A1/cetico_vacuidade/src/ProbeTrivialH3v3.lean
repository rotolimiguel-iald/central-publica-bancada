import ContratoQG_v3

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option maxHeartbeats 2000000

/-!
# ProbeTrivialH3v3 — O BALANÇO VAZIO contra H3 v3   [DIAGNÓSTICO; DEVE FALHAR; nunca importado]
  Frente contrato_v3, 23/09/2026.

  Dado um H2 v3 QUALQUER (hipótese `C2` — não se escolhe par), tenta-se o H3 mais barato: classe
  admissível só com o vácuo, matéria nula, resposta = o frame de H2, G = 1. Na v2 os números eram soltos e
  este tipo de habitante era barrado só pela amarração a um H2 inexistente. Na v3, com H2 DADO:
  * provados de verdade (com `first | … | trivial`, para a mutação só REMOVER erros): tela, ε, λ₀, unidade,
    vácuo admissível, energia do vácuo = 0 (de `bw` + `V_vac`), `matter_is_state` (0 = κ·0),
    `area_law` (0 = 0/4), `response_vac`, `response_det_unit_on`;
  * concedida a diferenciabilidade da área no frame de H2 (hipótese `hdiff`; é do frame, não do truque);
  * TEM de falhar: `admissible_nontrivial` — o vácuo não tem energia de boost ≠ 0.
  Resultado esperado (campos que falham): {admissible_nontrivial}. É o dente que substitui o `dA_ne` solto.
-/

namespace TGLExt.ContratoQGv3.ProbeH3

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Complex
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

theorem vac_boost_energy_zero (C2 : ContratoH2 W R) {b : ℝ}
    (hb : HasBoostEnergy C2.boost.V W.vac b) : b = 0 := by
  unfold HasBoostEnergy at hb
  have hc : (fun s : ℝ => ⟪W.vac, C2.boost.V s W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext s
    first | rw [C2.boost.V_vac] | rfl
  rw [hc] at hb
  have h0 := hb.unique (hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ))
  have : (b : ℂ) = 0 := by
    rcases mul_eq_zero.mp h0 with h | h
    · exact absurd h Complex.I_ne_zero
    · exact h
  exact_mod_cast this

/-- DEVE FALHAR em `admissible_nontrivial` (e só aí). -/
def probeEmptyBalance (C2 : ContratoH2 W R)
    (hdiff : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0) :
    ContratoH3 W R where
  H2 := C2
  G := 1
  G_pos := by first | exact one_pos | trivial
  screen := Set.Icc 0 1
  screen_measurable := by first | exact measurableSet_Icc | trivial
  screen_pos := by first | (rw [Real.volume_Icc_pi]; simp) | trivial
  screen_finite := by first | (rw [Real.volume_Icc_pi]; simp) | trivial
  eps := 1
  eps_pos := by first | exact one_pos | trivial
  lam0 := -1 / 4
  lam0_neg := by first | norm_num | trivial
  lam0_in_wedge := by first | norm_num | trivial
  admissible := {W.vac}
  admissible_unit := by
    first
    | (intro ψ hψ; rw [Set.mem_singleton_iff.mp hψ]; exact W.vac_norm)
    | trivial
  vac_admissible := by first | exact Set.mem_singleton _ | trivial
  admissible_energy := by
    first
    | (intro ψ hψ
       refine ⟨0, ?_⟩
       rw [Set.mem_singleton_iff.mp hψ]
       unfold HasBoostEnergy
       have hc : (fun s : ℝ => ⟪W.vac, C2.boost.V s W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
         funext s; rw [C2.boost.V_vac]
       rw [hc]
       simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ))
    | trivial
  admissible_nontrivial := by
    first
    | (refine ⟨W.vac, Set.mem_singleton _, 0, ?_, ?_⟩
       · unfold HasBoostEnergy
         have hc : (fun s : ℝ => ⟪W.vac, C2.boost.V s W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
           funext s; rw [C2.boost.V_vac]
         rw [hc]
         simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)
       · norm_num)
    | trivial
  response := fun _ => C2.E
  response_vac := by first | rfl | trivial
  response_det_unit_on := by first | (intro ψ _ x hx; exact C2.det_unit_on x hx) | trivial
  area_differentiable := by first | (intro ψ _; exact hdiff) | trivial
  matter := fun _ _ => 0
  matter_is_state := by
    first
    | (intro ψ hψ b hb
       rw [Set.mem_singleton_iff.mp hψ] at hb
       rw [vac_boost_energy_zero C2 hb, mul_zero]
       simp [horizonHeatK, pairing])
    | trivial
  area_law := by
    first
    | (intro ψ hψ k hk
       rw [Set.mem_singleton_iff.mp hψ] at hk
       have hk0 : HasModularEnergy C2.Δit W.vac 0 := by
         unfold HasModularEnergy
         have hc : (fun t : ℝ => ⟪W.vac, C2.Δit t W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
           funext t; rw [C2.bw, C2.boost.V_vac]
         rw [hc]
         simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)
       have hu := hk.unique hk0
       have hkk : (k : ℂ) = 0 := by
         have h1 : I * (k : ℂ) = I * ((0:ℝ) : ℂ) := neg_inj.mp hu
         simpa using mul_left_cancel₀ Complex.I_ne_zero h1
       have : k = 0 := by exact_mod_cast hkk
       rw [this]
       simp [deltaArea])
    | trivial

#print axioms vac_boost_energy_zero

end

end TGLExt.ContratoQGv3.ProbeH3
