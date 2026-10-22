import OrbitalBoostCovariance_v2
import OrbitalBoostContinuity_v2

set_option autoImplicit false
noncomputable section
open MeasureTheory
namespace ChatgptAudit.WignerRapidityMeasure016
open TGLExt.ContratoQGv31

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

/-- Packages the existing boost isometry with its proved inverse. -/
def orbitalBoostUnitary (m s : ℝ) :
    Lp E 2 (orbitalMeasure m) ≃ₗᵢ[ℂ] Lp E 2 (orbitalMeasure m) :=
  LinearIsometryEquiv.ofLinearIsometry (orbitalScalarBoost m s)
    (orbitalScalarBoost m (-s)).toLinearMap
    (by apply LinearMap.ext; intro f; exact orbitalScalarBoost_inverse m s f)
    (by
      apply LinearMap.ext
      intro f
      change orbitalScalarBoost m (-s) (orbitalScalarBoost m s f) = f
      simpa only [neg_neg] using orbitalScalarBoost_inverse m (-s) f)

theorem orbitalBoostUnitary_apply (m s : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalBoostUnitary m s f = orbitalScalarBoost m s f := rfl

theorem orbitalBoostUnitary_symm_apply (m s : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    (orbitalBoostUnitary m s).symm f = orbitalScalarBoost m (-s) f := rfl

theorem orbitalBoostUnitary_zero (m : ℝ) :
    orbitalBoostUnitary (E := E) m 0 = LinearIsometryEquiv.refl ℂ _ := by
  apply LinearIsometryEquiv.ext
  intro f
  exact orbitalScalarBoost_zero m f

theorem orbitalBoostUnitary_add (m s t : ℝ) :
    orbitalBoostUnitary (E := E) m (s+t) =
      (orbitalBoostUnitary m t).trans (orbitalBoostUnitary m s) := by
  apply LinearIsometryEquiv.ext
  intro f
  exact orbitalScalarBoost_add m s t f

theorem orbitalBoostUnitary_strongly_continuous (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    Continuous (fun s => orbitalBoostUnitary m s f) :=
  orbitalScalarBoost_strongly_continuous m f

variable [InnerProductSpace ℂ E] [CompleteSpace E]

/-- The exact conjugation type used by V_translations, without fabricating
the other AQFT fields or a normalized one-particle vacuum. -/
theorem orbitalBoostUnitary_conj_translations (m s : ℝ) (a : Fin 4 → ℝ) :
    (orbitalBoostUnitary (E := E) m s).conjStarAlgEquiv (orbitalTranslation m a) =
      orbitalTranslation m (wedgeBoostMap s a) := by
  apply ContinuousLinearMap.ext
  intro f
  rw [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    orbitalBoostUnitary_apply, orbitalBoostUnitary_symm_apply]
  exact orbitalScalarBoost_conjugates_translations m s a f

#print axioms orbitalBoostUnitary_apply
#print axioms orbitalBoostUnitary_symm_apply
#print axioms orbitalBoostUnitary_zero
#print axioms orbitalBoostUnitary_add
#print axioms orbitalBoostUnitary_strongly_continuous
#print axioms orbitalBoostUnitary_conj_translations
end ChatgptAudit.WignerRapidityMeasure016
