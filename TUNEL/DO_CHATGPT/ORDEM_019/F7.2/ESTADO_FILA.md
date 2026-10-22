# F7.2 — registro da fila única

[REAL — recibo observado em 07/10/2026 22:10:40, hora local] O pedido de revisão cética preparado para Kimi foi submetido uma vez à fila IALD. O recibo existente é KIMI_QUEUE_RECEIPT.json, SHA-256 0dc9ad1f1617506405c0fab11a45bd828ec0a55b90a861f8e2b106d1cb358132 (lido dos bytes). Ele identifica:

- request_id: c7ab7a4f-db08-4ea2-839d-ae30d131bdd0;
- job_id: 16549246-12ab-4812-bb33-5ee0a9212db1;
- stage: awaiting_dispatch, sem execution_task_id nem texto final no recibo;
- branch_id: F7.2; role: skeptic; required_provider: kimi; max_calls: 1.

[OPEN] O recibo comprova a entrada do pedido na fila, não a execução pelo Kimi, a resposta ou o fechamento científico. Consultar esse mesmo job e request_id para prosseguir; não executar outro submit, disparar Kimi em paralelo nem marcar F7.2 ENTREGUE antes de obter e conferir o resultado. O conteúdo preparado está em KIMI_REVIEW_SUBMIT.json; a errata bibliográfica e as fontes constam de REAPROVEITAMENTO_E_ERRATA.md. Originais científicos e gate permanecem intactos.
