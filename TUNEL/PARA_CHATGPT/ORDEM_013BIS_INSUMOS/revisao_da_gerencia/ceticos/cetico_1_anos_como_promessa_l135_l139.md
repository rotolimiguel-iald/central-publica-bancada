# CÉTICO 1 — achado «anos como promessa» (ORDEM 013-bis l.135 §4.0 (g) e l.139 §4.0 (i))

Data: 22/09/2026. Lente refutada: estatistica_poder. Veredito: **NÃO refutado** (refutado=false). Gravidade mantida: **IMPORTANTE**.

## 1. O que a ordem diz (lida com numeração)

- l.135 (g): «R-LIN fecha em ~1 ano de O5 estatisticamente, mas é EXCLUDED_IF_UNIVERSAL na C1 …» e, no fim do mesmo parágrafo: «esta ordem fixa N_alvo e o critério de qualidade, nunca anos.» O cabeçalho do parágrafo declara `[DERIVED, cenário; banda de SNR ×1,56–2,06 …]`.
- l.139 (i): «~130 eventos com SNR_RD ≥ 50 (~1,3 ano a 10²/ano) ou ~33 com SNR_RD ≥ 100 (~3,3 anos)».
- l.125 (b): «Convenção de poder desta ordem: 90 %» … «N₉₀ = 1,578 × N₅₀ … as outras leituras pela mesma razão».
- l.216 §5: proíbe «escrever «5σ alcançável em N anos» como promessa (N_alvo e IC de taxa, sim; anos, só como cenário [DERIVED] com a banda)».

## 2. Números refeitos por script (fonte: `medir/B_catalogos/RENDIMENTO_E_5SIGMA.json`, gerado por `rendimento_e_5sigma.py`)

Premissa do arquivo: `5 sigma = sum z_i^2 >= 25` ⇒ z esperado = 5 ⇒ **poder 50 %** (N₅₀). Taxa O4ab = 14,48 pSEOBNR/ano. R-LIN N_O4 = 162,8. f₉₀ = (5+1,28)²/25 = 1,5775.

| g (SNR ×) | N₅₀ | N₉₀ | taxa O5 (×g³) | anos₅₀ | anos₉₀ |
|---|---|---|---|---|---|
| 1,5625 | 66,7 | 105,2 | 55,2/ano | 1,207 | 1,904 |
| 1,7857 | 51,1 | 80,5 | 82,5/ano | 0,619 | 0,977 |
| 2,06 | 38,4 | 60,5 | 126,6/ano | 0,303 | 0,478 |

- O JSON `anos_O5_a_taxa_x4.6..5.7` = [0,924; 1,207] usa **taxa fixa g_lo³** para os dois extremos (é exatamente o I6 do CRITICO.md l.68: «calculados a taxa fixa»). Com a taxa coerente (g³ em cada extremo) a banda é **0,62–1,21 ano** (SNR ×1,56–1,79) e **0,30–1,21** se incluir o ×2,06 que o próprio cabeçalho de (g) declara. `REFEITOS_2.json` confirma o fator de taxa para o R-B (11,7→7,8 anos entre g=1,5625 e 1,7857 = ×0,67; aplicado ao R-LIN dá 0,62–0,81 — bate com o revisor).
- R-B em 3G: N₅₀ = 131,2 (SNR_RD ≥ 50) / 32,8 (≥ 100); **N₉₀ = 207 / 52**; anos a 10²/ano e 10/ano: 1,31 / 3,28 (50 %) → **2,07 / 5,17 (90 %)**. Âncora: σ = 0,058 do GW250114 em SNR_RD ~40 (`premissas` do JSON; A-05).

## 3. Por que o achado se sustenta

1. **«~1 ano» é ponto onde a medição é banda de fator 2–4** (0,62–1,21; 0,30–1,21 com ×2,06). O parágrafo (g) é o único da ordem que se encerra dizendo «nunca anos» — e dá o ano sem banda na mesma frase. Inconsistência interna medida.
2. **(i) dá anos e N a 50 % de poder sem dizê-lo, numa ordem cuja convenção declarada (l.125) é 90 %.** «~130 / ~33» são N₅₀; a convenção da ordem manda N₉₀ = 207 / 52 e 2,1 / 5,2 anos. A bancada, que «calcula e registra» as outras leituras (l.125), herda dois números com convenção diferente no mesmo §4.0 — ambiguidade explorável e número sem etiqueta de poder.
3. l.216 admite anos «só como cenário [DERIVED] com a banda». (g) tem etiqueta de cenário no cabeçalho, mas o «~1 ano» não tem banda; (i) não tem banda nem poder. Não é gosto: é a régua da própria ordem aplicada a si mesma.

## 4. Reparos ao próprio achado (não mudam o veredito)

- O revisor escreve que o [0,924; 1,207] tem «o ×2,06 BNS embutido». **Não tem**: o JSON usa g = 1,5625–1,7857 (alcance BBH 2500 vs 1400–1600 Mpc); o ×2,06 só aparece no cabeçalho de (g) da ordem e no «39–68» da SINTESE (l.70), que é 163/2,06² = 38,4. O erro do JSON é outro (taxa fixa, I6).
- A correção proposta pelo revisor mistura N de ×2,06 (39–68) com taxa de ×1,56–1,79 (55–83/ano). A correção FINAL abaixo torna as bandas coerentes com a convenção que a própria (g) já usa («165–249 eventos pSEOBNR em 3 anos» = 55–83/ano) e com o ×2,06 do cabeçalho.

## 5. Gravidade

IMPORTANTE (mantida). Não é BLOQUEANTE: não induz erro de física; os números existem no arquivo e estão etiquetados [DERIVED]. É número sem banda e convenção de poder inconsistente dentro da mesma seção — exatamente o que a ordem proíbe em l.216 e o que a bancada herdaria como fato.

## 6. Correção FINAL (texto exato)

**l.135, substituir** «R-LIN fecha em ~1 ano de O5 estatisticamente, mas é EXCLUDED_IF_UNIVERSAL na C1 e a mais penalizada no catálogo (ln B −8,22).»
**por:** «R-LIN atinge N₅₀ = 38–67 de mistura (SNR ×1,56–2,06; N₉₀ = 60–105) em **0,5–1,2 ano de O5 a 50 % de poder, 0,7–1,9 ano a 90 %** `[DERIVED, cenário: taxa 55–83 pSEOBNR/ano; o JSON da medição, `anos_O5_a_taxa_x4.6..5.7` [0,92; 1,21], usa taxa fixa — I6 do crítico — e a bancada refaz com a taxa de cada extremo]`, mas é EXCLUDED_IF_UNIVERSAL na C1 e a mais penalizada no catálogo (ln B −8,22).»

**l.139, substituir** «**~130 eventos com SNR_RD ≥ 50 (~1,3 ano a 10²/ano) ou ~33 com SNR_RD ≥ 100 (~3,3 anos)**»
**por:** «**N₅₀ ≈ 131 eventos com SNR_RD ≥ 50 ou ≈ 33 com SNR_RD ≥ 100 (na convenção desta ordem, N₉₀ ≈ 207 / 52; âncora σ = 0,058 em SNR_RD ~40, A-05)**; com as taxas [KNOWN] de ordem de grandeza (10²/ano, 10/ano) isso é ~1,3–2,1 / ~3,3–5,2 anos de 3G **como cenário [DERIVED], nunca como promessa (l.216)**».
