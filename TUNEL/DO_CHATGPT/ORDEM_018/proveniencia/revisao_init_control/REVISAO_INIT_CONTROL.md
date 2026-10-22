# Revisão independente do controle de inicialização — ORDEM_018 F3

[REAL — revisão documental/estática, 06/10/2026] **Um achado acionável P2: INIT-01.** A alternativa B tem preparação coerente para a dependência ASD, a substituição pela PSD analítica e os bloqueios científicos. O comando direto do pacote seq457 requer supervisão externa antes de uma execução delimitada em 60 s. Nenhum controle, waveform, likelihood, sampler ou PE foi executado nesta revisão.

## INIT-01 — teto de parede e recibo terminal

COMANDO_CONTROLE_NAO_EXECUTADO.json, linhas 3–16, chama diretamente control_init.py. Não há supervisor nesse comando. No controle, linhas 37–47, a conferência das entradas, dos 1.162 pins do runtime, das dependências e STARTED precede a instalação do temporizador, linha 53. A medição de parede começa na linha 50, também excluindo a preparação.

O handler de SIGALRM é Python; não é um encerrador externo contra espera indefinida ou rotina nativa que adie sua execução. RLIMIT_CPU(45,50) limita CPU, não espera/I/O. Um encerramento duro pode impedir a gravação de RESULT.json no finally, linhas 162–170. Portanto o comando não garante prazo global de 60 s nem recibo terminal. É conclusão estática; nenhum travamento foi produzido.

Correção concreta: supervisor aditivo pinado, com decisão específica, prazo monotônico desde entrada/launch, timeout externo, encerramento do grupo e recibo de exit/sinal/timeout inclusive antes de STARTED/RESULT. Reserva exclusiva da tentativa, sem retry, sem CLAIM científico ou nova campanha P3. Preservar pacote457. A coordenação aceitou o achado e prepara delta separado; ele ainda não está avaliado neste snapshot.

## Integridade e limite da verificação

O script próprio review_init_control_static.py concluiu **113 verificações estáticas/de integridade**, com 53 fontes registradas por bytes/SHA256:

- 31 arquivos do manifesto, inclusive backup, e 24 entradas do contrato;
- 16 snapshots de dependências: 15 correspondem ao manifesto congelado de 1.162 arquivos; apenas um ASD é adicional;
- correspondência do contrato com comando, alternativa B e PREPARED_NOT_EXECUTED;
- existência, por AST, dos dez métodos WFG/GWT envolvidos pelo controle;
- ausência de CONTROL_INIT_001, DECISAO_CONTROLE_INIT.json, CLAIM.json e AUTORIZACAO_COORDENACAO.json na pasta na hora da conferência.

Não importei código do autor, executei expressões dele, iniciei WSL ou abri NPZ com NumPy. O arquivo sintético foi lido somente como bytes para hash. Os 1.162 arquivos instalados não foram relidos nesta revisão: conferi o manifesto e as cópias locais. O controle futuro é que verificará a instalação atual.

Pins efetivamente lidos:

| Artefato | Bytes | SHA256 |
|---|---:|---|
| Manifesto457 | 11557 | 0aa5a11869c5ac03f92f672ccb3ec87c61c4abf7754c478aabd75846e48b5c8f |
| Contrato | 12962 | ec8ca95137da8f27ffeb1636cbe6fe779463286d62b341387a23b33649ced6a9 |
| control_init.py | 12654 | ee669d8c19434cd01315e3ed9f604f3c5f270c7edf5a86f3c2e680b7be4fcd95 |
| init_detectors.py | 4261 | 95dfef3df297d981a1a56fda4e617a0595768c98bee96979dfc208db55dd8890 |
| Snapshot ASD | 71136 | eb5ec9b081c3d86d2f4257b9aff6a57566d168b8a95e5e57b7909eebad021780 |

## Factory B e PSD

[DERIVED — fontes pinadas] networks.py, linhas 440–459, lê as configurações H1/L1; seu OSError pode virar ValueError “not implemented”. Ambas apontam ao mesmo arquivo instalado: /opt/lal_env/lib/python3.12/site-packages/bilby/gw/detector/noise_curves/aLIGO_O4_high_asd.txt. É a única nova leitura autorizada, por caminho exato; não é diretório, strain D ou posterior.

build_B, linhas 24–40, verifica bytes/hash, recusa homônimo no cwd, verifica o caminho da ASD carregada e substitui a PSD por objeto novo alimentado por f/psd do NPZ qualificado. A identidade do objeto novo é conferida.

verify_analytic_state, linhas 43–69, exige campos de arquivo None, igualdade exata da grade/PSD bruta/PSD efetiva, banda20–1024 Hz, duração32 s, amostragem4096 Hz, início999999984, window_factor1, ausência de notches e geometria compatível. O controle verifica após inserir n+s e antes de GWT (linha130), e novamente nos interferômetros da GWT (147). A curva default não é carregada na likelihood como PSD final.

O NPZ é aberto com allow_pickle=False. Identidade/normalização dos dois rótulos e hashes noise/signal/injected são comparados aos recibos já qualificados. A soma de SNR sobre arrays congelados não gera waveform/PSD ou centro observacional.

GWT, linhas145–222, mantém inativas as quatro marginalizações; sky/geocenter evita detector de referência extra. Sucesso dinâmico continua OPEN. A proposta DELTA_ALTERNATIVA_B.patch para um futuro P3 não foi aplicada ou certificada como integração: esta revisão cobre o controle independente.

## Bloqueios científicos e zeros

[REAL — mecanismos presentes; OPEN — qualificação dinâmica] O controle envolve o source importado e synthetic_only220, cinco métodos WFG, cinco GWT e bilby.run_sampler com contadores e exceção. wraps e __signature__ preservam a introspecção; signature/getfullargspec/source_parameter_keys são comparados no gerador efetivamente criado.

Antes de PASS, todas as tentativas e o contador nativo devem ser zero; caches de waveform/ruído devem ser None. Bloqueios capturados por bibliotecas também impedem PASS. Não há import direto de Dynesty ou chamada a run_sampler no AST do controle. Isso cobre o caminho pinado examinado, sem pretensão de envolver universalmente cada função das bibliotecas.

Esses zeros são condições codificadas; **não são contagens observadas de uma rodada nesta revisão**. Inicialização bem-sucedida, custo e inventário dinâmico permanecem OPEN.

## Allowlist e tentativa única

O hook só começa após os imports fixos/preload cp437. Depois dele, open por caminho limita leituras a entradas/runtime/dependências; as escritas ficam em RESULT.json, temporário e EDOM_LOG.jsonl. STARTED e mkdir precedem o hook. Rede/processos filhos selecionados são recusados.

Não há auditoria integral dos imports anteriores, syscalls nativas ou eventos de metadados/rename; o escritor conhecido usa destinos fixos e temp→replace. O contrato declara que não é confinamento OS. O inventário de open não deve ser promovido a prova de todos os acessos do processo.

A decisão deve corresponder ao hash/alternativa. mkdir(exist_ok=False) recusa segunda saída depois da reserva. Não remover a reserva nem repetir tentativa incerta. Ausência de CLAIM científico é adequada para este controle, não motivo para criar campanha. O supervisor deve registrar a tentativa separadamente.

**Parecer limitado:** preparação científica/PSD coerente; INIT-01 P2 precisa ser resolvido antes da execução. Preservar esta auditoria e revisar apenas o delta. Sucesso futuro não autoriza P3/PE, não qualifica convergência/cobertura e não abre D. Originais preservados; sem rede, execução upstream, ajuste, executor remoto ou mudança de gate.
