import TGLExt.MaxwellLiteratureBridge

/-!
Conditional wiring over the existing same Fock certificate and Maxwell form.
The physical form Q and the equality between its integrated charge and the
derivative of the actual boost matrix coefficient remain explicit obligations.
The modular factor 2*pi and the nonzero modular-energy witness are derived.
No tensor-zero substitute, physical field construction, full Lorentz-family
construction or all-directions curved H3 is asserted here.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.MatterReuse
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open TGLExt.ContratoQGv32 TGLExt.ImportedSQ TGLExt.MaxwellBridge
open ChatgptAudit.ModularCharge016

variable {L : LightOneParticle} (C : FockCertificate L)

/-- A physical generator-charge identity, not the desired modular conclusion. -/
def BoostChargeIdentity (Q : MaxwellQuadraticForm C) (N : KillingNormalization) : Prop :=
  ∀ ψ, Regular Q.Dom (toStress Q).toStressTensorData ψ →
    HasBoostEnergy (lightH2 C N).boost.V ψ
      (nullPlaneCharge (toStress Q).toStressTensorData ψ)

/-- A nonzero charge in the same regular domain, not a manufactured vacuum. -/
def NonzeroChargeState (Q : MaxwellQuadraticForm C) : Prop :=
  ∃ ψ, Regular Q.Dom (toStress Q).toStressTensorData ψ ∧
    nullPlaneCharge (toStress Q).toStressTensorData ψ ≠ 0

theorem linked_modular_charge (Q : MaxwellQuadraticForm C) (N : KillingNormalization)
    (hb : BoostChargeIdentity C Q N) :
    ∀ ψ, Regular Q.Dom (toStress Q).toStressTensorData ψ → ∀ k : ℝ,
      HasModularEnergy (lightDelta C) ψ k →
      k = 2 * Real.pi * nullPlaneCharge (toStress Q).toStressTensorData ψ := by
  intro ψ hψ k hk
  exact (modular_charge_of_boost_charge (lightH2 C N) (toStress Q).toStressTensorData
    {φ : C.F | Regular Q.Dom (toStress Q).toStressTensorData φ}
    (fun φ hφ => hb φ hφ)) ψ hψ k hk

theorem linked_nonzero_modular_state (Q : MaxwellQuadraticForm C) (N : KillingNormalization)
    (hb : BoostChargeIdentity C Q N) (hw : NonzeroChargeState C Q) :
    ∃ ψ, Regular Q.Dom (toStress Q).toStressTensorData ψ ∧
      ∃ k : ℝ, HasModularEnergy (lightDelta C) ψ k ∧ k ≠ 0 := by
  obtain ⟨ψ,hψ,hq⟩ := hw
  refine ⟨ψ,hψ,2*Real.pi*nullPlaneCharge (toStress Q).toStressTensorData ψ,?_,?_⟩
  · exact modularEnergy_of_boostEnergy (lightH2 C N) (hb ψ hψ)
  · exact mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hq

def assembleMaxwell (Q : MaxwellQuadraticForm C) (N : KillingNormalization)
    (hb : BoostChargeIdentity C Q N) (hw : NonzeroChargeState C Q) : MaxwellCertificate C :=
  toCertificate Q (linked_modular_charge C Q N hb)
    (linked_nonzero_modular_state C Q N hb hw)

theorem assembled_tensor_is_original (Q : MaxwellQuadraticForm C) (N : KillingNormalization)
    (hb : BoostChargeIdentity C Q N) (hw : NonzeroChargeState C Q) :
    (assembleMaxwell C Q N hb hw).T = toStress Q := rfl

theorem assembled_tensor_on_domain (Q : MaxwellQuadraticForm C) (N : KillingNormalization)
    (hb : BoostChargeIdentity C Q N) (hw : NonzeroChargeState C Q)
    (ψ : C.F) (hψ : ψ ∈ Q.Dom) :
    (assembleMaxwell C Q N hb hw).T.T ψ = Q.Q ψ :=
  toStress_on_dom Q hψ

/-- Consumption by the existing H3 on the standard light wedge, for this N. -/
def standardWedgeH3 (Q : MaxwellQuadraticForm C) (N : KillingNormalization)
    (hb : BoostChargeIdentity C Q N) (hw : NonzeroChargeState C Q)
    (G : ℝ) (hG : 0 < G) :
    ContratoH3v32 (lightNet C) (lightRealization C) N (lightBoost C) (toStress Q) :=
  lightH3v32 (assembleMaxwell C Q N hb hw) N G hG

end F1Fecho.MatterReuse
#print axioms F1Fecho.MatterReuse.linked_modular_charge
#print axioms F1Fecho.MatterReuse.linked_nonzero_modular_state
#print axioms F1Fecho.MatterReuse.assembleMaxwell
#print axioms F1Fecho.MatterReuse.assembled_tensor_is_original
#print axioms F1Fecho.MatterReuse.assembled_tensor_on_domain
#print axioms F1Fecho.MatterReuse.standardWedgeH3
