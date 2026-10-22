import ContratoQG_v31

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option maxHeartbeats 2000000

/-!
# ProbeTrivialH3v31 — O BALANÇO VAZIO contra H3 v3.1   [DIAGNÓSTICO; DEVE FALHAR; nunca importado]
  Frente contrato_v3, RODADA 2, 23/09/2026. Importa SÓ o tipo (para a mutação medir este arquivo sozinho).

  Dado um H2 v3.1 QUALQUER (C2) e um tensor T QUALQUER (não se escolhe par), tenta-se o H3 mais barato: classe
  admissível só com o vácuo, propagador nulo, θ = 0, G = 1. Provados de verdade (com `first | … | trivial`, para a
  mutação só REMOVER erros): fechamento por translações (U(a)Ω = Ω), `modular_charge` (0 = 2π·0),
  continuidade, o propagador nulo (nulo na fonte nula, covariante, simétrico, gauge), a expansão e a lei
  local (0 = −8πG·0).
  Concedido: a planura da tela de fundo de C2 (`hflat`, é do frame de H2, não do truque).
  TEM de falhar: `admissible_nontrivial` — o vácuo não tem energia modular ≠ 0.
-/

namespace TGLExt.ContratoQGv31.ProbeH3

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open MeasureTheory Complex
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem vac_modular_zero (C2 : ContratoH2 W R N) {k : ℝ} (hk : HasModularEnergy C2.Δit W.vac k) :
    k = 0 := by
  unfold HasModularEnergy at hk
  have hc : (fun t : ℝ => ⟪W.vac, C2.Δit t W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
    funext t
    first | rw [C2.bw, C2.boost.V_vac] | rfl
  rw [hc] at hk
  have h0 := hk.unique (hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ))
  have : (k : ℂ) = 0 := by
    have h1 : I * (k : ℂ) = 0 := neg_eq_zero.mp h0
    rcases mul_eq_zero.mp h1 with h | h
    · exact absurd h Complex.I_ne_zero
    · exact h
  exact_mod_cast this

theorem vac_null_energy (T : StressTensorData W) (x : Fin 4 → ℝ) : nullEnergy T W.vac x = 0 := by
  first | simp [nullEnergy, pairing, T.T_vac] | rfl

theorem vac_charge (T : StressTensorData W) : nullPlaneCharge T W.vac = 0 := by
  unfold nullPlaneCharge
  have : (fun p : ℝ × (Fin 2 → ℝ) => p.1 * nullEnergy T W.vac (p.1 • nullDir + screenEmbed p.2))
      = fun _ => (0:ℝ) := by
    funext p; rw [vac_null_energy, mul_zero]
  rw [this, integral_zero]

/-- DEVE FALHAR em `admissible_nontrivial` (e só aí). -/
def probeEmptyBalance (C2 : ContratoH2 W R N) (T : StressTensorData W)
    (hflat : ∀ x ∈ rightWedge, screenBlock (solderMetric4 (C2.E x)⁻¹) = -1) :
    ContratoH3 W R N T where
  H2 := C2
  G := 1
  G_pos := by first | exact one_pos | trivial
  admissible := {W.vac}
  admissible_unit := by
    first
    | (intro ψ hψ; rw [Set.mem_singleton_iff.mp hψ]; exact W.vac_norm)
    | trivial
  vac_admissible := by first | exact Set.mem_singleton _ | trivial
  admissible_translate := by
    first
    | (intro a ψ hψ; rw [Set.mem_singleton_iff.mp hψ, W.vac_invariant]; exact Set.mem_singleton _)
    | trivial
  modular_charge := by
    first
    | (intro ψ hψ k hk
       rw [Set.mem_singleton_iff.mp hψ] at hk ⊢
       rw [vac_modular_zero C2 hk, vac_charge, mul_zero])
    | trivial
  admissible_nontrivial := by
    first
    | (refine ⟨W.vac, Set.mem_singleton _, 0, ?_, ?_⟩
       · unfold HasModularEnergy
         have hc : (fun t : ℝ => ⟪W.vac, C2.Δit t W.vac⟫_ℂ) = fun _ => ⟪W.vac, W.vac⟫_ℂ := by
           funext t; rw [C2.bw, C2.boost.V_vac]
         rw [hc]
         simpa using hasDerivAt_const (0:ℝ) (⟪W.vac, W.vac⟫_ℂ)
       · norm_num)
    | trivial
  energy_continuous := by
    first
    | (intro ψ hψ x
       rw [Set.mem_singleton_iff.mp hψ]
       have : (fun l : ℝ => nullEnergy T W.vac (x + l • nullDir)) = fun _ => (0:ℝ) := by
         funext l; exact vac_null_energy T _
       rw [this]; exact continuous_const)
    | trivial
  background_screen_flat := by first | exact hflat | trivial
  propagator := fun _ _ => 0
  propagator_zero := by first | rfl | trivial
  propagator_covariant := by first | (intro a f; rfl) | trivial
  response_symm := by first | (intro ψ hψ x; exact Matrix.transpose_zero) | trivial
  lightcone_gauge := by first | (intro ψ hψ x; exact Matrix.zero_mulVec _) | trivial
  theta := fun _ _ => 0
  theta_is_expansion := by
    first
    | (intro ψ hψ x
       show HasDerivAt (fun l : ℝ => areaDensity (fun _ => (0 : Matrix (Fin 4) (Fin 4) ℝ)) (x + l • nullDir)) 0 0
       have : (fun l : ℝ => areaDensity (fun _ => (0 : Matrix (Fin 4) (Fin 4) ℝ)) (x + l • nullDir))
           = fun _ => (0:ℝ) := by
         funext l; simp [areaDensity]
       rw [this]
       exact hasDerivAt_const (0:ℝ) (0:ℝ))
    | trivial
  raychaudhuri_einstein := by
    first
    | (intro ψ hψ x
       rw [Set.mem_singleton_iff.mp hψ, vac_null_energy, mul_zero]
       exact hasDerivAt_const (0:ℝ) (0:ℝ))
    | trivial

#print axioms vac_modular_zero
#print axioms vac_null_energy
#print axioms vac_charge

end

end TGLExt.ContratoQGv31.ProbeH3
