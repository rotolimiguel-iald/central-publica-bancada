import CanonicalFockPolarRightAlgebraR6
import CanonicalFockGNSClosednessR5
import CanonicalFockGNSOrderR4
import CanonicalFockRegularRightGNSR11
import GeneralSineResolventApproxR2
import GeneralRegularCutoffCFCR1
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range
import CanonicalFockWeightSandwichR5
import GenericHilbertStarNormOrderR1

-- BEGIN SOURCE CanonicalFockPolarRightClosureR4
/-! Closure, strong-star transport and cutoff consequences on the SAME Fock
GNS. The regular-unitary polar identity remains explicit until its separate
actual polar consumer. Reuses V351 modules as incorporated in v393. -/
/-! Norm closure and ambient functional calculus for the actual polar-right
identity algebra. The antiunitary remains explicit until its concrete polar
consumer; the full-weight embedding is identified by proven cut maps. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (RegularHilbert dualOrbitRepresentation operatorFieldLift dualIntegralFamily operatorFieldLift_norm_le antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNSCuts F1Fecho.CanonicalFockGNSClosedness
open scoped Topology
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
theorem scalarPolarRight_iff_cuts 
    (b : core.toStarSubalgebra) :
    ScalarPolarRight J b ↔ ∀ A : scalarWeightLeftIdeal, ∀ n : ℕ,
      scalarGNSCutMap (n : ℝ)
        (antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)) =
        dualOrbitRepresentation (A.val.val*b.val) (scalarCutVacuum (n : ℝ)) := by
  constructor
  · intro hb A n
    obtain ⟨h,he⟩ := hb A
    rw [← he]
    exact scalarGNSCutMap_weight_embedding (n : ℝ) ⟨A.val*b,h⟩
  · intro h A
    exact scalarWeightGNSEmbedding_of_cut_actions (A.val*b) _ (h A)


/-- Closedness uses bounded cut identities, not a false finite-minorant
characterization of the nontracial weight. -/
theorem scalarPolarRight_isClosed  :
    IsClosed {b : core.toStarSubalgebra | ScalarPolarRight J b} := by
  have hπ : Continuous (scalarGNSRepresentation) := by
    have hb (b : core.toStarSubalgebra) :
        ‖scalarGNSRepresentation b‖ ≤ 1*‖b‖ := by
      rw [one_mul]
      apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg b)
      intro v
      change ‖F1Fecho.RegularScalarGNSAction.scalarGNSAmbientAction weightContext b v.val‖ ≤ ‖b.val‖*‖v.val‖
      exact (ContinuousLinearMap.le_opNorm _ _).trans
        (mul_le_mul_of_nonneg_right (F1Fecho.RegularScalarGNSAction.scalarGNSAmbientAction_norm_le weightContext b) (norm_nonneg v.val))
    have hLip : LipschitzWith 1 (scalarGNSRepresentation) := by
      apply LipschitzWith.of_dist_le_mul
      intro b c
      simpa only [dist_eq_norm, ← map_sub, NNReal.coe_one] using hb (b-c)
    exact hLip.continuous
  have hdual : Continuous (dualOrbitRepresentation (H := F)) := by
    have hb (b : RegularHilbert F →L[ℂ] RegularHilbert F) :
        ‖dualOrbitRepresentation b‖ ≤ 1*‖b‖ := by
      rw [one_mul]
      change ‖operatorFieldLift (dualIntegralFamily b)‖ ≤ (dualIntegralFamily b).bound
      exact operatorFieldLift_norm_le (dualIntegralFamily b)
    exact ((dualOrbitRepresentation (H := F)).toLinearMap.mkContinuous 1 hb).continuous
  have he : {b : core.toStarSubalgebra | ScalarPolarRight J b} =
      ⋂ A : scalarWeightLeftIdeal, ⋂ n : ℕ,
      {b | scalarGNSCutMap (n : ℝ)
        (antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)) =
        dualOrbitRepresentation (A.val.val*b.val) (scalarCutVacuum (n : ℝ))} := by
    ext b
    simp only [Set.mem_setOf_eq,Set.mem_iInter,scalarPolarRight_iff_cuts]
  rw [he]
  apply isClosed_iInter
  intro A
  apply isClosed_iInter
  intro n
  apply isClosed_eq
  · simp only [antiunitaryConjugate_apply]
    exact (scalarGNSCutMap (n : ℝ)).continuous.comp
      (J.continuous.comp
        ((hπ.comp continuous_star).clm_apply continuous_const))
  · exact (hdual.comp (continuous_const.mul continuous_subtype_val)).clm_apply continuous_const

theorem scalarPolarRightAlgebra_isClosed  :
    IsClosed (scalarPolarRightAlgebra J : Set core.toStarSubalgebra) :=
  (scalarPolarRight_isClosed J).inter ((scalarPolarRight_isClosed J).preimage continuous_star)


/-- Consume the ambient CFC, using a norm-closed image of the actual
right-identity algebra. No CFC or completeness of the core subtype is assumed. -/
theorem scalarRightAction_cfc 
    (b : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ core.toStarSubalgebra,
      (⟨cfc f b.val,hf⟩ : core.toStarSubalgebra) ∈
        scalarPolarRightAlgebra J := by
  let E := (scalarPolarRightAlgebra J).map core.toStarSubalgebra.subtype
  have hN : IsClosed (core.toStarSubalgebra : Set (RegularHilbert F →L[ℂ]
      RegularHilbert F)) := by
    change IsClosed (core : Set (RegularHilbert F →L[ℂ] RegularHilbert F))
    rw [← VonNeumannAlgebra.centralizer_centralizer core]
    exact Set.isClosed_centralizer _
  have hE : IsClosed (E : Set (RegularHilbert F →L[ℂ]
      RegularHilbert F)) :=
    hN.isClosedMap_subtype_val _ (scalarPolarRightAlgebra_isClosed J)
  letI := hE
  have hbE : b.val ∈ E := ⟨b,hb,rfl⟩
  have hc : cfc f b.val ∈ E := cfc_mem (𝕜' := ℂ) f hbE
  obtain ⟨d,hd,he⟩ := hc
  have hm : cfc f b.val ∈ core.toStarSubalgebra := he ▸ d.property
  refine ⟨hm,?_⟩
  have heq : d = (⟨cfc f b.val,hm⟩ : core.toStarSubalgebra) := Subtype.ext he
  exact heq ▸ hd


end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_iff_cuts
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_isClosed
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRightAlgebra_isClosed
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightAction_cfc

/-! Preserve the explicit polar-right identity under bounded strong-star limits on the same GNS; the approximants remain explicit inputs. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open scoped Topology
open F1Fecho.CanonicalFockGNSClosedness F1Fecho.CanonicalFockGNSOrder
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
/-- Pass a proved right identity to an actual bounded strong-star limit.
The approximating family is an input, not asserted to exist by this theorem. -/
theorem scalarRightAction_closed_of_bounded_strongStar 
    {ι : Type*} {l : Filter ι} [NeBot l]
    (b : ι → core.toStarSubalgebra)
    (B : core.toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(b i).val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (b i).val x) l (𝓝 (B.val x)))
    (hadjoint : ∀ x, Tendsto (fun i => (star (b i)).val x) l (𝓝 ((star B).val x)))
    (A : scalarWeightLeftIdeal)
    (hact : ∀ i, ∃ hi : A.val * b i ∈ scalarWeightLeftIdeal,
      scalarWeightGNSEmbedding ⟨A.val*b i,hi⟩ =
        antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star (b i))) (scalarWeightGNSEmbedding A)) :
    ∃ hAB : A.val * B ∈ scalarWeightLeftIdeal,
      scalarWeightGNSEmbedding ⟨A.val*B,hAB⟩ =
        antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star B)) (scalarWeightGNSEmbedding A) := by
  let T (i : ι) : scalarWeightLeftIdeal := ⟨A.val*b i,(hact i).choose⟩
  have hnorm (i : ι) : ‖(star (b i)).val‖ ≤ C := by
    change ‖star (b i).val‖ ≤ C
    simpa only [norm_star] using hbound i
  have hp := scalarGNSRepresentation_tendsto_of_uniformly_bounded
    (fun i => star (b i)) (star B) C hnorm hadjoint
      (J.symm (scalarWeightGNSEmbedding A))
  have hj := J.continuous.continuousAt.tendsto.comp hp
  have hgns : Tendsto (fun i => scalarWeightGNSEmbedding (T i)) l
      (𝓝 (antiunitaryConjugate (H := GNSHilbert) J
        (scalarGNSRepresentation (star B)) (scalarWeightGNSEmbedding A))) := by
    have hi (i : ι) : scalarWeightGNSEmbedding (T i) =
        antiunitaryConjugate (H := GNSHilbert) J
          (scalarGNSRepresentation (star (b i))) (scalarWeightGNSEmbedding A) :=
      (hact i).choose_spec
    simp only [Function.comp_def] at hj
    simpa only [hi,antiunitaryConjugate_apply] using hj
  apply scalarWeightGNSEmbedding_closed_of_bounded_strong T (A.val*B) _
    (‖A.val.val‖*C) _ _ hgns
  · intro i
    exact (norm_mul_le A.val.val (b i).val).trans
      (mul_le_mul_of_nonneg_left (hbound i) (norm_nonneg A.val.val))
  · intro x
    exact A.val.val.continuous.continuousAt.tendsto.comp (hstrong x)

end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightAction_closed_of_bounded_strongStar
set_option autoImplicit false
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open MeasureTheory Filter
open TGLV350.Regular (hilbertPositiveSqrt inverseCutoffFunction)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.RegularPositiveFlow
open scoped Topology
/-- An explicit bounded combination of the original regular translations. -/
def regularSineWindowCore (m : ℝ) :
    (core).toStarSubalgebra :=
  (1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
    (regularRightCoreElement (-1/m) - regularRightCoreElement (1/m))

theorem regularSineWindowCore_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (m : ℝ) :
    regularSineWindowCore m ∈ scalarPolarRightAlgebra J := by
  apply (scalarPolarRightAlgebra J).add_mem
  · exact (scalarPolarRightAlgebra J).smul_mem (scalarPolarRightAlgebra J).one_mem _
  · exact (scalarPolarRightAlgebra J).smul_mem ((scalarPolarRightAlgebra J).sub_mem
      (hreg (-1/m))
      (hreg (1/m))) _

theorem regularSineResolvent_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (m : ℝ) :
    ∃ h : regularSineResolvent fockFlow m ∈ core,
      (⟨regularSineResolvent fockFlow m,h⟩ : (core).toStarSubalgebra) ∈
        scalarPolarRightAlgebra J := by
  rw [regularSineResolvent_cfc]
  exact scalarRightAction_cfc J (regularSineWindowCore m)
    (regularSineWindowCore_right J hreg m) _

theorem regularSpectralResolvent_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) :
    (⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩ :
      (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J := by
  let b (n : ℕ) : (core).toStarSubalgebra :=
    ⟨regularSineResolvent fockFlow ((n : ℝ)+1),(regularSineResolvent_right J hreg ((n : ℝ)+1)).choose⟩
  let B : (core).toStarSubalgebra :=
    ⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩
  have hb (n : ℕ) : b n ∈ scalarPolarRightAlgebra J :=
    (regularSineResolvent_right J hreg ((n : ℝ)+1)).choose_spec
  have hs (n : ℕ) : star (b n) = b n :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSineResolvent_nonneg fockFlow ((n : ℝ)+1))).star_eq
  have hB : star B = B :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg fockFlow)).star_eq
  have hright : ScalarPolarRight J B := by
    intro A
    have ha : ∀ x, Tendsto (fun n => (star (b n)).val x) atTop (𝓝 ((star B).val x)) := by
      intro x
      simpa only [hs,hB] using regularSineResolvent_tendsto fockFlow x
    exact scalarRightAction_closed_of_bounded_strongStar J b B 1
      (fun n => regularSineResolvent_norm_le fockFlow ((n : ℝ)+1))
      (fun x => regularSineResolvent_tendsto fockFlow x) ha A (fun n => (hb n).1 A)
  change ScalarPolarRight J B ∧ ScalarPolarRight J (star B)
  rw [hB]
  exact ⟨hright,hright⟩



theorem regularInverseGeneratorCutoff_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (ε : ℝ) (hε : 0 < ε) :
    (⟨regularInverseGeneratorCutoff fockFlow ε,regularInverseGeneratorCutoff_mem fockFlow M ε⟩ :
      (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J := by
  obtain ⟨h,hb⟩ := scalarRightAction_cfc J
    ⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩
    (regularSpectralResolvent_right J hreg) (inverseCutoffFunction ε)
  have he : (⟨regularInverseGeneratorCutoff fockFlow ε,regularInverseGeneratorCutoff_mem fockFlow M ε⟩ :
      (core).toStarSubalgebra) = ⟨cfc (inverseCutoffFunction ε) (regularSpectralResolvent fockFlow),h⟩ :=
    Subtype.ext (regularInverseGeneratorCutoff_cfc fockFlow ε hε)
  rw [he]
  exact hb

/-- Consume the standard real/complex CFC bridges for the original positive
square root; no independent root is introduced. -/
private theorem hilbertPositiveSqrt_complex_cfc
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (h0 : 0 ≤ T) :
    hilbertPositiveSqrt T = cfc (fun z : ℂ => (Real.sqrt z.re : ℂ)) T := by
  rw [hilbertPositiveSqrt,CFC.sqrt_eq_real_sqrt _ h0,
    cfcₙ_eq_cfc Real.continuous_sqrt.continuousOn Real.sqrt_zero,
    cfc_real_eq_complex Real.sqrt (IsSelfAdjoint.of_nonneg h0)]

theorem scalarRightAction_sqrt (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : (core).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (h0 : 0 ≤ b.val) :
    ∃ h : hilbertPositiveSqrt b.val ∈ core,
      (⟨hilbertPositiveSqrt b.val,h⟩ : (core).toStarSubalgebra) ∈
        scalarPolarRightAlgebra J := by
  rw [hilbertPositiveSqrt_complex_cfc _ h0]
  exact scalarRightAction_cfc J b hb _

theorem regularInverseGeneratorCutoff_sqrt_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε) ∈ core,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε),h⟩ :
        (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J :=
  scalarRightAction_sqrt J
    ⟨regularInverseGeneratorCutoff fockFlow ε,regularInverseGeneratorCutoff_mem fockFlow M ε⟩
    (regularInverseGeneratorCutoff_right J hreg ε hε) (regularInverseGeneratorCutoff_nonneg fockFlow ε hε)


end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindowCore
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindowCore_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineResolvent_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSpectralResolvent_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularInverseGeneratorCutoff_right
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightAction_sqrt
#print axioms F1Fecho.CanonicalFockPolarRight.regularInverseGeneratorCutoff_sqrt_right

-- END SOURCE CanonicalFockPolarRightClosureR4

-- BEGIN SOURCE CanonicalFockRightCommutationR1
/-! The proved polar right identity commutes with the actual Fock left action.
No commutant equality or polar factor identification is assumed here. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockWeightSandwich F1Fecho.CanonicalFockRegular
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
theorem scalarPolarRight_commutes_left
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra) (hb : ScalarPolarRight J b)
    (c : core.toStarSubalgebra) :
    Commute (antiunitaryConjugate (H := GNSHilbert) J (scalarGNSRepresentation (star b)))
      (scalarGNSRepresentation c) := by
  let R := antiunitaryConjugate (H := GNSHilbert) J (scalarGNSRepresentation (star b))
  have hcore (A : scalarWeightLeftIdeal) :
      R (scalarGNSRepresentation c (scalarWeightGNSEmbedding A)) =
        scalarGNSRepresentation c (R (scalarWeightGNSEmbedding A)) := by
    obtain ⟨hAb,heAb⟩ := hb A
    let Ab : scalarWeightLeftIdeal := ⟨A.val*b,hAb⟩
    obtain ⟨hcAb,hecAb⟩ := hb (scalarWeightLeftProduct c A)
    have he : (⟨(scalarWeightLeftProduct c A).val*b,hcAb⟩ : scalarWeightLeftIdeal) =
        scalarWeightLeftProduct c Ab := Subtype.ext (mul_assoc c A.val b)
    calc
      _ = R (scalarWeightGNSEmbedding (scalarWeightLeftProduct c A)) :=
        congrArg R (scalarWeightGNSAction_intertwines c A)
      _ = scalarWeightGNSEmbedding ⟨(scalarWeightLeftProduct c A).val*b,hcAb⟩ :=
        hecAb.symm
      _ = scalarWeightGNSEmbedding (scalarWeightLeftProduct c Ab) :=
        congrArg scalarWeightGNSEmbedding he
      _ = scalarGNSRepresentation c (scalarWeightGNSEmbedding Ab) :=
        (scalarWeightGNSAction_intertwines c Ab).symm
      _ = _ := congrArg (scalarGNSRepresentation c) heAb
  ext1 x
  exact scalarWeightGNSEmbedding_denseRange.induction_on x
    (isClosed_eq (R.continuous.comp (scalarGNSRepresentation c).continuous)
      ((scalarGNSRepresentation c).continuous.comp R.continuous)) hcore
end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarPolarRight_commutes_left

-- END SOURCE CanonicalFockRightCommutationR1

-- BEGIN SOURCE CanonicalFockPerturbedWeightOrderR3
/-! Right perturbation norm and order in the actual Fock full-weight ideal.
The existing v393 calculation is specialized directly to avoid instance diamonds.
J and right membership remain explicit until the actual polar consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxErrors 3
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLV350.Regular (dualQuadraticIntegral antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightCompletion F1Fecho.CanonicalFockGNSOrder
open F1Fecho.CanonicalFockWeightSandwich
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
theorem scalarWeight_right_perturbed_norm (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val * (star A.val.val * A.val.val) * b.val)
      regularFockVacuum =
    ENNReal.ofReal (‖scalarGNSRepresentation (star b)
      (J.symm (scalarWeightGNSEmbedding A))‖^2) := by
  obtain ⟨hAb, he⟩ := hb.1 A
  calc
    _ = ENNReal.ofReal (‖scalarWeightGNSEmbedding ⟨A.val*b,hAb⟩‖^2) := by
      have hn := scalarWeightGNSEmbedding_norm_sq ⟨A.val*b,hAb⟩
      change ENNReal.ofReal (‖scalarWeightGNSEmbedding ⟨A.val*b,hAb⟩‖^2) =
        dualQuadraticIntegral (star (A.val.val*b.val)*(A.val.val*b.val))
          regularFockVacuum at hn
      simpa only [star_mul, mul_assoc] using hn.symm
    _ = ENNReal.ofReal (‖antiunitaryConjugate (H := GNSHilbert) J
        (scalarGNSRepresentation (star b)) (scalarWeightGNSEmbedding A)‖^2) :=
      congrArg (fun v : GNSHilbert => ENNReal.ofReal (‖v‖^2)) he
    _ = _ := congrArg (fun r : ℝ => ENNReal.ofReal (r^2))
      (J.norm_map
        (scalarGNSRepresentation (star b)
          (J.symm (scalarWeightGNSEmbedding A))))


theorem scalarWeight_right_perturbed_mono (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b c : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (hc : c ∈ scalarPolarRightAlgebra J)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      regularFockVacuum ≤
    dualQuadraticIntegral (star c.val * (star A.val.val*A.val.val) * c.val)
      regularFockVacuum := by
  rw [scalarWeight_right_perturbed_norm J b hb A,
    scalarWeight_right_perturbed_norm J c hc A]
  apply ENNReal.ofReal_le_ofReal
  have ho := scalarGNSRepresentation_monotone hbc
  have hp : scalarGNSRepresentation b * star (scalarGNSRepresentation b) ≤
      scalarGNSRepresentation c * star (scalarGNSRepresentation c) := by
    simpa only [map_mul,map_star] using ho
  have hn := F1Fecho.GenericHilbertStarNormOrder.star_apply_norm_sq_mono (scalarGNSRepresentation b)
    (scalarGNSRepresentation c) hp
    (J.symm (scalarWeightGNSEmbedding A))
  simpa only [map_star] using hn

end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_norm
#print axioms F1Fecho.CanonicalFockPolarRight.scalarWeight_right_perturbed_mono

-- END SOURCE CanonicalFockPerturbedWeightOrderR3
