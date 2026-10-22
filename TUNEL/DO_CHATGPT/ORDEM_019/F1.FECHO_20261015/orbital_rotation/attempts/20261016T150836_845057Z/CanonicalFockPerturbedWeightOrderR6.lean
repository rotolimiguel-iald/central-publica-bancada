import CanonicalFockPolarRightCutoffsR13
import GenericPolarRightNormR1
import CanonicalFockGNSOrderR4
import CanonicalFockWeightSandwichR5

/-! UNCOMPILED CANDIDATE, 2026-10-16, codex-mission-memory-review.
R6 replaces the timed-out value rewrite with typed congruence and composes
the generic order supplier before specializing its result to the Fock carrier.
R5 separates the actual full-weight norm conversion into typed steps and
uses the existing generic polar-right norm/order suppliers. The public
premises and targets are those of R4. The star-product calculation is first
proved at an abstract star ring, before specialization to the large carrier.
Direct flushed stage writes locate progress; a marker is not proof acceptance.
The full scaled trace and finite projection remain separate obligations. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open F1Fecho.CanonicalFockGNS (GNSHilbert)
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeight (regularFockVacuum)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockWeightCompletion (scalarWeightGNSEmbedding)
open F1Fecho.CanonicalFockGNSRepresentation (scalarGNSRepresentation)
open TGLV350.Regular (dualQuadraticIntegral)

#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_R6 generic squared norm transport start"
  h.flush

/-- Normalize the output of the existing generic order theorem while the
carrier and ideal are abstract, before supplying the large Fock instances. -/
private theorem represented_right_norm_squared_mono
    {𝒜 : Type*} {H : Type}
    [Ring 𝒜] [Algebra ℂ 𝒜] [StarRing 𝒜] [StarModule ℂ 𝒜]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : Submodule ℂ 𝒜) (Λ : N →ₗ[ℂ] H)
    (π : 𝒜 →⋆ₐ[ℂ] (H →L[ℂ] H)) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (b c : 𝒜)
    (hb : F1Fecho.GenericPolarRightAlgebra.ScalarPolarRight N Λ π J b)
    (hc : F1Fecho.GenericPolarRightAlgebra.ScalarPolarRight N Λ π J c)
    (hbc : π b*star (π b) ≤ π c*star (π c)) (a : N) :
    ‖π (star b) (J.symm (Λ a))‖^2 ≤ ‖π (star c) (J.symm (Λ a))‖^2 := by
  have hn := F1Fecho.GenericPolarRightAlgebra.rightProduct_squared_norm_mono
    (𝒜 := 𝒜) (H := H) N Λ π J b c hb hc hbc a
  rw [F1Fecho.GenericPolarRightAlgebra.rightProduct_norm,
    F1Fecho.GenericPolarRightAlgebra.rightProduct_norm] at hn
  exact hn

#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_R6 generic transport returned; concrete declarations start"
  h.flush

local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)

private abbrev fockPi : core.toStarSubalgebra →⋆ₐ[ℂ] (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
private abbrev fockLambda : scalarWeightLeftIdeal →ₗ[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightCompletion.scalarWeightGNSEmbedding

private theorem star_product_square {𝒜 : Type*} [Ring 𝒜] [StarRing 𝒜] (a b : 𝒜) :
    star (a*b)*(a*b) = star b*(star a*a)*b := by
  simp only [star_mul, mul_assoc]

#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_R6 norm declaration start"
  h.flush

theorem scalarWeight_right_perturbed_norm (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val * (star A.val.val * A.val.val) * b.val)
      regularFockVacuum =
    ENNReal.ofReal (‖scalarGNSRepresentation (star b)
      (J.symm (scalarWeightGNSEmbedding A))‖^2) := by
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 norm statement elaborated; before membership conversion"
      h.flush
  have hright : F1Fecho.GenericPolarRightAlgebra.ScalarPolarRight
      (𝒜 := core.toStarSubalgebra) (H := GNSHilbert)
      scalarWeightLeftIdeal fockLambda fockPi J b := hb.1
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 membership converted; before rightProduct"
      h.flush
  let P : scalarWeightLeftIdeal := F1Fecho.GenericPolarRightAlgebra.rightProduct
    (𝒜 := core.toStarSubalgebra) (H := GNSHilbert)
    scalarWeightLeftIdeal fockLambda fockPi J b hright A
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 rightProduct defined; before nested subtype value"
      h.flush
  have hv : P.val.val = A.val.val*b.val := rfl
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 nested subtype value ready; before GNS norm supplier"
      h.flush
  have hnorm : ENNReal.ofReal (‖fockLambda P‖^2) =
      dualQuadraticIntegral (star P.val.val*P.val.val) regularFockVacuum :=
    F1Fecho.CanonicalFockWeightSandwich.scalarWeightGNSEmbedding_norm_sq P
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 GNS norm supplier ready; before algebra conversion"
      h.flush
  have hsquare : star P.val.val*P.val.val =
      star (A.val.val*b.val)*(A.val.val*b.val) :=
    congrArg
      (fun D : TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
          TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F => star D*D) hv
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 typed square congruence ready; before generic star-product identity"
      h.flush
  have halg : star P.val.val*P.val.val =
      star b.val*(star A.val.val*A.val.val)*b.val :=
    hsquare.trans (star_product_square
      (𝒜 := TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
        TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F)
      A.val.val b.val)
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 algebra conversion ready; before integral transport"
      h.flush
  have hweight :
      dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val)
        regularFockVacuum = ENNReal.ofReal (‖fockLambda P‖^2) :=
    (congrArg
      (fun D : TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
          TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F =>
        dualQuadraticIntegral D regularFockVacuum) halg.symm).trans hnorm.symm
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 integral transport ready; before generic rightProduct_norm"
      h.flush
  have hrightnorm : ‖fockLambda P‖ =
      ‖fockPi (star b) (J.symm (fockLambda A))‖ :=
    F1Fecho.GenericPolarRightAlgebra.rightProduct_norm
      (𝒜 := core.toStarSubalgebra) (H := GNSHilbert)
      scalarWeightLeftIdeal fockLambda fockPi J b hright A
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 generic norm ready; before final norm-square transport"
      h.flush
  exact hweight.trans (congrArg (fun x : ℝ => ENNReal.ofReal (x^2)) hrightnorm)

#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_R6 norm declaration returned; mono declaration start"
  h.flush

theorem scalarWeight_right_perturbed_mono (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b c : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (hc : c ∈ scalarPolarRightAlgebra J)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      regularFockVacuum ≤
    dualQuadraticIntegral (star c.val * (star A.val.val*A.val.val) * c.val)
      regularFockVacuum := by
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 mono statement elaborated; before right membership"
      h.flush
  have hrightb : F1Fecho.GenericPolarRightAlgebra.ScalarPolarRight
      (𝒜 := core.toStarSubalgebra) (H := GNSHilbert)
      scalarWeightLeftIdeal fockLambda fockPi J b := hb.1
  have hrightc : F1Fecho.GenericPolarRightAlgebra.ScalarPolarRight
      (𝒜 := core.toStarSubalgebra) (H := GNSHilbert)
      scalarWeightLeftIdeal fockLambda fockPi J c := hc.1
  have ho : fockPi (b*star b) ≤ fockPi (c*star c) :=
    F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone hbc
  have hp : fockPi b*star (fockPi b) ≤ fockPi c*star (fockPi c) := by
    simpa only [map_mul, map_star] using ho
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 represented order ready; before generic squared norm monotonicity"
      h.flush
  have hn : ‖fockPi (star b) (J.symm (fockLambda A))‖^2 ≤
      ‖fockPi (star c) (J.symm (fockLambda A))‖^2 :=
    represented_right_norm_squared_mono
      (𝒜 := core.toStarSubalgebra) (H := GNSHilbert)
      scalarWeightLeftIdeal fockLambda fockPi J b c hrightb hrightc hp A
  run_tac
    IO.FS.withFile "R7_stages.log" .append fun h => do
      h.putStrLn "R7_R6 explicit squared norm monotonicity ready; before integral equality transport"
      h.flush
  calc
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val)
        regularFockVacuum =
        ENNReal.ofReal (‖fockPi (star b) (J.symm (fockLambda A))‖^2) :=
      scalarWeight_right_perturbed_norm J b hb A
    _ ≤ ENNReal.ofReal (‖fockPi (star c) (J.symm (fockLambda A))‖^2) :=
      ENNReal.ofReal_le_ofReal hn
    _ = dualQuadraticIntegral (star c.val*(star A.val.val*A.val.val)*c.val)
        regularFockVacuum :=
      (scalarWeight_right_perturbed_norm J c hc A).symm

#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_R6 both declarations returned; verify exit and axiom report"
  h.flush

end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_norm
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_mono
