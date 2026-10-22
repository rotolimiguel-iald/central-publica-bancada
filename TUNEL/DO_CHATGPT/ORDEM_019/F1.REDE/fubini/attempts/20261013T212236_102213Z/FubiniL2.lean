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

theorem measurable_of_distances {X Y : Type*} [MeasurableSpace X]
    [MetricSpace Y] [SecondCountableTopology Y] [MeasurableSpace Y] [BorelSpace Y]
    (f : X → Y) (hf : ∀ y, Measurable (fun x => dist (f x) y)) : Measurable f := by
  apply measurable_of_isOpen
  intro s hs
  let B : Set (Set Y) := {b | ∃ y r, b = Metric.ball y r ∧ b ⊆ s}
  have hB : ∀ b ∈ B, IsOpen b := by
    rintro b ⟨y,r,rfl,_⟩
    exact Metric.isOpen_ball
  have hBs : ⋃₀ B = s := by
    apply Set.Subset.antisymm
    · rintro y ⟨b, ⟨z,r,rfl,hsub⟩,hy⟩
      exact hsub hy
    · intro y hy
      obtain ⟨r,hr,hsub⟩ := Metric.isOpen_iff.mp hs y hy
      exact ⟨Metric.ball y r, ⟨y,r,rfl,hsub⟩, Metric.mem_ball_self hr⟩
  obtain ⟨C,hC,hCB,hCover⟩ := TopologicalSpace.isOpen_sUnion_countable B hB
  rw [← hBs, ← hCover, Set.preimage_sUnion]
  apply MeasurableSet.biUnion hC
  intro b hb
  obtain ⟨y,r,rfl,_⟩ := hCB hb
  exact measurableSet_lt (hf y) measurable_const

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

theorem measurable_section_eLpNorm (f : α × β → E) (hf : StronglyMeasurable f) :
    Measurable (fun y => eLpNorm (fun x => f (x,y)) 2 μ) := by
  simp_rw [eLpNorm_eq_lintegral_rpow_enorm_toReal (by norm_num : (2:ℝ≥0∞) ≠ 0)
    (by norm_num : (2:ℝ≥0∞) ≠ ⊤)]
  exact ((hf.enorm.pow_const _).lintegral_prod_left').pow_const _

theorem measurableSet_good_sections (f : Lp E 2 (μ.prod ν)) :
    MeasurableSet {y | MemLp (fun x => f (x,y)) 2 μ} := by
  have heq : {y | MemLp (fun x => f (x,y)) 2 μ} =
      {y | eLpNorm (fun x => f (x,y)) 2 μ < ⊤} := by
    ext y
    exact and_iff_right ((Lp.stronglyMeasurable f).comp_measurable
      (measurable_id.prodMk measurable_const)).aestronglyMeasurable
  rw [heq]
  exact measurableSet_lt (measurable_section_eLpNorm f (Lp.stronglyMeasurable f)) measurable_const

theorem sectionLp_dist (f : Lp E 2 (μ.prod ν)) (g : Lp E 2 μ) (y : β)
    (hy : MemLp (fun x => f (x,y)) 2 μ) :
    dist (sectionLp f y) g = (eLpNorm (fun x => f (x,y) - g x) 2 μ).toReal := by
  classical
  rw [sectionLp, dif_pos hy, Lp.dist_def]
  congr 1
  apply eLpNorm_congr_ae
  exact hy.coeFn_toLp.sub ae_eq_rfl

theorem sectionLp_stronglyMeasurable [IsSeparable μ] [TopologicalSpace.SeparableSpace E]
    (f : Lp E 2 (μ.prod ν)) : StronglyMeasurable (sectionLp f) := by
  classical
  letI : Fact ((2:ℝ≥0∞) ≠ ⊤) := ⟨by norm_num⟩
  borelize ↥(Lp E 2 μ)
  apply Measurable.stronglyMeasurable
  apply measurable_of_distances
  intro g
  have hm : Measurable (fun y => (eLpNorm (fun x => f (x,y) - g x) 2 μ).toReal) :=
    (measurable_section_eLpNorm (fun z => f z - g z.1)
      ((Lp.stronglyMeasurable f).sub ((Lp.stronglyMeasurable g).comp_measurable measurable_fst))).ennreal_toReal
  convert hm.piecewise (measurableSet_good_sections f) (measurable_const (a := dist 0 g)) using 1
  ext y
  by_cases hy : MemLp (fun x => f (x,y)) 2 μ
  · simp only [Set.piecewise, Set.mem_setOf_eq, hy, if_true]
    exact sectionLp_dist f g y hy
  · simp only [Set.piecewise, Set.mem_setOf_eq, hy, if_false, sectionLp, dif_neg hy]

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
