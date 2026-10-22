[REAL — ficha documental ORDEM015 §7; T12: PAGO]

# Reaproveitamento T12

## Artefato anterior efetivamente reutilizado

- `ORDEM_013_RINGDOWN/bis/e7_prepare/FREEZE_E7_V4.json` — SHA-256 `29b4776078f4be7c0e0dd721d2fa25e319f4cc5d273fca6d4719a7ac2953f2d0`
- Uso: produtor E7 congelado usado como referência para a variante com guarda.

## O que foi novo

- Variante E7 com fórmulas idênticas, 72 testes da variante, replay rc0 e subemenda V1.1.1 anterior ao uso; falha de ativação corrigida em V1.1.2.

## Teste e verificação

- `ORDEM_013_RINGDOWN/bis/e7_prepare_v1_1/RESULT.json` — SHA-256 `462c66dbc21efed2a7f9dadea5c990c32fea743fa1bf678d3f2f6762b44a523f`
- `ORDEM_013_RINGDOWN/bis/e7_prepare_v1_1/RITE_REPLAY_RESULT.json` — SHA-256 `9834bf3c799dedf29efda5d9554051dbc69cd2f3888561f404e64c8a1cafdc94`
- `ORDEM_013_RINGDOWN/bis/015/activation_v2/REGISTERED_RESULT.json` — SHA-256 `aa33411d85b05f40f235ab3a6fd34fbb975ca544ab8dce19388a7effeb168a32`
- Medidas essenciais da matriz: {"blind_tests": 0, "calibration_events": 33, "max_abs_delta_T05": 6.938893903907228e-17, "paired_220_rows": 330, "variant_tests": 72}.

## Limite do reaproveitamento

- Entrega do preparador/rito, sem eventos cegos, lnB ou z físico; replay não ativa campanha nem incorpora código em um.py.

## Custo e axiomas

- [REAL] 0 h de máquina pesada e 0 custos externos novos declarados; custo de revisão da coordenação não medido.
- Axiomas: N/A — sem Lean. Nenhuma ficha certifica compilação Lean ou move o gate.

## Fontes de controle

- Ordem oficial: `TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` — SHA-256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`
- Matriz T01–T13: `ORDEM_013_RINGDOWN/bis/015/closing_audit/T01_T13_CLOSING_AUDIT.json` — SHA-256 `f088f5819b3ac78da9d3b974f64d15def1f1eb4525ed0b65467e2e12f9be9caa`
- Orçamento v13: `ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json` — SHA-256 `eaa6412f8646b0f1d624341d5759fa2c1936da35436d8e0f9f53c6d2ad121b81`
