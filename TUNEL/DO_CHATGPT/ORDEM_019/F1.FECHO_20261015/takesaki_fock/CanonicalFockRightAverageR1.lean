import CanonicalFockWeightDomainR1
import TGLExt.V350ShiftCharacterAverage
import CanonicalFockWeightInvarianceR4

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.CanonicalFockRightAverage
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightInvariance
open scoped Topology ENNReal
noncomputable section

theorem regularUnitary_vacuum_is_shift  (t : ℝ) :
    regularUnitary t regularFockVacuum = shift t regularFockVacuum := by
  have h := congrArg (fun T : RegularHilbert F →L[ℂ] _ => T regularFockVacuum)
    (shift_commutes_fibre t (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)).symm
  change fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) (shift t regularFockVacuum) =
    shift t (fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) regularFockVacuum) at h
  change fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) (shift t regularFockVacuum) = _
  rw [h,fibre_boost_fixes_regularVacuum]

/-- Right multiplication on an orbit is a phase and ordinary translation.
No KMS identity or modular identification is assumed. -/
theorem scalarOrbit_right_regular 
    (A : (core).toStarSubalgebra) (s t : ℝ) :
    dualAmbient s (A.val * regularUnitary t) regularFockVacuum =
      characterPhase s t • shift t (dualAmbient s A.val regularFockVacuum) := by
  rw [map_mul,F1Fecho.RegularCovariantCore.dual_on_regular fockFlow]
  change dualAmbient s A.val (characterPhase s t • regularUnitary t regularFockVacuum) = _
  rw [map_smul,regularUnitary_vacuum_is_shift]
  congr 1
  have h := (VonNeumannAlgebra.mem_commutant_iff.mp (F1Fecho.RegularCoreFixed.shift_mem_regularCommutant fockFlow M t))
    (dualAction s A).val (dualAction s A).property
  exact congrArg (fun T : RegularHilbert F →L[ℂ] _ => T regularFockVacuum) h

theorem scalarOrbit_right_average 
    (A : (core).toStarSubalgebra) (s h : ℝ) :
    dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum =
      shiftCharacterAverage s h (dualAmbient s A.val regularFockVacuum) := by
  rw [map_mul]
  change dualAmbient s A.val (dualAmbient s (F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum) = _
  rw [F1Fecho.RegularCoreAverage.regularAverage_dual_apply fockFlow,shiftCharacterAverage_apply]
  change dualAmbient s A.val (((h⁻¹ : ℝ) : ℂ) • _) = ((h⁻¹ : ℝ) : ℂ) • _
  rw [map_smul]
  congr 1
  have hc := (characterPhase_continuous s).smul
    (regular_strongly_continuous regularFockVacuum)
  rw [← (dualAmbient s A.val).intervalIntegral_comp_comm (hc.intervalIntegrable 0 h)]
  apply intervalIntegral.integral_congr
  intro t _
  have he := scalarOrbit_right_regular A s t
  rw [map_mul,F1Fecho.RegularCovariantCore.dual_on_regular fockFlow] at he
  exact he

theorem scalarOrbit_right_average_norm_le 
    (A : (core).toStarSubalgebra) (s h : ℝ) :
    ‖dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum‖ ≤
      ‖dualAmbient s A.val regularFockVacuum‖ := by
  rw [scalarOrbit_right_average]
  exact shiftCharacterAverage_norm_map_le s h _

theorem scalarOrbit_right_average_tendsto 
    (A : (core).toStarSubalgebra) (s : ℝ) :
    Tendsto (fun h : ℝ => dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum)
      (𝓝[≠] 0) (𝓝 (dualAmbient s A.val regularFockVacuum)) := by
  simp_rw [scalarOrbit_right_average]
  exact shiftCharacterAverage_tendsto_identity s _

theorem scalarWeight_right_average_le 
    (A : (core).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) * (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h))
      regularFockVacuum ≤ dualQuadraticIntegral (star A.val * A.val) regularFockVacuum := by
  simp only [dualQuadraticIntegral,dualQuadraticIntegrand_star_mul]
  apply mul_le_mul_right
  apply lintegral_mono
  intro s
  exact ENNReal.ofReal_le_ofReal (pow_le_pow_left₀ (norm_nonneg _)
    (scalarOrbit_right_average_norm_le A s h) 2)

def scalarWeightRightRegularization  (A : scalarWeightLeftIdeal ) (h : ℝ) :
    scalarWeightLeftIdeal :=
  ⟨⟨A.val.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h,
    (core).mul_mem A.val.property (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h)⟩,
    (scalarWeight_right_average_le A.val h).trans_lt A.property⟩

theorem scalarWeightRightRegularization_uniform 
    (A : scalarWeightLeftIdeal ) (h : ℝ) (hh : 0 < h) :
    (scalarWeightRightRegularization A h).val ∈ finiteLeftIdeal :=
  HasFiniteDualSquare.left_mul _ _ (F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh)

end
end F1Fecho.CanonicalFockRightAverage
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockRightAverage).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
