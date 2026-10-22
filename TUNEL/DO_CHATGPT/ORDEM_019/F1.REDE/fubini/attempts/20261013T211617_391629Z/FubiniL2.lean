import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.SeparableMeasure
import Mathlib.MeasureTheory.Function.LpSpace.Complete
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1200000
open MeasureTheory Filter Topology
open scoped ENNReal

#check Lp.memLp
#check memLp_two_iff_integrable_sq_norm
#check Integrable.prod_left_ae
#check Integrable.prod_right_ae
#check StronglyMeasurable.prodMk_right
#check StronglyMeasurable.prodMk_left
#check integral_prod_symm
#check L2.norm_sq_eq_integral
#check L2.norm_sq_eq_integral_norm_sq
#check Lp.norm_def
#check measurable_of_measurable_dist
#check measurable_of_measurable_dist_countable
#check measurable_of_measurable_edist
#check Measurable.stronglyMeasurable
#check MeasureTheory.Lp.SecondCountableTopology
#check MemLp.toLp
#check MemLp.coeFn_toLp
#check MeasureTheory.lintegral_prod_symm
#check MeasureTheory.AEStronglyMeasurable.integral_prod_left'
#check MeasureTheory.StronglyMeasurable.integral_prod_left'

namespace F1Rede
variable {α β E : Type*} [MeasurableSpace α] [MeasurableSpace β]
  [NormedAddCommGroup E] {μ : Measure α} {ν : Measure β} [SFinite μ] [SFinite ν]

theorem memLp_section_ae (f : Lp E 2 (μ.prod ν)) :
    ∀ᵐ y ∂ν, MemLp (fun x => f (x,y)) 2 μ := by
  have hint := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp (Lp.memLp f)
  filter_upwards [hint.prod_right_ae] with y hy
  exact (memLp_two_iff_integrable_sq_norm
    ((Lp.stronglyMeasurable f).comp_measurable (measurable_id.prodMk measurable_const)).aestronglyMeasurable).mpr hy

#print axioms memLp_section_ae
end F1Rede
