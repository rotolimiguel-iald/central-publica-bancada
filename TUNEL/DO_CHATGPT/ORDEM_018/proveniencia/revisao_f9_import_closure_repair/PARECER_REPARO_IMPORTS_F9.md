# Revisão independente do reparo finito de imports F9

**Conclusão: nenhum bloqueador acionável identificado no delta examinado.** [REAL — leitura, hashes e AST] O pacote está apto a uma decisão separada da coordenação sobre a execução proposta; este parecer não a autoriza. O fechamento conferido trata as dependências concretas e a sonda de ausência reveladas por ffd6. Não certifica uma importação já bem-sucedida, todas as dependências dinâmicas possíveis ou resultado científico.

Pedido de preparação: e5d214e4-972e-41f5-bd14-0dc071c00e6b. Execução proposta: c4359a48-bf7c-4dd5-a753-8c3413774cdf. A unidade ffd6ccba-cd70-4747-aceb-a10003dfb7f4 permanece falha terminal. O manifesto examinado e o snapshot final constam no recibo de hashes ao lado.

## O que foi conferido

Foram realizadas **132 conferências estáticas**, todas satisfeitas, com **79 caminhos registrados por hash**. São comparações de bytes, AST e metadados; não são uma campanha de testes do candidato. O script independente inspect_delta_static.py não importa arquivos do pacote, não inicia WSL e não executa solver/controles. Seu único produto é a evidência desta revisão.

O manifesto de 27 membros e os 18 pins locais conferem em disco. As 27 adições do runtime foram lidas diretamente pela UNC, além dos metadados específicos de builtin e dos seis codecs CJK. Os 5.074 pins antigos foram comparados entre inventários, preservados exatamente; **não** houve novo rehash físico de todo aquele acervo. O worker continua responsável por conferir os arquivos e aliases no runtime antes do solver.

Foram reutilizados o exame do envelope 555 e sua correção documental 561. Não foi transferido o PASS do transporte stdlib 550 à pilha científica. O retrato inicial dos 27 membros e manifesto foi comparado ao final, sem mudança. Fontes, recibos e unidades consumidas não foram alterados.

## Fechamento concreto das dependências

[REAL/DERIVED — fonte e metadados] O inventário passa de 5.074 a 5.101 entradas pela adição exata de:

- nove fontes de charset_normalizer alcançadas a partir do inicializador;
- nove caches existentes, com cabeçalhos de timestamp/tamanho coerentes com os fontes;
- duas extensões ELF, cd e md;
- sete arquivos da distribuição charset_normalizer-3.5.1.dist-info.

As 59 arestas de importação foram reconstruídas independentemente por AST e correspondem à evidência do autor. A travessia inclui imports em corpos de funções. Os quatro pontos de importação dinâmica estão registrados separadamente: a enumeração estática não foi apresentada como traço observado.

As únicas duas raízes acrescentadas são o pacote charset_normalizer e sua distribuição instalada. Isso não permite ler qualquer arquivo existente nessas árvores: o ramo de ausência herdado só admite sondas inexistentes; arquivos existentes continuam exigindo pin individual. CLI e __main__ não foram acrescentados. Não houve liberação genérica de site-packages.

Os cabeçalhos dos nove caches têm o magic, flags, timestamp e tamanho declarados. Os bytes de fontes e caches conferem separadamente. Isso demonstra identidade e coerência do cabeçalho, **não** prova equivalência semântica do bytecode com o fonte; nenhum bytecode foi carregado ou decodificado nesta revisão. A presença de caches é pertinente porque -B impede sua escrita, não sua leitura.

O coletor ELF foi lido: usa cabeçalhos ELF64 little-endian, PT_LOAD/PT_DYNAMIC e DT_STRTAB para localizar DT_NEEDED/SONAME/RPATH, sem carregar bibliotecas. As duas extensões pinadas declaram libpthread.so.0 e libc.so.6; as seis arestas recursivas documentadas terminam nos candidatos já pinados, inclusive o loader. A comparação exigida dos aliases no Linux foi preservada. A identidade de um candidato por hash não foi convertida em observação do alias já resolvido neste novo processo.

unicodedata aparece em MODBUILT_NAMES e na tabela config.c do Python pinado. Ambos os arquivos foram relidos e conferidos. worker.py:89–94 exige ainda sua presença em sys.builtin_module_names no runtime efetivo. A solução respeita o tipo builtin, sem inventar unicodedata.so.

A constante _KNOWN_MB_CLASSES foi reconhecida por AST como frozenset literal com exatamente seis provedores. Os seis binários _codecs_cn, _codecs_hk, _codecs_iso2022, _codecs_jp, _codecs_kr e _codecs_tw foram relidos e conferem com pins anteriores. encodings.* permanece coberto pelo inventário stdlib existente. O recibo distingue esse vínculo textual de uma observação de codecs efetivamente carregados.

## Sonda ZIP e diagnóstico de exceção

[REAL — fonte] is_exactly_absent em worker.py:19–26 usa lstat e aceita somente FileNotFoundError. Existência, symlink inclusive pendente, ou outro OSError recusam a sonda. O preflight exige que a coleção de sondas especiais seja exatamente /usr/lib/python312.zip e volta a checar sua ausência antes dos imports. Na inspeção UNC desta revisão, o caminho estava ausente.

No hook, worker.py:125–145 recusa escrita antes de considerar a sonda. Cada open do caminho normalizado exato refaz lstat. Se ausente, registra EXACT_ABSENT_PROBE_NO_CONTENT; caso contrário, aciona o latch. O ZIP não ganha pin de conteúdo nem vira raiz genérica. A regra resolve a recusa concreta de 561 sem afirmar qual chamador produziu aquele evento histórico.

A ausência é uma observação de metadados num instante. Permanece a janela cooperativa stat/open explicitada pelo autor; isso não é isolamento do sistema operacional contra substituição concorrente maliciosa. Não foram afrouxadas permissões do host.

bounded_failure em worker.py:29–48 conserva os dois frames iniciais e os oito terminais, sem duplicar a interseção. Registra total, retidos, omitidos e a política SINGLE_EXCEPTION. Obtém somente metadados dos frames e não chama linecache nem abre fontes para formatar a exceção. Isso corrige a perda das frames terminais em limit=8 da versão anterior. Não conserva todas as cadeias __cause__/__context__, nem afirma que qualquer recibo arbitrário caberá no cap de streams; os caps e sua recusa visível continuam vigentes.

A rotina foi examinada por fonte/AST; não foi importada ou chamada. Tanto a falha interna quanto a externa usam a nova representação. O snapshot latched/journal_error ainda força FAILED_LATCHED; nenhuma exceção é promovida a sucesso por essa mudança.

## Preservação operacional e limites

[REAL — comparação] common.py, linux_control.py e launch_windows.py coincidem com os anteriores após substituir somente nomes de pasta e request_id. Permanecem PurePosixPath para tokens Linux, Path concreto para IO do host, claims exclusivos, identificação de processos, nonce, STOP/gate/pidfd, captura de erros/EOF, clipping de streams, limpeza e aceites finais. O defeito Windows→Linux anterior não foi reintroduzido.

Os limites e pins de executáveis Windows/Linux são idênticos. Permanecem 180 s nominais totais, 140 s de trabalho primário, 110 s de trabalho do filho e 25 s de limpeza Linux, sem retry e com uma chamada futura ao background. São prazos de protocolo/espera e monitoramento cooperativo, não garantia OS absoluta de duração, RSS ou todas as syscalls nativas. A divergência histórica do campo timeout100s não consumido pelo caminho direto permanece documentada, sem nova alteração.

Dez cópias científicas/revisões são byte a byte idênticas, e a configuração muda somente request_id. A admissão recebe os novos pins correspondentes; a matemática foi objeto de revisão própria da ROOT, não reexecutada aqui. Permanecem as verificações de origens de módulos e mapas nativos, checkpoints antes/depois de imports/solver/montagem, journal físico e saída não zero em falha.

Nesta conferência não havia AUTORIZACAO_ROOT.json, CLAIM.json, RUN ou RESULT.json no novo pacote. A autorização consumida não foi copiada. Este preparo não reabre ffd6, não move gate, não lê centros, não fornece likelihood, sigma, ln B ou certificado físico.

## Alcance e próximo passo

[OPEN — execução futura] Compatibilidade real das importações, aliases, biblioteca nativa e transporte sob o runtime-alvo só terá evidência se uma unidade específica for autorizada e executada. Não se exige campanha genérica adicional para componentes invariantes ou já medidos. Se ocorrer novo bloqueio, o contrato mantém falha visível, diagnóstico limitado e ausência de repetição automática.

A lacuna concreta da revisão 555 fica tratada por este candidato e pela errata 561 preservada ao lado; o aceite estático anterior não se torna retroativamente uma execução bem-sucedida. Resultado esperado de uma eventual chamada admitida continua limitado a ENGINEERING_ONLY.
