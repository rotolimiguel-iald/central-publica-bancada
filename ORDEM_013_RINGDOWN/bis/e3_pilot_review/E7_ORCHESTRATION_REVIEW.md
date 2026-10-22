# Revisão independente — orquestrador E7, antes da execução

[REAL] Revisado o SHA fresco registrado em `E7_ORCHESTRATION_REVIEW.json`, já com `min(deadline global, finalization_stop_utc)`. Nenhuma extração, consumo, importação científica ou execução de guard foi realizada. Foram executadas somente 12 fixtures do AST original de `main`, com guard, relógio, publicação e subprocessos substituídos por simuladores. Os 17 controles verificaram os comportamentos registrados, **inclusive falhas**; não significam aprovação do launcher.

**Não aprovar ainda a ativação E7.** Não há revisão E6 real nesta análise. O contrato mínimo esperado continua `approved:true` e `e6_result_sha256` igual aos bytes selecionados.

## Achados e correções exatas

- **E7-R1 — recibo incompleto de timeout.** `records.append` só ocorre após `subprocess.run` retornar. Nas fixtures timeout da primeira/segunda etapa, a etapa efetivamente tentada não consta em `commands` e seu log não recebe pin no recibo. Registrar início antes do lançamento e concluir o registro em `finally`: comando, início/fim, timeout/código/erro, hash do log existente e estado efetivamente observado de encerramento. Não fabricar `group_absent`. Não iniciar consumidor após falha do extrator.
- **E7-R2 — conclusão depois do prazo ainda recebe sucesso.** A redução ao menor deadline está correta, mas só há verificação antes das etapas. A fixture de retorno após o limite termina como sucesso. Conferir novamente o prazo antes de reconhecer conclusão; ultrapassagem deve produzir falha visível. Reservar margem para encerramento e recibos, sem reiniciar a reserva nem prolongar o limite global. A fixture demonstra a classificação indevida; não mede um estouro real do subprocesso.
- **E7-R3 — código zero não basta para concluir o transporte.** Segunda etapa simulada com rc=0 e arquivo final ausente produz sucesso. Antes do sucesso, exigir os dois arquivos regulares, JSON estrito e vínculos esperados: registro, autorização, posterior hash, escopo e contagem de 33 calibrações/zero eventos de teste no resultado final. Não recalcular ciência nem reinterpretar os veredictos. É uma lacuna defensiva de orquestração; não demonstra defeito no produtor congelado.
- **E7-R4 — parser permissivo no parecer independente.** `approved:false, approved:true` e `NaN` são aceitos por `json.loads`; ambas as fixtures alcançam as duas chamadas simuladas. Usar leitura estrita com recusa de chaves duplicadas/constantes não finitas para parecer, E6 e orçamento; exigir tipos e pins antes de criar autorização. O SHA garante bytes, não elimina ambiguidade semântica. Não há evidência de fraude em parecer real.

**E7-N1, preservação:** os quatro produtos principais têm preflight e a publicação exclusiva evita sobrescrita. Os logs usam `xb`, preservando bytes, mas log preexistente só é descoberto depois de publicar autorização. Incluir os dois logs e resíduos `.pending` no preflight; a fixture preservou os bytes antigos. Não apagar tentativa anterior automaticamente.

**Processos:** `subprocess.run(timeout)` atende o filho direto; o código não estabelece grupo próprio nem demonstra ausência de descendentes. Os dois entrypoints congelados inspecionados não lançam subprocessos/pools explicitamente. Portanto não afirmo órfão observado nem imponho campanha de teste científico. Se o contrato exigir árvore inteira, implementar sessão/grupo próprio com encerramento limitado à propriedade demonstrada e registrar a verificação; nunca varrer/matar processos globais. Tratar interrupções de forma a preservar um recibo parcial quando possível, sem mascarar o erro.

## O que foi conferido

[REAL] Pins atuais do guard, árvore completa dos dois produtores e plano coincidem com E2. O plano contém exatamente 33 IDs únicos, todos `calibration`. A leitura dos entrypoints confirmou verificação da árvore/guard/plano/autorização e recusa de papéis cegos antes das amostras. Não houve reanálise da baseline. O guard continua exigindo seu runtime científico pinado; o teste simulado não certifica esse runtime.

[REAL] Fixtures de aprovação falsa, prazo já expirado e produto existente recusam antes de autorização; rc não zero impede segunda etapa. O orçamento final e a revisão E6 precisam existir e ser auditados no lançamento. Esta revisão não autoriza execução.

Evidência reproduzível: `review_e7_orchestration_finite.py`, `E7_ORCHESTRATION_FINITE_RECEIPT.json`. A primeira tentativa local do teste encontrou a alteração concorrente de esquema do orçamento e falhou antes de produzir recibo; a fixture foi adaptada ao contrato fresco e executada sob `-B -O`. Nenhuma fonte de produção foi alterada.
