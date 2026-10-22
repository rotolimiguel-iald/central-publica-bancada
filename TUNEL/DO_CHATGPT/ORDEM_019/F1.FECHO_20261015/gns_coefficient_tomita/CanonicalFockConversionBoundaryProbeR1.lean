import CanonicalFockRightPolarBridgeR5
import GenericPolarRightNormR1
import GenericHilbertStarNormOrderR1
import CanonicalFockGNSOrderR4

/-! UNCOMPILED DIAGNOSTIC CANDIDATE, 2026-10-16, codex-mission-memory-review.
Three boundaries only: polar norm, represented order, regular conjugation.
Use canonical instances and infer the type of the existing representation;
no replacement Star, PartialOrder, or CompleteSpace instance is installed.
The norm/order transports are proved over an abstract Hilbert space first.
No integral, spectrum, modular balance, trace, or finite projection is rebuilt.
Flushed stage timestamps measure elaboration boundaries, not proof acceptance.
Require terminal EXIT0 and the three axiom reports before consuming this file. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 3
noncomputable section
namespace F1Fecho.CanonicalFockConversionBoundaryProbeR1
open F1Fecho.CanonicalFockGNS (GNSHilbert)
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockPolarRight (scalarPolarRightAlgebra)
open TGLV350.Regular (antiunitaryConjugate)

-- Inferred aliases preserve the supplier's complete instance arguments.
private abbrev pi := F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
private abbrev lambda := F1Fecho.CanonicalFockWeightCompletion.scalarWeightGNSEmbedding

private theorem norm_from_polar_identity
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B : H →L[ℂ] H) (u v : H)
    (h : u = antiunitaryConjugate J B v) : ‖u‖ = ‖B (J.symm v)‖ :=
  (congrArg (fun z : H => ‖z‖) h).trans (J.norm_map (B (J.symm v)))

private theorem mapped_star_norm_squared_mono
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B C Bs Cs : H →L[ℂ] H) (hBs : Bs = star B) (hCs : Cs = star C)
    (hBC : B * star B ≤ C * star C) (v : H) : ‖Bs v‖^2 ≤ ‖Cs v‖^2 := by
  rw [hBs, hCs]
  exact F1Fecho.GenericHilbertStarNormOrder.star_apply_norm_sq_mono B C hBC v

#eval IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
  h.putStrLn s!"{← IO.monoMsNow} generic transports returned; norm begins"
  h.flush

/-- Same rightProduct and actual representation as the failed norm consumer.
The identity is obtained from the already supplied polar-right witness, without
re-specializing a theorem that quantifies the entire star algebra and pi. -/
theorem rightProduct_norm
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert) (b : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (A : scalarWeightLeftIdeal) :
    ‖lambda (F1Fecho.GenericPolarRightAlgebra.rightProduct
      scalarWeightLeftIdeal lambda pi J b hb.1 A)‖ =
      ‖pi (star b) (J.symm (lambda A))‖ := by
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} norm before witness inference"
      h.flush
  have raw := (hb.1 A).choose_spec
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} norm witness inferred; before expected-type conversion"
      h.flush
  have checked : lambda (F1Fecho.GenericPolarRightAlgebra.rightProduct
      scalarWeightLeftIdeal lambda pi J b hb.1 A) =
      antiunitaryConjugate J (pi (star b)) (lambda A) := raw
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} norm witness converted; before Hilbert-only transport"
      h.flush
  have hn := norm_from_polar_identity J (pi (star b)) _ (lambda A) checked
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} norm transport inferred; before exact"
      h.flush
  exact hn

#eval IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
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
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} mono represented order ready; before Hilbert-only transport"
      h.flush
  have hn := mapped_star_norm_squared_mono (pi b) (pi c) (pi (star b)) (pi (star c))
    hstarb hstarc hp (J.symm (lambda A))
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} mono transport inferred; before exact"
      h.flush
  exact hn

#eval IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
  h.putStrLn s!"{← IO.monoMsNow} order returned; conjugation begins"
  h.flush

/-- Isolate supplier inference, expected-type checking, and equality transport.
The old R3 log had no marker between its supplier have and its following rw. -/
theorem conjugate_regular_right (t : ℝ) :
    antiunitaryConjugate F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
      (F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t) =
      pi (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement (-t)) := by
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation before supplier inference"
      h.flush
  have raw := F1Fecho.CanonicalFockRightPolar.scalarTomitaPolar_conjugate_regular_right t
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation supplier inferred; before expected-type conversion"
      h.flush
  have checked :
      antiunitaryConjugate F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
        (F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t) =
        pi (star (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement t)) := raw
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation supplier converted; before core equality"
      h.flush
  have hs := F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement_star t
  have mapped := congrArg (fun b : core.toStarSubalgebra => pi b) hs
  run_tac
    IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
      h.putStrLn s!"{← IO.monoMsNow} conjugation map inferred; before exact composition"
      h.flush
  exact checked.trans mapped

#eval IO.FS.withFile "R7_conversion_probe_R1.log" .append fun h => do
  h.putStrLn s!"{← IO.monoMsNow} all boundaries returned; require terminal EXIT0 and axioms"
  h.flush

end F1Fecho.CanonicalFockConversionBoundaryProbeR1
#print axioms F1Fecho.CanonicalFockConversionBoundaryProbeR1.rightProduct_norm
#print axioms F1Fecho.CanonicalFockConversionBoundaryProbeR1.represented_right_norm_squared_mono
#print axioms F1Fecho.CanonicalFockConversionBoundaryProbeR1.conjugate_regular_right
