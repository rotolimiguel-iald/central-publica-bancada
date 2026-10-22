# E6 V3 — closing independente focado R1–R5

**[REAL — preparo] BLOCKERS_CLOSED_PREPARATION_ONLY. R1–R5 fechados para o pacote V3 pinado abaixo.** Não é autorização E6, aprovação de recibos reais, resultado científico, extração E7 ou conclusão da ordem. E6 permanece condicionado aos recibos reais E3.2/E3.3/TEST, revisões e autorização do principal.

## Delta e evidência

[REAL] O código V3 difere da V2 congelada em **uma substituição literal de unidade**: `operational_information_target` O5 passa de `source_declared_information` para `sum_inverse_variance_dtau`. Contrato, schemas e SOURCE_PINS são byte a byte iguais à V2. Não houve mudança dos caminhos R1/R2/R4/R5 nem das outras verificações R3. A V2 foi reconferida contra todo seu manifesto; o handoff V3 declara que foi restaurada do snapshot após a separação das árvores. O closing atesta os bytes preservados no fechamento, não ausência de alterações transitórias durante a preparação.

[REAL] A origem foi conferida apenas como código/proveniência: `calculate_e0_core.py:144` define informação por soma de inversas das variâncias de δτ; `:163` define seu alvo informacional. `e0_rate_and_o5_scenarios_013bis.py:35` transporta `I_tau_target90` para `operational_information_target`; o selador E0 transporta o mesmo campo para o alvo de planejamento. Os hashes das fontes de definição conferem com o manifesto V3; os códigos de cenário/selador conferem com os hashes embutidos no E0 pinado. Assim, o reparo tipa um campo existente, sem conversão numérica, troca de contagem por informação ou nova aproximação.

[REAL] **6/6 mocks independentes V3 passaram:** O5 não-null preserva valor/pointer/tipo, O5 null permanece OPEN; rótulo genérico antigo, Hz, contagem de eventos e informação de τ440 são recusados no campo informacional τ220. A grade dummy mantém 180 células e o cenário O5 mantém gate OPEN, z físico null e AWAITING_DATA. Nenhum dado real foi montado em quadro.

A evidência V2 permanece **47/48**, com a falha original preservada. Seus 47 resultados satisfeitos são aproveitados exclusivamente porque o delta executável foi conferido como uma troca de rótulo; não se reescreve a falha histórica como PASS. O caso O5 anteriormente falho agora passa nos novos bytes. Os 60 checks do produtor são evidência do produtor, não substituem os mocks independentes.

| Achado | Closing focal |
|---|---|
| R1 | CLOSED: sequência documental/atividade após ativação, predecessores pinados, timeline revisada. GO anterior permitido; paredes NO_EXECUTION sem execução fictícia. Evidência real ainda será revisada. |
| R2 | CLOSED: números explicitamente físicos e vereditos de evidência exigem validade paga. UNDERPOWERED válido com z dummy 0,2 passou; nenhum requisito de poder ≥5. Razões condicionais com vermelho continuam permitidas. |
| R3 | CLOSED: unidades compatíveis por rota/campo; o próprio mapeamento histórico O5 agora é compatível e mantém a origem. |
| R4 | CLOSED: grupos futuros têm resultados físicos desabilitados neste contrato; projeções condicionais permanecem. Nenhum projeto de disponibilidade futura exigido. |
| R5 | CLOSED: dado presente/vermelho exige INCONCLUSIVE_SYSTEMATICS; ausência exige AWAITING_DATA; contradições recusadas. |

[OPEN] Hashes e timestamps documentais não provam execução física ou independência organizacional. Os adaptadores reais deverão ser conferidos com seus artefatos e paredes reais. Parede E3 não paga calibração nem 5σ; alvo N condicional não é poder observado; projeção/plot condicional não é detecção. NOT_FALSIFIED nunca é CONFIRMED.

[REAL — escopo] Escritas só em e6_review; sem alterar produtor/E2, ler seed/offset/posterior de teste/strain ou executar PE, MC, waveform, E6 main ou ativação real. Apenas código, contratos, hashes e metadados de presença foram consultados. Esta declaração não afirma cegueira absoluta. O plano de métricas e o candidato de injeções permanecem preservados.

## Pins finais medidos

| Artefato | SHA256 |
|---|---|
| `e6_prepare_v3/PREPARATION_MANIFEST_V3.json` | `42b26421cfc7c077ea0b1cf76d115007c597c0804eb74f6427aa01220e4a62eb` |
| `e6_prepare_v3/DELTA_AND_HANDOFF_V3.md` | `0a99d4783e8117f239f39eb3d47cbd939551bac694fd4e569e4d2adee14c2763` |
| `e6_prepare_v3/generate_reach_table.py` | `664b6256c4003caf5c5ca4d958aadda87ad7aa19f2a11c1c485c92d17829fc60` |
| `e6_prepare_v3/CONTRACT.json` | `4cfb991eb9fd26d03095bd40170d41add71b212870191c96e477fac8535eec80` |
| `e6_prepare_v3/SOURCE_PINS.json` | `b52b18616b15342987838edb77d7f4559dc81c5e3cfc8d91b9d957c33b6489af` |
| `e6_prepare_v3/OUTPUT_SCHEMA.json` | `958a719c42cf336330f0128f0082e24e261f1e2157bbc4d2d0ab9b8253214c50` |
| `e6_prepare_v3/STAGE_RECEIPT_SCHEMA.json` | `eba850a6ee55a7659d2a6f50dd5288d57b432ee8627df65f4bf387fddbea09fd` |
| `e6_review/E6_FOCUSED_REVIEW_V2.md` | `8874ec72c63b14a5918ea4d4900c0b9317ff9999e60a154d61de13dacc748a93` |
| `e6_review/E6_INDEPENDENT_FIXTURE_EVIDENCE_V2.json` | `50da07c40a6955a80e3fd25d84dc375c86e64953a5fbe5970c58676ff0b24d18` |
| `e6_review/review_r3_delta_v3.py` | `f848dbc52cef019a208b2c59df90e5f3c0853894300c58077b3408e33298d90d` |
| `e6_review/E6_R3_DELTA_V3_EVIDENCE.json` | `1ecec22035f895e8877903c668749c4ed381e5298fb906dc95c9b83660de7e34` |

[REAL] Manifesto V2: `5eff95bd65a0b2f32d9e81a3d9b1994e9082c1d29ed59dac8fe73a8b3be5b772`. Conferidos 208 artefatos V2 e 609 artefatos V3, além dos 14 pins externos. Recibo JSON pareado contém o pacote exato para futura vinculação pelo principal.

Fechado em 2026-09-22T23:06:35.340366+00:00.
