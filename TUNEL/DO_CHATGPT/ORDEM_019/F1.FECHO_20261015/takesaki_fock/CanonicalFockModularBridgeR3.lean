import GenericStarConjugationR3
import CanonicalFockConjugationActionR3
import CanonicalFockFullWeightTomitaR5
import RegularScalarRealGraphR2
import UnitaryAntiunitaryTransportR2
import CanonicalFockCoefficientUnitaryR3
import CoefficientFockConjugationR2
import CanonicalFockCoefficientIntervalsR5
import CanonicalFockCoefficientInclusionR6
import GaussianResolventAverageR6
import ClosedGraphRegularizationR3
import ClosedTomitaSquareGraphR1
import CanonicalFockWeightModularFlowR3
import SpectralUnitaryTransportR1
import UnitaryRootGraphTransportR1
import TGLExt.V350PartialSelfadjointRange

-- BEGIN EXACT BODY CanonicalFockGNSCovarianceR12
/-! Regular conjugation preserves the FULL actual GNS adjunction graph.
The star action and finite domain are paid by actual left/right products;
modular identification is not assumed from this covariance. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockGNSCovariance
open TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockConjugation
open F1Fecho.CanonicalFockFullWeightStarCore F1Fecho.CanonicalFockFullWeightTomita
open F1Fecho.RegularScalarRealGraph F1Fecho.CanonicalFockWeightSandwich

 def conjugateLeft (t:ℝ) (A:scalarWeightStarCore) : scalarWeightLeftIdeal :=
  scalarWeightLeftProduct (regularRightCoreElement t)
    (scalarRegularRightProduct (-t) ⟨A.val,A.property.1⟩)

 theorem conjugateLeft_star (t:ℝ) (A:scalarWeightStarCore) :
    star (conjugateLeft t A).val=(conjugateLeft t (star A)).val := by
  apply Subtype.ext
  change star (regularUnitary t*(A.val.val*regularUnitary (-t)))=
    regularUnitary t*(star A.val.val*regularUnitary (-t))
  exact GenericStarConjugation.regular_conjugation_star fockFlow t A.val.val

 def conjugateStar (t:ℝ) (A:scalarWeightStarCore) : scalarWeightStarCore :=
  GenericStarConjugation.starCoreOfLeft weightContext (conjugateLeft t A)
    (conjugateLeft t (star A)) (conjugateLeft_star t A)


 theorem conjugateStar_star (t:ℝ) (A:scalarWeightStarCore) :
    star (conjugateStar t A)=conjugateStar t (star A) :=
  Subtype.ext (conjugateLeft_star t A)

 theorem conjugate_embedding (t:ℝ) (A:scalarWeightStarCore) :
    regularConjugationGNS t (scalarWeightStarEmbedding A)=
      scalarWeightStarEmbedding (conjugateStar t A) :=
  regularConjugationGNS_intertwines t ⟨A.val,A.property.1⟩

 def conjugatePair (t:ℝ) : (GNSHilbert×GNSHilbert)→L[ℂ](GNSHilbert×GNSHilbert) :=
  (regularConjugationGNS t).prodMap (regularConjugationGNS t)

 theorem conjugate_raw_graph (t:ℝ) (p:GNSHilbert×GNSHilbert)
    (hp:p∈scalarWeightTomitaGraph) : conjugatePair t p∈scalarWeightTomitaGraph := by
  obtain ⟨A,rfl⟩:=hp
  refine ⟨conjugateStar t A,?_⟩
  apply Prod.ext
  · exact (conjugate_embedding t A).symm
  · exact (congrArg scalarWeightStarEmbedding (conjugateStar_star t A)).trans
      (conjugate_embedding t (star A)).symm

 theorem conjugate_closed_graph (t:ℝ) (p:GNSHilbert×GNSHilbert)
    (hp:p∈closedGraph weightContext) : conjugatePair t p∈closedGraph weightContext := by
  have hmap : ∀p∈closure scalarWeightTomitaGraph,
      conjugatePair t p∈closure scalarWeightTomitaGraph :=
    closure_minimal (fun p hp=>subset_closure (conjugate_raw_graph t p hp))
      (isClosed_closure.preimage (conjugatePair t).continuous)
  change conjugatePair t p∈closure (RegularScalarTomitaGraph.scalarTomitaGraph weightContext)
  change p∈closure (RegularScalarTomitaGraph.scalarTomitaGraph weightContext) at hp
  exact Eq.mp (congrArg (fun s=>conjugatePair t p∈s) scalarWeightTomitaGraph_closure_eq)
    (hmap p (Eq.mpr (congrArg (fun s=>p∈s) scalarWeightTomitaGraph_closure_eq) hp))
end F1Fecho.CanonicalFockGNSCovariance
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugateLeft_star
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugateStar_star
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_embedding
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_raw_graph
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_closed_graph

-- END EXACT BODY CanonicalFockGNSCovarianceR12
-- BEGIN EXACT BODY CanonicalFockWeightPolarBasicsR3

/-! Concrete antiunitary on the actual weight GNS, by the already proved
coefficient unitary. Its identification as the polar factor is a separate
graph theorem, not assumed by this definition. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightPolar
open TGLV350.Regular F1Rede.BosonicFock
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockCoefficientGNS
open F1Fecho.CoefficientFockConjugation

def scalarTomitaPolarFactor : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert :=
  UnitaryAntiunitaryTransport.conjugate coefficientUnitary coefficientJ

theorem scalarTomitaPolarFactor_apply (x : GNSHilbert) :
    scalarTomitaPolarFactor x =
      coefficientUnitary (coefficientJ (coefficientUnitary.symm x)) := rfl

theorem scalarTomitaPolarFactor_coefficient (x : RegularHilbert F) :
    scalarTomitaPolarFactor (coefficientUnitary x) = coefficientUnitary (coefficientJ x) :=
  UnitaryAntiunitaryTransport.on_unitary coefficientUnitary coefficientJ x

theorem scalarTomitaPolarFactor_involutive : Function.Involutive scalarTomitaPolarFactor :=
  UnitaryAntiunitaryTransport.involutive coefficientUnitary coefficientJ coefficientJ_involutive

theorem scalarTomitaPolarFactor_norm (x : GNSHilbert) :
    ‖scalarTomitaPolarFactor x‖ = ‖x‖ := scalarTomitaPolarFactor.norm_map x
end F1Fecho.CanonicalFockWeightPolar
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_coefficient
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_involutive
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_norm

-- END EXACT BODY CanonicalFockWeightPolarBasicsR3
-- BEGIN EXACT BODY CanonicalFockCoefficientFlowR14
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
open F1Fecho.CanonicalFockConjugation F1Fecho.CanonicalFockGNSCovariance
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
  have he : (coefficientEmbedding (fibre (RegularCovariantCore.boostCLM fockFlow t) f),
      coefficientEmbedding (fibre (RegularCovariantCore.boostCLM fockFlow t) g)) =
      (regularConjugationGNS t (coefficientEmbedding f),
        regularConjugationGNS t (coefficientEmbedding g)) :=
    Prod.ext (intertwines t f) (intertwines t g)
  exact Eq.mpr (congrArg (fun p=>p∈RegularScalarRealGraph.closedGraph weightContext) he)
    (conjugate_closed_graph t _ ((coefficientGraph_mem f g).mp hfg))
end F1Fecho.CanonicalFockCoefficientFlow
#print axioms F1Fecho.CanonicalFockCoefficientFlow.intertwines
#print axioms F1Fecho.CanonicalFockCoefficientFlow.cfc_intertwines
#print axioms F1Fecho.CanonicalFockCoefficientFlow.graph_invariant

-- END EXACT BODY CanonicalFockCoefficientFlowR14
-- BEGIN EXACT BODY CanonicalFockCoefficientGraphEqualityR10
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

-- END EXACT BODY CanonicalFockCoefficientGraphEqualityR10
-- BEGIN EXACT BODY CanonicalFockModularIdentificationR10
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

-- END EXACT BODY CanonicalFockModularIdentificationR10
-- BEGIN EXACT BODY CanonicalFockWeightPolarR4

/-! Actual polar decomposition on the SAME dual-weight GNS.
The root is the positive root of the independently constructed S-adjoint-S
resolvent; transport of the full graphs proves S=J root with equal domains.
No polar identity, traciality, or scaled trace is supplied as a hypothesis. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightPolar
open TGLV350.Regular ChatgptAudit.Continuous049
open F1Rede.BosonicFock F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.CoefficientFockConjugation
open F1Fecho.CanonicalFockCoefficientGraphEquality F1Fecho.CanonicalFockModularIdentification
open F1Fecho.CanonicalFockWeightModularOperator F1Fecho.CanonicalFockWeightClosedTomita
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace

abbrev scalarTomitaPositiveRoot :=
  resolventSquareRoot scalarTomitaResolvent scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective

theorem root_coefficient_graph_iff (x y : RegularHilbert F) :
    (coefficientUnitary x,coefficientUnitary y) ∈ scalarTomitaPositiveRoot.graph ↔
      (x,y) ∈ coefficientRoot.graph := by
  have h := UnitaryRootGraphTransport.root_graph_iff coefficientUnitary coefficientR hR h1 hi x y
  rw [transported_resolvent_eq] at h
  exact h

theorem polar_graph (x y : GNSHilbert) (hxy : (x,y) ∈ scalarTomitaPositiveRoot.graph) :
    (x,scalarTomitaPolarFactor y) ∈ ClosedTomitaSquareGraph.graph actualClosedInput := by
  obtain ⟨u,rfl⟩ := coefficientUnitary.surjective x
  obtain ⟨v,rfl⟩ := coefficientUnitary.surjective y
  have hs := (root_coefficient_graph_iff u v).mp hxy
  obtain ⟨w,hw,hv⟩ := (LinearPMap.mem_graph_iff coefficientRoot).mp hs
  rw [←unitary_graph,scalarTomitaPolarFactor_coefficient]
  refine ⟨(u,coefficientJ v),?_,rfl⟩
  refine ⟨w,Prod.ext hw ?_⟩
  change coefficientJ (coefficientRoot w)=coefficientJ v
  exact congrArg coefficientJ hv

theorem scalarTomitaRootDomain_le_closed : scalarTomitaPositiveRoot.domain ≤ closedTomitaDomain := by
  intro x hx
  have hg := polar_graph x (scalarTomitaPositiveRoot ⟨x,hx⟩)
    ((LinearPMap.mem_graph_iff scalarTomitaPositiveRoot).mpr ⟨⟨x,hx⟩,rfl,rfl⟩)
  obtain ⟨u,hu⟩ := hg
  have he : (u:GNSHilbert)=x := congrArg Prod.fst hu
  rw [←he]
  exact u.property

theorem scalarTomitaPolarFactor_root (x : scalarTomitaPositiveRoot.domain) :
    scalarTomitaPolarFactor (scalarTomitaPositiveRoot x) =
      closedTomita (Submodule.inclusion scalarTomitaRootDomain_le_closed x) := by
  have hg := polar_graph x (scalarTomitaPositiveRoot x)
    ((LinearPMap.mem_graph_iff scalarTomitaPositiveRoot).mpr ⟨x,rfl,rfl⟩)
  obtain ⟨u,hu⟩ := hg
  have he : u=Submodule.inclusion scalarTomitaRootDomain_le_closed x :=
    Subtype.ext (congrArg Prod.fst hu)
  have hs := congrArg Prod.snd hu
  change closedTomita u=scalarTomitaPolarFactor (scalarTomitaPositiveRoot x) at hs
  exact hs.symm.trans (congrArg closedTomita he)

theorem scalarClosedTomitaDomain_le_root : closedTomitaDomain ≤ scalarTomitaPositiveRoot.domain := by
  intro x hx
  have hg : (x,closedTomita ⟨x,hx⟩) ∈ ClosedTomitaSquareGraph.graph actualClosedInput :=
    ⟨⟨x,hx⟩,rfl⟩
  rw [←unitary_graph] at hg
  obtain ⟨p,hp,he⟩ := hg
  obtain ⟨u,hu⟩ := hp
  have hx' : coefficientUnitary (u:RegularHilbert F)=x :=
    (congrArg coefficientUnitary (congrArg Prod.fst hu)).trans (congrArg Prod.fst he)
  have hr := (root_coefficient_graph_iff (u:RegularHilbert F) (coefficientRoot u)).mpr
    ((LinearPMap.mem_graph_iff coefficientRoot).mpr ⟨u,rfl,rfl⟩)
  obtain ⟨v,hv,_⟩ := (LinearPMap.mem_graph_iff scalarTomitaPositiveRoot).mp hr
  have heq : (v:GNSHilbert)=x := hv.trans hx'
  rw [←heq]
  exact v.property

theorem scalarTomitaRootDomain_eq_closed : scalarTomitaPositiveRoot.domain=closedTomitaDomain :=
  le_antisymm scalarTomitaRootDomain_le_closed scalarClosedTomitaDomain_le_root

theorem scalarTomitaPositiveRoot_selfadjoint : IsSelfAdjoint scalarTomitaPositiveRoot :=
  resolventSquareRoot_selfadjoint _ scalarTomitaResolvent_nonneg
    scalarTomitaResolvent_injective scalarTomitaResolvent_le_one

theorem scalarTomitaPositiveRoot_dense : Dense (scalarTomitaPositiveRoot.domain:Set GNSHilbert) :=
  resolventSquareRoot_dense _ scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective

theorem scalarTomitaPositiveRoot_zero_only (x:scalarTomitaPositiveRoot.domain)
    (hz:scalarTomitaPositiveRoot x=0) : (x:GNSHilbert)=0 := by
  have he := scalarTomitaPolarFactor_root x
  rw [hz,map_zero] at he
  have hs : closedTomita (Submodule.inclusion scalarTomitaRootDomain_le_closed x)=0 := he.symm
  have hh := CanonicalFockWeightClosedTomita.involutive
    (Submodule.inclusion scalarTomitaRootDomain_le_closed x)
  have hez : (⟨closedTomita (Submodule.inclusion scalarTomitaRootDomain_le_closed x),
      CanonicalFockWeightClosedTomita.maps_domain _⟩:closedTomitaDomain)=0 := Subtype.ext hs
  rw [hez,map_zero] at hh
  exact hh.symm

theorem scalarTomitaPositiveRoot_denseRange : DenseRange scalarTomitaPositiveRoot.toFun :=
  partialSelfadjoint_denseRange scalarTomitaPositiveRoot scalarTomitaPositiveRoot_dense
    scalarTomitaPositiveRoot_selfadjoint scalarTomitaPositiveRoot_zero_only
end F1Fecho.CanonicalFockWeightPolar
#print axioms F1Fecho.CanonicalFockWeightPolar.root_coefficient_graph_iff
#print axioms F1Fecho.CanonicalFockWeightPolar.polar_graph
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaRootDomain_le_closed
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor_root
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarClosedTomitaDomain_le_root
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaRootDomain_eq_closed
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPositiveRoot_selfadjoint
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPositiveRoot_zero_only
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPositiveRoot_denseRange

-- END EXACT BODY CanonicalFockWeightPolarR4
