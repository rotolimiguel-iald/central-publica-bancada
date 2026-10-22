import CanonicalWedgeKMSR4
import Lean

/-! Exact imported-module audit of the new root-built KMS chain.
Includes generated and private declarations; absent modules refuse. -/
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [
    `StripPhaseBoundsR1, `KMSStripIntegralR2, `KMSBoundaryExchangeR1,
    `HalfModularStripR3, `CanonicalJBoostR3, `CanonicalH1StripR3,
    `WedgeOneParticleStripR2, `StripMaximumR2, `StripUniformLimitR2,
    `StripBoundaryLimitR1, `UnitaryCoefficientsUniformR2,
    `KMSGraphClosureR3, `CanonicalWedgeKMSR4]
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
