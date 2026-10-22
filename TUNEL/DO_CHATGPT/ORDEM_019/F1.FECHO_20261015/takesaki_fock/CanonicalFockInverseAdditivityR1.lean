import CanonicalFockPolarRightClosureR4
import CanonicalFockPerturbedWeightOrderR3
import GeneralInverseAdditivityR2
import GeneralCutoffAverageCommutationR1
import GeneralRegulatorOrderR1
import CanonicalFockInverseSupremumR2
import CanonicalFockWeightInvarianceR4
/-! Regulator order and positive additivity of the SAME inverse weight.
The intermediate actual polar-right identity is explicit; no tracial law is
assumed or concluded here. Its concrete discharge is a separate consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockInverseAdditivity
open TGLExt TGLV350.Regular Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockRegularRightGNS
open F1Fecho.CanonicalFockPolarRight F1Fecho.RegularPositiveFlow F1Fecho.RegularInverseWeight
open scoped ENNReal Topology
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
variable (hreg : ∀t,regularRightCoreElement t∈scalarPolarRightAlgebra J)

private theorem hilbert_sqrt_mul_star {E:Type}
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (B:E→L[ℂ]E) (hB:0≤B) : hilbertPositiveSqrt B*star (hilbertPositiveSqrt B)=B := by
  change CFC.sqrt B*star (CFC.sqrt B)=B
  rw [(CFC.sqrt_nonneg B).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self B hB]

include hreg in
theorem cutoff_antitone (e d:PositiveRegulator) (hed:e.val≤d.val)
    (X:PositiveInput) :
    cutoffWeight fockFlow regularFockVacuum d.val X.val ≤
      cutoffWeight fockFlow regularFockVacuum e.val X.val := by
  obtain ⟨hbm,hbr⟩:=regularInverseGeneratorCutoff_sqrt_right J hreg d.val d.property
  obtain ⟨hcm,hcr⟩:=regularInverseGeneratorCutoff_sqrt_right J hreg e.val e.property
  let b:core.toStarSubalgebra:=⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow d.val),hbm⟩
  let c:core.toStarSubalgebra:=⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow e.val),hcm⟩
  have hbc:b*star b≤c*star c:=by
    change b.val*star b.val≤c.val*star c.val
    rw [hilbert_sqrt_mul_star _ (regularInverseGeneratorCutoff_nonneg fockFlow d.val d.property),
      hilbert_sqrt_mul_star _ (regularInverseGeneratorCutoff_nonneg fockFlow e.val e.property)]
    exact regularInverseGeneratorCutoff_antitone fockFlow e.val d.val e.property d.property hed
  have hfinite (A:core.toStarSubalgebra) (hA:HasFiniteDualSquare A.val) :
      dualQuadraticIntegral (star b.val*(star A.val*A.val)*b.val) regularFockVacuum ≤
        dualQuadraticIntegral (star c.val*(star A.val*A.val)*c.val) regularFockVacuum := by
    exact scalarWeight_right_perturbed_mono J b c hbr hcr hbc
      ⟨A,F1Fecho.CanonicalFockFiniteWeight.finiteSquare_scalar_finite A.val hA⟩
  exact perturbed_comparison_all_positive fockFlow M regularFockVacuum
    F1Fecho.CanonicalFockWeightInvariance.fibre_boost_fixes_regularVacuum b c
    (regularInverseCutoffSqrt_commutes_average fockFlow d.val d.property)
    (regularInverseCutoffSqrt_commutes_average fockFlow e.val e.property)
    hfinite ⟨X.val,X.property.1⟩ X.property.2

include hreg in
theorem value_add (X Y:PositiveInput) :
    CanonicalFockInverseSupremum.value (add X Y)=
      CanonicalFockInverseSupremum.value X+CanonicalFockInverseSupremum.value Y :=
  inverseSupremum_add_of_antitone fockFlow regularFockVacuum X.val Y.val
    X.property.2 Y.property.2
    (fun e d hed=>cutoff_antitone J hreg e d hed X)
    (fun e d hed=>cutoff_antitone J hreg e d hed Y)

include hreg in
theorem cutoff_sequence_mono (X:PositiveInput) :
    Monotone (fun n:ℕ=>CanonicalFockInverseSupremum.cut (1/((n:ℝ)+1)) X) :=
  cutoff_sequence_mono_of_antitone fockFlow regularFockVacuum X.val
    (fun e d hed=>cutoff_antitone J hreg e d hed X)

end F1Fecho.CanonicalFockInverseAdditivity
#print axioms F1Fecho.CanonicalFockInverseAdditivity.cutoff_antitone
#print axioms F1Fecho.CanonicalFockInverseAdditivity.value_add
#print axioms F1Fecho.CanonicalFockInverseAdditivity.cutoff_sequence_mono
