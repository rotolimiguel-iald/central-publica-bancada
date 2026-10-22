import TensorNoFixedR1
import BosonicFock
import CanonicalWedge
import Mathlib.Analysis.Normed.Module.FiniteDimension

/-! The general no-projective-eigenvector hypothesis is propagated through
the actual completed symmetric tensor sectors. Only the vacuum can remain. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open UniformSpace
open scoped TensorProduct
namespace F1Fecho.CanonicalGammaNoFixed
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock
open F1Rede.CanonicalWedge F1Rede.SectorDirectSum

theorem zero_sector_span (x : Sector 0) : ∃ c : ℂ, c • vacuumSector = x := by
  have hs : ∀ z : Completion ℂ, z ∈ (ℂ ∙ ((1 : ℂ) : Completion ℂ)) := by
    intro z
    refine Completion.induction_on z
      (ℂ ∙ ((1 : ℂ) : Completion ℂ)).closed_of_finiteDimensional ?_
    intro c
    apply Submodule.mem_span_singleton.mpr
    refine ⟨c,?_⟩
    rw [← Completion.coe_smul]
    simp
  obtain ⟨c,hc⟩ := Submodule.mem_span_singleton.mp (hs (x : TensorHilbert 0))
  refine ⟨c,Subtype.ext ?_⟩
  exact hc

theorem positive_sector_fixed_zero
    (u : ℝ → H1 ≃ₗᵢ[ℂ] H1) (h0 : u 0 = LinearIsometryEquiv.refl ℂ H1)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s))
    (hno : ∀ f : H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u l f = c • f) → f = 0)
    (n : ℕ) (x : Sector (n+1)) (hx : ∀ l, gammaSector (u l) (n+1) x = x) : x = 0 := by
  apply Subtype.ext
  apply F1Fecho.TensorNoFixed.tensor_fixed_eq_zero Jcandidate u h0 hadd hno
    (fun l => algebraicGamma (u l) n) (x : TensorHilbert (n+1))
  intro l
  exact congrArg Subtype.val (hx l)

theorem gamma_no_fixed
    (u : ℝ → H1 ≃ₗᵢ[ℂ] H1) (h0 : u 0 = LinearIsometryEquiv.refl ℂ H1)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s))
    (_hcontinuous : ∀ ξ, Continuous (fun s => u s ξ))
    (hno : ∀ f : H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u l f = c • f) → f = 0)
    (ψ : F) (hψ : ∀ l, gamma (u l) ψ = ψ) : ψ ∈ (ℂ ∙ vacuum) := by
  have hpos (n : ℕ) : ψ (n+1) = 0 := by
    apply positive_sector_fixed_zero u h0 hadd hno n
    intro l
    exact congrArg (fun q : F => q (n+1)) (hψ l)
  obtain ⟨c,hc⟩ := zero_sector_span (ψ 0)
  apply Submodule.mem_span_singleton.mpr
  refine ⟨c,?_⟩
  apply lp.ext
  intro n
  cases n with
  | zero => simpa only [vacuum,sectorEmbedding_apply,lp.single_apply,lp.coe_smul,Pi.smul_apply] using hc
  | succ n =>
    rw [hpos n]
    simp [vacuum,sectorEmbedding_apply,lp.single_apply_ne]

end F1Fecho.CanonicalGammaNoFixed
#print axioms F1Fecho.CanonicalGammaNoFixed.zero_sector_span
#print axioms F1Fecho.CanonicalGammaNoFixed.positive_sector_fixed_zero
#print axioms F1Fecho.CanonicalGammaNoFixed.gamma_no_fixed
