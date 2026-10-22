import Mathlib.Algebra.Star.Basic
/-! Ring algebra before specializing to the large Fock representation. -/
set_option autoImplicit false
namespace F1Fecho.GenericStarConjugation
theorem conjugation_star {R:Type*} [NonUnitalSemiring R] [StarRing R]
    (u v a:R) (hu:star u=v) (hv:star v=u) :
    star (u*(a*v))=u*(star a*v) := by
  rw [star_mul,star_mul,hu,hv]
  exact mul_assoc _ _ _
end F1Fecho.GenericStarConjugation
#print axioms F1Fecho.GenericStarConjugation.conjugation_star
