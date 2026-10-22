import UnboundedGraphTransform_v2
import TGLExt.V350PartialOperatorSquare
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open ChatgptAudit.Continuous049 TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Geometric graph data, without assuming any kernel or gap conclusion. -/
structure NormalizedGraphWitness (D : H →ₗ.[ℂ] H) where
  A : H →L[ℂ] H
  B : H →L[ℂ] H
  positiveA : 0 ≤ A
  selfadjointB : IsSelfAdjoint B
  injectiveA : Function.Injective A
  commute : A*B=B*A
  squares : A*A+B*B=1
  represents : D=boundedGraphOperator A B injectiveA

/-- The named analytic conclusion; existence for an arbitrary prescribed D is not assumed. -/
def BoundedTransformPreservesKernelAndGap
    (D : H →ₗ.[ℂ] H) (b : H →L[ℂ] H) : Prop :=
  ambientKernel D=b.ker ∧ (∀ x, ‖b x‖ ≤ ‖x‖) ∧
  ∀ γ : ℝ, 0 ≤ γ →
    (∀ u : D.domain, (u : H) ∈ (ambientKernel D)ᗮ → γ*‖(u : H)‖ ≤ ‖D u‖) →
    ∀ x ∈ b.kerᗮ, (γ/Real.sqrt (1+γ^2))*‖x‖ ≤ ‖b x‖

theorem normalized_graph_pays_contract (D : H →ₗ.[ℂ] H)
    (w : NormalizedGraphWitness D) : BoundedTransformPreservesKernelAndGap D w.B := by
  rw [BoundedTransformPreservesKernelAndGap,w.represents]
  exact ⟨graph_ambientKernel w.A w.B w.injectiveA w.commute w.squares,
    graph_transform_contraction w.A w.B w.positiveA.isSelfAdjoint w.selfadjointB w.squares,
    fun γ hγ hg => graph_transform_gap w.A w.B w.injectiveA w.positiveA.isSelfAdjoint
      w.selfadjointB w.commute w.squares γ hγ hg⟩

theorem normalized_graph_inverse_one_add_square (D : H →ₗ.[ℂ] H)
    (w : NormalizedGraphWitness D) (z : H) :
    ∃ u : (partialOperatorSquare D).domain,
      (u : H)=(w.A*w.A) z ∧ (u : H)+partialOperatorSquare D u=z := by
  have hi : Function.Injective (w.A*w.A) := w.injectiveA.comp w.injectiveA
  have hb : w.B*w.B=1-w.A*w.A := by
    exact eq_sub_iff_add_eq.mpr (by simpa only [add_comm] using w.squares)
  rw [w.represents,boundedGraph_square_eq_resolvent w.A w.B (w.A*w.A)
    w.injectiveA hi w.commute rfl hb]
  exact resolvent_graph_resolvent_equation (w.A*w.A) hi z

theorem normalized_graph_normalizer_is_sqrt (D : H →ₗ.[ℂ] H)
    (w : NormalizedGraphWitness D) : CFC.sqrt (w.A*w.A)=w.A :=
  CFC.sqrt_unique rfl w.positiveA

#print axioms normalized_graph_pays_contract
#print axioms normalized_graph_inverse_one_add_square
#print axioms normalized_graph_normalizer_is_sqrt
end ChatgptAudit.UnboundedTransform016
