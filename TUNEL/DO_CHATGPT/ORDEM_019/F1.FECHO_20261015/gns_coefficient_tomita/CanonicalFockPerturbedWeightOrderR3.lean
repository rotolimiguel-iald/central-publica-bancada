import CanonicalFockPolarRightAlgebraR4
import CanonicalFockGNSOrderR4
import CanonicalFockWeightSandwichR5
import GenericHilbertStarNormOrderR1
/-! Right perturbation norm and order in the actual Fock full-weight ideal.
The existing v393 calculation is specialized directly to avoid instance diamonds.
J and right membership remain explicit until the actual polar consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLV350.Regular (dualQuadraticIntegral antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightCompletion F1Fecho.CanonicalFockGNSOrder
open F1Fecho.CanonicalFockWeightSandwich
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
theorem scalarWeight_right_perturbed_norm (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val * (star A.val.val * A.val.val) * b.val)
      regularFockVacuum =
    ENNReal.ofReal (‖scalarGNSRepresentation (star b)
      (J.symm (scalarWeightGNSEmbedding A))‖^2) := by
  obtain ⟨hAb, he⟩ := hb.1 A
  calc
    _ = ENNReal.ofReal (‖scalarWeightGNSEmbedding ⟨A.val*b,hAb⟩‖^2) := by
      have hn := scalarWeightGNSEmbedding_norm_sq ⟨A.val*b,hAb⟩
      change ENNReal.ofReal (‖scalarWeightGNSEmbedding ⟨A.val*b,hAb⟩‖^2) =
        dualQuadraticIntegral (star (A.val.val*b.val)*(A.val.val*b.val))
          regularFockVacuum at hn
      simpa only [star_mul, mul_assoc] using hn.symm
    _ = ENNReal.ofReal (‖antiunitaryConjugate J
        (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)‖^2) :=
      congrArg (fun v : GNSHilbert => ENNReal.ofReal (‖v‖^2)) he
    _ = _ := congrArg (fun r : ℝ => ENNReal.ofReal (r^2))
      (J.norm_map
        (scalarGNSRepresentation (star b)
          (J.symm (scalarWeightGNSEmbedding A))))


theorem scalarWeight_right_perturbed_mono (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b c : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (hc : c ∈ scalarPolarRightAlgebra J)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      regularFockVacuum ≤
    dualQuadraticIntegral (star c.val * (star A.val.val*A.val.val) * c.val)
      regularFockVacuum := by
  rw [scalarWeight_right_perturbed_norm J b hb A,
    scalarWeight_right_perturbed_norm J c hc A]
  apply ENNReal.ofReal_le_ofReal
  have ho := scalarGNSRepresentation_monotone hbc
  have hp : scalarGNSRepresentation b * star (scalarGNSRepresentation b) ≤
      scalarGNSRepresentation c * star (scalarGNSRepresentation c) := by
    simpa only [map_mul,map_star] using ho
  have hn := F1Fecho.GenericHilbertStarNormOrder.star_apply_norm_sq_mono (scalarGNSRepresentation b)
    (scalarGNSRepresentation c) hp
    (J.symm (scalarWeightGNSEmbedding A))
  simpa only [map_star] using hn

end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_norm
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_mono
