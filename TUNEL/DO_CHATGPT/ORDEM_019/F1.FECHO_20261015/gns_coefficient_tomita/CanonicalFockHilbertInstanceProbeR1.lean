import CanonicalFockRightPolarBridgeR5
import GenericHilbertStarNormOrderR1

/-! UNCOMPILED R44 diagnostic, codex-fock-r6-review, 2026-10-16.
The R5 concrete transport limits do not identify the expensive instance.
This isolated probe separates the three instance equalities, generic norm
and order specialization WITHOUT pi/weight ideal, and the native witness
shape WITHOUT existential elimination. Existing three consumer targets are
untouched. These tests add no premise to a scientific certificate.
Each declaration is bounded by 400000 heartbeats, below R5's failed 1800000.
A stage marker means only that elaboration continued: errors and each axiom
report determine acceptance. No complete R7, trace or PF result is asserted.
-/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 12
noncomputable section
namespace F1Fecho.CanonicalFockHilbertInstanceProbeR1
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockPolarRight (ScalarPolarRight)
open TGLV350.Regular (antiunitaryConjugate)

-- Preserve the R5 instance stack; do not silently change the objects tested.
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
private abbrev pi : core.toStarSubalgebra →⋆ₐ[ℂ] (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
private abbrev lambda : scalarWeightLeftIdeal →ₗ[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightCompletion.scalarWeightGNSEmbedding

private def genericStar (H : Type) [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] : Star (H →L[ℂ] H) := inferInstance

private theorem norm_from_polar_identity
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B : H →L[ℂ] H) (u v : H)
    (h : u = antiunitaryConjugate (H := H) J B v) : ‖u‖ = ‖B (J.symm v)‖ :=
  (congrArg (fun z : H => ‖z‖) h).trans (J.norm_map (B (J.symm v)))

#eval IO.println "R44_INSTANCE_PROBE begin normed instance equality"
theorem normed_instance_agrees :
    (inferInstance : NormedAddCommGroup GNSHilbert) =
      Submodule.normedAddCommGroup GNSSubspace := rfl
#print axioms normed_instance_agrees

#eval IO.println "R44_INSTANCE_PROBE begin inner-product instance equality"
theorem inner_instance_agrees :
    (inferInstance : InnerProductSpace ℂ GNSHilbert) =
      Submodule.innerProductSpace GNSSubspace := rfl
#print axioms inner_instance_agrees

#eval IO.println "R44_INSTANCE_PROBE begin star instance equality"
theorem star_instance_agrees :
    (inferInstance : Star (GNSHilbert →L[ℂ] GNSHilbert)) =
      genericStar GNSHilbert := rfl
#print axioms star_instance_agrees

#eval IO.println "R44_INSTANCE_PROBE begin generic norm without pi or ideal"
theorem norm_specialization
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (B : GNSHilbert →L[ℂ] GNSHilbert) (u v : GNSHilbert)
    (h : u = antiunitaryConjugate (H := GNSHilbert) J B v) :
    ‖u‖ = ‖B (J.symm v)‖ :=
  norm_from_polar_identity (H := GNSHilbert) J B u v h
#print axioms norm_specialization

#eval IO.println "R44_INSTANCE_PROBE begin generic order without pi or ideal"
theorem order_specialization
    (B C : GNSHilbert →L[ℂ] GNSHilbert)
    (hBC : B * star B ≤ C * star C) (v : GNSHilbert) :
    ‖star B v‖ ^ 2 ≤ ‖star C v‖ ^ 2 :=
  F1Fecho.GenericHilbertStarNormOrder.star_apply_norm_sq_mono
    (H := GNSHilbert) B C hBC v
#print axioms order_specialization

#eval IO.println "R44_INSTANCE_PROBE begin native witness without elimination"
theorem native_witness_shape
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert) (b : core.toStarSubalgebra)
    (hb : ScalarPolarRight J b) (A : scalarWeightLeftIdeal) :
    ∃ h : A.val * b ∈ scalarWeightLeftIdeal,
      lambda ⟨A.val * b, h⟩ =
        antiunitaryConjugate (H := GNSHilbert) J (pi (star b)) (lambda A) := hb A
#print axioms native_witness_shape

end F1Fecho.CanonicalFockHilbertInstanceProbeR1
