import PhotonContractTheorems_v2

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open ORDEM016.Photon.SpecificAQFT ORDEM016.Photon.ModularRealization
open ORDEM016.Photon.Contract
namespace ORDEM016.D5

def dilation (r : ℝ) (x : Fin 4 → ℝ) : Fin 4 → ℝ := r • x

theorem dilation_boost_commutes (r s : ℝ) (x : Fin 4 → ℝ) :
    dilation r (wedgeBoostMap s x)=wedgeBoostMap s (dilation r x) :=
  (wedgeBoostMap_smul s r x).symm

theorem dilation_wedge_iff (r : ℝ) (hr : 0<r) (x : Fin 4 → ℝ) :
    dilation r x ∈ rightWedge ↔ x ∈ rightWedge := by
  change |r*x 0|<r*x 1 ↔ |x 0|<x 1
  rw [abs_mul,abs_of_pos hr]
  exact mul_lt_mul_left hr

theorem dilation_wedge_image (r : ℝ) (hr : 0<r) : dilation r '' rightWedge=rightWedge := by
  ext x
  constructor
  · rintro ⟨y,hy,rfl⟩
    exact (dilation_wedge_iff r hr y).mpr hy
  · intro hx
    refine ⟨dilation r⁻¹ x,(dilation_wedge_iff r⁻¹ (inv_pos.mpr hr) x).mpr hx,?_⟩
    simp [dilation,smul_smul,hr.ne']

def scaledNormalization (N : KillingNormalization) (r : ℝ) (hr : 0<r) :
    KillingNormalization where
  point := dilation r N.point
  point_in_wedge := (dilation_wedge_iff r hr N.point).mpr N.point_in_wedge

theorem normalization_radius_scales (N : KillingNormalization) (r : ℝ) (hr : 0<r) :
    ContratoH2.refRadius (scaledNormalization N r hr)=r*ContratoH2.refRadius N := by
  change Real.sqrt ((r*N.point 1)^2-(r*N.point 0)^2)=r*Real.sqrt (N.point 1^2-N.point 0^2)
  have he : (r*N.point 1)^2-(r*N.point 0)^2=r^2*(N.point 1^2-N.point 0^2) := by ring
  rw [he,Real.sqrt_mul (sq_nonneg r),Real.sqrt_sq_eq_abs,abs_of_pos hr]

theorem normalized_kappa_scales {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    (N : KillingNormalization) (r : ℝ) (hr : 0<r)
    (C : ContratoH2 W R N) (C' : ContratoH2 W R (scaledNormalization N r hr)) :
    C'.kappa=C.kappa/r := by
  rw [C'.kappa_eq_inv_radius,C.kappa_eq_inv_radius,normalization_radius_scales]
  simp [div_div,mul_comm]

#print axioms dilation_boost_commutes
#print axioms dilation_wedge_iff
#print axioms dilation_wedge_image
#print axioms normalization_radius_scales
#print axioms normalized_kappa_scales
end ORDEM016.D5
