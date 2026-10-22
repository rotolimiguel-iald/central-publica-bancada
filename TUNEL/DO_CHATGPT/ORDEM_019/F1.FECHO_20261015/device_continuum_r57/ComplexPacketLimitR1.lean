import CompactPacketRefinementR1

/- Concrete complex finite-dimensional target family, dense in the SAME H1.
The real packet subspaces still recover local real localization; this file
complexifies the finite packets only for the global one-particle limit.
No physical device identification is postulated. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.DeviceContinuumR57
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.MaxwellLocalization
open F1Fecho.OrbitalScreen F1Fecho.OrbitalSpatial

def complexPacketSpace {O : Set Spacetime} (S : CompactPacket O) : Submodule ℂ H1 :=
  Submodule.span ℂ (S.val : Set H1)

instance complexPacketSpace_finite {O : Set Spacetime} (S : CompactPacket O) :
    FiniteDimensional ℂ (complexPacketSpace S) :=
  FiniteDimensional.span_finset ℂ S.val

theorem complexPacketSpace_mono {O : Set Spacetime} {S T : CompactPacket O}
    (h : S.val ⊆ T.val) : complexPacketSpace S ≤ complexPacketSpace T :=
  Submodule.span_mono h

theorem complexPacketSpace_directed (O : Set Spacetime) :
    Directed (· ≤ ·) (@complexPacketSpace O) := by
  classical
  intro S T
  exact ⟨joinPacket S T, complexPacketSpace_mono Finset.subset_union_left,
    complexPacketSpace_mono Finset.subset_union_right⟩

def complexPacketInclusion {O : Set Spacetime} {S T : CompactPacket O}
    (h : S.val ⊆ T.val) : complexPacketSpace S →ₗᵢ[ℂ] complexPacketSpace T where
  toLinearMap := Submodule.inclusion (complexPacketSpace_mono h)
  norm_map' _ := rfl

theorem complexPacketInclusion_comp {O : Set Spacetime} {R S T : CompactPacket O}
    (hRS : R.val ⊆ S.val) (hST : S.val ⊆ T.val) (x : complexPacketSpace R) :
    complexPacketInclusion hST (complexPacketInclusion hRS x) =
      complexPacketInclusion (hRS.trans hST) x := rfl

theorem complexPacketSpace_iSup (O : Set Spacetime) :
    (⨆ S : CompactPacket O, complexPacketSpace S) =
      Submodule.span ℂ (compactSupportedGenerators O) := by
  classical
  apply le_antisymm
  · exact iSup_le (fun S => Submodule.span_mono S.property)
  · apply Submodule.span_le.mpr
    intro v hv
    let S : CompactPacket O := ⟨{v}, by simpa using hv⟩
    exact (le_iSup (fun S : CompactPacket O => complexPacketSpace S) S)
      (Submodule.subset_span (by simp [S]))

theorem compact_wedge_generators_complex_dense :
    (Submodule.span ℂ (compactSupportedGenerators physicalRightWedge)).topologicalClosure = ⊤ := by
  let K := (Submodule.span ℂ (compactSupportedGenerators physicalRightWedge)).topologicalClosure
  have hc : IsClosed (K : Set H1) := Submodule.isClosed_topologicalClosure _
  have hr : Submodule.span ℝ (compactSupportedGenerators physicalRightWedge) ≤
      K.restrictScalars ℝ := by
    apply Submodule.span_le.mpr
    intro v hv
    exact (Submodule.le_topologicalClosure _) (Submodule.subset_span hv)
  have hw : compactLocalized physicalRightWedge ≤ K.restrictScalars ℝ :=
    Submodule.topologicalClosure_minimal _ hr hc
  have hs : Submodule.span ℂ (compactLocalized physicalRightWedge : Set H1) ≤ K :=
    Submodule.span_le.mpr hw
  have ht := Submodule.topologicalClosure_minimal _ hs hc
  rw [compactLocalized_rightWedge_eq, physical_right_wedge_complex_dense] at ht
  exact le_antisymm le_top ht

theorem complexPacket_union_dense :
    Dense (⋃ S : CompactPacket physicalRightWedge, (complexPacketSpace S : Set H1)) := by
  apply dense_iff_closure_eq.mpr
  rw [← Submodule.coe_iSup_of_directed _ (complexPacketSpace_directed _), complexPacketSpace_iSup]
  change ((Submodule.span ℂ (compactSupportedGenerators physicalRightWedge)).topologicalClosure :
    Set H1) = Set.univ
  rw [compact_wedge_generators_complex_dense]
  rfl

theorem complexPacketSpace_move {O P : Set Spacetime} (T : H1 →L[ℂ] H1)
    (hT : ∀ v ∈ compactSupportedGenerators O, T v ∈ compactSupportedGenerators P)
    (S : CompactPacket O) :
    (complexPacketSpace S).map T.toLinearMap =
      complexPacketSpace (movePacket (T.restrictScalars ℝ) hT S) := by
  classical
  rw [complexPacketSpace, Submodule.map_span]
  congr 1
  ext v
  simp [movePacket, complexPacketSpace]

#print axioms complexPacketSpace_finite
#print axioms complexPacketSpace_directed
#print axioms complexPacketInclusion
#print axioms complexPacketInclusion_comp
#print axioms complexPacketSpace_iSup
#print axioms compact_wedge_generators_complex_dense
#print axioms complexPacket_union_dense
#print axioms complexPacketSpace_move
end F1Fecho.DeviceContinuumR57
