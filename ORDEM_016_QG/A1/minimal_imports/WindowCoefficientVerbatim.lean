import WindowLemmasVerbatim
import TGLExt.TriadMaster
set_option autoImplicit false
namespace TGLExt.ContratoQGv31.ContratoH3
open TGL.SpecificAQFT TGL.ModularRealization TGLExt
noncomputable section
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization} {T : StressTensorData W}
theorem einstein_coefficient_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowHeat C.H2.kappa T ψ x c d
      = C.H2.kappa * windowArea (C.response ψ) x c d / (8 * Real.pi * C.G) := by
  rw [clausius_window, bekenstein_hawking_window C hψ x c d hθ]
  unfold ContratoH2.unruhTemperature
  exact einstein_coefficient_from_clausius _ _ _ C.G_pos.ne'


#print axioms einstein_coefficient_window
end
end TGLExt.ContratoQGv31.ContratoH3
