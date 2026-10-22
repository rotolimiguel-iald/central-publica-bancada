from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'CanonicalFockAntiAssemblyR1.lean').read_text(encoding='utf8').replace('import BosonicGammaJR2','import BosonicGammaJR4')
s+='''
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.Antilinear).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\\t" ++ n.toString ++ "\\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
'''
with (b/'CanonicalFockAntiAssemblyR2.lean').open('x',encoding='utf8') as f:f.write(s)
