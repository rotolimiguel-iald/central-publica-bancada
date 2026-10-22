import WickBoostRotation_v2
import TGLExt.GeometryFluctuation
import TGLExt.TheAngleIsTheProjection

set_option autoImplicit false
noncomputable section
open Matrix NormedSpace
namespace ChatgptAudit.Wick016

theorem genK_eq_Grot : TGLExt.genK = TGLExt.Grot := rfl

theorem rotGen_complex_eq_Grot : TGLExt.rotGen.map Complex.ofReal = TGLExt.Grot := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [TGLExt.rotGen,TGLExt.Grot]

theorem exp_genK_eq_rotation (phi : ℝ) :
    exp ((phi : ℂ) • TGLExt.genK) = TGLExt.Smat phi := by
  rw [genK_eq_Grot, TGLExt.exp_smul_Grot]

theorem exp_complex_rotGen_eq_rotation (phi : ℝ) :
    exp ((phi : ℂ) • TGLExt.rotGen.map Complex.ofReal) = TGLExt.Smat phi := by
  rw [rotGen_complex_eq_Grot, TGLExt.exp_smul_Grot]

theorem wick_boost_eq_exp_genK (phi : ℝ) :
    wickW⁻¹ * complexBoost (Complex.I*(phi : ℂ)) * wickW =
      exp ((phi : ℂ) • TGLExt.genK) := by
  rw [genK_eq_Grot, wick_boost_exponential]

theorem wick_boost_eq_exp_rotGen (phi : ℝ) :
    wickW⁻¹ * complexBoost (Complex.I*(phi : ℂ)) * wickW =
      exp ((phi : ℂ) • TGLExt.rotGen.map Complex.ofReal) := by
  rw [rotGen_complex_eq_Grot, wick_boost_exponential]

#print axioms genK_eq_Grot
#print axioms rotGen_complex_eq_Grot
#print axioms exp_genK_eq_rotation
#print axioms exp_complex_rotGen_eq_rotation
#print axioms wick_boost_eq_exp_genK
#print axioms wick_boost_eq_exp_rotGen
end ChatgptAudit.Wick016
