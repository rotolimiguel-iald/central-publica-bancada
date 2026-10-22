# F1.3 — v3.2, saída tipada do D1a.3

08/10/2026 · acréscimo à v3 e à v3.1 · sem novo provedor

**[REAL — estado consultado]** O Nós Vivo já registra a v3.1 e sua reauditoria. A tabela de factibilidade, a parede de Fubini L² vetorial, o uso direto de `genericTomita`/`genericTomitaAdjoint` em `H1`, as referências bibliográficas e a extensão da família curva até a linha 75 já estão em `COMPLEMENTO_V3_1_FACTIBILIDADE_20261008.md`; não são refeitos aqui. A reauditoria c1 `AUDITORIA_F1_3_C1_ad949e97.md` (SHA-256 `009ef22daccbeaf073872f2d10797893d549542e287a31c67846b69ba0e649af`) julgou os pedidos 1, 4, 5 e 6 atendidos, o 3 parcial e o 2 não atendido. A frase da v3.1 de que a saída só poderia ser tipada após construir está **corrigida ao lado**: a sonda da c1 tipou o enunciado sem construir um habitante.

## Saída D1a.3 adotada como proposta Lean

**[REAL — tipagem da sonda; OPEN — habitante]** `ENUNCIADO_D1A3_BGL_V3_2_20261008.lean` é cópia byte a byte da sonda `F13v31_D1a3_bgl.lean` da c1, SHA-256 `e4da9e865d00bdcb1c112fade347fe4a169e7e9d0e80227c81267861e6b9e540`. Seu log preservado (`ENUNCIADO_D1A3_BGL_V3_2_20261008.build.log`, SHA-256 `551efbbb4210041e6f6580e7f519646c1617af8d2f3576b9337d555287eb0556`) mostra EXIT 0 e `#print axioms` no trio `propext`, `Classical.choice`, `Quot.sound`; a única mensagem é de depreciação de `push_neg`. Trata-se da **compilação da c1**, não de uma nova compilação nossa.

O enunciado escolhido é `AuditF13v31.D1a3OutputBGL` (linhas 173–187). Ele recebe como campos ainda abertos `Fub`, `J_W`, `T` (candidato a `Δ_W^{1/2}`) e `σ`, além de fechamento, involução e densidade de `S_W := genericTomita T J`. Constrói `K(W_R)` **condicionalmente** por `closedAntilinearStandardSubspace` (linha 190), em vez de recebê-lo como campo livre. `IsTomitaSquare` (linha 43) caracteriza por igualdade de grafos a relação **`Δ_K = S_K†S_K`**, no padrão de `ContinuousModularReconstruction.lean:87–112`. `Δ` ainda é um **campo** da estrutura, determinado de modo único pelo grafo (`tomitaSquare_unique`, linha 79), não uma definição independente por `def`. `IsMultiplierAfter` (linha 50) fixa a multiplicação por `exp σ` após `partialFourier Fub`, e `ModularGroupIsBoost` (linha 56) vincula `B0(−2πt)` ao multiplicador `exp(itσ)` depois do Fourier. Esse último campo é o **contrato tipado do cálculo espectral**: ainda não define `Δ_K^{it}` em Lean nem prova sua identificação funcional completa com `B0`; essa etapa segue **[OPEN]**. A consequência `exists_nonzero` (linha 204) usa `H1_nontrivial` e a padronidade; **`∃ ξ ≠ 0` não é uma hipótese de saída**.

**[DERIVED — proposta para a fila do operador]** A interface tipada é `AuditF13v31.LightNetStandardWedgeDataBGL` (linha 222):

```lean
structure LightNetStandardWedgeDataBGL extends LightNetData where
  out : D1a3OutputBGL
  wedge_glue : toLightNetData.K rightWedge = out.KWR.toClosedSubmodule.toSubmodule
```

Os três componentes ficam tipados: rede existente, certificado modular definido pelo Tomita de `K(W_R)` e colagem com `D.K` na cunha direita. **Pede-se à gerência que registre a proposta na fila do operador** para decidir se o tipo do kernel deve ser fortalecido; esta nota não toma essa decisão nem altera `LightNetData`.

**[OPEN]** A estrutura compilar não fornece `Fub`, `J_W`, `T`, `σ`, `K(W_R)` físico, rede 4D nem habitante do certificado; também não demonstra positividade de `T`, a relação quadrática necessária para chamá-lo `Δ_W^{1/2}` ou o cálculo funcional `Δ_K^{it}`. O primeiro trabalho de construção segue D1a.1, começando pela equivalência de Fubini L² vetorial, ausente no pin. A tipagem não prova a realização física, não altera kernel, `um.py` ou gate.
