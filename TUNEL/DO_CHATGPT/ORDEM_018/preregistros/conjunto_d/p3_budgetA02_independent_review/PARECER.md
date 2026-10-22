# Revisão independente P3 A02

**STATIC_REVIEW_ONLY — aceite delimitado do delta.** Os achados P3A-01 e P3A-02 estão resolvidos no pacote 078a3c05-d30f-4c9c-a31a-8a78ca9b6893. Não foi localizado outro bloqueador concreto nesse recorte. Este aceite não autoriza execução, não demonstra contenção POSIX real e não qualifica convergência, recuperação, cobertura ou PE em D.

A revisão examinou bytes, JSON, AST, os contratos e a ligação entre os recibos de testes e suas versões. Não importou candidatos, não repetiu testes e não iniciou WSL, sinais/filhos reais, bibliotecas científicas ou provedores. Não abriu arrays/NPZ/PSD/ASD externos nem observados. Não criou AUTH, CLAIM ou ROOT_DECISION. O mapa externo não foi chamado, preservando a recusa anterior e a instrução de ROOT.

## Fechamento dos achados

**P3A-01 — resolvido no fluxo estático.** Em launch_p3.py:53–54, o handler chama somente cancellation.request(sig); process_supervision.py:18–21 apenas conserva o flag e número de sinal, sem raise, I/O ou mudança de máscara. A única consulta de máscara é pthread_sigmask(SIG_BLOCK,set()) em launch_p3.py:59, sem alteração do conjunto; sinais de cancelamento previamente bloqueados recusam o caminho antes do spawn (60–61).

process_supervision.py:45–48 atribui o handle retornado por spawn antes de interpretar o cancelamento. As esperas de trabalho (49–62) e recolhimento (88–100) usam min(wait_quantum,tempo_restante), e o launcher fixa0.25s (106–109). Em 72–103, cleanup é direto: não entra no context manager antigo nem troca handlers por SIG_IGN. O recorder permanece ativo durante poll/kill/wait. Cancelamento anterior impede spawn; durante spawn com handle retornado, espera ou cleanup conserva a posse e recusa aceite. Falha de spawn sem handle aparece como resultado incerto, sem retry.

A aceitação de processo exige retorno inteiro, deadline respeitado, ausência de erros e PROCESS_RETURNED/exit0 (108–126). Enviar SIGKILL não comprova término. Cancelamento registrado em cleanup também invalida sucesso (104–107). Erro/incerteza impede o caso seguinte no launcher (134–154). Nenhuma máscara de bloqueio é introduzida para herança pelo filho.

O launcher verifica cancelamento/prazo antes de avançar e após persistência dos recibos (70,94,152,165–171). A checagem após restauração dos handlers (185–193) é parte do delta final: ultrapassagem do prazo não conserva saída0 provisória. I/O ininterruptível, SIGKILL do supervisor, perda de host ou exceção alheia antes de Popen entregar o handle continuam limites explícitos; o pacote não promete tempo real rígido. Essa limitação não reabre o defeito corrigido do handler controlável que lançava antes de cleanup.

**P3A-02 — resolvido documentalmente.** CONTRATO_P3.json:287–295 apresenta o custo A vigente como proposta não consumida: 28820s nominais de supervisão, soma26410s de limites duros CPU, 200000 chamadas de likelihood e200000 reservas waveform. Isso coincide com limits e aggregate_maxima_proposed.

As linhas296–326 conservam os antigos7220/6610/20000 e o proxy histórico dentro de historical_reference_not_current_budget, com pin do contrato A e rótulo de não aplicação ao orçamento atual. Conferi igualdade integral de verbatim_fields com o cost do A. current_cost_prediction é null (339); não se fabrica medição de custo ou convergência. Por caso permanecem100000 chamadas,14400/14410s, CPU13200/13205s e8GiB, um worker/thread e dois casos sequenciais máximos, sem retry.

## Preservações e identidade

Os 41 membros e cinco backups do A02 correspondem:46 pins. O A original permanece intacto em seus40 membros+6 backups:46 pins; os seis membros do parecer A também correspondem ao manifesto. O A02 contém17 Python com AST válida e22 arquivos reutilizados byte-idênticos.

Os 14 campos científicos comparados, mais jobs, são iguais ao A; limits também é igual. Driver, guard, contadores, recuperação, validação de resultados, fonte QNM, priors, dados declarados, ruído pareado e seeds não receberam mudança científica. São referências/metadados dos dados: não leitura de seus bytes externos.

Em science_admission.py, o delta limita-se à identidade078a3c05 e raiz A02 (10–11). O restante coincide com A. O vínculo externo a manifesto/contrato/UUID de execução/escopo de acesso/escolha A/recursos/diagnóstico e referência do operador permanece obrigatório (31–117); o comando é candidato com placeholders, não lançamento. Os pins dos inputs internos conferem; referências externas preservam a mesma metadata do A e não foram abertas. Sua autorização de acesso e futura execução continuam decisões separadas, já previstas no contrato.

Validação numérica estrita e CLEAN_PARTIAL versus CLEAN_CONVERGED_NUMERICAL_ONLY foram preservadas byte a byte. Quantis/contração/posição da verdade continuam diagnóstico fraco; não produzem PASS científico. Dois casos pareados não demonstram cobertura e logZ entre datasets não é BF. INIT003 e demais terminais não foram reabertos. A02 não serve como rota alternativa para d72/F1.

## O que os testes existentes cobrem

Conferi seis relações de pins dos protocolos. No V1, os hashes de test_A02_stdlib.py e launch_p3.py correspondem aos backups preservados; process_supervision.py5392B/SHAdee36b24e9c7135bc9ebcd3a70efcdd5815539caab0685c1aa13c1993ed5ff4b é idêntico ao módulo final. Os métodos dos21 testes de supervisão são AST-idênticos entre V1 e final.

O recibo V1 registra22/22:21 casos artificiais do módulo puro e AST22 do launcher anterior. O único método alterado é AST22, que passou a conferir a ordem da checagem de prazo após restauração. Protocolo e recibo V2 correspondem aos hashes finais, e o comando seleciona somente AST22 via unittest. O recibo registra1/1. Portanto são23 invocações e22 casos distintos, sem afirmar nova execução integral da suíte final. A entrada direta __main__ não é o comando da regressão V2, distinção expressa no pacote.

Isso sustenta a cadeia documental declarada do código testado; os testes com doubles/AST não demonstram funcionamento de sinais, pgid, permissões, latência ou contenção nativa reais. Nenhum deles foi repetido por esta revisão.

## Limite da conclusão

[REAL documental] Os dois bloqueadores apontados no A foram tratados, e o escopo científico/limites foi preservado. Não há achado bloqueante adicional na composição examinada.

[OPEN] O aceite estático permite que ROOT decida os passos já previstos, mas não constitui decisão do operador, autorização de acesso às entradas, execução científica ou êxito de P3. Não foi proposta campanha adicional de controles. A revisão é local e não registrou no serviço externo do mapa.
