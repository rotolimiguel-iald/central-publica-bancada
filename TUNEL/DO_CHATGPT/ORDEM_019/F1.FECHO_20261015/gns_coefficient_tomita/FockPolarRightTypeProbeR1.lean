import CanonicalFockGNSRepresentationR6
import CanonicalFockWeightCompletionR5
import TGLExt.V350AntiunitaryPositiveConjugation
import Mathlib.Algebra.Star.Subalgebra
/-! Algebraic closure on the actual full-weight Fock domain. Reuses the
generic proof body at the concrete types to avoid an instance-diamond conversion.
J remains explicit until the actual polar consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockRegular
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
/-- The actual polar right identity on the existing full weight domain. -/
def ScalarPolarRight  (b : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) : Prop :=
  ∀ A : scalarWeightLeftIdeal, ∃ h : A.val*b ∈ scalarWeightLeftIdeal,
    scalarWeightGNSEmbedding ⟨A.val*b,h⟩ =
      antiunitaryConjugate (H := GNSHilbert) J
        (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)


end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.ScalarPolarRight
