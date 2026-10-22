# Revisão independente do encerramento INIT003

[REAL — recibos, hashes e leitura estática, 06/10/2026] **Encerramento terminal confirmado, com dois defeitos operacionais ligados: INIT003-END-01 e INIT003-END-02 (P2).** O GR produziu diagnóstico parcial sem convergência e com cinco operações bloqueadas não respeitadas pela regra de parada. O supervisor prosseguiu para RB; a coordenação interrompeu esse filho. Não há recuperação/cobertura qualificada nem autorização de repetição.

A auditoria própria concluiu **102 conferências documentais/de integridade**, com 62 fontes por hash: recibo ROOT e todos os arquivos nele listados, 30 pins do pacote consumido, autorização/claims/identidades, logs, estados, limites e caminho de parada no código. O NPZ diagnóstico foi lido somente como bytes para conferir SHA256; nenhuma estrutura do arquivo foi desserializada e nenhuma inferência foi calculada. Sem execução de controle/PE, import nativo, rede, sinal enviado, alteração do pacote ou nova autorização.

## Achados acionáveis

**INIT003-END-01 — driver só testa a violação de auditoria antes da amostragem.** O hook em driver_p3.py84–96 acumula blocked e levanta PermissionError. A linha137 testa a lista após construir GWT. O logl138–145 e budget103–106 não consultam a lista; o resultado195 apenas a serializa. Um importador pode capturar PermissionError, continuar pela fonte permitida e devolver a avaliação normalmente. A ausência de exceção no wrapper não elimina o evento persistido pelo hook. Na rodada, cinco strings aparecem no resultado final apesar do estado STOPPED_NOT_CONVERGED e error=null. A regra contratual de interromper após operação não permitida não foi cumprida durante essa fase.

**INIT003-END-02 — supervisor aceita estado parcial sem validar integridade operacional do resultado.** launch_p3.py47–51 lê somente status para decidir continuidade; não verifica blocked_operations. STOPPED_NOT_CONVERGED com exit0 está na lista de continuação. Por isso o resultado GR com cinco bloqueios foi aceito pelo programa para iniciar RB. O final do supervisor chama main sem propagar um código de falha; o exit0 reportado pelo ROOT é coerente com essa fonte mesmo após filho RB retornar−15. PROCESS_RETURNED significa apenas que o processo retornou, não que o job foi bem-sucedido.

Os achados qualificam a implementação de parada/aceitação. Não constituem refutação física, problema de domínio do modelo ou indício de exfiltração.

## Classificação do que foi medido

| Medida | GR final | RB |
|---|---:|---|
| Estado do filho | STOPPED_NOT_CONVERGED; retorno0 | Interrompido; retorno−15 |
| Likelihoods / chamadas nativas | 9738 / 9738 | Total final desconhecido |
| Parede do filho, recibo interno | 857,915204124 s | Sem RESULT final |
| CPU medida no recibo interno | 857,333447926 s | Total final desconhecido |
| Parede das chamadas da fonte | 814,740976005 s | Total final desconhecido |
| Delta logZ | 57,275736336 | Sem valor final |
| ESS ponderado | null | Sem valor final |

O GR permaneceu abaixo do teto10000 e dos limites de parede/CPU; isso não compensa a quebra da regra de auditoria. O stderr contém aviso do Dynesty sobre interrupção por maxiter/maxcall antes do critério delta(logZ). O contador externo terminou em9738, não10000, e budget_abort_count é zero: não afirmar que a guarda externa foi atingida exatamente, nem inventar a contabilidade interna do sampler. O delta informado está acima de0,1 e ESS não foi calculado; não há diagnóstico de convergência.

O recibo GR mantém iguais os estados analíticos antes/depois de GWT e initialization_qualified=true. Isso confirma a passagem da inicialização nessa rodada, sem garantir validade das operações posteriores. A PSD default não aparece como PSD final da likelihood nos recibos conferidos.

O último progresso completo de RB é PROGRESS_0000400.json: iteração400,1173 chamadas/1173 nativas,98,833943024 s de parede e98,411982474 s de CPU. **É progresso parcial, não total final.** O supervisor mede100,274255641 s para o processo RB, mas não mede por isso suas chamadas/CPU finais. Nenhum total ausente foi estimado ou extrapolado. A campanha registra958,936355163 s; esse custo observado pertence a uma tentativa incompleta e operacionalmente não aceita, não a uma recuperação qualificada.

## Denials de cache: alcance preciso

As cinco entradas pertencem a UNUSED_BYTECODE_CACHE e terminam em .cpyc, para lal/__init__, lal/_lal_swig, lalsimulation/__init__, lalsimulation/_lalsimulation_swig e src/temporal_contract. A fonte pseob_frequency_domain importa lal/lalsimulation nas linhas79–80 e temporal_contract na94, depois da instalação do hook. O padrão é compatível com sondagens de bytecode durante imports tardios, registradas pelo ROOT como tentativas de leitura que o importador capturou.

O hook recusou as operações; os recibos não demonstram leitura bem-sucedida fora da allowlist, saída de dados, abertura de D ou falha física. Também não autorizam reclassificar os bloqueios como permitidos retroativamente. São cinco registros de caminhos; a lista não contém modo/flags, timestamp ou índice de chamada de cada evento. Logo, a auditoria não localiza com precisão a primeira avaliação afetada nem reconstrói um rastro completo de acesso. A única checagem anterior de blocked aprovada situa os registros depois da inicialização examinada.

failure_receipt registra zero exceções reconhecidas/None/eventos e domain_error_total=null. O arquivo EDOM vazio e esses zeros não certificam ausência de violação de auditoria: são contadores de categorias diferentes. Não converter as sondagens em EDOM, nem concluir “zero EDOM total”.

## Identidade e interrupção

LAUNCH_STARTED vincula supervisor4716 à autorização e ao contrato. CHILD_STARTED/CLAIM vinculam GR4717 e RB4721 aos respectivos IDs e ao mesmo SHA de contrato. Os dois PROCESS_RECEIPT coincidem com as linhas da campanha; logs e RESULT GR conferem pelos hashes.

O recibo ROOT declara conferência prévia de driver/job/contrato/PGID4721 e envio de SIGTERM. Nesta revisão cruzam-se o PID4721 e a identidade com CHILD_STARTED/CLAIM e o retorno−15 com PROCESS_RECEIPT/campanha. A inspeção histórica do grupo e o ato de sinalização são testemunhados pelo recibo ROOT; não foram reexecutados ou reconstruídos como se fossem observação nova deste revisor. RESULT final RB está ausente. O encerramento é terminal; ausência do resultado não autoriza retry/resume, trocar ID ou renomear a saída.

A autorização476 concedia uma campanha exata sob condições; a auditoria não a transforma em permissão permanente. Pacotes V2/CODEC002, controle465, INIT003 e a revisão475 permanecem preservados. O novo achado corrige ao lado o alcance operacional à luz da execução, sem apagar a revisão estática anterior.

## Reparo mínimo proposto — desenho, não implementação/autorização

1. Manter uma marca persistente de violação de auditoria independente da exceção capturável. Conferi-la antes e depois de cada likelihood, ao terminar inicialização do sampler e antes de classificar/serializar qualquer resultado aceito ou parcial. Classificar como falha de auditoria, com prioridade sobre um status numérico parcial; conservar simultaneamente causas anteriores, contagens e evidências.
2. Delimitar a promessa de parada: checar apenas depois de logl impede a próxima avaliação, mas pode deixar completar a chamada em curso após um import capturado. Se o contrato exigir nenhuma chamada nativa posterior à primeira recusa, acrescentar um ponto de conferência depois dos imports tardios e antes do despacho nativo. A alteração deve ser preparada em artefato separado; não mudar a fonte consumida. Não “resolver” liberando um diretório de cache inteiro.
3. Registrar os eventos de auditoria com categoria, caminho, modo/flags, fase e contador da chamada, mantendo-os distintos de falhas de domínio. Persistir de modo que uma interrupção externa não dependa exclusivamente do RESULT final; evitar que o próprio registro recursivamente acione o hook.
4. No supervisor, exigir resultado bem formado com job/contrato corretos, estado de auditoria sem violações e contagens dentro dos limites antes de continuar. Ausência/má-formação/violação deve encerrar a campanha sem novo filho. Separar processo encerrado, parcial numericamente válido, convergência e recuperação; propagar código nãozero e estado explícito para falha terminal.
5. Qualificar futuramente a parada e o validador com stubs puros: biblioteca que captura uma recusa, recusa durante chamada, recusa ao finalizar, resultado parcial com blocked não vazio, recibo ausente/adulterado e retorno por sinal. Não executar nativas/PE para testar essa lógica. **Nenhum desses controles foi executado ou autorizado nesta unidade.**

Uma eventual preferência por pré-carregar dependências pinadas é alteração de preparação separada e não substitui a marca persistente de violação. A execução INIT003 não deve ser reclassificada como limpa depois do reparo.

## Pins principais

| Artefato | SHA256 lido |
|---|---|
| RECIBO_ROOT_ENCERRAMENTO_INIT003.json | 9ae3fae7696fca9a2e0c593d1bbf87cbd45da68d1e775e4cddf8119372650cf9 |
| CAMPAIGN_RECEIPT.json | 9c48442aeaa65d8c8f87dddcc6a4d9360eaeae7b0c84ff55ba6056d913c5ee57 |
| RESULT GR | 82111caa2b7cd4b78c9a4c8cc9614e3d22273e00cb903ce43bdad68c910275af |
| PROCESS_RECEIPT RB | 8a2a455add376424bc848b02c4e729d35d7de6c9479a44ac5fa090da25c4b697 |
| Último progresso RB | d73de98ac3b8f26683a846f48b4c68d77d980e8a741eba109ed322546ae513f4 |

[OPEN] Reparo e sua qualificação futura. A missão desta unidade encerra-se no parecer e no mapa, sem nova ciência, sem recuperação inferida e sem mover gate.
