import MaxwellSmearingNonzeroR3
import MaxwellSmearingLinearR2
import CanonicalSegalEssentialR6

/-! The concrete on-shell bivector smearing is consumed on the SAME canonical
bosonic Fock. Each compact regular-chart momentum tensor yields an essentially
self-adjoint Segal operator with the existing exponential core. A test gives a
nonzero vacuum excitation. This does not yet construct a spacetime Schwartz
restriction, a Wick stress tensor, or the modular-energy charge identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellSmearing
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Annihilation F1Fecho.Creation

def field (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0) : F →ₗ.[ℂ] F :=
  segal (smear f hreg)

theorem field_essentially_selfadjoint (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0) :
    IsSelfAdjoint (field f hreg).closure := segal_essentially_selfadjoint _

theorem field_has_exponential_core (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0) :
    (field f hreg).closure.HasCore domain := segal_closure_has_exponential_core _

theorem field_vacuum (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0) :
    field f hreg ⟨vacuum,vacuum_mem_domain⟩ =
      ((Real.sqrt 2)⁻¹ : ℂ) • oneParticle (smear f hreg) := segal_vacuum _

theorem exists_nonzero_field_vacuum : ∃ f : TestTensor,
    ∃ hreg : ∀ y∈tsupport f,y.1≠0,field f hreg ⟨vacuum,vacuum_mem_domain⟩≠0 := by
  obtain ⟨f,hreg,hf⟩ := exists_nonzero_smear
  refine ⟨f,hreg,?_⟩
  rw [field_vacuum]
  apply smul_ne_zero
  · exact inv_ne_zero (Complex.ofReal_ne_zero.mpr (Real.sqrt_ne_zero'.mpr (by norm_num)))
  · intro hz
    apply hf
    apply oneParticle.injective
    simpa using hz

end F1Fecho.MaxwellSmearing
#print axioms F1Fecho.MaxwellSmearing.field_essentially_selfadjoint
#print axioms F1Fecho.MaxwellSmearing.field_has_exponential_core
#print axioms F1Fecho.MaxwellSmearing.field_vacuum
#print axioms F1Fecho.MaxwellSmearing.exists_nonzero_field_vacuum
