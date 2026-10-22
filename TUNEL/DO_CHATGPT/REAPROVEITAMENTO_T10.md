[REAL — ficha documental ORDEM015 §7; T10: PARCIAL]

# Reaproveitamento T10

## Artefato anterior efetivamente reutilizado

- `ORDEM_013_RINGDOWN/C5_FISHER_v3.json` — SHA-256 `ef7a800369ba07328852b2ffe6a54c13f9b20476775f557113ca31fc50a5a22b`
- Uso: diagnóstico anterior da não identificabilidade com um único modo.

## O que foi novo

- Alternativas A/B/C medidas em escopo diagnóstico; banco sintético de 10 células gerado e custos por comando registrados.

## Teste e verificação

- `ORDEM_013_RINGDOWN/bis/015/t10/T10_FINAL_RESULT.json` — SHA-256 `689806ca4917868b066f8b5ffd0dcd9df5aad2470cef3c341adc18b010c72fce`
- `ORDEM_013_RINGDOWN/bis/015/t10/T10_A_FINAL_RESULT.json` — SHA-256 `b7608f8932478fab48cf945c59e73542780c6e55f46e19d707ba7b93ab53613b`
- `ORDEM_013_RINGDOWN/bis/015/t10/T10_C_BANK_RESULT_v4.json` — SHA-256 `05eb55665a1f8134bc88ca4a6361dd198e28b0c8db4ed0d52fe5396352c04216`
- Medidas essenciais da matriz: {"A_width_ratio": 2.0347237587829947, "C_SNR_bins": [19.1, 17.0, 15.0, 13.0, 12.0], "C_bank_cells": 10, "D_transfer_forecast_hours": [12.820179289752778, 19.23026893462917], "sigma_c": null, "sigma_injection_ensemble": null}.

## Limite do reaproveitamento

- Sem covariância real qualificada, recuperação do banco, transferência pSEOB ou σ(c) por leitura. Previsão D não é execução.

## Custo e axiomas

- [REAL] 0.201669556 h de máquina; transferência D de 12,820–19,230 h é previsão, não execução.
- Axiomas: N/A — sem Lean. Nenhuma ficha certifica compilação Lean ou move o gate.

## Fontes de controle

- Ordem oficial: `TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` — SHA-256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`
- Matriz T01–T13: `ORDEM_013_RINGDOWN/bis/015/closing_audit/T01_T13_CLOSING_AUDIT.json` — SHA-256 `f088f5819b3ac78da9d3b974f64d15def1f1eb4525ed0b65467e2e12f9be9caa`
- Orçamento v13: `ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json` — SHA-256 `eaa6412f8646b0f1d624341d5759fa2c1936da35436d8e0f9f53c6d2ad121b81`
