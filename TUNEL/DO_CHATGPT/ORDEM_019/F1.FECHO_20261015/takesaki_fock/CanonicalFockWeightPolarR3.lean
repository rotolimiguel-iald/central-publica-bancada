import CanonicalFockWeightPolarBasicsR2
import CanonicalFockModularIdentificationR9
import UnitaryRootGraphTransportR1
import TGLExt.V350PartialSelfadjointRange

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
