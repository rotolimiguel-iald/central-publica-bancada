# Preparação da revisão do resultado E6 — inativa

Ownership exclusivo deste verificador: `bis/e6_actual_review`. Não altera a preparação E6 de W, os pareceres de R, fontes congeladas, resultado ou assembler.

`verify_actual_e6.py` está preparado para uso **somente depois do GO do principal e da produção de E6**. Nesta preparação foi feita apenas análise sintática por AST e medição de hashes; o verificador não foi executado, nem mesmo contra fixtures. Não foi inspecionado resultado E6 atual/futuro. A preparação não é um parecer de aprovação de resultado.

O verificador usa apenas biblioteca padrão e leituras de metadados JSON/MD pinados, limitados a 25 MiB. Recusa cache, caminhos privados e arquivos de amostras; não importa o assembler/guard, não chama subprocessos, não faz PE, OLS, MC, FFT ou recomputação científica. Sua única escrita futura será um novo parecer JSON e temporário exclusivo nesta pasta; nenhuma saída anterior é substituída.

## Conferências previstas

- Produto cartesiano exato: dez leituras × três rotas × seis grupos, 180 células sem duplicatas; estatutos e unidades conforme contrato preparado.
- Cada métrica transportada: hash da fonte e igualdade tipada com seu JSON pointer, incluindo pisos históricos e contexto E1. Quantidade condicional não se torna medição física. Ausência de campo só admite `null/OPEN`, explícito.
- Cenários: nenhum teste observado, nenhum gate verde, `z_physical`, `lnB` e razão física nulos; gates das paredes vermelhos. Calibração/custo por posterior permanecem não pagos.
- Três adapters reais e reviews independentes: identidade E2, artefato/review/hash, bindings exatos, predecessor e cronologia da fonte, emissão e revisão. E3.2 identifica orçamento documental; E3.3/TEST identificam paredes sem execução, sem inventar horários de campanhas.
- SHA do JSON e Markdown confrontados com `RESULT_RECEIPT.json`; hash do resultado confrontado com o fornecido pelo principal; fontes e pacote reconferidos ao término.

A cronologia documental não prova, sozinha, execução física. A revisão dos adapters continua pertencendo a R. O futuro parecer registra essa distinção.

## Contrato futuro para E7

Argumentos obrigatórios para ativação: `--principal-go`, `--result`, `--result-sha256`, `--authorization`, `--authorization-sha256`, `--output`. Paths de entrada são os efetivamente comunicados pelo principal; não foram escolhidos/abertos antecipadamente. Saída nova diretamente nesta pasta, por exemplo `E6_ACTUAL_RESULT_REVIEW_001.json`.

Sem `--principal-go`, o programa permanece inativo e não abre resultados. O flag é uma trava operacional, não autorização autoemitida; somente usar após ordem do principal. Uma falha produz `approved:false` e achado explícito, nunca aprovação parcial. O resultado aceito emitirá `{ "approved": true, "e6_result_sha256": "hash medido e conferido" }`, com checks, fontes e limitações. Não publica autorização de E7 e não muda o resultado E6.

`PREPARATION_RECEIPT.json` pina este verificador e o pacote atual. Mudança de contrato/bytes requer revisão e novo recibo versionado, preservando esta preparação. Não há monitor, lançamento automático ou espera ocupada instalada.
