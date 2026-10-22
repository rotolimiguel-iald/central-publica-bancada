import ContratoQG_v31_Minimal

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace ChatgptAudit.WignerGeometry016
open TGLExt TGLExt.ContratoQGv31 TGL.SpecificAQFT Matrix

/-- A polynomial regional frame. It does not choose the physical pair W,R. -/
def wedgeFrame (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![x 1, x 0, 0, 0; x 0, x 1, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1]

theorem wedgeFrame_smooth (i j : Fin 4) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => wedgeFrame x i j) := by
  fin_cases i <;> fin_cases j <;> simp only [wedgeFrame, Matrix.of_apply,
    Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_succ] <;> fun_prop

theorem wedgeFrame_det (x : Fin 4 → ℝ) :
    (wedgeFrame x).det = x 1 ^ 2 - x 0 ^ 2 := by
  simp [wedgeFrame, Matrix.det_fin_four]
  <;> ring

theorem wedgeFrame_det_pos (x : Fin 4 → ℝ) (hx : x ∈ rightWedge) :
    0 < (wedgeFrame x).det := by
  rw [wedgeFrame_det]
  have h : |x 0| < x 1 := hx
  obtain ⟨h1,h2⟩ := abs_lt.mp h
  nlinarith

theorem wedgeFrame_det_unit (x : Fin 4 → ℝ) (hx : x ∈ rightWedge) :
    IsUnit (wedgeFrame x).det := isUnit_iff_ne_zero.mpr (ne_of_gt (wedgeFrame_det_pos x hx))

theorem wedgeFrame_dragged (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeFrame (wedgeBoostMap s x) = boostMat s * wedgeFrame x := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [wedgeFrame, wedgeBoostMap, boostMat, Matrix.mul_apply, Matrix.mulVec,
      dotProduct, Fin.sum_univ_four] <;> ring

theorem wedgeFrame_fiducial (k : ℝ) (hk : 0 < k) (x : Fin 4 → ℝ) :
    ∃ c : ℝ, 0 < c ∧ (fun i => wedgeFrame x i 0) = c • killingField k x := by
  refine ⟨k⁻¹, inv_pos.mpr hk, ?_⟩
  funext i
  fin_cases i <;> simp [wedgeFrame, killingField, hk.ne', mul_assoc]

theorem killing_boost_covariant (k s : ℝ) (x : Fin 4 → ℝ) :
    killingField k (wedgeBoostMap s x) = wedgeBoostMap s (killingField k x) := by
  funext i
  fin_cases i <;> simp [killingField, wedgeBoostMap, boostMat,
    Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> ring

#print axioms wedgeFrame_smooth
#print axioms wedgeFrame_det
#print axioms wedgeFrame_det_pos
#print axioms wedgeFrame_det_unit
#print axioms wedgeFrame_dragged
#print axioms wedgeFrame_fiducial
#print axioms killing_boost_covariant
end ChatgptAudit.WignerGeometry016
