import TGLExt.QGSolutionComplete

/-! Strict spacelike separation extends to the closure of one region when
the other remains open. It does not assert strict separation of both closures.
The proof perturbs the second point in both time directions. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter
open scoped Topology
namespace F1Fecho.SpacelikeGeometry
open TGL.SpecificAQFT
abbrev V := Fin 4→ℝ
def timeUnit : V := ![1,0,0,0]

theorem continuous_minkowskiSq : Continuous minkowskiSq := by
  unfold minkowskiSq
  fun_prop

theorem weak_spacelike_closure_left (A B:Set V) (h:SpacelikeSep A B)
    {x:V} (hx:x∈closure A) {y:V} (hy:y∈B) : minkowskiSq (x-y)≤0 := by
  have hc:IsClosed {z:V | minkowskiSq (z-y)≤0} :=
    isClosed_le (continuous_minkowskiSq.comp (continuous_id.sub continuous_const)) continuous_const
  exact hc.closure_subset_iff.mpr (fun z hz=>le_of_lt (h z hz y hy)) hx

theorem spacelike_closure_left_of_open (A B:Set V) (h:SpacelikeSep A B)
    (hB:IsOpen B) : SpacelikeSep (closure A) B := by
  intro x hx y hy
  have hw:=weak_spacelike_closure_left A B h hx hy
  by_contra hn
  have hz:minkowskiSq (x-y)=0 := le_antisymm hw (not_lt.mp hn)
  have hc:Continuous (fun t:ℝ=>y+t • timeUnit) := by fun_prop
  have he:∀ᶠt:ℝ in 𝓝 0,y+t • timeUnit∈B :=
    hc.continuousAt.tendsto.eventually (by simpa using hB.mem_nhds hy)
  obtain ⟨ε,hε,he⟩:=Metric.eventually_nhds_iff.mp he
  have hp:y+(ε/2) • timeUnit∈B := he (by simpa [Real.dist_eq] using (show |ε/2|<ε by rw [abs_of_pos (by positivity)];linarith))
  have hm:y+(-(ε/2)) • timeUnit∈B := he (by simpa [Real.dist_eq,abs_neg] using (show |ε/2|<ε by rw [abs_of_pos (by positivity)];linarith))
  have h1:=weak_spacelike_closure_left A B h hx hp
  have h2:=weak_spacelike_closure_left A B h hx hm
  simp only [minkowskiSq,Pi.sub_apply,Pi.add_apply,Pi.smul_apply,smul_eq_mul,
    timeUnit,Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.cons_val_two,
    Matrix.cons_val_three,mul_one,mul_zero,add_zero] at h1 h2 hz
  nlinarith [sq_pos_of_pos (show 0<ε/2 by positivity)]

end F1Fecho.SpacelikeGeometry
#print axioms F1Fecho.SpacelikeGeometry.weak_spacelike_closure_left
#print axioms F1Fecho.SpacelikeGeometry.spacelike_closure_left_of_open
