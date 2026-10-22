[REAL — ficha documental ORDEM015 §7; T05: PAGO]

# Reaproveitamento T05

## Artefato anterior efetivamente reutilizado

- `ORDEM_013_RINGDOWN/bis/e4_e5_prepare/runs/authorized_001/DETERMINISTIC_DIAGNOSTICS.json` — SHA-256 `a1e441ac0b16687d093d8590f70adae46acba100bee2c0923de17e687b88a55f`
- Uso: duas variantes determinísticas do 440 usadas no diagnóstico novo.

## O que foi novo

- Diagnóstico 440, duas variantes e pareamento QNM calculados; divergência do N90 da ordem corrigida pelo resultado reproduzível.

## Teste e verificação

- `ORDEM_013_RINGDOWN/bis/015/t05/RESULT.json` — SHA-256 `3d959ac7ce751bc69c7edac051bb774426930b6e183a6bc1567bd981d8b087d3`
- `TUNEL/DO_CHATGPT/ENTREGA_015_T05_440.md` — SHA-256 `5dd21bc79ec43e866e468d53c126d5f6b149adc983d2dea439805481c0c88ef6`
- Medidas essenciais da matriz: {"GW250114_440_draws": 40776, "O5_RB_N90_conditional": 2289.94, "paired_220_draws": 608681, "physical_N": null, "rho_440_effective_proxy": 1.763035274139}.

## Limite do reaproveitamento

- ρ440 é proxy Fisher dominado pelo prior, não SNR físico; N90 condicional a fontes idênticas e sem sistemática. Nenhum σ físico.

## Custo e axiomas

- [REAL] diagnóstico leve; horas de máquina pesada não debitadas no v13; custo monetário não informado.
- Axiomas: N/A — sem Lean. Nenhuma ficha certifica compilação Lean ou move o gate.

## Fontes de controle

- Ordem oficial: `TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` — SHA-256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`
- Matriz T01–T13: `ORDEM_013_RINGDOWN/bis/015/closing_audit/T01_T13_CLOSING_AUDIT.json` — SHA-256 `f088f5819b3ac78da9d3b974f64d15def1f1eb4525ed0b65467e2e12f9be9caa`
- Orçamento v13: `ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json` — SHA-256 `eaa6412f8646b0f1d624341d5759fa2c1936da35436d8e0f9f53c6d2ad121b81`
