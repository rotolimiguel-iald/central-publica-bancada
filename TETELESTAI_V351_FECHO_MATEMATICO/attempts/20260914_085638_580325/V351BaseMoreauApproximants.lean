import TGLExt.V351ExtendedBaseDualWeight
import TGLExt.V350DualEnergyOnResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV351
open TGLExt TGLV350.Regular Filter
open scoped Topology ENNReal NNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The minimum energy is the bounded quadratic form of I-R. -/
theorem dualResolvent_minimum_energy_value
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) :
    dualEnergy A v (R v) = ENNReal.ofReal (inner ℂ v ((1-R) v)).re := by
  have hf : dualQuadraticIntegral A (R v) ≠ ⊤ :=
    ne_of_lt (dualResolvent_limit_range_finite A R hA hlim v)
  have he := dualResolvent_limit_energy_identity A R hA hlim v
  have hq : dualQuadraticIntegral A (R v) =
      ENNReal.ofReal (inner ℂ (R v) (v-R v)).re := by
    rw [← he]
    exact (ENNReal.ofReal_toReal hf).symm
  have hp : 0 ≤ (inner ℂ (R v) (v-R v)).re := by
    rw [← he]
    exact ENNReal.toReal_nonneg
  unfold dualEnergy
  rw [hq, ← ENNReal.ofReal_add (sq_nonneg _) hp]
  congr 1
  simp only [ContinuousLinearMap.sub_apply, one_apply_eq_self, inner_sub_right,
    Complex.sub_re, norm_sub_sq (𝕜 := ℂ)]
  rw [inner_self_eq_norm_sq, inner_self_eq_norm_sq]
  rw [inner_re_symm (𝕜 := ℂ) v (R v)]
  ring

/-- A positive bounded operator in the original base represents each Moreau
minimum of the actual dual form. The minimizing vector remains in the same
regular Hilbert space. No bounded-output assumption is imposed on q_A. -/
theorem exists_base_moreau_approximant (P : SiteProfile) (A : PositiveCoreInput P)
    (c : ℝ) (hc : 0 < c) :
    ∃ D : TowerHilbert P →L[ℂ] TowerHilbert P,
      D ∈ theFactorObject P ∧ 0 ≤ D ∧ D ≤ (c : ℂ) • 1 ∧
      ∀ v : RegularHilbert (TowerHilbert P), ∃ w : RegularHilbert (TowerHilbert P),
        ENNReal.ofReal (inner ℂ v (fibre D v)).re =
          ENNReal.ofReal (c * ‖w-v‖^2) + dualQuadraticIntegral A.val w ∧
        ∀ z : RegularHilbert (TowerHilbert P),
          ENNReal.ofReal (inner ℂ v (fibre D v)).re ≤
            ENNReal.ofReal (c * ‖z-v‖^2) + dualQuadraticIntegral A.val z := by
  let A' := A.scale ⟨c⁻¹, (inv_pos.mpr hc).le⟩
  obtain ⟨R, hmR, hR, hone, hlim, hfix⟩ :=
    exists_dualResolvent_fixed P A'.val A'.property.1 A'.property.2
  let B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) :=
    (c : ℂ) • (1-R)
  have hRF : R ∈ dualFixedCore P := (dualFixedCore_mem_iff P R).mpr ⟨hmR,hfix⟩
  have hBF : B ∈ dualFixedCore P :=
    (dualFixedCore P).toStarSubalgebra.smul_mem
      ((dualFixedCore P).sub_mem (dualFixedCore P).one_mem hRF) (c : ℂ)
  have hB : 0 ≤ B := by
    rw [ContinuousLinearMap.nonneg_iff_isPositive]
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
      (sub_nonneg.mpr hone)).smul_of_nonneg (by exact_mod_cast hc.le)
  have hBbound : B ≤ (c : ℂ) • 1 := by
    rw [← sub_nonneg]
    have he : (c : ℂ) • (1 : RegularHilbert (TowerHilbert P) →L[ℂ] _) - B = (c : ℂ) • R := by
      dsimp [B]
      rw [smul_sub]
      abel
    rw [he, ContinuousLinearMap.nonneg_iff_isPositive]
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hR).smul_of_nonneg
      (by exact_mod_cast hc.le)
  obtain ⟨D, hD, hBD⟩ := (dualFixedCore_eq_amplified_base P B).mp hBF
  refine ⟨D,hD,(fibre_nonneg_iff D).mp (hBD ▸ hB),?_,?_⟩
  · apply (fibre_le_iff D ((c : ℂ) • 1)).mp
    have hf : fibre ((c : ℂ) • (1 : TowerHilbert P →L[ℂ] _)) = (c : ℂ) • 1 := by
      change fibre ((c : ℂ) • (1 : TowerHilbert P →L[ℂ] _)) = (c : ℂ) • 1
      rw [fibre_smul, fibre_one]
    rw [hf, ← hBD]
    exact hBbound
  · intro v
    have he : ENNReal.ofReal (inner ℂ v (fibre D v)).re =
        ENNReal.ofReal c * dualEnergy A'.val v (R v) := by
      rw [dualResolvent_minimum_energy_value A'.val R A'.property.2 hlim v, ← hBD]
      change ENNReal.ofReal (inner ℂ v ((c : ℂ) • ((1-R) v))).re = _
      simp only [inner_smul_right, Complex.mul_re, Complex.ofReal_re,
        Complex.ofReal_im, zero_mul, sub_zero]
      exact ENNReal.ofReal_mul hc.le
    have hscale : ∀ z : RegularHilbert (TowerHilbert P),
        ENNReal.ofReal c * dualEnergy A'.val v z =
          ENNReal.ofReal (c * ‖z-v‖^2) + dualQuadraticIntegral A.val z := by
      intro z
      change ENNReal.ofReal c *
        (ENNReal.ofReal (‖z-v‖^2) + dualQuadraticIntegral (c⁻¹ • A.val) z) = _
      rw [dualQuadraticIntegral_smul_operator _ (inv_pos.mpr hc).le,
        mul_add, ← mul_assoc, ← ENNReal.ofReal_mul hc.le,
        ← ENNReal.ofReal_mul hc.le, mul_inv_cancel₀ hc.ne',
        ENNReal.ofReal_one, one_mul]
    refine ⟨R v, he.trans (hscale (R v)), ?_⟩
    intro z
    rw [he, ← hscale z]
    exact mul_le_mul_right
      (dualResolvent_limit_minimizes_energy A'.val R A'.property.2 hlim v z)
      (ENNReal.ofReal c)

#print axioms dualResolvent_minimum_energy_value
#print axioms exists_base_moreau_approximant
end
end TGLV351
