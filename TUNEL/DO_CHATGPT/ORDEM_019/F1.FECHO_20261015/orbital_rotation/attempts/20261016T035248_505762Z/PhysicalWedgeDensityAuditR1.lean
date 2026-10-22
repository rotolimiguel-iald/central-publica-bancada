import HalfPlaneBoundaryUniquenessR4
import DominatedWithinIntegralR3
import PositiveCoefficientBoundaryR4
import PositiveCoefficientBothR4
import RegularCoefficientBoundaryR3
import RegularSemigroupClosureR3
import PhysicalWedgeNullGeometryR3
import SchwartzCutoffDerivativeR4
import SchwartzCutoffEstimateR5
import SchwartzCompactDensityR3
import SchwartzCutoffSupportR1
import PhysicalWedgeGroupInvariantR3
import PhysicalWedgeSchwartzClosureR3
import PhysicalLocalizedBoostR2
import PhysicalNetGeometryR1
import PhysicalCanonicalWedgeEqualityR3

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [`HalfPlaneBoundaryUniquenessR4, `DominatedWithinIntegralR3, `PositiveCoefficientBoundaryR4, `PositiveCoefficientBothR4, `RegularCoefficientBoundaryR3, `RegularSemigroupClosureR3, `PhysicalWedgeNullGeometryR3, `SchwartzCutoffDerivativeR4, `SchwartzCutoffEstimateR5, `SchwartzCompactDensityR3, `SchwartzCutoffSupportR1, `PhysicalWedgeGroupInvariantR3, `PhysicalWedgeSchwartzClosureR3, `PhysicalLocalizedBoostR2, `PhysicalNetGeometryR1, `PhysicalCanonicalWedgeEqualityR3]
  let indices := roots.filterMap env.getModuleIdx?
  unless indices.length == roots.length do throwError "MISSING_MODULE_REFUSED"
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if (env.getModuleIdxFor? n).any (fun i => indices.contains i) then
      count := count + 1
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "NON_TRIO_REFUSED {n}"
      match ci with
      | .axiomInfo _ => throwError "NEW_AXIOM_REFUSED {n}"
      | _ => pure ()
  if count == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("AUDITED_COUNT\t" ++ toString count)
