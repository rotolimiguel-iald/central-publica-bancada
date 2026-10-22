import PhysicalFourierTranslationR3
import PhysicalSmearTranslationR2
import PhysicalLocalizedSubspacesR3
import WedgeLaplaceKernelR2
import WedgeLaplaceIntegralR3
import WedgeLaplaceDerivativeR3
import WedgeLaplaceAnalyticR3
import WedgeLaplaceBoundaryR3
import LowerStripContourR1

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [`PhysicalFourierTranslationR3, `PhysicalSmearTranslationR2, `PhysicalLocalizedSubspacesR3, `WedgeLaplaceKernelR2, `WedgeLaplaceIntegralR3, `WedgeLaplaceDerivativeR3, `WedgeLaplaceAnalyticR3, `WedgeLaplaceBoundaryR3, `LowerStripContourR1]
  let indices := roots.filterMap env.getModuleIdx?
  unless indices.length == roots.length do throwError "MISSING_MODULE_REFUSED"
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if (env.getModuleIdxFor? n).any (fun i => indices.contains i) then
      count := count + 1
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
  if count == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("AUDITED_COUNT\t" ++ toString count)
