import CanonicalFockGNSCovarianceR4
import CanonicalFockCoefficientIntervalsR3
import CoefficientFockConjugationR2
/-! The coefficient embedding intertwines the actual regular GNS conjugation
with the actual CFC flow of the coefficient Tomita square. This is a unitary
flow calculation; equality of the two Tomita graphs is still separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientFlow
open F1Rede.BosonicFock
open TGLV350.Regular F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.CanonicalFockCoefficientIntervals
open F1Fecho.CanonicalFockRegularGNS F1Fecho.CanonicalFockGNSCovariance
open F1Fecho.RegularNormalizedFourier F1Fecho.CanonicalFockPolar

theorem intertwines (t:ℝ) (f:RegularHilbert F) :
    coefficientEmbedding (fibre (RegularCovariantCore.boostCLM fockFlow t) f)=
      regularConjugationGNS t (coefficientEmbedding f) := by
  apply Subtype.ext
  exact (spectralCode_fibre (RegularCovariantCore.boostCLM fockFlow t) f).trans
    (regularConjugationGNS_ambient t (coefficientEmbedding f)).symm

theorem cfc_intertwines (t:ℝ) (f:RegularHilbert F) :
    coefficientEmbedding (FibreModularCalculus.liftedFlow modularR modularR_nonneg modularR_le_one
      modularR_injective modularR_complement_injective t f)=
      regularConjugationGNS t (coefficientEmbedding f) := by
  rw [CoefficientFockConjugation.coefficient_modular_flow]
  exact intertwines t f

theorem graph_invariant (t:ℝ) (f g:RegularHilbert F) (hfg:(f,g)∈coefficientGraph) :
    (fibre (RegularCovariantCore.boostCLM fockFlow t) f,
      fibre (RegularCovariantCore.boostCLM fockFlow t) g)∈coefficientGraph := by
  apply (coefficientGraph_mem _ _).mpr
  rw [intertwines,intertwines]
  exact conjugate_closed_graph t _ ((coefficientGraph_mem f g).mp hfg)
end F1Fecho.CanonicalFockCoefficientFlow
#print axioms F1Fecho.CanonicalFockCoefficientFlow.intertwines
#print axioms F1Fecho.CanonicalFockCoefficientFlow.cfc_intertwines
#print axioms F1Fecho.CanonicalFockCoefficientFlow.graph_invariant
