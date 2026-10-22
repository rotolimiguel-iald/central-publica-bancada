[REAL] A-1.a — reprodução NÃO PAGA: duas falhas de recurso, sem julgamento da validade do contrato.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

Arquivo: cópia byte a byte de v3/ContratoQG.lean (contrato v2 na árvore de dependências).
Fonte SHA256: 02fd013827dca25159f262c66acc41cc2dcdc2a479abacd7afc2e9b8048e67fb

A primeira execução usou os trabalhadores padrão; a segunda usou -j1. Ambas mantiveram o limite de 8 GiB por processo e terminaram com std::bad_alloc. Nenhuma produziu a reprodução esperada de rc 0. O rc de recurso não é o rc 1 no campo nomeado exigido para os probes negativos.

Não haverá terceira repetição do mesmo contrato nesta rodada. Não foi alterado o código da prova, o limite, o kernel nem qualquer olean canônico.

Tempo de máquina Lean: 49.891000 s de parede; CPU agregada 46.968750 s. Horas de compilação: 0.013858611; máquina pesada Parte B: 0 h.

O primeiro comando e sua repetição estão integralmente registrados nos recibos abaixo; cwd = kernel canônico. Pico medido é memória comprometida de processo Windows Job, não RSS. Varredura de arquivos canônicos posteriores ao marcador: zero em ambas, sem erro de leitura.

C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\v3\reproduction_01.json
Recibo SHA256: ed29957462a9fcc0700bcc0c8e331bf567122119c5058a32d2f26678bf5019c4
Log SHA256: 0840a1348568c407aea02f172420f9ec80fc35afb4c820b0bc6203a94c9e6a7b
rc=3221226505; pico=8589934592 bytes; parede=26.125 s.
Comando (vetor de argumentos): ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe", "env", "lean", "-M8192", "-R", "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_016_QG\\A1\\v3", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_016_QG\\A1\\v3\\ContratoQG.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_016_QG\\A1\\v3\\ContratoQG.lean"]

C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\v3\reproduction_02_single_worker.json
Recibo SHA256: 80465e39d9a767844fe0e7ec73fbb60d1ce38cb7c3214a45ca647e1918ad2d5a
Log SHA256: 0476729d89ccebeaab38ba5a73e055ebae14b87efaff35f0e11421de282505b8
rc=3221226505; pico=8589930496 bytes; parede=23.76600000000326 s.
Comando (vetor de argumentos): ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe", "env", "lean", "-j1", "-M8192", "-R", "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_016_QG\\A1\\v3", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_016_QG\\A1\\v3\\ContratoQG.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_016_QG\\A1\\v3\\ContratoQG.lean"]

[OPEN] Reprodução dependente: W5, v3, v3.1, teoremas, paredes e probes não recebem rc inferido. Os resultados da gerência permanecem DECLARADOS para esta reprodução, não passam a REAL por referência.

Próximo ramo obrigatório: A-1.b. Controles algébricos com dependências mínimas podem ser medidos independentemente; não substituem a compilação contra ContratoH2/ContratoH3 v3.1. A extensão A-1.c deve conservar essa distinção. Nenhuma fronteira nem gate mudou.
