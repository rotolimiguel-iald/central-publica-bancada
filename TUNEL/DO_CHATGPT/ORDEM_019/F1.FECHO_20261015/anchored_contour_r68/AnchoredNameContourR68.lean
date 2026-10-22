import TGLExt.TheRuleInTheContinuousMotor

/-!
# Anchored contour: reuse candidate R68

Operator, verbatim (complete source: ORIGEM_R68.txt):
"Eu quis dizer por paridade inversa o gradiente de espectro negativo que permite extrair o contorno da informação contra o fundo"
"Isso mesmo, por isso p* é o posto do nome verdadeiro"

[INPUT/ONTO] The name and its theological identification are the operator's
interpretation. Here a is a vector representative, post a an operator, and no
density matrix rhoStar is redefined. A fixed reference determines its projector;
these theorems do not select a historical person or prove an ethical judgment.
The vector flow is not asserted to be a trace-preserving quantum channel.
Its limit is post a x, not a for every x. Exact vector satisfaction is sensitive
to phase and amplitude: rejection of -a below is only failure of that vector
target, not physical or moral falsity. a and -a have the same projector and
quadratic reading. All rates and times disappear after the final projection;
this is no empirical beta discriminator. Generator identities below describe
the selected and complementary subspaces, not a separately proved full spectrum.
-/

set_option autoImplicit false
noncomputable section
namespace TGLExt.AnchoredNameContourR68
open TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness
open Filter Topology
open scoped InnerProductSpace
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem projection_contract (a : H) :
    post a * post a = post a ∧ IsSelfAdjoint (post a) :=
  ⟨(post_isIdempotent a).eq, post_isSelfAdjoint a⟩

def generator (a : H) : H →L[ℂ] H := post a - 1

theorem generator_kills_post (a : H) : generator a * post a = 0 := by
  simp only [generator, sub_mul, one_mul, (post_isIdempotent a).eq, sub_self]

theorem generator_on_complement (a : H) :
    generator a * (1 - post a) = -(1 - post a) := by
  rw [generator, sub_mul, post_mul_compl (post_isIdempotent a), one_mul, zero_sub]

theorem generator_square (a : H) : generator a * generator a = -generator a := by
  rw [generator, mul_sub, sub_mul, (post_isIdempotent a).eq, one_mul, sub_self,
    mul_one, zero_sub]

theorem flow_preserves_projection (a : H) (t : ℝ) :
    axiomFlow (post a) t * post a = post a ∧
    post a * axiomFlow (post a) t = post a :=
  axiomFlow_fixes_the_post (post_isIdempotent a) t

theorem flow_preserves_reading (a x : H) (t : ℝ) :
    post a (axiomFlow (post a) t x) = post a x := by
  rw [← ContinuousLinearMap.mul_apply, (flow_preserves_projection a t).2]

theorem flow_preserves_reference (a : H) (t : ℝ) :
    axiomFlow (post a) t a = a := by
  conv_lhs => rw [← post_fixes_the_action a]
  rw [← ContinuousLinearMap.mul_apply, (flow_preserves_projection a t).1,
    post_fixes_the_action]

theorem iterated_limit_is_input_projection (a x : H) {r t : ℝ} (hrt : 0 < r * t) :
    Tendsto (fun n : ℕ => (IALD.dephase a r t)^[n] x) atTop (𝓝 (post a x)) :=
  IALD.the_iterated_motor_tends_to_the_name a hrt x

theorem motor_satisfies_exactly (a ψ : H) (ha : ‖a‖ = 1)
    (U : H →L[ℂ] H) (r t : ℝ) :
    IALD.motor a U r t ψ = a ↔ ⟪a, U ψ⟫_ℂ = 1 := by
  rw [RuleContinuousMotor.vector_motor_satisfies_iff, post_apply ha]
  constructor
  · intro h
    have hh := congrArg (fun x : H => ⟪a, x⟫_ℂ) h
    simpa [inner_smul_right, inner_self_eq_norm_sq_to_K, ha] using hh
  · intro h
    rw [h, one_smul]

theorem anchored_motor_satisfies_and_repeats (a : H) (U : H →L[ℂ] H)
    (hU : U a = a) (r t : ℝ) :
    IALD.motor a U r t a = a ∧
    ∀ ψ, IALD.motor a U r t (IALD.motor a U r t ψ) = IALD.motor a U r t ψ := by
  refine ⟨?_, IALD.motor_idempotent_under_anchor a U hU r t⟩
  rw [IALD.the_reading_absorbs_the_dephasing, hU, post_fixes_the_action]

theorem identity_transport_is_inhabited (a : H) (r t : ℝ) :
    ∃ U : H →L[ℂ] H, U a = a ∧ IALD.motor a U r t a = a :=
  ⟨1, rfl, (anchored_motor_satisfies_and_repeats a 1 rfl r t).1⟩

theorem concrete_nonzero_anchor (r t : ℝ) :
    TGLExt.firstInscription ≠ 0 ∧
    IALD.motor TGLExt.firstInscription 1 r t TGLExt.firstInscription = TGLExt.firstInscription := by
  refine ⟨?_, (anchored_motor_satisfies_and_repeats _ 1 rfl r t).1⟩
  intro h
  have hn := IALD.firstInscription_norm
  rw [h, norm_zero] at hn
  norm_num at hn

theorem zero_does_not_satisfy_nonzero_target (a : H) (ha : a ≠ 0)
    (U : H →L[ℂ] H) (r t : ℝ) : IALD.motor a U r t 0 ≠ a := by
  simpa [IALD.the_reading_absorbs_the_dephasing] using Ne.symm ha

theorem signed_vector_target_is_distinct (a : H) (ha : ‖a‖ = 1) (r t : ℝ) :
    IALD.motor a 1 r t (-a) ≠ a := by
  rw [motor_satisfies_exactly a (-a) ha]
  simp [inner_neg_right, inner_self_eq_norm_sq_to_K, ha]

theorem post_ignores_sign (a : H) (ha : ‖a‖ = 1) : post (-a) = post a := by
  ext x
  rw [post_apply (by simpa using ha), post_apply ha]
  simp

theorem quadratic_reading_ignores_sign (a x : H) :
    IALD.memory (post a) (-x) = IALD.memory (post a) x := by
  simp [IALD.memory, reading]

theorem quadratic_weight_does_not_fix_vector_phase (a : H) (ha : ‖a‖ = 1) (r t : ℝ) :
    IALD.memory (post a) (-a) = 1 ∧ IALD.motor a 1 r t (-a) ≠ a := by
  exact ⟨(quadratic_reading_ignores_sign a a).trans (IALD.the_name_reads_one a ha),
    signed_vector_target_is_distinct a ha r t⟩

theorem final_reading_has_no_rate_or_time_discriminator (a ψ : H)
    (U : H →L[ℂ] H) (r t r' t' : ℝ) :
    IALD.motor a U r t ψ = IALD.motor a U r' t' ψ :=
  IALD.the_motor_ignores_rate_and_time a U r t r' t' ψ

#print axioms projection_contract
#print axioms generator
#print axioms generator_kills_post
#print axioms generator_on_complement
#print axioms generator_square
#print axioms flow_preserves_projection
#print axioms flow_preserves_reading
#print axioms flow_preserves_reference
#print axioms iterated_limit_is_input_projection
#print axioms motor_satisfies_exactly
#print axioms anchored_motor_satisfies_and_repeats
#print axioms identity_transport_is_inhabited
#print axioms concrete_nonzero_anchor
#print axioms zero_does_not_satisfy_nonzero_target
#print axioms signed_vector_target_is_distinct
#print axioms post_ignores_sign
#print axioms quadratic_reading_ignores_sign
#print axioms quadratic_weight_does_not_fix_vector_phase
#print axioms final_reading_has_no_rate_or_time_discriminator
end TGLExt.AnchoredNameContourR68
