# Revisão independente da integração WSL com transporte corrigido

[REAL — revisão estática] Pacote request **5b67deb6-fec2-43d6-af61-347f1a3e5b83**, caso **WSL_CACHE_LATCH_POSIX_002**, raiz nova guard_wsl_corrected_transport_preparation. **Nenhum defeito material bloqueante identificado no escopo delimitado.** A preparação está apta à decisão específica de ROOT prevista pela gerente. Este parecer não é autorização de execução nem evidência de transporte real; não consome a unidade. Mapa antes:546; fontes e hashes no recibo desta revisão.

## Identidade, custódia e delta

A decisão2ea distingue pacote novo de reabertura do request4f5d terminal e limita o futuro consumo a um primário WSL, no máximo uma limpeza e um filho de controle. A nova identidade e as raízes Windows/Linux coincidem entre contrato, quatro instrumentos, inventário e comando proposto. A representação de destino usa PurePosixPath e as_posix; Path concreto permanece no I/O. A lista de argumentos conserva o caminho com espaços num elemento; não há shell, split de comando, aspas inseridas ou conversor genérico.

Conferi por bytes os27 artefatos do manifesto, o próprio manifesto, pins locais do contrato, fontes documentais e o retrato de24 arquivos da unidade terminal, inclusive seus CLAIM/RESULT. A cópia audit_guard coincide com a anterior. Os três pins Windows são relidos nesta revisão. Os14 pins Linux são confrontados com o recibo de leitura UNC já selado; **não foram relidos no host Linux nesta revisão**, não se invocou WSL e não se resolveu novamente o alias do interpretador. A validação futura em Linux continua exigindo o binário real /usr/bin/python3.12 e os pins completos. Isso preserva a diferença entre recibo documental e preflight efetivo.

O delta semântico após a troca de raiz/identidade contém a representação POSIX e os recibos de argumentos, junto de sua propagação e revalidação. Funções críticas que não deveriam mudar foram comparadas por AST após normalização da identidade/raiz; o guard foi comparado byte a byte. Os limites e o controle sintético permanecem os anteriores. A rotina de auditoria do autor foi conferida por hash como artefato, não executada.

## Transporte observado e revalidação

common.py66–108 constrói o mesmo argv de dez elementos para lançamento, inspeção e expectativa. O índice6 é o script; expected[6:] tem os quatro elementos de sys.argv. Supervisor e limpeza passam por linux_control.py137–146: observam sua própria identidade /proc, capturam sys.argv e escrevem o recibo exclusivo antes de aceitar a igualdade. O filho faz o mesmo em worker.py18–26 antes de CASE_CLAIM, execução do guard, fixture e hook. Nenhum valor recebido é fabricado pelo pai.

Cada recibo contém request, nonce, papel, PID, start_ticks, boot_id, executável e argv. validate_observed_argv recompõe os tokens; não aceita apenas flags booleanas. O supervisor verifica o recibo físico do filho, identidade do processo, PID retornado pelo Popen e parentesco; Windows verifica supervisor, filho e limpeza contra seus recibos físicos e identidades incorporadas. Portanto, os três papéis participam da aceitação; o inventário de exemplos continua explicitamente não observado. Fontes: common.py83–108; linux_control.py46–62/137–148; worker.py18–26; launch_windows.py84–93/105–110.

## Consumo único, processos e limpeza

O launcher exige autorização ROOT ligada ao contrato/revisão e recusa CLAIM/RUN/RESULT existentes. A criação exclusiva e fsync/readback de CLAIM antecedem wsl.exe. LINUX_CLAIM antecede Popen; CASE_CLAIM antecede o controle. Uma entrada direta repetida em qualquer papel encontra também seu ARGV_* exclusivo e falha antes de novo controle. Não há ramo de retry, resume, execução científica ou chamada remota.

STOP é persistido pelo pai antes da única limpeza. O supervisor verifica STOP antes e dentro do mesmo flock de lançamento; o filho também verifica STOP/prazo antes do caso. A limpeza usa a mesma trava e reinspeciona as identidades delimitadas. Um supervisor atrasado pode produzir metadados ou falhar, mas não lançar outro filho depois de adquirir a trava e ver STOP. A inspeção não alega ausência global de todo processo do sistema.

Os sinais usam pidfd aberto antes da releitura de identidade; exe e argv exatos incluem request/nonce. O identificador de processo estável evita sinalizar um PID alheio reutilizado; o filho verifica ainda PID e start_ticks do supervisor contra LINUX_CLAIM. Windows usa handles de seus próprios subprocessos, sem taskkill/pkill/encerramento amplo da distribuição. Erro de inspeção de processo do mesmo UID não vira ausência; produz incerteza visível. Essas são guardas cooperativas para os instrumentos pinados, não isolamento contra código hostil. Fontes: common.py50–81; linux_control.py13–27/64–91/104–135; worker.py15–20; launch_windows.py71–124.

## Prazo, captura e aceitação

O total nominal de60s começa na entrada do launcher, inclui preflight, WSL, limpeza, coleta, persistência e stdout final. Há40s para o primário e até55s para a limpeza; Linux reserva15s ao supervisor,9s ao trabalho e12s à limpeza. Há no máximo duas chamadas WSL de papéis distintos e um filho. Não há promessa de prazo duro do sistema operacional.

Após persistir RESULT, Windows confere o relógio; confere novamente depois de stdout com flush e só então pode retornar0. Supervisor e limpeza também verificam depois de seu recibo e depois de stdout. Assim, JSON provisório PASS não basta: saída externa0 e tempo total observado são requisitos existentes do contrato. I/O que bloqueie pode exceder o prazo nominal, mas não recebe aceite por este parecer.

A captura Windows conserva até32768 bytes por fluxo e registra overflow, erro, EOF e término de cada leitor. Não confunde thread encerrada com EOF. Linux conserva o mesmo limite, rejeita overflow e exige filho terminado/recolhido. A aceitação exige igualdade entre JSON físico e stdout, stderr vazio e captura íntegra; qualquer limpeza que tenha precisado matar um alvo impede PASS. Fontes: launch_windows.py13–64/96–141; linux_control.py29–44/98–102/132–135; contrato142–156/202–226.

## Leitura, hook e alcance

O controle único continua sendo uma fonte sintética VALUE=42: uma abertura de pyc recusada, PermissionError absorvido pelo importador e latch persistente barrando os checkpoints. O guard mantém o primeiro evento antes de serialização/I/O, journal preaberto com write completo/fsync, e erro de journal persistente. O pai confere journal físico e registros de chamadas reais.

Após o hook, somente fixture/journal exatos podem ser abertos para leitura; novos opens de escrita, outros imports/compile/exec, rede/subprocessos e operações listadas são recusados. Os recibos usam FDs já abertos. Nenhum dado observado, D, PE, waveform, likelihood, LAL ou solver participa. Não se altera allowlist científica. Essa unidade não certifica importação científica, integração nativa, caminho de timeout ou convergência.

## Decisão e limites

[DERIVED — leitura de implementação] A integração corrige o defeito de tipo de caminho que consumiu4f5d e exige evidência real de recebimento dos tokens antes do futuro PASS. [OPEN] Recebimento efetivo, resultado do hook e custo dependem da única execução específica que ROOT poderá decidir conforme a gerente. Não se infere resultado do controle a partir desta revisão.

As alternativas já registradas são suficientes: (A) launcher Windows + supervisor Linux + filho e limpeza delimitados, escolhida, cobre inicialização/captura; (B) somente supervisor Linux, não escolhida, não cobre independentemente esses limites externos. Não há bloqueio que exija novos testes genéricos ou novo requisito científico. Uma futura falha/incerteza permanece terminal; a inspeção/recuperação restrita deve preservar identidades e evidências, sem repetição automática.

[REAL — ações desta revisão] Somente leitura de bytes/texto/JSON/AST e gravação dos próprios parecer/recibo/manifesto. Zero importação ou execução dos candidatos/WSL/controles, zero CLAIM/autorização, zero observados. Pacote, unidade terminal, memórias compartilhadas e ledger preservados.
