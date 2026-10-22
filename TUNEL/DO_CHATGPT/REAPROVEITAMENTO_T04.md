[REAL — ficha documental ORDEM015 §7; T04: PARCIAL]

# Reaproveitamento T04

## Artefato anterior efetivamente reutilizado

- `ORDEM_013_RINGDOWN/bis/E3_PILOT_FAILURE_AUDIT_V1.json` — SHA-256 `2611d2d895d37645ab95de662ef126960292d1f6ca0a832a06ec515bdf5596c1`
- Uso: falha do piloto inicial usada como referência para a qualificação e os novos ramos.

## O que foi novo

- Adaptador qualificado e pilotos executados. Ramo F gerou posterior diagnóstico descritivo com rc0.

## Teste e verificação

- `ORDEM_013_RINGDOWN/bis/015/t04/QUALIFICATION_DELIVERY.json` — SHA-256 `13ce85290d91466cf6273e7fb3806a4edb8daf6cd64510949e78964282de5492`
- `ORDEM_013_RINGDOWN/bis/015/t04/pilot/RESULT.json` — SHA-256 `920e9f4de574b24ebfd9b1bb309338e7259c09a9ea0ee4c0f058dd625141b3ae`
- `ORDEM_013_RINGDOWN/bis/015/t04/branch_c/RESULT.json` — SHA-256 `9663242560623d92e933bdab82ca176022f6b3606ee285aceea6c8a9eecaea36`
- `ORDEM_013_RINGDOWN/bis/015/t04/branch_h/RESULT.json` — SHA-256 `d8565e08f755262b0cdbbe5c3c1fc2a9901343d51dc8740ca16947c00ca321b3`
- `ORDEM_013_RINGDOWN/bis/015/t04/branch_f/RESULT.json` — SHA-256 `3ed4951d27fb27d8b17a9443a93eed39b8c0a6d53263e0d4cd66f5b2e3c7e7c8`
- Medidas essenciais da matriz: {"branch_C_ESS": 1.0000000000004259, "branch_C_delta_logz": 425.33480044518365, "branch_F_ESS": 3051.7756961962286, "branch_F_delta_logz": 0.09997822135365081, "branch_F_posterior_samples": 2058, "branch_F_sigma_eligible": false, "pSEOB_pilot_posterior_accepted": false, "runner_qualified": true}.

## Limite do reaproveitamento

- Piloto pSEOB e ramo C pararam sem posterior aceito; H foi interrompido. F não identifica sozinho Mf/af/dτ220 e não entra em σ; custo por posterior científico convergido segue aberto.

## Custo e axiomas

- [REAL] 10.410584105 h contabilizadas nos ramos T04; custo de posterior científico aceito permanece aberto.
- Axiomas: N/A — sem Lean. Nenhuma ficha certifica compilação Lean ou move o gate.

## Fontes de controle

- Ordem oficial: `TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` — SHA-256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`
- Matriz T01–T13: `ORDEM_013_RINGDOWN/bis/015/closing_audit/T01_T13_CLOSING_AUDIT.json` — SHA-256 `f088f5819b3ac78da9d3b974f64d15def1f1eb4525ed0b65467e2e12f9be9caa`
- Orçamento v13: `ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json` — SHA-256 `eaa6412f8646b0f1d624341d5759fa2c1936da35436d8e0f9f53c6d2ad121b81`
