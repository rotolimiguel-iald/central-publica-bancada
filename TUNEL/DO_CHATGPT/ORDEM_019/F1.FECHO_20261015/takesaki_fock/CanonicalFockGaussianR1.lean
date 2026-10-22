import TGLExt.V350L2GaussianProfile
import CanonicalFockFaithfulWeightR2
import TGLExt.V350DualOrbitVonNeumann
import TGLExt.V350RegularFiniteWeight

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.CanonicalFockGaussian
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
noncomputable section

/-- An auxiliary vector of the existing orbit representation. It is not used
to replace the scalar dual weight or to change the physical input. -/
def scalarGaussianVacuum  :
    RegularHilbert (RegularHilbert (F)) :=
  (gaussianProfile_memLp_vector ((Real.sqrt dualHaarFactor : ℂ) • regularFockVacuum)).toLp
    (fun s : ℝ => (gaussianProfile s : ℂ) •
      ((Real.sqrt dualHaarFactor : ℂ) • regularFockVacuum))

theorem scalarGaussianVacuum_ae  :
    (scalarGaussianVacuum : ℝ → RegularHilbert (F)) =ᵐ[volume]
      fun s => (gaussianProfile s : ℂ) •
        ((Real.sqrt dualHaarFactor : ℂ) • regularFockVacuum) :=
  (gaussianProfile_memLp_vector ((Real.sqrt dualHaarFactor : ℂ) • regularFockVacuum)).coeFn_toLp

/-- A zero Gaussian-weighted orbit has zero unweighted orbit almost everywhere.
Strict positivity is used before any extended integral is evaluated. -/
theorem gaussian_zero_action_orbit_ae 
    (A : RegularHilbert (F) →L[ℂ] RegularHilbert (F))
    (hz : dualOrbitRepresentation A (scalarGaussianVacuum) = 0) :
    (fun s : ℝ => dualAmbient s A (regularFockVacuum)) =ᵐ[volume] 0 := by
  filter_upwards [scalarGaussianVacuum_ae,
    operatorFieldLift_ae (dualIntegralFamily A) (scalarGaussianVacuum),
    Lp.coeFn_zero (RegularHilbert (F)) 2 volume] with s h1 h2 h3
  have he : (gaussianProfile s : ℂ) •
      ((Real.sqrt dualHaarFactor : ℂ) • dualAmbient s A (regularFockVacuum)) = 0 := by
    have h := h2
    change dualOrbitRepresentation A (scalarGaussianVacuum) s =
      dualAmbient s A (scalarGaussianVacuum s) at h
    rw [hz,h3,h1,map_smul,map_smul] at h
    exact h.symm
  have hg : (gaussianProfile s : ℂ) ≠ 0 :=
    Complex.ofReal_ne_zero.mpr (ne_of_gt (gaussianProfile_pos s))
  have hc : (Real.sqrt dualHaarFactor : ℂ) ≠ 0 :=
    Complex.ofReal_ne_zero.mpr (ne_of_gt (Real.sqrt_pos.mpr dualHaarFactor_pos))
  exact (smul_eq_zero.mp ((smul_eq_zero.mp he).resolve_left hg)).resolve_left hc

/-- The Gaussian vector is separating for the concrete image of N, by the
already established faithfulness of the original scalar dual weight. -/
theorem scalarGaussianVacuum_separating 
    (A : RegularHilbert (F) →L[ℂ] RegularHilbert (F))
    (hA : A ∈ core)
    (hz : dualOrbitRepresentation A (scalarGaussianVacuum) = 0) : A = 0 := by
  have ho := gaussian_zero_action_orbit_ae A hz
  have hq : dualQuadraticIntegral (star A * A) (regularFockVacuum) = 0 := by
    simp only [dualQuadraticIntegral,dualQuadraticIntegrand_star_mul]
    have he : (fun s : ℝ => ENNReal.ofReal (‖dualAmbient s A (regularFockVacuum)‖ ^ 2))
        =ᵐ[volume] 0 := by
      filter_upwards [ho] with s hs
      simp only [Pi.zero_apply] at hs
      simp [hs]
    rw [lintegral_congr_ae he]
    simp
  have hm := (core).mul_mem
    ((core).toStarSubalgebra.star_mem' hA) hA
  have hs := (F1Fecho.CanonicalFockFaithfulWeight.weight_faithful
    ⟨star A * A,hm,star_mul_self_nonneg A⟩).mp hq
  exact (CStarRing.star_mul_self_eq_zero_iff A).mp hs

#print axioms scalarGaussianVacuum
#print axioms scalarGaussianVacuum_ae
#print axioms gaussian_zero_action_orbit_ae
#print axioms scalarGaussianVacuum_separating
end
end F1Fecho.CanonicalFockGaussian
