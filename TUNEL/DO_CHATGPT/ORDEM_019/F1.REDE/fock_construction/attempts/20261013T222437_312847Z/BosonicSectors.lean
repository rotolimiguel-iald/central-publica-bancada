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
def Algebraic : ℕ → Type
  | 0 => ℂ
  | n+1 => H1 ⊗[ℂ] Algebraic n

instance algebraicNorm : (n : ℕ) → NormedAddCommGroup (Algebraic n)
  | 0 => inferInstanceAs (NormedAddCommGroup ℂ)
  | n+1 => by
    letI := algebraicNorm n
    letI := algebraicInner n
    exact inferInstanceAs (NormedAddCommGroup (H1 ⊗[ℂ] Algebraic n))
where
  algebraicInner : (n : ℕ) → @InnerProductSpace ℂ (Algebraic n) _ (algebraicNorm n)
    | 0 => inferInstanceAs (InnerProductSpace ℂ ℂ)
    | n+1 => by
      letI := algebraicNorm n
      letI := algebraicInner n
      exact inferInstanceAs (InnerProductSpace ℂ (H1 ⊗[ℂ] Algebraic n))

instance algebraicIP (n : ℕ) : InnerProductSpace ℂ (Algebraic n) :=
  algebraicNorm.algebraicInner n

def algebraicGamma (u : H1 ≃ₗᵢ[ℂ] H1) : (n : ℕ) → Algebraic n ≃ₗᵢ[ℂ] Algebraic n
  | 0 => LinearIsometryEquiv.refl ℂ ℂ
  | n+1 => TensorProduct.congrIsometry u (algebraicGamma u n)

end F1Rede.BosonicSectors
