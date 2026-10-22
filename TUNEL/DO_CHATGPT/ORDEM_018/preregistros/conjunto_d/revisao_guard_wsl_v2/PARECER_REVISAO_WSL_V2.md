# Revisão independente do delta WSL V2

**Aceite estático do delta: WSL-01 e WSL-02 resolvidos no código lido; nenhum bloqueador novo localizado nesse recorte.** O parecer não executa ou autoriza a unidade. A decisão de consumo único cabe a ROOT após conferir os pins e emitir sua autorização específica.

[REAL documental] Mapa consultado antes, preparação523; o snapshot514 e o parecer519 foram preservados. Request único, ainda não consumido: `4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf`. Mesmo caso `WSL_CACHE_LATCH_001`, um controle, um filho de controle e60 s nominais. O helper de limpeza continua executando zero controles. Pastas distintas não autorizam dois consumos do mesmo pedido.

## Reparos conferidos

**WSL-01.** `launch_windows.py:15–42` inicia `errors` e `eof` separados para stdout/stderr. O EOF só é marcado no retorno normal `b""`; retorno de tipo indevido ou exceção é erro. `read` retém tipo/mensagem, `require_no_errors` levanta falha, e `join` exige ausência de erros, fim das duas threads, EOF dos dois fluxos e ausência de overflow. A checagem de erro aparece durante a espera e após join (`wait:55–64`). Assim, o caminho antes identificado — leitor stderr morto por erro com buffer vazio e stdout íntegro — não satisfaz a condição de sucesso do código V2.

[DERIVED] Se a leitura falhar durante o trabalho, `wait` propaga para o tratamento de falha; o finally mantém STOP e limpeza já previstos. Se a falha só for observada ao recolher as threads, o `join` final também a recusa. O status conservador pode se tornar `UNCERTAIN_ORPHAN_STATE` mesmo quando a incerteza é da captura; o recibo de limpeza continua distinto e não se deve inferir órfão físico apenas desse rótulo. Não é bloqueador novo.

`capture_state`, linhas124–125, persiste snapshots dos processos principal e de limpeza: erros, EOF, overflow, bytes retidos e término das threads. Há valores null quando o processo não foi criado. Snapshot de falha não constitui captura íntegra; o caminho PASS exige que os leitores tenham terminado e passado nas checagens.

**WSL-02.** `linux_control.py:39–41` calcula espaço restante, acrescenta somente `chunk[:room]` e recusa `len(chunk)>room`. A retenção lógica do buffer fica em32768 inclusive no caminho de overflow. O chunk temporário continua limitado a4096 na leitura; esse teto não é afirmação sobre RSS, alocação interna do bytearray ou buffers do SO.

## Delta delimitado e restrições preservadas

[REAL estático]130 conferências AST/texto/pins constam do recibo. `common.py` e `worker.py` permanecem idênticos descontando apenas o nome do diretório. O fonte Linux inteiro só difere pelo rebase e pelas três linhas do recorte do buffer. No AST Windows, removendo somente as implementações de `Capture`/`wait` e a nova chave `capture_state`, todo o restante coincide com514 após normalizar o diretório. Os quatro arquivos apontam para V2; o guard continua byte a byte idêntico.

Essa comparação conserva autorização/revisão por hash, claims exclusivos prévios, request/caso, nonce/argv/exe, inspeção de UID, start_ticks de pai no worker, pidfd, STOP+gate/flock, ausência de retry/resume, orçamento nominal, finally de limpeza e condições de saída. Os três caminhos de retorno mantêm verificações de prazo após recibo e após stdout/flush. Não foi exigido prazo duro do SO: JSON provisório isolado continua insuficiente sem captura íntegra, saída0 final e observação externa do encerramento.

O contrato só muda schema, pins locais, nova seção de revisão e uma exigência aditiva de captura íntegra. Limits, runtime, linux_pins/windows_pins, escopo, identidade/claims e política de leitura/escrita permanecem iguais. Comando proposto aponta ao launcherV2 e ao contratoV2 medido. Nenhum acréscimo de caso, campanha científica ou permissão para D/PE.

## Custódia e limite

Manifestos514/519/523 e seus artefatos foram relidos por hash/tamanho. Seis pins locaisV2 e três bináriosWindows foram medidos. Os14 pinsLinux foram comparados com o recibo documental já admitido, sem nova leituraUNC nem execuçãoWSL. O recibo distingue essas operações. AUTORIZACAO_ROOT, CLAIM, RUN e RESULT estavam ausentes em514/V2 no exame.

Zero candidato importado/executado; zero WSL, hook, stub, teste comportamental, journal instanciado, dadoD, ciência, rede ou provedor. Nenhum CLAIM/autorização criado. O auditor desta revisão importa apenas stdlib e trata todos os candidatos como texto/AST. O comportamento no runtime e os caminhos de timeout permanecem [OPEN]; uma execução rápida bem-sucedida não mediria todos os caminhos de falha. ROOT pode decidir a eventual execução específica sem tratar esta revisão como autorização.
