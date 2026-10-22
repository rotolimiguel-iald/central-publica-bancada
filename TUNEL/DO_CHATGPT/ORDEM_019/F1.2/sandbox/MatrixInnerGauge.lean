import TGLExt.ModularFlow

set_option autoImplicit false

namespace ORDEM019.F12

open TGLExt Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n] (ρ : Matrix n n ℂ)

/-- Algebraic dense-core model of the pointwise gauge on matrix-valued functions. -/
def gauge (f : ℝ → Matrix n n ℂ) (r : ℝ) : Matrix n n ℂ :=
  modPow ρ r * f r

def ungauge (f : ℝ → Matrix n n ℂ) (r : ℝ) : Matrix n n ℂ :=
  modPow ρ (-r) * f r

def matrixRep (a : Matrix n n ℂ) (f : ℝ → Matrix n n ℂ) (r : ℝ) : Matrix n n ℂ :=
  sigma ρ (-r) a * f r

def regularShift (t : ℝ) (f : ℝ → Matrix n n ℂ) (r : ℝ) : Matrix n n ℂ :=
  f (r - t)

/-- The inner modular representation becomes constant under the same gauge. -/
theorem gauge_matrixRep_ungauge (a : Matrix n n ℂ) (f : ℝ → Matrix n n ℂ) :
    gauge ρ (matrixRep ρ a (ungauge ρ f)) = fun r => a * f r := by
  funext r
  change modPow ρ r *
    ((modPow ρ (-r) * a * modPow ρ (-(-r))) * (modPow ρ (-r) * f r)) = a * f r
  rw [neg_neg]
  calc
    modPow ρ r * ((modPow ρ (-r) * a * modPow ρ r) *
        (modPow ρ (-r) * f r))
        = (modPow ρ r * modPow ρ (-r)) * a *
            ((modPow ρ r * modPow ρ (-r)) * f r) := by simp only [mul_assoc]
    _ = a * f r := by rw [modPow_mul_neg]; simp

/-- The regular translation becomes a matrix unitary times the same shift. -/
theorem gauge_shift_ungauge (t : ℝ) (f : ℝ → Matrix n n ℂ) :
    gauge ρ (regularShift t (ungauge ρ f)) =
      fun r => modPow ρ t * regularShift t f r := by
  funext r
  change modPow ρ r * (modPow ρ (-(r - t)) * f (r - t)) =
    modPow ρ t * f (r - t)
  rw [← mul_assoc, ← modPow_add]
  congr 1
  abel

#print axioms gauge_matrixRep_ungauge
#print axioms gauge_shift_ungauge

end
end ORDEM019.F12
