import CanonicalFockPolarRightAlgebraR4
import CanonicalFockWeightSandwichR5
/-! The proved polar right identity commutes with the actual Fock left action.
No commutant equality or polar factor identification is assumed here. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockWeightSandwich F1Fecho.CanonicalFockRegular
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
theorem scalarPolarRight_commutes_left
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra) (hb : ScalarPolarRight J b)
    (c : core.toStarSubalgebra) :
    Commute (antiunitaryConjugate J (scalarGNSRepresentation (star b)))
      (scalarGNSRepresentation c) := by
  let R := antiunitaryConjugate J (scalarGNSRepresentation (star b))
  have hcore (A : scalarWeightLeftIdeal) :
      R (scalarGNSRepresentation c (scalarWeightGNSEmbedding A)) =
        scalarGNSRepresentation c (R (scalarWeightGNSEmbedding A)) := by
    obtain ⟨hAb,heAb⟩ := hb A
    let Ab : scalarWeightLeftIdeal := ⟨A.val*b,hAb⟩
    obtain ⟨hcAb,hecAb⟩ := hb (scalarWeightLeftProduct c A)
    have he : (⟨(scalarWeightLeftProduct c A).val*b,hcAb⟩ : scalarWeightLeftIdeal) =
        scalarWeightLeftProduct c Ab := Subtype.ext (mul_assoc c A.val b)
    calc
      _ = R (scalarWeightGNSEmbedding (scalarWeightLeftProduct c A)) :=
        congrArg R (scalarWeightGNSAction_intertwines c A)
      _ = scalarWeightGNSEmbedding ⟨(scalarWeightLeftProduct c A).val*b,hcAb⟩ :=
        hecAb.symm
      _ = scalarWeightGNSEmbedding (scalarWeightLeftProduct c Ab) :=
        congrArg scalarWeightGNSEmbedding he
      _ = scalarGNSRepresentation c (scalarWeightGNSEmbedding Ab) :=
        (scalarWeightGNSAction_intertwines c Ab).symm
      _ = _ := congrArg (scalarGNSRepresentation c) heAb
  ext1 x
  exact scalarWeightGNSEmbedding_denseRange.induction_on x
    (isClosed_eq (R.continuous.comp (scalarGNSRepresentation c).continuous)
      ((scalarGNSRepresentation c).continuous.comp R.continuous)) hcore
end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_commutes_left
