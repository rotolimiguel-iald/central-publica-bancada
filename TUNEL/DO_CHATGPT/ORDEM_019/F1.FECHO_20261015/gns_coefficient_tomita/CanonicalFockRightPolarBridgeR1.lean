import CanonicalFockRightTomitaR2
import CanonicalFockModularBridgeR3
import CanonicalFockPolarRightAlgebraR2
import TGLExt.V350ResolventGraphTransport
/-! Consolidated right-action consumers, preserving the prepared statements,
with one import pass. All statements concern the same actual GNS. -/
/-! The actual maximal adjoint and S-adjoint-S commute with regular right
multiplication on their full domains. Reuse of the incorporated v393 proof,
instantiated at the already constructed Fock GNS closed operator. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRightSquare
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightClosedTomita
open F1Fecho.CanonicalFockRightTomita F1Fecho.CanonicalFockWeightModularOperator
abbrev scalarTomitaAdjointDomain := F1Fecho.ClosedTomitaOperator.scalarTomitaAdjointDomain actualClosedInput
abbrev scalarTomitaSquareDomain := F1Fecho.ClosedTomitaOperator.scalarTomitaSquareDomain actualClosedInput
abbrev scalarTomitaSquareInput := F1Fecho.ClosedTomitaOperator.scalarTomitaSquareInput actualClosedInput
abbrev scalarTomitaSquareAdjointInput := F1Fecho.ClosedTomitaOperator.scalarTomitaSquareAdjointInput actualClosedInput
/-- The closed-S intertwining determines a relation for its maximal adjoint.
The left operator is pi(y), while the right operator is the Hilbert adjoint
of R_y. This uses every vector in D(S), not only the algebraic core. -/
theorem scalarRegularRightTomitaAdjoint_pairing  (t : ℝ) (z : scalarTomitaAdjointDomain )
    (x : closedTomitaDomain) :
    inner ℂ (closedTomita x)
      (scalarGNSRepresentation  (regularRightCoreElement  t) z) =
    inner ℂ (star (regularRightGNS  t) (scalarTomitaAdjoint  z))
      (x : GNSHilbert) := by
  have hp : (scalarGNSRepresentation  (regularRightCoreElement  t)).adjoint =
      scalarGNSRepresentation  (star (regularRightCoreElement  t)) :=
    (map_star (scalarGNSRepresentation ) (regularRightCoreElement  t)).symm
  calc
    _ = inner ℂ
        ((scalarGNSRepresentation  (regularRightCoreElement  t)).adjoint
          (closedTomita x)) (z : GNSHilbert) :=
      ((scalarGNSRepresentation  (regularRightCoreElement  t)).adjoint_inner_left _ _).symm
    _ = inner ℂ
        (scalarGNSRepresentation  (star (regularRightCoreElement  t))
          (closedTomita x)) (z : GNSHilbert) :=
      congrArg (fun T : GNSHilbert →L[ℂ] GNSHilbert =>
        inner ℂ (T (closedTomita x)) (z : GNSHilbert)) hp
    _ = inner ℂ (closedTomita (scalarRegularRightClosedTomitaInput  t x))
        (z : GNSHilbert) :=
      congrArg (fun v : GNSHilbert => inner ℂ v (z : GNSHilbert))
        (scalarClosedTomita_regular_right_intertwines  t x).symm
    _ = inner ℂ (scalarTomitaAdjoint  z)
        (regularRightGNS  t (x : GNSHilbert)) :=
      F1Fecho.ClosedTomitaOperator.scalarTomitaAdjoint_pairing actualClosedInput z (scalarRegularRightClosedTomitaInput  t x)
    _ = _ := ((regularRightGNS  t).adjoint_inner_left _ _).symm

theorem scalarRegularRightTomitaAdjoint_maximal  (t : ℝ) (z : scalarTomitaAdjointDomain ) :
    ∃ hz : scalarGNSRepresentation  (regularRightCoreElement  t) z ∈
        scalarTomitaAdjointDomain ,
      scalarTomitaAdjoint 
        ⟨scalarGNSRepresentation  (regularRightCoreElement  t) z,hz⟩ =
      star (regularRightGNS  t) (scalarTomitaAdjoint  z) :=
  F1Fecho.ClosedTomitaOperator.scalarTomitaAdjoint_maximal actualClosedInput (scalarRegularRightTomitaAdjoint_pairing  t z)

def scalarRegularRightTomitaAdjointInput  (t : ℝ) (z : scalarTomitaAdjointDomain ) :
    scalarTomitaAdjointDomain  :=
  ⟨scalarGNSRepresentation  (regularRightCoreElement  t) z,
    (scalarRegularRightTomitaAdjoint_maximal  t z).choose⟩

theorem scalarTomitaAdjoint_regular_left_intertwines  (t : ℝ) (z : scalarTomitaAdjointDomain ) :
    scalarTomitaAdjoint  (scalarRegularRightTomitaAdjointInput  t z) =
      star (regularRightGNS  t) (scalarTomitaAdjoint  z) :=
  (scalarRegularRightTomitaAdjoint_maximal  t z).choose_spec

theorem scalarRegularRightSquare_S_image  (t : ℝ)
    (x : scalarTomitaSquareDomain ) :
    closedTomita (scalarRegularRightClosedTomitaInput  t (scalarTomitaSquareInput  x)) =
      scalarGNSRepresentation  (regularRightCoreElement  (-t))
        (scalarTomitaSquareAdjointInput  x : GNSHilbert) := by
  rw [scalarClosedTomita_regular_right_intertwines,regularRightCoreElement_star]
  rfl

theorem scalarRegularRight_mem_squareDomain  (t : ℝ)
    (x : scalarTomitaSquareDomain ) :
    regularRightGNS  t (x : GNSHilbert) ∈ scalarTomitaSquareDomain  := by
  refine ⟨scalarRegularRight_mem_closedTomitaDomain  t (scalarTomitaSquareInput  x),?_⟩
  change closedTomita
    (scalarRegularRightClosedTomitaInput  t (scalarTomitaSquareInput  x)) ∈ scalarTomitaAdjointDomain 
  rw [scalarRegularRightSquare_S_image]
  exact (scalarRegularRightTomitaAdjointInput  (-t) (scalarTomitaSquareAdjointInput  x)).property

def scalarRegularRightSquareInput  (t : ℝ)
    (x : scalarTomitaSquareDomain ) : scalarTomitaSquareDomain  :=
  ⟨regularRightGNS  t (x : GNSHilbert),scalarRegularRight_mem_squareDomain  t x⟩

/-- The SAME positive selfadjoint A=S†S commutes on its entire composition
 domain with right multiplication by the regular unitary lambda_t. -/
theorem scalarTomitaSquare_regular_right_commutes  (t : ℝ)
    (x : scalarTomitaSquareDomain ) :
    scalarTomitaSquare  (scalarRegularRightSquareInput  t x) =
      regularRightGNS  t (scalarTomitaSquare  x) := by
  have hi : scalarTomitaSquareAdjointInput  (scalarRegularRightSquareInput  t x) =
      scalarRegularRightTomitaAdjointInput  (-t) (scalarTomitaSquareAdjointInput  x) := by
    apply Subtype.ext
    exact scalarRegularRightSquare_S_image  t x
  calc
    _ = scalarTomitaAdjoint 
        (scalarTomitaSquareAdjointInput  (scalarRegularRightSquareInput  t x)) := rfl
    _ = scalarTomitaAdjoint 
        (scalarRegularRightTomitaAdjointInput  (-t) (scalarTomitaSquareAdjointInput  x)) :=
      congrArg (scalarTomitaAdjoint ) hi
    _ = star (regularRightGNS  (-t))
        (scalarTomitaAdjoint  (scalarTomitaSquareAdjointInput  x)) :=
      scalarTomitaAdjoint_regular_left_intertwines  (-t) (scalarTomitaSquareAdjointInput  x)
    _ = _ := by rw [regularRightGNS_star,neg_neg]; rfl

/-- The inverse is the already constructed right action at -t. -/
theorem scalarRegularRight_squareDomain_iff  (t : ℝ)
    (x : GNSHilbert) :
    regularRightGNS  t x ∈ scalarTomitaSquareDomain  ↔ x ∈ scalarTomitaSquareDomain  := by
  constructor
  · intro hx
    have h := scalarRegularRight_mem_squareDomain  (-t) ⟨regularRightGNS  t x,hx⟩
    change (regularRightGNS  (-t) * regularRightGNS  t) x ∈ scalarTomitaSquareDomain  at h
    simpa only [regularRightGNS_mul,neg_add_cancel,regularRightGNS_zero,
      ContinuousLinearMap.one_apply] using h
  · intro hx
    exact scalarRegularRight_mem_squareDomain  t ⟨x,hx⟩


end F1Fecho.CanonicalFockRightSquare
#print axioms F1Fecho.CanonicalFockRightSquare.scalarRegularRightTomitaAdjoint_pairing
#print axioms F1Fecho.CanonicalFockRightSquare.scalarRegularRightTomitaAdjoint_maximal
#print axioms F1Fecho.CanonicalFockRightSquare.scalarRegularRightTomitaAdjointInput
#print axioms F1Fecho.CanonicalFockRightSquare.scalarTomitaAdjoint_regular_left_intertwines
#print axioms F1Fecho.CanonicalFockRightSquare.scalarRegularRightSquare_S_image
#print axioms F1Fecho.CanonicalFockRightSquare.scalarRegularRight_mem_squareDomain
#print axioms F1Fecho.CanonicalFockRightSquare.scalarRegularRightSquareInput
#print axioms F1Fecho.CanonicalFockRightSquare.scalarTomitaSquare_regular_right_commutes
#print axioms F1Fecho.CanonicalFockRightSquare.scalarRegularRight_squareDomain_iff

/-! Regular right multiplication commutes with the exact resolvent and its
positive graph square root on the same Fock weight GNS. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRightRoot
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (resolventSquareRoot resolvent_sqrt_graph_transport_of_commute)
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

/-! The actual polar conjugation exchanges regular left and right multiplication. Uses the dense range of the proved positive root, not an input right-action identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRightPolar
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open scoped Topology
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightClosedTomita
open F1Fecho.CanonicalFockRightTomita F1Fecho.CanonicalFockWeightPolar
open F1Fecho.CanonicalFockPolarRight
open F1Fecho.CanonicalFockRightRoot (scalarRegularRightRootInput scalarTomitaPositiveRoot_regular_right_commutes)
/-- The actual polar antiunitary exchanges this right action with left
multiplication. The extension uses the dense image of the SAME positive root. -/
theorem scalarTomitaPolarFactor_regular_right  (t : ℝ)
    (z : GNSHilbert) :
    scalarTomitaPolarFactor (regularRightGNS t z) =
      scalarGNSRepresentation (star (regularRightCoreElement t))
        (scalarTomitaPolarFactor z) := by
  refine (scalarTomitaPositiveRoot_denseRange).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) z
  rintro _ ⟨x,rfl⟩
  have he : Submodule.inclusion (scalarTomitaRootDomain_le_closed)
      (scalarRegularRightRootInput t x) =
    scalarRegularRightClosedTomitaInput t
      (Submodule.inclusion (scalarTomitaRootDomain_le_closed) x) := Subtype.ext rfl
  calc
    _ = scalarTomitaPolarFactor
        (scalarTomitaPositiveRoot (scalarRegularRightRootInput t x)) :=
      congrArg (scalarTomitaPolarFactor) (scalarTomitaPositiveRoot_regular_right_commutes t x).symm
    _ = closedTomita (Submodule.inclusion (scalarTomitaRootDomain_le_closed)
        (scalarRegularRightRootInput t x)) := scalarTomitaPolarFactor_root _
    _ = closedTomita (scalarRegularRightClosedTomitaInput t
        (Submodule.inclusion (scalarTomitaRootDomain_le_closed) x)) :=
      congrArg (closedTomita) he
    _ = scalarGNSRepresentation (star (regularRightCoreElement t))
        (closedTomita (Submodule.inclusion (scalarTomitaRootDomain_le_closed) x)) :=
      scalarClosedTomita_regular_right_intertwines t _
    _ = _ := congrArg (scalarGNSRepresentation (star (regularRightCoreElement t)))
      (scalarTomitaPolarFactor_root x).symm

theorem scalarTomitaPolar_conjugate_regular_right  (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor) (regularRightGNS t) =
      scalarGNSRepresentation (star (regularRightCoreElement t)) := by
  apply ContinuousLinearMap.ext
  intro x
  have h := scalarTomitaPolarFactor_regular_right t ((scalarTomitaPolarFactor).symm x)
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.apply_symm_apply] using h

theorem scalarTomitaPolarFactor_regular_left  (t : ℝ)
    (z : GNSHilbert) :
    scalarTomitaPolarFactor
      (scalarGNSRepresentation (star (regularRightCoreElement t)) z) =
        regularRightGNS t (scalarTomitaPolarFactor z) := by
  have h := congrArg (scalarTomitaPolarFactor)
    (scalarTomitaPolarFactor_regular_right t (scalarTomitaPolarFactor z))
  simpa only [scalarTomitaPolarFactor_involutive z,
    scalarTomitaPolarFactor_involutive (regularRightGNS t (scalarTomitaPolarFactor z))] using h.symm

/-- The previously constructed right translation is the original polar right
action on every vector in the full scalar-weight ideal. -/
theorem scalarRightAction_regular  (t : ℝ)
    (A : scalarWeightLeftIdeal) :
    scalarWeightGNSEmbedding (scalarRegularRightProduct t A) =
      antiunitaryConjugate (scalarTomitaPolarFactor)
        (scalarGNSRepresentation (star (regularRightCoreElement t)))
          (scalarWeightGNSEmbedding A) := by
  rw [← regularRightGNS_intertwines,antiunitaryConjugate_apply,
    scalarTomitaPolarFactor_regular_left,LinearIsometryEquiv.apply_symm_apply]

theorem scalarPolarRightAlgebra_regular_mem (t : ℝ) :
    regularRightCoreElement t ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor := by
  have h (s : ℝ) : ScalarPolarRight scalarTomitaPolarFactor (regularRightCoreElement s) := by
    intro A
    exact ⟨(scalarRegularRightProduct s A).property,scalarRightAction_regular s A⟩
  exact ⟨h t,by simpa only [regularRightCoreElement_star] using h (-t)⟩
end F1Fecho.CanonicalFockRightPolar
#print axioms F1Fecho.CanonicalFockRightPolar.scalarTomitaPolarFactor_regular_right
#print axioms F1Fecho.CanonicalFockRightPolar.scalarTomitaPolar_conjugate_regular_right
#print axioms F1Fecho.CanonicalFockRightPolar.scalarTomitaPolarFactor_regular_left
#print axioms F1Fecho.CanonicalFockRightPolar.scalarRightAction_regular
#print axioms F1Fecho.CanonicalFockRightPolar.scalarPolarRightAlgebra_regular_mem
