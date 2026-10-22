import ContratoQG
-- NA TRANSPOSIÇÃO (TGLExt/ProbeTrivialH3.lean): `import TGLExt.ContratoQG`. Única mudança.

set_option autoImplicit false

/-!
# ProbeTrivialH3 -- CONTROLE NEGATIVO   [DIAGNÓSTICO; NUNCA importado por TGL.lean / TGLExt.lean]
  Frente W2_final, 23/09/2026 (2ª versão: contrato parametrizado por (W, R); docstring por C3 do cético).

Tenta habitar `ContratoH3 theSpecificAQFTWitness regularModularRealization` (o PAR LEGADO) com o
habitante GENÉRICO de H3 que hoje acende a bandeira formal (`theHorizon : HorizonEquilibriumData`,
TheMasterFires.lean: κ = 1, G = 1, δA = 1, δS = 1/4, δQ = 1/(8π) — aritmética exata, sem horizonte).

ESTE ARQUIVO DEVE FALHAR AO COMPILAR. Os cinco números soltos de `theHorizon` NÃO são recusados por
aritmética (cinco números sempre podem ser realizados por algum horizonte em algum lugar); são
recusados pela AMARRAÇÃO: todo `ContratoH3 W R` exige um `ContratoH2 W R` no MESMO horizonte, e δA, δS,
δQ são CALCULADOS da mesma cunha, do mesmo frame e do mesmo estado (`H2.profile`).

ONDE ELE FALHA, DITO COMO O LOG MOSTRA (C3; medido em probe_H3_result.txt, 5 erros): (1) na projeção
(`⟨_, rfl⟩` não encontra o `ContratoH3`); (2) no campo `H2` (dois erros: não há termo —
`contratoH2_empty_on_legacy_realization`); (3) em `dS_eq` (goal residual
`4⁻¹ = finiteEntropy (towerW mixProfile 0) − finiteEntropy (towerW sorry.profile 0)`: o perfil do estado
é o de H2, que não existe); (4) em `dQ_eq` (calor de matéria nula = 0 ≠ 1/(8π), por aritmética,
independente de H2). Os dois campos com `rfl` cujo goal CONTÉM o sorry sintético de `H2`
(`dA_eq := by rfl`, `clausius := by rfl`) NÃO acusam erro por SUPRESSÃO — o Lean silencia a falha de
`rfl` em goal com sorry sintético; isso não é prova. Medido em isolamento, com `C : ContratoH2 W₀ R₀`
genérico (`Check_isolated_fields.lean`, rc=1, 3 erros), que `rfl` falha nos dois e `simp` falha em `dS_eq`.
A linha de cada erro está no log, não nesta docstring.
-/

namespace TGLExt.ProbeTrivialH3

open TGL.SpecificAQFT TGL.ModularRealization ChatgptAudit TGLV354.TraceCompletion
open TGLExt TGLExt.ContratoQG

noncomputable section

/-! ### 1. `theHorizon` como projeção de algum contrato no par legado. DEVE FALHAR
    (o `⟨_, rfl⟩` não encontra o `ContratoH3`; e `theHorizon_is_not_a_contract_projection` refuta). -/
example : ∃ C : ContratoH3 theSpecificAQFTWitness regularModularRealization,
    C.toHorizonData = theHorizon :=
  ⟨_, rfl⟩

/-! ### 2. O HABITANTE INTEIRO com os números de `theHorizon` e o horizonte da cunha legada.
    DEVE FALHAR no campo `H2` (não há `ContratoH2` no par legado), em `dS_eq` e em `dQ_eq`; `dA_eq` e
    `clausius` (ambos `rfl`) ficam SUPRIMIDOS (goal com o sorry sintético de `H2`) — ver
    `Check_isolated_fields.lean`. -/
def probeH3 : ContratoH3 theSpecificAQFTWitness regularModularRealization where
  H2 := by
    -- não há termo: o par legado tem U = 1 (contratoH2_empty_on_legacy_realization)
    exact Classical.choice ⟨_⟩
  G := 1
  G_pos := one_pos
  screen := Set.Icc 0 1
  screen_measurable := measurableSet_Icc
  screen_pos := by
    rw [Real.volume_Icc_pi]
    simp
  screen_finite := by
    rw [Real.volume_Icc_pi]
    simp
  eps := 1
  eps_pos := one_pos
  lam0 := -1 / 4
  lam0_neg := by norm_num
  lam0_in_wedge := by norm_num
  matter := fun _ => 0
  perturbed := mixProfile
  level := 0
  dA := 1
  dA_eq := by
    -- 1 = areaVariation H2 (Set.Icc 0 1) 1 : não há como; o número é solto (SUPRIMIDO aqui)
    rfl
  dA_ne := one_ne_zero
  dS := 1 / 4
  dS_eq := by
    -- 1/4 = prefixEntropyIncrement H2.profile mixProfile 0 : não reduz sem H2 (ACUSA erro: goal residual)
    simp [ChatgptAudit.Response028.prefixEntropyIncrement]
  dQ := 1 / (8 * Real.pi)
  dQ_eq := by
    -- 1/(8π) = calor de matéria NULA = 0 : falso por aritmética
    simp [horizonHeat, pairing]
  area_entropy := by norm_num
  clausius := by
    -- κ do H2 inexistente (SUPRIMIDO aqui)
    rfl

end

end TGLExt.ProbeTrivialH3
