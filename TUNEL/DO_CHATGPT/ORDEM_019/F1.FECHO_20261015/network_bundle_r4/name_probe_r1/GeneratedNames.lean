import TGLExt.F1Fecho394.CanonicalWeylAssemblyR5
import Lean
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, _) in env.constants.toList do
    if "F1Rede.LightRay".isPrefixOf n.toString then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
