# P3 — pacote isolado e fase pré-hook B

Preparação **2bfd4665-a7e7-410a-aeb3-0406f90a596f**, posterior à comparação do mapa619 e registrada antes no mapa627. [REAL] Foram montadas cópias locais verificadas dos cinco candidatos e das 12 dependências admitidas, um delta mínimo no driver, um módulo de pre-hook e uma entrada candidata de inspeção de runtime/imports. Nenhum candidato foi importado ou executado; não houve WSL, biblioteca científica, waveform, likelihood, sampler, PE ou leitura de arrays/PSD/dados observados.

## Delta concreto

FONTES_PINADAS.json guarda as origens, ENTRADAS_FECHADAS.json enumera as entradas e DRIVER_DELTA.patch mostra a alteração integral. audit_guard.py, result_acceptance.py, launch_p3.py e src/pseob_source.py permanecem byte a byte iguais aos candidatos. As 12 dependências também. O driver muda somente para obter a identidade do adapter, chamar preload_known_imports antes do hook e registrar o recibo/hash dessa fase. Seu bloqueio incondicional PREPARATION_ONLY continua no primeiro comando de main. O launcher científico conserva o mesmo bloqueio.

O novo pre-hook carrega lal, lalsimulation, bilby.gw.source e temporal_contract. Confere arquivos pinados, origens __file__/__spec__, código Python da source/temporal e identidade única entre a função da source e a usada pelo adapter; recusa uma segunda identidade src.pseob_source. Registra módulos e arquivos realmente carregados, distinguindo pins históricos reconferidos de metadados novos da biblioteca padrão. Não chama função científica.

[INPUT — decisão ROOT] Adotada a alternativa B. [DERIVED — código] Esses imports passam a ocorrer ANTES do hook estrito P3. Os imports e checkpoints originais dentro da source continuam: devem recuperar os mesmos módulos do processo. Não se acrescentou permissão para diretórios de cache, removeu checkpoint, apagou latch ou redefiniu INIT003.

## Alternativas consideradas

A — Manter imports tardios e allowlist estrita: conserva o momento original de carregamento; o guard reparado torna uma nova recusa terminal. Não resolve a disponibilidade dos imports conhecidos que motivaram esta preparação.

B — Preload nominal, pinado e declarado: materializa os quatro imports antes do hook, conserva o guard depois e atesta source/adapter. É a escolha expressa de ROOT. Seu custo é deixar essa inicialização fora do hook estrito; não prova ausência de efeitos internos ou fechamento de todos os imports futuros. Não reescreve a falha anterior como sucesso.

Nenhuma alternativa prova contenção de syscalls nativas. A importação futura pode executar inicializadores Python/C. A inspeção proposta chama somente imports e o preload de codec existente; não chama waveform, helpers físicos LAL, função temporal, gerador, construtor de detector, likelihood ou sampler.

## Próximo passo mínimo preparado

qualify_imports.py contém supervisor e um único filho para conferir arquivos do runtime histórico, importar a mesma base e realizar a fase B. Exige decisão ROOT futura com hashes do manifesto/contrato, ação exclusiva QUALIFY_PINNED_IMPORTS_ONLY e identidade futura de qualificação. Não existe ROOT_DECISION, CLAIM, AUTH, diretório de execução ou identidade científica materializada.

COMANDO_CANDIDATO.json contém argv POSIX derivado do caminho existente. É comando futuro de imports, não de PE. Sem a decisão, recusa antes das bibliotecas científicas. Driver/launcher de PE permanecem incondicionalmente bloqueados mesmo se a inspeção vier a ser autorizada.

Propõe-se uma inspeção única: 120 segundos nominais totais, 110 para trabalho e reserva restante para recolhimento/finalização; uma thread, um filho direto. Reserva exclusiva persistente precede o filho; outra precede imports. Falha/interrupção consome a reserva, sem retomada/repetição. O supervisor controla o filho recém-criado por Popen; não enumera nem mata processos alheios. Aceitação exige exit0 externo, recibos compatíveis e ausência de FINALIZATION_FAILURE. COMPLETE isolado é provisório: atraso de I/O/hash/flush invalida a aceitação.

Limites nominais dependem de escalonamento/arquivos; não são hard realtime. O código proposto não chama descendentes adicionais; não promete conter descendentes criados por inicializadores nativos. O limite Linux de tamanho de arquivo é por arquivo do filho e vale após sua admissão; não é limite global de retenção. ROOT deve avaliar essas condições concretas na revisão operacional antes de aprovar.

## Fechamento e lacunas

[REAL — documental] Estrutura isolada, entradas locais fechadas, delta legível, política de bytecode, vínculos de módulo, contrato, comando candidato e conferência AST/pins estão preparados. Os pins Linux são referências HISTÓRICAS, não medições frescas. Nenhum arquivo instalado Linux foi lido agora. O JSON não demonstra disponibilidade atual. A conferência futura recusa divergência, sem repinar silenciosamente.

[OPEN — próximo passo único] Revisão independente e decisão específica para a inspeção de runtime/imports. Somente a execução admitida pode produzir evidência fresca do carregamento nesta montagem. Não é necessário repetir doubles/stdlib consumidos para obter essa evidência diferente.

[OPEN — ciência separada] Mesmo com imports bem-sucedidos, faltará contrato científico sucessor com identidades novas, entradas/arrays sintéticos pinados, decisão própria e runtime medido. Ele habilitará as entradas científicas em uma futura versão revisada e qualificará inicialização, chamada, journal e aceitação do filho. Recuperação, convergência e cobertura do sampler não são resultados desta preparação.

INIT003 permanece terminal. Doubles, Windows stdlib e WSL stdlib conservam escopos originais e não foram reproduzidos ou promovidos a qualificação científica. Não foram copiados autorizações, claims, resultados ou IDs de jobs consumidos para admitir execução nova. JSONs históricos conservam proveniência, sem virar autorização. Não há CONTRATO_P3 científico nem cópia de arrays/conteúdo ASD/PSD. Originais, fila, ledger e memórias compartilhadas permanecem intactos.
