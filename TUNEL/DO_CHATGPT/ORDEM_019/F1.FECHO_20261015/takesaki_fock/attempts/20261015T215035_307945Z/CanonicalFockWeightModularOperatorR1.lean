import CanonicalFockWeightClosedTomitaR2
import TGLExt.V350AntilinearAdjointGraph
import TGLExt.V350AntilinearComposition
import TGLExt.V350ClosedAntilinearResolvent
import TGLExt.V350PositiveSurjectiveResolvent
import TGLExt.V350PartialPositiveResolvent
import TGLExt.V351ResolventImaginaryContinuity
/-! The positive selfadjoint operator S_nu^* S_nu and its bounded resolvent
on the actual scalar dual-weight GNS space. Its domain is the exact adjoint
composition domain. No equality with regular or geometric modular flow is
inserted; the scalar weight is not called a scaled trace. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightModularOperator
open TGLExt TGLV350.Regular
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightClosedTomita
abbrev scalarClosedTomitaDomain := closedTomitaDomain
abbrev scalarClosedTomita := closedTomita
 theorem scalarClosedTomita_domain_dense : Dense (scalarClosedTomitaDomain : Set GNSHilbert) := domain_dense
 theorem scalarClosedTomita_is_closed : IsClosed (Set.range (fun x : scalarClosedTomitaDomain => ((x:GNSHilbert),scalarClosedTomita x))) := graph_closed
 theorem scalarClosedTomita_maps_domain (x:scalarClosedTomitaDomain) : scalarClosedTomita x ∈ scalarClosedTomitaDomain := maps_domain x
 theorem scalarClosedTomita_involutive (x:scalarClosedTomitaDomain) : scalarClosedTomita ⟨scalarClosedTomita x,scalarClosedTomita_maps_domain x⟩ = x := involutive x
def scalarTomitaAdjointDomain : Submodule ℂ (GNSHilbert) :=
  maximalAntilinearAdjointDomain (scalarClosedTomitaDomain) (scalarClosedTomita)

/-- The maximal complex-antilinear adjoint of the same closed operator on H_I. -/
def scalarTomitaAdjoint : GNSHilbert →ₛₗ.[starRingEnd ℂ] GNSHilbert :=
  maximalAntilinearAdjoint (scalarClosedTomitaDomain) (scalarClosedTomita)
    (scalarClosedTomita_domain_dense )

theorem scalarTomitaAdjoint_pairing (y : scalarTomitaAdjointDomain)
    (x : scalarClosedTomitaDomain) :
    inner ℂ (scalarClosedTomita x) (y : GNSHilbert) =
      inner ℂ (scalarTomitaAdjoint y) (x : GNSHilbert) :=
  maximalAntilinearAdjoint_pairing _ _ _ y x

theorem scalarTomitaAdjoint_maximal {y z : GNSHilbert}
    (h : ∀ x : scalarClosedTomitaDomain,
      inner ℂ (scalarClosedTomita x) y = inner ℂ z (x : GNSHilbert)) :
    ∃ hy : y ∈ scalarTomitaAdjointDomain, scalarTomitaAdjoint ⟨y,hy⟩ = z :=
  maximalAntilinearAdjoint_maximal _ _ _ h

theorem scalarTomitaAdjoint_domain_iff (y : GNSHilbert) :
    y ∈ scalarTomitaAdjointDomain ↔ ∃ z : GNSHilbert,
      ∀ x : scalarClosedTomitaDomain,
        inner ℂ (scalarClosedTomita x) y = inner ℂ z (x : GNSHilbert) := Iff.rfl

theorem scalarTomitaAdjoint_isClosed :
    IsClosed (Set.range (fun y : scalarTomitaAdjointDomain =>
      ((y : GNSHilbert),scalarTomitaAdjoint y))) :=
  maximalAntilinearAdjoint_isClosed _ _ _


/-- The composition domain is exactly x in D(S) with Sx in D(S†). -/
def scalarTomitaSquareDomain : Submodule ℂ (GNSHilbert) :=
  antilinearPreimageDomain (scalarClosedTomitaDomain) (scalarTomitaAdjointDomain)
    (scalarClosedTomita)

def scalarTomitaSquareInput : scalarTomitaSquareDomain →ₗ[ℂ]
    scalarClosedTomitaDomain :=
  antilinearPreimageInput _ _ _

theorem scalarTomitaSquareInput_coe (x : scalarTomitaSquareDomain) :
    (scalarTomitaSquareInput x : GNSHilbert) = x := rfl

theorem scalarTomitaSquareInput_image_mem (x : scalarTomitaSquareDomain) :
    scalarClosedTomita (scalarTomitaSquareInput x) ∈ scalarTomitaAdjointDomain :=
  antilinearPreimageInput_mem _ _ _ x

def scalarTomitaSquareAdjointInput : scalarTomitaSquareDomain →ₛₗ[starRingEnd ℂ]
    scalarTomitaAdjointDomain :=
  antilinearPreimageMap _ _ _

/-- The actual complex-linear composition. Self-adjointness is not part of
this definition and must be proved separately. -/
def scalarTomitaSquare : GNSHilbert →ₗ.[ℂ] GNSHilbert where
  domain := scalarTomitaSquareDomain
  toFun := (antilinearComposite (scalarClosedTomitaDomain) (scalarTomitaAdjointDomain)
    (scalarClosedTomita) (scalarTomitaAdjoint).toFun).toFun

theorem scalarTomitaSquare_domain_iff (x : GNSHilbert) :
    x ∈ (scalarTomitaSquare).domain ↔
      ∃ hx : x ∈ scalarClosedTomitaDomain,
        scalarClosedTomita ⟨x,hx⟩ ∈ scalarTomitaAdjointDomain := Iff.rfl

theorem scalarTomitaSquare_apply (x : scalarTomitaSquareDomain) :
    scalarTomitaSquare x = scalarTomitaAdjoint
      ⟨scalarClosedTomita (scalarTomitaSquareInput x),
        scalarTomitaSquareInput_image_mem x⟩ := rfl

theorem scalarTomitaSquare_pairing (x : scalarTomitaSquareDomain)
    (y : scalarClosedTomitaDomain) :
    inner ℂ (scalarTomitaSquare x) (y : GNSHilbert) =
      inner ℂ (scalarClosedTomita y)
        (scalarClosedTomita (scalarTomitaSquareInput x)) :=
  (scalarTomitaAdjoint_pairing (scalarTomitaSquareAdjointInput x) y).symm

theorem scalarTomitaSquare_symmetric :
    (scalarTomitaSquare).IsFormalAdjoint (scalarTomitaSquare) := by
  intro x y
  calc
    _ = inner ℂ (scalarClosedTomita (scalarTomitaSquareInput y))
        (scalarClosedTomita (scalarTomitaSquareInput x)) :=
      scalarTomitaSquare_pairing x (scalarTomitaSquareInput y)
    _ = (starRingEnd ℂ) (inner ℂ
        (scalarClosedTomita (scalarTomitaSquareInput x))
        (scalarClosedTomita (scalarTomitaSquareInput y))) :=
      (inner_conj_symm (𝕜 := ℂ)
        (scalarClosedTomita (scalarTomitaSquareInput y))
        (scalarClosedTomita (scalarTomitaSquareInput x))).symm
    _ = (starRingEnd ℂ) (inner ℂ (scalarTomitaSquare y) (x : GNSHilbert)) :=
      congrArg (starRingEnd ℂ)
        (scalarTomitaSquare_pairing y (scalarTomitaSquareInput x)).symm
    _ = _ := inner_conj_symm (𝕜 := ℂ) (x : GNSHilbert) (scalarTomitaSquare y)

theorem scalarTomitaSquare_quadratic (x : scalarTomitaSquareDomain) :
    (inner ℂ (x : GNSHilbert) (scalarTomitaSquare x)).re =
      ‖scalarClosedTomita (scalarTomitaSquareInput x)‖^2 := by
  calc
    _ = (inner ℂ (scalarTomitaSquare x) (x : GNSHilbert)).re :=
      inner_re_symm (𝕜 := ℂ) (x : GNSHilbert) (scalarTomitaSquare x)
    _ = (inner ℂ (scalarClosedTomita (scalarTomitaSquareInput x))
        (scalarClosedTomita (scalarTomitaSquareInput x))).re :=
      congrArg Complex.re (scalarTomitaSquare_pairing x (scalarTomitaSquareInput x))
    _ = _ := (norm_sq_eq_re_inner (𝕜 := ℂ)
      (scalarClosedTomita (scalarTomitaSquareInput x))).symm

theorem scalarTomitaSquare_positive (x : scalarTomitaSquareDomain) :
    0 ≤ (inner ℂ (x : GNSHilbert) (scalarTomitaSquare x)).re := by
  rw [scalarTomitaSquare_quadratic]
  exact sq_nonneg _

#print axioms scalarTomitaSquareDomain
#print axioms scalarTomitaSquareInput
#print axioms scalarTomitaSquareInput_coe
#print axioms scalarTomitaSquareInput_image_mem
#print axioms scalarTomitaSquareAdjointInput
#print axioms scalarTomitaSquare
#print axioms scalarTomitaSquare_domain_iff
#print axioms scalarTomitaSquare_apply
#print axioms scalarTomitaSquare_pairing
#print axioms scalarTomitaSquare_symmetric
#print axioms scalarTomitaSquare_quadratic
#print axioms scalarTomitaSquare_positive

/-- The full range of I+S†S is obtained from the same closed graph of S. -/
theorem scalarTomitaSquare_resolvent_surjective (z : GNSHilbert) :
    ∃ x : (scalarTomitaSquare).domain,
      (x : GNSHilbert)+scalarTomitaSquare x=z := by
  obtain ⟨x,hx⟩ := closedAntilinear_complex_resolvent
    (scalarClosedTomitaDomain) (scalarClosedTomita)
    (scalarClosedTomita_is_closed ) z
  obtain ⟨hy,hval⟩ := scalarTomitaAdjoint_maximal hx
  let w : scalarTomitaSquareDomain := ⟨(x : GNSHilbert),x.property,hy⟩
  refine ⟨w,?_⟩
  change (x : GNSHilbert)+scalarTomitaAdjoint ⟨scalarClosedTomita x,hy⟩=z
  rw [hval]
  abel

theorem scalarTomitaSquare_domain_dense :
    Dense ((scalarTomitaSquare).domain : Set (GNSHilbert)) :=
  positive_surjective_resolvent_domain_dense (scalarTomitaSquare)
    (scalarTomitaSquare_positive) (scalarTomitaSquare_resolvent_surjective)

/-- Actual self-adjointness on the composition domain, not a separate model. -/
theorem scalarTomitaSquare_selfadjoint : IsSelfAdjoint (scalarTomitaSquare) :=
  positive_surjective_resolvent_selfadjoint (scalarTomitaSquare)
    (scalarTomitaSquare_positive) (scalarTomitaSquare_resolvent_surjective)
    (scalarTomitaSquare_symmetric)

theorem scalarTomitaSquare_isClosed : (scalarTomitaSquare).IsClosed :=
  (scalarTomitaSquare_selfadjoint).isClosed

theorem scalarClosedTomita_zero_only (x : scalarClosedTomitaDomain)
    (hz : scalarClosedTomita x=0) : (x : GNSHilbert)=0 := by
  have hh : (⟨scalarClosedTomita x,scalarClosedTomita_maps_domain x⟩ :
      scalarClosedTomitaDomain)=0 := Subtype.ext hz
  have hi := scalarClosedTomita_involutive x
  rw [hh,map_zero] at hi
  exact hi.symm

/-- The positive self-adjoint composition has no zero vector in its kernel
apart from zero; no spectral gap is asserted. -/
theorem scalarTomitaSquare_zero_only (x : (scalarTomitaSquare).domain)
    (hz : scalarTomitaSquare x=0) : (x : GNSHilbert)=0 := by
  have hq := scalarTomitaSquare_quadratic x
  rw [hz,inner_zero_right] at hq
  have hn : ‖scalarClosedTomita (scalarTomitaSquareInput x)‖=0 :=
    (sq_eq_zero_iff).mp hq.symm
  exact scalarClosedTomita_zero_only (scalarTomitaSquareInput x) (norm_eq_zero.mp hn)

#print axioms scalarTomitaSquare_resolvent_surjective
#print axioms scalarTomitaSquare_domain_dense
#print axioms scalarTomitaSquare_selfadjoint
#print axioms scalarTomitaSquare_isClosed
#print axioms scalarClosedTomita_zero_only
#print axioms scalarTomitaSquare_zero_only

/-- A bounded resolvent of the actual S†S, on the same scalar GNS Hilbert space. -/
def scalarTomitaResolvent : GNSHilbert →L[ℂ] GNSHilbert :=
  partialPositiveResolvent (scalarTomitaSquare) (scalarTomitaSquare_positive)
    (scalarTomitaSquare_resolvent_surjective)

theorem scalarTomitaResolvent_equation (z : GNSHilbert) :
    ∃ x : (scalarTomitaSquare).domain,
      (x : GNSHilbert)=scalarTomitaResolvent z ∧
        (x : GNSHilbert)+scalarTomitaSquare x=z :=
  partialPositiveResolvent_equation _ _ _ z

theorem scalarTomitaResolvent_inverse (x : (scalarTomitaSquare).domain) :
    scalarTomitaResolvent ((x : GNSHilbert)+scalarTomitaSquare x)=
      (x : GNSHilbert) :=
  partialPositiveResolvent_inverse _ _ _ x

theorem scalarTomitaResolvent_norm_le (z : GNSHilbert) :
    ‖scalarTomitaResolvent z‖ ≤ ‖z‖ := partialPositiveResolvent_norm_le _ _ _ z

theorem scalarTomitaResolvent_injective : Function.Injective (scalarTomitaResolvent) :=
  partialPositiveResolvent_injective _ _ _

theorem scalarTomitaResolvent_nonneg : 0 ≤ scalarTomitaResolvent :=
  partialPositiveResolvent_nonneg _ _ _ (scalarTomitaSquare_symmetric)

theorem scalarTomitaResolvent_le_one : scalarTomitaResolvent ≤ 1 :=
  partialPositiveResolvent_le_one _ _ _ (scalarTomitaSquare_symmetric)

theorem scalarTomitaResolvent_selfadjoint : IsSelfAdjoint (scalarTomitaResolvent) :=
  IsSelfAdjoint.of_nonneg (scalarTomitaResolvent_nonneg)

/-- Equality as partial maps includes the exact composition domain. -/
theorem scalarTomitaResolvent_graph :
    resolventGraphOperator (scalarTomitaResolvent) (scalarTomitaResolvent_injective) =
      scalarTomitaSquare :=
  partialPositiveResolvent_graph _ _ _

#print axioms scalarTomitaResolvent
#print axioms scalarTomitaResolvent_equation
#print axioms scalarTomitaResolvent_inverse
#print axioms scalarTomitaResolvent_norm_le
#print axioms scalarTomitaResolvent_injective
#print axioms scalarTomitaResolvent_nonneg
#print axioms scalarTomitaResolvent_le_one
#print axioms scalarTomitaResolvent_selfadjoint
#print axioms scalarTomitaResolvent_graph

#print axioms scalarTomitaAdjoint
#print axioms scalarTomitaAdjoint_pairing
#print axioms scalarTomitaAdjoint_maximal
#print axioms scalarTomitaAdjoint_isClosed
end F1Fecho.CanonicalFockWeightModularOperator
