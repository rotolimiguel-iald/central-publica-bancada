# I02 — ligação por nó da investigação F9

Pedido 1fe78df6-efb2-4c57-93bd-499ad85d8b15. [REAL — preparação estática] A identidade foi persistida ANTES do código em PREPARATION_IDENTITY.json. Nenhuma execução científica, importação candidata, observação, WSL ou provedor foi feita nesta entrega.

## Alternativas e composição

A alternativa escolhida é um adaptador fino com módulos pinados injetados e armazenamento durável separado. A alternativa monolítica, que copiaria o solver de fundo, a geometria gaussiana e os integradores, foi rejeitada. I03 (cenários/C) e Q01 (qualificação) permanecem com seus responsáveis; não foram implementados de novo.

Em cada θ, a composição é: fornecedor externo do fundo → assemble_five → PreparedJoint/df482.integrate_at_fixed_theta → envelope exato do ThetaIntegrator. Um mesmo fundo alimenta H1–H5. O PreparedJoint mantém C inteira, X, 283 linhas, 63 nuisances, suporte, offsets e medida; ele é recebido pronto, nunca reconstruído pelo adaptador.

Os parâmetros de referência β/s/r_d são entradas explícitas, sem defaults. Eles ancoram as curvas dos extras; não substituem os priors nem ajustam β_TGL. O montador continua calculando o β fixo como α√e. A integração dos extras permanece no df482 e a integração externa em θ permanece no ad025. A precisão recebe uma admissão por montagem com o hash REAL da montagem produzida; não é usado hash provisório como se fosse resultado.

O perfil I05 passou pela revisão independente596 e pelo aceite ROOT598, exclusivamente ENGINEERING_ONLY. Quando profile_enabled=True, a API pinada produz um arquivo profile_json separado. O envelope de θ NÃO recebe campos adicionais. A opção é explícita e não calcula mínimo global ou certificados. Falha do perfil habilitado invalida o nó inteiro; não se entrega uma coleção parcial como sucesso.

## APIs

NodeContext(joint, *, admission_json, admission_sha256, theta_plan_json, theta_plan_sha256, assembly_admission_json, design_json, layout_json, assembler_module, consumer_module, prior_module, precision_module, theta_module, profile_module=None).

É o componente sem I/O. Recebe bytes já admitidos e módulos já carregados/verificados pelo chamador. Confere schema, pins, plano, contexto, configuração/runtime, estrutura, referências dos serviços, limites e âncoras. Não importa módulos por nome nem autentica objetos arbitrários a partir de atributos. SOURCE_PINS é preenchido pelo empacotador a partir de bytes lidos; o chamador futuro deve conferir os objetos efetivamente carregados.

A admissão F9_NODE_COUPLING_ADMISSION_V1 contém exatamente: schema, preparation_request_id, source_pins, theta_plan_sha256, anchors={beta,s,rd_Mpc}, precision, runtime_sha256, background_scope_id, supplier_reference, loaded_objects_reference, external_execution_authorization_reference, resource_limits_reference, profile_enabled. As referências são {id,sha256}; referências/strings não constituem autorização. O template precision contém services, os dois tetos de avaliações, as três metas de erro e caller_verification_reference do df482. Não há tolerâncias escolhidas automaticamente.

DurableStore(root, *, max_record_bytes) é o armazenamento separado. Exige diretório absoluto existente, protegido e em filesystem POSIX local previamente qualificado. Exige fsync de arquivo/diretório, O_EXCL, O_NOFOLLOW e publicação sem substituição por hardlink. O código não cria diretório raiz, não cria launcher e não oferece fallback silencioso para Windows nativo, filesystem remoto ou backend sem essas garantias. A qualificação do filesystem concreto pertence ao controlador; os flags POSIX sozinhos não provam durabilidade contra perda de energia em todo ambiente.

DurableNodeCallback(context, store, *, background_supplier, execution_guard) é o callback para evaluate_node do integrador existente. Recebe o descritor original e devolve exatamente {conditional_result,receipt}. O descritor é reconstruído com o método pinado _descriptor e a coordenada diádica canônica; comparar somente três floats seria insuficiente para identificar um nó.

## Fornecedor de fundo e fronteira de execução

background_supplier(request) é injetado e deve devolver exatamente três bytes JSON ORIGINAIS: packet_json, result_json e receipt_json. request liga identidade do fundo, nonce do claim persistido, autorização externa, limites e objetos carregados. O fornecedor é responsável por uma única chamada real e pela preservação externa de seu controle terminal. Não há implementação de fornecedor/launcher novo nesta pasta.

O formato do recibo de motor consumido é o já presente no worker c435: status ENGINEERING_BACKGROUND_RETURNED, request_id, nonce, configuration_sha256, runtime_sha256, background_result_sha256 e contadores solver_calls_attempted/returned. São exigidos 1/1, observed_reads=False e uniform_error_bound=None. O pacote deve apontar para o hash dos bytes desse recibo; seu result deve coincidir com o resultado original, e θ/runtime/configuração/engine/protocolo devem coincidir com a identidade pedida. Os bytes originais são armazenados, não reconstruídos para aparentar custódia.

O recibo ENGINEERING_BACKGROUND_RETURNED é intermediário e não prova sozinho saída limpa/recolhimento de processo ou ausência de falha de auditoria posterior. Por isso execution_guard é obrigatório, com três fases:

1. NODE_ACCESS: conferir autorização de leitura/reuso, contexto, código realmente carregado e configuração.
2. BACKGROUND_EXECUTION: conferir nova autorização externa, orçamento global durável, deadline/RAM/CPU/processos e nonce ANTES da chamada, já com claim persistido.
3. BACKGROUND_ACCEPTANCE: conferir e preservar externamente os recibos TERMINAIS, resultado final/auditoria/recolhimento do executor e cadeia dos bytes retornados ANTES de publicar o fundo como reutilizável.

O guard retorna None somente após suas verificações ou lança exceção. Não é substituído por um booleano de admissão. Sua realização operacional está fora deste adaptador: uma função vazia fornecida por um chamador não confiável não certifica nada. A identidade/pin do guard pertence ao controlador e às referências congeladas. O fornecedor e o guard devem conservar também originais de chamadas falhas; o marcador local de falha conserva tipo/código, sem inventar recibo de sucesso ou repetir para recuperar uma saída perdida.

c435/ffd6 continuam consumidos. Sua admissão de UM ponto não autoriza grade. O adaptador recusa esses IDs como novo background_scope_id, mas não pretende conhecer sozinho todo o ledger de unidades consumidas: o guard deve consultá-lo. Não existe renomeação automática para contornar falha.

## Duas identidades e máquina durável de estados

O claim do nó usa node_id e liga descritor, hash da admissão I02 e plano θ. Alterar âncoras/precisão/entrada mantendo o nó antigo causa incompatibilidade explícita.

O claim de fundo usa hash de scope_id, θ, configuração, runtime, engine, protocolo e fornecedor. Exclui cenário/y/C e âncoras dos extras, pois esses não alteram o fundo. Assim, cenários distintos podem compartilhar um fundo já completo sob a mesma autorização/configuração. Não se compartilham fundos entre configurações ou θ diferentes.

Ausente → criação exclusiva de claim → bytes/fsync de arquivo e diretório → permissão externa/chamada única → validação → resultado publicado. O_EXCL e a persistência precedem qualquer chamada ao fornecedor. Concorrentes não são donos do mesmo claim. Claim pendente, parcial, falho ou incerto nunca dispara retry. A ausência de resultado não é prova de que o solver não foi chamado.

O resultado é escrito primeiro em arquivo temporário exclusivo, sincronizado e publicado por hardlink sem sobrescrever. O link temporário permanece para recuperação explícita; não há limpeza automática. Erro de publicação/fsync propaga e deixa o claim consumido. Arquivos órfãos, links inesperados, JSON truncado, hash/tamanho divergente e conflito de falha com resultado são recusados. A proteção presume o diretório controlado e o filesystem qualificado; checksums não são assinatura contra um proprietário malicioso do filesystem.

Somente um resultado completo, consistente e validado é cache. No reuso, os bytes originais permanecem intactos; o recibo devolvido NESTE callback diz VERIFIED_DURABLE_CACHE e background_calls_this_callback=0. O recibo original do motor continua com 1/1. Não se relança fundo, montagem, integração de extras ou perfil para preencher um cache aceito. Se o nó falhar depois de o fundo ter sido aceito, o fundo permanece preservado, mas o nó não é repetido automaticamente.

## Envelope, hashes e limites

O adaptador reutiliza canonical_conditional_sha256 e _json_ready do theta_integrator. O único −inf legítimo é marcado como {$float:"-inf"} no campo log_conditional_integral correspondente. Ao ler cache, o tag é restaurado e a validação original é reaplicada. Na saída opcional I05, log_profile_deta usa um tag separado, sem interferir no hash do resultado condicional.

Um ThetaIntegrator efêmero e real é usado somente para sua validação _accept, nunca run. Isso reaproveita a validação exata do envelope sem duplicar o integrador. Seus contadores de validação são descartados; a instância externa mantém a contagem/cobertura real da grade. Essa dependência de API privada é explícita e presa ao hash do ad025. Não certifica cobertura global por nó.

O store conserva envelope, montagem, precisão e perfil opcional; o fundo guarda os três originais. Tamanhos por registro têm teto explícito. Quota total, número de nós, memória máxima, tempo e paralelismo são responsabilidade do controlador/guard, não garantias inferidas de max_record_bytes. Os limites já existentes do plano θ e dos serviços são preservados. Não foi feito benchmark de desempenho, teste de crash/concorrência ou teste numérico nesta preparação.

MM/V1 seguem condicionais; ENGINEERING_ONLY e UNBOUNDED_THEORY_ERROR são preservados. Nenhum status de cache, chamada bem-sucedida ou revisão estática produz sigma ou confirmação física. Esta entrega não abre observados nem o stack remoto. Antes de consumo: revisão independente do encadeamento/claims/recuperação e qualificação delimitada do que mudou, sob decisão própria de ROOT. I03 e Q01 não são duplicados.
