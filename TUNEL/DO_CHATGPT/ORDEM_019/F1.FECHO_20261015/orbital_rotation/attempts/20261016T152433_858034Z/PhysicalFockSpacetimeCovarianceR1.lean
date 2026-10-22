import PhysicalFockNetRealizationR2
import LorentzFutureRepresentationR1

/-! Covariance of the ACTUAL compact-test Maxwell Weyl net.

The earlier Fock consumer accepts a one-particle covariance premise. Here the
premise is discharged by the existing compact-localization theorems, on the
same H1, helicity representation, bosonic Fock space and net. The spacetime
coordinate adapter is an equality, not a second physical net.

This proves field-net covariance under the already constructed translations
and generated Lorentz transformations, including their composed frames.
It does not realize the mechanical device as this field theory, construct an
interacting/curved net, supply a trace/PF, or inhabit MaxwellCertificate.
-/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.PhysicalFockSpacetime
open TGLExt.ImportedSQ TGL.SpecificAQFT
open F1Rede.BosonicFock F1Fecho.Antilinear
open F1Fecho.MaxwellLocalization F1Fecho.MaxwellGlobal
open F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen

def spacetimeNet (O : Set Spacetime) : VonNeumannAlgebra F :=
  FieldWeyl.R (compactLocalized O)

theorem spacetimeNet_coordinate (O : Set (Fin 4 → ℝ)) :
    spacetimeNet (coordinateRegion O) = PhysicalFockNet.net O := rfl

theorem spacetimeNet_translate (a : Spacetime) (O : Set Spacetime)
    (A : F →L[ℂ] F) :
    A ∈ spacetimeNet O ↔
      (gamma (U1 (fun i => a i))).conjStarAlgEquiv A ∈ spacetimeNet (translateRegion a O) :=
  FieldWeyl.R_covariance (U1 (fun i => a i)) _ _
    (compactLocalized_translate_iff a O) A

theorem spacetimeNet_lorentz (L : generatedLorentz) (O : Set Spacetime)
    (A : F →L[ℂ] F) :
    A ∈ spacetimeNet O ↔
      (gamma (helicityUnitary L)).conjStarAlgEquiv A ∈ spacetimeNet (lorentzRegion L O) :=
  FieldWeyl.R_covariance (helicityUnitary L) _ _
    (compactLocalized_lorentz_iff L O) A

def frameUnitary (L : generatedLorentz) (a : Spacetime) : H1 ≃ₗᵢ[ℂ] H1 :=
  (helicityUnitary L).trans (U1 (fun i => a i))

def frameRegion (L : generatedLorentz) (a : Spacetime) (O : Set Spacetime) : Set Spacetime :=
  translateRegion a (lorentzRegion L O)

theorem compactLocalized_frame (L : generatedLorentz) (a : Spacetime)
    (O : Set Spacetime) (f : H1) :
    f ∈ compactLocalized O ↔ frameUnitary L a f ∈ compactLocalized (frameRegion L a O) :=
  (compactLocalized_lorentz_iff L O f).trans
    (compactLocalized_translate_iff a (lorentzRegion L O) (helicityUnitary L f))

theorem spacetimeNet_frame (L : generatedLorentz) (a : Spacetime)
    (O : Set Spacetime) (A : F →L[ℂ] F) :
    A ∈ spacetimeNet O ↔
      (gamma (frameUnitary L a)).conjStarAlgEquiv A ∈ spacetimeNet (frameRegion L a O) :=
  FieldWeyl.R_covariance (frameUnitary L a) _ _ (compactLocalized_frame L a O) A

theorem spacetimeNet_future_lorentz (L : FutureLorentz) (O : Set Spacetime)
    (A : F →L[ℂ] F) :
    A ∈ spacetimeNet O ↔
      (gamma (helicityUnitary (futureToGenerated L))).conjStarAlgEquiv A ∈
        spacetimeNet (lorentzRegion (futureToGenerated L) O) :=
  spacetimeNet_lorentz (futureToGenerated L) O A

theorem physicalNet_translate (a : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ))
    (A : F →L[ℂ] F) :
    A ∈ PhysicalFockNet.net O ↔
      (gamma (U1 a)).conjStarAlgEquiv A ∈ PhysicalFockNet.net (translate a O) :=
  PhysicalFockNet.net_covariant (U1 a) O (translate a O)
    (compactPhysicalNet_translate a O) A

theorem physicalNet_boost (s : ℝ) (O : Set (Fin 4 → ℝ)) (A : F →L[ℂ] F) :
    A ∈ PhysicalFockNet.net O ↔
      (gamma (B0 s)).conjStarAlgEquiv A ∈
        PhysicalFockNet.net (TGLExt.ContratoQGv31.wedgeBoostMap s '' O) :=
  PhysicalFockNet.net_covariant (B0 s) O _ (compactPhysicalNet_boost s O) A

end F1Fecho.PhysicalFockSpacetime
#print axioms F1Fecho.PhysicalFockSpacetime.spacetimeNet_coordinate
#print axioms F1Fecho.PhysicalFockSpacetime.spacetimeNet_translate
#print axioms F1Fecho.PhysicalFockSpacetime.spacetimeNet_lorentz
#print axioms F1Fecho.PhysicalFockSpacetime.compactLocalized_frame
#print axioms F1Fecho.PhysicalFockSpacetime.spacetimeNet_frame
#print axioms F1Fecho.PhysicalFockSpacetime.spacetimeNet_future_lorentz
#print axioms F1Fecho.PhysicalFockSpacetime.physicalNet_translate
#print axioms F1Fecho.PhysicalFockSpacetime.physicalNet_boost
