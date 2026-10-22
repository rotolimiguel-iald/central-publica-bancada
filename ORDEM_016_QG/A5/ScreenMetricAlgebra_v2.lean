import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring

set_option autoImplicit false
namespace ChatgptAudit.ScreenMetric016

def screenMetric (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![0,0,-a,-a]

theorem screenMetric_zero : screenMetric 0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [screenMetric,Matrix.diagonal]

theorem screenMetric_symmetric (a : ℝ) : (screenMetric a)ᵀ=screenMetric a := by
  simp [screenMetric]

theorem screenMetric_gauge (a : ℝ) : (screenMetric a).mulVec ![1,1,0,0]=0 := by
  ext i
  rw [screenMetric,Matrix.mulVec_diagonal]
  fin_cases i <;> simp

theorem screenMetric_area (a : ℝ) :
    -((screenMetric a) 2 2+(screenMetric a) 3 3)/2=a := by
  simp only [screenMetric,Matrix.diagonal_apply_eq,Matrix.cons_val_succ,Matrix.cons_val_zero]
  ring

#print axioms screenMetric_zero
#print axioms screenMetric_symmetric
#print axioms screenMetric_gauge
#print axioms screenMetric_area
end ChatgptAudit.ScreenMetric016
