import ExponentialTomitaInclusionR2
import WeylFiniteAlgebraR4
import ExponentialTomitaEqualityR4
import OneParticleDualityR2
import CanonicalFockDualWeightR3
import CanonicalTracedCoreAssemblyR1
import Lean

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [`ExponentialTomitaInclusionR2, `WeylFiniteAlgebraR4, `ExponentialTomitaEqualityR4, `OneParticleDualityR2, `CanonicalFockDualWeightR3, `CanonicalTracedCoreAssemblyR1]
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
