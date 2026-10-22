# CÉTICO 2 — achado «0,062 sem rastro» (ORDEM 013-bis, linha 133, §4.0 (f))

**Veredito: NÃO refutado (refutado=false). Gravidade mantida: IMPORTANTE.**

## O que medi (por script, 22/09/2026)

1. `medir/S_sintese/reconcilia.py:147` — `'QNM_sum_max': 0.062` é literal digitado; nenhum cálculo o produz.
   `medir/SINTESE.md:126/142/186` e `escrever_sintese.py:150` repetem o literal (fonte declarada: C5_BIAS_ABLATION 6fd926f371e38aa7; RECOLORED 0825d9e83c571554).
2. `medir/C_piso_sistematico/C_piso_medicoes.json`, `C_modelo_QNM_220_440_vs_FULL_IMR_por_t0_RB` (gerado por `s02_measure.py:99-114` a partir de `C5_BIAS_ABLATION.json`, fit 220_PLUS_440, content FULL_IMR, dtau = â·|δ_RB|):
   t0 6: SEOB −0,0501 / Phenom −0,0375 / média −0,0438 · 8: −0,0558 / −0,0537 / −0,0548 · 10: −0,0111 / −0,0140 / −0,0125 · 10,5: −0,0126 / −0,0104 / −0,0115 · 12: −0,0422 / −0,0256 / −0,0339 · 20: −0,0339 / −0,0024 / −0,0182.
   `H_piso_por_leitura.R-B.componentes.modelo_QNM_vs_IMR_span_6M_12M` = {min 0,01148, max 0,05479}. **Nenhum 0,062.** O máximo absoluto em qualquer t0 ≤ 20 t_M é 0,0558 (SEOB @ 8 t_M).
3. Bancada (só leitura) `C5_BIAS_ABLATION.json` (sha16 6fd926f371e38aa7 conferido): únicos valores em 0,055–0,07 são `a_hat` 0,0639 e −0,0678 (células 22_PLUS_44, em unidades de â; × δ_RB = ±0,0013 em δτ̂) e `residual_norm_squared` ~0,057. **Nenhum δτ̂ de 0,06x.**
4. Bancada `C5_RECOLORED_FORECAST.json` (sha16 0825d9e83c571554 conferido): valores em 0,055–0,07 são `absolute_bias` 0,0565 / 0,0635 / 0,0562 (results 42, 44, 134) — **viés do estimador COM ruído (N = 50 draws), em unidades de â, em células MATCHED_RINGDOWN** (SNR 10/40). Não é «soma-de-QNM vs IMR», não é δτ̂ e não é modo comum. Provável origem do literal 0,062 por leitura errada de unidade.
5. Sinal: `C_piso_medicoes.json` dá dtau_SEOB(10) = −0,01111; `C_piso_sinais_catalogo.json` (`s03_sinais_e_catalogo.py:13`, δτ̂ = â·eff com eff < 0) dá +0,01111. **Mesma grandeza, sinais opostos nos dois JSON.** A frase da ordem «mesmo sinal nas duas famílias, o sinal do +0,07 da LVK» só é verdadeira na convenção δτ̂_equiv = â·δ_RB (δ_RB = −0,0198; â < 0 nas duas famílias em 6–12 t_M ⟹ δτ̂ > 0). A ordem não a declara (grep «convenç», «â·δ»: linhas 32, 147, 172 — nenhuma sobre este sinal).
6. Razões recalculadas com piso R-B 0,003969: 0,01148 → 2,89×; 0,01254 → 3,16×; 0,05479 → 13,8×; 0,062 → 15,6×. A «3,2–16×» está só em SINTESE.md, não na linha 133 da ordem — a ordem herda apenas o span errado.

## Por que não é BLOQUEANTE
A conclusão de (f) não muda: a componente fica 2,9–13,8× acima do piso do R-B, «vermelha» em qualquer versão. Mas a ordem será imutável, o número 0,062 não existe em artefato nenhum, e a convenção de sinal que sustenta «mesmo sinal» está ausente — a bancada pode contestar os dois com razão.

## Correção final (substituir na linha 133 o trecho exato)
ANTES: `soma-de-QNM (220+440 @10 t_M) vs IMR: +0,0125 a +0,062 (mesmo sinal nas duas famílias, o sinal do +0,07 da LVK)`
DEPOIS: `soma-de-QNM (220+440) vs IMR completo, sem ruído: +0,0125 a 10 t_M (média das famílias; SEOB +0,0111, Phenom +0,0140), span +0,011 a +0,055 entre 6 e 12 t_M (2,9–13,8× o piso do R-B), na convenção δτ̂_equiv = â·δ_RB com δ_RB = −0,0198 (â < 0 nas duas famílias ⟹ sinal positivo, o sinal do +0,07 da LVK; C5_BIAS_ABLATION 6fd926f371e38aa7, células FULL_IMR × 220_PLUS_440)`
E em `reconcilia.py:147` / `reconciliacao.json:324` / `SINTESE.md:126,142,186`: 0,062 → 0,0548 (razão 3,2–16× → 2,9–13,8×; «1,1–6,2 %» → «1,1–5,5 %»), correção AO LADO.
