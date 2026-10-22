import GeneralRegularPositiveGraphR2
import GeneralRegularAbsorptionR1
import GeneralRegularImaginaryPowersR1
import GeneralRegularSpectralGraphR2
import GeneralRegularAffiliationR1
import GeneralRegularDualScalingR2
import GeneralRegularInverseCutoffR1
import GeneralDampedPhaseBalanceR1

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [`GeneralRegularPositiveGraphR2, `GeneralRegularAbsorptionR1, `GeneralRegularImaginaryPowersR1, `GeneralRegularSpectralGraphR2, `GeneralRegularAffiliationR1, `GeneralRegularDualScalingR2, `GeneralRegularInverseCutoffR1, `GeneralDampedPhaseBalanceR1]
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
