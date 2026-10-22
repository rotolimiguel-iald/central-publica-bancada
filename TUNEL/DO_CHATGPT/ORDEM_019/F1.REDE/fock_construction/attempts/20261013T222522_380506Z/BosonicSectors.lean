import BosonicTwoParticle
import Mathlib.Analysis.InnerProductSpace.l2Space
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open UniformSpace
open scoped TensorProduct
namespace F1Rede.BosonicSectors
open TGLExt.ImportedSQ F1Rede.BosonicTwoParticle

/-- Recursively bracketed algebraic tensor powers; completion is performed only
after constructing all adjacent permutations. The zero sector is the scalar field. -/
structure PreHilbert where
  carrier : Type
  [instN : NormedAddCommGroup carrier]
  [instI : InnerProductSpace ℂ carrier]
attribute [instance] PreHilbert.instN PreHilbert.instI

def powerData : ℕ → PreHilbert
  | 0 => ⟨ℂ⟩
  | n+1 => ⟨H1 ⊗[ℂ] (powerData n).carrier⟩

abbrev Algebraic (n : ℕ) := (powerData n).carrier

def algebraicGamma (u : H1 ≃ₗᵢ[ℂ] H1) : (n : ℕ) → Algebraic n ≃ₗᵢ[ℂ] Algebraic n
  | 0 => LinearIsometryEquiv.refl ℂ ℂ
  | n+1 => TensorProduct.congrIsometry u (algebraicGamma u n)

end F1Rede.BosonicSectors
