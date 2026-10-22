import TGLExt.O16.LightRayGaussianDensity_v2

set_option autoImplicit false
set_option maxHeartbeats 1200000

/-!
# A concrete standard-subspace net on the light ray
[DERIVED — sandbox candidate]
The objects below are constructed from the existing O16 operators and the
existing Fourier-transported standard subspace. No standardness or isotony
field is postulated. This is a real-subspace net of one-particle half-lines;
it is not a von Neumann algebra net in four-dimensional spacetime.
The final negative control preserves the existing obstruction to promoting
a single null translation coordinate to faithful four-dimensional translations.
-/

noncomputable section
open MeasureTheory Filter
open FormaInscrita.RetaDeLuz ChatgptAudit.Continuous049
open ChatgptAudit.FourierBridge016 ChatgptAudit.LightRayCore016

namespace F1Rede.LightRay

local instance : Module ℝ L2R := NormedSpace.complexToReal.toModule
local instance : NormedSpace ℝ L2R := NormedSpace.complexToReal

theorem translation_add_apply (a b : ℝ) (f : L2R) :
    U (a+b) f = U a (U b f) := by
  rw [U_add]
  rfl

theorem translation_inv_apply (a : ℝ) (f : L2R) : U (-a) (U a f) = f := by
  rw [← translation_add_apply, neg_add_cancel, U_zero]
  rfl

/-- The concrete null translations are continuous complex linear equivalences. -/
def translationEquiv (a : ℝ) : L2R ≃L[ℂ] L2R where
  toLinearEquiv :=
    { (U a).toLinearMap with
      invFun := U (-a)
      left_inv := translation_inv_apply a
      right_inv := by
        intro f
        simpa only [neg_neg] using translation_inv_apply (-a) f }
  continuous_toFun := (U a).continuous
  continuous_invFun := (U (-a)).continuous

theorem transport_mulI (e : L2R ≃L[ℂ] L2R) (S : ClosedSubmodule ℝ L2R) :
    S.mulI.mapEquiv (e.restrictScalars ℝ) =
      (S.mapEquiv (e.restrictScalars ℝ)).mulI := by
  ext x
  change x ∈ S.mulI.mapEquiv (e.restrictScalars ℝ) ↔
    x ∈ (S.mapEquiv (e.restrictScalars ℝ)).mulI
  simp only [ClosedSubmodule.mulI, ClosedSubmodule.mem_mapEquiv_iff,
    scalarSMulCLE_symm_apply, Units.smul_def, Units.val_inv_eq_inv_val,
    Complex.val_UnitI, Complex.inv_I]
  change (-Complex.I) • e.symm x ∈ S ↔ e.symm ((-Complex.I) • x) ∈ S
  rw [map_smul]

/-- Standardness is proved by transport through a complex linear equivalence. -/
def transportStandard (e : L2R ≃L[ℂ] L2R) (K : StandardSubspace L2R) :
    StandardSubspace L2R where
  toClosedSubmodule := K.toClosedSubmodule.mapEquiv (e.restrictScalars ℝ)
  IsSeparating := by
    rw [← transport_mulI, ← ClosedSubmodule.mapEquiv_inf_eq,
      K.IsSeparating, ClosedSubmodule.mapEquiv_bot_eq_bot]
  IsCyclic := by
    rw [← transport_mulI, ← ClosedSubmodule.mapEquiv_sup_eq,
      K.IsCyclic, ClosedSubmodule.mapEquiv_top_eq_top]

/-- K(a) = U(a) K(0), with the existing O16 standard subspace at a=0. -/
def halfline (a : ℝ) : StandardSubspace L2R :=
  transportStandard (translationEquiv a) (rapidityStandardSubspace (2 * Real.pi^2))

theorem mem_halfline (a : ℝ) (f : L2R) :
    f ∈ (halfline a).toClosedSubmodule ↔
      U (-a) f ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule :=
  ClosedSubmodule.mem_mapEquiv_iff _ _ _

theorem mem_halfline_image (a : ℝ) (f : L2R) :
    f ∈ (halfline a).toClosedSubmodule ↔
      ∃ g ∈ (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule, U a g = f := by
  rw [mem_halfline]
  constructor
  · intro hf
    refine ⟨U (-a) f, hf, ?_⟩
    simpa only [neg_neg] using translation_inv_apply (-a) f
  · rintro ⟨g, hg, rfl⟩
    simpa only [translation_inv_apply] using hg

theorem halfline_zero :
    (halfline 0).toClosedSubmodule =
      (rapidityStandardSubspace (2 * Real.pi^2)).toClosedSubmodule := by
  ext f
  rw [mem_halfline]
  simp only [neg_zero, U_zero, ContinuousLinearMap.one_apply]

/-- Inclusion follows from the proved O16 half-sided isotony. -/
theorem halfline_antitone {a b : ℝ} (hab : a ≤ b) :
    (halfline b).toClosedSubmodule ≤ (halfline a).toClosedSubmodule := by
  intro f hf
  obtain ⟨g, hg, rfl⟩ := (mem_halfline_image b f).mp hf
  rw [mem_halfline, ← translation_add_apply]
  exact halfline_isotony (-a+b) (by linarith) g hg

/-- Every real translation transports the actual half-line, in both directions. -/
theorem translation_covariance (t a : ℝ) (f : L2R) :
    U t f ∈ (halfline (t+a)).toClosedSubmodule ↔
      f ∈ (halfline a).toClosedSubmodule := by
  rw [mem_halfline, mem_halfline, ← translation_add_apply]
  have heq : -(t+a)+t = -a := by ring
  rw [heq]

theorem translation_image (t a : ℝ) :
    (halfline a).toClosedSubmodule.mapEquiv ((translationEquiv t).restrictScalars ℝ) =
      (halfline (t+a)).toClosedSubmodule := by
  ext f
  rw [ClosedSubmodule.mem_mapEquiv_iff]
  change U (-t) f ∈ (halfline a).toClosedSubmodule ↔
    f ∈ (halfline (t+a)).toClosedSubmodule
  have h := translation_covariance t a (U (-t) f)
  simpa only [show U t (U (-t) f) = f from by
    simpa only [neg_neg] using translation_inv_apply (-t) f] using h.symm

/-- The ray cannot supply faithful four-dimensional translations through one
linear coordinate. This is a proved negative control, not a missing import. -/
theorem no_four_dimensional_promotion (ell : (Fin 4 → ℝ) →ₗ[ℝ] ℝ) :
    ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ U (ell a) = 1 :=
  lightray_not_faithful_in_four U 1 U_zero ell

#print axioms translationEquiv
#print axioms transportStandard
#print axioms halfline
#print axioms mem_halfline_image
#print axioms halfline_antitone
#print axioms translation_covariance
#print axioms translation_image
#print axioms no_four_dimensional_promotion

end F1Rede.LightRay
