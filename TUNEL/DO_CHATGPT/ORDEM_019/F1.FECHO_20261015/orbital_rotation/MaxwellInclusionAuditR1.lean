import WedgePhysicalFourierR2
import LowerGaussianControlR2
import LowerGaussianContourR2
import MaxwellComplexRapidityR3
import RapidityExponentialSpanR2
import LowerStripFourierBalanceR4
import LowerGaussianReflectionR1
import MaxwellRapidityPolynomialR1
import RegularizedContourSpaceR4
import FourierLpPostcompR1
import ContourFourierBalanceR2
import FubiniTransposeR2
import FourierFubiniR3
import BoundedScalarL2LimitR3
import MaxwellStripCoefficientR5
import CircularConjugationR1
import PartialFourierRepresentativeR4
import MaxwellContourR2
import GaussianL2RemovalR4
import PartialFourierWeightedGraphR2
import MaxwellFourierBalanceR2
import MaxwellVectorBalanceR1
import CanonicalSectionCriterionR2
import RapidityGaussianR1
import PhysicalCircularRapidityR1
import MaxwellCanonicalWedgeR2
import MaxwellLocalizedInclusionR2
import RealSubspaceRegularizerUniquenessR2

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [`WedgePhysicalFourierR2, `LowerGaussianControlR2, `LowerGaussianContourR2, `MaxwellComplexRapidityR3, `RapidityExponentialSpanR2, `LowerStripFourierBalanceR4, `LowerGaussianReflectionR1, `MaxwellRapidityPolynomialR1, `RegularizedContourSpaceR4, `FourierLpPostcompR1, `ContourFourierBalanceR2, `FubiniTransposeR2, `FourierFubiniR3, `BoundedScalarL2LimitR3, `MaxwellStripCoefficientR5, `CircularConjugationR1, `PartialFourierRepresentativeR4, `MaxwellContourR2, `GaussianL2RemovalR4, `PartialFourierWeightedGraphR2, `MaxwellFourierBalanceR2, `MaxwellVectorBalanceR1, `CanonicalSectionCriterionR2, `RapidityGaussianR1, `PhysicalCircularRapidityR1, `MaxwellCanonicalWedgeR2, `MaxwellLocalizedInclusionR2, `RealSubspaceRegularizerUniquenessR2]
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
