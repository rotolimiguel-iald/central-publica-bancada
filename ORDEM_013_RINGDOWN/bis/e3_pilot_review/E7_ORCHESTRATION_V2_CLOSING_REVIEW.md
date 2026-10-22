# E7 — fechamento independente da orquestração v2

**E7-R1 a R4 e N1 fechados para os bytes pinados no JSON ao lado.** Executadas 22 fixtures somente do AST `main`/`strict_load`, sob `-B -O`, com relógio, guard, publicação e subprocessos simulados: 33 controles verdadeiros, incluindo os quatro pins/contratos documentais. Nenhuma extração ou consumo científico real, revisão de baseline, importação do guard ou lançamento de processo científico.

- R1: timeout das duas etapas deixa registro, erro e hash do log; interrupção deixa falha visível. O recibo afirma reap apenas do filho direto no retorno/timeout, sem inventar ausência de grupo.
- R2: o limite é o menor entre o prazo global e a reserva fixa, com margem de 30 segundos para encerramento. Retorno após prazo e validação além do prazo recusam sucesso. Não há reinício de horas. A margem não é garantia de tempo real para falhas do sistema de arquivos/SO.
- R3: rc zero com resultado ausente, quantidade/papel incorreto, matriz incompleta, hash do posterior errado, contagem booleana e afirmação física indevida falham visivelmente. O contrato esperado é 33 calibrações, zero testes e 20 linhas AWAITING_DATA, compatível com o entrypoint congelado lido.
- R4: duplicatas, NaN e `1e999` são recusados nas fixtures. A revisão inclui a última alteração `parse_float`, com SHA fresco antes/depois dos testes.
- N1: produto, log e `.pending` preexistentes recusam antes de autorização; bytes preservados.

A verificação dos produtores confirmou pins e plano de 33 IDs únicos de calibração, sem novos testes. O controle de processo continua limitado ao filho direto: entrypoints congelados não criam pools/filhos explicitamente, e o launcher não declara `group_absent`. Interrupção externa, pane do host ou falha de disco pode impedir recibo; não se certificou comportamento real do SO com mocks.

**Aprovação de código não é aprovação de E6 nem autorização de execução científica.** No lançamento ainda são necessários resultado E6, revisão independente com `approved:true`/hash exato, orçamento registrado e prazo vigente. A aprovação corresponde aos bytes medidos; novas alterações exigem nova conferência. Todos os pareceres anteriores permanecem preservados.
