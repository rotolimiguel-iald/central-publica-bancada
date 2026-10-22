import CanonicalFockRightPolarBridgeR5
import GenericPolarRightNormR1
import GenericHilbertStarNormOrderR1
import CanonicalFockGNSOrderR4

/-! UNCOMPILED DIAGNOSTIC CANDIDATE R4, 2026-10-16,
codex-fock-r6-review. R3 reached the concrete norm proof and stopped inside
its obtain/rcases line. Move existential elimination into a small generic
Hilbert theorem indexed only by a proposition; specialize with one exact
application to the SAME native ScalarPolarRight witness. This removes
concrete tactic case analysis and generic star-algebra/rightProduct inference.
The three public targets, all hypotheses, and the R3 local instances remain.
No trace, finite projection or complete R7 certificate is asserted.
Require terminal EXIT0 and all three axiom reports before consumption. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 3
noncomputable section
namespace F1Fecho.CanonicalFockConversionBoundaryProbeR4
open F1Fecho.CanonicalFockGNS (GNSHilbert)
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockPolarRight (ScalarPolarRight)
open TGLV350.Regular (antiunitaryConjugate)

-- Match the concrete aliases used by the green Fock/order suppliers.
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
private abbrev pi : core.toStarSubalgebra →⋆ₐ[ℂ] (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
private abbrev lambda : scalarWeightLeftIdeal →ₗ[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightCompletion.scalarWeightGNSEmbedding

private theorem norm_from_polar_identity
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B : H →L[ℂ] H) (u v : H)
    (h : u = antiunitaryConjugate (H := H) J B v) : ‖u‖ = ‖B (J.symm v)‖ :=
  (congrArg (fun z : H => ‖z‖) h).trans (J.norm_map (B (J.symm v)))

/-- Eliminate a proof-indexed existential before any concrete Fock specialization.
The witness proposition is abstract, so no concrete ideal/subtype is analyzed. -/
private theorem exists_norm_from_polar_identity
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {P : Prop} (u : P → H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B : H →L[ℂ] H) (v : H)
    (h : ∃ p : P, u p = antiunitaryConjugate (H := H) J B v) :
    ∃ p : P, ‖u p‖ = ‖B (J.symm v)‖ :=
  Exists.elim h (fun p hp =>
    Exists.intro p (norm_from_polar_identity (H := H) J B (u p) v hp))

private theorem mapped_star_norm_squared_mono
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B C Bs Cs : H →L[ℂ] H) (hBs : Bs = star B) (hCs : Cs = star C)
    (hBC : B * star B ≤ C * star C) (v : H) : ‖Bs v‖^2 ≤ ‖Cs v‖^2 := by
  rw [hBs, hCs]
  exact F1Fecho.GenericHilbertStarNormOrder.star_apply_norm_sq_mono (H := H) B C hBC v

#eval IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
  h.putStrLn s!"{← IO.monoMsNow} generic transports returned; norm begins"
  h.flush

/-- The native polar-right identity provides a genuine product in the full
weight ideal and its norm. The integral consumer can set P := ⟨A.val*b,h⟩;
its value is A.val*b by rfl. No generic rightProduct appears in this statement.
From the original algebra membership hb, obtain this native premise through
(scalarPolarRightAlgebra_mem_iff J b).mp hb, taking its first component. -/
theorem exists_rightProduct_norm
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert) (b : core.toStarSubalgebra)
    (hb : ScalarPolarRight J b) (A : scalarWeightLeftIdeal) :
    ∃ h : A.val * b ∈ scalarWeightLeftIdeal,
      ‖lambda ⟨A.val * b, h⟩‖ = ‖pi (star b) (J.symm (lambda A))‖ := by
  run_tac
    IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} norm before typed generic existential specialization"
      h.flush
  exact exists_norm_from_polar_identity (H := GNSHilbert)
    (P := A.val * b ∈ scalarWeightLeftIdeal)
    (fun hmem => lambda ⟨A.val * b, hmem⟩)
    J (pi (star b)) (lambda A) (hb A)

#eval IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
  h.putStrLn s!"{← IO.monoMsNow} norm returned; represented order begins"
  h.flush

/-- The same b b* order orientation. Membership is needed by the integral
identity, not by this already represented Hilbert norm inequality. -/
theorem represented_right_norm_squared_mono
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert) (b c : core.toStarSubalgebra)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal) :
    ‖pi (star b) (J.symm (lambda A))‖^2 ≤
      ‖pi (star c) (J.symm (lambda A))‖^2 := by
  have ho := F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone hbc
  have hp : pi b * star (pi b) ≤ pi c * star (pi c) := by
    simpa only [map_mul, map_star] using ho
  have hstarb : pi (star b) = star (pi b) := map_star pi b
  have hstarc : pi (star c) = star (pi c) := map_star pi c
  run_tac
    IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} mono represented order ready; before Hilbert-only transport"
      h.flush
  have hn := mapped_star_norm_squared_mono (H := GNSHilbert) (pi b) (pi c) (pi (star b)) (pi (star c))
    hstarb hstarc hp (J.symm (lambda A))
  run_tac
    IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} mono transport inferred; before exact"
      h.flush
  exact hn

#eval IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
  h.putStrLn s!"{← IO.monoMsNow} order returned; conjugation begins"
  h.flush

/-- Isolate supplier inference, expected-type checking, and equality transport.
The old R3 log had no marker between its supplier have and its following rw. -/
theorem conjugate_regular_right (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
      (F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t) =
      pi (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement (-t)) := by
  run_tac
    IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation before supplier inference"
      h.flush
  have raw := F1Fecho.CanonicalFockRightPolar.scalarTomitaPolar_conjugate_regular_right t
  run_tac
    IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation supplier inferred; before expected-type conversion"
      h.flush
  have checked :
      antiunitaryConjugate (H := GNSHilbert) F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
        (F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t) =
        pi (star (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement t)) := raw
  run_tac
    IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation supplier converted; before core equality"
      h.flush
  have hs := F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement_star t
  have mapped := congrArg (fun b : core.toStarSubalgebra => pi b) hs
  run_tac
    IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation map inferred; before exact composition"
      h.flush
  exact checked.trans mapped

#eval IO.FS.withFile "R7_conversion_probe_R4.log" .append fun h => do
  h.putStrLn s!"{← IO.monoMsNow} all boundaries returned; require terminal EXIT0 and axioms"
  h.flush

end F1Fecho.CanonicalFockConversionBoundaryProbeR4
#print axioms F1Fecho.CanonicalFockConversionBoundaryProbeR4.exists_rightProduct_norm
#print axioms F1Fecho.CanonicalFockConversionBoundaryProbeR4.represented_right_norm_squared_mono
#print axioms F1Fecho.CanonicalFockConversionBoundaryProbeR4.conjugate_regular_right
