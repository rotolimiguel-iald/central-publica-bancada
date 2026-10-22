# F7.2 — evidência nova R2/R3: leitura da v369 e ordens

**Estatuto:** [REAL] leitura e comparação das chaves de dois arquivos; [DERIVED] apenas as contas explicitamente condicionais. Esta evidência não altera os originais, o canal, o MCP ou o gate. `NOT_FALSIFIED` não é creditação.

## Custódia e escopo da leitura

- Core atual `um_absoluto.json`: SHA-256 `a74241ff380b1b0e3d44a8f2c39e7ad4d462624b145353f3e4d82f3131036e98` (5003275 bytes).
- Cópia v369 `v369_um_absoluto.json`: SHA-256 `456f0ab149bb13f6997972dbfaf9c72a2891d744c22f04241eefa619e4953a95` (4131975 bytes).
- Parecer cético c1 `AUDITORIA_F7_2_C1_RELATORIO_aed6e453.md`: SHA-256 `50785b396680ad71920e798a9faecdb4853dd389ccb72ea01f1a057be3af3a0b`.
- Aritmética do auditor `aritmetica_f72.json`: SHA-256 `d8c896d73e8899681ab100bed9406a528dd62bef7964b5176e4f3d5dbc13b156`.
- As chaves de v369 citadas abaixo foram lidas da cópia e confrontadas com `core.clock_test_result_v369` no core atual. β foi reconstruído em runtime como `ALPHA_FINE_CODATA_2018 × √e = 0.012031300400803142`; `τ★ = t_P = 5.391125282640084e-44 s` é a hipótese da v369, não uma medida de τ★.

## R2 — o que o core já havia decidido

1. `core.clock_test_result_v369.P1.best_matter = zn67_potzel1976`: Mössbauer de ⁶⁷Zn, 93 keV. O core dá `best_matter_bound_kind = NOMINAL`, `best_matter_bound_orders = 9.269626166` e `tau_star_bound_best_s = 1.003010756e-34 s` **dentro da leitura P1**. A ficha da plataforma (`P1.platforms[id=zn67_potzel1976]`) registra que só o resumo de Potzel 1976 foi aberto, mais E e T½ do ENSDF; o texto integral não foi verificado. Logo essa cota não deve ser apresentada como limite experimental direto da TGL.
2. `P3.verdict = P3_NO_LOCAL_OBSERVABLE`. Na leitura de tempo estocástico universal, o Hamiltoniano total reparametriza o tempo comum; o core diz que razão de frequências, largura e franja locais não veem o efeito.
3. `root_law.kbar_rest_mass_excluded = true`: a leitura da lei-raiz por massa de repouso foi excluída **na leitura do core**, não como exclusão universal da teoria.
4. `partition_tag = MODULAR_LAB_BRIDGE_OPEN`. A escolha física entre P1/P2/P3 ainda depende dessa ponte. O próprio protocolo marca as leituras condicionais.

## R3 — grandezas comparáveis e parede de interpretação

**Sr da v369, [DERIVED sob P1].** Em `sr87_kim2025`, `Γ_pred = 2.358836471e-15 s⁻¹`. Para 5σ, `σ_excesso necessário = Γ_pred/5 = 4.717672942e-16 s⁻¹`; o `σ_excesso` publicado usado pela v369 é `1.353202112e-03 s⁻¹`. A razão tem `log10(σ_hoje/σ_necessário) = 12.457634837` ordens, reproduzindo `P1.clock_5sigma_deficit_orders`. O requisito `five_sigma_requirement` é **para essa plataforma com o σ de hoje**: `ℏω ≥ 3006430.047793 eV` ou GHZ `N ≥ 1693625.635095` no cenário projetado. O core os chama de limites inferiores.

**Melhor matéria no core, [DERIVED sob P1; NOMINAL].** Para `zn67_potzel1976`, `ω = 1.417658841e+20 rad/s`, `Γ_pred = 6.517866493e-06 s⁻¹`, e a cota nominal é `1.212639265e+04 s⁻¹`. A separação é `log10(Γ_ub/Γ_pred) = 9.269626166` ordens. É numericamente 3.19 ordens menor que a distância de 5σ do Sr, mas os estimadores e estatutos são diferentes: esta subtração **não é um teste entre plataformas**.

O `σ_per_s = 4.728800886e+03 s⁻¹` da ficha Mössbauer daria, como **proxy cru e condicional [DERIVED]**, `Γ_pred/5 = 1.303573299e-06 s⁻¹` e uma redução de `log10(5σ/Γ_pred) = 9.559615572` ordens, equivalente por `Γ ∝ ω²` a `ℏω ≈ 5.620116e+09 eV` se todo o resto ficasse fixo. O próprio core põe `sigma_excess_per_s = null`, `Z_expected = null` e `falsifiable = false` nessa plataforma. Portanto o proxy **não é requisito de poder registrado**, nem projeto experimental fisicamente validado.

**Neutrinos, [DERIVED condicional; comparação dimensional, não likelihood TGL].** Com `E₀ = 1 GeV`, `τ★ = t_P`, vácuo, `Kfac = 1`, `Δm²₂₁ = 7,50×10⁻⁵ eV²` ou `Δm²₃₁ = 2,5×10⁻³ eV²` aproximados, usei `Γ_ν = (β/2)(τ★/ℏ)(Δm²/2E₀)²` em eV. Os limites publicados (GeV) e o confronto condicional são:

| Canal | Cota GeV | Γ TGL hipotética eV | log₁₀(cota/Γ) |
|---|---:|---:|---:|
| Fogli 2007 (gamma0, solar+KL, 95%) | 8.10e-29 | 6.929e-58 | 38.07 |
| De Romeri 2023 A (KL, 90%) | 7.80e-27 | 6.929e-58 | 40.05 |
| De Romeri 2023 E (KL, G21, 90%) | 7.90e-27 | 6.929e-58 | 40.06 |
| ORCA6 G21 NO (90%) | 2.80e-21 | 6.929e-58 | 45.61 |
| ORCA6 G21 IO (90%) | 4.60e-21 | 6.929e-58 | 45.82 |
| ORCA6 G31 NO (90%) | 8.40e-21 | 7.699e-55 | 43.04 |
| ORCA6 G31 IO (90%) | 2.20e-21 | 7.699e-55 | 42.46 |
| JUNO 1os dados, Beccaria&Ternes 2026 (G21=G31, 90%) [fora da entrega] | 4.10e-27 | 6.929e-58 | 39.77 |

A faixa é 38.07–45.82 ordens; a componente Γ₂₁ do cenário JUNO de taxas iguais fica a 39.77. **A hipótese `Γ₂₁ = Γ₃₁` do artigo JUNO não é produzida por esta substituição de Δm² na lei TGL;** sem operador TGL em matéria, evolução, ordenamento, `Kfac` e likelihood do mesmo cenário, a razão não é uma cota sobre τ★. Fogli também usa dissipador solar distinto do dephasing puro.

**Parede para interferometria de matéria [OPEN].** Para átomos, C₇₀ e nanopartículas, a tabela custodiada traz contraste e visibilidade publicados, mas não define `ω` físico efetivo por estado/caminho, a passagem do operador TGL `Γ→visibilidade`, o fundo instrumental separado nem `σ_excesso` verificado. A partição `MODULAR_LAB_BRIDGE_OPEN` impede selecionar P1/P2/P3 como identidade física já testada. Assim, não existe número honesto de poder em ordens nem `τ★_limite` desses interferômetros hoje. O `ω` de Mössbauer acima pertence a uma transição nuclear, não preenche essa lacuna das franjas.

**Efeito no gate:** nenhum. `SEM_LIMITE_TGL` permanece [OPEN] da ponte operador/canal; `NOT_FALSIFIED` não é creditação.
