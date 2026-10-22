import CanonicalFockRegularRightGNSR1
import CanonicalFockWeightSandwichR5
import RegularRightContinuityR1
/-! Actual commuting right action and regular-conjugation candidate on the
same weight GNS space. No equality with its CFC modular group is assumed. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.CanonicalFockRegularGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightSandwich
open F1Fecho.CanonicalFockRegularRightGNS
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
end F1Fecho.CanonicalFockRegularGNS
#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightGNS_commutes_left
#print axioms F1Fecho.CanonicalFockRegularGNS.regularRightGNS_strongly_continuous
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_intertwines
#print axioms F1Fecho.CanonicalFockRegularGNS.regularConjugationGNS_zero
