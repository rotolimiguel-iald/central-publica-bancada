import ContratoQG_v31
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option maxHeartbeats 2000000

/-!
# ProbeToyV31 — O BRINQUEDO DE W5 CONTRA A v3.1   [DIAGNÓSTICO; DEVE FALHAR; nunca importado pelo kernel]
  Frente contrato_v3, RODADA 2, 23/09/2026. Porte da ProbeToyV3 (e2aacdf9dd51327c): muda só o índice N (o relógio
  N₁ = (0,1,0,0), κ = 1) no lugar do observador.

  O brinquedo (W5_final): U(a) := Δ^{i a₂} (o fluxo da torre), rede/Hilbert/vácuo do par legado, frame
  `geoFrame` escrito à mão. HABITA a v2 (rc=0, medido). Aqui tenta-se o habitante v3 COMPLETO:

  * PROVADOS de verdade (cada um com `first | exact <prova> | trivial`, para que afrouxar o campo a True
    não CRIE erro — só pode REMOVER): κ, (Δ) `flow_implemented` (rfl), (S) o grupo de boosts
    V(s) = Δ^{−is/2π} com TODOS os seus campos, `bw`, continuidade das translações, o observador (κ = 1,
    x = (0,1,0,0)), o frame (C)(D)(E).
  * CONCEDIDO como hipótese: `kms` (Δ^{it} da torre É o grupo modular do vácuo da torre — [KNOWN], não
    formalizado aqui). Não se concede nada falso.
  * TENTADOS e que TÊM de falhar (o bloco (P)): `translations_faithful`, `positive_energy`, `null_ergodic`.

  O RESULTADO deste probe é o CONJUNTO de campos que falham (lido do log por linha). Esperado na linha de
  base: {translations_faithful, positive_energy, null_ergodic}. Sob a mutação «campo := True» de um deles,
  esse campo SAI do conjunto — o probe deixa de ter rc constante (resposta ao cético D-A).
  Refutações em kernel (não só «não achei prova»): `toy_not_v3_by_fidelity`, `toy_not_null_ergodic`
  (ContratoQG_v3_Paredes.lean). `positive_energy` no brinquedo: falha por falta de prova; a refutação
  (o gerador da torre tem os dois sinais) NÃO está formalizada.
-/

namespace TGLExt.ContratoQGv31.ProbeToy

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion ChatgptAudit
open TGLExt.ContratoQGv31 W5Final.Toy
open scoped InnerProductSpace

noncomputable section

def towerV (s : ℝ) : WH ≃ₗᵢ[ℂ] WH := u (-(s / (2 * Real.pi)))

theorem two_pi_rescale (s : ℝ) : -(2 * Real.pi * (-(s / (2 * Real.pi)))) = s := by
  have : (2 * Real.pi) ≠ 0 := by positivity
  field_simp

def toyBoostP : WedgeBoostRep toyW where
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
       have h := toy_poincare_relation (-(s / (2 * Real.pi))) a
       rw [two_pi_rescale] at h
       exact h)
    | trivial
  V_net := by
    first
    | (intro s O T hT
       have h := toy_bw_covariance (-(s / (2 * Real.pi))) O T hT
       rw [two_pi_rescale] at h
       exact h)
    | trivial

/-- o relógio de referência dos probes: o ponto (0,1,0,0) (raio de Rindler 1, κ = 1). -/
def N₁ : KillingNormalization where
  point := ![0, 1, 0, 0]
  point_in_wedge := by
    show |(![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp

/-- DEVE FALHAR — e o conjunto dos campos que falham É o resultado. -/
def probeToy (hkms : KMSAt toyW (fun t => u (-t)) 1) : ContratoH2 toyW toyR N₁ where
  kappa := 1
  kappa_pos := by first | exact one_pos | trivial
  Δit := u
  flow_implemented := by first | exact (fun _ _ => rfl) | trivial
  kms := by first | exact hkms | trivial
  boost := toyBoostP
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
       exact (modularFlow_strongly_continuous (P := mixProfile) ψ).comp (continuous_apply 2))
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
       simp)
    | trivial
  null_ergodic := by
    first
    | (intro ψ hψ
       exact Submodule.subset_span (Set.mem_singleton_iff.mpr (by simpa using hψ 0)))
    | trivial
  observer_unit := by first | (simp [N₁, minkowskiSq, killingField]) | trivial
  E := geoFrame
  smooth_on := by first | exact geoFrame_smooth | trivial
  det_unit_on := by first | exact geoFrame_det_unit_on | trivial
  dragged := by first | exact geoFrame_dragged | trivial
  fiducial_is_modular := by first | exact geoFrame_fiducial | trivial

#print axioms two_pi_rescale
#print axioms toyBoostP

end

end TGLExt.ContratoQGv31.ProbeToy
