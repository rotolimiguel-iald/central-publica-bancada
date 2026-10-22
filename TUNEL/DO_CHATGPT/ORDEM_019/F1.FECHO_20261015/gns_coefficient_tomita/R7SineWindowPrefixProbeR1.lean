import CanonicalFockPolarRightClosureR10

/-! Diagnostic prefix only. The active R11 candidate remains separate.
Markers go to this attempt's own cwd, not captured #eval stdout. -/
set_option autoImplicit false
set_option Elab.async false
noncomputable section
namespace F1Fecho.R7PrefixProbe
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockRegularRightGNS

#eval IO.FS.withFile "R7_probe.log" .append fun h => do
  h.putStrLn "before_regularSineWindowCore"
  h.flush

def regularSineWindowCore (m : ℝ) :
    (core).toStarSubalgebra :=
  (1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
    (regularRightCoreElement (-1/m) - regularRightCoreElement (1/m))

#eval IO.FS.withFile "R7_probe.log" .append fun h => do
  h.putStrLn "after_regularSineWindowCore"
  h.flush

end F1Fecho.R7PrefixProbe
#print axioms F1Fecho.R7PrefixProbe.regularSineWindowCore
