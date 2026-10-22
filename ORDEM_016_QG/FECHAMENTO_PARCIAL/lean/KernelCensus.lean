import TGL
import TGLExt
import Lean
open Lean
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.toList do
    let moduleName := (env.getModuleFor? n).map Name.toString |>.getD "?"
    if moduleName.startsWith "TGL" then
      let kind := match ci with
        | .thmInfo _ => "theorem"
        | .axiomInfo _ => "axiom"
        | .defnInfo _ => "definition"
        | _ => "generated_or_type"
      IO.println ("KERNEL_DECL\t" ++ n.toString ++ "\t" ++ moduleName ++ "\t" ++ kind)
