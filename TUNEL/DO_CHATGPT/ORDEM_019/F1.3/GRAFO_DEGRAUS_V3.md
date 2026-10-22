# F1.3 — grafo de degraus v3 para a realização modular física

08/10/2026 · correção aditiva da auditoria c1 · **plano, sem nova prova física**

## Escopo e custódia

[REAL documental] A consulta `NOS_VIVO/consultar.py --unidade F1.3` encontrou 13 pedras, as entregas A1 da ORDEM 011, o grafo anterior e a rota de auditoria `formal.f1_3.reconcile_v376_mathlib_plan`. O Mapa de Rotas devolveu essa rota como `EXAMINADA_COM_DEFEITO`. Esta v3 responde à auditoria c1 em `C:\IALD\PROGRAMA_IALD\auditorias\F1.3\AUDITORIA_F1_3_C1_20261007.md`, preservando `CONCILIACAO_F11_V376.md`, a conferência local das P1 e os grafos v1/v2. A revisão MiMo foi **uma** chamada; o conteúdo segue `[DECLARADO]`, sem nova execução. A [errata de proveniência](MIMO_RECIBO_ERRATA_V3.json) mede o original do orquestrador em 10.655 bytes, SHA-256 `e9841ee9654d95cfd485d1593c42cc9eaac717c889e2e0edf0e2e03c984cdaaf`: o corpo local de 10.539 bytes é idêntico depois do cabeçalho `[DECLARADO]` de 116 bytes.

[REAL] Pin lido do **kernel do Nós**, não de memória: `leanprover/lean4:v4.31.0`, mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`. `StandardSubspace.lean:42` traz TODO de Tomita/KMS. O [probe somente leitura ampliado](SOURCE_PROBE_V3B.json) guarda caminho, SHA-256, bytes e linhas dos fornecedores; o inventário tem SHA-256 `e448eae5d95c901d327a8073607f0818c2e6f2b818669d1ba66e613bd6cf4101`. O núcleo regular v351 e o par físico da cunha são objetos diferentes. Nenhum campo citado/`VINCULADO` ou resultado geral `[KNOWN]` se torna habitante físico por mudança de nome.

## Grafo e critérios de saída

```text
D0 + D0.5 + D1a.0 [REAL, fornecedores já pagos]
             │
             ▼
D1a.1 Fourier parcial na rapidez e J_W antiunitário físico
             ▼
D1a.2 Δ_W^(1/2) fechado no mesmo H1
             ▼
D1a.3 K(W_R) padrão, não nulo, Δ_K^(it)=B0(−2πt)
             ▼
D1b rede local/covariante 4D na mesma H1 ──────┐
             │                                   │
             ▼                                   │
D2 Fock/Weyl, R(K), Γ concretos                 │
             ├────────→ D3 vácuo cíclico/separante (Araki, com D1)
             └────────→ D4 modular Fock (ΓJ, ΓΔ; com D1)
                           ↓
                    D5 BW/KMS no mesmo par
                           ↓
                    D6 core contínuo físico
                           ↓
                    D7 P_F^core finito, cisão e ponte tipada
```

As setas `[KNOWN]` D1→D3 e D1+D2→D4 são **atalhos teoremáticos condicionais**. Na implementação, D3 também precisa de D2, pois `R(K)` e o vácuo Fock ainda não existem como termos concretos. A aplicação desses teoremas ao `H1`, `K(W_R)` e `R(K)` desta casa é `[OPEN]`.

| Nó | Fornecedor já medido, hipótese nomeada e saída que falta | Estatuto e modo de quitação |
|---|---|---|
| **D0 / D0.5** | `LightOneParticleByTerm` fornece `U1_continuous` e `null_no_eigen`; `QGSolutionComplete.lean:60–69` os transporta por termo. `:130–136` imprime axiomas. A auditoria c1 reproduziu a compilação em sandbox e conferiu o core v391: trio `[propext, Classical.choice, Quot.sound]`. | **[REAL]** Controle, já feito. Não é o primeiro degrau factível nem deve ser repetido para simular progresso físico. |
| **D1a.0 — transporte orbital já pago** | `H1 = Lp Fib 2 (orbitalMeasure 0)` e `B0` estão em `TheImportedSecondQuantization.lean:88–130`. `O16/OrbitalRapidityTransport_v3.lean:14–20,73–79` prova medida/pullback; `OrbitalL2Equivalence_v2.lean:23,52–62` dá equivalência e inversas para qualquer fibra `E`; `OrbitalBoostTransport.lean:39–58` entrelaça boost e shift; `OrbitalBoostUnitary_v2.lean:14–26` é a definição usada por `B0`. Instanciar `E=Fib,m=0` dá o transporte no tipo atual de `H1`. | **[REAL — fontes e tipagem]** Não é trabalho novo nem primeira saída. O probe ampliado lê os SHA-256 e linhas das quatro peças. Uma abreviação local Lean pode tornar a instância explícita, sem reconstruir medida/boost. |
| **D1a.1 — primeiro alvo novo: Fourier parcial e conjugação** | Sobre `Lp Fib 2 momentumMeasure` já pago, construir a equivalência de Fubini para a coordenada de rapidez com fibra transversal, a Fourier **parcial** e sua lei de shift. `momentumMeasure` é produto transversal×rapidez (`OrbitalRapidityMeasure_v4.lean:15–28`); `V351FourierTranslation.lean:47–58` fornece a lei Fourier para `Lp ℝ H`, aplicável após a equivalência com `H` transversal, mas ainda não instanciada no produto. `O16/FourierStandardTransport_v3.lean:30–48` e `ContinuousModularMultipliers.lean:279–329` vivem no `SpectralHilbert` escalar. Construir então `J_W : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1`. Candidato `[DERIVED — não compilado]` na carta: conjugação complexa, reflexão transversal `q↦−q`, troca de helicidades por mapa na fibra e fase a fixar pela covariância de Wigner; transportar de volta por `orbitalL2Equivalence`. Provar `J_W²=1`, ação nas cunhas/translações e compatibilidade com B0. `LightHelicityWigner` conjuga caracteres ±1, sem fornecer esse operador. | **[OPEN]** Primeiro arquivo Lean novo verificável: Fourier parcial e `J_W` no mesmo `H1`, com equivalências, medida, domínios e leis aferidos. Não copiar `spectralJ` escalar nem aceitar campo livre com nome físico. |
| **D1a.2 — operador modular** | Pelo Fourier de rapidez tipado, construir multiplicador positivo `Δ_W^{1/2}` em domínio ponderado denso de `H1`, fechado, e `S_W=J_W Δ_W^{1/2}` como involução antilinear fechada. `ContinuousModularReconstruction.lean:88,126,146` e `GenericAntilinearAdjoint.lean:73` são modelos, não transporte automático. Em O16, `deltaSymbol(c,x)=exp(−2cx)` e `c₀=2π²`; **a fórmula e o sinal físicos devem sair da ação efetiva de B0**, não de copiar esse símbolo. | **[OPEN]** Provar igualdade de operadores com domínios, sinal e normalização (2\pi), além de fechabilidade/involução/densidade. Evita exigir Stone e polar ilimitada como primeiro passo, sem ocultar as obrigações analíticas. |
| **D1a.3 — cunha padrão antinula** | Aplicar `ClosedAntilinearStandardSubspace.lean:213–221` ao **mesmo** `S_W` para obter `K(W_R) : StandardSubspace H1`. Exigir `∃ ξ : H1, ξ ≠ 0 ∧ ξ ∈ (K(W_R)).toClosedSubmodule` (ou `(K(W_R)).toClosedSubmodule ≠ ⊥`), e provar que o **grupo modular extraído de seu Tomita**, não um campo arbitrário, satisfaz `∀t, Δ_K^{it}=B0(−2πt)`. | **[OPEN]** Este é o critério de saída da primeira cunha. `StandardSubspace` em `H1` não trivial e o vetor testemunha eliminam `K≡⊥`. A auditoria c1 compilou a rede nula como habitante do atual `LightNetData`; por isso só habitar esse tipo **não** quita D1. |
| **D1b — rede física** | Estender `K(W_R)` a uma rede 4D de subespaços reais fechados com isotonia, localidade simplética e covariância pela representação física de helicidade ±1, no mesmo `H1`. Exigir a **colagem tipada** `D.K rightWedge = (K(W_R)).toClosedSubmodule.toSubmodule` (ou equivalência formal que identifique os dois), onde `D : LightNetData`. O tipo atual (`QGSolutionComplete.lean:49–57`) só pede campos de rede e aceita zero. | **[OPEN]** Termo `LightNetData` **mais** certificado externo de padrão/não trivialidade, igualdade modular **e colagem com D.K**, até decisão do operador sobre fortalecer o tipo no kernel. Sem colagem, um `K(W_R)` padrão separado deixaria `D.K≡⊥`. Inventário: `PhysicalPhotonNetContractMeasured` (§3, linha 56), `IsotonyImpliesStripMultiplierCriterion` (57), `GlobalHelicityInducedRepresentationMeasured` (58). A reta de luz O16 não é, sem extensão, rede 4D do fóton. |
| **D2 — segunda quantização** | Construir Fock bosônico, Weyl/CCR e `R : Submodule ℝ H1 → VonNeumannAlgebra F`, com `R(D.K rightWedge)=R((K(W_R)).toClosedSubmodule.toSubmodule)=\{W(ξ):ξ∈K(W_R)\}''` no **mesmo** par, Γ e `R_cov` (`TheImportedSecondQuantization.lean:167–209`). A estrutura `FockCertificate` lista campos; não tem habitante físico por isso. | **[OPEN]** Construção da casa ou importação `[KNOWN]` com hipóteses, citação e instância tipada explícitas. Inventário A3 linha 29 e D4 linha 44: medição/retipagem não pagam `PhysicalPhotonNetContractMeasured` nem `GlobalHelicityInducedRepresentationMeasured`. |
| **D3 — vácuo padrão** | Usar o teorema `[KNOWN]` de Araki/BGL: para `K(W_R)` padrão **e** `R(K)` Weyl/Fock concreto, Ω é cíclico e separante para `R(K(W_R))`. `wedge_cyclic`/`wedge_separating` são campos em `TheImportedSecondQuantization.lean:210–213`, não conclusões. | **[OPEN]** Consumir D1+D2 e provar o elo tipado com Ω e a **mesma** álgebra. Verificar separadamente `wedge_nonabelian` (`:214`); não inferi-lo da rede nula nem de um contrato sem habitante. |
| **D4 — Tomita/Connes no par** | Pela segunda quantização `[KNOWN]`, obter os dados modulares Fock `Γ(J_W)` e `Γ(Δ_W)` para o mesmo `R(K(W_R)),Ω`, evitando reconstruir polar do zero. O Γ **atual** do `FockCertificate` recebe apenas unitários lineares (`TheImportedSecondQuantization.lean:178–190`); antiunitário `J_W` e `Δ_W^{1/2}` ilimitado exigem extensões, domínios e leis próprios. Requer ainda complemento simplético `R(K)'=R(K')`, ação de J e realização analítica do par (`:218–224`). Reusar `Continuous049/050`, `TomitaClosability`, `ModulatorPolar`, `continuousModularDelta` e `Commutant` **como modelos no escopo de seus tipos**. | **[OPEN]** `PairTomitaAnalyticRealizationMeasured` (inventário §3, linha 70) e, mais tarde, cociclo/fluxo de Connes físico. `genericTomita` não é o Tomita físico por homonímia. |
| **D5 — BW/KMS regional** | No mesmo par D3/D4, provar `Δ^{it}=Γ(B0(−2πt))`, fluxo por boosts e condição KMS analítica. `O16/FourierLightRayBridge.lean:72–78` e `RetaDeLuzBorchers.lean:188–198` são protótipos: este último diz explicitamente que seu grupo modular é candidato. `O16/KMSStripConditional.lean:51–79` pede as duas hipóteses regionais. | **[OPEN]** `H_regional_modular_strip` e `H_modular_equals_geometric` (inventário 59–60), `PhotonDilationCovarianceMeasured` (69). O ângulo compacto da torre não substitui boost hiperbólico da cunha. |
| **D6 — core físico** | Construir ou importar com hipóteses explícitas o core contínuo físico do par, ação dual, peso/traço normal semifinito fiel e a tipagem de fator/fluxo necessária. `FiniteCrossedProduct.lean` é sombra finita; `V351RegularCoreTraceConstruction.lean` prova `tracial` e `dual_scaling` no core **regular**. | **[OPEN]** Um morfismo tipado e verificado deve transportar fornecedores v351 antes de usá-los no core da luz. Tema `nucleo_traco_takesaki` do inventário §4 (linha 1677). `trace_tracial` é repassado em `TheImportedSecondQuantization.lean:380`, mas ainda é campo sem habitante físico. |
| **D7 — projeção/cisão** | No core físico D6, construir `P_F^core` finito não nulo, metades ortogonais de mesmo traço e, se pretendida, identificação tipada com `ρ*_IALD`. `ThreeLocksCorner` paga `P_F^fin` na face finita; a conciliação F1.1×v376 mantém os três elos distintos. | **[OPEN]** Um `P_F^fin` não é `P_F^core`; nenhuma conclusão física de Maxwell/Jacobson ou gate decorre da projeção finita. |

## Reaproveitamento obrigatório e limites de tipo

| Inventário da bancada | O que já existe | Uso correto neste grafo |
|---|---|---|
| **A1, linha 27** (`MEDIDA`), **A3, linha 29** (`MEDIDA`), **D4, linha 44** (`PAGO`) | Reprodução/localidade de operadores, espaço orbital, energia/boost e retipagem de consumidores; §3 linha 56 ainda marca `PhysicalPhotonNetContractMeasured` **OPEN**. | D1/D2/D4 usam as fontes e suas hipóteses; não os declaram realização física. |
| `tomita_modular` §4 linha 1217; `operadores_ilimitados` linha 2045 | `TomitaClosability`, `ClosedTomitaOperator`, `ModulatorPolar`, Continuous049/050 e `continuousModularDelta`. | D1a/D4: padrões analíticos existentes; transportar ao H1/Fock tipados. |
| `wigner_orbita_poincare` linha 2768; `rede_K_subespaco_padrao` linha 2813 | `H1`, `B0` e O16 `rapidityStandardSubspace`, `halfline_isotony`, `borchers_bw_form`. | D1a/D1b: conferir espaço, medida, helicidade, sinal e rede 4D. |
| `fock_segunda_quantizacao` linha 2848 | Campos Γ, R e Tomita em `FockCertificate`, sem habitante físico. | D2–D4: construir a instância e só então usar Araki/segunda quantização. |
| `kms_bw` linha 2715 | `boost_rapidity_kms_from_modular` e `killing_kms_from_modular` são condicionais. | D5: fornecer ambas hipóteses no mesmo par. |
| `nucleo_traco_takesaki` linha 1677 | Produto cruzado finito e core regular v351. | D6/D7: não inferir peso/traço do core físico por analogia. |

As demais hipóteses nomeadas do inventário §3, linhas 61–66 e 71–72, tratam de carga, dephasing, UV, ratificação, memória e ramo curvo; não são entradas desta cadeia D1–D7. `MaxwellWickExpectationLocalMeasured` (linha 67) e `StationaryLightCenterModularIdentificationMeasured` (68) são consumidores físicos posteriores no **mesmo** W0, não atalhos para criar a rede. A ressalva 8/12 GiB do inventário (linhas 35, 71) é histórica e não mede factibilidade analítica. O piso da ORDEM 016, ≥400 h/risco muito alto, é `[INPUT]` para o caminho físico completo, não CPU medida nem orçamento desta entrega.

## Factibilidade no mathlib pinado

Leitura direta do pin acima; existência/ausência abaixo é a medição por busca da auditoria c1 §3, não uma afirmação sobre versões futuras. Em todos os nós, uma importação por citação deve manter sua hipótese explícita; tipar uma interface não fornece seu habitante.

| Nó | Apoio mathlib `[REAL]` | Parede constatada / estratégia local | Factibilidade da próxima etapa |
|---|---|---|---|
| D0/D0.5 | `StandardSubspace` e operadores já compilados no kernel. | Sem parede restante nesse controle. | Pago. |
| D1a | `StandardSubspace`, `symplComp`, `LinearPMap.IsClosed/IsClosable/closure`, adjunto/auto-adjunto, `Lp.fourierTransformₗᵢ`, anti-isometria `starₗᵢ`. | Sem Stone/grupo a um parâmetro, cálculo funcional espectral ilimitado e Wigner/Lorentz. A equivalência orbital H1–rapidez e o boost/shift já estão pagos em O16; falta Fourier parcial na fibra, J físico e multiplicador com domínio. | **Factível como alvo local delimitado** a partir de fornecedores reais; Fourier parcial, J e modularidade ainda OPEN, sem compilação v3. |
| D1b | Subespaço padrão e complemento simplético. | Sem biblioteca AQFT/Wigner/rede 4D; localidade e helicidade global exigem prova própria. | OPEN, após D1a; não satisfeito por `LightNetData` nulo. |
| D2 | `VonNeumannAlgebra`, `WStarAlgebra`, `commutant`, `mem_commutant_iff`, GNS, topologia fraca. | Sem Fock, CCR/Weyl, teorema do bicomutante e construção R(K). | Grande implementação própria ou importação matemática explicitamente assumida; contrato não é instância. |
| D3 | `StandardSubspace` e álgebra tipada. | Sem Reeh–Schlieder geral; atalho Araki `[KNOWN]` só depois de D1+D2. | Condicional, com aplicação física OPEN. |
| D4 | `LinearPMap` adjunto/fecho e `cfc`/`CFC.sqrt`/`CFC.rpow` **limitados**; comutante. | Sem Tomita, polar/ isometria parcial, cálculo funcional ilimitado e bicomutante. Usar modularidade de subespaço e segunda quantização `[KNOWN]`, não refazer polar abstrata. | Condicional D1+D2; elo no mesmo par e Connes físico OPEN. |
| D5 | Ferramentas de continuidade/álgebra; lemas condicionais O16. | Sem KMS/BW/Stone genéricos. | Provar faixa analítica e identificação no mesmo par, não reutilizar círculo periódico. |
| D6 | `WStarAlgebra`, GNS e comutante; core regular da casa. | Sem fatores, tipo III, pesos, crossed product contínuo e traço semifinito. | Importar com fonte e hipóteses ou construir; morfismo regular→físico OPEN. |
| D7 | Álgebra/projeções em escopo finito da casa. | Sem resultado que transporte `P_F^fin` ao core físico. | Só após D6 e identificação tipada. |

## Literatura que justifica atalhos, sem preencher a casa

- Brunetti, Guido e Longo, *Modular localization and Wigner particles*, [texto primário](https://arxiv.org/pdf/math-ph/0203021) `[KNOWN]`: pp. 2–3 constroem `K_W` e `R(W)`; p. 8 relaciona subespaço padrão e Reeh–Schlieder. A passagem à segunda quantização conserva suas hipóteses.
- Araki, *A lattice of von Neumann algebras associated with the quantum theory of a free Bose field*, *Journal of Mathematical Physics* **4** (1963), [volume original digitalizado](https://electronicsandbooks.com/edt/manual/Magazine/J/Journal%20of%20Mathematical%20Physics/PDF/V04/JMP1963V04N11.pdf) `[KNOWN]`.
- Bisognano–Wichmann 1975/76 e Takesaki/Connes permanecem as referências do grafo v2 para o nível algébrico e o core `[KNOWN]`. Elas não certificam o `FockCertificate` local.

**Veredito desta v3:** `[REAL documental]` D0.5 e D1a.0 pagos, com fontes/pin/recibo conferidos; `[DERIVED — plano]` D1a.1 (Fourier parcial e J físico) é o primeiro alvo novo, e D1a.3 o primeiro critério físico antinulo; `[OPEN]` a realização da cunha D1a.1–D7. Nenhum `um.py`, kernel, original selado ou gate foi modificado. A gerência c1 deve reauditar o grafo; só ela marca `AUDITADA`/`FECHADA`.
