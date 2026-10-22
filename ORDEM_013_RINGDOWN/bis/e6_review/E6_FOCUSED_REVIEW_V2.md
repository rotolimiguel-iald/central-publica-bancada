# E6 V2 — revisão focal R1–R5; R3 ainda OPEN

[REAL] **BLOCKING_FINDINGS_OPEN. Não autoriza E6.** Revisão exclusivamente dos deltas da V2 congelada; V1 preservada. Nenhum quadro real, recibo real E3/TEST, seed, posterior, strain, PE ou MC foi executado/lido.

[REAL] **48 mocks independentes: 47 expectativas satisfeitas; um positivo indevidamente recusado.** Nenhum negativo aceito. O positivo que falha é `R3_existing_O5_mapping_nonnull_information_dummy`: `ValueError: Incompatible semantic unit: TAU220_POPULATION/N90_information_target`. Não chamar 47/48 de PASS. Harness AST usa somente fixtures sob a área do revisor; não chama main. A grade dummy mantém 180 células/10 leituras. Manifesto e 14 pins externos conferiram; constantes de unidades coincidem com contrato.

| Achado original | Estado focal | Evidência |
|---|---|---|
| R1 | BLOCKER_CLOSED_FOR_REVIEWED_BYTES | Recusa estágio/atividade antes da ativação e TEST antes da calibração; pins predecessores e revisão de timeline divergentes recusados. GO fonte anterior a E2 é aceito com atividade válida; paredes NO_EXECUTION são aceitas sem inventar execução. |
| R2 | BLOCKER_CLOSED_FOR_REVIEWED_BYTES | Razão física com vermelho ou em calibração recusada; flags/completude/ligação de calibração exigidas para UNDERPOWERED. UNDERPOWERED válido com z dummy 0,2 é aceito: nenhum requisito de poder ≥5. Razão condicional com vermelho é aceita. Razão física TEST pode coexistir com razão física de calibração null. |
| R3 | OPEN — regressão no mapeamento histórico | Canal/unidade incompatível é corretamente recusado nos mocks de gate; porém o próprio mapeamento O5 produz unidade recusada para informação não-null. |
| R4 | BLOCKER_CLOSED_FOR_REVIEWED_BYTES | Os quatro grupos futuros recusam resultados físicos e aceitam cenários condicionais sem dados físicos. Nenhum desenho futuro adicional exigido. |
| R5 | BLOCKER_CLOSED_FOR_REVIEWED_BYTES | Dados presentes/vermelho/AWAITING_DATA recusado; presente/vermelho/INCONCLUSIVE aceito; ausente/OPEN/AWAITING_DATA aceito. |

## R3 remanescente: causa e correção delimitada

[REAL] `assemble_baselines` conserva `operational_information_target` dos forecasts E0 com `unit=source_declared_information`. A V2 só permite `sum_inverse_variance_dtau` nesse campo/rota. O novo `check_metric(..., route)` recusa a linha que o próprio builder monta. Conferência somente de metadados no E0 pinado identificou 32 de 80 linhas com o campo não-null; nenhum valor científico foi emitido ou recomputado. Um único forecast totalmente fictício reproduz a falha.

[INPUT — correção necessária] Corrigir em nova versão preservada o vínculo semântico desse campo: conferir sua proveniência documental e declarar o tipo informacional correto, sem tornar uma string genérica atalho para qualquer unidade. Não fazer novo cálculo, não alterar a fonte E0, não transformar contagem/volume em informação. Acrescentar positivo dummy de O5 não-null e negativo de unidade incompatível. Reconciliar código/contrato/schema/pins. A V2 congelada e esta falha permanecem como história.

[OPEN] O fechamento completo depende da versão corretiva, de seus pins e do fechamento desse único resíduo R3. R1/R2/R4/R5 não serão reabertos como nova ciência; somente se um delta posterior tocar esses caminhos. A validade física e a cronologia dos estágios reais continuam dependentes de recibos reais E3.2/E3.3/TEST, revisão e autorização posterior. O preparo aprovado não substituirá esses atos.

[DECLARADO] Coordenação encaminhada ao principal para W, porque o canal disponível nesta sessão não expõe W diretamente. Nomes e hashes de artefatos não provam independência organizacional nem execução física. NOT_FALSIFIED nunca equivale a CONFIRMED.

## Pins medidos

| Artefato | SHA256 |
|---|---|
| `e6_prepare_v2/PREPARATION_MANIFEST_V2.json` | `5eff95bd65a0b2f32d9e81a3d9b1994e9082c1d29ed59dac8fe73a8b3be5b772` |
| `e6_prepare_v2/generate_reach_table.py` | `ff7861eb81ac309a22d268cf9a8f56bc45980822bc07e1b806091aa06fa9064f` |
| `e6_prepare_v2/CONTRACT.json` | `4cfb991eb9fd26d03095bd40170d41add71b212870191c96e477fac8535eec80` |
| `e6_prepare_v2/OUTPUT_SCHEMA.json` | `958a719c42cf336330f0128f0082e24e261f1e2157bbc4d2d0ab9b8253214c50` |
| `e6_prepare_v2/STAGE_RECEIPT_SCHEMA.json` | `eba850a6ee55a7659d2a6f50dd5288d57b432ee8627df65f4bf387fddbea09fd` |
| `e6_prepare_v2/SOURCE_PINS.json` | `b52b18616b15342987838edb77d7f4559dc81c5e3cfc8d91b9d957c33b6489af` |
| `e6_review/review_fixtures_v2.py` | `1fa75050e67ab3da018f63ec727531c6da184d1e238e7db3d4e87b5dcb3d1cf4` |
| `e6_review/E6_INDEPENDENT_FIXTURE_EVIDENCE_V2.json` | `50da07c40a6955a80e3fd25d84dc375c86e64953a5fbe5970c58676ff0b24d18` |

Revisado em 2026-09-22T23:00:52.965115+00:00.
