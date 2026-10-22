import PhysicalCanonicalNetCompleteR1
import LorentzFutureRepresentationR1
import Mathlib.LinearAlgebra.FiniteDimensional.Defs

/-
Concrete finite packets of the EXISTING compact Maxwell smears, on the SAME
H1. Refinement is inclusion of finite lists of generators. Symmetries move
packets; no finite packet is assumed invariant. This does not identify the
packets with MQC cells, prove a device scaling limit, or change its dynamics.
-/
set_option autoImplicit false
set_option maxHeartbeats 500000

noncomputable section
namespace F1Fecho.DeviceContinuumR57
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.MaxwellLocalization
open F1Fecho.OrbitalScreen F1Fecho.OrbitalSpatial

abbrev CompactPacket (O : Set Spacetime) :=
  {s : Finset H1 // (s : Set H1) ⊆ compactSupportedGenerators O}

def packetSpace {O : Set Spacetime} (S : CompactPacket O) : Submodule ℝ H1 :=
  Submodule.span ℝ (S.val : Set H1)

instance packetSpace_finite {O : Set Spacetime} (S : CompactPacket O) :
    FiniteDimensional ℝ (packetSpace S) :=
  FiniteDimensional.span_finset ℝ S.val

def emptyPacket (O : Set Spacetime) : CompactPacket O :=
  ⟨∅, by simp⟩

instance compactPacket_nonempty (O : Set Spacetime) : Nonempty (CompactPacket O) :=
  ⟨emptyPacket O⟩

def joinPacket {O : Set Spacetime} (S T : CompactPacket O) : CompactPacket O := by
  classical
  exact ⟨S.val ∪ T.val, by
    intro v hv
    rcases Finset.mem_union.mp hv with h | h
    · exact S.property h
    · exact T.property h⟩

theorem packetSpace_mono {O : Set Spacetime} {S T : CompactPacket O}
    (h : S.val ⊆ T.val) : packetSpace S ≤ packetSpace T :=
  Submodule.span_mono h

theorem packetSpace_directed (O : Set Spacetime) :
    Directed (· ≤ ·) (@packetSpace O) := by
  classical
  intro S T
  exact ⟨joinPacket S T, packetSpace_mono Finset.subset_union_left,
    packetSpace_mono Finset.subset_union_right⟩

def packetInclusion {O : Set Spacetime} {S T : CompactPacket O}
    (h : S.val ⊆ T.val) : packetSpace S →ₗᵢ[ℝ] packetSpace T where
  toLinearMap := Submodule.inclusion (packetSpace_mono h)
  norm_map' _ := rfl

theorem packetInclusion_comp {O : Set Spacetime} {R S T : CompactPacket O}
    (hRS : R.val ⊆ S.val) (hST : S.val ⊆ T.val) (x : packetSpace R) :
    packetInclusion hST (packetInclusion hRS x) = packetInclusion (hRS.trans hST) x := rfl

theorem packetSpace_le_localized {O : Set Spacetime} (S : CompactPacket O) :
    packetSpace S ≤ compactLocalized O :=
  (Submodule.span_mono S.property).trans (Submodule.le_topologicalClosure _)

def enlargePacket {O P : Set Spacetime} (h : O ⊆ P) (S : CompactPacket O) :
    CompactPacket P :=
  ⟨S.val, by
    intro v hv
    obtain ⟨f, hr, hc, hs, he⟩ := S.property hv
    exact ⟨f, hr, hc, hs.trans h, he⟩⟩

theorem packetSpace_enlarge {O P : Set Spacetime} (h : O ⊆ P) (S : CompactPacket O) :
    packetSpace (enlargePacket h S) = packetSpace S := rfl

theorem packetSpace_iSup (O : Set Spacetime) :
    (⨆ S : CompactPacket O, packetSpace S) =
      Submodule.span ℝ (compactSupportedGenerators O) := by
  classical
  apply le_antisymm
  · exact iSup_le (fun S => Submodule.span_mono S.property)
  · apply Submodule.span_le.mpr
    intro v hv
    let S : CompactPacket O := ⟨{v}, by simpa using hv⟩
    exact (le_iSup (fun S : CompactPacket O => packetSpace S) S)
      (Submodule.subset_span (by simp [S]))

theorem packet_union_closure (O : Set Spacetime) :
    closure (⋃ S : CompactPacket O, (packetSpace S : Set H1)) =
      (compactLocalized O : Set H1) := by
  rw [← Submodule.coe_iSup_of_directed _ (packetSpace_directed O), packetSpace_iSup]
  rfl

/-- Dense global one-particle target, using complexification of the same
real wedge subspace. Real localization is not silently complexified. -/
theorem packet_wedge_complex_dense :
    (Submodule.span ℂ (closure (⋃ S : CompactPacket physicalRightWedge,
      (packetSpace S : Set H1)))).topologicalClosure = ⊤ := by
  rw [packet_union_closure, compactLocalized_rightWedge_eq]
  exact physical_right_wedge_complex_dense

def movePacket {O P : Set Spacetime} (T : H1 →L[ℝ] H1)
    (hT : ∀ v ∈ compactSupportedGenerators O, T v ∈ compactSupportedGenerators P)
    (S : CompactPacket O) : CompactPacket P := by
  classical
  exact ⟨S.val.image T, by
    rintro v hv
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hv
    exact hT x (S.property hx)⟩

theorem packetSpace_move {O P : Set Spacetime} (T : H1 →L[ℝ] H1)
    (hT : ∀ v ∈ compactSupportedGenerators O, T v ∈ compactSupportedGenerators P)
    (S : CompactPacket O) :
    (packetSpace S).map T.toLinearMap = packetSpace (movePacket T hT S) := by
  classical
  rw [packetSpace, Submodule.map_span]
  congr 1
  ext v
  simp [movePacket, packetSpace]

def packetMoveIsometry {O P : Set Spacetime} (T : H1 →L[ℝ] H1)
    (hT : ∀ v ∈ compactSupportedGenerators O, T v ∈ compactSupportedGenerators P)
    (hn : ∀ v : H1, ‖T v‖ = ‖v‖) (S : CompactPacket O) :
    packetSpace S →ₗᵢ[ℝ] packetSpace (movePacket T hT S) where
  toLinearMap := (T.toLinearMap.comp (packetSpace S).subtype).codRestrict _ (by
    intro x
    rw [← packetSpace_move T hT S]
    exact Submodule.mem_map.mpr ⟨x.val, x.property, rfl⟩)
  norm_map' x := hn x.val

theorem packetMove_intertwines {O P : Set Spacetime} (T : H1 →L[ℝ] H1)
    (hT : ∀ v ∈ compactSupportedGenerators O, T v ∈ compactSupportedGenerators P)
    (hn : ∀ v : H1, ‖T v‖ = ‖v‖) (S : CompactPacket O) (x : packetSpace S) :
    ((packetMoveIsometry T hT hn S x : packetSpace (movePacket T hT S)) : H1) = T x := rfl

theorem movePacket_mono {O P : Set Spacetime} (T : H1 →L[ℝ] H1)
    (hT : ∀ v ∈ compactSupportedGenerators O, T v ∈ compactSupportedGenerators P)
    {S R : CompactPacket O} (h : S.val ⊆ R.val) :
    (movePacket T hT S).val ⊆ (movePacket T hT R).val := by
  classical
  exact Finset.image_subset_image h

theorem packetMove_refinement {O P : Set Spacetime} (T : H1 →L[ℝ] H1)
    (hT : ∀ v ∈ compactSupportedGenerators O, T v ∈ compactSupportedGenerators P)
    (hn : ∀ v : H1, ‖T v‖ = ‖v‖) {S R : CompactPacket O}
    (h : S.val ⊆ R.val) (x : packetSpace S) :
    packetInclusion (movePacket_mono T hT h) (packetMoveIsometry T hT hn S x) =
      packetMoveIsometry T hT hn R (packetInclusion h x) := rfl

def packetTranslation (a : Spacetime) : H1 →L[ℝ] H1 :=
  (U1 (fun i => a i)).toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ

def translatePacket (a : Spacetime) {O : Set Spacetime} (S : CompactPacket O) :
    CompactPacket (translateRegion a O) :=
  movePacket (packetTranslation a) (compact_translated_generator a O) S

theorem packet_translate (a : Spacetime) {O : Set Spacetime} (S : CompactPacket O) :
    (packetSpace S).map (packetTranslation a).toLinearMap = packetSpace (translatePacket a S) :=
  packetSpace_move _ _ S

def translatePacketIsometry (a : Spacetime) {O : Set Spacetime} (S : CompactPacket O) :
    packetSpace S →ₗᵢ[ℝ] packetSpace (translatePacket a S) :=
  packetMoveIsometry (packetTranslation a) (compact_translated_generator a O)
    (fun v => (U1 (fun i => a i)).norm_map v) S

def packetLorentz (L : generatedLorentz) : H1 →L[ℝ] H1 :=
  (helicityUnitary L).toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ

def lorentzPacket (L : generatedLorentz) {O : Set Spacetime} (S : CompactPacket O) :
    CompactPacket (lorentzRegion L O) :=
  movePacket (packetLorentz L) (compact_lorentz_generator L O) S

theorem packet_lorentz (L : generatedLorentz) {O : Set Spacetime} (S : CompactPacket O) :
    (packetSpace S).map (packetLorentz L).toLinearMap = packetSpace (lorentzPacket L S) :=
  packetSpace_move _ _ S

def lorentzPacketIsometry (L : generatedLorentz) {O : Set Spacetime} (S : CompactPacket O) :
    packetSpace S →ₗᵢ[ℝ] packetSpace (lorentzPacket L S) :=
  packetMoveIsometry (packetLorentz L) (compact_lorentz_generator L O)
    (fun v => (helicityUnitary L).norm_map v) S

theorem packet_boost_apply (s : ℝ) (v : H1) : packetLorentz (generatedBoost s) v = B0 s v :=
  helicityUnitary_boost s v

theorem packet_future_lorentz (L : FutureLorentz) {O : Set Spacetime}
    (S : CompactPacket O) :
    (packetSpace S).map (packetLorentz (futureToGenerated L)).toLinearMap =
      packetSpace (lorentzPacket (futureToGenerated L) S) := packet_lorentz _ _

#print axioms packetSpace_finite
#print axioms packetSpace_directed
#print axioms packetInclusion
#print axioms packetInclusion_comp
#print axioms packetSpace_le_localized
#print axioms packetSpace_enlarge
#print axioms packetSpace_iSup
#print axioms packet_union_closure
#print axioms packet_wedge_complex_dense
#print axioms packetSpace_move
#print axioms packetMoveIsometry
#print axioms packetMove_intertwines
#print axioms movePacket_mono
#print axioms packetMove_refinement
#print axioms packet_translate
#print axioms translatePacketIsometry
#print axioms packet_lorentz
#print axioms lorentzPacketIsometry
#print axioms packet_boost_apply
#print axioms packet_future_lorentz
end F1Fecho.DeviceContinuumR57
