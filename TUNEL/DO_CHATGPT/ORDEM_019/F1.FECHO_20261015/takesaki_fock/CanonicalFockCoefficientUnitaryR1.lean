import CanonicalFockSpectralGNSR4
import CanonicalFockCoefficientDenseR5
/-! The same normalized Fourier coefficient isometry onto the actual GNS.
Both image inclusions are imported from their proved consumers. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientGNS
open TGLV350.Regular F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.RegularNormalizedFourier F1Fecho.CanonicalFockSpectralGNS
theorem GNS_eq_spectralCode_range :
    (GNSSubspace : Set (RegularHilbert (RegularHilbert F)))=Set.range (spectralCode (H:=F)) := by
  apply Set.Subset.antisymm GNS_subset_spectralCode
  rintro _ ⟨f,rfl⟩
  exact spectralCode_mem_GNS f

def coefficientToGNS : RegularHilbert F →ₗᵢ[ℂ] GNSHilbert where
  toFun f := ⟨spectralCode f,spectralCode_mem_GNS f⟩
  map_add' f g := Subtype.ext (spectralCode.map_add f g)
  map_smul' c f := Subtype.ext (spectralCode.map_smul c f)
  norm_map' f := spectralCode.norm_map f

theorem coefficientToGNS_surjective : Function.Surjective coefficientToGNS := by
  intro x
  obtain ⟨f,hf⟩ := GNS_subset_spectralCode x.property
  exact ⟨f,Subtype.ext hf⟩

def coefficientUnitary : RegularHilbert F ≃ₗᵢ[ℂ] GNSHilbert :=
  LinearIsometryEquiv.ofSurjective coefficientToGNS coefficientToGNS_surjective

theorem coefficientUnitary_coe (f : RegularHilbert F) :
    (coefficientUnitary f).val=spectralCode f := rfl

end F1Fecho.CanonicalFockCoefficientGNS
#print axioms F1Fecho.CanonicalFockCoefficientGNS.GNS_eq_spectralCode_range
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientToGNS_surjective
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientUnitary_coe
