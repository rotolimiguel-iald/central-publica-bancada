import OrbitalSpatialMeasureR1

/-! A genuine spatial quarter-turn: (q0,q1,p_long) maps to (p_long,q1,-q0).
It mixes the longitudinal and transverse directions. It is not the angular
two-by-two screen reading and does not introduce a helicity fiber action. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016

def quarterTurn : Spatial ≃ₗᵢ[ℝ] Spatial where
  toFun x := WithLp.toLp 2 (WithLp.toLp 2 ![x.snd,x.fst 1],-x.fst 0)
  invFun x := WithLp.toLp 2 (WithLp.toLp 2 ![-x.snd,x.fst 1],x.fst 0)
  left_inv x := by
    apply WithLp.ofLp_injective
    apply Prod.ext
    · apply WithLp.ofLp_injective
      funext i
      fin_cases i <;> simp
    · simp
  right_inv x := by
    apply WithLp.ofLp_injective
    apply Prod.ext
    · apply WithLp.ofLp_injective
      funext i
      fin_cases i <;> simp
    · simp
  map_add' x y := by
    apply WithLp.ofLp_injective
    apply Prod.ext
    · apply WithLp.ofLp_injective
      funext i
      fin_cases i <;> simp
    · simp [add_comm]
  map_smul' c x := by
    apply WithLp.ofLp_injective
    apply Prod.ext
    · apply WithLp.ofLp_injective
      funext i
      fin_cases i <;> simp
    · simp
  norm_map' x := by
    apply (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
    simp only [WithLp.prod_norm_sq_eq_of_L2,EuclideanSpace.real_norm_sq_eq,
      Fin.sum_univ_two]
    simp [Real.norm_eq_abs,sq_abs]
    ring

theorem quarterTurn_coordinates (p : MomentumCoordinates) :
    spatialAction quarterTurn p = (![p.2,p.1 1],-p.1 0) := rfl

theorem quarterTurn_moves_longitudinal :
    spatialAction quarterTurn (0,1) = (![1,0],0) := by
  rw [quarterTurn_coordinates]
  simp

theorem quarterTurn_orbital (m : ℝ) :
    MeasureTheory.MeasurePreserving (spatialAction quarterTurn)
      (orbitalMeasure m) (orbitalMeasure m) := spatialAction_orbital quarterTurn m

theorem quarterTurn_matrix_det :
    (!![0,0,1;0,1,0;-1,0,0] : Matrix (Fin 3) (Fin 3) ℝ).det = 1 := by
  rw [Matrix.det_fin_three]
  change (0:ℝ)*1*0-0*0*0-0*0*0+0*0*(-1)+1*0*0-1*1*(-1)=1
  norm_num

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.quarterTurn
#print axioms F1Fecho.OrbitalSpatial.quarterTurn_coordinates
#print axioms F1Fecho.OrbitalSpatial.quarterTurn_moves_longitudinal
#print axioms F1Fecho.OrbitalSpatial.quarterTurn_orbital

#print axioms F1Fecho.OrbitalSpatial.quarterTurn_matrix_det
