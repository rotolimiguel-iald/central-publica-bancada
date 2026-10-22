import SpacelikeOpenClosureR5

/-! The common spacelike region of a compact set is open. Only one original
support is closed; no strict separation of both closed supports is assumed. -/
set_option autoImplicit false
noncomputable section
open Filter
open scoped Topology
namespace F1Fecho.SpacelikeGeometry
open TGL.SpecificAQFT

def commonSpacelike (A:Set V) : Set V := {y | ∀x∈A,minkowskiSq (x-y)<0}

theorem commonSpacelike_open (A:Set V) (hA:IsCompact A) : IsOpen (commonSpacelike A) := by
  apply isOpen_iff_mem_nhds.mpr
  intro y hy
  exact hA.eventually_forall_of_forall_eventually (fun x hx=>by
    have hc:Continuous (fun z:V×V=>minkowskiSq (z.2-z.1)) :=
      continuous_minkowskiSq.comp (continuous_snd.sub continuous_fst)
    exact (isOpen_lt hc continuous_const).mem_nhds (hy x hx))

theorem support_subset_common_closure (A B:Set V) (h:SpacelikeSep A B)
    (hB:IsOpen B) : B⊆commonSpacelike (closure A) := by
  intro y hy x hx
  exact spacelike_closure_left_of_open A B h hB x hx y hy

theorem commonSpacelike_separation (A:Set V) : SpacelikeSep A (commonSpacelike A) :=
  fun x hx y hy=>hy x hx

theorem compact_common_neighborhood (A B:Set V) (hA:IsCompact (closure A))
    (hB:IsOpen B) (h:SpacelikeSep A B) :
    ∃ U:Set V,IsOpen U ∧ B⊆U ∧ SpacelikeSep (closure A) U :=
  ⟨commonSpacelike (closure A),commonSpacelike_open _ hA,
    support_subset_common_closure A B h hB,commonSpacelike_separation _⟩

end F1Fecho.SpacelikeGeometry
#print axioms F1Fecho.SpacelikeGeometry.commonSpacelike_open
#print axioms F1Fecho.SpacelikeGeometry.compact_common_neighborhood
