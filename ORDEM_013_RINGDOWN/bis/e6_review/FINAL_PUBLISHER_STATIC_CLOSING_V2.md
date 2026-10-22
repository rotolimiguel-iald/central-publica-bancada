# Publicador final V2 — closing estático PF1–PF3

[REAL — leitura estática] **PF1–PF3 CLOSED_IN_STATIC_SCOPE**, sem bloqueantes remanescentes nesse recorte. Fonte V2 lida integralmente e AST analisada; V1 preservada nos bytes do parecer anterior. Nenhuma função do publicador foi importada/executada, nenhum mock de publicação foi rodado e nenhum arquivo foi publicado no túnel.

| Achado | Reparo conferido |
|---|---|
| PF1 — bytes aprovados | review_raw/draft_raw são snapshots; o hash CLI é confrontado com review_pin e o JSON é extraído desses mesmos bytes. A aprovação referencia draft_pin, calculado sobre o snapshot que é copiado. O recibo usa review_pin/draft_pin, não hashes de releituras posteriores. O destino é lido e conferido; diferença recebe FINAL_DELIVERY_FAILED_VISIBLE, com failure e saída não zero. Orçamento/alocação são lidos em snapshots; allocation_sha256 vem do snapshot utilizado. |
| PF2 — caminhos relativos | draft_path/review_path são resolvidos uma vez e usados tanto para contenção/leitura quanto para referências relativas do recibo. O caminho relativo aceito não é reutilizado contra a raiz absoluta depois da cópia. |
| PF3 — prazo na conclusão | deadline é o mínimo entre hard_deadline e finalization_stop. Há checagem prévia; após cópia e hash do destino, stamp é confrontado com deadline e elapsed de40h. Conclusão fora do limite gera recibo FAILED_VISIBLE e saída1, sem status de entrega bem-sucedida. |

[REAL — escopo temporal] `timing_scope` declara exatamente o que foi medido: conclusão da cópia/hash do relatório, antes da serialização do recibo. O closing aceita esse recorte explícito; não afirma que a escrita do recibo terminou naquele instante ou antes do deadline. Não se reinicia relógio nem se amplia orçamento.

[REAL — leitura estática] strictJSON recusa chaves duplicadas, NaN/Infinity e overflow de float não finito. Aprovação continua exigindo `approved is True`, `draft_sha256` igual ao snapshot e `blocking_findings == []`. Destinos/pending preexistentes continuam recusados; publicação preserva bytes e exclusividade. Falha após criação do relatório pode deixar artefato parcial: o recibo de sucesso, quando existente, deve ser distinguido do FAILED_VISIBLE. Falha de I/O pode impedir emissão de recibo; não se declara transação atômica ou sucesso automático.

[OPEN] Este parecer valida somente os reparos locais pela fonte. Não é aprovação do draft final, E6/E7 ou ratificação externa, não certifica uma execução ainda não ocorrida e não substitui conferência dos bytes efetivamente publicados. O contrato final `approved:true,draft_sha256,blocking_findings:[]` somente será emitido após leitura do texto real enviado. Sem novo gate amplo, ciência, PE, posterior, seed/offset ou strain.

## Pins medidos

- Publicador V1 preservado: `c06373c90ea1f3b75a05997f1c8a7c82086a7431c84ac6edd4673ca87ef3db15`.
- Publicador V2 revisado: `d42fc24746e545d89f2c251461be2bdc6f39d41f220e5ec2e194f63a6f3b39ce`.
- Parecer PF1–PF3 V1: `ad4b1cfe7cac89aebee4a04fec814712042c1a33ed769e5d4600765295772a23`.

Emitido em 2026-09-22T23:42:05.869103+00:00.
