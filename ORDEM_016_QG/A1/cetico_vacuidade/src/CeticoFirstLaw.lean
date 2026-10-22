import ContratoQG_v3_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CÉTICO 2 — o δS de H3 v3 (= energia modular de −log Δ) NÃO TEM TERMO DE 1ª ORDEM em torno do vácuo
  [DIAGNÓSTICO do cético; scratchpad cetico_vacuidade; nunca importado pelo kernel; NÃO cunha nome reservado]

  O contrato H3 v3 define δS := ⟨ψ, (−log Δ) ψ⟩ (via `HasModularEnergy`) e o chama «primeira lei do
  emaranhamento, vale em 1ª ordem». Mas −log Δ é o hamiltoniano modular BILATERAL (K_W − K_W'), que ANIQUILA
  o vácuo: para ψ_ε = Ω + ε·φ, a energia modular é EXATAMENTE ε²·k_φ — o termo de 1ª ordem é identicamente
  zero (`modularEnergy_of_perturbation`). A primeira lei δS_W = δ⟨K_W⟩ é de 1ª ordem e usa o K_W UNILATERAL.
  Leitura: o número 2πb que entra em `area_law` é δQ/T (Clausius), não δS de emaranhamento; e o rótulo
  «vale em 1ª ordem» é falso para esta definição.
-/

namespace TGLExt.ContratoQGv3.CeticoVacuidade

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open Complex
open scoped InnerProductSpace ComplexConjugate

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

theorem inner_vac_Δit (C : ContratoH2 W R) (t : ℝ) (φ : W.H) :
    ⟪W.vac, C.Δit t φ⟫_ℂ = ⟪W.vac, φ⟫_ℂ := by
  have h := (C.Δit t).inner_map_map W.vac φ
  rw [ContratoH2.Δit_vac] at h
  exact h

/-- [DERIVED] ★★ a energia modular da perturbação Ω + ε·φ é ε²·k_φ: SEM termo de 1ª ordem. -/
theorem modularEnergy_of_perturbation (C : ContratoH2 W R) {φ : W.H} {k : ℝ}
    (hk : HasModularEnergy C.Δit φ k) (ε : ℝ) :
    HasModularEnergy C.Δit (W.vac + (ε : ℂ) • φ) (ε ^ 2 * k) := by
  unfold HasModularEnergy at hk ⊢
  have hfun : (fun t : ℝ => ⟪W.vac + (ε : ℂ) • φ, C.Δit t (W.vac + (ε : ℂ) • φ)⟫_ℂ)
      = fun t : ℝ => (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
          + ((ε : ℂ) ^ 2) * ⟪φ, C.Δit t φ⟫_ℂ := by
    funext t
    rw [map_add, map_smul, ContratoH2.Δit_vac, inner_add_left, inner_add_right, inner_add_right,
      inner_smul_left, inner_smul_left, inner_smul_right, inner_smul_right, inner_vac_Δit]
    simp only [Complex.conj_ofReal]
    ring
  rw [hfun]
  have h2 := (hk.const_mul ((ε : ℂ) ^ 2)).const_add
    (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
  refine h2.congr_deriv ?_
  push_cast
  ring

/-- [DERIVED] ★ em particular, a derivada em ε = 0 do δS do contrato ao longo de QUALQUER perturbação é 0. -/
theorem contract_deltaS_first_order_vanishes (C : ContratoH2 W R) {φ : W.H} {k : ℝ}
    (hk : HasModularEnergy C.Δit φ k) :
    HasDerivAt (fun ε : ℝ => ε ^ 2 * k) 0 0 := by
  have h := ((hasDerivAt_pow 2 (0:ℝ)).mul_const k)
  simpa using h

#print axioms inner_vac_Δit
#print axioms modularEnergy_of_perturbation
#print axioms contract_deltaS_first_order_vanishes

end

end TGLExt.ContratoQGv3.CeticoVacuidade
