import CanonicalFockCoefficientGraphEqualityR7
import CanonicalFockCoefficientUnitaryR3
import ClosedTomitaSquareGraphR1
import CanonicalFockWeightModularFlowR3
import SpectralUnitaryTransportR1
/-! The actual dual-weight modular group is the regular implementation.
The concrete coefficient unitary transports the full Tomita graphs, then
recognition of their independently constructed resolvents transports CFC.
No modular-flow equality or trace is supplied as an input. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockModularIdentification
open TGLV350.Regular F1Rede.BosonicFock ORDEM016.D6
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockCoefficientGNS
open F1Fecho.CanonicalFockCoefficientIntervals F1Fecho.CanonicalFockCoefficientInclusion
open F1Fecho.CanonicalFockCoefficientFlow F1Fecho.CanonicalFockCoefficientGraphEquality
open F1Fecho.CoefficientFockConjugation F1Fecho.CanonicalFockConjugation
open F1Fecho.CanonicalFockWeightModularOperator F1Fecho.CanonicalFockWeightModularFlow
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) := F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace

 theorem target_graph_eq : ClosedTomitaSquareGraph.graph actualClosedInput=
    (RegularScalarRealGraph.closedGraph weightContext:Set (GNSHilbert×GNSHilbert)) :=
  CanonicalFockWeightClosedTomita.graph_eq

 theorem unitary_graph :
    (coefficientUnitary.toHomeomorph.prodCongr coefficientUnitary.toHomeomorph) ''
      CoefficientTomitaSquare.graph coefficientRoot coefficientJ=
        ClosedTomitaSquareGraph.graph actualClosedInput := by
  ext p
  constructor
  · rintro ⟨q,hq,rfl⟩
    rw [target_graph_eq]
    exact coefficient_graph_into_GNS q.1 q.2 hq
  · intro hp
    obtain ⟨x,hx⟩:=coefficientUnitary.surjective p.1
    obtain ⟨y,hy⟩:=coefficientUnitary.surjective p.2
    have he:(coefficientUnitary.toHomeomorph.prodCongr coefficientUnitary.toHomeomorph) (x,y)=p :=
      Prod.ext hx hy
    refine ⟨(x,y),?_,he⟩
    rw [coefficient_graph_eq_GNS]
    apply (coefficientGraph_mem x y).mpr
    rw [target_graph_eq] at hp
    exact Eq.mpr (congrArg (fun p=>p∈RegularScalarRealGraph.closedGraph weightContext) he) hp

 theorem source_resolvent_mem (x:RegularHilbert F) :
    (coefficientR x,x-coefficientR x)∈antilinearSquareGraph
      (CoefficientTomitaSquare.graph coefficientRoot coefficientJ) := by
  rw [coefficient_square]
  rw [resolvent_graph_equation]
  change coefficientR x-coefficientR (coefficientR x)=coefficientR (x-coefficientR x)
  rw [map_sub]

 theorem resolvent_intertwines (x:RegularHilbert F) :
    coefficientUnitary (coefficientR x)=scalarTomitaResolvent (coefficientUnitary x) :=
  unitary_recognizes_square_resolvent coefficientUnitary _ _ unitary_graph
    coefficientR scalarTomitaResolvent source_resolvent_mem
    (ClosedTomitaSquareGraph.resolvent_inverse actualClosedInput) x

 theorem transported_resolvent_eq :
    SpectralTransport.transported coefficientUnitary coefficientR=scalarTomitaResolvent := by
  ext1 y
  obtain ⟨x,rfl⟩:=coefficientUnitary.surjective y
  change coefficientUnitary (coefficientR (coefficientUnitary.symm (coefficientUnitary x)))=
    scalarTomitaResolvent (coefficientUnitary x)
  rw [LinearIsometryEquiv.symm_apply_apply]
  exact resolvent_intertwines x

 theorem imaginary_intertwines (t:ℝ) (x:RegularHilbert F) :
    coefficientUnitary (FibreModularCalculus.liftedFlow
      CanonicalFockPolar.modularR CanonicalFockPolar.modularR_nonneg CanonicalFockPolar.modularR_le_one
      CanonicalFockPolar.modularR_injective CanonicalFockPolar.modularR_complement_injective t x)=
        scalarTomitaImaginaryPower t (coefficientUnitary x) := by
  have hh:=SpectralTransport.imaginaryPower coefficientUnitary coefficientR hR h1 hi hj t x
  rw [transported_resolvent_eq] at hh
  exact hh

 theorem actual_modular_implementation (t:ℝ) (y:GNSHilbert) :
    scalarTomitaImaginaryPower t y=regularConjugationGNS t y := by
  obtain ⟨x,rfl⟩:=coefficientUnitary.surjective y
  exact (imaginary_intertwines t x).symm.trans (cfc_intertwines t x)

theorem actual_regular_conjugation_norm (t:ℝ) (y:GNSHilbert) :
    ‖regularConjugationGNS t y‖=‖y‖ := by
  rw [←actual_modular_implementation]
  exact (scalarTomitaImaginaryPower t).norm_map y

theorem actual_regular_conjugation_group (s t:ℝ) (y:GNSHilbert) :
    regularConjugationGNS s (regularConjugationGNS t y)=regularConjugationGNS (s+t) y := by
  simp only [←actual_modular_implementation]
  exact scalarTomitaImaginaryPower_add s t y

end F1Fecho.CanonicalFockModularIdentification
#print axioms F1Fecho.CanonicalFockModularIdentification.unitary_graph
#print axioms F1Fecho.CanonicalFockModularIdentification.resolvent_intertwines
#print axioms F1Fecho.CanonicalFockModularIdentification.transported_resolvent_eq
#print axioms F1Fecho.CanonicalFockModularIdentification.imaginary_intertwines
#print axioms F1Fecho.CanonicalFockModularIdentification.actual_modular_implementation

#print axioms F1Fecho.CanonicalFockModularIdentification.actual_regular_conjugation_norm
#print axioms F1Fecho.CanonicalFockModularIdentification.actual_regular_conjugation_group
