import CanonicalFockGNSRepresentationR6
import CanonicalFockWeightCompletionR5
import TGLExt.V350AntiunitaryPositiveConjugation
/-! The full-weight polar-right identity for an explicit antiunitary on the
same Fock GNS space. The algebraic closure laws are proved. Identifying J with
the actual Tomita polar factor, and supplying concrete members, are separate consumers. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open scoped Topology
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
/-- The actual polar right identity on the existing full weight domain. -/
def ScalarPolarRight  (b : core.toStarSubalgebra) : Prop :=
  ∀ A : scalarWeightLeftIdeal, ∃ h : A.val*b ∈ scalarWeightLeftIdeal,
    scalarWeightGNSEmbedding ⟨A.val*b,h⟩ =
      antiunitaryConjugate J
        (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)

theorem scalarPolarRight_zero  : ScalarPolarRight J 0 := by
  intro A
  have h : A.val*0 ∈ scalarWeightLeftIdeal := by simp
  refine ⟨h,?_⟩
  have he : (⟨A.val*0,h⟩ : scalarWeightLeftIdeal) = 0 := Subtype.ext (mul_zero _)
  rw [he,map_zero,antiunitaryConjugate_apply,star_zero,map_zero]
  simp only [zero_apply,map_zero]

theorem scalarPolarRight_one  : ScalarPolarRight J 1 := by
  intro A
  have h : A.val*1 ∈ scalarWeightLeftIdeal := by simpa only [mul_one] using A.property
  refine ⟨h,?_⟩
  have he : (⟨A.val*1,h⟩ : scalarWeightLeftIdeal) = A := Subtype.ext (mul_one _)
  rw [he,antiunitaryConjugate_apply,star_one,map_one]
  simp only [one_apply_eq_self,LinearIsometryEquiv.apply_symm_apply]

theorem scalarPolarRight_add 
    (b c : core.toStarSubalgebra)
    (hb : ScalarPolarRight J b) (hc : ScalarPolarRight J c) : ScalarPolarRight J (b+c) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  obtain ⟨hAc,hec⟩ := hc A
  have h : A.val*(b+c) ∈ scalarWeightLeftIdeal := by
    simpa only [mul_add] using (scalarWeightLeftIdeal).add_mem hAb hAc
  refine ⟨h,?_⟩
  have he : (⟨A.val*(b+c),h⟩ : scalarWeightLeftIdeal) =
      (⟨A.val*b,hAb⟩ : scalarWeightLeftIdeal) + ⟨A.val*c,hAc⟩ :=
    Subtype.ext (mul_add _ _ _)
  rw [he,map_add,heb,hec]
  simp only [antiunitaryConjugate_apply,star_add,map_add,add_apply]

theorem scalarPolarRight_smul 
    (b : core.toStarSubalgebra) (hb : ScalarPolarRight J b) (c : ℂ) :
    ScalarPolarRight J (c • b) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  have h : A.val*(c • b) ∈ scalarWeightLeftIdeal := by
    simpa only [mul_smul_comm] using (scalarWeightLeftIdeal).smul_mem c hAb
  refine ⟨h,?_⟩
  have he : (⟨A.val*(c • b),h⟩ : scalarWeightLeftIdeal) =
      c • (⟨A.val*b,hAb⟩ : scalarWeightLeftIdeal) := Subtype.ext (mul_smul_comm _ _ _)
  rw [he,map_smul,heb]
  simp only [antiunitaryConjugate_apply,star_smul,map_smul,
    smul_apply,LinearIsometryEquiv.map_smulₛₗ,starRingEnd_apply,star_star]

theorem scalarPolarRight_mul 
    (b c : core.toStarSubalgebra)
    (hb : ScalarPolarRight J b) (hc : ScalarPolarRight J c) : ScalarPolarRight J (b*c) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  obtain ⟨hAbc,hec⟩ := hc ⟨A.val*b,hAb⟩
  have h : A.val*(b*c) ∈ scalarWeightLeftIdeal := by
    simpa only [mul_assoc] using hAbc
  refine ⟨h,?_⟩
  have he : (⟨A.val*(b*c),h⟩ : scalarWeightLeftIdeal) =
      ⟨(A.val*b)*c,hAbc⟩ := Subtype.ext (mul_assoc _ _ _).symm
  rw [he,hec,heb]
  simp only [antiunitaryConjugate_apply,star_mul,map_mul,mul_apply_eq_comp,
    LinearIsometryEquiv.symm_apply_apply]

/-- The two-sided star condition is explicit; it is not silently inferred
from a right-boundedness condition on b alone. -/
def scalarPolarRightAlgebra  :
    StarSubalgebra ℂ core.toStarSubalgebra where
  carrier := {b | ScalarPolarRight J b ∧ ScalarPolarRight J (star b)}
  zero_mem' := by simpa only [Set.mem_setOf_eq,star_zero] using And.intro (scalarPolarRight_zero J) (scalarPolarRight_zero J)
  one_mem' := by simpa only [Set.mem_setOf_eq,star_one] using And.intro (scalarPolarRight_one J) (scalarPolarRight_one J)
  add_mem' := by
    intro b c hb hc
    exact ⟨scalarPolarRight_add J b c hb.1 hc.1,
      by simpa only [star_add] using scalarPolarRight_add J (star b) (star c) hb.2 hc.2⟩
  mul_mem' := by
    intro b c hb hc
    exact ⟨scalarPolarRight_mul J b c hb.1 hc.1,
      by simpa only [star_mul] using scalarPolarRight_mul J (star c) (star b) hc.2 hb.2⟩
  algebraMap_mem' c := by
    have h := scalarPolarRight_smul J 1 (scalarPolarRight_one J) c
    have hs := scalarPolarRight_smul J 1 (scalarPolarRight_one J) (star c)
    simpa only [Set.mem_setOf_eq,Algebra.algebraMap_eq_smul_one,star_smul,star_one] using And.intro h hs
  star_mem' := by
    intro b hb
    exact ⟨hb.2,by simpa only [star_star] using hb.1⟩


end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.ScalarPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_zero
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_one
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_add
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_smul
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_mul
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRightAlgebra
