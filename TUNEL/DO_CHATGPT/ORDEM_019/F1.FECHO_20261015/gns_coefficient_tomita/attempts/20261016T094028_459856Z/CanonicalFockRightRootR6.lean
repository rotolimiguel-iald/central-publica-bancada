import GenericRightTomitaResolventR4
import GenericRootDomainTransportR2
import CanonicalFockWeightModularOperatorR3
import CanonicalFockRightTomitaR3

set_option autoImplicit false
noncomputable section
namespace F1Fecho.MappedStarFamily
variable {H A : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [Ring A] [StarRing A] [Algebra ℂ A]
theorem star_inverse_family (π : A →⋆ₐ[ℂ] (H →L[ℂ] H))
    (b : ℝ → A) (hb : ∀ t, star (b t) = b (-t)) (t : ℝ) :
    star (π (star (b t))) = π (star (b (-t))) := by
  simp only [← map_star,star_star,hb,neg_neg]
end F1Fecho.MappedStarFamily

/-! Regular right multiplication commutes with the exact resolvent and its
positive graph square root on the same Fock weight GNS. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRightRoot
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (resolventSquareRoot resolvent_sqrt_graph_transport_of_commute)
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockRegularRightGNS
open F1Fecho.CanonicalFockWeightModularOperator
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockRightTomita
abbrev scalarTomitaPositiveRoot := resolventSquareRoot (H := GNSHilbert) scalarTomitaResolvent
  scalarTomitaResolvent_nonneg scalarTomitaResolvent_injective
/-- Commutation is transferred from the full domain of A to its actual
bounded inverse (I+A)^(-1), using both inverse equations already proved. -/
theorem scalarTomitaResolvent_regular_right_commutes (t : ℝ) :
    Commute scalarTomitaResolvent (regularRightGNS t) := by
  with_reducible
    exact F1Fecho.GenericRightTomitaResolvent.resolvent_commutes
      (H := GNSHilbert) actualClosedInput regularRightGNS
      (fun s => scalarGNSRepresentation (star (regularRightCoreElement s)))
      regularRightGNS_star
      (F1Fecho.MappedStarFamily.star_inverse_family (H := GNSHilbert)
        (A := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) scalarGNSRepresentation
        regularRightCoreElement regularRightCoreElement_star)
      scalarRegularRight_mem_closedTomitaDomain
      scalarClosedTomita_regular_right_intertwines t

theorem scalarTomitaPositiveRoot_regular_right_graph  (t : ℝ)
    (x : (scalarTomitaPositiveRoot ).domain) :
    (regularRightGNS  t (x : GNSHilbert),
      regularRightGNS  t (scalarTomitaPositiveRoot  x)) ∈ (scalarTomitaPositiveRoot ).graph :=
  resolvent_sqrt_graph_transport_of_commute (H := GNSHilbert) (scalarTomitaResolvent ) (regularRightGNS  t)
    (scalarTomitaResolvent_nonneg ) (scalarTomitaResolvent_injective )
    (scalarTomitaResolvent_regular_right_commutes  t) _ _
    ((LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot )).mpr ⟨x,rfl,rfl⟩)

theorem scalarRegularRight_mem_rootDomain (t : ℝ)
    (x : scalarTomitaPositiveRoot.domain) :
    regularRightGNS t (x : GNSHilbert) ∈ scalarTomitaPositiveRoot.domain := by
  with_reducible
    exact GenericRootDomainTransport.domain_map (H := GNSHilbert)
      scalarTomitaResolvent (regularRightGNS t) scalarTomitaResolvent_nonneg
      scalarTomitaResolvent_injective (scalarTomitaResolvent_regular_right_commutes t) x

def scalarRegularRightRootInput (t : ℝ)
    (x : scalarTomitaPositiveRoot.domain) : scalarTomitaPositiveRoot.domain :=
  GenericRootDomainTransport.mappedInput (H := GNSHilbert)
    scalarTomitaResolvent (regularRightGNS t) scalarTomitaResolvent_nonneg
    scalarTomitaResolvent_injective (scalarTomitaResolvent_regular_right_commutes t) x

theorem scalarTomitaPositiveRoot_regular_right_commutes (t : ℝ)
    (x : scalarTomitaPositiveRoot.domain) :
    scalarTomitaPositiveRoot (scalarRegularRightRootInput t x) =
      regularRightGNS t (scalarTomitaPositiveRoot x) := by
  with_reducible
    exact GenericRootDomainTransport.root_map (H := GNSHilbert)
      scalarTomitaResolvent (regularRightGNS t) scalarTomitaResolvent_nonneg
      scalarTomitaResolvent_injective (scalarTomitaResolvent_regular_right_commutes t) x

theorem scalarRegularRight_rootDomain_iff (t : ℝ) (x : GNSHilbert) :
    regularRightGNS t x ∈ scalarTomitaPositiveRoot.domain ↔ x ∈ scalarTomitaPositiveRoot.domain := by
  have hi (y : GNSHilbert) : regularRightGNS (-t) (regularRightGNS t y) = y := by
    change (regularRightGNS (-t) * regularRightGNS t) y = y
    rw [regularRightGNS_mul,neg_add_cancel,regularRightGNS_zero,one_apply_eq_self]
  with_reducible
    exact GenericRootDomainTransport.domain_inverse_iff (H := GNSHilbert)
      scalarTomitaResolvent (regularRightGNS t) scalarTomitaResolvent_nonneg
      scalarTomitaResolvent_injective (scalarTomitaResolvent_regular_right_commutes t)
      (regularRightGNS (-t)) (scalarTomitaResolvent_regular_right_commutes (-t)) hi x


end F1Fecho.CanonicalFockRightRoot
#print axioms F1Fecho.CanonicalFockRightRoot.scalarTomitaResolvent_regular_right_commutes
#print axioms F1Fecho.CanonicalFockRightRoot.scalarTomitaPositiveRoot_regular_right_graph
#print axioms F1Fecho.CanonicalFockRightRoot.scalarRegularRight_mem_rootDomain
#print axioms F1Fecho.CanonicalFockRightRoot.scalarRegularRightRootInput
#print axioms F1Fecho.CanonicalFockRightRoot.scalarTomitaPositiveRoot_regular_right_commutes
#print axioms F1Fecho.CanonicalFockRightRoot.scalarRegularRight_rootDomain_iff

