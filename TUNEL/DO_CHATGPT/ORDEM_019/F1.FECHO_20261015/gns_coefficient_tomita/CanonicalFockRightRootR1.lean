import CanonicalFockRightSquareR1
import TGLExt.V350ResolventGraphTransport
/-! Regular right multiplication commutes with the exact resolvent and its
positive graph square root on the same Fock weight GNS. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRightRoot
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockRegularRightGNS
open F1Fecho.CanonicalFockWeightModularOperator F1Fecho.CanonicalFockRightSquare
abbrev scalarTomitaPositiveRoot := resolventSquareRoot scalarTomitaResolvent
  scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective
/-- Commutation is transferred from the full domain of A to its actual
bounded inverse (I+A)^(-1), using both inverse equations already proved. -/
theorem scalarTomitaResolvent_regular_right_commutes  (t : ℝ) :
    Commute (scalarTomitaResolvent ) (regularRightGNS  t) := by
  apply ContinuousLinearMap.ext
  intro z
  obtain ⟨x,hx,he⟩ := scalarTomitaResolvent_equation  z
  calc
    _ = scalarTomitaResolvent 
        (regularRightGNS  t ((x : GNSHilbert)+scalarTomitaSquare  x)) := by rw [he]; rfl
    _ = scalarTomitaResolvent 
        ((scalarRegularRightSquareInput  t x : GNSHilbert)+
          scalarTomitaSquare  (scalarRegularRightSquareInput  t x)) := by
      rw [map_add,scalarTomitaSquare_regular_right_commutes]
      rfl
    _ = (scalarRegularRightSquareInput  t x : GNSHilbert) :=
      scalarTomitaResolvent_inverse  _
    _ = _ := congrArg (regularRightGNS  t) hx

theorem scalarTomitaPositiveRoot_regular_right_graph  (t : ℝ)
    (x : (scalarTomitaPositiveRoot ).domain) :
    (regularRightGNS  t (x : GNSHilbert),
      regularRightGNS  t (scalarTomitaPositiveRoot  x)) ∈ (scalarTomitaPositiveRoot ).graph :=
  resolvent_sqrt_graph_transport_of_commute (scalarTomitaResolvent ) (regularRightGNS  t)
    (scalarTomitaResolvent_nonneg ) (scalarTomitaResolvent_injective )
    (scalarTomitaResolvent_regular_right_commutes  t) _ _
    ((LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot )).mpr ⟨x,rfl,rfl⟩)

theorem scalarRegularRight_mem_rootDomain  (t : ℝ)
    (x : (scalarTomitaPositiveRoot ).domain) :
    regularRightGNS  t (x : GNSHilbert) ∈ (scalarTomitaPositiveRoot ).domain := by
  obtain ⟨u,hu,_⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot )).mp
    (scalarTomitaPositiveRoot_regular_right_graph  t x)
  change (u : GNSHilbert)=regularRightGNS  t (x : GNSHilbert) at hu
  rw [← hu]
  exact u.property

def scalarRegularRightRootInput  (t : ℝ)
    (x : (scalarTomitaPositiveRoot ).domain) : (scalarTomitaPositiveRoot ).domain :=
  ⟨regularRightGNS  t (x : GNSHilbert),scalarRegularRight_mem_rootDomain  t x⟩

theorem scalarTomitaPositiveRoot_regular_right_commutes  (t : ℝ)
    (x : (scalarTomitaPositiveRoot ).domain) :
    scalarTomitaPositiveRoot  (scalarRegularRightRootInput  t x) =
      regularRightGNS  t (scalarTomitaPositiveRoot  x) := by
  obtain ⟨u,hu,hBu⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot )).mp
    (scalarTomitaPositiveRoot_regular_right_graph  t x)
  have he : scalarRegularRightRootInput  t x=u := Subtype.ext hu.symm
  rw [he]
  exact hBu

theorem scalarRegularRight_rootDomain_iff  (t : ℝ)
    (x : GNSHilbert) :
    regularRightGNS  t x ∈ (scalarTomitaPositiveRoot ).domain ↔
      x ∈ (scalarTomitaPositiveRoot ).domain := by
  constructor
  · intro hx
    have h := scalarRegularRight_mem_rootDomain  (-t) ⟨regularRightGNS  t x,hx⟩
    change (regularRightGNS  (-t) * regularRightGNS  t) x ∈ _ at h
    simpa only [regularRightGNS_mul,neg_add_cancel,regularRightGNS_zero,
      one_apply_eq_self] using h
  · intro hx
    exact scalarRegularRight_mem_rootDomain  t ⟨x,hx⟩


end F1Fecho.CanonicalFockRightRoot
#print axioms F1Fecho.CanonicalFockRightRoot.scalarTomitaResolvent_regular_right_commutes
#print axioms F1Fecho.CanonicalFockRightRoot.scalarTomitaPositiveRoot_regular_right_graph
#print axioms F1Fecho.CanonicalFockRightRoot.scalarRegularRight_mem_rootDomain
#print axioms F1Fecho.CanonicalFockRightRoot.scalarRegularRightRootInput
#print axioms F1Fecho.CanonicalFockRightRoot.scalarTomitaPositiveRoot_regular_right_commutes
#print axioms F1Fecho.CanonicalFockRightRoot.scalarRegularRight_rootDomain_iff
