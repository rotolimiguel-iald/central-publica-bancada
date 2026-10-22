import RegularCovariantCoreR3
import RegularScalarWeightStarAlgebraR2
/-! Abstract regular conjugation and full finite-star-domain assembly, before Fock specialization. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericStarConjugation
open TGLV350.Regular F1Fecho.RegularCovariantCore
open F1Fecho.RegularScalarGNS F1Fecho.RegularScalarWeightDomain
open F1Fecho.RegularScalarWeightStarAlgebra
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem regular_conjugation_star (B:UnitaryFlow H) (t:ℝ)
    (A:RegularHilbert H →L[ℂ] RegularHilbert H) :
    star (regularUnitary B t*(A*regularUnitary B (-t))) =
      regularUnitary B t*(star A*regularUnitary B (-t)) := by
  rw [star_mul,star_mul,RegularCovariantCore.regular_star,RegularCovariantCore.regular_star,neg_neg,mul_assoc]
def starCoreOfLeft (D:Context H) (A B:scalarWeightLeftIdeal D)
    (h:star A.val=B.val) : scalarWeightStarCore D :=
  ⟨A.val,A.property,by
    change star A.val ∈ scalarWeightLeftIdeal D
    rw [h]
    exact B.property⟩
end F1Fecho.GenericStarConjugation
#print axioms F1Fecho.GenericStarConjugation.regular_conjugation_star
#print axioms F1Fecho.GenericStarConjugation.starCoreOfLeft
