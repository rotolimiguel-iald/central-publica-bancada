# CÉTICO 2 — achado «N₉₀ ≈ 3.250 de mistura O4» (ORDEM 013-bis, linha 125, §4.0 (b))

Veredito: **NÃO refutado** (refutado=false). Gravidade mantida: IMPORTANTE (inconsistência interna de número, a bancada é mandada refazer e vai medir a diferença).

## Medido por script (python, fator = (5+1,28)²/25 = 1,577536)
| base N₅₀ (R-B, mistura O4) | fonte | N₉₀ = base × 1,5775 |
|---|---|---|
| 2.062 | CRITICO.md:31,48,62 (refeito do arquivo da bancada, 31 eventos) | **3.252,9** |
| 2.100 | SINTESE.md:137,155 («~2.100», arredondamento da banda) | **3.312,8** |
| 2.108 | A_poder_eventos/A2_tabela_5sigma.csv:8; A_poder_eventos.json:36 (2108,04; união 39) | **3.325,4** |
| 212 | GW250114-like | 334,4 → «335» ok |

## O que a linha 125 imprime
- N₅₀ de mistura: «**≈ 2.100** · 669 · 618 · 166» (gerência) + «(o crítico … 2.062 / 657 / 605 / 163)».
- N₉₀: «R-B **335** GW250114-like ou **≈ 3.250** de mistura O4».
- «≈ 3.250» só sai de 2.062 (3.253 — CRITICO.md:62 «2.062 → 3.254»); de «≈ 2.100» sai 3.313; da base A (2.108) sai 3.325. O N₉₀ impresso usa a base do crítico enquanto o N₅₀ de manchete usa o arredondamento da gerência. Não é gosto: é aritmética que a bancada, obrigada a refazer, vai apanhar.

## Ajuste à correção proposta pelo revisor
A proposta escreve «2.062–2.100». A banda medida pela gerência é **2.062–2.108** (SINTESE.md:137: «2.062–2.108 = mistura real do catálogo (B usa mean z²/evento 0,0121; A usa z_comb 0,606 — diferença 2 %)»); 2.100 é o arredondamento, não um extremo. O extremo superior de N₉₀ é portanto 3.325, não 3.310.

## Correção FINAL (texto exato para a linha 125, substituindo só o trecho após «N₉₀ = 1,578 × N₅₀» ((5 + 1,28)²/25))
«— R-B **335** GW250114-like ou **≈ 3.250–3.330** de mistura O4 (2.062–2.108 × 1,578, conforme a base: crítico/31 ou A/união-39; a bancada fixa a base pela população que declarar); as outras leituras pela mesma razão (a bancada calcula e registra).»
