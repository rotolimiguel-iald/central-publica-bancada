# RECIBO v366 — a V3 do D1 com dado real

17/09/2026 13:54 · da gerência (Claude, Central de Patentes) para a bancada. `um.py` v366 `3829685999814e3f` (rodada COMPLETA; 5679/5679; gate intocado).

## A linha e a execução

O operador ratificou a leitura da rota do fundo que vocês traduziram em 15/09: «é a primeira, rode» — Φ_tot = 1 + β|1 + w_ef| sobre o fluido total, com o vácuo (o zero modular) dentro da composição. Antes, na mesma tarde, ele distinguiu: «vácuo não é nada, vácuo é o zero modular». A tranca abriu; o protocolo V3 (`d5c35ea6d20b76eb`) rodou UMA vez, fora do cache lido pelo rito da v365, no instrumento da validação (camb 2.0.4, scipy 1.18.1, numpy 2.5.3, python 3.12.3, emcee 3.1.6). A primeira execução, num interpretador sem camb, morreu antes de qualquer número e está preservada por hash.

## O resultado (resultado sha16 `f048b17f12674f33`; a matriz da V2 recalculada no programa de forma independente)

- Fase 1 (β fixo = α√e contra ΛCDM; Planck comprimido + DESI DR1; n = 15): Δχ² = +6.614 (χ²_ΛCDM = 16.681; com SH0ES +6.168) → `D1_TENSION_2_TO_5_SIGMA`.
- Fase 2: H0 67.95 (ΛCDM) / 68.00 (TGL); tensão com SH0ES 4.89σ / 4.85σ — não aliviada.
- Fase 3 (cega): β = -0.01275 (+0.00795 / −0.00850); α√e a 3.01σ; β = 0 a 1.55σ → `D1_BETA_TENSION`.
- Veredito no programa: `TGL_D1_CAMB_V3_REAL__OPERATOR_LINE_RATIFIED__BESTFIT_D1_TENSION_2_TO_5_SIGMA__MCMC_D1_BETA_TENSION__ALPHA_SQRT_E_AT_3P01_SIGMA_AT_THRESHOLD__CHAIN_BELOW_50_TAU_IN_2_OF_4_PARAMS__TENSION_IS_NOT_FALSIFICATION__GATE_UNTOUCHED`.

**Ressalvas ditas junto:** o desvio está no limiar de 3σ da matriz (a fronteira TENSION/INCONCLUSIVE cabe no ruído de Monte Carlo); o emcee avisou cadeia < 50τ em 2 de 4 parâmetros; Planck comprimido; DESI DR1. Nada foi rerodado nem afrouxado. Tensão, não falsificação (a matriz exige 5σ). A V2 (v349) tinha Δχ² 9.70 e o mesmo desfecho MCMC.

## No programa

`prove_d1_camb_v3_real_v366` relê os seis arquivos da rodada (texto e sha256 embutidos), confere protocolo, linha, scripts e instrumento, e recalcula a matriz. Errata ao lado na função da v364: a checagem da tranca aceita a tranca aberta de forma válida (`_d1_v3_lock_opened_validly`).

## O que a gerência não fez

Nenhuma bandeira do gate mudou; cosmologia jamais vira prova matemática. Nada foi escrito nas pastas de vocês além deste recibo. Nenhuma custódia pública. PROVADA ≠ CONFIRMADA.
