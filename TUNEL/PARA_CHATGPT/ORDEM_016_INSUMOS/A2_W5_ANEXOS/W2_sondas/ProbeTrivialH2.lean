import ContratoQG
-- NA TRANSPOSIÇÃO (TGLExt/ProbeTrivialH2.lean): `import TGLExt.ContratoQG`. Única mudança.

set_option autoImplicit false

/-!
# ProbeTrivialH2 -- CONTROLE NEGATIVO   [DIAGNÓSTICO; NUNCA importado por TGL.lean / TGLExt.lean]
  Frente W2_final, 23/09/2026 (2ª versão: contrato parametrizado por (W, R)).

Tenta habitar `ContratoH2 theSpecificAQFTWitness regularModularRealization` (o PAR LEGADO, U = 1) com o
habitante GENÉRICO de H2 que hoje acende a bandeira formal (`theCurvedFrame : SmoothFrameData`,
StrongFrame.lean, E(x) = diag(1+x₀², 1, 1, 1)).

ESTE ARQUIVO DEVE FALHAR AO COMPILAR. Cada `example` abaixo é UMA cláusula do contrato aplicada a
`theCurvedFrame`, com a tentativa de prova mais forte que a aritmética permite; o erro do Lean em
cada uma é o resultado esperado. O padrão é o de `TGL/ProbeTrivial.lean`, invertido: lá, compilar
provava que o tipo era frouxo; aqui, NÃO compilar prova que o tipo morde.

O que é CONCEDIDO como hipótese (não é o dente deste probe): (B1) `hBW` e (Δ) `hvac` (Δ^{it} fixa o
vácuo — o kernel não tem esse lema para `modularFlowUnitary`). O que é PROVADO de verdade no par legado:
(Δ) `flow_implemented` (rfl, `legacy_flow_is_implemented`), (S) o estado (`mixProfile`, `refl`, rfl),
(B3) a relação de Poincaré (U = 1 ⟹ `map_one`). O que NÃO tem prova — os dentes —: (B2), (D), (E).

Se este arquivo passar a compilar, o contrato foi afrouxado — e o leitor Python
(`verify_h2h3_type_contracts`) DEVE apagar a bandeira.
-/

namespace TGLExt.ProbeTrivialH2

open TGL.SpecificAQFT TGL.ModularRealization ChatgptAudit TGLV354.TraceCompletion
open TGLExt TGLExt.ContratoQG

noncomputable section

/-! ### (B2) as translações do par legado NÃO são não-triviais: U := fun _ => 1. DEVE FALHAR. -/
example : ∃ a : Fin 4 → ℝ, theSpecificAQFTWitness.U a ≠ 1 :=
  ⟨0, by simp [legacy_translations_trivial]⟩

/-! ### (D) `theCurvedFrame` NÃO é arrastado pelo 1-jato do boost. DEVE FALHAR
    (a entrada (1,0) dá 0 = sinh s · (1 + x₀²)). -/
example : ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
    theCurvedFrame.E (wedgeBoostMap s x) = boostMat s * theCurvedFrame.E x := by
  intro s x hx
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [curvedFrame_E_apply, Matrix.mul_apply, boostMat, Fin.sum_univ_four, profileFn,
      wedgeBoostMap_apply0]

/-! ### (E) a fiducial de `theCurvedFrame` NÃO é a direção modular. DEVE FALHAR
    (coluna 0 = (1+x₀²)·e₀, mas ξ_κ(x) tem componente 1 = κ·x₀ ≠ 0 na cunha). -/
example : ∀ x ∈ rightWedge, ∃ c : ℝ, 0 < c ∧
    (fun i => theCurvedFrame.E x i 0) = c • killingField 1 x := by
  intro x hx
  refine ⟨1, one_pos, ?_⟩
  funext i
  fin_cases i <;> simp [curvedFrame_E_apply, killingField, profileFn]

/-! ### O HABITANTE INTEIRO: `theCurvedFrame` como `ContratoH2` no par legado. DEVE FALHAR
    em (B2), (D) e (E). (B1) e (Δ)-vácuo são concedidos como hipóteses; (Δ)-fluxo, (S) e (B3) são
    provados de verdade (o par legado PAGA o implementador e o estado — o que ele não paga é a rede
    física, U = 1, e o frame). -/
def probeH2
    (hBW : ∀ (t : ℝ) (O : Set (Fin 4 → ℝ)) (T : WCLM),
      T ∈ sameNet O →
        (modularFlowUnitary mixProfile t).conjStarAlgEquiv T
          ∈ sameNet (wedgeBoostMap (-(2 * Real.pi * t)) '' O))
    (hvac : ∀ t : ℝ, modularFlowUnitary mixProfile t (hOmega mixProfile) = hOmega mixProfile) :
    ContratoH2 theSpecificAQFTWitness regularModularRealization where
  kappa := 1
  kappa_pos := one_pos
  Δit := modularFlowUnitary mixProfile
  Δit_vac := hvac
  flow_implemented := legacy_flow_is_implemented
  profile := mixProfile
  stateIso := LinearIsometryEquiv.refl ℂ WH
  state_is_vac := rfl
  state_flow := fun _ _ => rfl
  bw_covariance := hBW
  translations_nontrivial := ⟨0, by simp [legacy_translations_trivial]⟩
  poincare_relation := by
    intro t a
    rw [legacy_translations_trivial, legacy_translations_trivial]
    exact map_one _
  E := theCurvedFrame.E
  smooth_on := fun i j => (theCurvedFrame.smooth i j).contDiffOn
  det_unit_on := fun x _ => theCurvedFrame.det_unit x
  dragged := by
    intro s x hx
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [curvedFrame_E_apply, Matrix.mul_apply, boostMat, Fin.sum_univ_four, profileFn,
        wedgeBoostMap_apply0]
  fiducial_is_modular := by
    intro x hx
    refine ⟨1, one_pos, ?_⟩
    funext i
    fin_cases i <;> simp [curvedFrame_E_apply, killingField, profileFn]

end

end TGLExt.ProbeTrivialH2
