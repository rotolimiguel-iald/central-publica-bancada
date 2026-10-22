import TGLExt.RuleQuadraticResidual
open Matrix Complex
open TGLExt TGLExt.TimeGravitonMatrix TGLExt.TimeGravitonFlow
open TGLExt.RuleQuadraticResidual
namespace QuadraticIndependentReview
noncomputable section

theorem impossible_hypothesis_is_inhabited : ∃ A : M2, Eg A ≠ A := by
  refine ⟨rootPlus, ?_⟩
  rw [Eg_rootPlus]
  exact Ne.symm concrete_nonzero_modes.1

theorem impossible_control (X : M2) : 0 < residual rootPlus X := by
  apply impossible_anchor_positive
  rw [Eg_rootPlus]
  exact Ne.symm concrete_nonzero_modes.1

theorem accepted_does_not_identify_raw_state :
    residual anchor transportedRho = 0 ∧ transportedRho ≠ anchor :=
  ⟨transported_accepted, transported_is_not_anchor⟩

theorem pinching_differs_from_one_polarization :
    Eg (1 : M2) ≠ projPlus * (1 : M2) * projPlus := by
  intro h
  have hc := congrArg (fun X : M2 => X 0 0) h
  norm_num [Eg, projPlus, projMinus, genK, Matrix.mul_apply, Fin.sum_univ_two,
    Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, Matrix.one_apply] at hc

#print axioms impossible_hypothesis_is_inhabited
#print axioms impossible_control
#print axioms accepted_does_not_identify_raw_state
#print axioms pinching_differs_from_one_polarization
end
end QuadraticIndependentReview
