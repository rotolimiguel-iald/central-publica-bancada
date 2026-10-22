# CÉTICO 2 — achado estatistica_poder A-03, ORDEM 013-bis l.149 (E0.3): o corte SNR_rede ≳ 95 exclui o GW250114 e zera a contagem

**Veredito: refutado = false (achado CONFIRMADO por refeito). Gravidade: IMPORTANTE (mantida).**

## Refeito por script (22/09/2026; fonte: `medir/B_catalogos/RENDIMENTO_E_5SIGMA.json` → `sigma_vs_snr_fit_31.events`, 31 pares (SNR_rede da Tabela 2 GWTC-5.0 TGR / Tabela 1 GWTC-4.0 TGR III; σ = (q95−q05)/3,29 da marginal de δτ̂₂₂₀); OLS em ln–ln, como `rendimento_e_5sigma.py:29`)
- Ajuste: A = 3,025, p = −0,860, sd do resíduo em **ln** = 0,244 (ddof 0) / 0,249 (ddof 1). Confere com a gerência (3,03·SNR^−0,86; 0,24) e com `REFEITOS_REVISAO.json`.
- σ_fit(SNR): 53 → 0,0996 · 76,9 → 0,0723 · 78,6 → 0,0710 · 95 → 0,0603. SNR(σ=0,06) = 95,6; SNR(σ=0,10) = 52,8.
- GW250114: SNR_rede 76,9 (Tabela 2 TGR) / **78,6 no GWOSC** (`gwosc_catalogs_raw.json`, o «1 acima de 78» da ordem É o GW250114); σ real 0,058; resíduo ln = −0,221 = −0,90 sd. **Fica abaixo do corte 95 nas duas convenções de SNR.**
- Sem o GW250114 o ajuste vira A = 2,12, p = −0,735 → SNR(σ=0,06) = 127: a âncora é o ponto de maior alavanca; o corte a 95 depende dela e ainda assim a exclui.
- Fração esperada (lognormal com sd 0,244; o ajuste é a mediana): P(σ ≤ 0,06 | SNR=53) = 0,02; | 76,9 = 0,22; | 78,6 = 0,25; | 95 = 0,49. P(σ ≤ 0,10 | 53) = 0,51; | 76,9 = 0,91; | 95 = 0,98.
- Contagens nos 31 do ajuste: σ ≤ 0,06 → 1; SNR ≥ 95 → **0**; SNR ≥ 75 → 1; SNR ≥ 50 → 1. GWOSC GWTC-5.0 (`MEDICAO_E.json`): SNR ≥ 30 → 5; máx 78,6 → **≥ 95 → 0**. O4 Discovery Papers: GW250207_115645 com 68,91 (fora do GWTC-5.0).

## Por que o achado está certo
A ordem define «GW250114-like» por σ = 0,058 (l.125) / σ ≤ 0,06 (SINTESE l.72), manda registrar N_alvo por essa população (l.148) e a sua taxa com IC90 de Poisson (l.135, l.153: «1 em 1,45 ano»), e ao mesmo tempo (l.149) manda que o critério registrado seja PRÉ-ANÁLISE e traduz σ ≤ 0,06 em SNR_rede ≳ 95. Pelo critério pré-análise a contagem em O4 é zero (nem o GW250114 passa), o que contradiz a taxa e torna o N_alvo «212 GW250114-like» vazio por definição. A ordem não diz (i) que o ajuste é a mediana (em SNR 95 só ~49 % dos eventos terão σ ≤ 0,06), (ii) em qual corte a bancada conta a taxa, (iii) qual SNR_rede (Tabela TGR 76,9 vs GWOSC 78,6) — três ambiguidades que a bancada pode explorar (registrar taxa 0, ou escolher o corte que convém). Não é BLOQUEANTE porque a ordem já manda refazer e contar (executável) e não decide nada do operador; é IMPORTANTE por inconsistência interna e ambiguidade explorável.

## Nota lateral (para o outro cético, não duplico): «0,24 dex» é 0,244 em ln (cetico1_L149_resid_ln_dex.md); a correção abaixo já diz «em ln».
