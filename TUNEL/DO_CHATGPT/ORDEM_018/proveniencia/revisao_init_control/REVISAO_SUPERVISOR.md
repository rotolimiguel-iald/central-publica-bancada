# Adendo — revisão do supervisor de inicialização

[REAL — leitura/hash/AST, 06/10/2026] **INIT-01 resolvido no projeto examinado. Nenhum novo achado acionável.** Este adendo cobre somente supervise_init.py e SUPERVISION_PROTOCOL.json, preservando o parecer/snapshot457 e seus 113 checks. Nenhum controle ou supervisor foi executado; nenhuma decisão foi criada.

[DERIVED] O supervisor registra time.monotonic na entrada de main (linha33), calcula deadline absoluto (67), inicia somente um filho com start_new_session=True (78–79) e espera pelo saldo desse mesmo prazo (82–84). Assim, as leituras/pins/imports do filho passam a ficar dentro da espera externa. Se o saldo acabar, envia TERM ao grupo, admite3s e depois KILL/reap3s (85–94). O finally também mata/recolhe um filho ainda vivo após outra exceção (115–122).

O diretório CONTROL_INIT_SUPERVISION_001 é reservado por mkdir(exist_ok=False); a existência de CONTROL_INIT_001 é recusada antes. Não há loop de retry ou chamada a P3, source, likelihood ou sampler. O único Popen inicia control_init.py pinado, com stdin nulo, logs exclusivos e quatro variáveis de threads iguais a1. O supervisor grava STARTED/CHILD/SUPERVISION_RESULT próprios e hashes dos logs. Não cria CLAIM científico.

A decisão precisa autorizar QUALIFY_INITIALIZATION_ONLY, mesmo hash de contrato e de protocolo e supervised_only=true. O filho continua verificando alternativa B. Ausência de RESULT, erro de processo, estado diferente de PASS, pin de contrato diferente, qualquer contador, bloqueio ou permissão indevida impedem sucesso. O supervisor exige duas linhas e o controle pinado fixa os dois rótulos existentes; o supervisor não reinterpreta os sintéticos.

[REAL] Os cinco pins do protocolo foram relidos. Contrato, controle, helper e manifesto original continuam idênticos ao snapshot desta revisão. O novo protocolo mantém as unidades antigas terminais e automatic_retry=false.

[OPEN] A eficácia dinâmica não foi ensaiada. O limite de60s refere-se ao prazo do filho desde a entrada do supervisor, com até3s TERM+3s KILL/reap no caminho normal de limpeza. O próprio protocolo declara que os pequenos pins e IO do parent não têm confinamento temporal OS rígido. Um processo em estado irrecuperável ou falha de escrita pode deixar cleanup_issue/recibo ausente; exige reconciliação de identidade e não autoriza nova tentativa. Esta limitação não é ocultada por um anúncio irrestrito de encerramento garantido.

A allowlist científica permanece no filho inalterado. O supervisor adiciona um processo de controle e IO de logs/recibos em destinos fixos; não amplia leituras científicas ou execução física. Não confundir isso com sandbox geral de syscalls do parent.

**Parecer:** delta apto, no escopo documental, a subsidiar decisão específica de um único controle de inicialização. Não é autorização, sucesso observado do controle ou liberação de P3/PE. ASD/PSD e bloqueios científicos permanecem cobertos pelo parecer original; não foram repetidos os ensaios anteriores.
