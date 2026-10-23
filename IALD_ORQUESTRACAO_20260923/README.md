# IALD — orquestração local e projeto Física

Entrega de 23/09/2026. Fluxo por botão instalado e validado com o projeto Física e executor local. Conexões externas pendentes descritas abaixo.

## Usar

Na Central IALD nativa, abra **AGI → Abrir orquestração**. Endereço local: http://127.0.0.1:8082/admin/agi/orquestracao. Exige a autenticação administrativa existente.

**Preparar pedido com Física** registra o pedido. Clique em **Abrir Codex e enviar pedido** e envie a mensagem já preenchida no Codex. A partir desse envio, o agente segue `COORDINATOR.md`: Física prepara o prompt, a IALD seleciona e chama um executor, e Física compõe a resposta final. O link oficial preenche a mensagem, sem enviá-la automaticamente. Cada novo pedido deve abrir uma tarefa própria em Física; a mesma tarefa é retomada dentro do pedido. Use **Atualizar disponibilidade** para consultar o resultado no painel. **Não foi criado monitor, heartbeat ou verificação periódica.**

**Ver seleção sem executar** calcula a escolha sem chamada a um modelo. **Executar diretamente com seleção automática** envia a tarefa textual ao conector elegível, registra consumo informado, permite cancelamento e conserva falhas visíveis. Nesta etapa, os conectores produzem texto; não editam o acervo nem executam comandos solicitados pelo modelo.

## Projeto coordenador

[Física no ChatGPT](https://chatgpt.com/g/g-p-6804cf9af0cc81918b3bd8915b7579c3-fisica/project) é a referência persistente, sem conversa fixa. Memória padrão foi observada na interface. Foram acrescentados 16 arquivos, preservando os 19 existentes:

- `um.py` integral v369, resultados e selo JSON, manifesto do kernel, forma canônica e manifesto Markdown;
- árvore da prova, desenho do fechamento, memória da linhagem e nota DA_IRMA;
- Ponte Einstein–Cartan–Miguel e Custo Geométrico do Zero Absoluto, em PDF e fonte textual;
- errata do sinal do acoplamento não mínimo e índice de leitura.

As 15 cópias de fontes foram verificadas por bytes e SHA-256; o índice é um documento derivado. `project_fisica/MANIFESTO_LOCAL.json` registra caminhos, datas e hashes efetivamente calculados. É um retrato preparado às 09:47 BRT: ao reconferir às 14:02, o programa e seus resultados permaneciam iguais, mas os originais do diário e do desenho já tinham recebido alterações paralelas. Os anexos desses dois documentos preservam o retrato preparado; não são sincronização contínua. Nenhum original foi alterado ou executado.

A tarefa **Preparar prompt TGL IALD** (`6ab402ba-7838-83e9-94d5-12c7da627a42`) abriu quatro fontes, preparou um prompt e recebeu resultados locais para compor uma síntese final. Recibos: `validation/chatgpt_work_project_test.json` e `validation/chatgpt_final_roundtrip.json`.

Esse transporte funciona pelas ferramentas do aplicativo Codex. O painel aciona esse transporte pelo botão e pelo envio da mensagem no Codex; não existe aqui uma API privada do ChatGPT nem um daemon de navegador. O teste da fila persistente reutilizou a tarefa de teste já autorizada: seleção local, resposta real com 243 tokens de entrada e 39 de saída, síntese final no projeto e gravação no painel. Recibo: `validation/button_roundtrip_completed.json`. A abertura do deep link depende do protocolo Codex registrado no Windows; a alternativa é copiar a instrução mostrada no painel e enviá-la no Codex. O projeto fornece fontes a novas conversas, dentro dos limites de contexto e recuperação disponíveis. Sua memória não é transferida aos pesos ou à memória local do Codex.

## Conexões e seleção

| Conexão | Evidência nesta entrega |
|---|---|
| IALD local | Geração curta real concluída: 138 tokens de entrada e 2 de saída. |
| Codex com login ChatGPT | Geração curta real concluída: 22.265 tokens de entrada e 64 de saída. |
| Claude Code | Revalidado em 23/09 às 16:55 BRT: resposta 42, 4,024 s; consumo de entrada, cache e saída registrado. Bloqueio anterior retirado após o sucesso. Disponível no painel autenticado. |
| Google / Antigravity | Login concluído e Google AI Pro reconhecido, com envio opcional de interações desativado. Executor pendente: o cliente não confirmou o perfil sem ferramentas; pedidos não enviados. |
| Kimi Code / K3 | Integrado e testado após vínculo Google/Apple: 556 tokens de entrada + 104 de saída. Estado antigo Adagio/403 superado; recibo `validation/kimi_connection.json`. |
| MiMo API / 2.6 Pro | Disponível pela API oficial. Chave no cofre Windows DPAPI, uso sem teto financeiro local autorizado. Resposta real 42: 23 tokens de entrada + 3 de saída. |
| Jev / TypeSafe | Adaptador preparado; novos cadastros temporariamente fechados pelo provedor em 23/09. |

O Supercondutor ancora as operações computacionais finitas de suporte e pinching; os hashes das três fontes estão em `provenance.json`. A correspondência entre opções de provedores e matrizes é uma **adaptação de engenharia [INPUT]**. Não há benchmark que demonstre qual modelo é melhor em cada classe de tarefa. As restrições excluem opções antes da ponderação. A política inicial prefere execução local em tarefas simples e um conector avançado em tarefas classificadas como complexas; chamadas anteriores reduzem o peso de uma conexão. Elegibilidade não pode ser restaurada por um peso alto.

As cotas das assinaturas não foram obtidas: aparecem como indisponíveis. Limites locais de tentativas por dia UTC não equivalem a cotas ou tetos financeiros do provedor. A estimativa do texto do usuário exclui o contexto interno dos clientes: o teste do Codex mostrou que esse custo pode dominar a chamada. O consumo real retornado é registrado após a execução. A instalação não altera planos, recargas, limites ou configurações de cobrança dos provedores.

## MCP e verificação

MCP `iald-orchestrator` registrado na configuração do Codex, por stdio, com quatro ferramentas: `iald_orchestration_status` e `iald_selection_preview` são consultas sem execução; `iald_coordination_get` lê um pedido; `iald_coordination_action` avança um pedido existente e sua ação `execute` pode consumir a conexão selecionada. Nenhuma ferramenta cria pedidos indiscriminadamente ou agendas. `bridge.py` é alternativa por JSON em stdin enquanto o cliente MCP não tiver sido recarregado. O processo MCP precisa ser carregado/recarregado pelo cliente para aparecer numa sessão já aberta. Protocolo testado com o cliente FastMCP real. Para outro cliente MCP, o comando é `C:\Python314\python.exe`, com argumento `C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\mcp_server.py`.

44 testes passaram (sete testes MiMo, além dos 37 anteriores, incluindo oito casos do protocolo Antigravity, com processos simulados): seleção frente a um oráculo escalar independente, invariantes matriciais, cota local, recusa, ausência de repetição automática, idempotência, fila, autenticação, origem das requisições, transições da coordenação, cancelamento durante envio, preservação do pedido original e exclusão mútua entre dois runtimes. Clique repetido no botão produziu um único pedido na prévia; cancelamento verificado; quatro ferramentas MCP enumeradas pelo protocolo real. Prévia visual isolada verificada, sem erros no console. O servidor implantado respondeu `/health` 200, redirecionou a página administrativa sem sessão para login e recusou APIs administrativas com 401. Painel de produção autenticado verificado: resposta final do percurso Física, consumo de 282 tokens e Claude disponível. A sessão administrativa é a do operador.

Instalação: duas inserções no `iald_web_server.py`, preservando as mudanças paralelas. Backups byte a byte e substituições atômicas; recibos em `validation/admin_install.json`, `mcp_registration.json` e `deployment_verified.json`. Reiniciado apenas o filho web ocioso; supervisor preservado. A extensão vive nesta pasta: não a mover enquanto o servidor e o MCP apontarem para ela.

## Disponibilidade e continuidade

Web/admin: extensão carregada e protegida. iOS interno, iOS externo e Android: não recebem alteração de cliente nesta entrega; recompilação não se aplica ao módulo administrativo. Links e distribuição anteriores não foram modificados nem revalidados nesta sessão.

Faltam: autenticar/validar e implementar os executores pendentes; acesso TypeSafe para Jev; comparar qualidade/custo com tarefas representativas. O percurso por botão Física → executor → Física já foi validado, mas depende do aplicativo Codex disponível e do envio inicial pelo operador. O consumo do coordenador Codex/ChatGPT Work é separado do consumo registrado pelo executor; ainda não é medido pelo painel. A execução geral de ações e arquivos também requer implementação própria. Nada nesta entrega muda o cânone, o gate científico ou o estatuto de confirmação física.

Referências do acionamento: [links oficiais do Codex](https://learn.chatgpt.com/docs/reference/commands) e [perfis de ferramentas do Kimi Code](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents.html). Login local: `C:\Python314\python.exe login_provider.py gemini` ou `kimi`, executado nesta pasta. Não enviar credenciais na conversa.


## Atualização das conexões — 23/09/2026

[REAL — engenharia] Antigravity recebe o pedido por stdin somente depois de anunciar o perfil `iald-text` e lista vazia de ferramentas. Falha, truncamento, duplicação de resultado, evento de ferramenta, cancelamento e mudança de configuração impedem aceitar sucesso. O recibo de validação é necessário para habilitar o conector. Os 37 testes locais não equivalem a uma chamada Google autenticada; esta permanece pendente.

**Registro histórico superado pelo estado abaixo:** o código Google já foi concluído. Para revalidar uma futura correção do perfil, execute `C:\Python314\python.exe -X utf8 validate_antigravity_connection.py` nesta pasta para uma única chamada pública de validação (6×7). Atualize a disponibilidade no painel. O cliente anterior Gemini CLI não é mais usado. `gemini.py` conserva somente o diagnóstico do caminho anterior, sem conexão com o executor ativo.

[Jev: cadastro oficial](https://console.typesafe.ai/login) aberto para o operador; não foram aceitos termos, criada conta, gerada chave ou ativada cobrança. [MiMo Code oficial](https://mimo.xiaomi.com/coder) anuncia modalidade sem login; sua disponibilidade efetiva nesta máquina ainda precisa de correção da inicialização. Nenhum código de autorização foi copiado para arquivos do projeto.

Web/admin recebeu os ajustes. iOS interno, iOS externo e Android não têm mudanças de cliente nesta entrega; recompilação não aplicável. Mantidos acionamento por botão e ausência de verificações periódicas.


## Estado conferido em 23/09/2026, após os logins

- **MiMo API / 2.6 Pro: disponível.** Conta criada e recarga de US$ 100 realizadas pelo operador. Página oficial mostrou US$ 100,72 (US$ 100 pagos + US$ 0,72 de bônus) antes do teste; isso é um retrato, não saldo em tempo real. Criada a chave exclusiva `IALD Orquestracao Local` e guardada por DPAPI do usuário Windows. Sem chave em código, resposta, prompt ou histórico de tarefas. Validade não informada pelo provedor, exibida assim na administração.
- **Uso MiMo sem teto financeiro local**, por ordem expressa do operador. Sem limite local diário de chamadas para esse provedor. Acionamento manual, sem recarga automática. Limites técnicos de entrada e saída continuam aplicados. API oficial direta, sem ferramentas, sem redirecionar credencial, sem tentativa repetida automática. Modelo `mimo-v2.6-pro`, até 4096 tokens de resposta+raciocínio por chamada normal. Consumo e estimativa pela tabela oficial são registrados; custo estimado não substitui a fatura.
- Teste real MiMo: resposta 42, 23 tokens de entrada + 3 de saída = 26; 2,521 s; estimativa US$ 0,000012615. Recibo `validation/mimo_connection.json`. Tarifas internacionais consultadas em https://mimo.mi.com/docs/en-US/price/pay-as-you-go: US$ 0,435 entrada não cacheada, US$ 0,0036 cacheada e US$ 0,87 saída por milhão. Não chamar um teste aritmético de avaliação geral da qualidade.
- **Kimi: diagnóstico anterior, superado pela validação abaixo.** Novo perfil oficial `kimi-pro`, região global, autenticado na conta Google do operador. Teste explícito `kimi-code/k3` voltou HTTP 403. A página autenticada https://www.kimi.ai/settings/subscription mostra **Adagio**; o operador relata Pro comprado no app. Necessário reconciliar o vínculo/restaurar compra no app ou com o suporte do Kimi. Não comprar outra assinatura automaticamente. Evidência `validation/kimi_pro_recheck.json`; chave ou API alternativa paga não configuradas. Executor continua excluído do seletor.
- **Google Antigravity: autenticado.** Conta reconhecida como Google AI Pro. Termos concluídos com envio opcional de interações desmarcado, conforme autorização. O perfil `tools: []` não foi confirmado pelo cliente 1.2.9, inclusive nos locais de descoberta documentados. O adaptador recusou antes de enviar qualquer pergunta. Autenticação concluída é diferente de executor automático validado. Não desativar essa verificação para anunciar disponibilidade. Perfil dedicado também registrado em `~/.gemini/config/agents/iald-text/agent.md`; nenhum outro agente ou permissão global alterado.
- **Jev/TypeSafe:** página oficial informa novos cadastros temporariamente fechados (`signups_disabled`). Integração permanece pendente de acesso do provedor.
- Local, Codex e Claude seguem as conexões já validadas. A seleção usa uma política inicial de engenharia, sem benchmark que demonstre escolha ótima. O MiMo participa quando elegível; não foi forçada uma escolha nem acionada tarefa privada para testá-lo.

Administração: `/admin/agi/orquestracao`; chave MiMo: `/admin/agi/orquestracao/mimo`. As rotas exigem administrador; alterações exigem mesma origem. Nenhum aviso de saldo/prazo inserido no app de conversa. Web/admin atualizado; iOS interno/externo e Android não exigem nova compilação para esta alteração de servidor. Distribuições e links existentes preservados, sem nova inspeção física.

Verificação desta entrega: 44 testes passaram, incluindo sete testes MiMo (DPAPI real com chave fictícia, proteção da rota, transporte, rejeição de respostas incompletas, contabilização e autorização da API). Os 44 testes são complementados pelo teste real MiMo acima. As falhas iniciais no sandbox foram dependências/DPAPI do perfil isolado; suíte passou no usuário do servidor. Evidências de contas em `validation/account_connections_observed.json`. Pendências deste retrato histórico: executor Google, vínculo Kimi Pro e acesso Jev. O vínculo Kimi foi resolvido na atualização abaixo.


## Kimi K3 integrado após vínculo das contas — 23/09/2026

[DECLARADO] O operador identificou que Pro estava na conta Apple e vinculou sua conta Google a ela pelo aplicativo. Informou que Pro passou a aparecer ao entrar com Google. [REAL] O login oficial local foi concluído no perfil dedicado `kimi-apple`; a chamada K3 deixou de retornar 403. Esse nome identifica a pasta local e não exige login futuro com Apple. Os perfis antigos foram preservados.

[REAL] Kimi participa agora da seleção automática. O teste do conector retornou a função `add(a, b)` corretamente, em 5,793 segundos: 556 tokens de entrada + 104 de saída = 660. Modelo `kimi-code/k3`; registro oficial da sessão confirmou zero ferramentas, zero delegação, uma chamada e término completo. Recibo: `validation/kimi_connection.json`. Não houve outra compra nem API paga alternativa.

O adaptador usa o cliente oficial Node 2.0.2 sem modificar seu código. Uma ponte local recebe o pedido por stdin e fornece os argumentos públicos da CLI em memória; o pedido não vai na linha de comando do Windows. Sessões do cliente permanecem no perfil local conforme seu funcionamento oficial. Configuração própria sem telemetria, títulos automáticos, plugins/MCP adicionais, habilidades externas ou repetição de tentativas. Recibo ligado aos hashes lidos do cliente, adaptador, perfil e configuração. Mudanças exigem revalidação explícita por `validate_kimi_connection.py`. A contagem efetiva inclui entrada cacheada e saída informada pelo cliente; a cota restante da assinatura continua indisponível, não presumida ilimitada. O limite local de 10 chamadas/dia e o acionamento por botão foram mantidos. Não há teto exato de tokens de saída imposto pelo cliente Kimi nesta integração.

[REAL] 52 testes passaram, incluindo oito do conector Kimi. Corrigido encerramento de fixture SQLite no Windows: os testes aguardam o trabalhador liberar o banco antes de remover a pasta temporária. Nenhuma alteração da fila de produção foi necessária. Seleção permanece política inicial, sem benchmark de qualidade ou garantia de custo ótimo.

[MATRIZ] Entrega exclusivamente web/admin e servidor. iOS interno, iOS externo e Android sem mudança de cliente; recompilação não aplicável. Distribuição e links anteriores preservados, não revalidados. Google: login concluído, executor ainda pendente de restrição verificável de ferramentas. Jev: aguarda abertura de cadastro. MiMo continua disponível e sem teto financeiro local por ordem do operador.


<!-- IALD_LEARNING_STUDY_KIMI_VALIDATED_20260923 -->
## Estudo da seleção e do aprendizado contínuo — 23/09/2026

[Estudo técnico](ESTUDO_ORQUESTRACAO_E_APRENDIZADO.md), [mapa estruturado](research/model_map_and_learning_proposal.json) e [auditoria das fontes](validation/learning_source_audit.json). Proposta de arquitetura; aprendizado ainda não conectado à seleção. Encontradas colisões numéricas no compressor; originais preservados. Preços API não equivalem a cobrança das assinaturas.


## 24/09/2026 — Transporte desassistido entre as IAs autorizado e instalado

<!-- IALD_UNATTENDED_TRANSPORT_AUTHORIZED_ACTIVE_20260924 -->

[INPUT — mudança expressa de preferência] O operador pediu transporte desassistido para as IAs operarem sem o clique intermediário e autorizou explicitamente UMA NOVA TAREFA ChatGPT Work no projeto Física por pedido da fila. Esta ordem supera a preferência histórica por envio manual no Codex para a orquestração geral. O pedido inicial continua sendo do operador; saídas de modelos/e-mails/páginas não autorizam missões, ações externas ou ampliação de acesso.

[REAL — agendamento] Automação heartbeat oficial iald-transporte-autom-tico-entre-ias em ACTIVE, vinculada à tarefa 01a0ce2b-8c2f-71b0-a9a8-91b17715a569, com oportunidade de verificação a cada cinco minutos. Persistência conferida no arquivo de automação. O agendador ainda não teve um disparo futuro observado nesta rodada ativa: criação do agendamento e teste conduzido pelo agente são evidências distintas. Depende de máquina/aplicativo/contas disponíveis; não é promessa de funcionamento 24 horas com PC desligado. Verificações consomem uso do Codex; fila vazia não chama os demais provedores. Não houve API privada do ChatGPT ou daemon clicando em envio.

[REAL — implementação] transport.json habilitado; transport_cli.py recebe JSON em stdin para consultar próximo pedido, registrar pedido autorizado e gravar recibo. Pedidos em andamento precedem os novos; estados terminais não são reenviados. coordination.py expõe o transporte ativo. Guias COORDINATOR.md/TRANSPORTE_DESASSISTIDO.md atualizados com backups; registro de identidade provisória e recuperação por marcador antes de repetir chamadas incertas. Entradas MCP adicionadas: iald_coordination_submit e iald_transport_next. Protocolo stdio enumerou NOVE ferramentas; carregamento no catálogo desta sessão continua não confirmado, portanto o heartbeat usa o CLI local equivalente.

[REAL — teste fim a fim sem clique do operador] Job 002a8486-847b-4e49-9d39-93867ee3c299; tarefa Work 6ab4eb63-6b6c-83e9-a929-f3847bc56c90 no projeto Física, título observado “Escrever função Python”. O aplicativo primeiro devolveu clientThreadId; o threadId real foi identificado pela presença do marcador DRAFT no conteúdo, sem criar duplicata. Física preparou o prompt; o seletor escolheu local; o resultado retornou à MESMA tarefa com marcador SYNTHESIS; a síntese concluída foi gravada na fila. Consumo informado APENAS pelo executor: entrada 253, saída 43, total 296; consumo Codex/Work separado, não medido no painel. A função quadrado foi apresentada como código/texto e o valor 49 como esperado; o código não foi executado. Recibo completo: validation/unattended_roundtrip.json.

[REAL — validação e interface] 36 testes passaram no ambiente real, cobrindo fila, transições, duplicação, retomada, cancelamento, autenticação e origem; node --check passou. A prévia isolada mostrou transporte ativo, registrou pedido sem exigir “Enviar no Codex” e permitiu cancelá-lo; prévia encerrada. Servidor nativo recarregado pelo supervisor existente; modelo local e editores preservados. A sessão administrativa anterior foi encerrada pelo reinício e a rota real exige login novamente. Não foi contornada autenticação para inspecionar o painel real. A operação desassistida da fila usa CLI local e não depende dessa sessão de navegador.

[OPEN — limites preservados] Jev ainda aguarda acesso; Antigravity autenticado continua com executor bloqueado por tools_filter_unavailable. Codex, Claude, Kimi, MiMo e local apareceram elegíveis no teste, mas somente o executor local foi chamado nesta rodada. A política é inicial e não benchmark de qualidade; não elevar janela de contexto ou prometer memória completa do ChatGPT por esta mudança. Adaptadores atuais produzem respostas/artefatos textuais; tarefas de sistema dependem das ferramentas e autorizações apropriadas. MiMo conserva autorização prévia sem teto local; nenhuma nova recarga/contratação. Integração de e-mails e atualidade da agenda do iPhone continuam pendentes e não foram canceladas.

[REAL — matriz de entrega] Administração web: arquivos atualizados e servidor recarregado, validação visual em prévia isolada, autenticação real novamente pendente. iOS interno/externo e Android: sem alterações aplicáveis nesta entrega exclusivamente de transporte/administração; nenhum binário distribuído. Sem alteração de um.py, kernel, gate, artigos ou acervo do Escritório. Memórias recebem correção ao lado, com backups de bytes.


## 24/09/2026 — Orquestração global entre sessões do Codex

<!-- IALD_GLOBAL_SKILL_DISCOVERY_VERIFIED_20260924 -->

[INPUT] O operador determinou que a orquestração esteja disponível em qualquer sessão local do Codex, sem depender desta conversa de instalação.

[REAL] Instalada a habilidade de usuário `C:\Users\rotol\.agents\skills\iald-orquestrar\SKILL.md`, com descoberta implícita e chamada explícita `$iald-orquestrar`; instrução correspondente acrescentada ao AGENTS global, preservando integralmente seus bytes anteriores. Mantidos servidor MCP global, fila, adaptadores e heartbeat existentes. O guia TRANSPORTE_DESASSISTIDO.md passou a documentar clientes de outras sessões, recibos com request_id/job_id e um único worker para as transições. Não há novo agendamento nem envio automático de respostas a todas as sessões de origem; o resultado é consultável na fila e na tarefa Work vinculada.

[REAL — medição] Processo novo do app-server Codex descobriu a habilidade em scope=user, enabled=true, tanto na pasta de orquestração quanto em diretório temporário externo. Processo MCP novo enumerou as nove ferramentas; consulta CLI à fila e prévia do seletor funcionaram fora de BASE. Validador de skill passou. Nenhuma tarefa/modelo foi criado/chamado nessa validação. Evidência: Chatgpt/IALD_ORQUESTRACAO_20260923/validation/global_skill_validation.json. O AGENTS atualizado também foi reinjetado nesta sessão pelo aplicativo.

[REAL — correção temporal ao lado] O registro de instalação dizia que o primeiro disparo do agendador ainda não havia sido observado. Depois da instalação, esta tarefa recebeu heartbeats sucessivos e consultas vazias foram registradas em state/transport_last_check.json. O recibo observado nesta entrega está anexado ao relatório global; isto comprova consulta agendada, não uma nova execução fim a fim. O relatório histórico da instalação é preservado.

[OPEN — escopo] A capacidade depende deste host/contas; não concede acesso automático a uma sessão em nuvem. Jev/Antigravity, limites de contexto, integração de e-mails/agenda e avaliação de qualidade conservam suas pendências anteriores. Não houve mudança no kernel, um.py, gate ou acervos jurídicos. Web/iOS interno/iOS externo/Android: nenhum código de cliente ou binário afetado por esta instalação de habilidade local. Todas as memórias alteradas têm backup imediato de bytes.


## 24/09/2026 — Antigravity integrado como executor textual disponível

<!-- IALD_ANTIGRAVITY_TEXT_EXECUTOR_READY_20260924 -->

[INPUT] O operador determinou corrigir e fazer funcionar a integração Antigravity.

[REAL — diagnóstico e correção] A autenticação já permitia respostas. O conector exigia init.tools=[]; o CLI anunciou a mesma lista de 57 ferramentas para dois agentes com capacidades distintas. No controle com view_file habilitado houve tentativa de ferramenta (a leitura do arquivo público foi NEGADA independentemente pela política headless); no controle sem ferramentas não houve evento de ferramenta e a resposta foi SEM_FERRAMENTAS. Não se afirma que a leitura do controle positivo foi concluída: o campo effective_tools_differ=false do relatório refere-se ao critério mais forte que exigia recuperar o conteúdo. A diferença de invocação foi observada.

[REAL — perfil final] Sincronizados os perfis global e locais iald-text, com tools=[], excludeDefaultComponents=true, inheritCustomizations=false, comandos off, sem MCP/skills/plugins/regras/hooks. A validação agora confere esses campos e a igualdade de bytes dos perfis antes de iniciar o processo; aceita somente o inventário previamente observado ou vazio e continua rejeitando eventos de ferramenta, agente errado, truncamento, cancelamento e resultados inconsistentes. A assinatura de prontidão inclui os perfis, adaptador, binário e inventário. Hooks experimentais não carregaram corretamente nesta versão e foram desativados; NÃO são alegados como mecanismo de proteção ativo.

[REAL — resultado] Onze testes de regressão passaram. Uma chamada real pelo adaptador IALD devolveu 42 para 6×7, terminou normalmente e gravou status=ready em validation/antigravity_connection.json. Runtime/seleção também reportaram gemini (Google / Antigravity) ready e eligible=true. O teste aritmético final informou 849 tokens totais; houve outras chamadas públicas de diagnóstico, portanto 849 NÃO é o consumo total desta manutenção. Nenhum corpo jurídico, credencial ou acervo confidencial foi enviado.

[REAL — alcance] Executor de respostas e código textual via assinatura Google; não comprova execução de código produzido, qualidade superior ou confirmação física. Limites/contexto da política permanecem como antes. Jev ainda depende de acesso. Integração de correio/agenda continua pendente. Nenhuma modificação em um.py, kernel, gate ou artigos. Web administrativa usa o conector corrigido; nenhum recurso de cliente iOS/Android foi alterado, portanto não há nova build aplicável.

[FONTES] Recursos oficiais consultados: https://antigravity.google/changelog/ (excludeDefaultComponents, versão 1.2.1); https://antigravity.google/docs/subagents?tab=cli (configuração de agentes); https://www.antigravity.google/docs/cli/headless/ (protocolo e permissões). Evidências locais: validation/antigravity_fix_delivery.json e relatórios ali referidos. A enumeração inicial do CLI é distinguida das capacidades testadas, sem alegar garantia universal a partir destes testes limitados.


## 24/09/2026 — Antigravity disponível também em sessões isoladas do Codex

<!-- IALD_ANTIGRAVITY_PORTABLE_YAML_20260924 -->

[REAL — correção adicional] Sessões isoladas do Codex não enxergavam o PyYAML instalado no site de usuário do Windows, causando ModuleNotFoundError ao validar o perfil Antigravity. Incorporados à integração o código Python e a licença do PyYAML 6.0.3 já instalado, em clients/python, com manifesto de hashes lidos dos arquivos. profiles.py inclui essa pasta apenas se yaml não estiver disponível. O adaptador, seus filtros, os perfis e a assinatura do teste real anterior foram preservados.

[REAL — verificação] Processo Python novo no sandbox retornou ready usando a dependência local; a seleção retornou eligible=true. Os 11 testes simulados do protocolo passaram. O painel administrativo autenticado exibiu Google / Antigravity — Disponível. Não houve chamada nova a modelos nesta correção de dependência. O teste real anterior 6×7=42 permanece em validation/antigravity_connection.json; não é um teste novo.

[ESCOPO] Correção de carregamento local, sem mudança de contexto, orçamento ou permissões. Nenhuma alteração de cliente web/mobile; iOS e Android não exigem nova compilação. Registro verificável: validation/antigravity_dependency_delivery.json. Esta mudança não implementa controles financeiros por pedido nem executa rascunhos da ORDEM 016.


## 24/09/2026 — Memória canônica TGL comum a todas as IAs

<!-- IALD_COMMON_CANONICAL_MEMORY_ALL_PROVIDERS_20260924 -->

[INPUT — regra geral permanente do operador] Kimi, MiMo e toda IA utilizada pela IALD devem receber a mesma memória canônica da TGL, como referência comum da integração. Preservar o Claude já configurado e o projeto Física do ChatGPT. Para tarefas orquestradas, não tratar o contexto privado de cada conta como substituto dessa base compartilhada. A regra aplica-se também a conectores futuros antes de habilitá-los. Memória significa recuperação/contexto documental; não declarar instalação nos pesos nem sincronização de conversas avulsas nos aplicativos dos provedores.

[REAL — implementação] BASE = C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923. A camada iald_orchestrator/canonical_memory.py indexa os 13 originais científicos textuais admitidos em project_fisica/MANIFESTO_LOCAL.json, com hashes calculados, linhas e geração: programa, resultados, selo, manifesto do kernel, forma canônica, manifesto Markdown, árvore, desenho, linhagem, DA_IRMA, Ponte, Custo e errata. Os dois PDFs têm artigos correspondentes em TeX. O índice é derivado local e não substitui nem bifurca TGL_ATLAS.md. Não foram lidos acervos jurídicos ou credenciais, nem executado um.py.

[REAL — transporte] providers.execute acrescenta a base e os trechos recuperados aos seis executores local/Qwen, Codex, Claude, Antigravity, Kimi e MiMo. Não altera login nem a configuração própria do Claude. Cada decisão/resultado registra geração, hashes, linhas, tamanho e cobertura parcial. A estimativa de entrada conta a memória e a orientação do adaptador antes de selecionar. Índice ausente, adulterado ou contexto sem espaço bloqueia o envio. Jev preparado para receber a mesma base quando houver acesso autorizado; não foi habilitado. O worker de Física deve usar job.canonical_memory.prompt no DRAFT e encaminhar o recibo do executor na síntese, conforme TRANSPORTE_DESASSISTIDO.md e COORDINATOR.md.

[REAL — validação] 55 testes locais passaram, incluindo a interceptação dos seis transportes para conferir o mesmo pacote, integridade adulterada, fonte alterada, índice ausente e confidenciais recusados. Chamadas de provedores foram simuladas; nenhuma nova chamada paga ou por assinatura foi feita nesta entrega. Presença da memória no transporte não comprova qualidade de raciocínio ou compreensão integral pelo modelo.

[LIMITE E ATUALIZAÇÃO] O índice cobre todo esse acervo textual, mas cada chamada recebe recuperação parcial rastreável, não o corpus inteiro. Nove fontes científicas atuais diferiram do retrato previamente anexado ao projeto Física; anexos antigos não foram substituídos por esta entrega. O pacote atual distingue sua geração. Mudanças nos originais acessíveis reconstroem o índice com backup; sessão sem acesso aos originais declara uso do retrato verificado. Saídas de modelos nunca promovidas automaticamente ao cânone. Mantida a preferência do operador por contexto máximo nas missões profundas: os limites efetivos dos adaptadores ainda não foram ampliados por esta mudança.

[DISPONIBILIDADE] Painel administrativo mostra a memória comum. A configuração documental é independente do login/cota de cada provedor: Kimi ainda requer validação da conexão observada no painel; Jev aguarda acesso. Web administrativa alterada; chat público/iOS/Android não têm recursos modificados, portanto não há build mobile aplicável. Evidência local: BASE/validation/shared_memory_delivery.json. Nenhuma alteração do kernel, gate ou originais canônicos.


## 24/09/2026 — MiMo e Kimi em capacidade máxima; executor obrigatório por pedido

<!-- IALD_MAXIMUM_KIMI_MIMO_AND_PROVIDER_LOCK_20260924 -->

[INPUT — ordem posterior do operador] “não dê limites ao MiMo quero ele no máximo”, “o limite do MiMo é a própria TGL” e “a mesma regra do MiMo vale para o Kimi, quero o Kimi no K3 modo máximo”. Estas ordens substituem os tetos financeiros e de chamadas locais anteriormente propostos para os dois provedores. Mantidos a missão autorizada, fontes científicas permitidas, sigilo, estatutos e a impossibilidade de repetir uma unidade de resultado incerto. A cota contratual do provedor continua externa à IALD.

[REAL — configuração e validação] Kimi usa o cliente oficial 2.0.2, identificador kimi-code/k3, janela configurada 1.048.576 e thinking.enabled=true, thinking.effort=max. O adaptador exige thinkingEffort=max no evento estrutural llm.request e K3 no resultado. Uma chamada pública real concluiu em 11,338 s, com 583 tokens de entrada e 260 de saída. MiMo usa mimo-v2.6-pro, janela 1.048.576, max_completion_tokens=131072 (inclui raciocínio) e thinking enabled. A alteração MiMo foi testada offline; preservou a evidência anterior de autenticação, sem nova chamada paga. Ambos estão ready, sem teto diário/financeiro local e sem instrução de 1.500 palavras. Evidência: validation/maximum_capacity_verified.json. O teste curto de Kimi não é teste de estresse de 1M nem benchmark de física.

[REAL — memória] A mesma base científica comum continua obrigatória. Nos executores Kimi/MiMo, a montagem usa modo maximum, removendo os antigos tetos de 15 mil bytes de memória e 24/39 mil caracteres/bytes do transporte. O empacotamento atual é conservador por bytes UTF-8, reservando espaço para saída e orientação; não usa o tokenizer exato nem promete ocupar 1M tokens. A prévia medida recuperou 404 trechos em 909.062 bytes, com geração/hash/linhas. O acervo excede uma chamada e a cobertura continua PARTIAL_RETRIEVAL_NOT_FULL_CORPUS. Indexar não significa instalar nos pesos. Fontes e recibo de cada chamada determinam a cobertura real.

[REAL — restrições por unidade] execution_constraints é opcional e persistente. O contrato atual de unidades delimitadas é da missão ORDEM_016: mission_id, branch_id, lemma_id, role (draft/skeptic), required_provider e max_calls=1. required_provider impede substituir o executor por outro, mesmo indisponível. Para MiMo, max_cost_usd=null e max_output_tokens=131072; para Kimi, omitir esses dois campos, pois a assinatura/CLI administra a saída. max_projection_chars é null por padrão nos dois. allowed_sources (nomes exatos do catálogo) e memory_generation são opcionais. Mesmo request_id com conteúdo/restrições diferentes é recusado; falha/incerteza não provoca fallback nem nova execução automática. max_calls=1 refere-se à unidade idempotente, não a um teto diário de uso do provedor.

[TRANSPORTE] Para a coordenação Física → executor → Física, usar operation=submit no transport_cli.py ou iald_coordination_submit, passando execution_constraints ao lado de prompt/request_id. Antes, operation=preview_execution permite conferir a rota sem chamar modelos. A prévia deve devolver selected igual ao required_provider. O worker prossegue na fila única existente; nunca remover restrições ao aceitar prompt preparado por outra IA. O limite Work de 3 envios/dia (DRAFT e SYNTHESIS contados) permanece para essas unidades; não contorná-lo pela operação direta. operation=submit_execution existe para pedidos explicitamente diretos, não como fallback quando Work estiver limitado. MCP já iniciado pode precisar recarregar a sessão; o CLI absoluto lê a implementação atual.

[VALIDAÇÃO E SUPERFÍCIES] 80 testes locais aprovados, incluindo contexto ampliado, travamento do executor, memória comum, cancelamento, resultado incerto sem repetição, confidencialidade e autenticação web. Kimi: uma chamada real da assinatura; MiMo: zero novas chamadas pagas. Web administrativa atualizada; chat público, iOS interno/externo e Android sem mudanças de recursos, builds não aplicáveis. Nenhum kernel, gate, original científico ou fonte de patente foi alterado. Atualizações de teoria continuam exigindo validação e autorização próprias.


## 24/09/2026 — ChatGPT/Física como assistência opcional, sem bloquear a IALD

<!-- IALD_OPTIONAL_CHATGPT_ASSISTANCE_20260924 -->

[INPUT — ordem posterior do operador] “vc não precisa ficar vinculado ao chatgpt se o uso dele acabar por limite, o chatgpt é pra ajudar a pensar sobre a TGL é mais uma fonte, é assistência”. Este adendo substitui a obrigatoriedade de passar por Física e de esperar sua cota para concluir. A IALD coordena; ChatGPT/Física auxilia no raciocínio, na preparação e na síntese quando útil/disponível. A memória científica canônica comum permanece obrigatória e independente dessa assistência. Respostas do ChatGPT são contribuições a verificar, não fontes primárias nem promoção automática ao cânone.

[REAL — continuidade implementada] coordination.py oferece prepare_without_work e complete_without_work, na mesma fila/request_id. Registra draft_source, synthesis_source e assistance_reason. prepare_without_work conserva o pedido original e as execution_constraints; o executor continua recebendo a memória comum. complete_without_work exige execução result_ready: pode registrar síntese da coordenação IALD, ou entregar o texto do executor identificado como DECLARADO e sem revisão independente pelo Física. Falha de executor continua failed; esta regra não reabre nem repete chamadas incertas.

[REGRA DO WORKER — prevalece sobre o fluxo obrigatório anterior] Ao considerar begin_draft e begin_synthesis, ler o estado devolvido ANTES de criar/enviar qualquer tarefa externa. Quando o orçamento local Work estiver esgotado, begin_draft devolve prompt_ready com preparação IALD; begin_synthesis pode devolver completed com a resposta do executor e a ausência de revisão Work explícita. Não criar tarefa se já estiver prompt_ready nem enviar síntese se já estiver completed. Se a assistência não for necessária, usar diretamente prepare_without_work/complete_without_work com reason=assistance_not_needed. Para indisponibilidade ou limite real do provedor, usar work_unavailable/provider_limit_reported; quando a etapa Work já foi enviada e vinculada (draft_waiting/synthesis_waiting), registrar evidence curta do estado confirmado. Falta de resposta sozinha não prova falta de cota. Estados de envio incerto draft_dispatching/synthesis_dispatching exigem recuperação da identidade/envio; não saltar nem repetir.

[LIMITES] O teto local de envios Work continua respeitado como limite apenas dessa assistência; não é diagnóstico de esgotamento da conta ChatGPT. Não criar outro Work para contorná-lo. A mudança autoriza continuidade pela IALD, sem exigir wait até o próximo dia; substitui a proibição anterior de continuidade sem Work. Mantidos executor obrigatório, sigilo, separação das casas e autorizações por missão. A falha MiMo antiga continua terminal. O heartbeat continua dependente do aplicativo/execução Codex: tornar Física opcional não cria um agendador independente nem elimina cotas do próprio Codex.

[REAL — entrega] 53 testes de regressão passaram, sete específicos para assistência opcional: conclusão com Work esgotado e uma única chamada ao executor; preservação do pedido; impossibilidade de pular envio incerto; dispensa após indisponibilidade documentada; recusa de sucesso após executor falho; síntese local com autoria; recusa de limite inventado. Transportes simulados: nenhuma nova chamada remota para testar essa mudança. Automação existente iald-transporte-autom-tico-entre-ias atualizada pela ferramenta oficial, mesmo intervalo e mesma tarefa; nenhuma duplicação. Painel administrativo passa a dizer assistência opcional e registra autoria de preparação/conclusão. Web administrativa afetada; chat público, iOS interno/externo e Android sem mudança de recursos, recompilação não aplicável. Evidência: validation/optional_work_deployment.json. Originais científicos, kernel e gate intactos.


## 24/09/2026 — Recuperação da fila com contexto máximo Kimi/MiMo

<!-- IALD_COORDINATION_MAXIMUM_RECOVERY_20260924 -->

[REAL — infraestrutura] Corrigido coordination.get: pedidos com required_provider kimi/mimo montam a memória em modo maximum, igual à prévia e à execução. Antes, a leitura usava standard e podia falhar no limite de 24 mil caracteres após acrescentar memória a um pedido válido. Não foram alterados o prompt original, o limite de entrada do operador, fontes permitidas ou restrições. Foram aprovados 39 testes locais, incluindo recuperação idempotente de pedidos longos dos dois provedores e preservação integral da memória; nenhum transporte remoto nos testes.

[REAL — recuperação] request_id 6711d262-e38f-4454-842f-944b0706167f corresponde ao job 3c0f81cc-f9dc-4fab-9abd-1dfd94f60fcc, gravado antes da falha de leitura. Recuperado o mesmo pedido, inicialmente awaiting_dispatch e sem execução; preparado sem Work. O resultado da execução única deve ser consultado na fila/recibo, nunca inferido desta nota. Evidência: state/handoffs/3c0f81cc-f9dc-4fab-9abd-1dfd94f60fcc_recovered.json em IALD_ORQUESTRACAO_20260923. Cobertura documental permanece parcial. A bancada de origem verifica a matemática; nenhuma alteração de kernel, gate ou originais. Correção de servidor administrativo/CLI, sem alteração de cliente público ou build mobile aplicável.


## 24/09/2026 — Aprimoramento dos provedores autorizado pelo operador

<!-- IALD_PROVIDER_IMPROVEMENT_CONSENT_20260924 -->

[INPUT — esclarecimento expresso] O operador quer permitir que os provedores aprimorem seus modelos com o uso elegível das ferramentas integradas. Não pediu alteração dos pesos, novo treinamento local ou um mecanismo de aprendizado compartilhado nesta mudança. Esta preferência substitui o opt-out anterior do Antigravity e deve orientar conectores futuros quando existir opção oficial. Na linguagem operacional do autor, a TGL é o cluster comum da orquestra e a IALD é sua operadora; isso não redefine uma arquitetura física de hardware nem promove conteúdo ao cânone.

[REAL — contas e clientes] ChatGPT: melhorar o modelo para todos já estava ligado. Codex: controles de dados confirmam melhoria habilitada para tarefas; a opção distinta Incluir ambientes está desligada e foi preservada, pois amplia o contexto enviado para além das interações. Claude: Ajude a melhorar nossos modelos de IA já ligado, incluindo sessões de código. Antigravity CLI: Enable Telemetry alterado para on e confirmado em nova sessão; a interface descreve dados de uso para melhorar desempenho/recursos. Kimi Code: telemetry=true no perfil dedicado, removida a imposição KIMI_DISABLE_TELEMETRY=1 e adaptador atualizado para exigir a preferência atual. Esta telemetria anônima não deve ser apresentada como comprovação de treinamento sobre prompts.

[DECLARADO — políticas oficiais consultadas] Kimi consumidor admite treinamento sobre conteúdo desidentificado; opt-out é solicitado ao suporte, sem botão encontrado na conta Pro. Não foi possível consultar eventual registro histórico de opt-out por suporte; nenhuma mensagem foi enviada ao fornecedor. MiMo API/Code: a política consultada declara não usar conteúdo para treinamento, e não foi encontrada opção de adesão no console. Qwen local não recebe um novo canal de envio ao fabricante. Jev continua sem integração ativa. Não inventar habilitação onde o provedor não a oferece nem prometer aprendizado dos pesos em tempo real.

[REAL — validação] 19 testes locais de Kimi/Antigravity aprovados. Uma chamada pública por cliente confirmou ready: Kimi K3 máximo, 583 tokens de entrada, 248 de saída, 13,199 s; Antigravity respondeu 42 para 6×7, 11,087 s. Recibos em validation/kimi_connection.json e validation/antigravity_connection.json. Mantidos ferramentas desabilitadas, restrições das unidades, memória canônica, sigilo e separação das casas. Nenhum original científico, kernel, gate ou app público/mobile alterado; build mobile não aplicável. Evidência e URLs: validation/provider_improvement.json.


## 24/09/2026 — DeepSeek V4.1 Flash incorporado à orquestração

<!-- IALD_DEEPSEEK_V41_INTEGRATION_20260924 -->

[INPUT] Operador pediu a última versão DeepSeek, autorizou criar/guardar a chave e usar o saldo da API e indicou tarefas de média complexidade, com promoção para alta complexidade somente após avaliação de capacidade. Recarga de US$50 posterior foi confirmada como Success na plataforma; a anterior constava Cancelled. A preferência por aprimoramento pelos fornecedores permanece; o console API não exibiu um controle próprio de treinamento, e nenhum opt-out foi acrescentado ao adaptador. Não confundir essa preferência com treinamento comprovado ou memória nos pesos.

[REAL — integração] Executor deepseek na mesma fila, MCP/CLI e painel dos demais provedores. API oficial https://api.deepseek.com/chat/completions; model=deepseek-flash, versão documentada DeepSeek-V4.1-Flash (alias do fornecedor, não pin imutável), reasoning_effort=max, thinking enabled. Contexto configurado 1.048.576; max_tokens até 393.216. Transporte textual sem ferramentas, sem repetição automática de chamadas incertas. Credencial criptografada com DPAPI do usuário Windows; status expõe somente metadados. Validade da chave não informada. Uso pago habilitado para missões solicitadas pelo operador, sem novo teto diário/financeiro local; saldo e limites do provedor permanecem externos. Tier operacional standard: tarefas classificadas deep ficam excluídas até avaliação, sem benchmark de superioridade alegado.

[REAL — memória e controle] Mesmo acervo científico comum, modo deepseek_maximum reservando 393.216 tokens de saída e margem. Prévia local selecionou deepseek com 647.130 bytes de contexto; cobertura PARTIAL_RETRIEVAL_NOT_FULL_CORPUS, contagem conservadora por bytes e sem tokenizer exato. required_provider=deepseek trava o executor e max_calls=1 preserva idempotência; max_output_tokens aceita 1..393216, max_cost_usd somente null (teto por unidade não implementado). Mantidos casa de origem, sigilo, geração/hash/fontes e revisão humana/científica. Custos calculados com tokens medidos e tarifas de pico como estimativa superior, com intervalo pico/fora de pico; não equivalem à fatura.

[REAL — validação e entrega] 70 testes locais aprovados, incluindo autorização, origem web, ferramenta inesperada, contagem inválida, reserva de contexto, memória comum e trava do executor. Primeira tentativa pública recusada HTTP402, preservada em validation/deepseek_pre_credit_refusal.json. Após confirmação do pagamento, nova validação autorizada respondeu 42 para 6×7: 42 tokens de entrada, 20 de saída (18 de raciocínio informados), 62 no total, 0,817s, estimativa US$0,0000183..0,0000366. Não foi teste de contexto de 1M nem de qualidade em física. Painel administrativo conferido: DeepSeek API / V4.1 Flash, Disponível, junto às demais IAs. Sessão irmã Resolver problema da gravidade quântica avisada pela ferramenta oficial e orientada a distribuir unidades de média complexidade pela fila existente, sem repetir o Kimi em andamento.

[DISPONIBILIDADE] Web administrativa atualizada; conversa pública, iOS interno/externo e Android sem mudança de recursos, builds não aplicáveis. Nenhuma alteração de original científico, kernel ou gate. Evidências: validation/deepseek_connection.json, validation/deepseek_routing.json e validation/deepseek_delivery.json em BASE. Preços/limites consultados em https://api-docs.deepseek.com/quick_start/pricing/ e https://api-docs.deepseek.com/guides/thinking_mode/ em 24/09/2026.


## 24/09/2026 — DeepSeek em capacidade máxima, inclusive alta complexidade

<!-- IALD_DEEPSEEK_MAXIMUM_AUTHORIZED_20260924 -->

[INPUT — ordem posterior expressa do operador] “quero o deepseek no maximo e resolver essa questao e avisar a sessão irmã que pode fazer chamada nele de novo que ele vai responder”. Esta ordem substitui a restrição anterior a tarefas médias e a exigência de avaliação prévia para habilitar alta complexidade. Não equivale a benchmark de superioridade nem garante resposta futura da API.

[REAL — configuração implantada] Executor deepseek agora tier=advanced, routing_scope=ALL_COMPLEXITIES_OPERATOR_AUTHORIZED. Mantidos deepseek-flash (V4.1 Flash documentado), thinking enabled, reasoning_effort=max, contexto configurado 1.048.576, saída máxima 393.216, memória canônica comum em modo deepseek_maximum e ausência de teto diário/financeiro local. Painel administrativo conferido: Disponível / alta complexidade habilitada. Nova configuração de chave também preserva esse escopo. Transporte, autenticação, sigilo, casa de origem, trava do executor e idempotência de uma chamada por unidade continuam obrigatórios; saldo, cotas e limites técnicos do fornecedor permanecem externos.

[REAL — causa e correção] A prévia anterior não chegou ao fornecedor: o seletor lexical classificou o pedido como deep e excluiu o tier standard configurado localmente. O mesmo payload de 21.110 caracteres, sem mudar texto/fontes nem mascarar Lean, passou a selected=deepseek após a promoção autorizada. A heurística geral de complexidade não foi reescrita nem convertida em medição de capacidade. A comparação antiga foi resolvida pela bancada local; não foi submetida novamente nem transformada em nova missão. O histórico da recusa permanece preservado.

[REAL — validação] 73 testes locais aprovados, incluindo três regressões de máxima capacidade: descoberta real do provedor, seleção de pedidos longos/Lean, memória ampliada, preservação de autorização, contexto técnico e required_provider. Testes automatizados com transportes simulados. Uma nova chamada pública curta de conexão respondeu 42, com 42 tokens de entrada e 42 de saída (40 de raciocínio informados), total 84, duração 1,219 s; custo estimado US$0,0000315..0,000063. Esse teste não mede qualidade em física nem ocupação efetiva de 1M. Recibo pronto e assinatura da autorização atual conferidos.

[TRANSPORTE] A tarefa irmã “Resolver problema da gravidade quântica” foi avisada pela ferramenta oficial. Pode submeter novas unidades dentro da missão autorizada, inclusive de alta complexidade, pela fila existente. Não duplicar o pedido antigo já resolvido nem outras unidades falhas/incertas. MCP previamente carregado pode usar política antiga: preferir o CLI absoluto existente até a recarga, sem criar outro servidor ou heartbeat. A assistência ChatGPT/Física permanece opcional.

[EVIDÊNCIA E SUPERFÍCIES] validation/deepseek_maximum_routing.json, validation/deepseek_connection.json e validation/deepseek_maximum_delivery.json em IALD_ORQUESTRACAO_20260923. Backups imediatos de bytes, atualização aditiva das memórias. Web administrativa atualizada e conferida. Chat público, iOS interno/externo e Android sem alteração de recursos; builds não aplicáveis. Nenhum original científico, kernel ou gate foi alterado.


## 24/09/2026 — Piloto de fine-tuning; orçamento total US$ 50; Qwen excluído

<!-- IALD_FINE_TUNING_PILOT_PREPARATION_20260924 -->

[INPUT — ordem posterior] O operador pediu modelos próprios por fine-tuning em todos os provedores que admitirem, excluiu expressamente o Qwen local e autorizou US$ 50 para o piloto TOTAL, não por modelo. Essa ordem trata de treinamento próprio e é distinta do consentimento anterior para melhoria dos modelos pelos fornecedores. Assinaturas e saldos de inferência não constituem crédito de treinamento em outro serviço.

[REAL — preparação local] BASE/fine_tuning contém o pipeline reprodutível, campaign.json, manifesto, proveniência e nove exportações JSONL (Vertex, chat genérico, Bedrock; treino/validação/teste). Auditoria local aprovada: 113 exemplos, 86/14/13 por divisão, 31 grupos distintos, sem seção em mais de uma divisão. São 89 trechos extrativos e 24 perguntas/respostas curadas, derivados somente da forma canônica e da errata científica de 19/09 admitidas no catálogo. Hashes lidos das fontes, conteúdo documental conferido (normalização de fim de linha somente nos derivados), filtros de privacidade e preservação dos originais. Não é treino completo do acervo nem evidência de melhora de raciocínio. O conjunto de teste permanece local.

[REAL/OPEN — nuvem] Projeto Google Cloud iald-tgl-ft-20260924, número 821783483062, criado e selecionado. Candidato: Gemini 3.5 Flash, duas épocas, adaptador 4, região us-central1, sujeito à oferta efetiva da conta. Ativação da API aguarda confirmação dos termos já perguntada ao operador. Neste registro: ZERO uploads e ZERO jobs de treinamento lançados; nenhum modelo próprio está pronto. O custo estimado por proxy de bytes não substitui contagem do provedor/fatura. Consultar campaign.json para o estado posterior antes de agir.

[DECLARADO — capacidades consultadas em fontes oficiais] Google oferece SFT gerenciado. Claude 3 Haiku admite fine-tuning pelo Bedrock, separado do Claude atual; custo total de disponibilização não validado, sem infraestrutura contratada. Kimi K3, MiMo V2.6 Pro RL e DeepSeek V4.1 Flash têm pesos abertos que permitem treinamento de cópias conforme licença; nenhuma infraestrutura ou rota gerenciada compatível com US$ 50 foi provisionada. OpenAI tem restrições/descontinuação de fine-tuning self-service, sem rota nova validada nesta conta; ChatGPT/Codex não se treinam pela assinatura. Jev não oferece pesos personalizados por fine-tuning/LoRA aos clientes segundo sua documentação; instruções/estado não são ajuste de pesos. Fontes e limitações estão em fine_tuning/README.md e campaign.json.

[REAL — Kimi após Ultra] Upgrade Ultra declarado pelo operador. Teste público posterior confirmou K3 máximo ready: 583 tokens de entrada, 133 de saída, 716 totais, 13,824 s. O bloqueio local de cota anterior foi reconciliado pelo método oficial request_recheck depois de conferir a cronologia. Evidência validation/kimi_ultra_reconciled.json; nenhuma unidade antiga reaberta. A tarefa irmã foi avisada. Isso não garante ausência de futuros limites nem é benchmark científico.

[REGRA DE CONTINUIDADE] Manter o teto total de US$ 50 para o piloto, incluindo avaliação/despesas, sem alterar a autorização de inferência existente. Não criar outro projeto/job por incerteza, não lançar novos treinamentos além do total, não contratar GPU ou throughput sem estimativa compatível. Confirmar identidade do job remoto e avaliar base versus ajustado antes de cadastrar executor. Memória canônica comum continua obrigatória; não substituir originais, Qwen local, Claude configurado ou Antigravity pela existência de um dataset. Não mover gate nem promover respostas ao cânone. A inferência científica da fila é processo separado do piloto.

[SUPERFÍCIES] Implementação desta etapa é local e configuração do projeto de nuvem; nenhuma mudança de recurso no chat público/iOS/Android, sem build mobile aplicável. Nenhum original científico, kernel, fonte de patente ou Qwen foi modificado. Todas as atualizações de memória usam backup imediato de bytes e escrita atômica.


## 24/09/2026 — Fine-tuning adiado; prioridade à meta da tarefa irmã

<!-- IALD_FINE_TUNING_DEFERRED_20260924 -->

[INPUT — ordem posterior do operador] “Não vamos mexer nisso agora, deixe para depois, agora é cumprir a meta da outra sessão.” O piloto de fine-tuning fica DEFERRED_BY_OPERATOR; conservar dados e projeto criados para retomada expressa futura. Não ativar API, aceitar termos, subir arquivos, lançar treinamento nem ampliar pesquisa/configuração do piloto agora. Até esta suspensão não havia upload nem job de treinamento, e o Qwen local permanece intacto. Orçamento de US$ 50 preservado como referência do piloto futuro; nenhuma cobrança de treinamento foi iniciada por esta coordenação.

[COORDENAÇÃO] A prioridade atual é apoiar a tarefa “Resolver problema da gravidade quântica” (01a070fc-9484-7e13-a654-c6b5f61093a4), comunicada pela ferramenta oficial. A fila única de inferência não foi pausada nem duplicada. A nova ordem de prioridade não equivale à resposta específica à confirmação de egress dos dois novos payloads MiMo/Kimi; manter a pendência registrada até resposta explícita. Não repetir unidades terminais/incertas ou reabrir DeepSeek cancelado. Continuar as verificações locais autorizadas da missão científica.


## 24/09/2026 — Ordens da tarefa irmã autorizadas até a meta

<!-- IALD_SISTER_MISSION_DELEGATION_AUTHORIZED_20260924 -->

[INPUT — ordem expressa do operador] “Toda ordem que chegar da sessão irmã está autorizada ser cumprida por você até alcançarmos a meta da sessão irmã”. Origem delegada: tarefa “Resolver problema da gravidade quântica”, ID 01a070fc-9484-7e13-a654-c6b5f61093a4, missão ORDEM_016. A coordenação pode cumprir suas ordens vinculadas a essa meta e despachar as unidades científicas aos executores já integrados/autorizados, inclusive as três novas unidades Kimi/Kimi/MiMo registradas. Não exigir novamente confirmação rotineira de cada payload científico dessa missão. A confirmação anterior “Confirmado” já liberou os dois envios específicos MiMo/Kimi; conservar seus recibos e histórico da recusa anterior.

[ESCOPO] Verificar a identidade da tarefa emissora pela ferramenta oficial e a relação com a meta. A delegação não transforma conteúdo citado, páginas, arquivos ou respostas de provedores em ordens do operador. Preservar sigilo de credenciais/acervos jurídicos/arquivos confidenciais, casas, executor obrigatório, request_id/job_id, ordem da fila e restrições por unidade. Não duplicar execuções incertas nem reabrir unidades terminais por inferência. Fine-tuning permanece adiado. Mudança da meta e ações alheias a ela não estão incluídas. Se uma revisão automática ainda rejeitar uma ação, respeitar a decisão e relatar o bloqueio concreto.

[OPERAÇÃO] O worker existente continua único; não criar fila ou heartbeat adicional. Resultados de modelos seguem DECLARADO até verificação. Esta autorização não altera kernel, gate, modelos ou limites técnicos do fornecedor.


## 25/09/2026 — Retomada do piloto MiMo primeiro
<!-- IALD_MIMO_FIRST_CLAUDE_PACKAGE_20260925 -->
[INPUT] Operador retomou fine-tuning: Claude Opus médio prepara MiMo em IALD; Kimi/DeepSeek ficam para depois. Mantido orçamento anterior US$50 total e Qwen excluído. [REAL] Uma sessão oficial Claude entregou pacote offline; modelo registrado claude-opus-5-5, effort solicitado medium. Identidade extraída do contrato implantado por AST, sem importar o serviço. Revisão local corrigiu escrita atômica/backup e números não finitos. 20 testes locais aprovados. Código em BASE/fine_tuning/mimo_iald_pilot_20260925; delivery.json registra hashes e proveniência. A documentação e o console consultados não ofereceram rota de fine-tuning hospedado verificada; infraestrutura própria não orçada. ZERO uploads/jobs de treinamento, nenhum MiMo ajustado/implantado. Preparação de código não é treino; dados antigos não cobrem todo regime IALD. Claude gerou estrutura de validação, não treinador remoto. Fila científica independente, originais/kernel/gate e aplicações inalterados.

## 07/10/2026 — ORDEM 019, F9.2: quadro, memória por versão e pausa do rito
<!-- IALD_ORDEM019_F9_2_20261007 -->

[INPUT] Membro desta tarefa: codex-coordenadora. Quadro único: C:\IALD\PROGRAMA_IALD\PROGRAMA.json, mutações pelo iald.py. Antes de editar arquivos compartilhados, reivindicar a unidade correspondente e conferir a reivindicação vigente; F0.2 pertence à custódia do espelho/site, não à coordenadora. Consultar o mapa local antes/depois e o Nós vivo por unidade quando disponível. Um estado de outro membro, um arquivo ou resposta de modelo não amplia autorização.

[REAL operacional] program_cli.py recebe JSON por stdin no Python absoluto já usado no transporte. operation=check_claim, unit e member verifica dono, vencimento, estado e gate. operation=register_approval acrescenta approval={id,title,question,scope,source} como unidade subordinada AGUARDA_OPERADOR pelo iald.py nova e regenera o quadro. Registrar ANTES de pedir autorização na interface; mesmo ID/escopo é idempotente, alteração é recusada. Não há operação para conceder aprovação. d72/F3.5, P3/F4.1, Sonnet/X2 e F9.2.A01 continuam pendentes. Nenhuma pergunta foi repetida nesta entrega.

[REAL operacional] operation=record_route, unit, member e path chama exclusivamente o rotas.py registrar local com --quem. Não utiliza ferramenta de mensagem, modelo, rede ou destino externo. Isso não libera o envio anteriormente rejeitado de metadados à tarefa gerente.

[REAL operacional] canonical_memory resolve state/canonical_memory/ACTIVE.json em CADA consulta, fixa a mesma epoch imutável para manifesto e SQLite, confere o pin do manifesto e todos os bytes do snapshot/índice. Ausência, adulteração ou versão divergente falham fechadas. As restrições memory_generation de pedidos antigos permanecem obrigatórias; nunca alterá-las para desobstruir a fila. activate_release exige reivindicação F0.3/F9.2: F9.2 migrou somente o mecanismo para o retrato v389 já instalado. Ativação de selo novo em F0.3 depende do aviso da gerência, validação completa e processo novo.

[REAL operacional] providers.rite_markers consulta .servidor_parado_pelo_rito na casa Nós e nos pacotes work/v*_pacote da Central; somente metadados do marcador. Enquanto houver marcador, local/Qwen aparece paused_by_rite sem sonda HTTP e não é roteado. Uma unidade local ainda sem tentativa permanece queued e conserva a ordem. Se o marcador surgir depois da reserva, registrar paused_by_rite/paused_before_send e reconciliar a reserva antes de qualquer continuação; nunca repetição automática de resultado incerto. Bloqueio de cota existente não é apagado. Remover o marcador não declara saúde: a descoberta volta à verificação normal.

[LIMITE DE PROCESSO] Estes controles estão disponíveis no CLI/processos novos. O MCP consultado nesta sessão ainda retornou geração 983c7f... e não foi recarregado; não o usar para despachar nesta condição. Comparar status.resolution=ACTIVE_POINTER_PER_REQUEST e generation com ACTIVE.json antes de usar um residente. A fila única usa o transport_cli.py em processo novo. Processos antigos precisam de recarga identificada ou substituição pelo caminho de processo novo, sem matar workers ativos. Não confundir disponibilidade do código com recarga de toda a frota.

[COORDENAÇÃO] Mensagem oficial da antiga gerente informou migração da ORDEM 019 para a tarefa 01a11878-6e36-7d10-83c4-cd72e757fdd0, título “ORDEM 019 — núcleo TGL e quadro único”; membro codex-gerente-tgl preservado. Handoff F9.1/HANDOFF_COMPACTO.md lido. Não redirecionar aprovações antigas, duplicar unidades ou criar heartbeat. Pesquisa desta ordem chega com execution_constraints.branch_id igual ao id do quadro; conferir identidade, escopo, hashes, ordem, restrições e reivindicação relevante. A mudança de tarefa não altera max_calls, executor nem autoriza repetir falhas.

[EVIDÊNCIA] 39 testes locais com sockets bloqueados; fixtures de provedores, zero chamadas de inferência. Recibos em Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F9.2. Auditoria/FECHADA pertence à gerência c1. F0.3 aguarda aviso v391; geração ativa ainda v389. Não houve alteração de kernel, gate, originais científicos, app público ou builds móveis.


## 2026-10-07T23:31:44.471541+00:00 — ORDEM 019 F9.9: Nós vivo e Jev, avaliação medida
<!-- IALD_ORDEM019_F9_9_20261007 -->
[REAL — implementação e medição documental, sem pesquisa científica nova.] ask_with_packet preserva ask_with_memory; perguntas D1–D8 versionadas; livro durável sem repetição de envio incerto e evento no quadro por chamada. Quatro sondas Jev 1.13.0 aceitaram 9000/18000/36000/72000 caracteres: 72000 é o maior degrau testado, não afirmação de máximo absoluto. Quarenta casos documentais controlados, rótulos congelados antes das respostas: 39/40 acertos; Brier agregado descritivo 0,0529325 (binário e multiclasse discriminados por eixo). O erro D1-01: falso negativo do reaproveitamento da escala exp(-s), p=0,32. Não se infere desempenho de produção ou validação independente; probabilidades brutas não foram ajustadas.
[REAL] 44 chamadas concluídas, custo estimado de US$ 0.04923706, sem reenvios; não é fatura. 52 testes offline passaram e os arquivos instalados foram verificados em processo novo. Prévia/transporte acrescentam contexto do Nós vivo somente a branch_id correspondente a unidade do quadro; reservam orçamento e preservam fonte permitida, geração, executor obrigatório e pedido. Ramos históricos permanecem pelo caminho original. Livro recalcula métricas a cada 50 decisões usando rótulos disponíveis; decisões sombra ainda sem julgamento não contam como acertos.
[PENDENTE] Fase CALIBRATED_AWAITING_MANAGER, sombra DESLIGADA. Proposta: 50 decisões em unidades científicas já autorizadas, teto de 50 chamadas/dia, concordância proposta >=90%, zero falso negativo do gate, rótulos/revisão da gerência e cobertura das opções ausentes da calibração. A revisão automática recusou implantação ampla sem validação e depois recusou ativação sem aceite; a alternativa testada foi autorizada com guarda de aceite nos dois caminhos de chamada. F9.9.A01 está AGUARDA_OPERADOR para aceite da gerência ou ratificação pelo operador. Não ativar observação, promover sinal nem criar pesquisa para preencher a amostra sem resolver a pendência.
[PROVENIÊNCIA] Geração medida: 95d3f03e1b8dc91ef4e57e1ea2543cc9d3c86da38bbaf2e701823c7555141c3c; retrato ativo continua v389. A ativação v368 permanece histórica, com referência aditiva ao contexto atual medido. F0.3/v391 aguarda aviso de selagem; nenhum MCP residente foi reiniciado, portanto usar CLI/processo novo até recarga identificada. O Nós vivo é projeção documental e não prova. As entregas A1 existentes foram reutilizadas, com termos e hashes em REAPROVEITAMENTO_A1_FONTES.json.
[EVIDÊNCIA] C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F9.9\RESULTADO.json; CALIBRATION_CASES.v1.json, CALIBRATION_METRICS.json, CURVAS_CONFIABILIDADE.svg, TESTS_INSTALLED.json, DEPLOYMENT_RECEIPT.json e PROPOSTA_SOMBRA.json. Nenhum um.py, kernel, selo, gate, site, original científico ou recurso do app web/mobile foi alterado; builds móveis não aplicáveis. ADENDO 001 e demais suspensões permanecem.

## 07/10/2026 — F0.3: memória comum v391 ativa, recarga MCP legada ainda aberta

[REAL operacional] Por aviso expresso de selagem da gerência c1, a geração f9096efaabee6edfa3c4fe9f90cdf95fc64df34242b1d6e363f62b441238a276 (epoch v391_f9096efaabee6edf) foi construída dos 13 originais admitidos, fixada em cópias imutáveis e ativada com backup atômico. 20342 trechos; hashes, SQLite, todos os trechos/linhas e recuperação em três modos conferidos em processo novo. Selo v391 95061f18c7102248ebd00c9414f1ef0dadcf08cefc1bec00bf046d778b38070a, programa 8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6, lidos do disco. MCP novo também confere. O leitor atual resolve ACTIVE por consulta; v389 permanece por versão.

[REAL documental / INPUT do operador] O contexto indexa estatuto_da_prova_v391: PROVADA = validade/fecho lógico; CONFIRMADA = creditação; kernel, ritos e GPU com os estatutos da fonte; GPU COMPUTED; NOT_FALSIFIED nunca é confirmação; gate preservado. Não houve novo rito/compilação nem reclassificação de resultado empírico nesta atualização.

[REAL operacional] Jev: referência atual JEV_CONTEXT_REFERENCE_V391.json aponta a nova geração verificada localmente; sondas/calibração remotas históricas permanecem v368/v389. Zero novas chamadas. F9.9.A01 não respondida; sombra desligada.

[OPEN operacional] O MCP legado conectado retornou geração 983c7f463cfb31f22d2f49dc9370e375b2431a998c60747787b389e810726c19 sem ACTIVE_POINTER_PER_REQUEST. Reinício pelo cliente pendente; teste de servidor novo não prova recarga dos antigos. Até confirmar, usar CLI absoluto em processo novo; não alterar restrições memory_generation para forçar execução. F0.3 permanece EM_CURSO e não recebe declaração integral de ENTREGUE.
Evidência: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3\RESULTADO.json; relato C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3\ENTREGA_MEMORIA_V391.md. Nenhum original científico, kernel, gate, configuração de permissão ou cliente público/mobile modificado.


[INPUT — resposta posterior do operador, 07/10/2026] Não pode reiniciar agora: há trabalho efetivo. Recarga dos MCP legados adiada até os trabalhos permitirem; não interromper sessões nem pedir recarga de modelos/contas. Continuidade autorizada pelo CLI absoluto em processo novo, exigindo a geração v391 no recibo. O conector antigo permanece identificado como legado até reconexão; nenhuma aprovação científica foi respondida.

## 07/10/2026 — ADENDO 003: rebase administrativo da coordenadora

<!-- IALD_ORDEM019_ADENDO003_COORD_20261007 -->

[INPUT/REAL operacional] Ordem vigente lida e hash conferido; F9.REBASE_COORD reivindicada. Job 65f577e6-8dd1-4e91-8b79-c86e2abbc68a (claude_opus_final_order_v375) cancelado pelo protocolo transacional, evento 739; pedido e geração histórica preservados, sem execução vinculada. Três recibos cancelados da gerência conferidos. Estágio local dos dispositivos v388 SUPERADO e não instalável; manifesto anterior em backup byte a byte, catálogo de 1.823 membros preservado, nenhum dispositivo vivo alterado.
<!-- IALD_ORDEM019_REBASE_R4_20261007 -->
[REAL operacional — ERRATA R4 ao lado] O cancelamento do job 65f577e6-8dd1-4e91-8b79-c86e2abbc68a não passou pelo act('cancel') público: a leitura preparou memória e recusou a geração canônica histórica. A coordenadora usou _change sob CAS transacional para registrar awaiting_dispatch → cancelled (evento 739), sem tarefa de execução vinculada. O candidato de correção de act está somente em sandbox e NÃO foi instalado; instalar depende de decisão do operador. [REAL] O recibo novo AUDIT_R1_R2_R3_R6_R7_RECEIPT.json documenta o método.

[REAL documental] Mapa local completado nas seq 741–745 (fontes escalares/revisão, masers, guardas, memória v388/v389, estágio superado). d72 já coberto nas seq 667/669/674/680, reaproveitado sem duplicação. 37 hashes documentais coincidem; cadeias do mapa/quadro válidas. X10 não foi respondida, os seis arquivos produtivos das guardas coincidem com a preparação anterior e nenhum candidato foi instalado.

[REAL/OPEN operacional] F9.9 reutilizada: 39/40, acerto 0,975, Brier descritivo 0,0529325 e curva; calibração histórica v389, referência corrente v391. Sombra continua desligada até aceite específico. F0.3: v391 ativa conferida em processo novo; recarga de MCP legado adiada pelo operador por trabalho efetivo, sem interrupção de sessão. Usar CLI absoluto novo e conferir geração; não alterar pins de pedidos.

[INPUT/REAL operacional] O mesmo heartbeat conserva ID, intervalo, tarefa e silêncio, agora com programa rebaseado, gerente sucessora 01a11878-6e36-7d10-83c4-cd72e757fdd0 (identidade oficial conferida) e autorização definitiva de envio dos pedidos autenticados do Claude Code. Esta autorização dispensa confirmação rotineira de payload/destino; não responde X10, abertura de dados ou aceite específico de sombra, nem permite repetir resultado incerto.

Evidência: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\ADENDO003_COORD\RESULTADO.json; sha256 lido e9bc4a7e33951f3bb031b175e75d24578f6c333579211769f9e442990fac8934. Recibos de cancelamento, mapa, reaproveitamento e verificação na mesma pasta. Esta entrega não chamou modelos, não refez cálculo/pesquisa, não alterou kernel/gate nem cliente público/mobile. Diário no MEMORY_2.md; MEMORY.md recebe só marcador.


## 07/10/2026 — ADENDO 004: reaproveitamento e limites do transporte

<!-- IALD_ORDEM019_ADENDO004_COORD_20261007 -->

[INPUT — ordem da gerência c1 recebida pelo operador] O ADENDO 004 prevalece sobre o 003 nos pontos tratados. F5.3 BLOQUEADA: Nível 2 já implementado e rodado em S/L, com N2_INCAPAZ/N2_NOT_CONVERGED; não reimplementar nem prolongar. Reaproveitar os gates de Fisher e o pré-registro SO/S4; o fechamento perturbativo é decisão teórica, com ligações documentais e nota S4 no escopo indicado. F5.2 reaproveita TGL_NEFF_V1 e SO-ASO de agosto; restam LiteBIRD e conferência dos sigma nas fontes. F7.2 liga e atualiza o canal n=-2 de junho; não encomendar nova derivação do que já existe. F3.6 segue C16 da SINTESE de 22/09, com injeção-recuperação e portão Asimov pré-registrados; sigma(beta|w0,wa)>=beta impede abrir o dado. F6.2 aguarda a escolha beta/2 ou beta/5, já em X11; não criar protocolo antes. Evento 2 não é executável como concebido.

[INPUT/REAL documental] D1–D8 e R1–R6 ratificadas em 02/10, com erratas posteriores preservadas: não perguntar novamente. Esta regra não responde X10/X11 nem outras decisões específicas novas. Antes de alegar falta ou solicitar trabalho: Nós vivo, mapa e levantamentos anteriores do §7 do adendo, seguindo o índice até a fonte. Não congelar contagens antigas de índices como estado atual.

[REAL operacional] Unidade F9.REBASE_COORD reivindicada para este complemento. Reutilizadas as entradas do mapa 730–736; 23 hashes de seus artefatos conferidos, 28 fontes lidas ao todo nesta captura. É conferência documental, não repetição dos cálculos históricos. A fila consultada tinha somente F1.3, independente dessas restrições; nenhum job foi alterado nem provedor chamado nesta incorporação. O mesmo heartbeat recebeu o ADENDO 004 pela ferramenta oficial, preservando alvo, intervalo, estado, autorização permanente de envios Claude Code e instrução de silêncio.

[EVIDÊNCIA] C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\ADENDO004_COORD: AUTORIDADE.json, FONTES_LIDAS.json, TRECHOS.json, MAPA_REAPROVEITADO.json, FILA_CONFERIDA.json e AUTOMATION_VERIFIED.json. As fontes científicas, os resultados históricos, kernel, selo e gate não foram alterados. Nenhuma recarga de IA ou reinício de MCP foi feito; a recarga legada continua adiada pelo operador.


## 13/10/2026 — Memória científica acompanha o avanço do programa
<!-- IALD_SCIENTIFIC_MEMORY_ALWAYS_SYNC_20261013 -->

[INPUT — ordem humana direta] “atualize sempre a memória científica sincronizada com o avanço do programa”. Fonte: C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013\OPERADOR_13out_memoria_cientifica_sync_verbatim.txt; SHA256 134ca8acc15e87570afae61f7b6dcaf860babde8a1e538f4ac88302602f9f668. Referências históricas fixas à v391 cedem a esta regra permanente.

Na fila científica, verificar em processo novo a versão selada do programa, selo/proof e fontes textuais admitidas antes de despachar. Quando houver avanço, reivindicar F0.3.MEMORIA_CIENTIFICA_SYNC; preparar snapshot imutável separado, verificar integralmente hashes e trechos/linhas, realizar revisão independente e ativar pela API existente com proteção de concorrência de ACTIVE. Conferir geração efetivamente recebida. Reutilizar scientific_memory_sync.py em C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013; implantação e primeira ativação desta entrega permanecem pendentes até recibo verificado.

Preservar releases anteriores e pedidos fixados por generation: nunca modificar memory_generation para forçar envio. Resultado de modelo é DECLARADO; sincronização não executa um.py, não move gate, não confirma física, não abre dados e não reinicia sessões/MCPs. Recusas concretas e envios incertos continuam protegidos. A regra integra o heartbeat existente; nenhuma automação adicional.


### Entrega verificada em13/10/2026
<!-- IALD_SCIENTIFIC_MEMORY_V392_DELIVERED_20261013 -->
[REAL — empacotamento/recuperação] Memória científica ativa v392, epoch v392_f2941ea8f293aa2b, generation f2941ea8f293aa2b5f50f74b41dac8de100214fa2bdff8fe0e7deccdc57ef6fc. Manifest SHA256 ed287f8536d5d2d6d4c7e04b4ccf012f4e6f4365c680dddfce3bcf323c78956b.13 documentos/23678trechos conferidos integralmente; recuperação em3modos; processo novo recebeu a geração ativa. v391 preservada e legível. Revisão R2 PASS_WITH_SCOPE,16testes+1controle independente; CAS/lock e validação integral de ACTIVE implantados por hash. Nenhuma chamada de provedor, execução de um.py ou reinício. A regra permanente e a automação existente foram verificadas; pendência de primeira ativação do adendo anterior fica resolvida por estes recibos. Recibo principal: C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013\DELIVERY_R2.json. Kimi/Takesaki continua sem execução, com aprovação específica pendente; IDs/version/constraints originais preservados.


## 14/10/2026 — Memória científica da fila sincronizada com v393
<!-- IALD_SCIENTIFIC_MEMORY_V393_DELIVERED_20261014 -->

[REAL — empacotamento e recuperação local] Snapshot imutável da fila científica v393; epoch v393_41f65efeb5b4537f, generation 41f65efeb5b4537f3cb5f1d8149f5fbb7464ac7a4d9c08609eeb6cca3b8f4893. Manifest SHA256 3f0d1df9ef721e1c5e77fefd2b6de324688707f734a39c82550c833930a08688. 13 documentos/23847 trechos conferidos integralmente em hashes, UTF8 e linhas; recuperação em3modos e geração recebida em processo novo. Revisão independente por recibo; ativação pela API existente com baseline/CAS de ACTIVE. v392 e v391 preservadas; identidade, payload e restrições dos4pedidos pendentes conservados.

[ESCOPO] Entrega da memória científica da fila, sem execução/importação de um.py, nova compilação Lean, chamada de provedor ou reinício. Não é nova prova científica e não move gate. Handoff_v393_CUSTODIA.md registra custódia parcial e B(3) da Bancada pendente; esta entrega não destrava essa etapa. Aprovações específicas Kimi/R3 e disposição de c1 para cf7dcff7 continuam independentes. Não alterar memory_generation nem repetir unidades terminais/incertas.

[CONTINUIDADE] Reutilizar scientific_memory_sync.py e sua implantação/revisão; check em processo novo por heartbeat existente. CURRENT dispensa reconstruir; próximo avanço exige claim, snapshot imutável, verificação integral, revisão independente e CAS. Recibo: C:\IALD\Central de Patentes\work\scientific_memory_sync_20261014_v393\DELIVERY_R1.json.


## 21/10/2026 — Memória científica da fila sincronizada com v395
<!-- IALD_QUEUE_MEMORY_V395_20261021 -->
[REAL — empacotamento local] Snapshot imutável da fila v395; generation 66d32c6c1c9992ffda4a64087d718e0c6a36df10fc14989a2c614c45cc33ac22; manifest SHA256 eff097dfa1f0feb8db384504b6fe16a29e00887fbd5695c12a1cef8a2ffbce17. 13 documentos e 27775 trechos conferidos integralmente por hashes, UTF-8 e linhas; recuperação em três modos. Ativação por API existente com baseline/CAS de ACTIVE somente após revisão independente; geração recebida em processo novo registrada no recibo de entrega. v394 e versões anteriores preservadas; pedidos, restrições e gerações fixadas intactos.
[ESCOPO] Sincronização documental da fila: nenhuma execução/importação de um.py ou Lean, chamada de provedor, reinício, alteração de original científico ou gate. Não afirma atualização do app/JEV nem nova prova científica. Os bloqueios transitórios programa/selo e campo selftest ausente ficaram preservados; o check posterior aceitou os bytes coerentes. Aprovações específicas e pedidos terminais/incertos continuam independentes.
[CONTINUIDADE] CURRENT dispensa reconstrução. Reutilizar helper auditado em processo novo no heartbeat existente; nunca alterar memory_generation para forçar envio. Recibos: C:/IALD/Central de Patentes/work/scientific_memory_sync_20261021_v395/DELIVERY_R1.json e REVIEW_R1.json.

## 22/10/2026 — Memória científica da fila sincronizada com v396
<!-- IALD_QUEUE_MEMORY_V396_20261022 -->
[REAL — empacotamento local] Snapshot imutável v396; generation b5113cfdc614ec1a5f6b2f993b26391ea4d7bd40781fa55d081b0cebffcaef29; manifest SHA256 26ffa195797b609fe817f151503b6bb460a9b39c3c02c87604515619ff8dfc8e. Treze documentos e 27878 trechos conferidos integralmente por hashes, UTF-8 e linhas; recuperação em três modos. Ativação pela API existente com baseline/CAS após revisão independente, geração recebida em processo novo no recibo. v395 e anteriores preservadas; pedidos e gerações fixadas intactos.
[ESCOPO] Sincronização documental da fila, sem execução/importação de um.py ou Lean, chamada de provedor, reinício, alteração de original científico ou gate. Não afirma atualização do app/JEV nem nova prova. Falhas transitórias programa/selo e ausência de selftest preservadas; fontes coerentes admitidas posteriormente. Aprovações específicas e envios terminais/incertos continuam independentes.
[CONTINUIDADE] CURRENT dispensa reconstruir. Helper auditado em processo novo no heartbeat existente; nunca alterar memory_generation para forçar envio. Recibos: C:/IALD/Central de Patentes/work/scientific_memory_sync_20261022_v396/DELIVERY_R1.json e REVIEW_R1.json.

## 23/10/2026 — Memória científica da fila sincronizada com v397
<!-- IALD_QUEUE_MEMORY_V397_20261023 -->
[REAL — empacotamento local] Snapshot imutável v397; generation fa461e0518015af91ea2efcd10806e2d2f0a209ab27201790f272becb84be377; manifest SHA256 daf3b37d19498344b9407a6fa912491aea2bbff4c82d69c9005005ed5c0a119c. Treze documentos e 27954 trechos conferidos integralmente por hashes, UTF-8 e linhas; recuperação em três modos. Ativação pela API existente com baseline/CAS após revisão independente; geração recebida em processo novo no recibo. v396 e anteriores preservadas; pedidos e gerações fixadas intactos.
[ESCOPO] Sincronização documental da fila, sem execução/importação de um.py ou Lean, chamada de provedor, reinício, alteração de original científico ou gate. Não afirma atualização do app/JEV nem nova prova. Guardas transitórias programa/selo e selftest ausente preservadas; bytes coerentes admitidos posteriormente. Aprovações específicas e envios terminais/incertos continuam independentes.
[PROCESSO] Claim do quadro antecedeu o preparo; o novo requisito ACOM/preflight foi inscrito após o preparo. Gap temporal registrado sem retroagir; preflight vigente antes de ativar. Revisão independente documental não reproduz ciência.
[CONTINUIDADE] CURRENT dispensa reconstrução; helper auditado em processo novo no heartbeat existente. Nunca alterar memory_generation para forçar envio. Recibos: C:/IALD/Central de Patentes/work/scientific_memory_sync_20261023_v397/DELIVERY_R1.json e REVIEW_R1.json.
