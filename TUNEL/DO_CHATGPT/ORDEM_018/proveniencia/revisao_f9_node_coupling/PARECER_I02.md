# Revisão independente I02 — composição por nó e armazenamento durável

[REAL — revisão estática] **Nenhum bloqueador material identificado no encadeamento pinado, sob a fronteira confiável declarada.** A preparação pode seguir à decisão de ROOT sobre integração/qualificação delimitada. Este parecer não autoriza solver, grade, observados ou consumo de unidade; não qualifica por execução o filesystem ou os módulos.

Pedido1fe78df6-efb2-4c57-93bd-499ad85d8b15. Consulta prévia: mapa610. Manifesto de3510 bytes medido antes de ler as fontes; oito membros e16 pins de dependências conferidos. O recibo próprio preserva o snapshot inicial, a conferência final, backups declarados e o exame de AST. As fontes do adaptador/store foram lidas integralmente; interfaces chamadas foram confrontadas com assembler, a987, df482, ad025, I05 e formato de recibo do worker de referência.

## Composição e alternativas

A alternativa fina escolhida preserva as responsabilidades: fornecedor externo produz o fundo original; assemble_five constrói as cinco médias; PreparedJoint conserva dados/C/estrutura admitidos; df482 integra apenas os extras; o ad025 externo integra θ. A alternativa monolítica duplicaria solver, suporte gaussiano e regras numéricas, introduzindo outra linhagem sem necessidade. Uma terceira forma, callback apenas em memória, simplificaria a interface mas perderia o marcador persistente necessário após queda/incerteza. O store separado atende a esse requisito sem reimplementar a ciência.

NodeContext recebe o PreparedJoint pronto. Não lê nem constrói y/C, não altera transformações de linhas ou cria matriz. As verificações do consumidor mantêm283 linhas/63 nuisances, X, unidades, respostas, suporte afim e normalização comum. O adaptador não redefine a medida plana nem a converte em prior próprio. Exceção de engenharia propaga; não há fallback de likelihood zero.

Os três valores beta/s/rd_Mpc são âncoras explícitas admitidas dentro dos domínios do assembler, não defaults inferidos nem valores ajustados neste pacote. O mesmo θ é passado a H1–H5; cada extra é incluído apenas no respectivo modelo. H1 continua calculando β_TGL=α_CODATA_2018·sqrt(e) no assembler. H4 mantém δ=−5log10(1+s); H5 altera rd nas13 linhas BAO, preservando rstar CMB. Os priors/Jacobianos continuam no df482. O parâmetro de referência não substitui a integral do extra.

Após assemble_five, o adaptador serializa a montagem e mede o hash dos bytes realmente produzidos. Só então cria a admissão de precisão por montagem, com consumer_admission_sha256 e assembly_sha256 reais, serviços/IDs pinados e metas/tetos explícitos. Não há hash fictício do resultado, nem atualização silenciosa de tolerâncias. integrate_at_fixed_theta é chamada uma vez por novo nó.

## Interface exata com θ e perfil opcional

O descritor tem o conjunto exato de campos do ad025. São verificados inteiros, denominador diádico, nível permitido, numeradores, forma reduzida e igualdade canônica com o descritor reconstruído pela implementação pinada. Identificar só os três floats de θ seria mais fraco; o código usa também execução, contexto, callback, admissão, configuração e coordenada reduzida.

O envelope devolvido contém exatamente conditional_result e receipt. canonical_conditional_sha256 e _json_ready vêm do ad025. O único −inf numérico admitido é o log_conditional_integral com status correspondente a suporte genuinamente nulo. No cache seu tag é restaurado e a validação original é reaplicada; erro de engenharia não recebe esse tag. A cadeia liga montagem, precisão, fundo e contexto pelos respectivos bytes/hashes.

Um ThetaIntegrator efêmero é construído para reaproveitar __init__/_descriptor/_accept, com callback proibido. run não é chamado. Seu estado de validação é descartado: ele não certifica cobertura da grade nem contagem global. Essas permanecem com a instância externa. A dependência de métodos privados é real, delimitada pelo pin, e precisará de reexame se o ad025 mudar.

I05 é opt-in explícito. Sua assinatura coincide com a chamada e seu resultado vai a profile_json separado; nenhum campo extra entra no envelope θ. Preserva estimativa factível condicional, priors não aplicados, mínimo global ausente e certificados não disponíveis. Falha de perfil habilitado aborta o nó. O perfil não constitui substituto da integração dos extras ou autorização para nova busca.

## Identidades e fundo comum

O node_id vem do plano original. O claim acrescenta descritor, admissão I02 e hash do plano. Reusar a mesma chave mudando âncoras, precisão ou admissão dá conflito, sem renovar automaticamente o nó.

A identidade de fundo inclui scope_id, θ, configuração, runtime, engine, protocolo e referência do fornecedor. Não inclui cenário/y/C, perfil ou âncoras dos extras, pois esses não mudam o fundo. Assim, cenários com contextos diferentes podem usar o mesmo fundo completo em θ idêntico sob a mesma autorização/configuração. Mudanças nesses componentes da identidade produzem outra chave; isso não concede autorização a essa nova chave.

O fornecedor retorna exatamente packet_json/result_json/receipt_json, em bytes originais. O adaptador confere a cadeia de hashes, igualdade do resultado do packet, θ, runtime/configuração/engine/protocolo, scope/nonce e contadores inteiros1/1. O schema do recibo coincide com a construção estática do worker usado como referência. Não se leu ou reutilizou sua saída científica. O recibo ENGINEERING_BACKGROUND_RETURNED é intermediário: o guard de aceitação externo precisa conferir término/auditoria/coleta antes da publicação.

c435/ffd6 são recusados expressamente como novo background_scope_id. A lista não é o ledger inteiro; a vedação de repetir qualquer outra unidade terminal/incerta continua dever do controlador. Q01 consumido não foi executado nem reaberto nesta revisão, e seu PASS finito não se torna certificado uniforme do I02.

## Claims, publicação e cache

DurableStore exige raiz absoluta existente e POSIX; não cria raiz nem oferece emulação Windows. Cada claim é criado com O_EXCL/O_NOFOLLOW e sincronização do arquivo e do diretório antes de devolver propriedade. Um concorrente não se torna segundo dono: encontra cache completo ou recebe recusa de pendência/falha/incerteza. Um arquivo parcial conserva a ocupação. Result/failure sem claim é órfão recusado.

No callback, NODE_ACCESS precede o claim do nó. O claim do fundo antecede BACKGROUND_EXECUTION e a única chamada ao fornecedor. Validação dos originais e BACKGROUND_ACCEPTANCE antecedem commit do fundo. Só depois se computa a montagem/prior e se publica o nó. Fundo já aceito pode sobreviver a uma falha posterior do nó, mas o nó falho não é recalculado automaticamente. Se outro cenário chegar enquanto o fundo ainda está pendente, a política é recusa conservadora, não espera/retry: o controlador deve planejar a ordem de consumo.

O resultado é primeiro escrito em temporário exclusivo, com fsync de bytes e diretório; hardlink publica sem substituir destino existente; fsync do diretório confirma essa etapa. O temporário permanece deliberadamente. claim_sha256, tamanhos, hashes e base64 validado ligam os bytes armazenados. JSON com chave duplicada/não finito e estado failure conflitante são recusados. O cache exige todos os arquivos do nó, o fundo completo e suas validações. Não executa fornecedor, montagem, prior ou perfil para completar lacunas.

O recibo de reuso diz VERIFIED_DURABLE_CACHE e zero chamadas deste callback. Os bytes originais e o recibo original1/1 permanecem intactos. Hash do resultado condicional não depende dessa alteração do recibo externo de uso. A instância θ externa continua recebendo o envelope exato e mantém seus contadores.

## Fronteiras e limites que o aceite preserva

1. **Compatibilidade antes de gastar:** NodeContext confere o hash da admissão do joint e do plano, mas a igualdade joint._admission['prediction_admission_sha256'] == plan['assembly_admission_sha256'] só é imposta posteriormente em PreparedJoint.evaluate_five (likelihood_consumer.py:347–350). Uma combinação incompatível falha fechada, porém pode já ter consumido um fundo antes dessa detecção. O contrato já atribui a NODE_ACCESS a conferência de autorização de acesso/reuso e de contexto/configuração, mas não enuncia essa comparação específica como check local do construtor. Recomendo concretizar esse dever no controlador por essa igualdade antes da chamada; uma futura validação antecipada local também seria possível. Isso é recomendação rastreável de implementação, não novo requisito de permissão nem evidência de guard já implementado. Não é caminho de sucesso científico incorreto, mas o construtor não deve ser anunciado como preflight completo de todas as combinações.

2. **Código e execução confiáveis:** SOURCE_PINS, REQUEST_ID, isinstance e referências em JSON não autenticam objetos Python arbitrários. O chamador precisa conferir os módulos carregados e o guard real. NODE_ACCESS trata acesso/contexto; BACKGROUND_EXECUTION trata autorização nova, orçamento global durável e limites/processos; BACKGROUND_ACCEPTANCE confere recibos terminais, auditoria e coleta. Retornar None de um guard vazio não cria essa evidência. O próprio fornecedor precisa conservar os originais das chamadas falhas.

3. **Durabilidade condicionada:** O_NOFOLLOW cobre o componente final aberto e a raiz direta é verificada contra symlink; o código não é confinamento contra substituição hostil de diretório/ancestrais ou proprietário malicioso. “Links inesperados” na nota deve ser lido nesse alcance, sem alegar inventário de todos os hardlinks externos. Um store protegido e filesystem local qualificado são premissas. fsync/hardlink presentes na fonte não medem comportamento real após crash/perda de energia.

4. **Falhas persistentes:** Uma falha de publicação/sincronização propaga e tenta registrar failure; se o próprio filesystem impedir esse registro, não há prova local completa do término. Não apagar claims nem inferir liberação da ausência de failure. A reconciliação de erro/incerteza e o veto de reutilização após falha terminal externa pertencem também ao guard/ledger. Este pacote não fornece transação distribuída ou garantia infalível contra interrupção entre instruções. Os fluxos normais preservam a recusa em vez de repetir o solver.

5. **Recursos e validade:** max_record_bytes limita cada registro lido/escrito, não RAM máxima, número de nós, espaço total ou duração. A montagem do JSON/base64 em memória antecede a checagem final de tamanho de publicação. Tempo/CPU/RAM/deadline/paralelismo e quotas totais são externos. O adapter/store não contém launcher nem os enforce. ENGINEERING_ONLY, UNBOUNDED_THEORY_ERROR e MM/V1 condicionais permanecem. Não é exigido certificado uniforme para produzir estimativas honestas, nem atribuído um certificado inexistente.

[REAL — atividade desta revisão] Apenas leituras, hashes, AST e confronto documental/algébrico. Nenhum import/instância dos candidatos, store, guard, solver, matriz, WSL, provedor, dado observado, AUTH/CLAIM ou controle numérico. Arquivos do autor, ledger e memórias compartilhadas ficaram intactos. Os checks do recibo próprio são estruturais, não testes de execução/crash/concorrência. Parecer favorável restrito à preparação pinada, com as obrigações externas e os limites acima preservados.
