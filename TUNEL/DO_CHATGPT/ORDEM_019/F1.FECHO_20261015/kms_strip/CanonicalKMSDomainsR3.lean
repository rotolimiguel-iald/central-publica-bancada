import CanonicalFockPolarR1

/-! Genuine half-modular domains for the concrete Weyl algebra/vacuum pair.
These are consequences of the closed Tomita graph, not extra analytic-vector
assumptions. The strip spectral representation is supplied separately. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.CanonicalKMSDomains
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.ExponentialLift F1Fecho.ExponentialTomita
open F1Fecho.WedgePairTomita F1Fecho.ExponentialTomitaEquality
open F1Fecho.CanonicalFockPolar F1Fecho.Antilinear

theorem algebra_vector_half_domain (A : F→L[ℂ]F) (hA : A∈algebra KWR) :
    A vacuum ∈ canonicalLift.domain :=
  tomita_domain_eq ▸ algebra_vector_domain KWR A hA

theorem half_on_algebra_vector (A : F→L[ℂ]F) (hA : A∈algebra KWR) :
    canonicalLift ⟨A vacuum,algebra_vector_half_domain A hA⟩ = JF ((star A) vacuum) := by
  apply JF.injective
  rw [canonicalFockJ_involutive]
  calc
    JF (canonicalLift ⟨A vacuum,algebra_vector_half_domain A hA⟩) =
        S KWR ⟨A vacuum,algebra_vector_domain KWR A hA⟩ :=
      (actual_tomita_polar ⟨A vacuum,algebra_vector_domain KWR A hA⟩).symm
    _ = _ := S_algebra_vector KWR A hA

theorem half_on_adjoint_vector (A : F→L[ℂ]F) (hA : A∈algebra KWR) :
    canonicalLift ⟨(star A) vacuum,algebra_vector_half_domain (star A) (star_mem hA)⟩ =
      JF (A vacuum) := by
  simpa only [_root_.star_star] using half_on_algebra_vector (star A) (star_mem hA)

theorem half_vector_norm (A : F→L[ℂ]F) (hA : A∈algebra KWR) :
    ‖canonicalLift ⟨A vacuum,algebra_vector_half_domain A hA⟩‖ = ‖(star A) vacuum‖ := by
  rw [half_on_algebra_vector A hA,JF.norm_map]

end F1Fecho.CanonicalKMSDomains
#print axioms F1Fecho.CanonicalKMSDomains.algebra_vector_half_domain
#print axioms F1Fecho.CanonicalKMSDomains.half_on_algebra_vector
#print axioms F1Fecho.CanonicalKMSDomains.half_on_adjoint_vector
#print axioms F1Fecho.CanonicalKMSDomains.half_vector_norm
