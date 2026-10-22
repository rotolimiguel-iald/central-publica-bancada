import CanonicalFockFiniteProjectionR3
import CanonicalFockMatrixCornerR2

/-! DECLARADO / UNCOMPILED CANDIDATE, R51, 2026-10-16.
Composition of the actual Fock corner, finite subprojection and existing
inverse-supremum tracial law. Reuses the proof of V354FiniteEqualSplit and
V354NormalizedSplit with the actual Fock suppliers, never SiteProfile.
The trace normalization is performed by the actual dual action. No corner,
finite projection, type-II property, equality of halves, or trace law is an
input to the final existence theorems. The two imported R51 suppliers have
terminal EXIT0 receipts. This consumer remains DECLARADO and uncompiled; it
does not claim a total cyclic trace or a complete RemainingModularCoreInput.
Require EXIT0 and all three public axiom reports. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockNormalizedSplitR4
open TGLExt TGLV350.Regular
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeight (PositiveInput add positiveDual)
open F1Fecho.CanonicalFockInverseSupremum (value value_dual)
open F1Fecho.CanonicalFockActualInverseAdditivityR2 (value_add)
open F1Fecho.CanonicalFockActualPositiveTracePackageR2 (positiveSquare value_tracial)
open F1Fecho.CanonicalFockFiniteProjectionR3 (finite_subprojection_exists dual_calibration)
open F1Fecho.CanonicalFockMatrixCornerR2 (core_matrix_corner)
open scoped ENNReal

/- All star-ring rewrites occur here, on a generic Hilbert space. The
concrete Fock theorem below only specializes these identities. The double
star form of the returned projection matches positiveSquare (star a)
definitionally, without a concrete adjoint rewrite. -/
private theorem compressed_corner_algebra {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (e v q : H →L[ℂ] H) (hq : IsStarProjection q)
    (hv : star v*v=e) (hev : e*v=0) (hqe : q*e=q) :
    star (v*q)*(v*q)=q ∧
      IsStarProjection (star (star (v*q))*star (v*q)) ∧
      q*(star (star (v*q))*star (v*q))=0 := by
  let a := v*q
  have hqs := hq.isSelfAdjoint.star_eq
  have hqq : q*q=q := hq.isIdempotentElem
  have ha2 : star a*a=q := by
    change star (v*q)*(v*q)=q
    calc
      _ = q*(star v*v)*q := by rw [star_mul,hqs]; noncomm_ring
      _ = q := by rw [hv,hqe,hqq]
  have haq : a*q=a := by
    change (v*q)*q=v*q
    rw [mul_assoc,hqq]
  have hqv : q*v=0 := by
    calc
      _ = (q*e)*v := by rw [hqe]
      _ = 0 := by rw [mul_assoc,hev,mul_zero]
  have hqa : q*a=0 := by
    change q*(v*q)=0
    rw [← mul_assoc,hqv,zero_mul]
  have hr : IsStarProjection (a*star a) := by
    constructor
    · change (a*star a)*(a*star a)=a*star a
      calc
        _ = a*(star a*a)*star a := by noncomm_ring
        _ = a*star a := by rw [ha2,haq]
    · change star (a*star a)=a*star a
      rw [star_mul,star_star]
  have hqr : q*(a*star a)=0 := by
    rw [← mul_assoc,hqa,zero_mul]
  refine ⟨ha2,?_,?_⟩
  · simpa only [star_star] using hr
  · simpa only [star_star] using hqr

private theorem mapped_orthogonal {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (phi : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (q r : H →L[ℂ] H) (hqr : q*r=0) : phi q * phi r = 0 := by
  calc
    _ = phi (q*r) := (map_mul phi q r).symm
    _ = phi 0 := congrArg phi hqr
    _ = 0 := map_zero phi

private abbrev AmbientHilbert := RegularHilbert F1Rede.BosonicFock.F
private abbrev ambientNormedAddCommGroup : NormedAddCommGroup AmbientHilbert := inferInstance
private abbrev ambientInnerProductSpace : InnerProductSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientNormedSpace : NormedSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientModule : Module ℂ AmbientHilbert := inferInstance
private abbrev ambientTopologicalSpace : TopologicalSpace AmbientHilbert := inferInstance
private abbrev ambientUniformSpace : UniformSpace AmbientHilbert := inferInstance
private abbrev ambientCompleteSpace : CompleteSpace AmbientHilbert := inferInstance
private abbrev ambientStar : Star (AmbientHilbert →L[ℂ] AmbientHilbert) := inferInstance
private abbrev ambientOrder : PartialOrder (AmbientHilbert →L[ℂ] AmbientHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := AmbientHilbert)
attribute [local instance] ambientNormedAddCommGroup ambientInnerProductSpace
  ambientNormedSpace ambientModule ambientTopologicalSpace ambientUniformSpace
  ambientCompleteSpace ambientStar ambientOrder

#eval IO.println "R51_SPLIT begin actual finite equal split"
theorem finite_equal_split :
    ∃ q r : PositiveInput,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      value q=value r ∧ 0<value q ∧ value q<⊤ := by
  obtain ⟨e,v,he,hene,hv,hev⟩ := core_matrix_corner
  obtain ⟨q,hq,hpos,hfin,hqe⟩ := finite_subprojection_exists e he hene
  let a : core.toStarSubalgebra := v*⟨q.val,q.property.1⟩
  let r := positiveSquare (star a)
  have hcomp : star a.val*a.val=q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 :=
    @compressed_corner_algebra AmbientHilbert ambientNormedAddCommGroup
      ambientInnerProductSpace ambientCompleteSpace e.val v.val q.val hq hv hev hqe
  have ht : value q=value r := by
    have hA : positiveSquare a=q := Subtype.ext hcomp.1
    simpa only [hA] using value_tracial a
  exact ⟨q,r,hq,hcomp.2.1,hcomp.2.2,ht,hpos,hfin⟩
#print axioms finite_equal_split

/-- The sum is a positive finite projection with equal positive faces. -/
theorem finite_split_support :
    ∃ q r : PositiveInput,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      IsStarProjection (add q r).val ∧ 0<value (add q r) ∧ value (add q r)<⊤ ∧
      value q=value r ∧ 0<value q := by
  obtain ⟨q,r,hq,hr,hqr,ht,hpos,hfin⟩ := finite_equal_split
  refine ⟨q,r,hq,hr,hqr,hq.add hr hqr,?_,?_,ht,hpos⟩
  · rw [value_add]
    exact hpos.trans_le (le_add_right le_rfl)
  · rw [value_add,← ht]
    exact ENNReal.add_lt_top.mpr ⟨hfin,hfin⟩
#print axioms finite_split_support

#eval IO.println "R51_SPLIT begin actual dual normalization"
/-- Exact positive-data interface for PF=Q+R in RemainingModularCoreInput. -/
theorem normalized_split_exists :
    ∃ q r : PositiveInput,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      value (add q r)=1 ∧ value q=value r := by
  obtain ⟨q,r,hq,hr,hqr,_,hpos,hfin,ht,_⟩ := finite_split_support
  let s := Real.log (value (add q r)).toReal
  let Q := positiveDual s q
  let R := positiveDual s r
  have hQ : IsStarProjection Q.val := hq.map (dualAmbient s)
  have hR : IsStarProjection R.val := hr.map (dualAmbient s)
  have hQR : Q.val*R.val=0 :=
    @mapped_orthogonal AmbientHilbert ambientNormedAddCommGroup
      ambientInnerProductSpace ambientCompleteSpace (dualAmbient s) q.val r.val hqr
  have hadd : add Q R=positiveDual s (add q r) := by
    apply Subtype.ext
    change dualAmbient s q.val + dualAmbient s r.val=dualAmbient s (q.val+r.val)
    exact (map_add (dualAmbient s) q.val r.val).symm
  refine ⟨Q,R,hQ,hR,hQR,?_,?_⟩
  · rw [hadd]
    exact dual_calibration (add q r) hpos hfin
  · change value (positiveDual s q)=value (positiveDual s r)
    rw [value_dual,value_dual,ht]
#print axioms normalized_split_exists

end F1Fecho.CanonicalFockNormalizedSplitR4
