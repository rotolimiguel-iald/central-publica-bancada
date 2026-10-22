import PhysicalCompactNetGeometryR1
import PhysicalCompactNetLocalityR2
import PhysicalCompactWedgeComparisonR1
import PhysicalCanonicalWedgeEqualityR3
import CanonicalFockAssemblyR1

/-! A concrete global Maxwell LightNetData and its exact nonzero canonical
wedge on the SAME H1. The compact-test net is compared to the prior physical
Schwartz wedge by a theorem, never by renaming. Other Fock, trace and Maxwell
charge certificates are separate obligations and are not fabricated here. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal TGLExt.ImportedSQ TGL.SpecificAQFT
open F1Fecho.NetworkReuse F1Rede.CanonicalWedge

theorem compactPhysicalNet_local (O P : Set (Fin 4 → ℝ)) (hsep : SpacelikeSep O P) :
    ∀ f ∈ compactPhysicalNet O, ∀ g ∈ compactPhysicalNet P, (inner ℂ f g).im=0 := by
  intro f hf g hg
  exact compactLocalized_locality (coordinateRegion O) (coordinateRegion P)
    (fun x hx y hy => hsep (fun i => x i) hx (fun i => y i) hy) f g hf hg

theorem compactPhysicalNet_wedge_glue :
    compactPhysicalNet rightWedge=KWR.toClosedSubmodule.toSubmodule :=
  compactPhysicalNet_rightWedge.trans
    (compactLocalized_rightWedge_eq.trans physical_right_wedge_eq_KWR)

def physicalCanonicalNet : CanonicalNetInput where
  toLightNetData :=
    { helicity := 1
      helicity_light := Or.inl rfl
      K := compactPhysicalNet
      K_mono := compactPhysicalNet_mono
      K_local := compactPhysicalNet_local
      K_translate := compactPhysicalNet_translate
      K_boost := compactPhysicalNet_boost }
  wedge_glue := compactPhysicalNet_wedge_glue

theorem physical_light_net_inhabited : Nonempty TGLExt.QGSolution.LightNetData :=
  ⟨physicalCanonicalNet.toLightNetData⟩

theorem physical_canonical_net_nonzero :
    ∃ v : H1, v ∈ physicalCanonicalNet.K rightWedge ∧ v≠0 :=
  canonical_wedge_nonzero physicalCanonicalNet

theorem physical_canonical_net_zero_refused : physicalCanonicalNet.K rightWedge≠⊥ :=
  zero_wedge_refused physicalCanonicalNet

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.compactPhysicalNet_local
#print axioms F1Fecho.MaxwellLocalization.compactPhysicalNet_wedge_glue
#print axioms F1Fecho.MaxwellLocalization.physicalCanonicalNet
#print axioms F1Fecho.MaxwellLocalization.physical_light_net_inhabited
#print axioms F1Fecho.MaxwellLocalization.physical_canonical_net_nonzero
#print axioms F1Fecho.MaxwellLocalization.physical_canonical_net_zero_refused
