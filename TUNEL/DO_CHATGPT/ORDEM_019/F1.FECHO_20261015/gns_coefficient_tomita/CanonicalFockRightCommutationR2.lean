import CanonicalFockPolarRightAlgebraR6
import GenericPolarRightCommutationR2

/-! Specialize the existing dense-range commutation theorem to the actual
full-weight Fock ideal. No separate concrete replay of its long proof is needed.
The named right identity is consumed, not assumed for every element. -/
set_option autoImplicit false
set_option Elab.async false
set_option maxHeartbeats 400000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLV350.Regular (antiunitaryConjugate)
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockWeightSandwich F1Fecho.CanonicalFockRegular
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace

theorem scalarPolarRight_commutes_left
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra) (hb : ScalarPolarRight J b)
    (c : core.toStarSubalgebra) :
    Commute (antiunitaryConjugate (H := GNSHilbert) J (scalarGNSRepresentation (star b)))
      (scalarGNSRepresentation c) := by
  exact F1Fecho.GenericPolarRightAlgebra.commutes_left_of_right_identity
    scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
    scalarWeightGNSEmbedding_denseRange
    (fun c A => ⟨(scalarWeightLeftProduct c A).property,
      (scalarWeightGNSAction_intertwines c A).symm⟩) b hb c

end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_commutes_left
