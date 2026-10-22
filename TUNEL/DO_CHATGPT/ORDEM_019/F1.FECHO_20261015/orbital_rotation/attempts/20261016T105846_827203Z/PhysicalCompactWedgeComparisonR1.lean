import PhysicalCompactNetCovarianceR1
import PhysicalWedgeSchwartzClosureR3
import TGLExt.LightOneParticleByTerm

/-! Comparison of the compact-test wedge with the original Schwartz-test
wedge. Cutoffs give compact support; a positive spatial shift moves its
closure into the open wedge. Strong continuity removes the shift. The
same smearing map and H1 are used throughout. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open Filter
open scoped Topology
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.SpacetimeLorentz TGLExt.ImportedSQ

def inwardWedgeShift (e : ℝ) : Spacetime := coordinateEquiv.symm (fun i => if i=1 then e else 0)

theorem inwardWedgeShift_zero : inwardWedgeShift 0=0 := by
  apply PiLp.ext
  intro i
  simp [inwardWedgeShift]

theorem cutoff_wedge_support (s : ℝ) (f : SchwartzTensor)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    Function.support (SchwartzCutoff.cutoff s f : Spacetime → TensorValue) ⊆ physicalRightWedge := by
  intro x hx
  apply hs
  intro hz
  exact hx (by rw [SchwartzCutoff.cutoff_apply,hz,smul_zero])

theorem shifted_compact_wedge_tsupport (e : ℝ) (he : 0<e) (f : SchwartzTensor)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    tsupport (translateTest (inwardWedgeShift e) f : Spacetime → TensorValue) ⊆ physicalRightWedge := by
  have hclosed : IsClosed {x : Spacetime | |x 0| ≤ x 1} := isClosed_le (by fun_prop) (by fun_prop)
  have hts : tsupport (f : Spacetime → TensorValue) ⊆ {x : Spacetime | |x 0| ≤ x 1} :=
    closure_minimal (fun x hx => (hs hx).le) hclosed
  rw [translateTest_tsupport]
  intro x hx
  have hb := hts hx
  change |(x-inwardWedgeShift e) 0| ≤ (x-inwardWedgeShift e) 1 at hb
  have hzero : inwardWedgeShift e 0=0 := by simp [inwardWedgeShift]
  have hone : inwardWedgeShift e 1=e := by simp [inwardWedgeShift]
  simp only [PiLp.sub_apply,hzero,hone,sub_zero] at hb
  change |x 0|<x 1
  linarith

theorem shifted_wedge_smear_mem_compact (e : ℝ) (he : 0<e) (f : SchwartzTensor)
    (hr : IsRealTest f)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    U1 (fun i => inwardWedgeShift e i) (circularSmear f) ∈ compactLocalized physicalRightWedge := by
  have ht := (U1 (fun i => inwardWedgeShift e i)).continuous.continuousAt.tendsto.comp
    (circularSmear_continuous.continuousAt.tendsto.comp (SchwartzCutoff.cutoffSequence_tendsto f))
  apply (compactLocalized_closed physicalRightWedge).mem_of_tendsto ht
  apply Eventually.of_forall
  intro n
  let g := SchwartzCutoff.cutoffSequence f n
  have hgr : IsRealTest g := cutoff_real _ f hr
  have hgc : HasCompactSupport (g : Spacetime → TensorValue) :=
    SchwartzCutoff.cutoff_compact _ (by positivity) f
  have hgs : Function.support (g : Spacetime → TensorValue) ⊆ physicalRightWedge :=
    cutoff_wedge_support _ f hs
  exact (Submodule.le_topologicalClosure _) (Submodule.subset_span
    ⟨translateTest (inwardWedgeShift e) g,translateTest_real _ g hgr,
      translateTest_compact _ g hgc,shifted_compact_wedge_tsupport e he g hgs,
      circularSmear_translate _ g⟩)

theorem wedge_smear_mem_compact (f : SchwartzTensor) (hr : IsRealTest f)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    circularSmear f ∈ compactLocalized physicalRightWedge := by
  have ha : Tendsto (fun n : ℕ => fun i : Fin 4 => inwardWedgeShift (1/((n:ℝ)+1)) i)
      atTop (𝓝 (0 : Fin 4 → ℝ)) := by
    apply tendsto_pi_nhds.mpr
    intro i
    by_cases hi : i=1
    · simpa [inwardWedgeShift,hi] using (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))
    · simpa [inwardWedgeShift,hi] using (tendsto_const_nhds : Tendsto (fun _ : ℕ => (0 : ℝ)) atTop (𝓝 0))
  have ht := (TGLExt.LightByTerm.light_translations_strongly_continuous (circularSmear f)).continuousAt.tendsto.comp ha
  rw [U1_zero] at ht
  apply (compactLocalized_closed physicalRightWedge).mem_of_tendsto ht
  exact Eventually.of_forall (fun n => shifted_wedge_smear_mem_compact _ (by positivity) f hr hs)

theorem compactLocalized_rightWedge_eq :
    compactLocalized physicalRightWedge=localized physicalRightWedge := by
  apply le_antisymm (compactLocalized_le_localized _)
  apply Submodule.topologicalClosure_minimal _ _ (compactLocalized_closed _)
  apply Submodule.span_le.mpr
  rintro v ⟨f,hr,hs,rfl⟩
  exact wedge_smear_mem_compact f hr hs

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.shifted_compact_wedge_tsupport
#print axioms F1Fecho.MaxwellLocalization.wedge_smear_mem_compact
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_rightWedge_eq
