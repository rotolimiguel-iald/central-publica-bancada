# Revisão independente do supervisor POSIX e da proposta sucessora

Pedido ROOT `44cecdda-e259-43e7-b42f-04eb0e951e4f`; revisão `2edbb481-7acd-4e75-aec8-c71a1bc2440c`; alvo `f7e2ffb8-6efb-4d0d-85c1-59c7a8f932bc`. Início no mapa657. Revisão local por bytes, JSON, AST e leitura de fluxo. Nenhum candidato importado ou executado; nenhuma chamada científica, WSL, provedor, AUTH, CLAIM ou ROOT_DECISION. O pacote autor e39f88 ficaram intactos.

## Conclusão delimitada

**[REAL documental / DERIVED da leitura] Aceite estático limitado ao supervisor de qualificação stdlib e à coerência dos diffs cooperativos. Não é aceite de execução, qualificação Linux ou integração científica F1.** Não encontrei alteração escondida de prior/modelos nem uma razão para refazer I03,755c ou outros controles consumidos. A proposta faz uma distinção válida de alcance: eventos Python auditados não equivalem a interceptação universal de operações nativas.

O núcleo de integração ainda falta no próprio pacote: o único filho executável preparado é stdlib; o adaptador39 recusa toda admissão científica; a porta sucessora permanece abstrata. Isso está declarado pelo autor. A existência dos arquivos/propostas não muda esse fato. O próximo trabalho útil é uma composição concreta com os módulos existentes, seguida de **qualificação conjunta** em unidade nova, preservando o prior inteiro e os critérios vigentes. Não é outra camada matemática nem uma repetição de testes matriciais.

As referências abaixo são relativas a `f9_supervisor_preparation`, salvo indicação. O JSON desta revisão associa cada localizador à fonte e ao hash calculado. `VERIFICACOES_ESTATICAS.json` contém o inventário completo, os hunks reconstruídos em memória e os limites da conferência.

## O que foi conferido

- Os25membros,18fontes e8backups do manifesto atual coincidem com seus bytes e com o intake ROOT. As duas cópias declaradas, AuditLatch e porta39, são byte a byte idênticas às fontes.
- Os nove Python passam por AST; não foram importados. Os dois diffs aplicam-se exatamente **em memória**, sem fuzz, e o sucessor do controlador coincide em tamanho/hash com SUCESSOR_DERIVACAO. A porta reconstruída coincide com a proposta em disco. `_grid`, `_verify_bindings` e `_preparation` mantêm a mesma AST; assinaturas dos quatro métodos da porta coincidem com o adaptador e a proposta.
- O controlador proposto conserva a cobertura integral da caixa do prior, os planos/contagens por cenário e os resultados ENGINEERING_ONLY com p/sigma/verdict nulos. Os diffs restringem a SYNTHETIC_ONLY; não abrem observados. O validador exige operações nativas null e não permite trocar desconhecimento por zero.
- Claims são persistentes por unidade/root estável: `ProtectedDirectory.reserve`,122–127, faz mkdir exclusivo e fsync; `publish`,129–158, usa criação exclusiva, readback e hardlink sem sobrescrita. O diretório parcial permanece consumido após falha. A estabilidade da root por unidade depende do registro externo explicitamente confiável, não de assinatura criptográfica inventada.
- `process_supervisor`,147–162, usa argv fixo/sem shell, sessão nova, descritores fechados, pidfd, identidade de processo e GO/nonce; captura limitada está em100–122. O filho espera GO antes de claim/hook/behavior (`qualification_child`,28–41). O pai confere ready, journal físico vazio e limites por nome,181–195. Sucesso precisa reap, resultado/identidade e saída externa, não apenas uma string PASS.
- RLIMIT_AS limita espaço virtual, CPU limita CPU, FSIZE limita um arquivo regular, NOFILE limita descritores; não há alegação de quota global de disco, RSS ou contenção de descendentes pelo SO. O pai declara `OS_deadline_guarantee=False`, `native_IO_isolation=False` e `descendant_OS_containment=False`,220–230.

## Achados materiais priorizados

### R1 — P1, integração aberta já declarada: ainda não existe o executor científico admitido

Âncoras: `process_supervisor.py`,47–50 e144–148; `supervisor_adapter.py`,29–54 e56–71; `supervisor_port_cooperative_proposal.py`,15–42; contratoG1/G2.

O pai aceita exclusivamente STDLIB_PROCESS_QUALIFICATION e lança qualification_child.py. O adaptador consome uma tentativa de admissão e sempre levanta NativePolicyUnavailable; não há transição a ADMITTED. A proposta sucessora define interfaces e parser de recibos, mas não uma classe concreta que as cumpra. Portanto aplicar apenas os diffs não produz execução F1.

**Próximo passo:** montar um sucessor completo, em pasta/identidade novas, com controlador/fornecedor existentes, porta scoped e adaptador concreto; bootstrap carrega os módulos/objetos reais sob a política revisada e chama `run_once`. Preservar `prediction_worker` callable; nunca invocar o main c435 ou editar39f88. A lista fixa de sete módulos do supervisor stdlib,70–74, não é o fechamento do pacote científico: o sucessor precisa de seus próprios pins, comando e escopo explícitos. Isto não pede nova prova matemática.

### R2 — P1, integração aberta já declarada: o guard bloqueia operações necessárias do I02

Âncoras: `cooperative_policy.py`,23–50; `f9_node_preflight_repair_preparation/durable_nodes.py`,53–97,130–163; `f9_controller_preparation/controller.py`,249–259 e344–349; contratoG3.

Após o hook, caminhos de escrita são recusados; `os.link` também. Mesmo a abertura do diretório para fsync e `fdopen` sobre descritores recém-abertos precisam ser previstas no contrato. Logo uma simples ligação ao DurableStore falharia antes ou durante claim/publicação. O guard atual foi feito para o filho stdlib com descritores de staging preabertos, não para o store científico.

**Próximo passo:** consumir o resultado da revisão I02_99e2 já atribuída e autorizar precisamente as operações de seus dois roots protegidos: leitura, criação exclusiva de claims/temporários, posse de descritores, fsync, hardlink sem overwrite e leitura de retorno. Preservar imutabilidade, falhas sticky, ausência de retry e proibição de paths arbitrários. Não bifurcar o I02 nem ampliar a allowlist para uma árvore genérica.

### R3 — P1, integração aberta já declarada: ACK e prazo por chamada não chegam ao pai

Âncoras: `native_progress.py`,15–80 e83–120; `process_supervisor.py`,100–120 e147–156; `f9_controller_preparation/background_supplier.py`,68–91; contratoG4.

A fonte de progresso valida sequência, unidade e nonce, recusa nonce reutilizado, persiste ENTER antes de ACK e mantém estado ativo para o prazo. Os nomes BEFORE_NATIVE_BACKGROUND/AFTER_NATIVE_BACKGROUND coincidem com o fornecedor. Porém o pai preparado observa apenas stdout/stderr; nenhum pipe de progresso é passado, nenhum loop chama `receive`/`next_deadline`, e o adaptador não chama `exchange`. Não existe timeout operacional por chamada só por esses métodos estarem escritos.

**Próximo passo:** abrir e vincular os dois pipes no bootstrap/pai do mesmo sucessor; mapear `context['nonce']` do fornecedor para `call_nonce`, guardar sequência e identidade dos descritores; o mesmo watchdog deve atender captura e progresso com o menor prazo ativo. BEFORE só retorna após ACK; EOF, persistência/ACK perdido, timeout ou chamada inacabada permanecem consumo incerto, sem repetição. No encerramento, confrontar o estado terminal do progresso com contagens e os registros persistidos. `progress_record_sha256` no ACK é hoje um campo devolvido, não uma conferência independente dos bytes no filho; a ligação externa deve conferir os registros, sem atribuir isso ao parser sozinho.

### R4 — P1 para aceite F1, integração aberta já declarada: runtime, objetos, quota e aceitação externa

Âncoras: `process_supervisor.py`,75–86 e218–254; `cooperative_policy.py`,68–80; `supervisor_port_cooperative_proposal.py`,45–86; `f9_controller_preparation/controller.py`,80–109 e317–346; contratoG5/G6.

O inventário Linux histórico foi conferido **como arquivo**. Não mede runtime atual, mapas nativos, objetos vivos ou número efetivo de threads BLAS/CAMB. `verify_loaded_modules` mede paths/bytes; o controlador já distingue fonte de identidade de objeto. A política científica precisa ligar os objetos efetivamente usados aos módulos pinados e a confiança nativa declarada.

RLIMIT_FSIZE não limita o total do store. O parser terminal scoped confere formato/contagens/pins, mas `resource_measurements` pode ser um dicionário vazio; nonce/identidade têm validação de forma, não comparação com valores esperados do pai. Journal/watchdog referências também precisam de resolução externa. Isso é compatível com seu escopo de **parser**, que expressamente exige aceitação externa; não satisfaz sozinho a qualificação de recursos/execução.

**Próximo passo:** inventário atual sob escopo autorizado e comparação dos objetos/mapas reais; quota total persistente coerente com claims, registros e hardlinks; coletor de recursos e verificador externo que compare nonce/processo/pins/contagens/journal/resultado, reap e exit. Resultados parciais nunca contam como conclusão. Não anunciar execução bem-sucedida pela aceitação de um JSON fabricável.

### R5 — P2, delimitação adicional do relógio e da recuperação

Âncoras: `process_supervisor.py`,124–143,198–219 e248–254; `posix_protocol.py`,176–181.

O relógio `started` nasce **depois** de preflight, coleta da identidade e reserva/fsync do diretório. A leitura inicial de plano/decisão também fica antes. Portanto `total_seconds` e `wall_before_terminal_persistence` não medem toda a duração desde a entrada do comando. A medida cobre o trecho iniciado ali; uma chamada do sistema bloqueada não é interrompida por um check posterior. Isso limita o alcance, já declarado como nominal, e precisa estar explícito no sucessor.

Na janela entre Popen e vinculação pidfd/identidade, uma falha pode deixar `expected_child` ausente: o finally registra estado incerto e fecha streams, sem atestar reap. `kill_exact` também pode encontrar processo já encerrado ao reler /proc. O código não promove esses casos a sucesso. Não exigir uma garantia impossível nem sinalizar PID não vinculado; manter a incerteza visível.

**Ação na integração:** definir relógio externo que cubra bootstrap/preflight/encerramento, guardar a identidade assim que disponível e verificar o encerramento de toda unidade; se inconclusivo, conservar claim e impedir nova chamada. A distinção não demanda outra campanha numérica de matrizes.

### R6 — P3, proveniência histórica dos backups, sem evidência de perda atual

Âncoras: `NOTA_BACKUPS.json`,1–9; `NOTA_PREPARACAO.md`,21; oito pins no manifesto e intake ROOT.

Conferi todos os oito backups; os snapshots Python, inclusive os dois recuperados, são não vazios, têm AST válida e os hashes declarados. As diferenças para os atuais são mudanças de fonte verificáveis, registradas por intervalo na conferência. As fontes originais39f88 e AuditLatch continuam idênticas. **Não há base nesta revisão para afirmar perda desses originais.**

A nota informa reconstrução por reversão e comparação com hashes medidos antes da colisão de nomes. O pacote contém os snapshots e hashes atuais, mas não anexa o recibo/evento original daquela medição anterior. Assim, presença/integridade atual = REAL; cronologia da recuperação byte a byte = DECLARADO pelo autor nesta revisão. Para fechar a proveniência, basta anexar o registro pré-incidente já existente, se disponível; não repetir nenhuma execução nem recriar a história. Essa limitação não transforma o incidente em perda demonstrada ou bloqueio científico.

## Próximo passo conjunto — ordem proposta, não execução autorizada

1. Fechar o **mesmo sucessor** com bootstrap/adaptador, política de store e pipes no pai, usando os artefatos revisados acima e o resultado I02_99e2. O escopo cooperativo explicitado basta para o recorte sintético com bibliotecas confiáveis/pinadas; não condicionar esse recorte à invenção de sandbox universal.
2. Congelar manifesto/contrato dessa composição completa e um payload sintético compatível com o domínio inteiro do prior, os cinco modelos, a família declarada e recursos suficientes. O plano concreto determina o orçamento; não escolher subconjunto para fazê-lo caber. Preservar V1 escalar e proposta conjunta90da como identidades distintas.
3. Sob futura decisão ROOT, qualificar a **passagem efetiva** pai→bootstrap→controlador→I02→fornecedor/solver→assembler→consumer/prior/theta→stores→terminal externo. Medir reutilização do background, transformações únicas, contagens completas e consumo durável, aproveitando I03/755c já qualificados. As recusas indispensáveis de protocolo/interrupção devem pertencer ao desenho dessa integração, não a repetições equivalentes dos controles consumidos.
4. Separar esse resultado de engenharia da abertura física§6, da qualificação Q02/Q03 e do observado. Nenhuma nova significância é produzida por este recibo. P3 tem executor/revisão próprios; não duplicados aqui. Fontes/memória divergentes continuam impedindo novas chamadas remotas.

**Limite deste parecer:** não foi aferido Linux, processo, hook, kill/reap, FS, RAM, CPU, disco, bibliotecas ou cálculo. Aceite estático não substitui essas medições. Uma primeira execução do meu inspetor de AST falhou por nome incorreto de uma função (`_verify_preparation` em vez de `_preparation`); corrigi o inspetor com backup de bytes e a segunda conferência completou. Não houve execução ou alteração do candidato nessa correção.
