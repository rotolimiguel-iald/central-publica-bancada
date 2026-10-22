[REAL — fechamento somente de F4-R1/F4-R2; sem mudança de gate]

# Fechamento dos achados F4

2026-09-22T18:03:21.036814+00:00. **APROVADOS os dois achados nomeados.** Não restou bloqueante de F4-R1/R2 nas versões examinadas. Esta aprovação não abrange toda F4, a calibração física nem novos artefatos F2.

F4-R1: `C5_FISHER_v3.json` recalcula cada linha de `same_source_R_B` usando a referência única PSD/R-B/SNR40/FREQUENCY_FREE_TAU_GR_FIXED. Recalculei independentemente `log1p(x)/sigma × snr_ratio_to_O4`, média z²/2 e desvio-padrão z. As quatro linhas conferem. A tabela antiga foi preservada integralmente em `same_source_R_B_linear_historical`; todos os 384 records permanecem iguais à v2. A convenção pontual está explícita.

| PSD | z e desvio-padrão corretos | média lnB correta |
|---|---:|---:|
| O4 | 0.400717975961 | 0.0802874481289 |
| O5 | 0.794772113532 | 0.315831356224 |
| ET | 3.81699745878 | 7.28473480016 |
| CE | 6.95726884705 | 24.2017949051 |

F4-R2: `PORTAO_DO_PODER_013_v2.json` conserva os 16 valores de controle e acrescenta rho_used, rho_kind e scope com o significado pedido: cenários separados de forma de PSD, normalizados ao mesmo rho de rede; não são z medidos por detector nem Fisher combinado da rede. Bases, 50 readings e vereditos permanecem inalterados.

Os hashes de supersedes, builder e parecer anterior conferem. O ponteiro current_fisher identifica v3; a dependência histórica congelada continua íntegra. O builder foi lido, não executado/importado. Insumos antigos e novos permaneceram intactos durante os controles. A lista de mudanças estruturais foi comparada com a lista autorizada; nenhuma diferença inesperada.

Mantém-se a conclusão anterior: maior z condicional 0,713209021511; INCONCLUSIVE_SYSTEMATICS e FAILED_TWO_FAMILY_CALIBRATION. Nenhuma PE, injeção ou execução de um.py. Axiomas: N/A — sem Lean.

Reprodução: Python bundled, `-B -O bis/c1_review/close_f4_findings.py`, a partir de uma cópia isolada preservando a estrutura relativa, pois as saídas recusam sobrescrita. Evidência: `bis/c1_review/f4_closing_results.json`; SHA256 `aa7d18458edde146c711974ebf6629b12aed165c79843a3e322d7c7540a8c94a`. Script SHA256 `75e8134e53076f4420c3c84f9f6f2dc79724bed4f0b5ddb4c274f119c2c42381`.

| Arquivo (relativo a ORDEM_013_RINGDOWN) | SHA256 lido |
|---|---|
| `C5_FISHER_v2.json` | `ac36fe7eb92d6b315a368ba8ea43ee09ad2d52e4456a0c9bfc61ae06bffb5b6f` |
| `C5_FISHER_v3.json` | `ef7a800369ba07328852b2ffe6a54c13f9b20476775f557113ca31fc50a5a22b` |
| `PORTAO_DO_PODER_013.json` | `ec5e012bc40a3e005bc83533b4b5dab4af0d221c86ee92aa521a96b3f067cab0` |
| `PORTAO_DO_PODER_013_v2.json` | `c2972e3cc32286532908875b2a3ddb5d168d0669a6846e3e2c1d16e855c2b133` |
| `refeito/correct_f4_review_013bis.py` | `e230fb2fde0175d100f0162c13753eac51f54e929f61294992d1a7841285027f` |
| `bis/F4_POWER_GATE_REVIEW.md` | `35b02b3d0a4d45ecfbacc156f73c909eeab10f9e12bf07a6ca169b37b6d4d914` |
