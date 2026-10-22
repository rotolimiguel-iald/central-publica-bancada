import WedgeDraggedFrame_v6

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.WignerGeometry016.ExistingCalibration
open TGLExt TGLExt.ContratoQGv31 TGL.SpecificAQFT Matrix

/- Existing proofs copied unchanged from ContratoQG_v31_Teoremas.
Only the namespace/import context changes for isolated compilation.
This is reuse, not a new derivation of the calibration. -/
def refRadius (N : KillingNormalization) : ℝ := Real.sqrt (N.point 1 ^ 2 - N.point 0 ^ 2)

theorem refRadius_pos (N : KillingNormalization) : 0 < refRadius N := by
  have hx : |N.point 0| < N.point 1 := N.point_in_wedge
  obtain ⟨h1, h2⟩ := abs_lt.mp hx
  unfold refRadius
  apply Real.sqrt_pos.mpr
  nlinarith

theorem observer_unit_of_index (N' : KillingNormalization) :
    minkowskiSq (killingField (1 / refRadius N') N'.point) = 1 := by
  have hr := refRadius_pos N'
  have hsq : refRadius N' ^ 2 = N'.point 1 ^ 2 - N'.point 0 ^ 2 := by
    unfold refRadius
    have hx : |N'.point 0| < N'.point 1 := N'.point_in_wedge
    obtain ⟨h1, h2⟩ := abs_lt.mp hx
    rw [Real.sq_sqrt (by nlinarith)]
  simp [minkowskiSq, killingField]
  field_simp
  linarith [hsq]


/-- The geometric fields are assembled from existing suppliers for any supplied N. -/
theorem geometric_fields_reused (N : KillingNormalization) :
    0 < 1 / refRadius N ∧
    minkowskiSq (killingField (1 / refRadius N) N.point) = 1 ∧
    (∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => wedgeFrame x i j) rightWedge) ∧
    (∀ x ∈ rightWedge, IsUnit (wedgeFrame x).det) ∧
    (∀ s x, x ∈ rightWedge →
      wedgeFrame (wedgeBoostMap s x) = boostMat s * wedgeFrame x) ∧
    (∀ x ∈ rightWedge, ∃ c : ℝ, 0 < c ∧
      (fun i => wedgeFrame x i 0) = c • killingField (1 / refRadius N) x) := by
  have hk : 0 < 1 / refRadius N := one_div_pos.mpr (refRadius_pos N)
  exact ⟨hk, observer_unit_of_index N,
    fun i j => (wedgeFrame_smooth i j).contDiffOn,
    wedgeFrame_det_unit, fun s x _ => wedgeFrame_dragged s x,
    fun x _ => wedgeFrame_fiducial _ hk x⟩

#print axioms refRadius_pos
#print axioms observer_unit_of_index
#print axioms geometric_fields_reused
end ChatgptAudit.WignerGeometry016.ExistingCalibration
