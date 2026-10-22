# Preparação do transporte WSL corrigido

[REAL — preparação] Novo request 5b67deb6-fec2-43d6-af61-347f1a3e5b83, caso WSL_CACHE_LATCH_POSIX_002, em pasta separada. A decisão gerencial seleciona a alternativa 2: eventual consumo único somente após pins, revisão independente da integração/delta e autorização específica de ROOT. O comando está proposto; nenhum CLAIM, autorização ou execução foi produzido aqui. O request antigo 4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf permanece terminal e intacto.

## Delta permitido

A representação PurePosixPath do mapa 533, revisada em 536, produz o token Linux por as_posix; Path concreto permanece para I/O do host. Raízes, request/caso e pins são novos e coerentes. Somente a observação e validação explícitas de argv, solicitadas por ROOT, foram acrescentadas à integração.

Cada receptor — supervisor, cleanup e filho — lê seu próprio /proc cmdline e sys.argv antes de controle/hook ou sinal. Grava ARGV_SUPERVISOR.json, ARGV_CLEANUP.json ou ARGV_CHILD.json por escrita exclusiva, fsync e releitura. Gravar antes de exigir igualdade permite conservar diagnóstico de desvio. Uma falha anterior à observação pode não deixar recibo de argv; sua ausência nunca significa igualdade. A comparação verifica listas completas e identidade, não só booleanos autodeclarados.

A mesma identidade de processo observada é vinculada ao claim/resultado do papel. Os pais recomputam a expectativa, comparam os recibos físicos e vinculam o processo antes de aceitar PASS. O filho é conferido pelo supervisor e pelo launcher Windows; este confere também supervisor e cleanup. As observações integram CASE_RESULT, LINUX_RESULT, CLEANUP_RESULT e o RESULT externo. Não há processo receptor extra.

INVENTARIO_INTERFACE.json traz exemplos esperados como dados, com nonce placeholder: dez tokens internos, quatorze externos e quatro em sys.argv. O caminho Linux com espaços permanece um elemento. O executável Windows conserva sua sintaxe. Não há split, shell string, aspas embutidas ou conversão genérica de drive/UNC. Os exemplos não são observações.

## Preservação e limites

O AST integral de worker, linux_control e launch_windows, após rebase de raiz/identidade, volta ao original ao remover apenas os acréscimos de recibos. As funções antigas de common permanecem iguais exceto argv_for; o prefixo de common coincide com a candidata revisada após rebase. Os patches completos e após rebase estão em delta/. sources/audit_guard.py é cópia de bytes exatos.

Contrato limits, runtime, single_control, identity_and_claims, pins Windows/Linux e condições antigas de falha permanecem iguais. Conservam-se STOP durável, gate flock antes de Popen, pidfd com identidade exata, captura com EOF/erros e clip antes de append, journal e checkpoints. A única fixture continua VALUE=42 pelo SourceFileLoader, cache pyc negado, latch persistente e callback zero.

Prazos nominais: total60s, primário40s desde entrada, cleanup/coleta55s, supervisor Linux15s, trabalho do filho9s e cleanup Linux12s; retenção32768 bytes por fluxo/processo. Até um primário, um cleanup apenas de identidade e um filho. ENTRY não foi deslocado: as novas leituras e gravações consomem os mesmos prazos. Sem retry/resume. PASS físico provisório exige saída final zero, captura íntegra e prazo externo; não há garantia de deadline rígido do sistema operacional.

Desvio/falha de argv exige exceção e saída não zero antes do controle/sinal. A limpeza existente permanece restrita às identidades exatas; falta de prova pode gerar estado incerto, sem fallback/repetição.

## Verificação realizada

O auditor documental próprio executou 113 conferências de fontes/AST/JSON/pins. Não importou candidatos, avaliou construtores, executou stubs ou controles. Foram relidos17 pins: três arquivos Windows e quatorze arquivos admitidos de runtime/stdlib Linux por UNC. Após recusa inicial do sandbox, a leitura restrita foi autorizada. Nenhum wsl.exe ou Python Linux foi iniciado. Não se alega resolução do alias do interpretador por UNC; o futuro preflight mantém a exigência exata de realpath.

Isso mede preparação documental e custódia, não duração/custo/qualificação do controle. Transporte real e resultado desta unidade continuam OPEN. Nenhum D, PE, LAL, solver, série observada, provider ou rede. Memórias compartilhadas e ledger não foram alterados; a rota foi consultada e ROOT fará o registro de coordenação. A entrega termina aqui para revisão independente por proveniência.

Pins relidos:

- CONTRATO_WSL.json: 15992 bytes; SHA-256 f8b94deaad13f14e1246431b36f4264ffa99f2314c527768b5869e5b66015b1a.
- RECIBO_ANALISE_ESTATICA.json: 13353 bytes; SHA-256 53e125ef732a16b4ca5a2fb07d9a11d8ea120faa0fbd9a6e663e2db51ed2204b.
- RUNTIME_READONLY_RECEIPT.json: 4724 bytes; SHA-256 03681b4c638175a4414f09a5d2311d5cb2ae9fc6b1ce7fff3db22d1669b957dd.
- COMANDO_PROPOSTO_NAO_EXECUTADO.json: 1072 bytes; SHA-256 6952fc05ddd25af5d25d04d8206bdd3ae4166069ce46b9f688fbbe81be40d90e.
