import CanonicalFockRightTomitaR2
import CanonicalFockWeightModularOperatorR3
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
