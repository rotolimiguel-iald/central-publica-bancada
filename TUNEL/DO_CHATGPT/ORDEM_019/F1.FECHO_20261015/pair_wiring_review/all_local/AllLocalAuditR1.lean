import CanonicalWeylAssemblyR5
import CanonicalWedgeFlowR2
import PairTomitaClosabilityR2
import PairClosedTomitaR2
import OneParticleSymplecticR2
import WedgePairTomitaR2
import WeylAntiunitaryR4
import Lean

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [`F1Fecho.NetworkWeyl, `F1Fecho.CanonicalWedgeFlow, `F1Fecho.PairTomita, `F1Fecho.OneParticleSymplectic, `F1Fecho.WedgePairTomita, `F1Fecho.WeylAntiunitary]
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if roots.any (fun p => p.isPrefixOf n) then
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
