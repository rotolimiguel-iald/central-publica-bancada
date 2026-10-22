[REAL — lido por script em 26/09/2026 22:30 (−03); ordem da gerência; COMEÇA SÓ DEPOIS da ORDEM 016 (ver §1)]

# ORDEM 017 — A QUITAÇÃO POR TERMO DE H2 E H3: CONSTRUIR OS CERTIFICADOS DA LUZ

**CITA:** `um.py` v373 (sha16 `ba914d49498d209b`), com o kernel `TGLExt.TheImportedSecondQuantization` (sha16 `ef35478400ef07f2`), `TGLExt.QGReaderUVLock` (sha16 `77ba8803c7cd0a80`) e `TGLExt.QGCitationDischarge` (sha16 `78cd50266981be50`); `ORDEM_016_a_gravidade_quantica_primeiro.md` (sha16 `c0614dbd8d9ba606`); `RECIBO_016_FECHAMENTO_PARCIAL.md` (sha16 `26bed47e51d49826`); a lista `P3_HIPOTESES_ABERTAS.json` do fechamento parcial (sha16 `faed6d9cd0528d85`).

**Ordem do operador (26/09/2026, verbatim):** «confirmo tudo, pode fazer» — em resposta à proposta da gerência de mandar a classe B (a quitação POR TERMO) como ordem à bancada, depois da Parte B da ORDEM 016.

## 0. Onde estamos (lido do selo v373)

- A QG da TGL está formalizada como **implicação fechada por citação**. Na v373, H2 e H3 ficaram **quitadas por citação, numa classe própria** (`qgCite_*`, bandeiras `gpc_`): o tipo de cada nome carrega os certificados citados — `LightOneParticle`, `FockCertificate`, `MaxwellCertificate` — como hipóteses.
- **Por termo, nada mudou:** `gpf_H2`, `gpf_H3` e `gpi_H3` seguem falsas, porque **nenhum habitante dos três certificados é exibido**. A fronteira do gate (`kernel_frontier.remaining`) tem dois itens: H2 (o quadro modular suave e a identificação geométrica) e H3 (área–calor no mesmo horizonte físico).
- O que esta ordem pede é exatamente isso: **exibir os habitantes**. Quem constrói os três certificados por termo cunha os nomes reservados por termo.

## 1. Quando

1. **Não começar antes** de `DO_CHATGPT\ENTREGA_016_RELATORIO_FINAL.md` estar entregue. A Parte B da ORDEM 016 (o ringdown) **não pausa** por causa desta ordem.
2. Depois disso, trabalhar por **fases**, cada uma com entrega própria (§3). Uma fase só abre com a anterior entregue.

## 2. O alvo, em tipos (nada de prosa)

Os três nomes reservados POR TERMO, com os tipos que o contrato já fixa:

    TGLExt.qgPrice_H2_smoothModularFourFrame_discharged    : ContratoH2 W₀ R₀ N₀
    TGLExt.qgPrice_H3_localHorizonEquilibrium_discharged  : ContratoH3 W₀ R₀ N₀ T₀
    TGLExt.qgImport_H3_horizonEquilibriumData_produced    : ContratoImportH3 W₀ R₀ N₀ T₀ qgPrice_H2_…

com W₀ = `lightNet C₀`, R₀ = `lightRealization C₀`, para **um certificado C₀ CONSTRUÍDO** (não hipótese). O caminho: habitar `LightOneParticle`, `FockCertificate L₀` e `MaxwellCertificate C₀` **por termo**; os construtores `lightH2`, `lightH3`, `lightImport` da v372 fazem o resto.

## 3. As fases

| fase | o que construir | as hipóteses nomeadas da P3 que ela descarrega |
|---|---|---|
| **F0 — mapa** (teto 6 h) | Para cada campo dos três certificados: o que a Mathlib já tem (nome exato), o que falta, e **a árvore de alternativas** (pelo menos duas rotas por campo difícil). Nenhum teorema novo; só o mapa, com nomes Lean verificados por `#check`. | — |
| **F1 — a luz de uma partícula** | Um habitante de `LightOneParticle`: a representação de helicidade ±1 sobre a órbita sem massa (a fibra `Fib` e `H1` da v372), a rede de subespaços padrão `K(O)` com `K_mono`, `K_local`, `K_translate`, `K_boost`, `U1_continuous`, `null_no_eigen`. | `GlobalHelicityInducedRepresentationMeasured`, `IsotonyImpliesStripMultiplierCriterion` |
| **F2 — o Fock** | Um habitante de `FockCertificate L₀`: o Fock simétrico, o funtor Γ, a rede de Weyl `R(K)` como álgebras de von Neumann, a separação e a ciclicidade na cunha, `bw_kms`, a realização de Tomita, `Γ_no_fixed`, o núcleo de Takesaki com o traço. | `H_modular_equals_geometric`, `H_regional_modular_strip`, `PairTomitaAnalyticRealizationMeasured`, `PhotonDilationCovarianceMeasured`, `StationaryLightCenterModularIdentificationMeasured` |
| **F3 — Maxwell** | Um habitante de `MaxwellCertificate C₀`: o domínio nomeado, o tensor ⟨ψ, :T_ab: ψ⟩ (Wick) como `StressTensorDataLocalV32`, o elo da carga modular (`charge_link`) e o estado coerente não trivial. | `MaxwellWickExpectationLocalMeasured`, `PhysicalModularChargeLinkMeasured`, `TeleologicalPhysicalInputsMeasured` |
| **F4 — a cunhagem** | Os três nomes reservados por termo, com `#print axioms` no trio, e o leitor A-8 da v372 (`#assert_exact_type`) aceitando cada um contra o tipo do §2. | — |

Cada fase entrega em `DO_CHATGPT\ORDEM_017\F<n>\`: os `.lean`, um log de compilação por arquivo, `#print axioms` de cada declaração, e `ENTREGA_017_F<n>.md` com estatuto por campo (PAGO / MEDIDA com o lema que falta, nomeado).

## 4. O protocolo (vale para toda fase)

- **Árvore de alternativas obrigatória.** Diante de um campo difícil, abrir pelo menos duas rotas e tentar as duas antes de registrar MEDIDA. **Parede só a gerência declara.** Uma MEDIDA diz o lema exato que falta e por que as rotas tentadas não o deram.
- **Campo citado ≠ campo pago.** Onde o campo exigir um teorema publicado que não cabe na fase, ele pode ficar como hipótese NOMEADA, dita no arquivo — mas então o nome reservado por termo **não** é cunhado, e isso se diz.
- **Instâncias locais sempre com nome próprio**, prefixado pelo módulo (achado do RECIBO 016: anônimas colidem quando dois arquivos entram no mesmo ambiente).
- **Compilação isolada** sobre uma cópia limpa do kernel v373 (`lake env lean <arquivo> -R <pasta> -o <pasta>`). Nunca `lake build` no kernel canônico; a bancada não escreve o `um.py`.
- **Colisão de nomes** conferida contra todas as declarações do kernel v373, por script; colisão listada, nunca silenciada.
- Zero `sorry`, zero `axiom`; `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}.
- Pedido por pergunta com `request_id` próprio, ledger no ato, nada confidencial (as regras da §8 da ORDEM 016 continuam valendo).

## 5. O que não muda

Nada move o gate: segue `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`. A quitação por termo, se vier, é a quitação **da implicação sem as hipóteses citadas** — não é confirmação da natureza. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.
