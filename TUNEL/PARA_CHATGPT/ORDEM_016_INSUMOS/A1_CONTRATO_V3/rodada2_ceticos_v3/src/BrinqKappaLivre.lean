import ContratoQG_v3_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# BrinqKappaLivre — «κ ESCOLHIDO DEPOIS»   [CÉTICO 1 / lente BRINQUEDO; DIAGNÓSTICO POSITIVO: DEVE COMPILAR]
  Cético 1 do contrato v3, 23/09/2026. Scratchpad. NÃO cunha nome reservado; nada move o gate.

  Pergunta: o contrato v3 diz (docstring (C4)) que «κ está AMARRADO três vezes». Se este arquivo compila,
  então de QUALQUER habitante hipotético C de `ContratoH2 W R` e de QUALQUER κ' > 0 fabrica-se outro
  habitante com `kappa = κ'`, com o MESMO Δit, o MESMO grupo de boosts, o MESMO frame E e os MESMOS campos
  (P) — só o observador fiducial muda (raio 1/κ'). O mesmo vale para `ContratoH3` (mesmo G, mesma
  resposta, mesma matéria). Logo o VALOR de κ não é fixado pelo tipo: é a escolha do observador (gauge da
  normalização do campo de Killing). O que o tipo fixa é o PRODUTO β_Killing·κ = 2π (reescala do KMS).

  Estatutos: tudo [DERIVED] aqui. Sem sorry, sem axiom. β jamais aparece.
-/

namespace TGLExt.ContratoQGv3.CeticoBrinquedo

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Complex
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- o observador de raio 1/κ' sobre o eixo x¹. -/
def obsAt (κ' : ℝ) : Fin 4 → ℝ := ![0, 1 / κ', 0, 0]

theorem obsAt_in_wedge {κ' : ℝ} (h : 0 < κ') : obsAt κ' ∈ rightWedge := by
  show |(obsAt κ') 0| < (obsAt κ') 1
  simp [obsAt]
  exact h

theorem obsAt_unit {κ' : ℝ} (h : 0 < κ') : minkowskiSq (killingField κ' (obsAt κ')) = 1 := by
  have h0 : κ' ≠ 0 := h.ne'
  simp [minkowskiSq, killingField, obsAt]
  field_simp
  exact Or.inl trivial

/-- ★ A REPARAMETRIZAÇÃO: de um habitante C, outro com κ = κ' (tudo o mais igual, salvo o observador). -/
def rekappa (C : ContratoH2 W R) (κ' : ℝ) (hκ' : 0 < κ') : ContratoH2 W R where
  kappa := κ'
  kappa_pos := hκ'
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer := obsAt κ'
  observer_in_wedge := obsAt_in_wedge hκ'
  observer_unit := obsAt_unit hκ'
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := by
    intro x hx
    obtain ⟨c, hc, h⟩ := C.fiducial_is_modular x hx
    have hk := C.kappa_pos
    refine ⟨c * C.kappa / κ', by positivity, ?_⟩
    rw [h]
    funext i
    simp only [killingField, Pi.smul_apply, smul_eq_mul]
    field_simp

theorem rekappa_kappa (C : ContratoH2 W R) (κ' : ℝ) (hκ' : 0 < κ') :
    (rekappa C κ' hκ').kappa = κ' := rfl

/-- a MESMA física: Δit, boost e frame idênticos (rfl). -/
theorem rekappa_same_physics (C : ContratoH2 W R) (κ' : ℝ) (hκ' : 0 < κ') :
    (rekappa C κ' hκ').Δit = C.Δit ∧ (rekappa C κ' hκ').boost = C.boost ∧
      (rekappa C κ' hκ').E = C.E := ⟨rfl, rfl, rfl⟩

/-- ★★ O VALOR DE κ NÃO É FIXADO PELO TIPO: se há UM habitante, há um para CADA κ' > 0. -/
theorem kappa_is_free (h : Nonempty (ContratoH2 W R)) :
    ∀ κ' : ℝ, 0 < κ' → ∃ C : ContratoH2 W R, C.kappa = κ' := by
  intro κ' hκ'
  obtain ⟨C⟩ := h
  exact ⟨rekappa C κ' hκ', rfl⟩

/-- ★★ a «temperatura de Unruh» do tipo também é livre: toda T' > 0 ocorre. -/
theorem unruhTemperature_is_free (h : Nonempty (ContratoH2 W R)) :
    ∀ T' : ℝ, 0 < T' → ∃ C : ContratoH2 W R, C.unruhTemperature = T' := by
  intro T' hT'
  obtain ⟨C⟩ := h
  refine ⟨rekappa C (2 * Real.pi * T') (by positivity), ?_⟩
  unfold ContratoH2.unruhTemperature
  show 2 * Real.pi * T' / (2 * Real.pi) = T'
  field_simp

/-- ★ o que o tipo fixa, de fato: dois habitantes quaisquer satisfazem KMS do fluxo de Killing com o MESMO
    produto β·κ = 2π — a normalização é livre, o 2π não. -/
theorem kms_product_is_two_pi (C : ContratoH2 W R) :
    (2 * Real.pi / C.kappa) * C.kappa = 2 * Real.pi := by
  have := C.kappa_pos.ne'
  field_simp

/-! ## a MESMA reparametrização em H3 (mesmo G, mesma resposta, mesma matéria) -/

/-- o calor de Jacobson é LINEAR em κ. -/
theorem horizonHeatK_linear (κ : ℝ) (S : Set (Fin 2 → ℝ)) (ε l₀ : ℝ)
    (T : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) :
    horizonHeatK κ S ε l₀ T = κ * horizonHeatK 1 S ε l₀ T := by
  unfold horizonHeatK
  have hpt : ∀ x : Fin 4 → ℝ, ∀ M : Matrix (Fin 4) (Fin 4) ℝ,
      pairing M (killingField κ x) nullDir = κ * pairing M (killingField 1 x) nullDir := by
    intro x M
    unfold pairing killingField
    rw [one_smul, smul_dotProduct, smul_eq_mul]
  simp_rw [hpt]
  rw [← intervalIntegral.integral_const_mul]
  congr 1
  funext l
  rw [integral_const_mul]

def rekappa3 (H : ContratoH3 W R) (κ' : ℝ) (hκ' : 0 < κ') : ContratoH3 W R where
  H2 := rekappa H.H2 κ' hκ'
  G := H.G
  G_pos := H.G_pos
  screen := H.screen
  screen_measurable := H.screen_measurable
  screen_pos := H.screen_pos
  screen_finite := H.screen_finite
  eps := H.eps
  eps_pos := H.eps_pos
  lam0 := H.lam0
  lam0_neg := H.lam0_neg
  lam0_in_wedge := H.lam0_in_wedge
  admissible := H.admissible
  admissible_unit := H.admissible_unit
  vac_admissible := H.vac_admissible
  admissible_energy := H.admissible_energy
  admissible_nontrivial := H.admissible_nontrivial
  response := H.response
  response_vac := H.response_vac
  response_det_unit_on := H.response_det_unit_on
  area_differentiable := H.area_differentiable
  matter := H.matter
  matter_is_state := by
    intro ψ hψ b hb
    have h := H.matter_is_state ψ hψ b hb
    have hk := H.H2.kappa_pos
    show horizonHeatK κ' H.screen H.eps H.lam0 (H.matter ψ) = κ' * b
    rw [horizonHeatK_linear] at h ⊢
    have h1 : horizonHeatK 1 H.screen H.eps H.lam0 (H.matter ψ) = b := by
      have := mul_left_cancel₀ hk.ne' (h.trans (by ring : H.H2.kappa * b = H.H2.kappa * b))
      exact this
    rw [h1]
  area_law := H.area_law

/-- ★★ em H3 também: se há UM habitante, há um para CADA κ' > 0, com o MESMO G. -/
theorem kappa_is_free_H3 (h : Nonempty (ContratoH3 W R)) :
    ∀ κ' : ℝ, 0 < κ' → ∃ H : ContratoH3 W R, H.H2.kappa = κ' := by
  intro κ' hκ'
  obtain ⟨H⟩ := h
  exact ⟨rekappa3 H κ' hκ', rfl⟩

theorem rekappa3_same_G (H : ContratoH3 W R) (κ' : ℝ) (hκ' : 0 < κ') :
    (rekappa3 H κ' hκ').G = H.G ∧ (rekappa3 H κ' hκ').response = H.response := ⟨rfl, rfl⟩

#print axioms obsAt_unit
#print axioms rekappa
#print axioms rekappa_same_physics
#print axioms kappa_is_free
#print axioms unruhTemperature_is_free
#print axioms kms_product_is_two_pi
#print axioms horizonHeatK_linear
#print axioms rekappa3
#print axioms kappa_is_free_H3
#print axioms rekappa3_same_G

end

end TGLExt.ContratoQGv3.CeticoBrinquedo
