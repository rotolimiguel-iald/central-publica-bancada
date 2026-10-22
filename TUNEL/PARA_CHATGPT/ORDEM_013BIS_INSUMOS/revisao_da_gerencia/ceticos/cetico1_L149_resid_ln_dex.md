# CÉTICO 1 — ORDEM 013-bis, linha 149 (E0.3): «resíduo 0,24 dex»

**Veredito: achado NÃO refutado (refutado=false). Gravidade mantida: IMPORTANTE.**

## O que foi medido (script, não memória)
- `medir/B_catalogos/rendimento_e_5sigma.py:29` — `p,lnA=np.polyfit(np.log(S),np.log(G),1)`; `:33` — `resid=np.log(G)-(lnA+p*np.log(S))`; `:35` — `'log_resid_sd':float(resid.std())`. `np.log` é logaritmo NATURAL. A dispersão sai em nepers (ln), não em dex.
- `RENDIMENTO_E_5SIGMA.json` → `sigma_vs_snr_fit_31`: A = 3,02665, p = −0,85992, log_resid_sd = 0,24446 (ln).
- Refeito por script a partir dos 31 pares (SNR, σ) gravados no JSON (σ arredondado a 4 casas): A = 3,0249, p = −0,8597, sd_ln = 0,2444, **sd_dex = 0,1062** (= 0,2444/ln 10; ajuste direto em log10 dá o mesmo 0,10616).
- Limiares da linha 149 conferem: σ ≤ 0,06 → SNR = 95,6; σ ≤ 0,10 → SNR = 52,8 (a ordem diz «≳ 95» e «≳ 53» — corretos).
- `revisao/estatistica_poder/REFEITOS_REVISAO.json:180` `resid_0p244_e_ln_nao_dex` {ln 0,2445; dex 0,1062} — coerente com o meu refazer.

## Por que não se refuta
A palavra «dex» é uma unidade (log10). O número 0,24 é em ln. A frase erra a unidade por fator ln 10 = 2,303. Não é gosto: a bancada é mandada a «refazer o ajuste» (linha 149) e, se refizer em log10 (o usual em astronomia), encontra 0,106 dex e declara divergência falsa; se refizer em ln e copiar «dex», propaga a unidade errada ao registro pré-analítico (`PORTAO_DA_AMPLIACAO_V1.json`). Os limiares de SNR não dependem da unidade do resíduo, logo o erro não muda a física do corte — por isso IMPORTANTE, não BLOQUEANTE.

## Correção FINAL (substituir na linha 149, só o parêntese)
De: `σ ≈ 3,03·SNR_rede^−0,86 (resíduo 0,24 dex) [DERIVED]`
Para: `σ ≈ 3,03·SNR_rede^−0,86 (dispersão residual 0,24 em ln, ≙ 0,11 dex; A = 3,027, p = −0,860, 31 eventos) [DERIVED]`
