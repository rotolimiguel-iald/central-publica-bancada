import PhysicalCompactNetCovarianceR1
import PhysicalCompactSpacelikeR6
import GenericSymplecticSpanR2

/-! Causal locality for the compact-test net on the same physical Maxwell H1.
All pairs of points in the two regions are strictly spacelike. The previous
all-Schwartz net is not identified with this net by definition. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal TGLExt.ImportedSQ TGL.SpecificAQFT

theorem compactLocalized_locality (O P : Set Spacetime)
    (hsep : ∀ x ∈ O, ∀ y ∈ P, minkowskiSq (fun i => x i-y i)<0)
    (u v : H1) (hu : u ∈ compactLocalized O) (hv : v ∈ compactLocalized P) :
    (inner ℂ u v).im=0 := by
  apply GenericSymplecticSpan.closed_spans_zero
    (compactSupportedGenerators O) (compactSupportedGenerators P) ?_ u v hu hv
  rintro x ⟨f,hfr,hfc,hfs,rfl⟩ y ⟨g,hgr,hgc,hgs,rfl⟩
  exact physical_compact_spacelike_zero f g hfr hgr hfc hgc
    (fun x hx y hy => hsep x (hfs hx) y (hgs hy))

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_locality
