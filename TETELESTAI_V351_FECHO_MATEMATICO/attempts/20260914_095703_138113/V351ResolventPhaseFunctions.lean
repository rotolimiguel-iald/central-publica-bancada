import TGLExt.ModularFlowLevel
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Continuity

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace TGLV350.Regular
open Filter ChatgptAudit
open scoped Topology
noncomputable section

/-- Endpoint damping for the imaginary powers of `(1-T)/T`. -/
def resolventDamping (x : ℝ) : ℝ := x * (1-x)

/-- Only this damped function is fed to bounded continuous functional calculus. -/
def resolventPhaseFunction (t x : ℝ) : ℂ :=
  (resolventDamping x : ℂ) * modularPhase t (Real.log ((1-x)/x))

theorem resolventPhaseFunction_norm (t x : ℝ) :
    ‖resolventPhaseFunction t x‖ = ‖resolventDamping x‖ := by
  simp [resolventPhaseFunction, norm_mul, modularPhase_norm]

theorem resolventPhaseFunction_zero_time (x : ℝ) :
    resolventPhaseFunction 0 x = (resolventDamping x : ℂ) := by
  simp [resolventPhaseFunction, modularPhase]

theorem resolventPhaseFunction_add (s t x : ℝ) :
    resolventPhaseFunction s x * resolventPhaseFunction t x =
      (resolventDamping x : ℂ) * resolventPhaseFunction (s+t) x := by
  simp only [resolventPhaseFunction, modularPhase_add]
  ring

theorem resolventPhaseFunction_star (t x : ℝ) :
    star (resolventPhaseFunction t x) = resolventPhaseFunction (-t) x := by
  simp only [resolventPhaseFunction, star_mul, Complex.star_def,
    map_mul, Complex.conj_ofReal]
  unfold modularPhase
  rw [← Complex.exp_conj]
  congr 2
  simp

theorem resolventPhaseFunction_gram (t x : ℝ) :
    star (resolventPhaseFunction t x) * resolventPhaseFunction t x =
      ((resolventDamping x)^2 : ℝ) := by
  rw [resolventPhaseFunction_star, resolventPhaseFunction_add]
  simp [resolventPhaseFunction_zero_time, pow_two]

/-- Joint continuity survives the logarithmic singularities at both endpoints. -/
theorem resolventPhaseFunction_joint_continuous :
    Continuous (fun p : ℝ × ℝ => resolventPhaseFunction p.1 p.2) := by
  rw [continuous_iff_continuousAt]
  intro p
  by_cases hp : p.2=0 ∨ p.2=1
  · have hz : resolventDamping p.2=0 := by
      rcases hp with h|h <;> simp [resolventDamping,h]
    have hg : resolventPhaseFunction p.1 p.2=0 := by simp [resolventPhaseFunction,hz]
    change Tendsto _ _ (𝓝 _)
    rw [hg]
    apply squeeze_zero_norm (fun q => (resolventPhaseFunction_norm q.1 q.2).le)
    have ht : Continuous (fun q : ℝ × ℝ => ‖resolventDamping q.2‖) := by
      unfold resolventDamping
      fun_prop
    simpa only [hz,norm_zero] using ht.continuousAt.tendsto (x := p)
  · push_neg at hp
    have hc : ContinuousAt (fun q : ℝ × ℝ => (1-q.2)/q.2) p :=
      (continuousAt_const.sub continuous_snd.continuousAt).div continuous_snd.continuousAt hp.1
    have hn : (1-p.2)/p.2 ≠ 0 := div_ne_zero (sub_ne_zero.mpr (Ne.symm hp.2)) hp.1
    have hl := hc.log hn
    unfold resolventPhaseFunction modularPhase resolventDamping
    exact ((continuous_snd.mul (continuous_const.sub continuous_snd)).complex_ofReal.continuousAt).mul
      (((continuous_fst.continuousAt.mul hl).complex_ofReal.mul continuousAt_const).cexp)

theorem resolventPhaseFunction_continuous (t : ℝ) : Continuous (resolventPhaseFunction t) :=
  resolventPhaseFunction_joint_continuous.comp (continuous_const.prodMk continuous_id)

#print axioms resolventDamping
#print axioms resolventPhaseFunction
#print axioms resolventPhaseFunction_norm
#print axioms resolventPhaseFunction_zero_time
#print axioms resolventPhaseFunction_add
#print axioms resolventPhaseFunction_star
#print axioms resolventPhaseFunction_gram
#print axioms resolventPhaseFunction_joint_continuous
#print axioms resolventPhaseFunction_continuous
end
end TGLV350.Regular
