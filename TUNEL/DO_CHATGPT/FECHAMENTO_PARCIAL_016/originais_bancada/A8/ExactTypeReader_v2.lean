import Lean

open Lean Elab Command Term Meta

/- Engineering prototype. The caller must pin the contract, closed indices,
candidate declaration and this checker. Success is not ratification. -/
elab "#assert_exact_type " candidate:ident " : " expected:term : command => do
  liftTermElabM do
    let name ← realizeGlobalConstNoOverloadWithInfo candidate
    let value ← mkConstWithFreshMVarLevels name
    let actual ← inferType value
    let target ← elabType expected
    synthesizeSyntheticMVarsNoPostponing
    let actual ← instantiateMVars actual
    let target ← instantiateMVars target
    if actual.hasFVar || target.hasFVar || actual.hasMVar || target.hasMVar then
      throwError "EXACT_TYPE_OPEN_CONTEXT: closed indices and a closed declaration are required"
    unless ← isDefEq actual target do
      throwError "EXACT_TYPE_MISMATCH: {name} has type {actual}, expected {target}"
    logInfo m!"EXACT_TYPE_ACCEPTED: {name} : {target}"
