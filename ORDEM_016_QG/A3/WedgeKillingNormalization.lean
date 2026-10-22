import WedgeDraggedFrame_v3

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace ChatgptAudit.WignerGeometry016
open TGLExt TGLExt.ContratoQGv31 TGL.SpecificAQFT Matrix

/-- Calibration is supplied by the reference point, not inferred from W,R. -/
def referenceRate (N : KillingNormalization) : ℝ :=
  1 / Real.sqrt (N.point 1 ^ 2 - N.point 0 ^ 2)

theorem reference_radius_positive (N : KillingNormalization) :
    0 < Real.sqrt (N.point 1 ^ 2 - N.point 0 ^ 2) := by
  have h : |N.point 0| < N.point 1 := N.point_in_wedge
  obtain ⟨h1,h2⟩ := abs_lt.mp h
  apply Real.sqrt_pos.mpr
  nlinarith

theorem referenceRate_positive (N : KillingNormalization) : 0 < referenceRate N :=
  one_div_pos.mpr (reference_radius_positive N)

theorem referenceRate_unit (N : KillingNormalization) :
    minkowskiSq (killingField (referenceRate N) N.point) = 1 := by
  have hr := reference_radius_positive N
  have hq : Real.sqrt (N.point 1 ^ 2 - N.point 0 ^ 2) ^ 2 =
      N.point 1 ^ 2 - N.point 0 ^ 2 := Real.sq_sqrt (le_of_lt (Real.sqrt_pos.mp hr))
  simp [minkowskiSq, killingField, referenceRate]
  field_simp
  nlinarith [hq]

theorem wedge_boost_hasDerivAt (k s : ℝ) (x : Fin 4 → ℝ) :
    HasDerivAt (fun t => wedgeBoostMap (k*t) x)
      (killingField k (wedgeBoostMap (k*s) x)) s := by
  apply hasDerivAt_pi.mpr
  intro i
  have hc := (Real.hasDerivAt_cosh (k*s)).comp s ((hasDerivAt_id s).const_mul k)
  have hs := (Real.hasDerivAt_sinh (k*s)).comp s ((hasDerivAt_id s).const_mul k)
  fin_cases i
  · convert (hc.mul_const (x 0)).add (hs.mul_const (x 1)) using 1 <;>
      simp [wedgeBoostMap, killingField, boostMat, Matrix.mulVec, dotProduct,
        Fin.sum_univ_four] <;> ring
  · convert (hs.mul_const (x 0)).add (hc.mul_const (x 1)) using 1 <;>
      simp [wedgeBoostMap, killingField, boostMat, Matrix.mulVec, dotProduct,
        Fin.sum_univ_four] <;> ring
  · simpa [wedgeBoostMap, killingField, boostMat, Matrix.mulVec, dotProduct,
      Fin.sum_univ_four] using hasDerivAt_const s (x 2)
  · simpa [wedgeBoostMap, killingField, boostMat, Matrix.mulVec, dotProduct,
      Fin.sum_univ_four] using hasDerivAt_const s (x 3)

/-- Only geometric fields of H2: no vacuum, algebra or modular identification is supplied. -/
theorem geometric_fields_for_reference (N : KillingNormalization) :
    0 < referenceRate N ∧
    minkowskiSq (killingField (referenceRate N) N.point)=1 ∧
    (∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => wedgeFrame x i j) rightWedge) ∧
    (∀ x ∈ rightWedge, IsUnit (wedgeFrame x).det) ∧
    (∀ s x, wedgeFrame (wedgeBoostMap s x)=boostMat s*wedgeFrame x) ∧
    (∀ x ∈ rightWedge, ∃ c : ℝ, 0<c ∧
      (fun i => wedgeFrame x i 0)=c • killingField (referenceRate N) x) := by
  exact ⟨referenceRate_positive N, referenceRate_unit N,
    fun i j => (wedgeFrame_smooth i j).contDiffOn,
    wedgeFrame_det_unit, wedgeFrame_dragged,
    fun x _ => wedgeFrame_fiducial _ (referenceRate_positive N) x⟩

#print axioms reference_radius_positive
#print axioms referenceRate_positive
#print axioms referenceRate_unit
#print axioms wedge_boost_hasDerivAt
#print axioms geometric_fields_for_reference
end ChatgptAudit.WignerGeometry016
