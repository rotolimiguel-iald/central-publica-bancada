# Observador externo do piloto — pronto para revisão, não ativado

[REAL — implementação e testes finitos; OPEN — observação real] `observer.py` é uma ferramenta independente, stdlib, para metadados do Linux. Modo padrão inativo: não lê job ou /proc. Não inicia/controla processos nem lê stdout, logs, strain, amostras, checkpoints, cmdline/environ ou memória. Não altera runner, controlador, E2, priors, orçamento ou deadlines.

**Não é gate para o piloto ou para a ordem completa.** Ausência, erro, término antecipado ou cobertura incompleta do observador só afetam sua telemetria. Um piloto sem custo convergido continua podendo entregar diagnóstico honesto de interrupção e gasto; não inventar posterior ou custo de evento convergido.

## Destino corrigido após revisão do principal

Fonte e testes vivem nesta pasta. Todas as observações reais, inclusive MANIFEST, SNAPSHOTS.ndjson e SUMMARY, serão criadas em **B/cache/E3_PILOT_OS_OBSERVER_V1/observation_NNN**. Isso permite snapshots acima de 25 MB sem gravá-los em bis. O primeiro desenho escrevia em HERE; foi corrigido antes de qualquer observação. Nenhuma observação antiga precisou ser movida. Raiz cache e pai são conferidos contra resolução de links, nome é fechado e diretório da tentativa é exclusivo. Testes de armazenamento usam apenas uma árvore cache fictícia temporária dentro desta pasta, removida de forma confinada.

## Interface futura; não executada nesta entrega

Principal inicia separadamente, no mesmo WSL/PID namespace e fora do grupo do controlador, depois de seu próprio review. Usar Python stdlib e `-B -O`, script `observer.py`, com `--observe`, `--context-sha256`, `--registration-sha256`, `--config-sha256` e `--output-name observation_001`. Hashes devem ser medidos dos metadados autorizados; não preencher por memória. Não se recebe diretório arbitrário, evento alternativo ou comando científico. Contexto aceito somente em `B/cache/E3_PSEOB_PILOT_V1/LAUNCH_CONTEXT.json`, job GW250114_PILOT.

`--max-seconds` limita somente o observador, padrão 8 h + 15 s e máximo de interface 10 h + 15 s. Ele termina até o menor entre seu limite monotônico e stop_utc do contexto + 15 s. Os 15 s são janela documental, nunca extensão da ciência. Um observador iniciado mais tarde não reinicia o orçamento do piloto. O controlador congelado continua dono da parada/cleanup.

## O que a implementação mede

Vínculo inicial por contexto/hash, PID/start_ticks, UID e namespace; boot_id registrado. Descobre um único líder filho do controlador, com PID=PGID=SID, depois descendentes por cadeia observada e grupo/sessão. Nomes de processos não selecionam ownership. PIDs conhecidos podem continuar após reparenting; PID reutilizado, mudança de grupo, UID/namespace ou contador decrescente é recusado/quarentenado. Não descobre processos já desaparecidos e não presume cobertura completa.

CPU própria de cada processo é o maior utime+stime visto, somado uma vez por identidade e convertido por SC_CLK_TCK. Não adiciona cutime/cstime ou CPU dos threads novamente. CPU do controlador é separada; nunca somar automaticamente com RUSAGE_CHILDREN. Counter cumulativo do controlador começa na criação do processo, podendo incluir preparação anterior ao relógio do receipt. Não denominar todo descendente como worker científico. CPU observada é limite inferior, não custo exato de uma rodada convergida.

Leituras /proc limitadas a stat, status (só UID retido), task/children, boot_id e readlink do namespace. A leitura de stat é repetida para detectar troca de identidade. Arquivos de metadados limitados a 64 KiB; máximo de 128 identidades e 128 threads por descoberta. Amostragem nominal de 5 s, com aumento automático até 30 s se a própria coleta atrasar. O sweep não é atômico; UTC/monotônico antes/depois e custo do observador são registrados. Erros de leitura são lacunas, não zero CPU nem confirmação de ausência.

SUMMARY vincula SHA256 e número de bytes do **prefixo de snapshots completos**, não promete hash de uma possível cauda truncada. Não sobrescreve arquivos existentes. Processo encerrado abruptamente pode deixar apenas manifesto e prefixo sem SUMMARY; isso é OBSERVER_INCOMPLETE, nunca sucesso implícito. OBSERVER_COMPLETE significa recibo do controlador encontrado e reconhecido, não convergência ou cleanup aprovados pelo observador. Detalhes de cleanup/convergência seguem revisão própria.

## Verificação e limites

`test_observer.py` usa grafo de processos inteiramente fictício e arquivos próprios temporários. Testa allowlist, JSON estrito, parsing de comm, ownership/PID reutilizado, reparenting, CPU sem dupla contagem, acesso negado, corrida de identidade, relógio UTC corrigido, deadlines, confinamento cache, exclusividade, escrita truncada e inatividade padrão. Executado sob `-O`; guardas não dependem de assert. Recibo final registra runtime, hashes e resultados efetivamente obtidos.

Não foi lançado observador contra o piloto, nem lido /proc real. Não foi medido overhead em job real. Não se alega certificação do adaptador /proc ao vivo. SOURCE/likelihood_calls, ESS, convergência e custo por evento convergido ficam null no resumo do observador. A revisão independente do principal e eventual ativação pertencem a ele, sem atrasar o piloto já autorizado.
