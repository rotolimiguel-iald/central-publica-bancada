import CanonicalFockCoefficientInclusionR6
import CanonicalFockCoefficientFlowR12
import GaussianResolventAverageR6
import ClosedGraphRegularizationR3
/-! Equality of the actual coefficient and GNS Tomita graphs. The reverse
inclusion uses constructed Gaussian regularizers, their actual root-domain
range, and their strong convergence; no maximality or graph equality is an input. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.CanonicalFockCoefficientGraphEquality
open F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockPolar F1Fecho.CoefficientFockConjugation
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.CanonicalFockCoefficientIntervals
open F1Fecho.CanonicalFockCoefficientInclusion F1Fecho.CanonicalFockCoefficientFlow
open F1Fecho.GaussianResolventAverage F1Fecho.FibreModularCalculus
local instance : InnerProductSpace ℝ (RegularHilbert F) := InnerProductSpace.complexToReal

abbrev coefficientR := fibre modularR
abbrev hR := fibre_nonneg modularR_nonneg
abbrev h1 := lifted_le_one modularR modularR_le_one
abbrev hi := fibre_operator_injective modularR modularR_injective
abbrev hj := lifted_complement_injective modularR modularR_complement_injective
abbrev coefficientAverage (n:ℕ) := average coefficientR hR h1 hi hj (scale n)

def realGNSGraph : Submodule ℝ (WithLp 2 (RegularHilbert F×RegularHilbert F)) :=
  coefficientGraph.comap (WithLp.prodContinuousLinearEquiv 2 ℝ (RegularHilbert F)
    (RegularHilbert F)).toLinearMap

theorem realGNSGraph_closed : IsClosed (realGNSGraph:Set (WithLp 2 (RegularHilbert F×RegularHilbert F))) :=
  coefficientGraph_closed.preimage (WithLp.prodContinuousLinearEquiv 2 ℝ (RegularHilbert F)
    (RegularHilbert F)).continuous

theorem average_preserves (n:ℕ) (x y:RegularHilbert F) (hxy:(x,y)∈coefficientGraph) :
    (coefficientAverage n x,coefficientAverage n y)∈coefficientGraph := by
  let U:ℝ→RegularHilbert F≃ₗᵢ[ℂ]RegularHilbert F := fun t=>
    resolventImaginaryPower coefficientR hR h1 hi hj (scale n*t)
  have hc:∀x,Continuous (fun t=>U t x) := fun x=>
    (resolventImaginaryPower_strongly_continuous coefficientR hR h1 hi hj x).comp
      (continuous_const.mul continuous_id)
  have hu:∀t x y,WithLp.toLp 2 (x,y)∈realGNSGraph→
      WithLp.toLp 2 (U t x,U t y)∈realGNSGraph := by
    intro t x y hxy
    change (U t x,U t y)∈coefficientGraph
    change (x,y)∈coefficientGraph at hxy
    change (liftedFlow modularR modularR_nonneg modularR_le_one modularR_injective
        modularR_complement_injective (scale n*t) x,
      liftedFlow modularR modularR_nonneg modularR_le_one modularR_injective
        modularR_complement_injective (scale n*t) y)∈coefficientGraph
    rw [coefficient_modular_flow,coefficient_modular_flow]
    exact graph_invariant (scale n*t) x y hxy
  exact ClosedGraphRegularization.average_preserves_graph realGNSGraph realGNSGraph_closed
    U hc hu GaussianLogScalar.gaussianWeight GaussianLogScalar.gaussianWeight_integrable x y hxy

theorem average_range (n:ℕ) (x:RegularHilbert F) :
    ∃y,(coefficientAverage n x,y)∈CoefficientTomitaSquare.graph coefficientRoot coefficientJ := by
  obtain ⟨y,hy⟩:=average_root_domain coefficientR hR h1 hi hj (scale n) (scale_ne_zero n) x
  refine ⟨coefficientJ y,?_⟩
  apply (CoefficientFockPointwise.generic_graph_iff coefficientRoot coefficientJ
    coefficientJ_involutive _ _).mpr
  simpa only [coefficientJ_involutive] using hy

theorem coefficient_graph_eq_GNS :
    CoefficientTomitaSquare.graph coefficientRoot coefficientJ=
      (coefficientGraph:Set (RegularHilbert F×RegularHilbert F)) := by
  refine ClosedGraphRegularization.graph_eq_of_regularizers _ _ coefficient_graph_closed ?_
    coefficientGNSGraph_functional (fun n x=>coefficientAverage n x)
    (average_tendsto coefficientR hR h1 hi hj) average_preserves average_range
  rintro ⟨x,y⟩ hxy
  exact (coefficientGraph_mem x y).mpr (coefficient_graph_into_GNS x y hxy)

end F1Fecho.CanonicalFockCoefficientGraphEquality
#print axioms F1Fecho.CanonicalFockCoefficientGraphEquality.average_preserves
#print axioms F1Fecho.CanonicalFockCoefficientGraphEquality.average_range
#print axioms F1Fecho.CanonicalFockCoefficientGraphEquality.coefficient_graph_eq_GNS
