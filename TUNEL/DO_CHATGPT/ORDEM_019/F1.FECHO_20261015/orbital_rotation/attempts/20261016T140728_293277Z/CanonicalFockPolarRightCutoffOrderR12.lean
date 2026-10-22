import R7SineWindowClosureProbeR5

/-! Cutoff and right-action consequences using the compiled first-resolvent module.
The full scaled trace/PF construction remains a later obligation.
No original or earlier attempt is replaced. -/
set_option autoImplicit false
set_option Elab.async false
set_option maxHeartbeats 600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open MeasureTheory Filter
open TGLV350.Regular (hilbertPositiveSqrt inverseCutoffFunction)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.RegularPositiveFlow
open scoped Topology
#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "before_regularSpectralResolvent_right"
  h.flush

theorem regularSpectralResolvent_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) :
    (⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩ :
      (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J := by
  let b (n : ℕ) : (core).toStarSubalgebra :=
    ⟨regularSineResolvent fockFlow ((n : ℝ)+1),(regularSineResolvent_right J hreg ((n : ℝ)+1)).choose⟩
  let B : (core).toStarSubalgebra :=
    ⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩
  have hb (n : ℕ) : b n ∈ scalarPolarRightAlgebra J :=
    (regularSineResolvent_right J hreg ((n : ℝ)+1)).choose_spec
  have hs (n : ℕ) : star (b n) = b n :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSineResolvent_nonneg fockFlow ((n : ℝ)+1))).star_eq
  have hB : star B = B :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg fockFlow)).star_eq
  have hright : ScalarPolarRight J B := by
    intro A
    have ha : ∀ x, Tendsto (fun n => (star (b n)).val x) atTop (𝓝 ((star B).val x)) := by
      intro x
      simpa only [hs,hB] using regularSineResolvent_tendsto fockFlow x
    exact scalarRightAction_closed_of_bounded_strongStar J b B 1
      (fun n => regularSineResolvent_norm_le fockFlow ((n : ℝ)+1))
      (fun x => regularSineResolvent_tendsto fockFlow x) ha A (fun n => (hb n).1 A)
  change ScalarPolarRight J B ∧ ScalarPolarRight J (star B)
  rw [hB]
  exact ⟨hright,hright⟩



#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_STAGE regularInverseGeneratorCutoff_right"
  h.flush

theorem regularInverseGeneratorCutoff_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (ε : ℝ) (hε : 0 < ε) :
    (⟨regularInverseGeneratorCutoff fockFlow ε,regularInverseGeneratorCutoff_mem fockFlow M ε⟩ :
      (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J := by
  have hm := lift_predicate_eq (fun T => T ∈ core)
    (fun z => z ∈ scalarPolarRightAlgebra J)
    (regularInverseGeneratorCutoff_cfc fockFlow ε hε)
    (scalarRightAction_cfc J
      ⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩
      (regularSpectralResolvent_right J hreg) (inverseCutoffFunction ε))
  exact hm.choose_spec



#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_STAGE hilbertPositiveSqrt_complex_cfc"
  h.flush

/-- Consume the standard real/complex CFC bridges for the original positive
square root; no independent root is introduced. -/
private theorem hilbertPositiveSqrt_complex_cfc
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (h0 : 0 ≤ T) :
    hilbertPositiveSqrt T = cfc (fun z : ℂ => (Real.sqrt z.re : ℂ)) T := by
  rw [hilbertPositiveSqrt,CFC.sqrt_eq_real_sqrt _ h0,
    cfcₙ_eq_cfc Real.continuous_sqrt.continuousOn Real.sqrt_zero,
    cfc_real_eq_complex Real.sqrt (IsSelfAdjoint.of_nonneg h0)]

#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_STAGE scalarRightAction_sqrt"
  h.flush

theorem scalarRightAction_sqrt (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : (core).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (h0 : 0 ≤ b.val) :
    ∃ h : hilbertPositiveSqrt b.val ∈ core,
      (⟨hilbertPositiveSqrt b.val,h⟩ : (core).toStarSubalgebra) ∈
        scalarPolarRightAlgebra J := by
  exact lift_predicate_eq (fun T => T ∈ core)
    (fun z => z ∈ scalarPolarRightAlgebra J)
    (hilbertPositiveSqrt_complex_cfc b.val h0)
    (scalarRightAction_cfc J b hb (fun z : ℂ => (Real.sqrt z.re : ℂ)))


#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_STAGE regularInverseGeneratorCutoff_sqrt_right"
  h.flush

theorem regularInverseGeneratorCutoff_sqrt_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε) ∈ core,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε),h⟩ :
        (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J :=
  scalarRightAction_sqrt J
    ⟨regularInverseGeneratorCutoff fockFlow ε,regularInverseGeneratorCutoff_mem fockFlow M ε⟩
    (regularInverseGeneratorCutoff_right J hreg ε hε) (regularInverseGeneratorCutoff_nonneg fockFlow ε hε)


end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindowCore
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindowCore_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineResolvent_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSpectralResolvent_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularInverseGeneratorCutoff_right
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightAction_sqrt
#print axioms F1Fecho.CanonicalFockPolarRight.regularInverseGeneratorCutoff_sqrt_right

-- END SOURCE CanonicalFockPolarRightClosureR4

-- BEGIN SOURCE CanonicalFockRightCommutationR1
/-! The proved polar right identity commutes with the actual Fock left action.
No commutant equality or polar factor identification is assumed here. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockWeightSandwich F1Fecho.CanonicalFockRegular
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_STAGE scalarPolarRight_commutes_left"
  h.flush

theorem scalarPolarRight_commutes_left
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra) (hb : ScalarPolarRight J b)
    (c : core.toStarSubalgebra) :
    Commute (antiunitaryConjugate (H := GNSHilbert) J (scalarGNSRepresentation (star b)))
      (scalarGNSRepresentation c) := by
  let R := antiunitaryConjugate (H := GNSHilbert) J (scalarGNSRepresentation (star b))
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

-- END SOURCE CanonicalFockRightCommutationR1

-- BEGIN SOURCE CanonicalFockPerturbedWeightOrderR3
/-! Right perturbation norm and order in the actual Fock full-weight ideal.
The existing v393 calculation is specialized directly to avoid instance diamonds.
J and right membership remain explicit until the actual polar consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLV350.Regular (dualQuadraticIntegral antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightCompletion F1Fecho.CanonicalFockGNSOrder
open F1Fecho.CanonicalFockWeightSandwich
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_STAGE scalarWeight_right_perturbed_norm"
  h.flush

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
    _ = ENNReal.ofReal (‖antiunitaryConjugate (H := GNSHilbert) J
        (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)‖^2) :=
      congrArg (fun v : GNSHilbert => ENNReal.ofReal (‖v‖^2)) he
    _ = _ := congrArg (fun r : ℝ => ENNReal.ofReal (r^2))
      (J.norm_map
        (scalarGNSRepresentation (star b)
          (J.symm (scalarWeightGNSEmbedding A))))


#eval IO.FS.withFile "R7_stages.log" .append fun h => do
  h.putStrLn "R7_STAGE scalarWeight_right_perturbed_mono"
  h.flush

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

-- END SOURCE CanonicalFockPerturbedWeightOrderR3
