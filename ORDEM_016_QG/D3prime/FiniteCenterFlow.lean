import ConjugatedFormScope_v2

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix TGLExt
namespace ORDEM016.D3prime

theorem angular_flow_inverse (θ : ℝ) : angFamily θ*angFamily (-θ)=1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [angFamily,genK,Matrix.mul_apply,Fin.sum_univ_two,Real.cos_neg,Real.sin_neg,
      Complex.ext_iff] <;>
    (repeat' constructor) <;> nlinarith [Real.cos_sq_add_sin_sq θ]

theorem finite_center_angular_fixed (θ : ℝ) :
    angFamily θ*finiteCenter*angFamily (-θ)=finiteCenter := by
  rw [finite_center_commutes_angular,mul_assoc,angular_flow_inverse,mul_one]

/-- The counterexample flow is unitary, not an arbitrary invertible matrix. -/
theorem phase_flow_adjoint (t : ℝ) : (phaseFlow t).conjTranspose=phaseFlow (-t) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [phaseFlow,Matrix.conjTranspose_apply,←Complex.exp_conj]

theorem phase_flow_unitary (t : ℝ) : phaseFlow t*(phaseFlow t).conjTranspose=1 := by
  rw [phase_flow_adjoint,phase_flow_inverse]

#print axioms angular_flow_inverse
#print axioms finite_center_angular_fixed
#print axioms phase_flow_adjoint
#print axioms phase_flow_unitary
end ORDEM016.D3prime
