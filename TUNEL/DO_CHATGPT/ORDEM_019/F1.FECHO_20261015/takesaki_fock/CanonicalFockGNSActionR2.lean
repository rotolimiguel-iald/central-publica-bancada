import CanonicalFockGNSR2
import TGLExt.V350StrongOperatorField
/-! Concrete left GNS action of the SAME Fock core. The ambient multiplier
is the actual dual orbit. Its restriction is proved to preserve the completion
of the orbit range, and intertwines actual left multiplication. -/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.CanonicalFockGNSAction
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockGNS
def scalarGNSLeftProduct 
    (B : (core).toStarSubalgebra) (A : finiteLeftIdeal) :
    finiteLeftIdeal :=
  ⟨B * A.val,finiteLeftIdeal_left_mul B A.val A.property⟩

/-- The ambient left action uses the same dual orbit at every coordinate.
Restriction to the completed GNS range is a separate step. -/
def scalarGNSAmbientAction 
    (B : (core).toStarSubalgebra) :
    RegularHilbert (RegularHilbert F) →L[ℂ]
      RegularHilbert (RegularHilbert F) :=
  operatorFieldLift (dualIntegralFamily B.val)

theorem scalarGNSAmbientAction_norm_le 
    (B : (core).toStarSubalgebra) :
    ‖scalarGNSAmbientAction B‖ ≤ ‖B.val‖ :=
  operatorFieldLift_norm_le (dualIntegralFamily B.val)

theorem scalarGNSAmbientAction_intertwines 
    (B : (core).toStarSubalgebra) (A : finiteLeftIdeal) :
    scalarGNSAmbientAction B (scalarGNSOrbit A) =
      scalarGNSOrbit (scalarGNSLeftProduct B A) := by
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily B.val) (scalarGNSOrbit A),
    scalarGNSOrbit_ae A,scalarGNSOrbit_ae (scalarGNSLeftProduct B A)]
    with s h1 h2 h3
  change operatorFieldLift (dualIntegralFamily B.val) (scalarGNSOrbit A) s = _
  rw [h1,h3]
  change dualAmbient s B.val (scalarGNSOrbit A s) = _
  rw [h2]
  change dualAmbient s B.val ((↑(Real.sqrt dualHaarFactor) : ℂ) •
    dualAmbient s A.val.val regularFockVacuum) =
    (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s (B.val*A.val.val) regularFockVacuum
  rw [map_smul,map_mul]
  rfl

theorem scalarGNSAmbientAction_preserves 
    (B : (core).toStarSubalgebra) :
    ∀ v ∈ GNSSubspace, scalarGNSAmbientAction B v ∈ GNSSubspace := by
  have h : Set.MapsTo (scalarGNSAmbientAction B)
      ((scalarGNSLinear).range : Set _) ((scalarGNSLinear).range : Set _) := by
    rintro v ⟨A,rfl⟩
    exact ⟨scalarGNSLeftProduct B A, (scalarGNSAmbientAction_intertwines B A).symm⟩
  exact h.closure (scalarGNSAmbientAction B).continuous

def scalarGNSAction  (B : (core).toStarSubalgebra) :
    GNSHilbert →L[ℂ] GNSHilbert :=
  (scalarGNSAmbientAction B).restrict (scalarGNSAmbientAction_preserves B)

theorem scalarGNSAction_apply 
    (B : (core).toStarSubalgebra) (v : GNSHilbert) :
    (scalarGNSAction B v).val = scalarGNSAmbientAction B v.val := rfl

theorem scalarGNSAction_norm_le 
    (B : (core).toStarSubalgebra) : ‖scalarGNSAction B‖ ≤ ‖B.val‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
  intro v
  exact (scalarGNSAmbientAction B).le_of_opNorm_le
    (scalarGNSAmbientAction_norm_le B) v.val

theorem scalarGNSAction_intertwines 
    (B : (core).toStarSubalgebra) (A : finiteLeftIdeal) :
    scalarGNSAction B (GNSEmbedding A) =
      GNSEmbedding (scalarGNSLeftProduct B A) := by
  apply Subtype.ext
  exact scalarGNSAmbientAction_intertwines B A


end F1Fecho.CanonicalFockGNSAction
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockGNSAction).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
