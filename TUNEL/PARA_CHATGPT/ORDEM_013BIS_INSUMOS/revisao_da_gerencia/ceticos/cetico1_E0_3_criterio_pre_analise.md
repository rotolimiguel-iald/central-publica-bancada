# CÉTICO 1 — achado «E0.3: o corte SNR ≳ 95 exclui o próprio GW250114» (ORDEM 013-bis, l.149)

**Veredito: NÃO REFUTADO (refutado=false). Gravidade mantida: IMPORTANTE.**

## O que refiz por script (`cetico1_E0_3_refeito_stdout.txt`, nesta pasta)

Fonte dos 31 pares (SNR_rede, σ): `medir/B_catalogos/RENDIMENTO_E_5SIGMA.json` → `sigma_vs_snr_fit_31.events`.
Fonte da contagem GWOSC: `medir/E_instrumento/gwosc_catalogs_raw.json` (coluna 2 = SNR de rede).

| item | ordem / revisor | refeito |
|---|---|---|
| ajuste ln σ = ln A + p ln SNR | A = 3,03; p = −0,86 | A = 3,025; p = −0,860 |
| dispersão do resíduo | «0,24 dex» (l.149) | **0,244 em ln** (ddof=0) = 0,106 dex — a ordem erra a unidade; `REFEITOS_REVISAO.json:resid_0p244_e_ln_nao_dex` já o registra |
| σ_fit(76,9) / (78,6) / (95) | 0,0723 / 0,0710 / 0,0603 | 0,0723 / 0,0710 / 0,0603 |
| SNR para σ = 0,06 / 0,10 | 95,5 / 52,7 | 95,6 / 52,8 |
| resíduo do GW250114 | −0,22 em ln | −0,221 em ln = −0,87 sd (dentro da dispersão) |
| P(σ ≤ 0,06 \| SNR) sob lognormal sd 0,244 | — | SNR 53: 0,02 · 76,9: 0,23 · **95: 0,49** · 120: 0,78 · 150: 0,94 |
| GWTC-5.0: SNR ≥ 30 / 50 / 75 / 95 | 5 / — / 1 / — | **5 / 1 / 1 / 0**; máx 78,6 (GW250114) |
| GWTC-4.0/4.1: ≥ 50 | — | 0 (máx 43,0) |
| O4 Discovery Papers: ≥ 50 / ≥ 75 | — | 1 (GW250207_115645, 68,91) / 0 |

## Por que o achado se sustenta

1. A reta é a **mediana** condicional: em SNR_rede = 95 só ~49 % dos eventos teriam σ ≤ 0,06; o critério «σ ≤ 0,06 ≙ SNR ≳ 95» é uma correspondência de medianas, não um corte que garante a classe. A ordem não diz isso.
2. O corte a 95 **zera** a contagem de «GW250114-like» em todo catálogo público (GWTC-4.0/4.1/5.0: 0 eventos ≥ 95), e exclui o próprio evento-âncora (78,6 em GWOSC; 76,9 na tabela da bancada). Isto contradiz a l.135 («UMA contagem: 1 em 1,45 ano de O4; IC90 [0,035; 3,3]/ano») e torna N_alvo = 212/335 «GW250114-like» (l.125, E0.2) uma população vazia por definição pré-análise.
3. A ordem manda «contar quantos passam cada corte» sem fixar **qual corte define a população de N_alvo** — a bancada pode escolher 53, 95 ou o σ pós-análise, e cada escolha muda N_alvo por fator > 3. É a ambiguidade que a pré-registração existe para fechar.

## Inconsistência lateral (nota, mesma linha)

- SNR_rede do GW250114: **76,9** no ajuste da bancada (`sigma_vs_snr_fit_31`) vs **78,6** em GWOSC (GWTC-5.0). A ordem cita «1 acima de 78» com base no GWOSC e σ(76,9) com base na tabela — a bancada deve declarar qual SNR usa (GWOSC vs tabela TGR) e refazer o ajuste com uma só convenção.
- «resíduo 0,24 dex» → «resíduo 0,244 em ln (0,106 dex)».

## Não é BLOQUEANTE porque

A linha já manda a bancada **refazer e contar** (não copia número), e o erro é de definição/ambiguidade, não de física nem de régua; corrigido o texto, nada mais na Parte B muda de número. Mas publicada como está, a bancada receberia como fato um critério que exclui a âncora — por isso IMPORTANTE, não NOTA.

## Correção FINAL (substitui o item 3 da E0, l.149)

Ver o campo `correcao_ajustada` do StructuredOutput (texto idêntico).
