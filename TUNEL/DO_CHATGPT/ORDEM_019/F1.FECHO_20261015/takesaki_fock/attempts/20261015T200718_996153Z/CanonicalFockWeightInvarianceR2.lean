import CanonicalFockFaithfulWeightR2
import TGLExt.V350ScalarModularInvariance
/-! The constructed Fock dual weight is invariant under the actual regular
boost conjugation. Invariance alone does NOT identify this candidate flow as
the modular group of the weight; no KMS premise is silently introduced. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.CanonicalFockWeightInvariance
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight

theorem regular_conjugation_eq_fibre (t : ℝ)
    (A : RegularHilbert F →L[ℂ] RegularHilbert F) (hA : A ∈ core) :
    star (regularUnitary t) * A * regularUnitary t =
      star (fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)) * A *
      fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) := by
  have hs : shift (-t) * A = A * shift (-t) :=
    ((VonNeumannAlgebra.mem_commutant_iff.mp
      (F1Fecho.RegularCoreFixed.shift_mem_regularCommutant fockFlow M (-t))) A hA).symm
  rw [F1Fecho.CanonicalFockRegular.regular_star]
  unfold F1Fecho.CanonicalFockRegular.regularUnitary F1Fecho.RegularCovariantCore.regularUnitary
  rw [← fibre_star,F1Fecho.RegularCovariantCore.boostCLM_star]
  calc
    _ = fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow (-t)) * (shift (-t) * A) *
        (fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) * shift t) := by simp only [mul_assoc]
    _ = fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow (-t)) * A *
        (shift (-t) * fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)) * shift t := by
      rw [hs]
      simp only [mul_assoc]
    _ = (fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow (-t)) * A *
         fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)) * (shift (-t) * shift t) := by
      rw [shift_commutes_fibre]
      simp only [mul_assoc]
    _ = _ := by rw [shift_mul, neg_add_cancel, shift_zero, mul_one]

theorem fibre_boost_fixes_regularVacuum (t : ℝ) :
    fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) regularFockVacuum = regularFockVacuum := by
  change fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) (testVector vacuum) = testVector vacuum
  rw [fibre_testVector]
  change testVector (gamma (B0 (-(2*Real.pi*t))) vacuum) = testVector vacuum
  rw [gamma_vacuum]

def regularConjugate (A : PositiveInput) (t : ℝ) : PositiveInput :=
  ⟨star (regularUnitary t) * A.val * regularUnitary t,
    core.mul_mem (core.mul_mem
      (core.toStarSubalgebra.star_mem' (regular_mem t)) A.property.1) (regular_mem t),
    star_left_conjugate_nonneg A.property.2 _⟩

theorem weight_regular_invariant (A : PositiveInput) (t : ℝ) :
    weight (regularConjugate A t) = weight A := by
  change dualQuadraticIntegral (star (regularUnitary t) * A.val * regularUnitary t)
    regularFockVacuum = dualQuadraticIntegral A.val regularFockVacuum
  rw [regular_conjugation_eq_fibre t A.val A.property.1,
    dualQuadraticIntegral_bimodule,fibre_boost_fixes_regularVacuum]

end F1Fecho.CanonicalFockWeightInvariance
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockWeightInvariance).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
