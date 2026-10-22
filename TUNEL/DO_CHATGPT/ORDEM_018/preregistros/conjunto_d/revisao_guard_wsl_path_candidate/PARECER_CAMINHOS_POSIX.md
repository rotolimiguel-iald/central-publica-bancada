# Revisão independente da candidata de representação POSIX

[REAL — documental] O delta do mapa 533 não apresenta achado bloqueante no recorte de caminhos literais e três papéis fixos. As 119 conferências documentais/AST/pins passaram. [DERIVED] A separação entre representação POSIX transportada e caminho concreto de I/O remove a dependência do sistema hospedeiro na composição do token do script. [OPEN] Este parecer não valida transporte real por wsl.exe, abertura do script Linux, hooks, journal, controle ou ciência. Nenhuma candidata foi importada ou executada.

## Objeto, identidade e limite

A unidade histórica `4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf` permanece terminal. Foram lidos o manifesto da candidata, seu contrato, delta, inventário, exemplos como dados, fontes de biblioteca padrão e evidência documental da falha. O exame é do reparo de representação; não requalifica a auditoria científica inteira. As fontes, os CLAIMs e resultados consumidos permanecem intactos. Não foi criado request, launcher, CLAIM ou autorização.

A candidata é `common.py.candidate.txt`, uma cópia textual que conserva a identidade e a raiz históricas para descrever o delta. Essa identidade não é uma proposta de consumo. O arquivo não deve ser renomeado, aplicado ao pacote consumido ou executado por força deste parecer. Integração futura exige decisão própria, identidade apropriada e pins novamente conferidos.

## Causa anterior e semântica da candidata

No `common.py` consumido, a linha 8 construía LINUX com Path e as linhas 64–66 serializavam `str(LINUX/script)`. A fonte Windows de pathlib seleciona WindowsPath quando os.name é nt. Os registros reais de lançamento e cleanup contêm o token com barras invertidas no índice externo 10. Portanto, preservar esse trecho por igualdade AST não preservava a semântica de destino pretendida. Essa lacuna da revisão 526 continua registrada na errata 529; não é apagada por esta candidata.

Na candidata, linhas 3 e 8 introduzem explicitamente PurePosixPath para LINUX_ARGV_ROOT. Linhas 10–11 mantêm Path concreto para I/O e selecionam WIN no Windows. Linhas 66–68 serializam exclusivamente `(LINUX_ARGV_ROOT/script).as_posix()` no token do script. O Path concreto LINUX pode assumir tipo WindowsPath no Windows, mas já não alimenta argv; ali BASE seleciona WIN. No Linux, LINUX permanece Path concreto para I/O.

A leitura de fonte, além da comparação AST, sustenta esta cadeia: PurePath.__new__ só seleciona a variante por sistema quando cls é exatamente PurePath; instanciar a subclasse explícita PurePosixPath conserva essa classe. Seu parser/flavour é posixpath, e a operação de junção reconstrói type(self). A serialização usa separador POSIX. Os nomes relativos fixos linux_control.py e worker.py não introduzem nova âncora. Espaços não são separadores de caminho e continuam parte da mesma string. Não se inferiu um conversor genérico de drives Windows, UNC ou nomes arbitrários.

## Todos os pontos de transporte e de identidade

| Índice externo no argv de wsl.exe | Conteúdo e tratamento |
|---|---|
| 0 | Caminho Windows de wsl.exe; deve conservar sintaxe Windows. |
| 1–3 | `--distribution`, `Ubuntu-24.04`, `--exec`; literais sem transformação. |
| 4 | `/opt/lal_env/bin/python`; string POSIX fixa, não Path Windows. |
| 5–9 | `-I`, `-S`, `-B`, `-X`, `utf8`; cinco tokens preservados. |
| 10 | Script Linux: único token construído por PurePosixPath e as_posix, absoluto, com barras normais e espaços preservados. |
| 11–13 | Papel, request e nonce; tokens próprios, sem conversão de caminho. |

O argv interno tem dez elementos; o externo tem quatorze. Para supervisor e cleanup, o script é linux_control.py; para child, worker.py. `launch_windows.py` 50–53 monta a lista externa usando argv_for; seus lançamentos principal e cleanup seguem o mesmo construtor. `linux_control.py` 75–78 usa argv_for para o filho. `worker.py` 13–18 e common.scoped_processes usam esse mesmo construtor para identidade esperada. Assim, a grafia usada para lançar supervisor/filho e reconhecer processos/limpeza deriva da mesma representação POSIX. Não há um segundo construtor independente de token de script nos quatro instrumentos examinados.

O pacote não acrescenta --root. Esse nome aparece no contrato somente como hipótese de interface futura; não representa um token transportado nesta unidade. Os exemplos de papéis, comprimentos e posições foram comparados como dados congelados, sem avaliar o construtor ou o candidato. Os placeholders de nova identidade nos exemplos não criam uma identidade executável.

## Espaços e fronteira de subprocess

No Windows, Popen recebe lista e a biblioteca padrão a serializa internamente por list2cmdline, cujas regras delimitam argumentos contendo espaço/tab com aspas. Não há shell string, split, aspas embutidas manualmente ou URL encoding no delta. No Linux, o caminho observado na fonte de subprocess converte a sequência para lista e a encaminha a fork_exec, com a transformação de shell restrita ao ramo shell=True.

Isso sustenta a preservação pretendida de cada token pelo código Python. Não demonstra por si só como wsl.exe, um consumidor distinto, recebeu e interpretou esses tokens. Nem prova abertura do arquivo de destino. Essa fronteira continua OPEN até uma eventual unidade específica observar argv recebido e recibos. O transporte anterior preservou espaços no erro, mas não foi reutilizado como ensaio da candidata.

## Alternativas e alcance da escolha

A alternativa A, escolhida no contrato, separa PurePosixPath para transporte e Path concreto para I/O. Ela torna explícito o tipo do destino e cobre supervisor, cleanup, filho e comparações de identidade por uma função comum. A alternativa B, aplicar as_posix ao Path concreto existente, seria menor para esse literal fixo, mas ainda interpretaria a entrada conforme a sintaxe do host antes de serializá-la. A preferência por A é justificada pela fronteira entre tipos; não autoriza normalização arbitrária ou alteração do controle.

## Fontes primárias locais lidas

- `C:\Python314\Lib\pathlib\__init__.py`: 125–133 (PurePath), 157–170 (junção e tipo), 251–267 (serialização), 325–328 (as_posix), 601–608 (PurePosixPath), 632–635 (Path).
- `C:\Python314\Lib\posixpath.py`: 72–92 (junção POSIX).
- `C:\Python314\Lib\subprocess.py`: 582–649 (list2cmdline e espaços), 1471–1476 (serialização de argumentos).
- `\\wsl.localhost\Ubuntu-24.04\usr\lib\python3.12\pathlib.py`: 348–350, 380–385, 430–435, 450–454, 719–723, 802–809 e 1166–1169 (mesma cadeia semântica no runtime Linux).
- `\\wsl.localhost\Ubuntu-24.04\usr\lib\python3.12\subprocess.py`: 1808–1818 e 1885–1893 (lista, ramo shell e fork_exec).

Os hashes e tamanhos dessas fontes constam do recibo independente. A leitura dos dois arquivos Linux por UNC exigiu escalonamento restrito após recusa do sandbox; nenhum wsl.exe ou Python Linux foi iniciado. Foram executados apenas scripts próprios de leitura, hashing, parsing AST e documentação. Zero importações/execuções da candidata, construtores de caminho-alvo avaliados, controles, hooks, WSL, dados D, PE ou chamadas remotas.

## Parecer

Aceite estático restrito da representação proposta, sem achado bloqueante adicional neste delta. O contrato mantém explícita a ausência de validação dinâmica e de autorização de consumo. A rotina de papéis segue seus chamadores fechados; não foi promovida a validador genérico de entradas. Limites, STOP/gate, pidfd, política de retry e ciência não foram redesenhados nem requalificados. Cabe à coordenação deliberar separadamente sobre eventual conferência pura isolada ou nova unidade de transporte. Nada neste parecer reabre 4f5d ou permite aplicar o delta a artefatos consumidos.

Pins relidos dos objetos principais:

- `MANIFESTO_PREPARACAO_CAMINHOS.json`: 3382 bytes; SHA-256 `607ceb483aae8ef3025ae2e586dace04d689f8d2d754aadadc5d85a4a06789ee`.
- `CONTRATO_INTERFACE_CAMINHOS.json`: 3801 bytes; SHA-256 `10b6c782f5f681bb798efb4f263b45eb564322a20db7cfd1019e3ef7a46711a9`.
- `common.py.candidate.txt`: 4742 bytes; SHA-256 `f0ddcbff558ccd0796889e4300a1c52c932a213e82569a9a3c678b193be05b91`.
- `RECIBO_REVISAO_CAMINHOS.json`: 17079 bytes; SHA-256 `d306753006aa975b830f696c352ba8a695632c66447c667d7541bfd9fb312612`.
