import SchwartzCompactDensityR3

/-! Compact approximation preserves the original nonzero support exactly as
an inclusion. No strict geometric margin for two closed supports is inferred. -/
set_option autoImplicit false
noncomputable section
open SchwartzMap
namespace F1Fecho.SchwartzCutoff
variable {F:Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]

theorem cutoff_support_subset (s:ℝ) (f:SchwartzMap E F) :
    Function.support (cutoff s f:E→F) ⊆ Function.support (f:E→F) := by
  intro x hx hzero
  apply hx
  rw [cutoff_apply,hzero,smul_zero]

theorem cutoff_tsupport_subset (s:ℝ) (f:SchwartzMap E F) :
    tsupport (cutoff s f:E→F) ⊆ tsupport (f:E→F) :=
  closure_mono (cutoff_support_subset s f)

theorem cutoffSequence_supported (f:SchwartzMap E F) (n:ℕ) :
    HasCompactSupport (cutoffSequence f n:E→F) ∧
    Function.support (cutoffSequence f n:E→F) ⊆ Function.support (f:E→F) :=
  ⟨cutoff_compact _ (by positivity) f,cutoff_support_subset _ f⟩

end F1Fecho.SchwartzCutoff
#print axioms F1Fecho.SchwartzCutoff.cutoff_support_subset
#print axioms F1Fecho.SchwartzCutoff.cutoffSequence_supported
