import CanonicalFockGNSR5
import RegularScalarGaussianR1
/-! The auxiliary Gaussian separating vector of the actual regular Fock
algebra, obtained by instantiating a proved generic construction. It does not
replace the original weight or identify it with a trace. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockGaussian
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS

abbrev scalarGaussianVacuum : RegularHilbert (RegularHilbert F) :=
  F1Fecho.RegularScalarGaussian.scalarGaussianVacuum weightContext

theorem scalarGaussianVacuum_ae :
    (scalarGaussianVacuum : ℝ → RegularHilbert F) =ᵐ[volume]
      fun s => (gaussianProfile s : ℂ) • ((Real.sqrt dualHaarFactor : ℂ) • regularFockVacuum) :=
  F1Fecho.RegularScalarGaussian.scalarGaussianVacuum_ae weightContext

theorem gaussian_zero_action_orbit_ae (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hz : dualOrbitRepresentation A scalarGaussianVacuum = 0) :
    (fun s : ℝ => dualAmbient s A regularFockVacuum) =ᵐ[volume] 0 :=
  F1Fecho.RegularScalarGaussian.gaussian_zero_action_orbit_ae weightContext A hz

theorem scalarGaussianVacuum_separating (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : A ∈ core) (hz : dualOrbitRepresentation A scalarGaussianVacuum = 0) : A=0 :=
  F1Fecho.RegularScalarGaussian.scalarGaussianVacuum_separating weightContext A hA hz

end F1Fecho.CanonicalFockGaussian
#print axioms F1Fecho.CanonicalFockGaussian.scalarGaussianVacuum
#print axioms F1Fecho.CanonicalFockGaussian.scalarGaussianVacuum_ae
#print axioms F1Fecho.CanonicalFockGaussian.gaussian_zero_action_orbit_ae
#print axioms F1Fecho.CanonicalFockGaussian.scalarGaussianVacuum_separating
