import CanonicalFockRegularRightGNSR11
import RegularConjugationContinuityR1
import CanonicalFockWeightSandwichR5
import RegularRightContinuityR2
/-! Actual commuting right action and regular-conjugation candidate on the
same weight GNS space. No equality with its CFC modular group is assumed. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.CanonicalFockRegularGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightSandwich
open F1Fecho.CanonicalFockRegularRightGNS
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
/-- Associativity on the full scalar-weight ideal, followed by density,
proves commutation with EVERY represented left algebra element. -/
theorem regularRightGNS_commutes_left (t : ℝ)
    (B : (core).toStarSubalgebra) :
    Commute (regularRightGNS t) (scalarGNSRepresentation B) := by
  apply ContinuousLinearMap.ext
  intro z
  change regularRightGNS t (scalarGNSRepresentation B z) =
    scalarGNSRepresentation B (regularRightGNS t z)
  refine (scalarWeightGNSEmbedding_denseRange).induction ?_
    (isClosed_eq ((regularRightGNS t).continuous.comp (scalarGNSRepresentation B).continuous)
      ((scalarGNSRepresentation B).continuous.comp (regularRightGNS t).continuous)) z
  rintro _ ⟨a,rfl⟩
  have hp : scalarRegularRightProduct t (scalarWeightLeftProduct B a) =
      scalarWeightLeftProduct B (scalarRegularRightProduct t a) := by
    apply Subtype.ext
    exact mul_assoc B a.val (regularRightCoreElement t)
  calc
    _ = regularRightGNS t (scalarWeightGNSEmbedding (scalarWeightLeftProduct B a)) :=
      congrArg (regularRightGNS t) (scalarWeightGNSAction_intertwines B a)
    _ = scalarWeightGNSEmbedding (scalarRegularRightProduct t (scalarWeightLeftProduct B a)) :=
      regularRightGNS_intertwines t (scalarWeightLeftProduct B a)
    _ = scalarWeightGNSEmbedding (scalarWeightLeftProduct B (scalarRegularRightProduct t a)) :=
      congrArg (scalarWeightGNSEmbedding) hp
    _ = scalarGNSRepresentation B (scalarWeightGNSEmbedding (scalarRegularRightProduct t a)) :=
      (scalarWeightGNSAction_intertwines B (scalarRegularRightProduct t a)).symm
    _ = _ := congrArg (scalarGNSRepresentation B) (regularRightGNS_intertwines t a).symm


theorem regularRightGNS_strongly_continuous (z : GNSHilbert) :
    Continuous (fun t : ℝ => regularRightGNS t z) := by
  apply continuous_induced_rng.mpr
  exact F1Fecho.RegularRightContinuity.rightAmbient_strongly_continuous (H := F) z.val

def regularConjugationGNS (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  scalarGNSRepresentation (regularRightCoreElement t) * regularRightGNS (-t)

theorem regularConjugationGNS_intertwines (t : ℝ) (A : scalarWeightLeftIdeal) :
    regularConjugationGNS t (scalarWeightGNSEmbedding A) =
      scalarWeightGNSEmbedding (scalarWeightLeftProduct (regularRightCoreElement t)
        (scalarRegularRightProduct (-t) A)) := by
  change scalarGNSRepresentation (regularRightCoreElement t)
    (regularRightGNS (-t) (scalarWeightGNSEmbedding A)) = _
  rw [regularRightGNS_intertwines,scalarWeightGNSAction_intertwines]

theorem regularConjugationGNS_zero : regularConjugationGNS 0=1 := by
  have he : regularRightCoreElement 0 = 1 := Subtype.ext (F1Fecho.RegularCovariantCore.regular_zero fockFlow)
  simp only [regularConjugationGNS,neg_zero,regularRightGNS_zero,he,map_one,mul_one]


theorem regularRightCoreElement_mul (s t : ℝ) :
    regularRightCoreElement s * regularRightCoreElement t = regularRightCoreElement (s+t) :=
  Subtype.ext (F1Fecho.RegularCovariantCore.regular_mul fockFlow s t)

theorem regularConjugationGNS_mul (s t : ℝ) :
    regularConjugationGNS s * regularConjugationGNS t = regularConjugationGNS (s+t) := by
  unfold regularConjugationGNS
  calc
    _ = scalarGNSRepresentation (regularRightCoreElement s) *
        (regularRightGNS (-s) * scalarGNSRepresentation (regularRightCoreElement t)) * regularRightGNS (-t) := by
      simp only [mul_assoc]
    _ = (scalarGNSRepresentation (regularRightCoreElement s) *
        scalarGNSRepresentation (regularRightCoreElement t)) *
        (regularRightGNS (-s) * regularRightGNS (-t)) := by
      rw [(regularRightGNS_commutes_left (-s) (regularRightCoreElement t)).eq]
      simp only [mul_assoc]
    _ = _ := by rw [← map_mul,regularRightCoreElement_mul,regularRightGNS_mul,← neg_add]

theorem regularConjugationGNS_star (t : ℝ) :
    star (regularConjugationGNS t) = regularConjugationGNS (-t) := by
  unfold regularConjugationGNS
  rw [star_mul,regularRightGNS_star,← map_star,regularRightCoreElement_star]
  exact (regularRightGNS_commutes_left (-(-t)) (regularRightCoreElement (-t))).eq

theorem regularConjugationGNS_unitary (t : ℝ) :
    star (regularConjugationGNS t) * regularConjugationGNS t=1 ∧
    regularConjugationGNS t * star (regularConjugationGNS t)=1 := by
  rw [regularConjugationGNS_star,regularConjugationGNS_mul,regularConjugationGNS_mul]
  simp only [neg_add_cancel,add_neg_cancel,regularConjugationGNS_zero,and_self]



theorem regularConjugationGNS_ambient (t : ℝ) (z : GNSHilbert) :
    (regularConjugationGNS t z).val =
      TGLV350.Regular.fibre (TGLV350.Regular.fibre
        (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)) z.val := by
  change (TGLV350.Regular.dualOrbitRepresentation (regularUnitary t) *
    F1Fecho.RegularRightAction.ambient (H:=F) (-t)) z.val = _
  exact congrArg (fun T => T z.val)
    (F1Fecho.RegularConjugationAmbient.regular_conjugation_is_base_fibre fockFlow t)

theorem regularConjugationGNS_strongly_continuous (z : GNSHilbert) :
    Continuous (fun t : ℝ => regularConjugationGNS t z) := by
  apply continuous_induced_rng.mpr
  exact (F1Fecho.RegularConjugationAmbient.base_fibre_strongly_continuous fockFlow z.val).congr
    (fun t => (regularConjugationGNS_ambient t z).symm)

end F1Fecho.CanonicalFockRegularGNS
#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightGNS_commutes_left
#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightGNS_strongly_continuous
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_intertwines
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_zero

#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightCoreElement_mul
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_mul
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_star
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_unitary

#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_ambient
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_strongly_continuous
