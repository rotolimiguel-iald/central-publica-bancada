[REAL — ficha documental ORDEM015 §7; T15: NÃO_PAGO]

# Reaproveitamento T15

## Artefato anterior efetivamente reutilizado

- `ORDEM_013_RINGDOWN/bis/015/t10/T10_A_FINAL_RESULT.json` — SHA-256 `b7608f8932478fab48cf945c59e73542780c6e55f46e19d707ba7b93ab53613b`
- Uso: medição T10-A usada apenas como proxy de tempo e diagnóstico do estimador.

## O que foi novo

- Pré-registro e MEDIDA de inviabilidade: H1 excede o limiar de condicionamento; estimador delta_f ausente; 0 injeções e 0 ajustes.

## Teste e verificação

- `ORDEM_013_RINGDOWN/bis/015/t15/T15_MEDIDA.json` — SHA-256 `3eb35d872ad4d6f30e95a8ca4ab62c772f6aa7352d64b20ef04b21ce95c114f7`
- `H1_pass=false`; `pilot_injections_run=0`; `posterior_fits_run_T15=0` no recibo T15.

## Limite do reaproveitamento

- Proxy de T10-A em ruído sintético e parâmetro dtau220 não transfere para recuperação browniana de delta_f em ruído real; sigma_jit,rec e sigma_sys permanecem nulos.

## Custo e axiomas

- [REAL] 0 h de máquina gasta; 1 h alocada; [DERIVED] 0,254–0,710 h de parede proxy para 50–100 ajustes, sem medição de execução T15.
- Axiomas: N/A — sem Lean. Nenhuma ficha certifica compilação Lean ou move o gate.

## Fontes de controle

- Ordem oficial: `TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md` — SHA-256 `c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3`
- Recibo específico: `ORDEM_013_RINGDOWN/bis/015/t15/T15_MEDIDA.json` — SHA-256 `3eb35d872ad4d6f30e95a8ca4ab62c772f6aa7352d64b20ef04b21ce95c114f7`
- Orçamento v13: `ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json` — SHA-256 `eaa6412f8646b0f1d624341d5759fa2c1936da35436d8e0f9f53c6d2ad121b81`
