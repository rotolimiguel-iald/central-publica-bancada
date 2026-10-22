import ContratoQG_v3

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# GuardasV3 — UMA GUARDA POR CAMPO `Prop` do contrato v3   [DIAGNÓSTICO; nunca importado pelo kernel]
  Frente contrato_v3, 23/09/2026. Resposta ao cético final de W2 («os probes no par legado têm rc
  CONSTANTE: afrouxar `dragged`/`fiducial_is_modular` a True não muda nada»).

  Cada `guard_<Estrutura>_<campo>` LÊ o conteúdo do campo (ou uma consequência dele que só ele dá) de um
  habitante QUALQUER. Importa SÓ o tipo (`ContratoQG_v3`). Na linha de base todas compilam; na mutação
  `campo := True` (harness `mutacao/mutar.py`) a guarda do campo tem de ACUSAR ERRO — é a medida de que
  o campo não é decorativo no tipo. (Que ele MORDA um habitante ruim é medido pelos probes negativos,
  cujo CONJUNTO de campos que falham é o resultado.)
-/

namespace TGLExt.ContratoQGv3.Guardas

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Complex
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-! ### WedgeBoostRep -/
theorem guard_WedgeBoostRep_V_zero (B : WedgeBoostRep W) (ψ : W.H) : B.V 0 ψ = ψ := by
  rw [B.V_zero]; rfl
theorem guard_WedgeBoostRep_V_add (B : WedgeBoostRep W) (a b : ℝ) (ψ : W.H) :
    B.V (a + b) ψ = B.V a (B.V b ψ) := by
  rw [B.V_add]; rfl
theorem guard_WedgeBoostRep_V_continuous (B : WedgeBoostRep W) (ψ : W.H) :
    Continuous (fun s : ℝ => B.V s ψ) := B.V_continuous ψ
theorem guard_WedgeBoostRep_V_vac (B : WedgeBoostRep W) (s : ℝ) : B.V s W.vac = W.vac := B.V_vac s
theorem guard_WedgeBoostRep_V_translations (B : WedgeBoostRep W) (s : ℝ) (a : Fin 4 → ℝ) :
    (B.V s).conjStarAlgEquiv (W.U a) = W.U (wedgeBoostMap s a) := B.V_translations s a
theorem guard_WedgeBoostRep_V_net (B : WedgeBoostRep W) (s : ℝ) (O : Set (Fin 4 → ℝ))
    (T : W.H →L[ℂ] W.H) (hT : T ∈ W.net O) :
    (B.V s).conjStarAlgEquiv T ∈ W.net (wedgeBoostMap s '' O) := B.V_net s O T hT

/-! ### ContratoH2 -/
theorem guard_ContratoH2_kappa_pos (C : ContratoH2 W R) : 0 < C.unruhTemperature :=
  div_pos C.kappa_pos (by positivity)
theorem guard_ContratoH2_flow_implemented (C : ContratoH2 W R) (t : ℝ)
    (a : R.modular.wedgeAlgebra.toStarSubalgebra) :
    ((R.modular.modularFlow t) a).val W.vac = C.Δit t (a.val ((C.Δit t).symm W.vac)) := by
  rw [C.flow_implemented]; rfl
theorem guard_ContratoH2_kms (C : ContratoH2 W R) : KMSAt W (fun t => C.Δit (-t)) 1 := C.kms
theorem guard_ContratoH2_bw (C : ContratoH2 W R) (t : ℝ) :
    C.Δit t W.vac = C.boost.V (-(2 * Real.pi * t)) W.vac := by
  rw [C.bw]
theorem guard_ContratoH2_translations_continuous (C : ContratoH2 W R) (ψ : W.H) :
    Continuous (fun l : ℝ => W.U (l • nullDir) ψ) :=
  (C.translations_continuous ψ).comp (continuous_id.smul continuous_const)
theorem guard_ContratoH2_translations_faithful (C : ContratoH2 W R) : W.U nullDir ≠ 1 := by
  intro h
  have h0 := congrFun (C.translations_faithful _ h) 0
  simp [nullDir] at h0
theorem guard_ContratoH2_positive_energy (C : ContratoH2 W R) : PositiveEnergy W := C.positive_energy
theorem guard_ContratoH2_null_ergodic (C : ContratoH2 W R) (ψ : W.H)
    (h : ∀ l : ℝ, W.U (l • nullDir) ψ = ψ) : ψ ∈ (ℂ ∙ W.vac) := C.null_ergodic ψ h
theorem guard_ContratoH2_observer_in_wedge (C : ContratoH2 W R) : 0 < C.observer 1 := by
  have h : |C.observer 0| < C.observer 1 := C.observer_in_wedge
  exact lt_of_le_of_lt (abs_nonneg _) h
theorem guard_ContratoH2_observer_unit (C : ContratoH2 W R) :
    minkowskiSq (killingField C.kappa C.observer) = 1 := C.observer_unit
theorem guard_ContratoH2_smooth_on (C : ContratoH2 W R) (i j : Fin 4) :
    ContDiffOn ℝ (⊤ : ℕ∞) (fun x => C.E x i j) rightWedge := C.smooth_on i j
theorem guard_ContratoH2_det_unit_on (C : ContratoH2 W R) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    (C.E x).det ≠ 0 := (C.det_unit_on x hx).ne_zero
theorem guard_ContratoH2_dragged (C : ContratoH2 W R) (s : ℝ) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    C.E (wedgeBoostMap s x) = boostMat s * C.E x := C.dragged s x hx
theorem guard_ContratoH2_fiducial_is_modular (C : ContratoH2 W R) {x : Fin 4 → ℝ}
    (hx : x ∈ rightWedge) :
    ∃ c : ℝ, 0 < c ∧ (fun i => C.E x i 0) = c • killingField C.kappa x :=
  C.fiducial_is_modular x hx

/-! ### ContratoH3 -/
theorem guard_ContratoH3_G_pos (C : ContratoH3 W R) : 0 < 4 * C.G := by
  have := C.G_pos; linarith
theorem guard_ContratoH3_screen_measurable (C : ContratoH3 W R) : MeasurableSet C.screen :=
  C.screen_measurable
theorem guard_ContratoH3_screen_pos (C : ContratoH3 W R) : volume C.screen ≠ 0 :=
  C.screen_pos.ne'
theorem guard_ContratoH3_screen_finite (C : ContratoH3 W R) : volume C.screen ≠ ⊤ :=
  C.screen_finite.ne
theorem guard_ContratoH3_eps_pos (C : ContratoH3 W R) : 0 < C.eps / 2 := by
  have := C.eps_pos; linarith
theorem guard_ContratoH3_lam0_neg (C : ContratoH3 W R) : C.lam0 ≤ 0 := C.lam0_neg.le
theorem guard_ContratoH3_lam0_in_wedge (C : ContratoH3 W R) : -C.eps < 2 * C.lam0 := by
  have := C.lam0_in_wedge; linarith
theorem guard_ContratoH3_admissible_unit (C : ContratoH3 W R) {ψ : W.H} (h : ψ ∈ C.admissible) :
    ψ ≠ 0 := by
  intro h0; have := C.admissible_unit ψ h; rw [h0, norm_zero] at this; exact zero_ne_one this
theorem guard_ContratoH3_vac_admissible (C : ContratoH3 W R) : C.admissible.Nonempty :=
  ⟨W.vac, C.vac_admissible⟩
theorem guard_ContratoH3_admissible_energy (C : ContratoH3 W R) {ψ : W.H} (h : ψ ∈ C.admissible) :
    ∃ b : ℝ, HasBoostEnergy C.H2.boost.V ψ b := C.admissible_energy ψ h
theorem guard_ContratoH3_admissible_nontrivial (C : ContratoH3 W R) :
    ∃ ψ ∈ C.admissible, ∃ b : ℝ, HasBoostEnergy C.H2.boost.V ψ b ∧ b ≠ 0 := C.admissible_nontrivial
theorem guard_ContratoH3_response_vac (C : ContratoH3 W R) :
    deltaArea C.H2.E (C.response W.vac) C.screen C.eps = 0 := by
  unfold deltaArea; rw [C.response_vac, sub_self]
theorem guard_ContratoH3_response_det_unit_on (C : ContratoH3 W R) {ψ : W.H} (h : ψ ∈ C.admissible)
    {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) : (C.response ψ x).det ≠ 0 :=
  (C.response_det_unit_on ψ h x hx).ne_zero
theorem guard_ContratoH3_area_differentiable (C : ContratoH3 W R) {ψ : W.H} (h : ψ ∈ C.admissible) :
    DifferentiableAt ℝ (fun l => screenAreaOf (C.response ψ) C.screen C.eps l) 0 :=
  C.area_differentiable ψ h
theorem guard_ContratoH3_matter_is_state (C : ContratoH3 W R) {ψ : W.H} (h : ψ ∈ C.admissible)
    {b : ℝ} (hb : HasBoostEnergy C.H2.boost.V ψ b) :
    horizonHeatK C.H2.kappa C.screen C.eps C.lam0 (C.matter ψ) = C.H2.kappa * b :=
  C.matter_is_state ψ h b hb
theorem guard_ContratoH3_area_law (C : ContratoH3 W R) {ψ : W.H} (h : ψ ∈ C.admissible) {k : ℝ}
    (hk : HasModularEnergy C.H2.Δit ψ k) :
    4 * C.G * k = 4 * C.G * (deltaArea C.H2.E (C.response ψ) C.screen C.eps / (4 * C.G)) := by
  rw [← C.area_law ψ h k hk]

/-! ### ContratoImportH3 -/
theorem guard_ContratoImportH3_same_horizon {h2 : ContratoH2 W R} (I : ContratoImportH3 W R h2) :
    (I.produce h2).H2 = h2 := I.same_horizon h2

#print axioms guard_WedgeBoostRep_V_zero
#print axioms guard_WedgeBoostRep_V_add
#print axioms guard_WedgeBoostRep_V_continuous
#print axioms guard_WedgeBoostRep_V_vac
#print axioms guard_WedgeBoostRep_V_translations
#print axioms guard_WedgeBoostRep_V_net
#print axioms guard_ContratoH2_kappa_pos
#print axioms guard_ContratoH2_flow_implemented
#print axioms guard_ContratoH2_kms
#print axioms guard_ContratoH2_bw
#print axioms guard_ContratoH2_translations_continuous
#print axioms guard_ContratoH2_translations_faithful
#print axioms guard_ContratoH2_positive_energy
#print axioms guard_ContratoH2_null_ergodic
#print axioms guard_ContratoH2_observer_in_wedge
#print axioms guard_ContratoH2_observer_unit
#print axioms guard_ContratoH2_smooth_on
#print axioms guard_ContratoH2_det_unit_on
#print axioms guard_ContratoH2_dragged
#print axioms guard_ContratoH2_fiducial_is_modular
#print axioms guard_ContratoH3_G_pos
#print axioms guard_ContratoH3_screen_measurable
#print axioms guard_ContratoH3_screen_pos
#print axioms guard_ContratoH3_screen_finite
#print axioms guard_ContratoH3_eps_pos
#print axioms guard_ContratoH3_lam0_neg
#print axioms guard_ContratoH3_lam0_in_wedge
#print axioms guard_ContratoH3_admissible_unit
#print axioms guard_ContratoH3_vac_admissible
#print axioms guard_ContratoH3_admissible_energy
#print axioms guard_ContratoH3_admissible_nontrivial
#print axioms guard_ContratoH3_response_vac
#print axioms guard_ContratoH3_response_det_unit_on
#print axioms guard_ContratoH3_area_differentiable
#print axioms guard_ContratoH3_matter_is_state
#print axioms guard_ContratoH3_area_law
#print axioms guard_ContratoImportH3_same_horizon

end

end TGLExt.ContratoQGv3.Guardas
