import TGLExt.ModularFlowSpectrum
import TGLExt.TheImportedSecondQuantization

/-
R57: obstruction to reusing the existing product-tower modular flow as
the canonical one-particle boost. This is NOT a no-go theorem for other
cell dynamics, scaling limits, or the Fock representation.
-/
set_option autoImplicit false
set_option maxHeartbeats 400000

noncomputable section
namespace F1Fecho.DeviceContinuumR57
open TGLExt ChatgptAudit TGLExt.ImportedSQ

/-- Even an arbitrary reparametrization cannot turn this pure-point flow
into a nonzero bounded intertwiner with the continuous orbital boost. -/
def TowerBoostIntertwines (P : SiteProfile) (clock : ℝ → ℝ)
    (V : TowerHilbert P →L[ℂ] H1) : Prop :=
  ∀ (s : ℝ) (x : TowerHilbert P),
    V (modularFlow P (clock s) x) = B0 s (V x)

theorem intertwiner_kills_localEigenvector (P : SiteProfile) (clock : ℝ → ℝ)
    (V : TowerHilbert P →L[ℂ] H1) (hV : TowerBoostIntertwines P clock V)
    (N : ℕ) (i j : chainIdx N) :
    V (localEigenvector P N i j) = 0 := by
  apply B0_no_eigen
  intro s
  refine ⟨modularPhase (clock s) (Real.log (localEigenvalue P N i j)),
    modularPhase_norm _ _, ?_⟩
  rw [← hV s, modularFlow_eigenvector, map_smul]

theorem towerBoost_intertwiner_eq_zero (P : SiteProfile) (clock : ℝ → ℝ)
    (V : TowerHilbert P →L[ℂ] H1) (hV : TowerBoostIntertwines P clock V) :
    V = 0 := by
  have hs : ∀ x ∈ Submodule.span ℂ (localEigenvectors P), V x = 0 := by
    intro x hx
    induction hx using Submodule.span_induction with
    | mem x hx =>
      obtain ⟨N, i, j, rfl⟩ := hx
      exact intertwiner_kills_localEigenvector P clock V hV N i j
    | zero => exact map_zero V
    | add x y hx hy hxe hye => simp only [map_add, hxe, hye, add_zero]
    | smul c x hx hxe => simp only [map_smul, hxe, smul_zero]
  have hc : IsClosed {x : TowerHilbert P | V x = 0} :=
    isClosed_eq V.continuous continuous_const
  ext x
  exact closure_minimal hs hc (localEigenvectors_total (P := P) x)

theorem no_towerBoost_isometric_intertwiner (P : SiteProfile) (clock : ℝ → ℝ) :
    ¬ ∃ V : TowerHilbert P →ₗᵢ[ℂ] H1,
      TowerBoostIntertwines P clock V.toContinuousLinearMap := by
  rintro ⟨V, hV⟩
  have hz := towerBoost_intertwiner_eq_zero P clock V.toContinuousLinearMap hV
  have ho : V (hOmega P) = 0 := by
    exact congrArg (fun T : TowerHilbert P →L[ℂ] H1 => T (hOmega P)) hz
  have hn : ‖V (hOmega P)‖ = 1 := (V.norm_map _).trans (hOmega_norm (P := P))
  rw [ho, norm_zero] at hn
  exact zero_ne_one hn

#print axioms intertwiner_kills_localEigenvector
#print axioms towerBoost_intertwiner_eq_zero
#print axioms no_towerBoost_isometric_intertwiner
end F1Fecho.DeviceContinuumR57
