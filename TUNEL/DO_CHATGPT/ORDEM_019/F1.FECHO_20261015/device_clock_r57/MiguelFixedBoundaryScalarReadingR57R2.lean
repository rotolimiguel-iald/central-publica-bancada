import TGLExt.SelectionAngleReconstruction

/-!
R57 candidate: fixed Miguel boundary with an independently supplied complex signal.
The source patent multiplies the output by G_OH. This file preserves that scalar
placement: A_beta(z)=z*S(thetaMiguel beta), not S(thetaMiguel beta+omega*t).
It constructs an encoder, reader and decoder for this family, preserving the
reflection/transmission ratio. It does not prove that any GKLS observable equals
the prescribed G_OH, determine a physical clock, or derive the amplitude tanh.
No identification of J with P, no H3 or global device realization is asserted.
-/

set_option autoImplicit false
namespace ChatgptAudit.MiguelFixedBoundaryR57R2
open TGLExt ChatgptAudit.SelectionAngle Matrix Complex
noncomputable section

def scalarBoundary (beta : ℝ) (z : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  z • Smat (thetaMiguel beta)

def fixedDecoder (beta : ℝ) (w : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (w * Complex.exp (-((thetaMiguel beta : ℝ) : ℂ) * Complex.I)) •
    Smat (thetaMiguel beta)

theorem phaseReading_smul (z : ℂ) (A : Matrix (Fin 2) (Fin 2) ℂ) :
    phaseReading (z • A) = z * phaseReading A := by
  unfold phaseReading
  rw [Matrix.mul_smul]
  simp only [Matrix.smul_apply, smul_eq_mul]
  ring

theorem phaseReading_smat (theta : ℝ) :
    phaseReading (Smat theta) = Complex.exp ((theta : ℂ) * Complex.I) := by
  rw [← angular_form_is_the_boundary_s_matrix]
  exact phase_reading_is_the_angular_phase theta

theorem fixed_boundary_reads_scalar (beta : ℝ) (z : ℂ) :
    phaseReading (scalarBoundary beta z) =
      z * Complex.exp (((thetaMiguel beta : ℝ) : ℂ) * Complex.I) := by
  rw [scalarBoundary, phaseReading_smul, phaseReading_smat]

theorem fixed_boundary_reconstructed (beta : ℝ) (z : ℂ) :
    fixedDecoder beta (phaseReading (scalarBoundary beta z)) = scalarBoundary beta z := by
  rw [fixed_boundary_reads_scalar]
  unfold fixedDecoder scalarBoundary
  rw [mul_assoc, the_two_readings_are_conjugate, mul_one]

theorem fixed_boundary_rereading (beta : ℝ) (z : ℂ) :
    projPlus * (projPlus * scalarBoundary beta z) = projPlus * scalarBoundary beta z := by
  unfold scalarBoundary
  simp only [Matrix.mul_smul]
  rw [← angular_form_is_the_boundary_s_matrix]
  rw [observing_adds_nothing]

theorem fixed_boundary_reflected_weight {beta : ℝ} (h0 : 0 ≤ beta) (h1 : beta ≤ 1) (z : ℂ) :
    Complex.normSq ((scalarBoundary beta z).mulVec e1 1) = Complex.normSq z * beta := by
  simp only [scalarBoundary, Matrix.smul_mulVec, Pi.smul_apply, smul_eq_mul,
    Complex.normSq_mul]
  rw [normSq_reflection, sin_thetaMiguel h0 h1, Real.sq_sqrt h0]

theorem fixed_boundary_transmitted_weight {beta : ℝ} (h0 : 0 ≤ beta) (h1 : beta ≤ 1) (z : ℂ) :
    Complex.normSq ((scalarBoundary beta z).mulVec e1 0) = Complex.normSq z * (1-beta) := by
  simp only [scalarBoundary, Matrix.smul_mulVec, Pi.smul_apply, smul_eq_mul,
    Complex.normSq_mul]
  rw [normSq_transmission]
  have h := Real.sin_sq_add_cos_sq (thetaMiguel beta)
  rw [sin_thetaMiguel h0 h1, Real.sq_sqrt h0] at h
  have hcos : Real.cos (thetaMiguel beta) ^ 2 = 1-beta := by linarith
  rw [hcos]

theorem zero_signal_is_zero (beta : ℝ) : scalarBoundary beta 0 = 0 := by
  simp [scalarBoundary]

#print axioms fixed_boundary_reads_scalar
#print axioms fixed_boundary_reconstructed
#print axioms fixed_boundary_rereading
#print axioms fixed_boundary_reflected_weight
#print axioms fixed_boundary_transmitted_weight
#print axioms zero_signal_is_zero
end
end ChatgptAudit.MiguelFixedBoundaryR57R2
