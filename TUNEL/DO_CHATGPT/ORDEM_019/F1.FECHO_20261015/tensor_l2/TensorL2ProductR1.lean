import VectorTensorL2R2
import L2UnitaryMapR2
import FubiniL2

/-! Two vector-valued L2 factors represented on the product measure, on the
same completed Hilbert tensor product. No spectral or modular statement is
asserted here. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory UniformSpace TopologicalSpace
open scoped TensorProduct ENNReal
namespace F1Fecho.TensorL2Product
open CompletedTensor
variable {X Y E F : Type*} [MeasurableSpace X] [MeasurableSpace Y]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

theorem tensor_separable [SeparableSpace E] [SeparableSpace F] : SeparableSpace (CT E F) := by
  have hc : Continuous (pure (E:=E) (F:=F)) :=
    (Completion.continuous_coe _).comp ((bilinear (E:=E) (F:=F)).continuous₂.comp₂
      continuous_fst continuous_snd)
  have hs := (isSeparable_range hc).span (R:=ℂ) |>.closure
  have ht := pure_total (E:=E) (F:=F)
  change (Submodule.span ℂ (Set.range (pure (E:=E) (F:=F)))).topologicalClosure=⊤ at ht
  rw [← Submodule.topologicalClosure_coe,ht] at hs
  exact isSeparable_univ_iff.mp hs

variable (μ : Measure X) (ν : Measure Y)

def innerUnitary : CT E (Lp F 2 ν)≃ₗᵢ[ℂ]Lp (CT E F) 2 ν :=
  (comm (E:=E) (F:=Lp F 2 ν)).trans
    ((VectorTensorL2.unitary ν).trans (L2UnitaryMap.unitary ν comm))

theorem innerUnitary_ae (x:E) (g:Lp F 2 ν) :
    innerUnitary ν (pure (x,g)) =ᵐ[ν] fun y=>pure (x,g y) := by
  change L2UnitaryMap.unitary ν comm (VectorTensorL2.unitary ν (comm (pure (x,g)))) =ᵐ[ν] _
  rw [comm_pure]
  filter_upwards [L2UnitaryMap.unitary_ae ν comm (VectorTensorL2.unitary ν (pure (g,x))),
    VectorTensorL2.pure_ae ν g x] with y hy hg
  rw [hy,hg,comm_pure]

/-- The intermediate nested representation requires no separability or S-finiteness. -/
def nestedUnitary : CT (Lp E 2 μ) (Lp F 2 ν)≃ₗᵢ[ℂ]Lp (Lp (CT E F) 2 ν) 2 μ :=
  (VectorTensorL2.unitary μ).trans (L2UnitaryMap.unitary μ (innerUnitary ν))

theorem nestedUnitary_ae (f:Lp E 2 μ) (g:Lp F 2 ν) :
    ∀ᵐ x ∂μ, nestedUnitary μ ν (pure (f,g)) x =ᵐ[ν] fun y=>pure (f x,g y) := by
  filter_upwards [L2UnitaryMap.unitary_ae μ (innerUnitary ν)
    (VectorTensorL2.unitary μ (pure (f,g))),VectorTensorL2.pure_ae μ f g] with x hx hf
  change nestedUnitary μ ν (pure (f,g)) x=innerUnitary ν
    (VectorTensorL2.unitary μ (pure (f,g)) x) at hx
  rw [hx,hf]
  exact innerUnitary_ae ν (f x) g

variable [SFinite μ] [SFinite ν] [IsSeparable ν]
  [SeparableSpace E] [SeparableSpace F]

/-- The order is ν.prod μ, matching the existing Fubini convention. -/
def unitary : CT (Lp E 2 μ) (Lp F 2 ν)≃ₗᵢ[ℂ]Lp (CT E F) 2 (ν.prod μ) := by
  letI : SeparableSpace (CT E F) := tensor_separable
  letI : InnerProductSpace ℝ (CT E F) := InnerProductSpace.complexToReal
  exact (nestedUnitary μ ν).trans (F1Rede.fubiniL2Equiv (𝕜:=ℂ)).symm

end F1Fecho.TensorL2Product
#print axioms F1Fecho.TensorL2Product.tensor_separable
#print axioms F1Fecho.TensorL2Product.innerUnitary_ae
#print axioms F1Fecho.TensorL2Product.nestedUnitary_ae
#print axioms F1Fecho.TensorL2Product.unitary
