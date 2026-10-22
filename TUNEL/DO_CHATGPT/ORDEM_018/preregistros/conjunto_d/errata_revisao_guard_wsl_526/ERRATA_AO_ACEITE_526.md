# Errata ao aceite estático526 — caminho Linux materializado no Windows

**A unidade `4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf` foi consumida uma vez e falhou antes de abrir `linux_control.py`. Não há autorização para corrigi-la, relançá-la, reabrir seu CLAIM ou repetir seu controle.** Esta errata fica ao lado do parecer526; fontes, pareceres e evidências consumidas permanecem intactos.

## Evidência e causa

[REAL documental] `EXEC_RESULT_OFFICIAL_TOOL.json` registra saída externa nãozero; `RESULT.json` registra exit2 para principal e limpeza, status `UNCERTAIN_ORPHAN_STATE`, `linux=null`, `cleanup=null`. Os dois stderr guardados em `RUN` dizem `can't open file` e `No such file or directory`. Os dois stdout estão vazios. O mesmo nonce/request está em CLAIM, recibo e processos Windows. Os valores, tempos e hashes lidos estão no recibo documental desta errata; não são novo benchmark.

`RUN/WSL_PROCESS.json` e `RUN/CLEANUP_WSL_PROCESS.json` guardam o token real de script começando por `\mnt\c\...` e terminando em `\linux_control.py`. O Python Linux tratou esse token com barras invertidas como nome relativo, anexando-o ao cwd Linux no diagnóstico. Não é evidência de que o script local não exista: o defeito está no token transportado, antes de ler o código pretendido.

[DERIVED, sustentado pelo argv real] Em `common.py:3`, a implementação importa `pathlib.Path`; em8, constrói `LINUX=Path("/mnt/c/...")`; em64–66, `argv_for` usa `str(LINUX/script)`. No launcher Windows, `Path` escolhe `WindowsPath`. A fonte local `C:/Python314/Lib/pathlib/__init__.py:632–635` mostra essa escolha por `os.name`, e325–328 documenta que `as_posix` faz a serialização com barras diretas. Nenhum candidato ou construção alternativa de caminho foi executado nesta análise.

`launch_windows.py:50–52` recebe `g.argv_for(...)` e o passa a `wsl.exe --exec`. Esse caminho é usado no lançamento principal, linha80, e no helper de limpeza, linha95. Assim os dois comandos falham na mesma fronteira. Não é falha da matemática, da fonte waveform, do audit hook ou do pidfd: essas etapas Linux do pacote não foram alcançadas nos lançamentos registrados.

## Correção do alcance do parecer526

Eu não identifiquei esse defeito preexistente na revisão526. A comparação por AST confirmou a preservação de `common.py` descontando o diretório e deixou passar a semântica dependente do host de `Path`. Igualdade com514 não demonstrava que o token Windows→Linux tinha a forma correta. A frase «nenhum bloqueador novo localizado no delta» descrevia aquele exame restrito, mas **não sustenta a prontidão operacional do pacote**, contrariada agora pela execução documentada.

Os reparos estáticos WSL-01/02 continuam descritos pelos respectivos deltas, mas o pacoteV2 consumido não é uma qualificação WSL aprovada. As capturas registram término/EOF normais e os erros de abertura reais; isso não exercita exceção na thread leitora, overflow Linux, hook, journal, latch ou timeout. Não usar a falha para alegar aprovação ou reprovação desses controles não alcançados.

## Rótulo de incerteza e preservação

O launcher marca `UNCERTAIN_ORPHAN_STATE` quando seu helper de limpeza não entrega a prova prevista. Aqui a limpeza também não abriu seu script. Esse rótulo conserva a falta de evidência exigida pelo contrato; por si só não comprova processo Linux vivo nem ausência de órfãos. Não inspecionei processos vivos nesta unidade. ROOT conduz separadamente a inspeção somente de leitura das identidades.

Os PIDs registrados são identidades históricas dos processos Windows; não devem ser usados para sinalizar processos atuais. A ausência dos recibos/claims Linux e da pastaCASE foi conferida como evidência de disco limitada, em conjunto com a falha de abertura, sem inferir ausência global de processos. Não houve sinal, cleanup, WSL, hook, controle, stub, ciência ou chamada remota nesta errata.

## Duas alternativas, somente propostas para nova decisão

**A — representação POSIX explícita para argv.** Usar uma base separada `PurePosixPath` ou `posixpath.join` para construir o token Linux, mantendo `Path` concreto para operações de arquivo no host correspondente. Essa separação torna o destino do token explícito. Não basta substituir cegamente a variável global por um caminho puro: o código Linux também usa `BASE` para leitura/escrita e precisa preservar suas operações concretas. É a alternativa conceitualmente preferida, sem implementação ou adoção aqui.

**B — serialização explícita com `as_posix`.** Manter a construção existente e serializar o token final por `(LINUX/script).as_posix()`. É um delta menor para o literal fixo `/mnt/c/...`, mas ainda depende da análise do caminho pela classe do host; não generalizar a drivesWindows, UNC ou entrada arbitrária. O fonte local de pathlib sustenta a operação; nenhuma variante foi avaliada como controle nesta unidade.

Uma futura proposta deve preservar argv em lista, espaços dentro de um único token, destino absoluto POSIX, ausência de barras invertidas, mesma construção para supervisor/cleanup e coerência da identidade parent/child. Isso é condição documental candidata, não autorização para teste ou terceiro lançamento. Qualquer nova unidade exige decisão específica e identidade própria; **o pedido consumido4f5d permanece terminal**.
