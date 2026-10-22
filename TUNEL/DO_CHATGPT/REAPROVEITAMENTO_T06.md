[REAL — ficha documental ORDEM015 §7; T06: PAGO]

# Reaproveitamento T06

## Artefato anterior efetivamente reutilizado

- `ORDEM_013_RINGDOWN/bis/E7_FINAL_EXECUTION_V1.json` — SHA-256 `035212e25370f7d7c780c4a2e1f4a5732785d83b55e60417e8c5ee9ea31f10c9`
- Uso: recibo histórico dos posteriores de calibração empregados na rota IV.

## O que foi novo

- Rota IV diagnóstica não cega executada sobre 33 posteriores com dois perfis e jackknife.

## Teste e verificação

- `ORDEM_013_RINGDOWN/bis/015/t06/RESULT.json` — SHA-256 `ed606fd444bc94b7e8a5c2b3c85aba7b305bf7a8c90a3df8de8b390f28e3d0d3`
- `ORDEM_013_RINGDOWN/bis/015/t06/AUDIT.json` — SHA-256 `106fe25b98366db3cffc6c6b29bd14583b5dee1dc6e282c389ee75b428c07694`
- Medidas essenciais da matriz: {"Gaussian_LRT": 0, "Gaussian_nominal_profile_limit": 0.023328574, "KDE_LRT": 0, "KDE_nominal_profile_limit": 0.023188691, "events": 33, "physical_sigma_jitter": null}.

## Limite do reaproveitamento

- Limites são níveis nominais de perfil, sem cobertura física calibrada; seleção, prior conjunto e transferência de jitter permanecem abertos.

## Custo e axiomas

- [REAL] diagnóstico leve; horas de máquina pesada não debitadas no v13; custo monetário não informado.
- Axiomas: N/A — sem Lean. Nenhuma ficha certifica compilação Lean ou move o gate.

## Fontes de controle

- Ordem oficial: `TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` — SHA-256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`
- Matriz T01–T13: `ORDEM_013_RINGDOWN/bis/015/closing_audit/T01_T13_CLOSING_AUDIT.json` — SHA-256 `f088f5819b3ac78da9d3b974f64d15def1f1eb4525ed0b65467e2e12f9be9caa`
- Orçamento v13: `ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json` — SHA-256 `eaa6412f8646b0f1d624341d5759fa2c1936da35436d8e0f9f53c6d2ad121b81`
