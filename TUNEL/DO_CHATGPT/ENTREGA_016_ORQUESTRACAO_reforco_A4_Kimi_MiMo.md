[REAL — distribuição e compilação local; respostas de provedores ainda não são prova]

# ORDEM 016 — reforço A4 para Kimi/MiMo

Data UTC: 2026-09-24T17:27:08.515879+00:00.
Abertura sha256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Foram preparadas três unidades novas, distintas das A3: Kimi cético da faixa KMS; Kimi cético do alcance geométrico do quociente polar; MiMo da álgebra das dez leituras. As três prévias selecionaram o executor exigido. Memória comum pelo transporte; uma chamada por unidade, sem substituição automática.

Kimi KMS registrado: `4cc14b01-d6f7-4bb4-b9b4-5308cb6b060b`. A segunda submissão foi recusada antes de chamada remota porque havia cinco coordenações pendentes. A terceira não foi submetida nesta rodada. A coordenação oficial recebeu os payloads e a ordem de registrá-los com os mesmos UUIDs quando abrir vaga; não se ampliou nem se contornou a fila.

| Provedor | Unidade | request_id |
|---|---|---|
| kimi | kimi_kms_strip_scope | 33cff3ad-b1f8-459a-a180-14d7d475351a |
| kimi | kimi_polar_geometry_scope | 5c6322c7-b76e-4381-ac02-7955eedbecc9 |
| mimo | mimo_ten_readings_algebra | 103de974-4c81-4252-8ee9-0ef4f7c5f0d2 |

## Estado observado da fila

| job_id | Estado | Execução |
|---|---|---|
| 6cdeb9a0-20f7-45af-8b96-4bf5bb35c8f2 | failed | failed |
| f8ec22e7-21c2-4bf4-b3bc-29655e681481 | completed | result_ready |
| cc64f514-586e-48c9-b6bb-e3b963d16bff | execution_waiting | running |
| 63b4e640-2b1a-4f7e-8213-76b2eb94d3e5 | awaiting_dispatch | None |
| a947924d-70c2-4191-97f2-d845f56420ee | awaiting_dispatch | None |
| 4cc14b01-d6f7-4bb4-b9b4-5308cb6b060b | awaiting_dispatch | None |

A falha MiMo anterior IncompleteRead foi preservada sem repetição. Não há recibo de consumo final para essa tentativa; custo não confirmado, nunca zero presumido.

## Prova local que acompanha a revisão

KMSStripConditional.lean: 3 declarações auditadas, rc0, somente propext/Classical.choice/Quot.sound. O corpo de kms_rescale_existing foi comparado textualmente ao insumo: reutilizado sem alteração. As duas composições novas provam a reescala de uma faixa KMS modular já assumida para rapidez 2π e tempo de Killing 2π/κ.

**Não se produziu o estado/rede regional.** H_regional_modular_strip e H_modular_equals_geometric permanecem hipóteses explícitas. Nenhum gate alterado.

Fonte SHA256: `63fd714315d50e182061839e4ad66a1b4fd8ccff2dde80bf1e5d7b18f7414574`.
Log SHA256: `18f027ce5cf38bb592f3e58c0fdac77ca3cb0f82ca3f78470cbce9a004ca5729`.
Tempo de máquina: 24.542s parede; 24.391s CPU.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A4\kms_strip_manifest.json`.
Custódia da distribuição: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A4\orchestration_reviews_20260924\dispatch_snapshot.json`.

## Adendo 2026-09-24T17:28:55.919623+00:00

A segunda unidade Kimi foi registrada pela coordenação: `4f01bd55-230e-4510-be80-742372dd74b2`, estado `awaiting_dispatch`. Mantido o request_id original; a recusa local anterior permanece em seu recibo. A unidade MiMo A4 segue preparada para a próxima vaga.

A revisão Kimi A3 anterior concluiu: 317451 tokens de entrada, 14012 de saída, 331463 totais. A ponte sugerida já existe em 23 declarações cujas fontes/logs foram novamente conferidos nesta rodada, sem nova compilação. Nenhuma reimplementação. O contraexemplo §2.2 foi rejeitado: retirar um aberto do suporte não torna a fase identicamente 1 no complemento. Resposta preservada com correção ao lado.
