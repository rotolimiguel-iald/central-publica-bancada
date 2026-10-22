# Revisão independente do envelope e runtime da integração F9

**Parecer: aceite estático limitado, sem bloqueador concreto identificado neste recorte.** [REAL — leitura, hashes e AST] Os 24 membros e o manifesto permaneceram iguais ao snapshot inicial. Esta revisão não autoriza execução, não qualifica dinamicamente CAMB ou seus imports e não confere um certificado científico. Nenhuma correção do pacote é exigida por este parecer.

Preparação f07e4aba-e976-4d78-be1c-449968d4a305; execução apenas proposta ffd6ccba-cd70-4747-aceb-a10003dfb7f4. Casa Central de Patentes; revisão por chatgpt-codex/ordem-018/proveniencia. Consulta anterior ao exame: rota hubble.fase9_razao_discriminante, último registro retornado548. O ponto/configuração matemática recebe revisão independente separada de derivacoes.

## Integridade e alcance da leitura

Manifesto conferido: 4055 bytes, SHA256 `0f97167b195f10940e8cb5d529fc57a531122c3357cf58aa629b847938b82300`. Contrato: 7161 bytes, SHA256 `2eda2e426a8b9b9c4c2b751367b9265095ec5bafa1f83ea78f55c5f82c412315`. Foram feitas86 comparações de pins sobre46 caminhos distintos:24 membros do manifesto,18 pins locais do contrato,22 referências de linhagem, o pedido de preparação,18 arquivos do snapshot inicial e3 executáveis/bibliotecas Windows. Todas conferiram. Dez arquivos Python foram analisados por AST, sem importar ou executar seus módulos. As14 referências Linux do contrato coincidem com as entradas do inventário; essa comparação é documental, não nova leitura dos14 arquivos Linux.

Os sete originais científicos/guard copiados continuam exatos conforme seus hashes de origem. A nota NOTA_INTEGRACAO.md e VERIFICACAO_FINAL_ESTATICA.json chegaram como suplementos fora do manifesto inicial; seus pins estão separados no recibo. Não tratei sua chegada como alteração dos24 membros congelados. No instante desta conferência, AUTORIZACAO_ROOT.json, CLAIM.json, RUN e RESULT.json estavam ausentes. Não escrevi nenhum deles.

[REAL — leitura dirigida] Dez fontes instaladas de CAMB/NumPy/SciPy/stdlib foram lidas como bytes por UNC, com hashes calculados e iguais ao inventário. Uma leitura inicial foi impedida pela sandbox; a leitura restrita por escalonamento foi autorizada e concluída. Não houve rejeição de auto-review nem processo Linux iniciado. Não fiz nova leitura dos5.074 arquivos completos do runtime: RUNTIME_INVENTORY continua inventário fornecido, com conferência seletiva independente e verificações obrigatórias no futuro filho.

## Runtime, aliases e diagnóstico

O worker acrescenta explicitamente o único site-packages indicado após o início com `-I -S -B`; não chama site nem executa arquivos .pth. Antes do hook e do solver, confere os pins e os aliases Linux contra os candidatos de mesmo hash. A resolução por SONAME é evidência documental de candidato, não prova de symlink. A obrigação de conferir o alias real no Linux foi conservada. Ausência ou divergência interrompe a unidade antes do solver.

A cadeia lida inclui CAMB/baseconfig→ctypes/NumPy e SciPy→_lib._testutils→sysconfig. A suspeita de omissão do alias longo `_sysconfigdata__linux_x86_64-linux-gnu.py` foi **refutada** pela fonte instalada: sysconfig.py497–502 monta o nome curto a partir de abiflags e multiarch; o fonte curto está pinado. SciPy/_lib/_testutils.py44 de fato consulta HOST_GNU_TYPE na importação. Os dois caminhos exatos consultados para a dependência opcional cython não foram encontrados via UNC; isso não constitui inventário universal de módulos opcionais.

O inventário contém5.074 caminhos únicos,1.998 fontes.py e1.999 arquivos.pyc. De1.998 fontes,1.997 possuem o cache CPython3.12 convencional pinado; a exceção é config-3.12-x86_64-linux-gnu/python-config.py. Portanto, a hipótese de centenas de sondagens provocadas pela exclusão geral de pyc **não corresponde ao inventário entregue**. O worker registra sondagens ausentes dentro das árvores previstas, mas não libera arquivo existente sem pin. A nota declara a janela stat/open e o alcance cooperativo desse mecanismo.

[OPEN — execução] A lista missing_runtime_probes não possui limite próprio e integra o recibo de stdout. O teto de32.768 bytes permanece por fluxo em ambos os pais; LINUX_RESULT acrescenta seu envelope ao CASE_RESULT. Não derivei, da cadeia concreta lida, uma explosão normal que ultrapasse esse teto. Não proponho aumento nem recusa com base só nessa possibilidade. Se houver overflow real, a coleta falha e não pode aceitar sucesso; não é permitido inferir um resultado científico a partir de artefatos parciais.

A lacuna diagnóstica de NC02 não foi repetida na verificação de módulos: worker.py114–138 conserva fase, módulo/caminho e motivo; os mapeamentos nativos recebem diagnóstico próprio. A primeira ausência não é reduzida a um rótulo genérico sem identidade. O conjunto de imports efetivos e de mapeamentos de /proc/self/maps será comparado aos pins após os imports e depois do motor/montador. Essas medidas não observam todas as syscalls/leituras nativas nem equivalem a confinamento do sistema operacional.

## Transporte comparado ao PASS550

A linhagem parte do candidato PurePosixPath e dos instrumentos V2, não de uma cópia integral do pacote que produziu o PASS550. A comparação AST independente encontrou iguais os oito componentes selecionados: Capture e wait Windows; gate, stop_child e capture Linux; exact_signal, scoped_processes e argv_for. Isso demonstra continuidade desses componentes; não transfere o PASS stdlib para CAMB/NumPy/SciPy.

Os três recibos instrumentais extras de argv do pacote550 não foram transportados integralmente. A obrigação atual de identidade continua implementada por outra combinação concreta: tokens Linux construídos por PurePosixPath/as_posix em lista sem shell, script Windows fixo, request/nonce/contrato/autorização, claims exclusivas, argv/exe de /proc do filho conferidos pelo supervisor e argv/identidade do supervisor conferidos pelo filho. As strings com espaços permanecem tokens inteiros. Cleanup usa as mesmas formas POSIX para selecionar somente os comandos desta request/nonce. A falta dos três recibos extras não demonstrou defeito de representação ou de seleção neste contrato novo; não foi tratada como bloqueador automático.

As claims antecedem lançamento/importação científica e são exclusivas. A existência de CLAIM/RUN/RESULT impede replay; claims não são removidas. STOP é persistido antes de abrir o cleanup. O mesmo gate cerca a criação do filho e o cleanup, impedindo lançamento atrasado depois do STOP. Sinalização Linux exige identidade exata conferida e pidfd; Windows usa handles próprios dos Popen. A inspeção se limita aos processos/identidades/instantes descritos, sem promessa absoluta sobre órfãos ou alterações adversariais do host.

Capture Windows conserva erros e EOF separadamente e exige encerramento normal dos dois fluxos; morte de thread não conta como EOF. Ambos os capturadores recortam o chunk antes de acrescentá-lo e recusam excesso de32KiB. Erro/overflow não vira PASS. Foi preservado o reparo WSL-01/02.

## Latch, saída final e prazos

O guard é cópia exata do já revisado. AuditLatch marca latched/count/primeiro evento antes da escrita do journal, preserva erro de journal e mantém checkpoints mesmo se a PermissionError original for absorvida. Há checkpoints depois dos imports, antes e depois da chamada nativa interceptada, depois do motor, depois da montagem e antes da aceitação. O mecanismo não se baseia em suposta infalibilidade de SystemExit/BaseException.

A tentativa a camb.get_background é contada antes da chamada e limitada a uma, com função original restaurada em finally. O termo “uma chamada” refere-se a essa entrada do motor; não afirma ausência de inicializações/código nativo durante importação das bibliotecas. Não são chamados main, validate, run_controls ou execute_worker_once históricos. Nenhuma unidade terminal antiga é reaberta.

Para aceitar, o supervisor exige status/identidade do filho, tentativa e retorno iguais a1, zero bloqueios no snapshot e journal físico vazio correspondente, hashes físicos dos quatro artefatos e presença das cinco saídas de283componentes com nuisance63 e ENGINEERING_ONLY. Exige também stdout igual ao recibo em disco e filho encerrado com exit0 e stderr vazio. Windows só aceita depois do cleanup sem processos correspondentes encontrados/encerrados tardiamente, persiste seu recibo e verifica o prazo após I/O e após stdout. O consumidor externo ainda deve exigir exit0 e duração final; o status provisório escrito antes de uma falha tardia não basta.

Os prazos efetivos são180s totais nominais Windows,140s de trabalho primário,110s de trabalho Linux,125s até o fechamento do supervisor Linux e25s do cleanup. O fechamento dos pais pode envolver I/O cooperativo sem limite rígido de SO. A memória é o pico informado pelo engine, sem enforcement de RSS alegado. EFFECTIVE_CONFIGURATION conserva100s no campo herdado timeout_seconds_per_worker; prediction_worker não o consome. Essa diferença foi declarada na nota e não foi promovida a uma obrigação100s inexistente na chamada direta. Para esta unidade, contrato/envelope determinam os limites efetivos acima.

## Conclusão e fronteiras

[REAL — resultado desta revisão] Nenhum bloqueador novo demonstrado no envelope/runtime examinado; pins e snapshot preservados. Não foram executados candidatos, WSL, hooks, controles, CAMB, likelihood, sampler ou dados observados. Não foi criada autorização/claim/unidade e nenhuma memória compartilhada ou ledger foi alterado.

[OPEN] Imports reais, resolução dos aliases, duração, RSS e resposta da primeira chamada permanecem não medidos nesta revisão. As verificações concretas do pacote tratam falhas de engenharia como falha/incerteza, nunca likelihood zero ou sucesso físico. Um eventual resultado aceito será previsão de engenharia local, não V1, ajuste, evidência, cota uniforme, significância ou certificado físico. A decisão específica de execução pertence à coordenação ROOT após reunir também a revisão matemática; este parecer não acrescenta uma nova campanha de controles ou uma barreira genérica de permissão.

Evidências locais: STATIC_METADATA_RESULT.json; RUNTIME_SOURCE_READS.json; PASS550_STATIC_COMPARISON.json; SNAPSHOT_INICIAL.json; RECIBO_REVISAO_F9_ENGINE_ASSEMBLY.json. Os hashes completos desses artefatos e deste parecer constam do manifesto da revisão.
