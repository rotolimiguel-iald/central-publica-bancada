import CanonicalFockGNSRepresentationR6
import TGLExt.V350DualOrbitStrongLimits
/-! Positivity and bounded-strong continuity of the actual Fock weight GNS representation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockGNSOrder
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation
open scoped Topology
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
/-- Transfer bounded strong nets to the actual completed finite-ideal representation.
This does not claim closability of the involutive graph. -/
theorem scalarGNSRepresentation_tendsto_of_uniformly_bounded 
    {ι : Type*} {l : Filter ι}
    (T : ι → core.toStarSubalgebra)
    (B : core.toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 (B.val v)))
    (v : GNSHilbert) :
    Tendsto (fun i => scalarGNSRepresentation (T i) v) l
      (𝓝 (scalarGNSRepresentation B v)) := by
  apply tendsto_subtype_rng.mpr
  exact dualOrbit_tendsto_of_uniformly_bounded
    (fun i => (T i).val) B.val C hbound hT v.val

theorem scalarGNSRepresentation_nonneg 
    (B : core.toStarSubalgebra) (hB : 0 ≤ B) :
    0 ≤ scalarGNSRepresentation B := by
  have ha : 0 ≤ dualOrbitRepresentation B.val := by
    have h := OrderHomClass.monotone (dualOrbitRepresentation (H:=F)) hB
    simpa only [map_zero] using h
  rw [ContinuousLinearMap.nonneg_iff_isPositive,
    ContinuousLinearMap.isPositive_iff_complex] at ha ⊢
  intro v
  exact ha v.val

theorem scalarGNSRepresentation_monotone  :
    Monotone (scalarGNSRepresentation) := by
  intro A B h
  have hp := scalarGNSRepresentation_nonneg (B-A) (sub_nonneg.mpr h)
  rw [map_sub] at hp
  exact sub_nonneg.mp hp

end F1Fecho.CanonicalFockGNSOrder
#print axioms F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
#print axioms F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_nonneg
#print axioms F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone
