[REAL — ficha documental ORDEM015 §7; T02: PAGO]

# Reaproveitamento T02

## Artefato anterior efetivamente reutilizado

- `ORDEM_013_RINGDOWN/bis/e3_pilot_failure_diagnostic/DIAGNOSIS.json` — SHA-256 `3d02f43355301dab5a110c44fae48f569fe6f13aa84828703cf75da4b6f170d6`
- Uso: diagnóstico anterior confrontado com o replay nativo.

## O que foi novo

- Adendo nativo reproduziu a fronteira, a sequência com aborto no sorteio 16 e a regra de fmax; diagnóstico da falha entregue.

## Teste e verificação

- `ORDEM_013_RINGDOWN/bis/e3_pilot_failure_diagnostic/DIAGNOSIS_ADENDO_v2.json` — SHA-256 `54abbd376a6aae3baeab6f9f7d7bbd71942715ce33c41ec025e817b8cbf7c160`
- `TUNEL/DO_CHATGPT/ENTREGA_015_T02_diagnostico.md` — SHA-256 `98ab7df984ffe41261d39505f407f7165bf9168130a56f4aa7472fd98990b516`
- Medidas essenciais da matriz: {"cpu_seconds": 399.66127300000005, "pooled_EDOM_fraction": 0.0435, "registered_scan": {"CRASH": 37, "DOMAIN_RETURNED_NONE": 3, "FINITE": 80, "OTHER": 0}, "wall_seconds": 462.909858519}.

## Limite do reaproveitamento

- Mecanismo do heap é inferido da fonte; retLen/indAmax/Nrdwave não medidos. Nenhuma PE nova ou σ físico.

## Custo e axiomas

- [REAL] 462,909858519 s de parede e 399,661273 s CPU na reprodução; custo monetário não informado.
- Axiomas: N/A — sem Lean. Nenhuma ficha certifica compilação Lean ou move o gate.

## Fontes de controle

- Ordem oficial: `TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` — SHA-256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`
- Matriz T01–T13: `ORDEM_013_RINGDOWN/bis/015/closing_audit/T01_T13_CLOSING_AUDIT.json` — SHA-256 `f088f5819b3ac78da9d3b974f64d15def1f1eb4525ed0b65467e2e12f9be9caa`
- Orçamento v13: `ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json` — SHA-256 `eaa6412f8646b0f1d624341d5759fa2c1936da35436d8e0f9f53c6d2ad121b81`
