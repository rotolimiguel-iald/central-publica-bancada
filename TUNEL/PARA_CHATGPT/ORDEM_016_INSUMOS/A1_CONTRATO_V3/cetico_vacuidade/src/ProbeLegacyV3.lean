import ContratoQG_v3
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option maxHeartbeats 2000000

/-!
# ProbeLegacyV3 — O PAR LEGADO (U = 1) CONTRA A v3   [DIAGNÓSTICO; DEVE FALHAR; nunca importado]
  Frente contrato_v3, 23/09/2026.

  (theSpecificAQFTWitness, regularModularRealization): U = 1, fluxo = torre. Tenta-se o habitante v3
  COMPLETO. PROVADOS de verdade: κ, (Δ) rfl, (S) grupo de boosts V(s) = Δ^{−is/2π} + `bw`, continuidade
  e ENERGIA POSITIVA (U = 1 ⟹ correlação constante), observador, frame `geoFrame`. CONCEDIDO: `kms`
  ([KNOWN] para a torre). TÊM de falhar: `translations_faithful`, `null_ergodic`.
  Resultado esperado na linha de base (conjunto de campos que falham): {translations_faithful, null_ergodic}.
  Refutações em kernel: `contratoH2_empty_on_legacy`, `legacy_not_null_ergodic` (Teoremas/Paredes).
-/

namespace TGLExt.ContratoQGv3.ProbeLegacy

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion ChatgptAudit
open TGLExt.ContratoQGv3 W5Final.Toy
open scoped InnerProductSpace

noncomputable section

def towerV (s : ℝ) : WH ≃ₗᵢ[ℂ] WH := u (-(s / (2 * Real.pi)))

theorem two_pi_rescale (s : ℝ) : -(2 * Real.pi * (-(s / (2 * Real.pi)))) = s := by
  have : (2 * Real.pi) ≠ 0 := by positivity
  field_simp

def legacyBoostP : WedgeBoostRep theSpecificAQFTWitness where
  V := towerV
  V_zero := by
    first
    | (ext v
       change modularFlow mixProfile (-((0:ℝ) / (2 * Real.pi))) v = v
       simpa using modularFlow_zero_time (P := mixProfile) v)
    | trivial
  V_add := by
    first
    | (intro a b
       ext v
       change modularFlow mixProfile (-((a + b) / (2 * Real.pi))) v
         = modularFlow mixProfile (-(a / (2 * Real.pi))) (modularFlow mixProfile (-(b / (2 * Real.pi))) v)
       rw [modularFlow_group]
       congr 1
       ring)
    | trivial
  V_continuous := by
    first
    | (intro ψ
       have h : Continuous (fun s : ℝ => -(s / (2 * Real.pi))) := by fun_prop
       exact (modularFlow_strongly_continuous (P := mixProfile) ψ).comp h)
    | trivial
  V_vac := by
    first
    | (intro s; exact modularFlow_fixes_omega _)
    | trivial
  V_translations := by
    first
    | (intro s a
       rw [TGLExt.ContratoQG.legacy_translations_trivial, TGLExt.ContratoQG.legacy_translations_trivial]
       exact map_one _)
    | trivial
  V_net := by
    first
    | (intro s O T hT
       have h := legacy_bw_covariance (-(s / (2 * Real.pi))) O T hT
       rw [two_pi_rescale] at h
       exact h)
    | trivial

/-- DEVE FALHAR — e o conjunto dos campos que falham É o resultado. -/
def probeLegacy (hkms : KMSAt theSpecificAQFTWitness (fun t => modularFlowUnitary mixProfile (-t)) 1) :
    ContratoH2 theSpecificAQFTWitness regularModularRealization where
  kappa := 1
  kappa_pos := by first | exact one_pos | trivial
  Δit := modularFlowUnitary mixProfile
  flow_implemented := by first | exact (fun _ _ => rfl) | trivial
  kms := by first | exact hkms | trivial
  boost := legacyBoostP
  bw := by
    first
    | (intro t
       ext v
       change modularFlow mixProfile t v
         = modularFlow mixProfile (-((-(2 * Real.pi * t)) / (2 * Real.pi))) v
       congr 1
       have : (2 * Real.pi) ≠ 0 := by positivity
       field_simp)
    | trivial
  translations_continuous := by
    first
    | (intro ψ
       have : (fun a : Fin 4 → ℝ => theSpecificAQFTWitness.U a ψ) = fun _ => ψ := by
         funext a; rw [TGLExt.ContratoQG.legacy_translations_trivial]; rfl
       rw [this]; exact continuous_const)
    | trivial
  translations_faithful := by
    first
    | (intro a ha
       funext i
       have := congrArg (fun T : WH →L[ℂ] WH => T (hOmega mixProfile)) ha
       simp at this
       exact this)
    | trivial
  positive_energy := by
    first
    | (intro a ha ψ
       refine ⟨fun _ => ⟪ψ, ψ⟫_ℂ, diffContOnCl_const, ⟨‖⟪ψ, ψ⟫_ℂ‖, fun z _ => le_refl _⟩, ?_⟩
       intro t
       rw [TGLExt.ContratoQG.legacy_translations_trivial]
       rfl)
    | trivial
  null_ergodic := by
    first
    | (intro ψ hψ
       exact Submodule.subset_span (Set.mem_singleton_iff.mpr (by simpa using hψ 0)))
    | trivial
  observer := ![0, 1, 0, 0]
  observer_in_wedge := by
    first
    | (show |(![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
       simp)
    | trivial
  observer_unit := by first | (simp [minkowskiSq, killingField]) | trivial
  E := geoFrame
  smooth_on := by first | exact geoFrame_smooth | trivial
  det_unit_on := by first | exact geoFrame_det_unit_on | trivial
  dragged := by first | exact geoFrame_dragged | trivial
  fiducial_is_modular := by first | exact geoFrame_fiducial | trivial

#print axioms two_pi_rescale
#print axioms legacyBoostP

end

end TGLExt.ContratoQGv3.ProbeLegacy
