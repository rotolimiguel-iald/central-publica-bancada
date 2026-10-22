import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Tactic

set_option autoImplicit false
namespace ChatgptAudit.NormalizedFirstOrder016
noncomputable section

def reading (a b c r ε : ℝ) : ℝ := (a + 2*b*ε + c*ε^2)/(1+r*ε^2)

theorem reading_hasDerivAt (a b c r : ℝ) :
    HasDerivAt (reading a b c r) (2*b) 0 := by
  have hu : HasDerivAt (fun ε : ℝ => a+2*b*ε+c*ε^2) (2*b) 0 := by
    convert ((hasDerivAt_const (0:ℝ) a).add
      ((hasDerivAt_id (0:ℝ)).const_mul (2*b))).add
      (((hasDerivAt_id (0:ℝ)).pow 2).const_mul c) using 1 <;> norm_num
  have hv : HasDerivAt (fun ε : ℝ => 1+r*ε^2) 0 0 := by
    convert (hasDerivAt_const (0:ℝ) (1:ℝ)).add
      (((hasDerivAt_id (0:ℝ)).pow 2).const_mul r) using 1 <;> norm_num
  convert hu.div hv (by norm_num) using 1 <;> norm_num [reading]

theorem reading_deriv (a b c r : ℝ) : deriv (reading a b c r) 0 = 2*b :=
  (reading_hasDerivAt a b c r).deriv

theorem no_linear_term_iff (a b c r : ℝ) :
    deriv (reading a b c r) 0 = 0 ↔ b = 0 := by
  rw [reading_deriv]
  constructor
  · intro h
    linarith
  · rintro rfl
    ring

theorem normalized_bilateral_hasDerivAt (k r : ℝ) :
    HasDerivAt (fun ε : ℝ => k*ε^2/(1+r*ε^2)) 0 0 := by
  simpa [reading] using reading_hasDerivAt 0 0 k r

theorem pair_example_derivative :
    deriv (reading 0 (-(Real.sqrt 2)/3) 4 1) 0 = -(2*Real.sqrt 2)/3 := by
  rw [reading_deriv]
  ring

theorem pair_example_derivative_ne_zero :
    deriv (reading 0 (-(Real.sqrt 2)/3) 4 1) 0 ≠ 0 := by
  rw [pair_example_derivative]
  have hp : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  positivity

#print axioms reading_hasDerivAt
#print axioms reading_deriv
#print axioms no_linear_term_iff
#print axioms normalized_bilateral_hasDerivAt
#print axioms pair_example_derivative
#print axioms pair_example_derivative_ne_zero
end
end ChatgptAudit.NormalizedFirstOrder016
