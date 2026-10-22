import TGLExt.DecisionCommutation
import TGLExt.RuleTruthContract

/-! Three same-state consumers of existing DecisionCommutation and RuleTruthContract.
D(P)=diag(d(P)) and rho(P)=diag(P) are built from the SAME P. The generator
constraint vanishes along every chosen family, but a nonconstant such family
is not thereby a solution of the evolution ODE rho'=generator(rho).
Arrays may be restricted to normalized positive probabilities; the algebra
holds even without those restrictions. A nonnegative rate is needed for a
physical dephasing interpretation, not for these zero identities.
The reading E is explicitly assumed to fix diagonals. No general conditional
expectation/pinching theorem is rebuilt or claimed. A fixed target differs from
Y(P)=rho(P); no action stationarity, physical realization, or H3 follows here.
The separate canonical modular state invariance is already in
TGLExt.CanonicalModularStationarity, and is not re-proved by these statements. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace TGLExt.SameStateSpectralSelectionR89
open Matrix RuleTruthContract
noncomputable section

def sameStateDissipator {n : ℕ} (d : (Fin n → ℝ) → Fin n → ℝ)
    (gamma : ℝ) (P : Fin n → ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  let D := Matrix.diagonal (d P)
  let rho := Matrix.diagonal P
  (-gamma/2) • (D*(D*rho-rho*D)-(D*rho-rho*D)*D)

/-- The derivative is of the constraint residual, not the state trajectory. -/
theorem same_state_generator_constraint_along_family {n : ℕ}
    (d : (Fin n → ℝ) → Fin n → ℝ) (gamma : ℝ)
    (P : ℝ → Fin n → ℝ) (t0 : ℝ) :
    (∀ t, sameStateDissipator d gamma (P t)=0) ∧
    (∀ i j, HasDerivAt (fun t => sameStateDissipator d gamma (P t) i j) 0 t0) := by
  have hz (p : Fin n → ℝ) : sameStateDissipator d gamma p=0 := by
    have hc : Matrix.diagonal (d p)*Matrix.diagonal p =
        Matrix.diagonal p*Matrix.diagonal (d p) := by
      apply (TGLExt.decided_iff_block (d p) (Matrix.diagonal p)).mpr
      intro i j hij
      by_cases he : i=j
      · subst j
        exact (hij rfl).elim
      · simp [Matrix.diagonal, he]
    simp only [sameStateDissipator, hc, sub_self, mul_zero, zero_mul, smul_zero]
  refine ⟨fun t => hz (P t), ?_⟩
  intro i j
  simpa only [hz, Matrix.zero_apply] using hasDerivAt_const t0 (0 : ℝ)

theorem moving_target_is_automatically_admissible {n : ℕ}
    (E : Matrix (Fin n) (Fin n) ℝ → Matrix (Fin n) (Fin n) ℝ)
    (fixes_diagonal : ∀ p : Fin n → ℝ, E (Matrix.diagonal p)=Matrix.diagonal p)
    (P : Fin n → ℝ) :
    Admissible E (Matrix.diagonal P) (Matrix.diagonal P) := fixes_diagonal P

theorem fixed_target_selects_probability {n : ℕ}
    (E : Matrix (Fin n) (Fin n) ℝ → Matrix (Fin n) (Fin n) ℝ)
    (fixes_diagonal : ∀ p : Fin n → ℝ, E (Matrix.diagonal p)=Matrix.diagonal p)
    (y P : Fin n → ℝ) :
    Admissible E (Matrix.diagonal y) (Matrix.diagonal P) ↔ P=y := by
  unfold Admissible
  rw [fixes_diagonal P]
  constructor
  · intro h
    funext i
    have he := congrArg (fun A : Matrix (Fin n) (Fin n) ℝ => A i i) h
    simpa only [Matrix.diagonal_apply_eq] using he
  · intro h
    rw [h]

#print axioms sameStateDissipator
#print axioms same_state_generator_constraint_along_family
#print axioms moving_target_is_automatically_admissible
#print axioms fixed_target_selects_probability
end
end TGLExt.SameStateSpectralSelectionR89
