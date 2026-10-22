# CÉTICO 1 — achado «0,062 sem rastro / sinal por convenção» (ORDEM 013-bis, linha 133, §4.0 (f))

Veredito: NÃO REFUTADO. Gravidade mantida: IMPORTANTE.

## O que medi (por script, 22/09/2026)
- reconcilia.py:147: `'QNM_sum_max': 0.062` é literal digitado; nenhuma chave do S_sintese o calcula.
- C_piso_medicoes.json `H_piso_por_leitura.*.componentes.modelo_QNM_vs_IMR_span_6M_12M` = {min 0,011482; max 0,054785}; `..._10M_media_familias` = 0,012536.
- C5_BIAS_ABLATION.json da bancada (sha16 6fd926f371e38aa7, 35.276 bytes; 108 células, só `a_hat`, sem δτ̂): células FULL_IMR × 220_PLUS_440 em 6–12 t_M, convertidas por â·δ_RB (δ_RB = −0,019845, mediana posterior GW250114, C_piso_medicoes `efeito_delta_tau_hat_GW250114_mediana_posterior`):
  SEOB 6/8/10/10,5/12 t_M = +0,0501/+0,0558/+0,0111/+0,0126/+0,0422; Phenom = +0,0375/+0,0537/+0,0140/+0,0104/+0,0256.
  Máximo POR FAMÍLIA = 0,0558 (SEOB @8 t_M); média das famílias: span 0,0115–0,0548. Nenhuma conversão produz 0,062.
  Único valor em [0,0595; 0,0645] no arquivo: `results[38].a_hat = 0,0639` (um â, não um δτ̂).
- Razões refeitas (piso = |δ|/5 por leitura): R-B 2,89–13,8× (com 0,062: 3,15–15,6×); R-MOD 1,56–7,44×; R-RAIZ-0 1,55–7,39×; R-LIN 0,80–3,83×.
- Sinal: s02_measure.py:102 usa `d_RB = abs(eff["R-B"])` → JSON de medições dá dtau NEGATIVO (−0,0111 @10 t_M); s03 usa `eff` assinado (−0,01985) → JSON de sinais dá +0,0111. Os dois JSON discordam de sinal na mesma grandeza. Os â FULL_IMR 220+440 são todos negativos em 6–12 t_M (10/10), logo «mesmo sinal nas duas famílias» é verdadeiro em qualquer convenção; o «+» que casa com o +0,07 da LVK só existe na convenção δτ̂_equiv = â·δ_RB (â<0, δ_RB<0), que a ordem não declara.
- Origem provável do «0,062» [CONJECTURE]: transcrição de |−0,0617| (`D_t0_LVK_release...` 220+221 @12 t_M vs 10 t_M, C_piso_medicoes.json:6075) ou do «6,2 %» da SINTESE.md:118 — linha de t₀, não de soma-de-QNM.

## Impacto na ordem
- Linha 133: só o «+0,062». A ordem NÃO cita a razão «3,2–16×» (está só na SINTESE.md:126/:51); a linha 135 «1,7–13×» usa o 10 t_M (0,0125/0,0074 = 1,70) e o 0,097 das outras fontes — não herda o erro.
- Conclusão física de (f) («condição vermelha para todas as leituras») NÃO muda: 0,0548 ainda é 13,8× o piso do R-B. Por isso IMPORTANTE, não BLOQUEANTE.

## Correção FINAL (substituir na linha 133 o trecho entre «soma-de-QNM» e «LVK);»)
«soma-de-QNM (220+440) vs IMR completo: +0,0125 a 10 t_M (média das famílias; SEOB +0,0111, Phenom +0,0140), span +0,011 a +0,055 entre 6 e 12 t_M (2,9–13,8× o piso do R-B; máximo por família +0,056, SEOB @8 t_M) — convenção declarada: δτ̂_equiv = â·δ_RB, com â do C5_BIAS_ABLATION (sha16 `6fd926f371e38aa7`) e δ_RB = −0,0198 (mediana GW250114); os â são negativos nas duas famílias em todo t₀ ∈ [6, 12] t_M, logo δτ̂_equiv > 0 nas duas — o sinal do +0,07 da LVK);»
