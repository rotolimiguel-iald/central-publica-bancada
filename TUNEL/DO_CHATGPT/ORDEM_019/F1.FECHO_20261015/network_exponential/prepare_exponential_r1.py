from pathlib import Path
BASE=Path(__file__).resolve().parent
build=(BASE.parent/'network_antiunitary/build_antiunitary.py').read_text(encoding='utf-8')
build=build.replace("[BASE, BASE.parent/'network_reuse']", "[BASE, BASE.parent/'network_reuse', BASE.parent/'network_antiunitary']")
with (BASE/'build_exponential.py').open('x',encoding='utf-8',newline='\n') as f: f.write(build)
src=r'''import BosonicGammaJR5
import BosonicFockContinuity
import Mathlib.Analysis.Normed.Algebra.Exponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Analytic.Uniqueness
import Mathlib.Analysis.Analytic.OfScalars

/-! Exponential vectors in the previously constructed canonical bosonic Fock space.
The sectors and Hilbert direct sum are imported unchanged. This module constructs
the vectors by a proved l2 estimate; neither membership nor their inner kernel is
assumed as a field. No Weyl, Tomita, KMS, or global net theorem is asserted here. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open UniformSpace
open scoped TensorProduct ENNReal
namespace F1Fecho.Exponential
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock

theorem pureAlgebraic_inner (x y : H1) (n : ℕ) :
    inner ℂ (pureAlgebraic x n) (pureAlgebraic y n) = (inner ℂ x y)^n := by
  induction n with
  | zero => change inner ℂ (1 : ℂ) 1 = _; simp
  | succ n ih =>
    change inner ℂ (x ⊗ₜ[ℂ] pureAlgebraic x n) (y ⊗ₜ[ℂ] pureAlgebraic y n) = _
    rw [TensorProduct.inner_tmul, ih, pow_succ, mul_comm]

theorem pureTensor_inner (x y : H1) (n : ℕ) :
    inner ℂ (pureTensor n x) (pureTensor n y) = (inner ℂ x y)^n := by
  change inner ℂ (pureAlgebraic x n : Completion (Algebraic n))
    (pureAlgebraic y n : Completion (Algebraic n)) = _
  rw [Completion.inner_coe, pureAlgebraic_inner]

theorem pureAlgebraic_smul (z : ℂ) (x : H1) (n : ℕ) :
    pureAlgebraic (z • x) n = z^n • pureAlgebraic x n := by
  induction n with
  | zero => change (1 : ℂ) = z^0 • (1 : ℂ); simp
  | succ n ih =>
    change (z • x) ⊗ₜ[ℂ] pureAlgebraic (z • x) n = z^(n+1) • (x ⊗ₜ[ℂ] pureAlgebraic x n)
    rw [ih, TensorProduct.smul_tmul, TensorProduct.tmul_smul, smul_smul, pow_succ']

theorem pureTensor_smul (z : ℂ) (x : H1) (n : ℕ) :
    pureTensor n (z • x) = z^n • pureTensor n x := by
  apply Subtype.ext
  change (pureAlgebraic (z • x) n : Completion (Algebraic n)) =
    z^n • (pureAlgebraic x n : Completion (Algebraic n))
  rw [pureAlgebraic_smul, Completion.coe_smul]

def weight (n : ℕ) : ℝ := (Real.sqrt (n.factorial : ℝ))⁻¹

theorem weight_pos (n : ℕ) : 0 < weight n := by
  unfold weight
  positivity

theorem weight_sq (n : ℕ) : weight n ^ 2 = (n.factorial : ℝ)⁻¹ := by
  unfold weight
  rw [inv_pow, Real.sq_sqrt (by positivity)]

theorem complex_weight_sq (n : ℕ) : (weight n : ℂ)^2 = (n.factorial : ℂ)⁻¹ := by
  exact_mod_cast weight_sq n

def component (x : H1) (n : ℕ) : Sector n := (weight n : ℂ) • pureTensor n x

theorem component_norm_sq (x : H1) (n : ℕ) :
    ‖component x n‖^2 = (‖x‖^2)^n / (n.factorial : ℝ) := by
  rw [component, norm_smul, Complex.norm_real, abs_of_pos (weight_pos n), pureTensor_norm,
    mul_pow, weight_sq]
  rw [div_eq_mul_inv, ← pow_mul, ← pow_mul]
  ring

theorem component_inner (x y : H1) (n : ℕ) :
    inner ℂ (component x n) (component y n) = (inner ℂ x y)^n / (n.factorial : ℂ) := by
  rw [component, component, inner_smul_left, inner_smul_right, pureTensor_inner]
  simp only [Complex.conj_ofReal, ← mul_assoc]
  rw [← pow_two, complex_weight_sq, div_eq_mul_inv, mul_comm]

theorem component_mem_lp (x : H1) : Memℓp (component x) 2 := by
  apply (memℓp_gen_iff (by norm_num : 0 < (2 : ℝ≥0∞).toReal)).mpr
  have hs := NormedSpace.expSeries_div_summable (‖x‖^2)
  simpa only [ENNReal.toReal_ofNat, Real.rpow_two, component_norm_sq] using hs

def exponential (x : H1) : F := ⟨component x, component_mem_lp x⟩

@[simp] theorem exponential_apply (x : H1) (n : ℕ) : exponential x n = component x n := rfl

theorem exponential_inner (x y : H1) :
    inner ℂ (exponential x) (exponential y) = Complex.exp (inner ℂ x y) := by
  have hs := lp.hasSum_inner (exponential x) (exponential y)
  simp only [exponential_apply, component_inner] at hs
  have he := NormedSpace.expSeries_div_hasSum_exp (inner ℂ x y)
  rw [← Complex.exp_eq_exp_ℂ] at he
  exact hs.unique he

theorem exponential_norm_sq (x : H1) : ‖exponential x‖^2 = Real.exp (‖x‖^2) := by
  rw [F1Rede.SectorStrongContinuity.norm_sq_eq_tsum]
  simp only [exponential_apply, component_norm_sq]
  have he := NormedSpace.expSeries_div_hasSum_exp (‖x‖^2)
  rw [← Real.exp_eq_exp_ℝ] at he
  exact he.tsum_eq

end F1Fecho.Exponential

#print axioms F1Fecho.Exponential.pureTensor_inner
#print axioms F1Fecho.Exponential.pureTensor_smul
#print axioms F1Fecho.Exponential.component_mem_lp
#print axioms F1Fecho.Exponential.exponential_inner
#print axioms F1Fecho.Exponential.exponential_norm_sq
'''
with (BASE/'ExponentialVectorsR1.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(src)
