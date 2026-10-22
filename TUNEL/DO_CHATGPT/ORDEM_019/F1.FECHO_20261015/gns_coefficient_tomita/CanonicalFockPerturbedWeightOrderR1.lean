import CanonicalFockPolarRightAlgebraR3
import CanonicalFockGNSOrderR3
import GenericPolarRightNormR1
/-! Norm and order of right perturbations on the existing Fock full-weight
ideal. J and membership are explicit until the actual polar consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLV350.Regular (dualQuadraticIntegral)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightCompletion F1Fecho.CanonicalFockGNSOrder
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)

theorem scalarWeightGNSEmbedding_norm_sq (A : scalarWeightLeftIdeal) :
    ENNReal.ofReal (‖scalarWeightGNSEmbedding A‖^2) =
    dualQuadraticIntegral (star A.val.val*A.val.val) regularFockVacuum :=
  F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_norm_sq A

def scalarRightProduct (b : core.toStarSubalgebra) (hb : ScalarPolarRight J b)
    (A : scalarWeightLeftIdeal) : scalarWeightLeftIdeal :=
  F1Fecho.GenericPolarRightAlgebra.rightProduct
    scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J b hb A

theorem scalarWeight_right_perturbed_product (b : core.toStarSubalgebra)
    (hb : ScalarPolarRight J b) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val) regularFockVacuum =
    ENNReal.ofReal (‖scalarWeightGNSEmbedding (scalarRightProduct J b hb A)‖^2) := by
  have hn := scalarWeightGNSEmbedding_norm_sq (scalarRightProduct J b hb A)
  change ENNReal.ofReal (‖scalarWeightGNSEmbedding (scalarRightProduct J b hb A)‖^2) =
    dualQuadraticIntegral (star (A.val.val*b.val)*(A.val.val*b.val)) regularFockVacuum at hn
  simpa only [star_mul,mul_assoc] using hn.symm

theorem scalarWeight_right_perturbed_norm (b : core.toStarSubalgebra)
    (hb : b∈scalarPolarRightAlgebra J) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val) regularFockVacuum =
    ENNReal.ofReal (‖scalarGNSRepresentation (star b) (J.symm (scalarWeightGNSEmbedding A))‖^2) := by
  rw [scalarWeight_right_perturbed_product J b hb.1 A]
  exact congrArg (fun r : ℝ => ENNReal.ofReal (r^2))
    (F1Fecho.GenericPolarRightAlgebra.rightProduct_norm
      scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J b hb.1 A)

theorem scalarWeight_right_perturbed_mono (b c : core.toStarSubalgebra)
    (hb : b∈scalarPolarRightAlgebra J) (hc : c∈scalarPolarRightAlgebra J)
    (hbc : b*star b≤c*star c) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val) regularFockVacuum ≤
    dualQuadraticIntegral (star c.val*(star A.val.val*A.val.val)*c.val) regularFockVacuum := by
  rw [scalarWeight_right_perturbed_product J b hb.1 A,
    scalarWeight_right_perturbed_product J c hc.1 A]
  apply ENNReal.ofReal_le_ofReal
  have ho := scalarGNSRepresentation_monotone hbc
  have hp : scalarGNSRepresentation b*star (scalarGNSRepresentation b) ≤
      scalarGNSRepresentation c*star (scalarGNSRepresentation c) := by
    simpa only [map_mul,map_star] using ho
  exact F1Fecho.GenericPolarRightAlgebra.rightProduct_squared_norm_mono
    scalarWeightLeftIdeal scalarWeightGNSEmbedding scalarGNSRepresentation J b c hb.1 hc.1 hp A
end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeightGNSEmbedding_norm_sq
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightProduct
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_product
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_norm
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_mono
