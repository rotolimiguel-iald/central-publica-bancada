import PhysicalSmearTranslationR2
import PhysicalCompactPairLocalityR1

/-! The real bilinear symplectic pairing of the actual Maxwell test map.
No causal locality is assumed or proved by bilinearity alone. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen TGLExt.ImportedSQ

def circularSmearCLM : SchwartzTensor →L[ℂ] H1 :=
  circularH1.symm.toLinearIsometry.toContinuousLinearMap.comp physicalSmearCLM

theorem circularSmearCLM_apply (f : SchwartzTensor) :
    circularSmearCLM f = circularSmear f := rfl

def physicalTestPairing : SchwartzTensor →ₗ[ℝ] SchwartzTensor →ₗ[ℝ] ℝ where
  toFun f :=
    { toFun := fun g => (inner ℂ (circularSmearCLM f) (circularSmearCLM g)).im
      map_add' := by intro g h; simp only [map_add,inner_add_right,Complex.add_im]
      map_smul' := by
        intro r g
        simp only [map_smul_of_tower,← Complex.coe_smul,inner_smul_real_right,
          Complex.smul_im,smul_eq_mul,RingHom.id_apply] }
  map_add' := by
    intro f g
    ext h
    simp only [map_add,inner_add_left,Complex.add_im,LinearMap.add_apply]
  map_smul' := by
    intro r f
    ext g
    simp only [map_smul_of_tower,← Complex.coe_smul,inner_smul_real_left,
      Complex.smul_im,smul_eq_mul,LinearMap.smul_apply,RingHom.id_apply]

theorem physicalTestPairing_apply (f g : SchwartzTensor) :
    physicalTestPairing f g = (inner ℂ (circularSmear f) (circularSmear g)).im := rfl

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.physicalTestPairing
