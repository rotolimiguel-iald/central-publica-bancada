import CanonicalFockModularGraphEqualityR1
import ModularTransportTargetR1

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

 theorem target_graph_mem_iff (x y:GNSHilbert) :
    (x,y)∈ClosedTomitaSquareGraph.graph actualClosedInput ↔
      (x,y)∈RegularScalarRealGraph.closedGraph weightContext :=
  Iff.of_eq (congrArg (fun S:Set (GNSHilbert×GNSHilbert)=>(x,y)∈S) target_graph_eq)

 theorem unitary_graph :
    (coefficientUnitary.toHomeomorph.prodCongr coefficientUnitary.toHomeomorph) ''
      CoefficientTomitaSquare.graph coefficientRoot coefficientJ=
        ClosedTomitaSquareGraph.graph actualClosedInput :=
  ModularTransportTarget.graph_image (H := RegularHilbert F) (E := GNSHilbert)
    coefficientUnitary (CoefficientTomitaSquare.graph coefficientRoot coefficientJ)
    (ClosedTomitaSquareGraph.graph actualClosedInput) (fun x y =>
      (target_graph_mem_iff (coefficientUnitary x) (coefficientUnitary y)).trans
        ((coefficientGraph_mem x y).symm.trans
          (Iff.of_eq (congrArg (fun S : Set (RegularHilbert F × RegularHilbert F) => (x,y) ∈ S)
            coefficient_graph_eq_GNS.symm))))

 theorem source_resolvent_mem (x:RegularHilbert F) :
    (coefficientR x,x-coefficientR x)∈antilinearSquareGraph
      (CoefficientTomitaSquare.graph coefficientRoot coefficientJ) := by
  rw [coefficient_square]
  apply (resolvent_graph_equation (H := RegularHilbert F) coefficientR hi
    (coefficientR x) (x-coefficientR x)).mpr
  change coefficientR x-coefficientR (coefficientR x)=coefficientR (x-coefficientR x)
  rw [map_sub]

 theorem resolvent_intertwines (x:RegularHilbert F) :
    coefficientUnitary (coefficientR x)=CanonicalFockWeightModularOperator.scalarTomitaResolvent (coefficientUnitary x) :=
  unitary_recognizes_square_resolvent (H := RegularHilbert F) (K := GNSHilbert) coefficientUnitary _ _ unitary_graph
    coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent source_resolvent_mem
    (ClosedTomitaSquareGraph.resolvent_inverse actualClosedInput) x

 theorem transported_resolvent_eq :
    SpectralTransport.transported (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary coefficientR=CanonicalFockWeightModularOperator.scalarTomitaResolvent :=
  ModularTransportTarget.transported_eq (H := RegularHilbert F) (E := GNSHilbert)
    coefficientUnitary coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent
    resolvent_intertwines

 theorem imaginary_intertwines (t:ℝ) (x:RegularHilbert F) :
    coefficientUnitary (FibreModularCalculus.liftedFlow
      CanonicalFockPolar.modularR CanonicalFockPolar.modularR_nonneg CanonicalFockPolar.modularR_le_one
      CanonicalFockPolar.modularR_injective CanonicalFockPolar.modularR_complement_injective t x)=
        scalarTomitaImaginaryPower t (coefficientUnitary x) :=
  ModularTransportTarget.imaginary_target (H := RegularHilbert F) (E := GNSHilbert)
    coefficientUnitary coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent
    hR h1 hi hj scalarTomitaResolvent_nonneg scalarTomitaResolvent_le_one
    scalarTomitaResolvent_injective
    (F1Fecho.ClosedTomitaFlow.scalarTomitaResolvent_complement_injective actualClosedInput)
    transported_resolvent_eq t x

 theorem actual_modular_implementation (t:ℝ) (y:GNSHilbert) :
    scalarTomitaImaginaryPower t y=regularConjugationGNS t y := by
  calc
    _=scalarTomitaImaginaryPower t (coefficientUnitary (coefficientUnitary.symm y)):=
      congrArg (fun z:GNSHilbert=>scalarTomitaImaginaryPower t z)
        (coefficientUnitary.apply_symm_apply y).symm
    _=coefficientUnitary (FibreModularCalculus.liftedFlow
        CanonicalFockPolar.modularR CanonicalFockPolar.modularR_nonneg CanonicalFockPolar.modularR_le_one
        CanonicalFockPolar.modularR_injective CanonicalFockPolar.modularR_complement_injective
        t (coefficientUnitary.symm y)):=
      (imaginary_intertwines t (coefficientUnitary.symm y)).symm
    _=regularConjugationGNS t (coefficientUnitary (coefficientUnitary.symm y)):=
      cfc_intertwines t (coefficientUnitary.symm y)
    _=regularConjugationGNS t y:=congrArg (regularConjugationGNS t)
      (coefficientUnitary.apply_symm_apply y)

theorem actual_regular_conjugation_norm (t:ℝ) (y:GNSHilbert) :
    ‖regularConjugationGNS t y‖=‖y‖ := by
  exact (congrArg norm (actual_modular_implementation t y)).symm.trans
    ((scalarTomitaImaginaryPower t).norm_map y)

theorem actual_regular_conjugation_group (s t:ℝ) (y:GNSHilbert) :
    regularConjugationGNS s (regularConjugationGNS t y)=regularConjugationGNS (s+t) y := by
  calc
    _=scalarTomitaImaginaryPower s (regularConjugationGNS t y):=
      (actual_modular_implementation s (regularConjugationGNS t y)).symm
    _=scalarTomitaImaginaryPower s (scalarTomitaImaginaryPower t y):=
      congrArg (fun z:GNSHilbert=>scalarTomitaImaginaryPower s z)
        (actual_modular_implementation t y).symm
    _=scalarTomitaImaginaryPower (s+t) y:=scalarTomitaImaginaryPower_add s t y
    _=regularConjugationGNS (s+t) y:=actual_modular_implementation (s+t) y

end F1Fecho.CanonicalFockModularIdentification
#print axioms F1Fecho.CanonicalFockModularIdentification.unitary_graph
#print axioms F1Fecho.CanonicalFockModularIdentification.resolvent_intertwines
#print axioms F1Fecho.CanonicalFockModularIdentification.transported_resolvent_eq
#print axioms F1Fecho.CanonicalFockModularIdentification.imaginary_intertwines
#print axioms F1Fecho.CanonicalFockModularIdentification.actual_modular_implementation

#print axioms F1Fecho.CanonicalFockModularIdentification.actual_regular_conjugation_norm
#print axioms F1Fecho.CanonicalFockModularIdentification.actual_regular_conjugation_group

-- END DERIVED BODY CanonicalFockModularIdentificationR12

-- BEGIN DERIVED BODY CanonicalFockWeightPolarR6

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
  resolventSquareRoot (H := GNSHilbert) CanonicalFockWeightModularOperator.scalarTomitaResolvent scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective

theorem root_coefficient_graph_iff (x y : RegularHilbert F) :
    (coefficientUnitary x,coefficientUnitary y) ∈ scalarTomitaPositiveRoot.graph ↔
      (x,y) ∈ coefficientRoot.graph :=
  ModularTransportTarget.root_target (H := RegularHilbert F) (E := GNSHilbert)
    coefficientUnitary coefficientR CanonicalFockWeightModularOperator.scalarTomitaResolvent
    hR h1 hi scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective
    transported_resolvent_eq x y

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

-- END DERIVED BODY CanonicalFockWeightPolarR6
