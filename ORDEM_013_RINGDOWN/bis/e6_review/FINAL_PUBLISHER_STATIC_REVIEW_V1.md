# Publicador final — revisão estática delimitada V1

[REAL — fonte lida, sem execução] **LOCAL_PUBLICATION_FIXES_REQUIRED.** Revisão apenas de preservação dos bytes aprovados, recibo e prazo em `refeito/publish_final_report_013bis.py`. Não foi executado/importado o publicador, não houve publicação ou leitura de draft final inexistente/não enviado. Não é novo gate científico ou revisão ampla da campanha. O futuro contrato `approved:true, draft_sha256, blocking_findings:[]` será emitido somente após leitura do texto efetivo.

## PF1 — usar os mesmos bytes na validação, cópia e recibo [OPEN, P1]

Linhas 16–18 conferem hash do review e depois o relêem para parse; conferem hash do draft e depois, na linha 26, o relêem para publicar. Linhas 31–32 calculam hashes novos para o recibo. Uma alteração entre leituras permite publicar bytes diferentes antes de detectar o problema, ou registrar hash de review/draft diferente daquele usado na aceitação. A checagem do destino na linha 27 é útil, mas ocorre depois da publicação exclusiva; não remove a entrega divergente já criada. Esta é uma possibilidade demonstrada pelo fluxo da fonte, não afirmação de alteração maliciosa ou incidente real.

Correção local: ler snapshots dos bytes do review e draft, validar hash CLI do review antes de seu parse e validar hash desses mesmos bytes do draft contra a aceitação. Publicar exatamente o snapshot validado. Gerar o recibo com os hashes desses snapshots e conferir o destino. Congelar também os bytes/metadados de orçamento usados para prazo se o recibo for atribuir o pin à mesma decisão. Verificações de estabilidade adicionais devem acontecer antes do efeito; não chamar uma releitura tardia de prova dos bytes previamente usados. Sem nova arquitetura ou reexecução científica.

## PF2 — caminho relativo falha depois de criar a entrega [OPEN, P1]

A linha 15 aceita `a.draft.resolve()`/`a.review.resolve()` dentro de Chatgpt. Porém as linhas 31–32 usam os paths originais em `.relative_to(R)`, com R absoluto. Um argumento CLI relativo válido passa a primeira guarda e provoca ValueError ao construir o recibo, depois de a entrega já existir.

[REAL — verificação sem I/O] Foi avaliada somente a operação pathlib em um nome fictício: containment do path resolvido foi verdadeiro; `.relative_to(raiz_absoluta)` do path relativo lançou ValueError. Nenhum draft ou destino foi criado.

Correção local: resolver os dois caminhos uma vez antes das validações/efeitos e usar os mesmos objetos para leitura, referência e recibo, ou recusar explicitamente relativos antes de publicar. Preparar todos os campos de caminho antes do primeiro efeito evita essa falha determinística. Não substituir saídas existentes.

## PF3 — checar o prazo também na conclusão registrada [OPEN, P2]

Linha 23 verifica limite da reserva final e 40h antes da cópia. Linha 28 coleta o instante de conclusão, mas não o confronta com os limites antes de emitir status DELIVERED e o recibo. Uma operação iniciada antes do stop e concluída depois pode receber sucesso fora do prazo.

Correção local: revalidar os mesmos limites junto ao ato final/instante declarado e antes de publicar recibo de sucesso. Se cruzar o limite, preservar eventual artefato parcial e falhar explicitamente, sem status de entrega concluída dentro da reserva. Não reiniciar o relógio, ampliar orçamento ou exigir novo GO. O hard deadline existente deve continuar coerente com o limite de 40h; esta leitura não recalcula orçamento científico.

## O que já está correto neste recorte

A aprovação exige `approved is True`, hash do draft e `blocking_findings == []`; o review tem pin CLI. O destino final é fixo, saídas/pending preexistentes são recusadas e a escrita usa temporário, flush/fsync e link exclusivo. O destino é conferido após cópia. A publicação é byte a byte, sem reformatar o Markdown. Campos físicos do recibo conservam ausência de 5σ/PE cega/injeções; não há chamadas de ciência. As duas saídas não formam transação atômica: uma falha depois do relatório pode deixar entrega parcial sem recibo, que não deve ser descrita como concluída. Não se exige uma transação nova para corrigir os três pontos concretos.

[OPEN] Ratificação externa permanece externa. O texto final, sua suficiência de fontes, E6/E7 e TF1–3 serão conferidos na revisão do draft real quando enviado. Este parecer não antecipa `approved:true` nem certifica conteúdo ainda não lido.

## Pins lidos

| Fonte | SHA256 |
|---|---|
| `ORDEM_013_RINGDOWN/refeito/publish_final_report_013bis.py` | `c06373c90ea1f3b75a05997f1c8a7c82086a7431c84ac6edd4673ca87ef3db15` |
| `ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json` | `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f` |
| `ORDEM_013_RINGDOWN/ORCAMENTO_40H.json` | `892e416585062eef5229e01c2e8a6c5b8d3c4ee8a10a72798c0ab2034e5f42e4` |

Emitido em 2026-09-22T23:39:53.887881+00:00. Escritas restritas à área do revisor; produtor intocado.
