import ContratoQG_v31_Minimal
import TeleologicalMatrix_v2

set_option autoImplicit false
noncomputable section
open MeasureTheory Matrix Set
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
namespace ChatgptAudit.TeleologicalContract016
namespace TM := ChatgptAudit.TeleologicalMatrix016
namespace NR := ChatgptAudit.NullRay016

theorem null_direction_exact : nullDir=TM.n := rfl

theorem source_density_exact {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H) :
    nullEnergy T ψ=TM.sourceDensity (T.T ψ) := rfl

theorem area_density_exact (G : ℝ) (f : TM.StressSource) :
    areaDensity (TM.response G f)=TM.responseArea G f := rfl

theorem propagated_geometry_in_contract (G : ℝ) (f : TM.StressSource) (x : Fin 4 → ℝ) :
    (TM.response G f x)ᵀ=TM.response G f x ∧
    (TM.response G f x).mulVec nullDir=0 ∧
    areaDensity (TM.response G f) x=NR.area nullDir (8*Real.pi*G) (TM.sourceDensity f) x :=
  TM.response_fields G f x

theorem local_equations_in_contract {W : TGLSpecificAQFTWitness} (T : StressTensorData W)
    (ψ : W.H) (G : ℝ) (x : Fin 4 → ℝ)
    (hc : Continuous (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)))
    (hi : ∀ l, IntegrableOn (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)) (Ioi l))
    (hm : ∀ l, IntegrableOn (fun u : ℝ => u*nullEnergy T ψ (x+u • nullDir)) (Ioi l)) :
    HasDerivAt (fun u : ℝ => areaDensity (TM.response G (T.T ψ)) (x+u • nullDir))
      (NR.expansion nullDir (8*Real.pi*G) (nullEnergy T ψ) x) 0 ∧
    HasDerivAt (fun u : ℝ => NR.expansion nullDir (8*Real.pi*G) (nullEnergy T ψ)
      (x+u • nullDir)) (-(8*Real.pi*G)*nullEnergy T ψ x) 0 :=
  TM.response_ray_equations G (T.T ψ) x hc hi hm

#print axioms null_direction_exact
#print axioms source_density_exact
#print axioms area_density_exact
#print axioms propagated_geometry_in_contract
#print axioms local_equations_in_contract
end ChatgptAudit.TeleologicalContract016
