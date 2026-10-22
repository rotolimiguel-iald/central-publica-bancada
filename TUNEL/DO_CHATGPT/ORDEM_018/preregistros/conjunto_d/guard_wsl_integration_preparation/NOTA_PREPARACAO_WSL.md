# Qualificação stdlib na WSL — preparação de um controle

**PREPARATION_ONLY_NOT_AUTHORIZED_NOT_EXECUTED.** Request `4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf`, caso `WSL_CACHE_LATCH_001`. Zero execuções de candidato/WSL/runtime-alvo, hooks, journals, autorizações e CLAIMs nesta entrega. Os processos Python Windows usados aqui só escreveram artefatos e fizeram leitura, AST e hashes.

## Pergunta e fronteira

[INPUT] Qualificar no interpretador da bancada somente esta sequência: SourceFileLoader real tenta ler o cache pyc sintético; PermissionError é absorvida; o fonte trivial `VALUE = 42` termina normalmente; o journal original grava e retorna de fsync; o checkpoint seguinte impede callback trivial e o checkpoint final continua bloqueado.

A unidade Windows `278b56a3` já foi consumida uma vez com três PASS (recibo ROOT, mapa509). Não a reproduzimos. Este é um controle novo de plataforma com identidade nova e um único caso, não novo teste físico ou retomada INIT003. Os 21 doubles/mapa497 e o guard revisado/mapa491 são referências delimitadas; nenhum deles certifica antecipadamente o runtime WSL.

## Alternativas comparadas

| Alternativa | Decisão antes da implementação |
|---|---|
| A — launcher Windows, supervisor Linux e um filho descartável; helper Linux separado somente para limpeza/inspeção | Escolhida: inclui partida WSL no prazo nominal, captura independente e inspeção dos processos Linux. O helper de limpeza executa zero controles. |
| B — somente supervisor Linux e Windows aguardando | Menos código, mas a partida/captura WSL e a conferência após perda de saída ficam fora do seu relógio; rejeitada para este recorte. |

Foi adotado teto nominal de 60 s, dentro do máximo permitido, com 40 s para a fase principal incluindo partida WSL, limpeza até o segundo55 e reserva final de5 s. Não alegamos que30 s são impossíveis nem que60 s foram medidos: é orçamento preventivo fixado sem rodar benchmark. Supervisor Linux:15 s desde entrada, trabalho do filho no máximo9 s; helper de limpeza:12 s. IO, escalonamento e inicialização do SO não têm teto absoluto garantido por este código cooperativo.

## Runtime e fontes locais

[REAL documental] Leitura UNC restrita de `/opt/lal_env/pyvenv.cfg` registra versão3.12.3 e executável `/usr/bin/python3.12`. O hash atual desse binário coincide com a linha correspondente do recibo `VERIFICACAO_RUNTIME_INIT003.json`, previamente pinado. O recibo histórico ENVIRONMENT_PREFLIGHT também registra `/opt/lal_env/bin/python`,3.12.3. Nenhum interpretador WSL foi iniciado para esta conferência.

O acesso UNC ao symlink `/opt/lal_env/bin/python` não resolveu o alvo; isso está no recibo. A futura pré-validação Linux exige explicitamente `sys.executable` nesse caminho, seu realpath `/usr/bin/python3.12`, versão3.12 e hash do binário. Não presumimos resolução UNC do symlink. `-I -S -B -X utf8` impede site e escrita de bytecode; em CPython3.12, `-S` pode deixar prefix no ambiente base. A qualificação usa o mesmo binário com bibliotecas stdlib, não importa o ambiente científico.

[REAL documental] O fonte local `/usr/lib/python3.12/importlib/_bootstrap_external.py`, linha1087, chama `get_data(bytecode_path)` dentro de `try/except OSError`; linha1131 condiciona escrita à ausência de `dont_write_bytecode`. Isso fundamenta o mecanismo proposto. Sua execução e absorção reais continuam [OPEN]. Pins:14 arquivos Linux de runtime/stdlib,6 fontes/identidade locais e3 binários Windows; hashes medidos, não de memória. O sandbox negou a leitura UNC inicial; escalonamento restrito de leitura conseguiu os arquivos admitidos. Não houve rede, provedor ou leitura de dados D.

## Instrumento e aceite do único caso

`sources/audit_guard.py` é cópia byte a byte da fonte original revisada. O worker é instrumento novo, sem os outros dois casos Windows. A única fixture tem uma linha constante. Antes do hook, abre journal e descritor do resultado; depois, a allowlist de leitura contém apenas o fonte sintético e o journal exatos. O cache é alvo negativo obrigatório. Novas escritas por abertura, novos processos, rede, ctypes, imports adicionais e execução de outro fonte são recusados. Descritores já abertos de journal/resultado e stdout são usados; isso não é confinamento de syscalls/código hostil.

`audit.__cantrace__ = True` permite observar os.write/fsync reais via sys.setprofile. Nenhum builtin ou journal é substituído. O resultado exige um bloqueio esperado, nenhuma operação inesperada, primeira ocorrência/sequence1 retida, fonte retornando normalmente, callback0, checkpoint seguinte e final bloqueados, retorno de escrita/fsync e JSONL físico idêntico ao snapshot. PermissionError simplesmente propagada não satisfaz o caso. Retorno de fsync não prova persistência após perda de energia.

O supervisor cruza resultado físico e stdout, stderr vazio, exit0, journal/hash/linhas e identidade. O launcher exige também o exit0 do supervisor e a limpeza externa sem alvos mortos no caminho de sucesso. Um PASS rápido não exercita intencionalmente timeout, kill ou falhas de infraestrutura.

## Identidade, claims e limpeza

`AUTORIZACAO_ROOT.json` não existe nesta preparação. Sua criação exige revisão/decisão específica ROOT, request/contrato exatos, um controle, um filho de controle e60 s; exemplo de esquema no contrato não é autorização. `CLAIM.json` exclusivo, fsync e readback antecedem `wsl.exe`. Linux grava seu claim antes de Popen; o filho verifica PID/nonce/start_ticks do pai e grava CASE_CLAIM antes de executar guard, fixture, hook ou journal. Existência de CLAIM/RUN/RESULT impede replay; não há reset/retry/resume.

Os comandos Linux são fixos e carregam request/nonce. `/proc` vincula PID, start_ticks, boot_id, exe e argv. O sinal usa pidfd aberto antes da conferência, evitando sinal por PID solto. A capacidade pidfd é conferida no supervisor antes do controle. Não há pkill, taskkill, encerramento de distribuição WSL ou sinal em grupo amplo.

O launcher grava STOP durável antes da limpeza. Um gate flock comum cobre checagem de STOP e lançamento do filho; a limpeza inspeciona sob o mesmo gate. Um supervisor atrasado deve ver STOP antes de lançar. O helper só pode sinalizar os comandos/nonce exatos desta unidade. O launcher controla os clientes `wsl.exe` pelos handles dos próprios Popen. Falha de identidade/inspeção/limpeza dá `UNCERTAIN_ORPHAN_STATE`, nunca PASS, e requer recuperação específica sem repetir o caso.

A afirmação permitida é **ausência das identidades vivas controladas no instante final inspecionado**, com fence persistente contra novo filho. Não é ausência absoluta de todos os órfãos do sistema; zombies/entradas que desapareceram não são processos vivos inferidos como execução pendente. Se a plataforma impedir comprovar as identidades próprias, o estado fica incerto. Nenhuma promessa geral de isolamento de processos nativos decorre deste teste.

## Prazo e observação final

O relógio Windows começa na primeira leitura monotônica após import time, antes dos demais imports e pré-validação; o tempo de bootstrap anterior só aparece na medição externa de ROOT. O prazo nominal inclui WSLstart e os IOs subsequentes. Há verificações após gravar o recibo e após stdout/flush; atraso retorna código nãozero e invalida JSON provisoriamente PASS. O aceite ROOT deve cruzar **arquivo físico, captura completa, exitcode final e duração externa observada**, sem tratar um recibo isolado como sucesso tardio.

Os limites são cooperativos. A captura retém no máximo32KiB por fluxo/processo e overflow falha. Wait/reap/join são finitos. IO do sistema ou indisponibilidade WSL pode exceder o orçamento nominal; o código não se apresenta como hard deadline do SO. O recibo separa duração antes do IO final da observação externa do encerramento.

## Estado de preparação

[REAL estático]55 conferências passaram: AST/imports, pins locais/Windows, vínculo das14 leituras Linux, escopo único, claims/nonce/identidade, fence, verificações de prazo, guard idêntico e ausência de consumo. São conferências do texto/custódia, não testes dinâmicos. A nova preparação não alterou guard original, fonte científica, driver, sampler, allowlists científicas ou memórias compartilhadas.

Entrega para revisão ROOT: contrato, comando proposto, worker, supervisor/limpeza Linux, launcher Windows, protocolo comum, pins, recibo estático e manifesto. Nenhuma autorização para waveform, likelihood, sampler, PE, D ou jobs terminais é inferida da qualificação stdlib.

Ajuste ainda na preparação: inspeção de processos do mesmo UID agora falha visivelmente em PermissionError, em vez de poder omitir identidade inacessível. Processos de outros UIDs ficam fora do conjunto candidato; nenhum sinal lhes é enviado. Delta e backups preservados, sem execução de limpeza.
