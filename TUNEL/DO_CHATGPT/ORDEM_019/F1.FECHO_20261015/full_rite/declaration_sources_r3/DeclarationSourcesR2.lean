import TGL
import TGLExt
import Lean

/-! Read-only provenance exported from the successfully compiled environment.
This records defining modules, including generated declarations. It is not a
text parser and does not promote an absent declaration to a verified one. -/
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut count := 0
  for (n, _) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? n then
      let mod := env.header.moduleNames[idx]!
      if (`TGL).isPrefixOf mod || (`TGLExt).isPrefixOf mod then
        count := count + 1
        IO.println ("DECL_SOURCE\t" ++ n.toString ++ "\t" ++ mod.toString)
  if count == 0 then throwError "EMPTY_PROVENANCE_REFUSED"
  IO.println ("SOURCE_COUNT\t" ++ toString count)
