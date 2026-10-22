"""Prepare clean compilation environment and kernel symbol census."""
from pathlib import Path
import json
from prepare_part_d import save,write,R
S=R/'FECHAMENTO_PARCIAL';E=S/'compiler_env';L=S/'lean';E.mkdir();L.mkdir()
for f in ['lean-toolchain','lakefile.toml','lake-manifest.json']:
    write(E/f,(R/'A8/compiler_env'/f).read_bytes())
imports=json.loads((R/'A8/READONLY_IMPORT_PATHS.json').read_bytes())
imports[0]=str(S/'kernel_v371/.lake/build/lib/lean')
save(S/'compile_config.json',dict(root=str(L),cwd=str(E),logs=str(S/'logs'),imports=imports,lake=r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe'))
write(L/'KernelCensus.lean',b'''import TGL
import TGLExt
import Lean
open Lean
run_cmd do
  let env \xe2\x86\x90 Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.toList do
    let moduleName := (env.getModuleFor? n).map Name.toString |>.getD "?"
    if moduleName.startsWith "TGL" then
      let kind := match ci with
        | .thmInfo _ => "theorem"
        | .axiomInfo _ => "axiom"
        | .defnInfo _ => "definition"
        | _ => "generated_or_type"
      IO.println ("KERNEL_DECL\\t" ++ n.toString ++ "\\t" ++ moduleName ++ "\\t" ++ kind)
''')
print(str(S/'compile_config.json'))
