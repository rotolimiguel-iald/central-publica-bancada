import WeylAntiunitaryR4
import OneParticleDualityR2

/-! The existing antiunitary carries the concrete wedge Weyl algebra to the
algebra of its one-particle symplectic complement. The latter commutes with
the original algebra. Equality with the whole operator commutant, and a polar
identification, are not asserted here. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.WedgeAntiAlgebra
open TGLExt TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.Antilinear F1Fecho.OneParticleDuality

abbrev JF := gammaJ Jcandidate Jcandidate_involutive

def conjugate (a : F →L[ℂ] F) : F →L[ℂ] F where
  toFun v := JF (a (JF v))
  map_add' x y := by simp only [map_add]
  map_smul' c x := by
    simp only [map_smulₛₗ,map_smul,starRingEnd_apply,star_star,RingHom.id_apply]
  cont := JF.continuous.comp (a.continuous.comp JF.continuous)

theorem conjugate_involutive (a : F →L[ℂ] F) : conjugate (conjugate a) = a := by
  apply ContinuousLinearMap.ext
  intro v
  change JF (JF (a (JF (JF v)))) = a v
  simp only [JF,gammaJ_involutive]

theorem conjugate_mul (a b : F →L[ℂ] F) :
    conjugate (a*b) = conjugate a * conjugate b := by
  apply ContinuousLinearMap.ext
  intro v
  change JF (a (b (JF v))) = JF (a (JF (JF (b (JF v)))))
  simp only [JF,gammaJ_involutive]

theorem conjugate_field (f : H1) : conjugate (FieldWeyl.W f) = FieldWeyl.W (-Jcandidate f) := by
  apply ContinuousLinearMap.ext
  intro v
  change JF (FieldWeyl.W f (JF v)) = _
  rw [WeylAntiunitary.field_intertwining]
  simp only [JF,gammaJ_involutive]

theorem image_generators :
    conjugate '' WeylNet.generators FieldWeyl.W KWR.toClosedSubmodule.toSubmodule =
      WeylNet.generators FieldWeyl.W KWR.symplComp.toClosedSubmodule.toSubmodule := by
  ext a
  constructor
  · rintro ⟨b,⟨f,hf,rfl⟩,rfl⟩
    refine ⟨-Jcandidate f,?_,(conjugate_field f).symm⟩
    exact KWR.symplComp.toClosedSubmodule.toSubmodule.neg_mem
      ((Jcandidate_mem_symplectic_iff f).mpr hf)
  · rintro ⟨g,hg,rfl⟩
    refine ⟨FieldWeyl.W (-Jcandidate g),⟨-Jcandidate g,?_,rfl⟩,?_⟩
    · exact KWR.toClosedSubmodule.toSubmodule.neg_mem (Jcandidate_of_symplectic g hg)
    · rw [conjugate_field,map_neg,Jcandidate_involutive,neg_neg]

theorem conjugate_wedge_algebra :
    conjugate '' (FieldWeyl.R KWR.toClosedSubmodule.toSubmodule : Set (F →L[ℂ] F)) =
      (FieldWeyl.R KWR.symplComp.toClosedSubmodule.toSubmodule : Set (F →L[ℂ] F)) := by
  change conjugate '' (WeylNet.generatedAlgebra (WeylNet.generators FieldWeyl.W KWR.toClosedSubmodule.toSubmodule) : Set (F →L[ℂ] F)) =
    (WeylNet.generatedAlgebra (WeylNet.generators FieldWeyl.W KWR.symplComp.toClosedSubmodule.toSubmodule) : Set (F →L[ℂ] F))
  rw [WeylNet.generatedAlgebra_coe _ (WeylNet.generators_star_closed _ FieldWeyl.W_star _),
      WeylNet.generatedAlgebra_coe _ (WeylNet.generators_star_closed _ FieldWeyl.W_star _),
      conj_commutant conjugate conjugate_mul conjugate_involutive,
      conj_commutant conjugate conjugate_mul conjugate_involutive,image_generators]

theorem conjugate_wedge_commutes
    (a : F →L[ℂ] F) (ha : a ∈ FieldWeyl.R KWR.toClosedSubmodule.toSubmodule)
    (b : F →L[ℂ] F) (hb : b ∈ FieldWeyl.R KWR.toClosedSubmodule.toSubmodule) :
    Commute b (conjugate a) := by
  have hac : conjugate a ∈ FieldWeyl.R KWR.symplComp.toClosedSubmodule.toSubmodule := by
    rw [← SetLike.mem_coe,← conjugate_wedge_algebra]
    exact ⟨a,ha,rfl⟩
  exact FieldWeyl.R_local _ _ (fun f hf g hg =>
    ClosedSubmodule.mem_symplComp_iff.mp hg f hf) b hb (conjugate a) hac

end F1Fecho.WedgeAntiAlgebra
#print axioms F1Fecho.WedgeAntiAlgebra.conjugate_involutive
#print axioms F1Fecho.WedgeAntiAlgebra.conjugate_mul
#print axioms F1Fecho.WedgeAntiAlgebra.conjugate_field
#print axioms F1Fecho.WedgeAntiAlgebra.image_generators
#print axioms F1Fecho.WedgeAntiAlgebra.conjugate_wedge_algebra
#print axioms F1Fecho.WedgeAntiAlgebra.conjugate_wedge_commutes
