import FibreModularCalculusR2
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
#synth CompleteSpace (RegularHilbert H)
#synth InnerProductSpace ℂ (RegularHilbert H)
#synth CStarRing (RegularHilbert H→L[ℂ]RegularHilbert H)
#synth NonUnitalContinuousFunctionalCalculus ℂ (RegularHilbert H→L[ℂ]RegularHilbert H) IsStarNormal
#synth NonUnitalContinuousFunctionalCalculus ℝ (RegularHilbert H→L[ℂ]RegularHilbert H) IsSelfAdjoint
#synth NonUnitalContinuousFunctionalCalculus ℝ≥0 (RegularHilbert H→L[ℂ]RegularHilbert H) (0≤·)
