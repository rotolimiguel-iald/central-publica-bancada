# Parecer independente pré-execução — NC02 racional

**Sem achado bloqueador no recorte estático examinado.** [REAL — leitura/bytes/AST; DERIVED — conferência algébrica] A implementação dos dois casos fixos corresponde ao payload final bf2a e ao contrato concreto de ROOT. O pacote pode ser submetido à decisão específica de execução única. Este parecer não concede essa autorização e não declara controles passados, cadeia dinâmica de imports qualificada ou certificado físico.

Foram lidos integralmente os seis módulos novos: builder, codec_adapter, verifier, worker_controls, supervisor e finalization. Os 536 pins de execução são únicos e coincidem com os bytes atuais; os 506 pins de runtime estão contidos neles. Os 14 membros do manifesto também coincidem. Não há AUTORIZACAO_ROOT.json, CLAIM.json, RUN, TERMINAL_RECEIPT.json ou FINALIZATION_FAILURE.json no instante registrado pelo recibo. Fontes próprias foram preservadas como snapshots textuais de bytes; nada foi alterado no pacote do autor.

## Contrato, identidade e separação do esperado

O payload `F9_NC02_RATIONAL_UNIT_PROPOSAL_V1`, de preparação bf2a5692-1aff-423e-9345-7bfa256d5072, fixa dois casos em ordem e o alvo exclusivamente sintético. A identidade de execução distinta c8909840-5b14-4bf5-bc2b-dfc71dbdbcaa está preparada, ainda sem consumo. O plano numérico maior e a interface física não foram tratados como execução autorizada de seus outros controles.

O builder confere esquema/identidade, geometria exata, caixa, casos, duais e testemunha (`builder.py:77–132`). Sua saída possui precisamente os campos esperados pelo verificador: `reason` está presente em ambos os caminhos, e `witness` contém `u`, `eta`, `residual`. O negativo emite o resíduo de anulamento e conserva coeficientes, lower, upper e witness como null. O envelope exterior vincula os hashes do payload/dependências à identidade; a ausência desses hashes dentro da função pura é a interface acordada na nota do builder, não uma lacuna de ligação no worker.

Em `worker_controls.py:137–141`, as respostas esperadas são copiadas para uso exclusivo pelo envelope, removidas de cada caso e a referência de prova é removida antes de qualquer chamada às implementações. Builder e verifier recebem cópias desligadas do estado do chamador; a verificação independente ocorre antes da comparação com o resultado esperado (`151–160`). Os valores fixados pelo builder são as entradas da fixture, não lower/upper de saída. O verificador não importa builder, adapter ou Fraction, mas compartilha explicitamente o parser canônico pinado — independência da aritmética de construção, não de todo o runtime ou da gramática.

## Conferência matemática por leitura, sem execução aritmética

Para este caso C=I2, X=(1,1), b(u)=(1,u), u em[0,1/2] e eta real:

q(u,eta)=(1−eta)^2+(u−eta)^2.

A identidade de quadrado não negativo dá q≥2vᵀb−vᵀv quando Xᵀv=0. Para v=(1/4,−1/4), o anulamento é exato e a expressão dual é 3/8−u/2. Por ser afim, o mínimo na célula fechada está em um extremo, dando o esperado simbólico L=1/8. Na testemunha u=1/2, eta=3/4, o resíduo é (1/4,−1/4) e sua norma quadrada dá o esperado U=1/8. Igualdade dos dois certificaria o mínimo desta fixture se a unidade qualificada produzir e verificar esses resultados; aqui são derivações documentais, não resultados de execução.

O builder deriva coeficientes, avalia extremos, combina com zero e calcula a testemunha (`154–194`). O verifier segue outra rota: recompõe b nos dois extremos, calcula a expressão dual diretamente, confere os coeficientes por suas avaliações, recompõe resíduo e norma e confere sua viabilidade (`verifier.py:125–153`). A testemunha factível fornece uma cota superior para o ínfimo; não se presume que seu eta já veio de um otimizador. O código só usa norma euclidiana porque exige C exatamente I2.

No negativo, 1/4−255/1024=1/1024. Com eta irrestrito, o termo nuisance remanescente não tem erro uniformemente limitado; recusar antes de formar bounds segue o contrato numérico §3.2. Não há cutoff numérico. A recusa precisa trazer motivo e bounds null; o verificador exige ambos (`116–123`). O caso não é recusa da teoria física nem estatística observada.

As entradas passam pelo codec canônico tail V2 de512bits; o adaptador valida tamanho, tipos exatos, denominador positivo, redução e retorno das mesmas strings. Os intermediários explícitos passam por guardas de4096bits antes de produto/soma, inclusive produtos cruzados de comparação. Fraction recebe pares inteiros já limitados; o ramo inteiro de sua fonte normaliza por gcd/divisão. As guardas são conservadoras e podem recusar cancelamentos que caberiam após redução. Isso não é arredondamento nem promessa de RAM rígida. O verifier usa pares de inteiros e gcd com guardas próprias. Não se executou Fraction ou qualquer caso nesta revisão.

## Caminhos, imports e reutilização read-only do codec

A cadeia lida é coerente com o lançamento Windows `-I -S -B -X utf8`:

- Supervisor insere explicitamente a pasta absoluta do pacote antes de importar `finalization` (`20–22`). Não depende de cwd ou user-site para encontrar esse módulo.
- Worker é um script absoluto passado em lista de argv para o mesmo executável Windows pinado (`supervisor.py:195–201`). A fonte `subprocess.py` local usa `list2cmdline` nessa plataforma e `CreateProcess`; o espaço em `Central de Patentes` permanece parte do argumento tratado pela biblioteca. Não existe token Linux ou WSL nesta unidade. O defeito anterior de `Path` Windows serializado para Linux não reaparece nesse transporte entre processos Windows.
- O worker pré-carrega stdlib, dataclasses e fractions antes do hook. Após conferir pins, cria o acesso à medição Windows e instala audit; o carregamento de candidatos usa bytes de caminho absoluto e `compile/exec`, com `__file__` e registro em `sys.modules` antes da avaliação. Isso evita sondagem de pyc para esses fontes.
- `tail_envelope.py` é carregado como `nc02_pinned_tail_codec`, com dependências stdlib já carregadas; seus dataclasses são definidos, mas nenhuma cauda/agregação/controle antigo é chamada. A única função recebida por builder/verifier é `_rational`. A constatação vale para a cadeia explícita e o AST lidos, não para uma execução presumida.
- Adapter é registrado como `codec_adapter` antes do builder, satisfazendo seu import mesmo sob `-I`. Fractions e math são imports stdlib já realizados. Os 506 pins incluem a closure anterior e inventário conservador; o worker ainda exige que todas as origens absolutas efetivamente carregadas pertençam à lista (`165–167`). Não se declara closure das DLLs do Windows.

Os três possíveis arquivos de configuração locais `python314._pth`, `python._pth` e `pyvenv.cfg` foram verificados como ausentes em C:/Python314 neste recorte. Isso não equivale a inventariar toda configuração do host. Foram lidas fontes primárias instaladas de pathlib/stdlib pertinentes ao raciocínio da cadeia; não foi importado módulo candidato para testar a conclusão. A verificação dinâmica de imports continua pertencendo à eventual unidade, não a uma etapa extra criada por este parecer.

## Encerramento e alcance dos limites

O preflight confere identidade, pins, executável, autorização específica ligada aos hashes e ausência de consumo (`supervisor.py:75–115`). CLAIM tem criação exclusiva antes do lançamento; falha/incerteza de escrita não relança. O tempo do preflight/CLAIM não entra no prazo nominal, conforme o protocolo que começa imediatamente antes do Popen. A duração desde esse ponto inclui bootstrap, coleta, recibo de identidade, persistência final e stdout.

O worker recebe deadline absoluto de8s contado pelo supervisor antes do lançamento. Há checkpoints antes/depois do carregamento e de cada etapa dos dois casos, depois da serialização e após flush de stdout. O supervisor limita a espera inicial a10s contados do mesmo início, pede kill pelo handle do filho em timeout e usa somente o saldo dos30s para coletar. Se falta tempo/prova de término, conserva PROCESS_STATE_UNCERTAIN. Não é prometido confinamento de duração pelo SO nem ausência universal de órfãos.

A lista de audit mantém a primeira recusa mesmo quando uma PermissionError for absorvida; o checkpoint seguinte falha. A lista é limitada a16 eventos, suficiente para latch e primeiro evento, não contador ilimitado. Escritas/novos processos/rede são recusados pelo hook após sua instalação; o leitor de memória Windows é preparado antes. Isso é proteção da cadeia auditada e não sandbox inviolável contra código arbitrário.

O finalizer é byte a byte o da versão tail V2 pinada. Persiste somente recibo provisório, relê seu hash, confere relógio, emite/flush e confere novamente o relógio (`finalization.py:65–92`). Falha tardia tenta recibo de invalidação e retorna nãozero. Não há persistência adicional no caminho de retorno0 depois da última observação. O aceite exige observar externamente o exit0, o recibo provisório correto com controls_status PASS e ausência de FINALIZATION_FAILURE. Stdout PASS ou recibo isolado não bastam; retorno0 do filho também não substitui o do supervisor.

O contrato concreto explicita corretamente: caps de stdout128KiB/stderr8KiB são aceitação pós-coleta, não buffers limitados durante communicate. A medição PeakWorkingSetSize≤256MiB é observada antes de serializar o report; não é enforcement de RSS pelo SO nem limite certificado de toda a vida do processo. O supervisor confere esse valor observado. Não foi inventado requisito de hardRSS, e esta revisão não mediu memória, desempenho ou prazo.

## Parecer e limites finais

Aceite **somente da preparação estática examinada**, sem correção requerida neste recorte. ROOT pode tomar sua decisão específica sobre os dois casos já delimitados; este parecer não solicita uma campanha adicional nem cria autorização, CLAIM, request ou comando de consumo.

Permanece [OPEN] a execução real, o resultado dos dois casos, a closure observada e o encerramento pelos recibos. Mesmo eventual PASS seria qualificação local da pequena fixture racional e do transporte observado, não do backend completo, suporte singular geral, oráculo cosmológico, mínimo F9, integral/evidência, dado D, significância ou confirmação física. INIT003 e WSL4f5d permanecem terminais, sem replay. Memórias compartilhadas não foram alteradas; o mapa recebe apenas esta revisão documental.
