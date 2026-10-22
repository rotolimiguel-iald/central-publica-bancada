import CanonicalFockGNSClosednessR3
import CanonicalFockGNSOrderR1
import CanonicalFockPolarRightAlgebraR1
/-! Preserve the explicit polar-right identity under bounded strong-star limits on the same GNS; the approximants remain explicit inputs. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open scoped Topology
open F1Fecho.CanonicalFockGNSClosedness F1Fecho.CanonicalFockGNSOrder
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
/--ass a proved right identity to an actual bounded strong-star limit.
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
        antiunitaryConjugate J
          (scalarGNSRepresentation (star (b i))) (scalarWeightGNSEmbedding A)) :
    ∃ hAB : A.val * B ∈ scalarWeightLeftIdeal,
      scalarWeightGNSEmbedding ⟨A.val*B,hAB⟩ =
        antiunitaryConjugate J
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
      (𝓝 (antiunitaryConjugate J
        (scalarGNSRepresentation (star B)) (scalarWeightGNSEmbedding A))) := by
    have hi (i : ι) : scalarWeightGNSEmbedding (T i) =
        antiunitaryConjugate J
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
