# Controlador Q02 — preparação39f88c04

[REAL documental] `controller.py` e `background_supplier.py` materializam o grafo da integral externa, sem outro solver. O módulo de theta continua sendo ad025, o acoplamento usa a cópia99e2, o fornecedor chama apenas o `prediction_worker` existente. A regra de integração, os modelos e as medidas vêm das fontes pinadas. Nenhum candidato foi importado/executado.

## O que está ligado

`run_once` confere bytes de plano, admissão, configuração e módulos; exige todos os nós da grade mais fina na caixa original. Cria claim global exclusivo antes de `prepare_joint`; para cada cenário, prepara o contexto uma vez e liga NodeContext → DurableNodeCallback → ThetaIntegrator. A callback consome claims de nó/fundo antes de entrar no motor. O novo fornecedor recebe `{identity,claim_nonce,references}`, seleciona o point_id congelado de theta e chama `prediction_worker(configuration, point_id, 'reference')`. Instrumenta uma chamada CAMB por fundo e emite os três bytes originais: result, receipt e packet. Não usa main/execute_worker_once/CLAIM das unidades históricas.

O cache de background inclui escopo, theta, configuração, runtime, física/protocolo e fornecedor. Entre cenários admitidos compatíveis ele permite zero novas chamadas para o mesmo fundo. Cada contexto de C/admissão mantém sua likelihood própria. Os cinco modelos compartilham um fundo por theta; não são cinco chamadas de CAMB.

A grade completa e os tetos de frio são conferidos antes do primeiro callback. Nenhum nível/orçamento foi escolhido aqui: esses números devem entrar como INPUT explícito e ser aprovados. Teto insuficiente, falha de nó, serviço, guard ou prazo encerra a unidade, sem uma integral sobre parte do prior. O resultado mantém ENGINEERING_ONLY, erros herdados não limitados, p/sigma/verdict nulos e todos os diagnósticos existentes. Famílias sintéticas pequenas não passam a ser a família científica600; o manifesto de cenários e O02 definem a lista futura.

## Ligação ausente identificada, sem autorização por flag

O worker c435 tem somente main() preso a `g.REQUEST`, `CLAIM.json`, `RUN/CASE` e `effective['points'][0]`. Não exporta `background_supplier(request)`; não foi chamado nem alterado. A adaptação isolada fecha essa assinatura específica, mas não instala um supervisor de SO.

`supervisor_port.py` define a assinatura concreta pendente: `QualifiedSupervisor.admit`, `checkpoint`, `process_identity`, `terminal_audit`. Todos são abstratos e lançam exceção por padrão. **Não existe implementação qualificada nesta pasta.** A decisão futura deve pinçar o adaptador real e a sua revisão; ele deverá autenticar autoridade ROOT/liberação de observados, módulos efetivamente carregados, runtime nativo/stdlib, guard de I/O, mapas nativos, uma thread científica, proteção/identidade dos diretórios persistentes, watchdog e limpeza do processo possuído. Receber hash/nome/flag não executa essas verificações. Hash de fonte é somente uma conferência de consistência; não é prova de bytecode ou objeto carregado.

O DurableStore atual exige POSIX local com fsync de arquivo/diretório e hardlink exclusivo. Windows é recusado. O NumPy Windows encontrado por outra unidade não qualifica esse armazenamento nem o motor que usa `resource` e o runtime CAMB Linux. É necessária uma unidade de runtime/import/FS própria para o grafo completo; o recibo histórico de um ponto não a substitui.

## Protocolo de insumos futuros

O contrato JSON e API_ESTRUTURAL listam campos exatos. `artifacts` contém buffers explícitos, JSON pinados e `source:<role>` com os bytes das fontes; o código não descobre caminhos de observados. A ROOT cria/aprova futuramente uma identidade de execução distinta, request, configuração global, planos theta e admissões. Não foram criados nesta entrega.

A física e a precisão de background são comparadas ao template consumido **como referência de bytes**; só metadados de identidade, pontos e recursos podem mudar. O escopo/proibições de background continuam limitados à predição; não se reinterpretam como autorização do controlador para observados. A integral conjunta requer sua própria decisão e fontes. Mudança da física/precisão precisa de revisão de contrato, sem ajustes silenciosos.

Para não criar um ciclo impossível de hashes, o request fixa um `coupling_template` sem a referência de autorização. A decisão fixa o hash desse request. Após verificar ambos, o código acrescenta a referência dos bytes reais da decisão ao template em memória e obtém a admissão completa99e2. Esse documento derivado é guardado no resultado durável; não é uma autoridade autogerada.

`run_store_root` e `store_root` são diretórios já existentes, absolutos, distintos e protegidos; entram no hash do request aprovado. A proteção contra mover/apagar o ledger e repetir com outra raiz pertence ao supervisor/operador, não é atribuída a uma classe Python. Um claim incompleto ou falho bloqueia; sucesso também não é reexecutado pelo controlador. Consultar recibos existentes não é retry científico.

## Recursos e terminação

Há checagens cooperativas de parede e checagem do tempo de cada fundo quando ele retorna. Uma chamada nativa travada exige watchdog externo; não é interrompida magicamente por Python. O relógio local começa depois do claim global. Carregamento/preflight/encerramento são responsabilidade do limite global externo. Memória e armazenamento nominais são INPUT; não houve medição nem quota de SO implementada. O cap por registro do store já existe e pode causar falha terminal se dimensionado mal.

A publicação final exige a auditoria original do supervisor, cinco modelos em cada cenário e contagens completas, e guarda request/decisão/admissões derivadas. Ainda exige conferência externa de exit/limpeza. Uma morte abrupta pode deixar só claim: resultado incerto, jamais nova execução automática. Não há aceitação científica por publicação de um JSON.

## Próximas dependências reais

- Revisão independente destes bytes e aceitação99e2, sem repetir controles consumidos.
- Port concreto do supervisor; qualificação do guard/runtime/FS no grafo completo e escolha de recursos/níveis como INPUT.
- Q01 matriz da gerente755c3b08, mantida separada; esta pasta não contém seus fixtures.
- Instanciação do request/admissões/configuração e eventual decisão específica ROOT para unidade realmente nova. V1 e abertura de observados continuam separados e reservados.
- Execução Q02 futura mede custo/precisão limitada na caixa inteira; preparação não é resultado Q02. Q03/certificados e relatório F4 continuam abertos.

Nenhum AUTH, CLAIM, ROOT_DECISION, observado, cálculo científico, WSL ou provedor foi criado/chamado. Originais, kernel, memórias compartilhadas e ledger foram preservados. O único exame de código feito nesta preparação é leitura, AST e hashes.
