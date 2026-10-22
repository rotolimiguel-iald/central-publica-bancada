import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.SeparableMeasure
import Mathlib.MeasureTheory.Function.LpSpace.Complete
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1200000
open MeasureTheory Filter Topology
open scoped ENNReal


namespace F1Rede
variable {α β E : Type*} [MeasurableSpace α] [MeasurableSpace β]
  [NormedAddCommGroup E] {μ : Measure α} {ν : Measure β} [SFinite μ] [SFinite ν]

theorem memLp_section_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, MemLp (fun x => f (x,y)) 2 μ := by
  have hint := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp (Lp.memLp f)
  filter_upwards [hint.prod_left_ae] with y hy
  exact (memLp_two_iff_integrable_sq_norm
    ((Lp.stronglyMeasurable f).comp_measurable (measurable_id.prodMk measurable_const)).aestronglyMeasurable).mpr hy

noncomputable def sectionLp (f : Lp E 2 (μ.prod ν)) (y : β) : Lp E 2 μ := by
  classical
  exact if h : MemLp (fun x => f (x,y)) 2 μ then h.toLp (fun x => f (x,y)) else 0

theorem sectionLp_coe_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, (sectionLp f y : α → E) =ᵐ[μ] fun x => f (x,y) := by
  classical
  filter_upwards [memLp_section_ae f] with y hy
  simp only [sectionLp, dif_pos hy]
  exact hy.coeFn_toLp

section RealInner
variable [InnerProductSpace ℝ E]

theorem norm_sq_integral (f : Lp E 2 μ) :
    ‖f‖^2 = ∫ x, ‖f x‖^2 ∂μ := by
  rw [← real_inner_self_eq_norm_sq, L2.inner_def]
  simp only [real_inner_self_eq_norm_sq]

theorem sectionLp_norm_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, ‖sectionLp f y‖^2 = ∫ x, ‖f (x,y)‖^2 ∂μ := by
  filter_upwards [sectionLp_coe_ae f] with y hy
  rw [norm_sq_integral]
  exact integral_congr_ae (hy.mono fun x hx => by simpa only using congrArg (fun z : E => ‖z‖^2) hx)

theorem norm_sq_disintegration (f : Lp E 2 (μ.prod ν)) :
    ‖f‖^2 = ∫ y, ‖sectionLp f y‖^2 ∂ν := by
  rw [norm_sq_integral, integral_prod_symm]
  · exact integral_congr_ae ((sectionLp_norm_ae f).mono fun _ hy => hy.symm)
  · exact (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp (Lp.memLp f)

end RealInner
#print axioms memLp_section_ae
#print axioms sectionLp_coe_ae
#print axioms norm_sq_integral
#print axioms sectionLp_norm_ae
#print axioms norm_sq_disintegration
end F1Rede
