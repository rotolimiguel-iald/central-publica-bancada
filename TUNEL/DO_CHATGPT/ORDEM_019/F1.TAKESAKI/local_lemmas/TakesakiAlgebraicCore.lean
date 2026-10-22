import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith

set_option autoImplicit false

/-!
# F1.TAKESAKI: two elementary, conditional algebraic steps

[DERIVED — sandbox candidate, not the general Takesaki theorem]
The house already proves the positive-parameter fixed-point obstruction in
`TGLExt.GlobalLiftLadder.DualScalingData.fixed_tau_zero`, and realizes dual
scaling on the v351 regular core. This file isolates the unital obstruction
for arbitrary real s, and the algebraic reweighting calculation.

No von Neumann algebra, crossed product, dual weight, affiliated positive
operator, canonical trace, or equality with the v351 construction is built
here. `reweighted_scaling` names its exact three assumptions. In an analytic
application the covariance of Q, its domain, and the identification of phi
are substantive obligations, not consequences proved by this lemma.
The nonzero two-coordinate witness below is only an algebraic model.
-/

namespace F1Takesaki

/-- A finite positive value at a preserved unit forbids nontrivial exponential
scaling. Neither traciality nor a matrix algebra is needed for this obstruction.
It does not apply to the infinite value of a semifinite trace at the unit. -/
theorem unital_finite_scaling_forces_zero
    {M : Type*} [One M] (tau : M → ℝ) (theta : M → M) (s : ℝ)
    (unit_positive : 0 < tau 1) (unit_preserved : theta 1 = 1)
    (scaling : ∀ x, tau (theta x) = Real.exp (-s) * tau x) :
    s = 0 := by
  have hunit : tau 1 = Real.exp (-s) * tau 1 := by
    simpa only [unit_preserved] using scaling 1
  have hexp : Real.exp (-s) = 1 := by
    apply mul_right_cancel₀ (ne_of_gt unit_positive)
    simpa only [one_mul] using hunit.symm
  have hneg : -s = 0 := Real.exp_injective (by simpa using hexp)
  exact neg_eq_zero.mp hneg

/-- For tau := phi ∘ Q, invariance of phi and scalar covariance of Q give
the scale law. Covariance of Q is the real analytic obligation in a Takesaki
application. This statement neither assumes the scale law as a field nor
derives that covariance from preservation of the identity alone. -/
theorem reweighted_scaling
    {M : Type*} [SMul ℝ M] (phi : M → ℝ) (theta Q : M → M) (s : ℝ)
    (phi_invariant : ∀ x, phi (theta x) = phi x)
    (phi_homogeneous : ∀ x, phi (Real.exp (-s) • x) = Real.exp (-s) * phi x)
    (reweight_covariant : ∀ x, Q (theta x) = Real.exp (-s) • theta (Q x))
    (x : M) :
    (phi ∘ Q) (theta x) = Real.exp (-s) * (phi ∘ Q) x := by
  change phi (Q (theta x)) = Real.exp (-s) * phi (Q x)
  rw [reweight_covariant, phi_homogeneous, phi_invariant]

/-- Invariance alone does not imply scaling: the real identity map preserves
the positive functional at its unit, but nonzero s cannot obey the scale law. -/
theorem invariant_identity_does_not_scale (s : ℝ) (nonzero : s ≠ 0) :
    (∀ x : ℝ, (id : ℝ → ℝ) (id x) = id x) ∧
      ¬ (∀ x : ℝ, (id : ℝ → ℝ) (id x) = Real.exp (-s) * id x) := by
  refine ⟨fun _ => rfl, ?_⟩
  intro scaling
  exact nonzero (unital_finite_scaling_forces_zero id id s
    (by norm_num) rfl scaling)

/-- A nonzero algebraic witness. The first coordinate is invariant; Q reads
the second coordinate into the first. There is no operator-algebra claim. -/
noncomputable def modelTheta (s : ℝ) (x : ℝ × ℝ) : ℝ × ℝ := (x.1, Real.exp (-s) * x.2)
def modelPhi (x : ℝ × ℝ) : ℝ := x.1
def modelQ (x : ℝ × ℝ) : ℝ × ℝ := (x.2, 0)

theorem algebraic_witness_hypotheses (s : ℝ) :
    (∀ x, modelPhi (modelTheta s x) = modelPhi x) ∧
    (∀ x, modelPhi (Real.exp (-s) • x) = Real.exp (-s) * modelPhi x) ∧
    (∀ x, modelQ (modelTheta s x) = Real.exp (-s) • modelTheta s (modelQ x)) ∧
    modelPhi (modelQ (0, 1)) = 1 := by
  refine ⟨fun _ => rfl, fun _ => rfl, ?_, rfl⟩
  intro x
  simp [modelQ, modelTheta, Prod.smul_mk, smul_eq_mul]

theorem algebraic_witness_scales (s : ℝ) (x : ℝ × ℝ) :
    (modelPhi ∘ modelQ) (modelTheta s x) =
      Real.exp (-s) * (modelPhi ∘ modelQ) x := by
  obtain ⟨hphi, hhom, hcov, _⟩ := algebraic_witness_hypotheses s
  exact reweighted_scaling modelPhi (modelTheta s) modelQ s hphi hhom hcov x

#print axioms unital_finite_scaling_forces_zero
#print axioms reweighted_scaling
#print axioms invariant_identity_does_not_scale
#print axioms algebraic_witness_hypotheses
#print axioms algebraic_witness_scales

end F1Takesaki
