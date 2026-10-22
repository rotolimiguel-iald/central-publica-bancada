import CanonicalFockCoefficientUnitaryR3
import CoefficientFockConjugationR2
import UnitaryAntiunitaryTransportR2
import UnitaryRootGraphTransportR1
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
namespace F1Fecho.CanonicalFockUnitaryCoherence
open F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockCoefficientGNS
open F1Fecho.CoefficientFockConjugation
 def testJ : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert :=
  UnitaryAntiunitaryTransport.conjugate (H := RegularHilbert F) (E := GNSHilbert)
    coefficientUnitary coefficientJ
 theorem testJ_invol : Function.Involutive testJ :=
  UnitaryAntiunitaryTransport.involutive (H := RegularHilbert F) (E := GNSHilbert)
    coefficientUnitary coefficientJ coefficientJ_involutive
 def testTransport (R : RegularHilbert F →L[ℂ] RegularHilbert F) : GNSHilbert →L[ℂ] GNSHilbert :=
  SpectralTransport.transported (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary R
end F1Fecho.CanonicalFockUnitaryCoherence
#print axioms F1Fecho.CanonicalFockUnitaryCoherence.testJ_invol
