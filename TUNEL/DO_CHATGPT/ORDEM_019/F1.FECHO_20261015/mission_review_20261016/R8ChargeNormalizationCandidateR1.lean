import RegularFockMaxwellQuadraticR2

/-! Review candidate only: NOT COMPILED. No new Maxwell hypothesis and no
certificate inhabitant. The first theorem only unwraps the existing tensor.
The factor is the analytically derived angular-Fourier calibration; its charge
identity and full-domain extension are separate open obligations in the report.
Pinned R2 is preserved. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.MaxwellGlobal.R8ChargeReview
open MeasureTheory TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore

 theorem existing_tensor_on_domain {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (psi : regularFockDomain) :
    (TGLExt.MaxwellBridge.toStress (regularMaxwellQuadraticForm A)).T psi.val =
      realCoordinateStress psi := by
  have hm : psi.val ∈ (regularMaxwellQuadraticForm A).Dom := psi.property
  exact (TGLExt.MaxwellBridge.toStress_on_dom (regularMaxwellQuadraticForm A) hm).trans
    (funext (fun x => regularMaxwellQuadraticForm_exact A psi x))

 def angularStressFactor : ℝ := ((2 * Real.pi) ^ (3 : ℕ))⁻¹

 theorem angularStressFactor_pos : 0 < angularStressFactor := by
  unfold angularStressFactor
  positivity

 def normalizedTensorCandidate (psi : regularFockDomain) (x : Fin 4 → ℝ) :
    Matrix (Fin 4) (Fin 4) ℝ :=
  angularStressFactor • realCoordinateStress psi x

 /- Exact original requirements, not a replacement certificate. The raw R2
    charge goal has the normalization obstruction detailed in the report. -/
 def rawChargeLinkRemaining {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) : Prop :=
  ∀ psi, Regular (regularMaxwellQuadraticForm A).Dom
      (TGLExt.MaxwellBridge.toStress (regularMaxwellQuadraticForm A)).toStressTensorData psi →
    ∀ k : ℝ, HasModularEnergy (lightDelta A.toCertificate) psi k →
      k = 2 * Real.pi * nullPlaneCharge
        (TGLExt.MaxwellBridge.toStress (regularMaxwellQuadraticForm A)).toStressTensorData psi

 def rawNontrivialRemaining {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) : Prop :=
  ∃ psi, Regular (regularMaxwellQuadraticForm A).Dom
      (TGLExt.MaxwellBridge.toStress (regularMaxwellQuadraticForm A)).toStressTensorData psi ∧
    ∃ k : ℝ, HasModularEnergy (lightDelta A.toCertificate) psi k ∧ k ≠ 0

end F1Fecho.MaxwellGlobal.R8ChargeReview
