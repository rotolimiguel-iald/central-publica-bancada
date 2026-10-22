import Mathlib.Analysis.InnerProductSpace.Adjoint
/-! Adjoint of the restriction to a reducing closed subspace. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.ClosedSubmoduleRestriction
variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (S : Submodule ℂ E) [CompleteSpace S]
theorem adjoint_restrict (A B : E →L[ℂ] E)
    (hA : ∀ x∈S, A x∈S) (hB : ∀ x∈S, B x∈S) (hs : star A=B) :
    (A.restrict hA).adjoint=B.restrict hB := by
  ext1 x
  apply ext_inner_left ℂ
  intro y
  rw [ContinuousLinearMap.adjoint_inner_right]
  change inner ℂ (A y.val) x.val=inner ℂ y.val (B x.val)
  rw [←hs,ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
end F1Fecho.ClosedSubmoduleRestriction
#print axioms F1Fecho.ClosedSubmoduleRestriction.adjoint_restrict
