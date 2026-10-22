# Correção preparada da cadeia de imports F9

[REAL — preparação estática] Pedido e5d214e4-972e-41f5-bd14-0dc071c00e6b. Esta pasta contém uma proposta nova, separada da execução terminal ffd6. A preparação usa leitura de fontes, AST, cabeçalhos ELF, hashes e metadados; não importa os candidatos, não inicia WSL/Python Linux, não chama CAMB ou likelihood e não lê centros observados. A presença de código executável nesta pasta não autoriza seu lançamento.

## Falha de origem e correção delimitada

A unidade anterior foi encerrada como FAILED_TERMINAL_CLEANED, com zero tentativas de get_background. A revisão de proveniência conservou três alvos de open recusados: a sonda /usr/lib/python312.zip e o fonte/cache de charset_normalizer. A sequência profunda completa e o chamador exato do ZIP não estavam conservados; não os reconstruímos como se fossem observados.

[DERIVED — cadeia textual] O diagnóstico estabeleceu a rota SciPy Array API → expansão pública de NumPy → f2py → crackfortran → charset_normalizer. Nesta preparação, a análise AST percorreu a dependência instalada a partir de seu __init__, inclusive imports dentro de funções, sem executá-los. São nove módulos Python alcançáveis. CLI, __main__ e arquivos de outros pacotes não ganharam permissão por essa análise.

O inventário novo mantém os 5.074 pins anteriores e acrescenta exatamente 27 arquivos: nove fontes Python, nove caches existentes, duas extensões ELF (cd/md) e sete arquivos de metadados da distribuição instalada. Não há liberação genérica de site-packages. Cada arquivo existente permanece sujeito ao pin individual. O cache é inventariado porque -B impede a gravação de bytecode, não sua leitura. Cabeçalhos e sua correspondência com os fontes estão registrados; bytecode não foi carregado ou decodificado como código executável nesta coleta.

DEPENDENCY_CLOSURE_EVIDENCE.json contém arestas de imports com linhas, metadados de caches, dependências ELF DT_NEEDED e referências aos candidatos nativos já presentes no inventário. A resolução dos aliases continua exigindo comparação real de hashes no Linux antes do solver. Um SONAME coincidente não é apresentado como observação do symlink em execução.

As dependências absolutas do pacote recaem na stdlib já inventariada. unicodedata é identificado em MODBUILT_NAMES e na tabela de inicialização config.c do Python pinado; o worker novo conferirá também sua presença em sys.builtin_module_names antes de importar o motor. Não foi criado um arquivo fictício unicodedata.so. A primeira coleta parou na exigência de arquivo separado, antes de gravar evidência; a leitura dos metadados resolveu essa diferença de tipo.

Os imports dinâmicos têm tratamento documental explícito: encodings.* usa a família stdlib já inventariada e seis provedores CJK determinados pela constante instalada _KNOWN_MB_CLASSES. DYNAMIC_CODEC_EVIDENCE.json conserva a definição e os hashes desses seis binários. Sua leitura AST reconhece a estrutura literal de frozenset sem chamar a definição do pacote. O mesmo documento confere que o sysconfig deste Python calcula o nome por abiflags/multiarch, sem acrescentar linux; nenhum alias Python adicional foi liberado por hipótese.

## Sonda ZIP: ausência, não conteúdo

O caminho /usr/lib/python312.zip foi consultado por lstat via UNC e estava ausente no momento da coleta. O worker exigirá novamente ausência antes dos imports e em cada evento de open desse caminho exato. Somente FileNotFoundError admite a sonda sem conteúdo; existência, symlink existente ou outro erro de lstat recusam a operação. A regra é anterior à aceitação de qualquer leitura comum. Escrita permanece proibida.

O caminho não recebe pin de conteúdo nem vira raiz de leitura. Se passar a existir, a unidade futura falhará visivelmente. A checagem é um monitor cooperativo de Python e conserva a limitação stat/open: não é um mecanismo de isolamento do sistema operacional contra alterações concorrentes maliciosas. Não foram alteradas permissões do host nem se alegou observação de todas as syscalls nativas.

## Diagnóstico de erro conservado

O handler novo guarda o total de frames da exceção, os dois iniciais e os oito terminais, deduplicando a interseção. Nomes de arquivo/função, linhas e mensagem têm limites de tamanho. A obtenção usa metadados dos frames diretamente e não consulta linecache ou abre fontes adicionais durante o tratamento do erro.

O campo traceback continua textual e recebe contagem total/retida/omitida e política explícita. Trata a exceção capturada, sem alegar uma cadeia ilimitada de causas. Preserva o audit latch, journal físico, caps de streams e os recusadores já existentes. Não há captura transformada em sucesso nem limpeza do latch após uma recusa.

## O que permanece igual e o que muda

As cópias de background_controls.py, five_model_assembly.py, audit_guard.py, layout, desenho linear, protocolo de origem, metadados do motor, parâmetros H1–H5 e recibos das revisões do montador/transporte são byte a byte as anteriores. Beta fixa continua calculada no montador pela regra alpha vezes raiz de e; não foi copiada como literal novo.

EFFECTIVE_CONFIGURATION.json muda somente request_id. O ponto de prior, grade z=0 mais os sete BAO, perfil reference, modelos e parâmetros físicos permanecem iguais. A diferença histórica entre metadado timeout100s e trabalho Linux110s continua explícita: o primeiro pertence ao CLI antigo não chamado; a política efetiva permanece no supervisor. Não foi misturada uma alteração de timeout a esta correção de imports.

common.py, linux_control.py e launch_windows.py mudam somente identidade/caminhos. Permanecem a claim exclusiva, uma chamada futura ao motor, sem repetição automática, deadlines nominais, limite de filhos/threads, STOP persistente, identificação de processos, pidfd e cleanup. Isso não é um novo teste científico nem uma repetição autorizada por inferência; a preparação apenas materializa o delta necessário para uma decisão posterior.

ASSEMBLY_ADMISSION.json recebe os hashes reais da nova configuração e do inventário; CONTRATO_WSL.json recebe os pins reais, a identidade nova e o resumo do delta. Nenhuma autorização ROOT da unidade consumida é copiada. Somente uma revisão independente própria e uma decisão específica poderão admitir uma futura execução.

SOURCE_LINEAGE.json registra fontes e snapshots protegidos; DELTA_REPAIR.diff compara o código/configuração com a unidade consumida. Para o inventário, a lista exata das 27 adições fica na evidência de dependências, evitando uma listagem integral redundante. A preparação verifica que os 24 membros antigos, seu manifesto, autorização, claims, resultados e arquivos da execução não foram alterados.

## Alcance da entrega

[REAL] Manifesto, AST e comparação de bytes qualificam somente a preparação documental. Não comprovam sucesso dos imports, desempenho, previsão CAMB ou compatibilidade dinâmica de todas as dependências possíveis. A cadeia finita demonstrada foi tratada; uma eventual leitura imprevista continua sendo falha visível. Não se exige um certificado uniforme do solver para produzir estimativas de engenharia, nem se promove essa preparação a evidência física.

Esta pasta não contém AUTORIZACAO_ROOT.json, CLAIM.json, RUN ou RESULT.json. O futuro resultado, se admitido e produzido, continuará ENGINEERING_ONLY. Sem ajuste, sigma, ln B, leitura de observados, campanha ou alteração do gate. O consumidor conjunto y/C → T → Gaussian, preparado por outra unidade, não é modificado nem executado aqui. MM e as condições de seu uso permanecem no respectivo contrato.

Próximo passo: revisão independente do delta concreto e decisão da coordenação. A unidade terminal ffd6 não deve ser editada nem repetida.
