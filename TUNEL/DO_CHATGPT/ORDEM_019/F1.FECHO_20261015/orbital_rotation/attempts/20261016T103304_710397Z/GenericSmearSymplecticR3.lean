import Mathlib.Analysis.InnerProductSpace.LinearMap

/-! Real symplectic bilinearity of a complex-linear continuous test map. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericSmearSymplectic
variable {X H : Type} [NormedAddCommGroup X] [NormedSpace ℂ X]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H]

def pairing (T : X →L[ℂ] H) : X →ₗ[ℝ] X →ₗ[ℝ] ℝ where
  toFun f :=
    { toFun := fun g => (inner ℂ (T f) (T g)).im
      map_add' := by intro g h; simp only [map_add,inner_add_right,Complex.add_im]
      map_smul' := by
        intro r g
        change (inner ℂ (T f) (T (r • g))).im = r * (inner ℂ (T f) (T g)).im
        have ht : T (r • g) = (r : ℂ) • T g := by rw [← Complex.coe_smul,map_smul]
        rw [ht,inner_smul_right]
        simp [Complex.mul_im] }
  map_add' := by
    intro f g
    ext h
    change (inner ℂ (T (f+g)) (T h)).im =
      (inner ℂ (T f) (T h)).im + (inner ℂ (T g) (T h)).im
    simp only [map_add,inner_add_left,Complex.add_im]
  map_smul' := by
    intro r f
    ext g
    change (inner ℂ (T (r • f)) (T g)).im = r * (inner ℂ (T f) (T g)).im
    have ht : T (r • f) = (r : ℂ) • T f := by rw [← Complex.coe_smul,map_smul]
    rw [ht,inner_smul_left]
    simp [Complex.mul_im]

end F1Fecho.GenericSmearSymplectic
#print axioms F1Fecho.GenericSmearSymplectic.pairing
