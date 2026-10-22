import ContratoQG_v31_Minimal

set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory Matrix Set
open TGLExt.ContratoQGv31
namespace ChatgptAudit.NullPropagator016

abbrev Source := (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ

def areaResponse (G : ℝ) (f : Source) (x : Fin 4 → ℝ) : ℝ :=
  -(8*Real.pi*G)*(∫ u : ℝ in Ioi 0,
    u*pairing (f (x+u • nullDir)) nullDir nullDir)

def screenMetric (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![0,0,-a,-a]

def propagator (G : ℝ) (f : Source) (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  screenMetric (areaResponse G f x)

theorem areaResponse_zero (G : ℝ) : areaResponse G 0 = 0 := by
  funext x
  simp [areaResponse,pairing]

theorem areaResponse_covariant (G : ℝ) (f : Source) (b : Fin 4 → ℝ) :
    areaResponse G (fun x => f (x-b)) = fun x => areaResponse G f (x-b) := by
  funext x
  have heq : ∀ u : ℝ, x+u • nullDir-b = (x-b)+u • nullDir := by
    intro u; abel
  simp only [areaResponse,heq]

theorem screenMetric_zero : screenMetric 0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [screenMetric,Matrix.diagonal]

theorem screenMetric_symmetric (a : ℝ) : (screenMetric a)ᵀ=screenMetric a := by
  simp [screenMetric]

theorem screenMetric_gauge (a : ℝ) : (screenMetric a).mulVec nullDir=0 := by
  ext i
  fin_cases i <;> simp [screenMetric,nullDir,Matrix.mulVec,dotProduct,Fin.sum_univ_succ,Matrix.diagonal]

theorem screenMetric_area (a : ℝ) (x : Fin 4 → ℝ) :
    areaDensity (fun _ => screenMetric a) x=a := by
  simp [areaDensity,screenMetric,Matrix.diagonal]
  ring

theorem propagator_zero (G : ℝ) : propagator G 0=0 := by
  funext x
  simp only [propagator,areaResponse_zero,Pi.zero_apply,screenMetric_zero]

theorem propagator_covariant (G : ℝ) (f : Source) (b : Fin 4 → ℝ) :
    propagator G (fun x => f (x-b)) = fun x => propagator G f (x-b) := by
  funext x
  simp only [propagator,areaResponse_covariant]

theorem propagator_geometric_fields (G : ℝ) (f : Source) (x : Fin 4 → ℝ) :
    (propagator G f x)ᵀ=propagator G f x ∧
    (propagator G f x).mulVec nullDir=0 ∧
    areaDensity (propagator G f) x=areaResponse G f x := by
  refine ⟨screenMetric_symmetric _,screenMetric_gauge _,?_⟩
  exact screenMetric_area _ x

#print axioms areaResponse_zero
#print axioms areaResponse_covariant
#print axioms screenMetric_zero
#print axioms screenMetric_symmetric
#print axioms screenMetric_gauge
#print axioms screenMetric_area
#print axioms propagator_zero
#print axioms propagator_covariant
#print axioms propagator_geometric_fields
end ChatgptAudit.NullPropagator016
