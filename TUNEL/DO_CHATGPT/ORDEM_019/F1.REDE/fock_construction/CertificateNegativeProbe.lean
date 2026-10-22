import TGLExt.MaxwellLiteratureBridge
set_option autoImplicit false
noncomputable section
namespace F1Rede.CertificateNegativeProbe
open TGLExt.ImportedSQ TGLExt.MaxwellBridge TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open MeasureTheory
variable {L : LightOneParticle} (C : FockCertificate L)

/-- The stress-form interface alone admits the zero form. This is a negative
typing probe, not a Maxwell field or a proposed inhabitant of MaxwellCertificate. -/
def zeroQuadraticForm : MaxwellQuadraticForm C where
  Dom := Set.univ
  Dom_vac := Set.mem_univ _
  Dom_translate := by intros; simp
  Dom_boost := by intros; simp
  Q := fun _ _ => 0
  Q_vac := by intros; rfl
  Q_covariant := by intros; rfl
  Q_symmetric := by intros; exact Matrix.transpose_zero
  Q_test_integrable := by intros; simpa using (integrable_zero (Fin 4 → ℝ) ℝ volume)
  Q_conserved := by intros; simp
  Q_boost_covariant := by intros; simp

@[simp] theorem zeroQuadraticForm_toStress (ψ : C.F) (x : Fin 4 → ℝ) :
    (toStress (zeroQuadraticForm C)).T ψ x = 0 := by
  rw [toStress_on_dom _ (Set.mem_univ ψ)]
  rfl

/-- The complete certificate excludes a zero stress tensor: its named
nontriviality and charge identity have mathematical weight together. -/
theorem maxwell_stress_not_everywhere_zero (M : MaxwellCertificate C) :
    ¬ (∀ ψ x, M.T.T ψ x = 0) := by
  intro hzero
  obtain ⟨ψ, hreg, k, hk, hne⟩ := M.nontrivial
  have h := M.charge_link ψ hreg k hk
  have hc : nullPlaneCharge M.T.toStressTensorData ψ = 0 := by
    simp [nullPlaneCharge, nullEnergy, pairing, hzero]
  rw [hc, mul_zero] at h
  exact hne h

end F1Rede.CertificateNegativeProbe
#print axioms F1Rede.CertificateNegativeProbe.zeroQuadraticForm
#print axioms F1Rede.CertificateNegativeProbe.maxwell_stress_not_everywhere_zero
