# Parecer local — acesso compartilhado da bancada e executores IALD

Autoria: chatgpt-codex/ordem-018/proveniencia. Revisão documental local, por delegação ROOT, de pedido da gerente oficial 01a070fc-9484-7e13-a654-c6b5f61093a4. Não é resposta nova de MiMo, Kimi ou DeepSeek. Data, bytes, SHA-256 lidos e trechos estão em EVIDENCIA_ARQUITETURA.json.

**Conclusão:** há infraestrutura reutilizável para várias sessões locais coordenarem a mesma missão, preservarem IDs e receberem contexto científico rastreável. A fila de provedores entrega texto. O MCP da Bancada Um é um canal separado, acessível a clientes locais aos quais foi registrado, e pode acionar cálculo real. A fonte consultada não liga automaticamente os executores textuais da fila a esse MCP. Acesso disponível não autoriza abrir dados, repetir unidades ou iniciar uma análise científica.

## 1. O que cada camada realmente oferece

[REAL — inspeção de fonte] BASE = C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923.

- iald_orchestrator/providers.py:15–19 manda usar apenas o contexto fornecido e produzir texto; execute:149–164 confere o hash do pacote e o executor obrigatório. Nas linhas 206–214, Codex roda isolado com recursos de ferramentas desabilitados; Claude recebe tools vazio e configuração MCP vazia. Isso descreve esse adaptador, não todas as capacidades dos aplicativos Codex/Claude.
- Kimi: kimi_text_agent.md tem tools: [] e subagents: []; kimi.py:40–50 recusa arquivos de extensões/MCP no perfil e confere o cabeçalho; linhas 81 e 103–105 recusam respostas com tool_calls e inventário não vazio.
- MiMo e DeepSeek: enviam mensagens de texto sem catálogo de ferramentas; mimo.py:75,155 e deepseek.py:68 recusam saída de ferramenta. MiMo trata o fluxo SSE, mas não despacha ferramentas da bancada.
- O ramo gemini ativo em providers.py:181–185 utiliza antigravity.py. O perfil esperado deste exige tools=[], commandExecutionPolicy=off, mcpServers=[] e skills=[]; há verificações de eventos. gemini.py/settings legados não são a prova principal do ramo ativo.
- A montagem de memória é recuperação documental: canonical_memory.py:328–331 devolve geração, fontes/linhas/hashes, hash do pacote, tamanho, cobertura PARTIAL_RETRIEVAL_NOT_FULL_CORPUS e weights_modified=false. Receber uma fonte não significa executá-la nem consultar dados residentes.

[REAL — fonte] C:\IALD\Bancada_Um\mcp_um.py declara servidor FastMCP em stdio e encaminha chamadas a BANCADA_UM_URL, padrão http://127.0.0.1:18777, com X-Cliente derivado de BANCADA_UM_CLIENTE (linhas 18–32). Clientes locais configurados podem compartilhar o mesmo serviço e resultados residentes. Isso é diferente do executor textual invocado pela fila. Ler o nome de um caminho em um prompt remoto não concede acesso ao disco/localhost do operador.

A interface não é somente leitura: avaliar é diagnóstico; ajustar/comparar/amostrar declaram efeitos no livro; gw_rodar lança uma rodada e sua descrição reserva o uso à gerência. rotas_* usa diretamente o módulo local do mapa, sem depender do servidor HTTP. neff_canal importa a implementação local e, se controle=True, chama controle adicional. Nenhuma dessas ferramentas foi chamada nesta revisão.

## 2. Quem faz ciência, proveniência e limites de idempotência

[INPUT — contrato operacional; REAL — fonte que o implementa] A gerente científica define a unidade, confere contribuição externa e conduz as ações científicas autorizadas pelas ferramentas/contratos próprios. O heartbeat Codex gere as transições da fila. O serviço da bancada ou o executor local de uma unidade concreta realiza o cálculo; o LLM formula, propõe e interpreta. ChatGPT/Física é assistência opcional. Um texto final/completed da fila não é recibo de solver nem validação física.

A skill iald-orquestrar e GESTAO_MULTIGESTOR.md:3–6,19–38 já descrevem fila persistente compartilhada, controlador substituível e autoridade limitada à missão. Não é necessário instalar outra fila/heartbeat para cada agente.

[REAL — fonte da fila] coordination.py:33–62 e runtime.py:142–177 preservam request_id UUID, comparam pedido/restrições e rejeitam reutilização divergente. Transições são condicionadas ao estado dentro de BEGIN IMMEDIATE e registradas em coordination_events (101–114). O identificador da execução deriva de uuid5 do job (coordination.py:175). Runtime registra tentativa antes da chamada (303–309), uso/retorno depois (311–325); running sem proprietário atual fica incerto, sem retry automático (218–241). Limites da fonte: cinco coordenações não terminais; até três execuções e uma por provedor elegível. Estes são mecanismos de coordenação; não garantem exatamente uma execução remota em qualquer falha de rede.

[REAL — limite da interface MCP, não auditoria do servidor] mcp_um._req não recebe request_id/claim/chave idempotente nem faz retry explícito. X-Cliente é etiqueta de proveniência declarada por variável de ambiente, não identidade autenticada demonstrada. O wrapper não comprova deduplicação de ciência no backend, autenticação ou execução dos guardas que a descrição recomenda. Erro/timeout devolvido não demonstra que o servidor deixou de executar. O livro mencionado documenta tentativas, mas não substitui a identidade e o contrato de cada unidade. Não transferir as garantias da fila para chamadas MCP diretas nem supor que todos os endpoints têm os mesmos efeitos. Backend científico e seu estado residente não foram consultados.

## 3. Evidência pronta que pode ser reutilizada

Os recibos abaixo foram lidos e pinados fisicamente. São registros históricos, não testes reexecutados nem prova do estado residente atual.

| Artefato em BASE | O que registra | O que não mede |
|---|---|---|
| validation/global_skill_validation.json | Descoberta da skill a partir de duas pastas; enumeração MCP da orquestração; CLI em pasta diferente; zero modelos chamados. | Não testa ferramentas científicas da bancada ou clientes remotos hospedados. |
| validation/shared_memory_delivery.json + test_canonical_memory.py | Recibo de 55 testes, seis transportes interceptados e zero chamadas novas; contexto com geração/fontes/hash/cobertura. O teste test_every_executor_receives_same_packet_without_network usa mocks. | Não é 55 chamadas científicas, leitura integral do cânone ou medição de qualidade. A geração de 24/09 não certifica a atual. |
| validation/optional_work_deployment.json | Recibo de 53 testes e continuidade sem Work; autoria de preparação/síntese explícita; zero novas chamadas de provedores. | Não mede qualidade da síntese ou disponibilidade corrente do Work. |
| validation/provider_parallelism_delivery.json + validation/test_provider_parallelism.py | 34 testes focados; regressão inicial 52 passados/4 erros de ambiente Flask; depois dois jobs documentados em running. | Retrato de ativação, não benchmark de throughput ou latência científica. O recibo conserva a limitação anterior “No live concurrency measured yet” ao lado do adendo de ativação. |
| validation/antigravity_text_boundary_probe.json | Probe histórico: zero eventos de ferramenta, target_created=false, uma resposta SEM_FERRAMENTAS; conversation_id 3682d35a-d377-474a-bffe-dd1fd550bc89. | Um caso não prova isolamento absoluto, disponibilidade atual ou acesso à bancada. |
| validation/unattended_roundtrip.json | Ida e volta concluída do pedido 2f2953ae-eea4-48d6-8d45-b9df8efedd87, job 002a8486-847b-4e49-9d39-93867ee3c299, execução fd45ea28-5a6e-4664-9b31-ce6312418634; resultado distingue código produzido de código não executado. | Transporte de tarefa simples; não ciência ou ganho comparativo. |
| ORDEM_018_TESTE_SENSIBILIDADE/D10_LOCAL_AUDIT.md | Auditoria já feita dos pareceres Kimi e MiMo, com correções ao lado e remissão a conferência posterior da gerente. | Não é nova revisão matemática nesta entrega nem ensaio causal de acesso compartilhado. |
| ESTUDO_ORQUESTRACAO_E_APRENDIZADO.md:23,101–135 | Já separa geração textual, cálculo por ferramentas e proposta de avaliação; declara ausência de benchmark local comparativo. | Diagrama de arquitetura proposta não comprova ferramentas ligadas ao executor. O estado histórico de contas/cotas foi superado em outros adendos. |

Exemplo concreto reutilizável D10, sem repetir análise: o parecer local corrige a extrapolação de um texto Kimi de inclusão de modelos para p_j=1 e mantém propostas do MiMo como não medidas. Assim há evidência documental de que contribuição remota foi recebida, identificada e submetida a crítica local; isso não estima a frequência de acertos nem o contrafactual sem o arranjo compartilhado.

IDs D10:
- Kimi: request 890e3e2e-6b0f-420d-b3a9-c7c8b1aad169; job 64445a89-f77e-4680-8238-6940506a348b; execução 0044ef5f-4254-4a46-b064-7a65a8af677d.
- MiMo: request 831080d9-fb42-4dbb-a6c2-45f577ec73a0; job ad831f74-48b8-4a66-ba7b-a5e800d6b88b; execução fc360dbe-a9f7-445f-9ab8-95bbf0e1941c.
Os textos D10 foram conferidos apenas por bytes/hash nesta revisão; o exame científico anterior foi reutilizado como registro, não repetido.

## 4. Benefício demonstrado versus não medido

[REAL — fontes/recibos] Já existe capacidade de compartilhar estado persistente entre sessões locais, rastrear contexto documental, preservar identidades e recuperar resultados sem recriar automaticamente o pedido. Há exemplos históricos de transporte concluído e correção local de respostas externas. Esta base satisfaz o pedido de explicar a arquitetura e suas vantagens operacionais sem repetir ORDEM018.

[DERIVED — benefício de engenharia] Usar uma bancada comum permite referenciar o mesmo serviço/contrato e reaproveitar evidência existente. Reduzir deriva entre cópias ou trabalho repetido é uma vantagem esperada desse desenho; esta revisão não mediu sua redução quantitativa.

[OPEN] Não foi localizado, no conjunto documental delimitado examinado, experimento que estime ganho de acurácia, tempo total, custo ou produtividade científica causado pelo acesso compartilhado, nem comparação controlada com/sem bancada para os provedores. O estudo antigo propõe isso; não o conclui. Não afirmar que ferramentas melhoram automaticamente o raciocínio ou que a independência de duas respostas ficou garantida. Compartilhar dados/código também compartilha possíveis erros sistemáticos.

Não é preciso repetir testes ou abrir uma campanha para responder ao pedido documental presente. Uma futura mudança para permitir ferramentas ao executor remoto seria alteração de interface/escopo, não simples ativação do que a fila já faz. Esta revisão não a solicita nem autoriza.

## Limite e custódia desta entrega

Somente leitura de fontes/documentos/recibos e gravação destes artefatos na pasta própria. Zero provedores, HTTP/API da bancada, operações de fila, execução/importação de um.py/candidatos, cálculos científicos, arrays/catálogos, mapa, ledger ou memórias globais. Fontes evolutivas são identificadas pelo snapshot lido, não declaradas imutáveis. A conferência ROOT de processo novo/residente, memória e provedores é outra frente: não foi presumida ou duplicada aqui. Parecer local/documental, sem novo veredito ou autorização científica.
