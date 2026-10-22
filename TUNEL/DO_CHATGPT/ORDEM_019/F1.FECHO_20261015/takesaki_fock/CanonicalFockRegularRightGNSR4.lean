import CanonicalFockWeightCompletionR5
import RegularRightActionR2

set_option autoImplicit false
set_option maxErrors 2
set_option synthInstance.maxHeartbeats 250000
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace F1Fecho.CanonicalFockRegularRightGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockRightAverage F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockWeightInvariance
noncomputable section
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace

def regularRightCoreElement (t : ℝ) :
    (core).toStarSubalgebra :=
  ⟨regularUnitary t,regular_mem t⟩

theorem regularRightCoreElement_star (t : ℝ) :
    star (regularRightCoreElement t) = regularRightCoreElement (-t) :=
  Subtype.ext (F1Fecho.RegularCovariantCore.regular_star fockFlow t)

theorem scalarWeight_right_regular_eq
    (A : (core).toStarSubalgebra) (t : ℝ) :
    TGLV350.Regular.dualQuadraticIntegral (star (A.val * regularUnitary t) *
      (A.val * regularUnitary t)) (regularFockVacuum) =
    TGLV350.Regular.dualQuadraticIntegral (star A.val * A.val) (regularFockVacuum) :=
  F1Fecho.RegularRightAction.weight_right_regular fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum A t

def scalarRegularRightProduct
    (t : ℝ) (A : scalarWeightLeftIdeal) : scalarWeightLeftIdeal :=
  ⟨A.val * regularRightCoreElement t,by
    change TGLV350.Regular.dualQuadraticIntegral (star (A.val.val * regularUnitary t) *
      (A.val.val * regularUnitary t)) (regularFockVacuum) < ⊤
    rw [scalarWeight_right_regular_eq]
    exact A.property⟩

/-- The character acts on the outer coordinate and TGLV350.Regular.shift on the inner coordinate. -/

def regularRightAmbient (t : ℝ) :
    TGLV350.Regular.RegularHilbert (TGLV350.Regular.RegularHilbert (F)) →L[ℂ]
      TGLV350.Regular.RegularHilbert (TGLV350.Regular.RegularHilbert (F)) :=
  F1Fecho.RegularRightAction.ambient (H:=F) t

theorem characterPhase_comm (s t : ℝ) : TGLV350.Regular.characterPhase s t = TGLV350.Regular.characterPhase t s := by
  unfold TGLV350.Regular.characterPhase
  congr 1
  ring

theorem regularRightAmbient_zero : regularRightAmbient 0 = 1 := F1Fecho.RegularRightAction.ambient_zero

theorem regularRightAmbient_mul (s t : ℝ) :
    regularRightAmbient s * regularRightAmbient t = regularRightAmbient (s+t) :=
  F1Fecho.RegularRightAction.ambient_mul s t

theorem regularRightAmbient_star (t : ℝ) :
    star (regularRightAmbient t) = regularRightAmbient (-t) :=
  F1Fecho.RegularRightAction.ambient_star t

theorem scalarRegularRightOrbit_intertwines
    (t : ℝ) (A : scalarWeightLeftIdeal) :
    regularRightAmbient t (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A) =
      F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarRegularRightProduct t A) := by
  apply Lp.ext
  filter_upwards [TGLV350.Regular.characterMultiplier_ae t (TGLV350.Regular.fibre (TGLV350.Regular.shift t) (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A)),
    TGLV350.Regular.fibre_ae (TGLV350.Regular.shift t) (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A),F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_ae A,
    F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_ae (scalarRegularRightProduct t A)] with s h1 h2 h3 h4
  change TGLV350.Regular.characterMultiplier t (TGLV350.Regular.fibre (TGLV350.Regular.shift t) (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A)) s = _
  rw [h1,h2,h3,h4]
  change TGLV350.Regular.characterPhase t s • TGLV350.Regular.shift t ((↑(Real.sqrt TGLV350.Regular.dualHaarFactor) : ℂ) •
    TGLV350.Regular.dualAmbient s A.val.val (regularFockVacuum)) =
    (↑(Real.sqrt TGLV350.Regular.dualHaarFactor) : ℂ) •
      TGLV350.Regular.dualAmbient s (A.val.val * regularUnitary t) (regularFockVacuum)
  rw [map_smul,scalarOrbit_right_regular,characterPhase_comm t s,smul_comm]

theorem regularRightAmbient_preserves_GNS (t : ℝ) :
    ∀ v ∈ GNSSubspace, regularRightAmbient t v ∈ GNSSubspace := by
  have h : Set.MapsTo (regularRightAmbient t)
      ((F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear).range : Set _) ((F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear).range : Set _) := by
    rintro v ⟨A,rfl⟩
    exact ⟨scalarRegularRightProduct t A,(scalarRegularRightOrbit_intertwines t A).symm⟩
  rw [← scalarWeight_completion_eq]
  exact h.closure (regularRightAmbient t).continuous

def regularRightGNS (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  (regularRightAmbient t).restrict (regularRightAmbient_preserves_GNS t)

theorem regularRightGNS_intertwines (t : ℝ) (A : scalarWeightLeftIdeal) :
    regularRightGNS t (scalarWeightGNSEmbedding A) =
      scalarWeightGNSEmbedding (scalarRegularRightProduct t A) :=
  Subtype.ext (scalarRegularRightOrbit_intertwines t A)

theorem regularRightGNS_zero : regularRightGNS 0 = 1 := by
  ext1 x
  apply Subtype.ext
  exact congrArg (fun T => T x.val) (regularRightAmbient_zero)

theorem regularRightGNS_mul (s t : ℝ) :
    regularRightGNS s * regularRightGNS t = regularRightGNS (s+t) := by
  ext1 x
  apply Subtype.ext
  exact congrArg (fun T => T x.val) (regularRightAmbient_mul s t)

theorem regularRightGNS_star (t : ℝ) :
    star (regularRightGNS t) = regularRightGNS (-t) := by
  ext1 v
  apply ext_inner_left ℂ
  intro w
  rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
  change inner ℂ (regularRightAmbient t w.val) v.val =
    inner ℂ w.val (regularRightAmbient (-t) v.val)
  rw [← regularRightAmbient_star,ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_right]

theorem regularRightGNS_unitary (t : ℝ) :
    star (regularRightGNS t) * regularRightGNS t = 1 ∧
      regularRightGNS t * star (regularRightGNS t) = 1 := by
  simp [regularRightGNS_star,regularRightGNS_mul,regularRightGNS_zero]

#print axioms regularRightCoreElement
#print axioms regularRightCoreElement_star
#print axioms scalarWeight_right_regular_eq
#print axioms scalarRegularRightProduct
#print axioms regularRightAmbient
#print axioms characterPhase_comm
#print axioms regularRightAmbient_zero
#print axioms regularRightAmbient_mul
#print axioms regularRightAmbient_star
#print axioms scalarRegularRightOrbit_intertwines
#print axioms regularRightAmbient_preserves_GNS
#print axioms regularRightGNS
#print axioms regularRightGNS_intertwines
#print axioms regularRightGNS_zero
#print axioms regularRightGNS_mul
#print axioms regularRightGNS_star
#print axioms regularRightGNS_unitary
end
end F1Fecho.CanonicalFockRegularRightGNS
