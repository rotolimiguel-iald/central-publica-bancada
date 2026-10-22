import ExponentialVectorsR1
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule

/-! Totality is derived by uniqueness of a scalar analytic power series and by
the actual closed-span definition of each existing symmetric sector. No density
assumption, alternative Fock space, or nonzero placeholder is introduced. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open Filter Topology UniformSpace
namespace F1Fecho.Exponential
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock

theorem component_smul (z : ℂ) (x : H1) (n : ℕ) :
    component (z • x) n = z^n • component x n := by
  simp only [component, pureTensor_smul, smul_smul]
  rw [mul_comm]

def coefficient (v : F) (x : H1) (n : ℕ) : ℂ :=
  inner ℂ (v n) (component x n)

theorem scalar_series (v : F) (x : H1) (z : ℂ) :
    HasSum (fun n => z^n * coefficient v x n) (inner ℂ v (exponential (z • x))) := by
  have hs := lp.hasSum_inner v (exponential (z • x))
  simpa only [exponential_apply, component_smul, inner_smul_right, coefficient] using hs

theorem coefficients_zero_of_orthogonal (v : F)
    (hv : ∀ x : H1, inner ℂ v (exponential x) = 0) (x : H1) (n : ℕ) :
    coefficient v x n = 0 := by
  let p := FormalMultilinearSeries.ofScalars ℂ (coefficient v x)
  have hp : HasFPowerSeriesAt (0 : ℂ → ℂ) p 0 := by
    apply hasFPowerSeriesAt_iff.mpr
    apply Filter.Eventually.of_forall
    intro z
    simpa only [p, FormalMultilinearSeries.coeff_ofScalars, smul_eq_mul, Pi.zero_apply,
      hv] using scalar_series v x z
  have he := hp.apply_eq_zero n (1 : ℂ)
  simpa only [p, FormalMultilinearSeries.ofScalars_apply_eq, one_pow, smul_eq_mul,
    mul_one] using he

theorem pure_inner_zero_of_orthogonal (v : F)
    (hv : ∀ x : H1, inner ℂ v (exponential x) = 0) (x : H1) (n : ℕ) :
    inner ℂ (v n) (pureTensor n x) = 0 := by
  have h := coefficients_zero_of_orthogonal v hv x n
  unfold coefficient component at h
  rw [inner_smul_right] at h
  exact (mul_eq_zero.mp h).resolve_left (by exact_mod_cast (ne_of_gt (weight_pos n)))

theorem sector_eq_zero_of_pure_inner_zero (n : ℕ) (v : Sector n)
    (hv : ∀ x : H1, inner ℂ v (pureTensor n x) = 0) : v = 0 := by
  let f : TensorHilbert n →L[ℂ] ℂ := innerSL ℂ (v : TensorHilbert n)
  have hspan : algebraicSymmetricSpan n ≤ LinearMap.ker f.toLinearMap := by
    apply Submodule.span_le.mpr
    rintro _ ⟨x, rfl⟩
    change inner ℂ (v : TensorHilbert n) (pureCompleted n x) = 0
    exact hv x
  have hclosure : symmetricSpace n ≤ LinearMap.ker f.toLinearMap :=
    (algebraicSymmetricSpan n).topologicalClosure_minimal hspan f.isClosed_ker
  have he : inner ℂ (v : TensorHilbert n) (v : TensorHilbert n) = 0 :=
    hclosure v.property
  apply Subtype.ext
  exact inner_self_eq_zero.mp he

theorem exponential_orthogonal_zero (v : F)
    (hv : ∀ x : H1, inner ℂ v (exponential x) = 0) : v = 0 := by
  ext n
  exact sector_eq_zero_of_pure_inner_zero n (v n)
    (fun x => pure_inner_zero_of_orthogonal v hv x n)

theorem exponential_total :
    (Submodule.span ℂ (Set.range exponential)).topologicalClosure = ⊤ := by
  apply Submodule.topologicalClosure_eq_top_iff.mpr
  apply le_antisymm _ bot_le
  intro v hv
  apply Submodule.mem_bot.mpr
  apply exponential_orthogonal_zero v
  intro x
  exact (Submodule.mem_orthogonal' _ v).mp hv (exponential x)
    (Submodule.subset_span ⟨x, rfl⟩)

end F1Fecho.Exponential

#print axioms F1Fecho.Exponential.scalar_series
#print axioms F1Fecho.Exponential.coefficients_zero_of_orthogonal
#print axioms F1Fecho.Exponential.sector_eq_zero_of_pure_inner_zero
#print axioms F1Fecho.Exponential.exponential_orthogonal_zero
#print axioms F1Fecho.Exponential.exponential_total
