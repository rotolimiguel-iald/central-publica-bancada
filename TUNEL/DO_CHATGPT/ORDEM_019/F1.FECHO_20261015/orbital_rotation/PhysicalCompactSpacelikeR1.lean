import PhysicalSymplecticPairingR1
import PhysicalFrameWedgeLocalityR2

/-! Causal commutation of actual compact Maxwell tests with strictly spacelike
topological supports. The finite cover is constructed from opposite physical
wedges; no global locality premise is used. Extension to the entire region
net remains a separate theorem. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen F1Fecho.SpacetimeLorentz
open TGL.SpecificAQFT F1Fecho.SpacelikeGeometry TGLExt.ImportedSQ

theorem physicalFrameRight_open (L : generatedLorentz) (a : Spacetime) :
    IsOpen (physicalFrameRegion L a physicalRightWedge) := by
  change IsOpen {x : Spacetime | |action L.val (x-a) 0| < action L.val (x-a) 1}
  exact isOpen_lt (by fun_prop) (by fun_prop)

theorem physicalFrameLeft_open (L : generatedLorentz) (a : Spacetime) :
    IsOpen (physicalFrameRegion L a physicalLeftWedge) := by
  change IsOpen {x : Spacetime | |action L.val (x-a) 0| < -action L.val (x-a) 1}
  exact isOpen_lt (by fun_prop) (by fun_prop)

theorem physical_frame_test_pair_zero (L : generatedLorentz) (a : Spacetime) :
    TestPairZero physicalTestPairing (physicalFrameRegion L a physicalRightWedge)
      (physicalFrameRegion L a physicalLeftWedge) := by
  intro f g hfr hgr hfs hgs
  exact physical_frame_opposite_symplectic L a (circularSmear f) (circularSmear g)
    ((Submodule.le_topologicalClosure _) (Submodule.subset_span ⟨f,hfr,hfs,rfl⟩))
    ((Submodule.le_topologicalClosure _) (Submodule.subset_span ⟨g,hgr,hgs,rfl⟩))

theorem physical_compact_spacelike_zero (f g : SchwartzTensor)
    (hfr : IsRealTest f) (hgr : IsRealTest g)
    (hfc : HasCompactSupport (f : Spacetime → TensorValue))
    (hgc : HasCompactSupport (g : Spacetime → TensorValue))
    (hsep : ∀ x ∈ tsupport (f : Spacetime → TensorValue),
      ∀ y ∈ tsupport (g : Spacetime → TensorValue),
      minkowskiSq (fun i => x i-y i) < 0) :
    (inner ℂ (circularSmear f) (circularSmear g)).im = 0 := by
  apply compact_pair_zero physicalTestPairing f g hfr hgr hfc hgc
  intro x y
  obtain ⟨L,m,hx,hy⟩ := spacelike_pair_opposite_wedges
    (fun i => x.val i) (fun i => y.val i) (hsep x.val x.property y.val y.property)
  let a : Spacetime := coordinateEquiv.symm m
  refine ⟨physicalFrameRegion L a physicalRightWedge,
    physicalFrameRegion L a physicalLeftWedge,physicalFrameRight_open L a,
    physicalFrameLeft_open L a,?_,?_,physical_frame_test_pair_zero L a⟩
  · exact hx
  · exact hy

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.physical_compact_spacelike_zero
