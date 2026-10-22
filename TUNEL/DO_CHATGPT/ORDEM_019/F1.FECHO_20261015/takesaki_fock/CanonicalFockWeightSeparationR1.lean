import CanonicalFockFiniteWeightR4
/-! The actual dual weight cannot itself fill the exp(-s) trace-scaling slot.
This does not assert that no correctly perturbed trace exists. -/
set_option autoImplicit false
set_option maxHeartbeats 700000
noncomputable section
namespace F1Fecho.CanonicalFockWeightSeparation
open F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockFiniteWeight

theorem explicit_unit_finite_value : weight (averageSquare 1) = 1 := by
  simpa only [inv_one,ENNReal.ofReal_one] using weight_averageSquare 1 (by norm_num)

theorem weight_not_scaled_trace_interface :
    ¬ (∀ (s : ℝ) (A : PositiveInput),
      weight (positiveDual s A) = ENNReal.ofReal (Real.exp (-s)) * weight A) := by
  intro h
  have he := h 1 (averageSquare 1)
  rw [weight_dual_invariant,explicit_unit_finite_value,mul_one] at he
  have ht : ENNReal.ofReal (Real.exp (-1)) < 1 :=
    ENNReal.ofReal_lt_one.mpr (Real.exp_lt_one_iff.mpr (by norm_num))
  exact (ne_of_lt ht) he.symm

end F1Fecho.CanonicalFockWeightSeparation
#print axioms F1Fecho.CanonicalFockWeightSeparation.explicit_unit_finite_value
#print axioms F1Fecho.CanonicalFockWeightSeparation.weight_not_scaled_trace_interface
