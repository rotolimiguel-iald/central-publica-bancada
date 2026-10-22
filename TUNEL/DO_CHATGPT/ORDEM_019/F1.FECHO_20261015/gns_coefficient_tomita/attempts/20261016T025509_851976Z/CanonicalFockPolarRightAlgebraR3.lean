import CanonicalFockGNSRepresentationR6
import CanonicalFockWeightCompletionR5
import GenericPolarRightAlgebraR2
/-! Specialize the proved abstract polar-right algebra to the existing full
weight domain and actual Fock GNS representation. The explicit J still needs
its polar consumer; no concrete member is assumed by these closure laws. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightCompletion
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
abbrev ScalarPolarRight := F1Fecho.GenericPolarRightAlgebra.ScalarPolarRight
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
abbrev scalarPolarRight_zero := F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_zero
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
abbrev scalarPolarRight_one := F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_one
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
abbrev scalarPolarRight_add := F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_add
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
abbrev scalarPolarRight_smul := F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_smul
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
abbrev scalarPolarRight_mul := F1Fecho.GenericPolarRightAlgebra.scalarPolarRight_mul
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
abbrev scalarPolarRightAlgebra := F1Fecho.GenericPolarRightAlgebra.scalarPolarRightAlgebra
  (H := GNSHilbert) (𝒜 := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)
  scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J
end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.ScalarPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_zero
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_one
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_add
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_smul
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_mul
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRightAlgebra
