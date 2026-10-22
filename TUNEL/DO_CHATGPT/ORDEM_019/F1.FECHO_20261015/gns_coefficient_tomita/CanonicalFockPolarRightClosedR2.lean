import CanonicalFockPolarRightAlgebraR1
import CanonicalFockGNSClosednessR3
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range
/-! Norm closure and ambient functional calculus for the actual polar-right
identity algebra. The antiunitary remains explicit until its concrete polar
consumer; the full-weight embedding is identified by proven cut maps. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
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
        (antiunitaryConjugate J
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
        (antiunitaryConjugate J
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
