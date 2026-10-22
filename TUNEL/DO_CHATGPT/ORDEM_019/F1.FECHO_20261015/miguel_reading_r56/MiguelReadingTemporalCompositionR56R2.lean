import TGLExt.SelectionAngleReconstruction

/-!
R56 candidate. Human clarification: “Observador=forma matricial da luz”;
“Exatamente, agora vc quer demonstrar o ângulo de Miguel (ângulo de abertura da
fronteira) que é a leitura”. Full authorized wording is pinned in OPERADOR_VERBATIM_R56.json.

This file reuses the existing angular reader and decoder. The family with parameter
thetaMiguel beta + Omega*t is explicitly chosen here; no device generator, physical
clock normalization, global net realization or all-direction H3 is constructed.
The input Omega is not inferred from beta. The scalar spectral phase here has rate
Omega; the off-diagonal density coherence in the earlier R9 has rate 2*Omega.
No equality between the antiunitary J and the linear projection P is asserted.
-/

set_option autoImplicit false
namespace ChatgptAudit.MiguelReadingR56R2
open TGLExt ChatgptAudit.SelectionAngle Matrix Complex
noncomputable section

def readerForm (beta Omega t : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  Smat (thetaMiguel beta + Omega * t)

theorem initial_form (beta Omega : ℝ) : readerForm beta Omega 0 = Smat (thetaMiguel beta) := by
  simp [readerForm]

theorem opening_reconstructed (beta : ℝ) :
    angularDecoder (phaseReading (Smat (thetaMiguel beta))) = Smat (thetaMiguel beta) :=
  miguel_boundary_reconstructed_from_its_selected_face beta

theorem opening_weights {beta : ℝ} (h0 : 0 ≤ beta) (h1 : beta ≤ 1) :
    Complex.normSq ((Smat (thetaMiguel beta)).mulVec e1 1) = beta ∧
    Complex.normSq ((Smat (thetaMiguel beta)).mulVec e1 0) = 1 - beta := by
  constructor
  · rw [normSq_reflection, sin_thetaMiguel h0 h1, Real.sq_sqrt h0]
  · rw [normSq_transmission]
    have h := Real.sin_sq_add_cos_sq (thetaMiguel beta)
    rw [sin_thetaMiguel h0 h1, Real.sq_sqrt h0] at h
    linarith

theorem moving_reading (beta Omega t : ℝ) :
    phaseReading (readerForm beta Omega t) =
      Complex.exp (((thetaMiguel beta + Omega * t : ℝ) : ℂ) * Complex.I) := by
  unfold readerForm
  rw [← angular_form_is_the_boundary_s_matrix]
  exact phase_reading_is_the_angular_phase _

theorem moving_reconstruction (beta Omega t : ℝ) :
    angularDecoder (phaseReading (readerForm beta Omega t)) = readerForm beta Omega t := by
  unfold readerForm
  rw [← angular_form_is_the_boundary_s_matrix]
  exact angular_family_reconstructed_from_one_selected_face _

theorem moving_rereading (beta Omega t : ℝ) :
    projPlus * (projPlus * readerForm beta Omega t) = projPlus * readerForm beta Omega t := by
  unfold readerForm
  rw [← angular_form_is_the_boundary_s_matrix]
  exact observing_adds_nothing _

theorem phase_relative_to_opening (beta Omega t : ℝ) :
    phaseReading (readerForm beta Omega t) =
      phaseReading (readerForm beta Omega 0) * Complex.exp (((Omega*t : ℝ) : ℂ)*Complex.I) := by
  rw [moving_reading, moving_reading, ← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem common_opening_for_any_rate (beta Omega1 Omega2 : ℝ) :
    readerForm beta Omega1 0 = readerForm beta Omega2 0 := by
  simp [initial_form]

theorem outside_angular_family_selection_is_not_injective :
    projPlus ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ) ∧ projPlus*projPlus=projPlus*1 :=
  ambient_selection_has_distinct_inputs

#print axioms opening_reconstructed
#print axioms opening_weights
#print axioms moving_reading
#print axioms moving_reconstruction
#print axioms moving_rereading
#print axioms phase_relative_to_opening
#print axioms common_opening_for_any_rate
#print axioms outside_angular_family_selection_is_not_injective
end
end ChatgptAudit.MiguelReadingR56R2
