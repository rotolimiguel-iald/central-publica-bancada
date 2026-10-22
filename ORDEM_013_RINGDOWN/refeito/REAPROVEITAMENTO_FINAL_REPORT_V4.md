# Aproveitamento — gerador documental final v4

[INPUT — ordem do principal] Sucessor da v3; v3 e draft existente preservados. Autoria W; R revisará o novo texto real. Não executar antes de os achados de R serem consolidados. Esta ficha não altera a autorização nem acrescenta gates científicos.

Reutilizada integralmente a arquitetura documental da v3, com estas correções pontuais:

- `historical_ratio_cell`: só apresenta a razão C4 herdada quando a predição de referência E0 é numérica e finita. Ausência, texto, booleano ou não finito devolvem OPEN. A nota distingue o zero histórico de R-PROP/R-RAIZ-COHERENT da predição zero sob R-GLOBAL. Não muda E0/C4/E6/E7 nem recalcula ciência.
- `load_b2_costs`: lê os campos de duração da campanha sintética E2, recibo do produtor E4/E5, revisão independente E4/E5 e controlador E4/E5, conferindo hashes e tamanhos declarados no manifesto B2. Mostra ponteiro, pin e escopo por linha. O tempo do controlador sobrepõe o do produtor e não é somado; o ledger contínuo permanece separado.

CLI preservada. O destino padrão novo é `bis/final_report_v4_001`, com os mesmos nomes `FINAL_REVIEW_DRAFT.md` e `FINAL_REVIEW_DRAFT_MANIFEST.json`, **sem `--replay`** no uso normal. Um `--output-dir` explícito também pode escolher outro destino novo. Nenhum arquivo entregue é substituído. Replay continua sendo opção distinta, documental, não uma publicação final.

As cinco correções da v3 permanecem: integridade efetiva e exceções visíveis; pins do closure; E6 como anexo integrante e sinóptico por três rotas; estatutos e OPEN efetivos E7; custos observados e ficha/comando de reprodução. Sem amostras/HDF, sem nova ciência, sem rerun E6/E7. Os metadados desta implementação não são aprovação do draft sucessor.

Pins da v3/draft anterior e evidências sintáticas/fixtures finitas constam de `FINAL_REPORT_V4_IMPLEMENTATION_MANIFEST.json`. N/A — sem Lean.
