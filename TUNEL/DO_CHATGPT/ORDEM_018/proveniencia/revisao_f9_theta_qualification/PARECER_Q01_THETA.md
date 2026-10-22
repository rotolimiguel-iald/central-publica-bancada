# Parecer independente — Q01_THETA_COLLECTION

Revisão de 06/10/2026, autor chatgpt-codex/ordem-018/proveniencia. Unidade examinada: 4e9a80ad-dac3-4c6c-8ec5-b7927a9c056d. Mapa anterior: 620.

## Conclusão e achados

[DERIVED — revisão estática] Não identifiquei bloqueador material no pacote pinado para a futura qualificação sintética delimitada. O preparo é coerente com os quinze casos, suas referências analíticas e recusas, a identidade ad025 do integrador e a decisão de execução única prevista. Esta revisão não autoriza nem executa a unidade; seu estatuto é ACEITE_ESTATICO_LIMITADO, não PASS de controles.

[REAL — bytes/AST] Manifesto inicial e final, oito membros, um backup, quinze fontes e executável Python foram conferidos por leitura de bytes e SHA-256. O recibo desta revisão contém cada caminho absoluto, tamanho, hash e resultado. Não houve importação do candidato, de cases ou driver, nem execução de referências numéricas/controles, fonte científica, solver, WSL ou provedor. Não foram criados ROOT_DECISION, AUTH, CLAIM ou artefatos de consumo. A ausência desses caminhos é observação datada, não promessa sobre eventos posteriores.

Não são bloqueadores deste recorte, mas limitam o que se poderá afirmar:

1. O driver confere o formato de review_reference; a leitura do parecer, a identidade e seu hash são responsabilidade de ROOT antes da decisão. Isso é fronteira explícita do chamador, não prova de revisão produzida pelo driver.
2. Receipts de fundo/cache são fixtures sintéticas. VERIFIED_DURABLE_CACHE e hashes de fundo distintos não demonstram execução CAMB, cache POSIX, fsync, hardlink, guard real ou igualdade tardia de I02. O contrato preserva como preflight futuro joint._admission['prediction_admission_sha256'] == plan['assembly_admission_sha256'] antes de qualquer fundo.
3. A decisão é somente para Q01_THETA_COLLECTION. O Q01 escalar PASS9 já consumido é referência histórica; não é repetido. Q02/Q03 físicos, I02, covariância/centros e evidências observacionais continuam fora do escopo.
4. Tolerâncias float são critérios de engenharia, sem arredondamento dirigido ou prova uniforme. T06 demonstra por construção que concordância entre níveis pode coexistir com massa não amostrada. Não se promove convergência estimada a certificado.

## Referências analíticas e alcance dos casos

[DERIVED — álgebra documental] A caixa em H0, omega_b, omega_c tem volume 40 × (3/200) × (1/10) = 3/50; sua densidade uniforme é 50/3. O Jacobiano e a densidade se cancelam na integração no cubo unitário. As escalas sintéticas são 1, 2, 3, 1/2 e 5; não são dados físicos.

| Caso | Referência e caminho revisado | Chamadas / aceitas |
|---|---|---:|
| T01 | Funções constantes; integral igual à escala; normalização da caixa/prior, flags e contadores de precisão preservados. Reentrada posterior é recusada sem callback. | 125 / 125 |
| T02 | (1+u³)(1+v²)(1+w), integral (5/4)(4/3)(3/2)=5/2, multiplicada pela escala. Simpson tensorial é exato em aritmética real para esses graus por eixo. | 125 / 125 |
| T03/T04 | Mesmo tensor com deslocamento comum +1000/−1000 no log. Log Z recebe esse deslocamento; razões o cancelam. Referência não exige exp(±1000). | 125 / 125 cada |
| T05 | H5 tem −∞ com estatuto legítimo de suporte zero. O integrador completa os níveis e só ao final recusa NO_POSITIVE_SAMPLED_MASS; não confunde zero legítimo com falha de engenharia. | 125 / 125 |
| T06 | Em H1: 1+32 max(0,1−abs(u−1/8)/(1/32)). Triângulo tem base 1/16, altura 32, área 1; integral total 2. Todos os nós u=0,1/4,1/2,3/4,1 estão fora do suporte [3/32,5/32], dando amostragem 1. H2 constante 2: razão verdadeira 1 versus razão amostrada 1/2. | 125 / 125 |

Os dois níveis usam grades 3³ e 5³. A grade grossa é subconjunto da fina por identidade racional reduzida; são 125 callbacks únicos, não 152. A conferência de coordenadas exige o produto cartesiano completo. O resultado comparado é log Z = offset + log(multiplier × scale), e a razão perante H2 é log(scale/2), exceto o contraste verdadeiro do pico explicitamente separado. T05 não produz resultado familiar aceito. Qualquer eventual PASS significa que o comportamento previsto foi observado nesse exemplo, não que a integral física foi certificada.

A referência de T06 é adversarial à interpretação excessiva e não um modelo de erro físico. As tolerâncias 1e−11 e 3e−10 são declaradas e verificadas como condições de teste, sem afirmação de prova intervalar.

## Nove recusas alcançáveis

[DERIVED — leitura de fluxo] Revisei os pontos em cases.py:73–157, run_case:43–246 e theta_integrator.py:150–445. As mutações não são todas interceptadas antes da condição que desejam exercitar: seguem as interfaces e chegam às verificações relevantes do integrador.

| Caso | Mutação e recusa alcançada | Tentadas / aceitas |
|---|---|---:|
| N01 | Orçamento 124 para 125 nós; BUDGET_ERROR no construtor, antes do callback. | 0 / 0 |
| N02 | O mesmo objeto Sentinel é lançado na terceira tentativa. É propagado, não convertido em densidade zero; reentrada após falha retorna REPLAY_ERROR sem nova chamada. | 3 / 2 |
| N03 | Normalização de nuisance muda no nó 2; MEASURE_CHANGED. | 2 / 1 |
| N04 | Hash do resultado condicional é deliberadamente substituído no nó 2; PIN_ERROR. | 2 / 1 |
| N05 | −∞ com ENGINEERING_ESTIMATE em vez de estatuto de suporte zero; DENSITY_ERROR. | 1 / 0 |
| N06 | H5 é removida no nó 2; SCHEMA_ERROR ao conferir conjunto de modelos. | 2 / 1 |
| N07 | Mesmo hash de fundo em dois θ distintos; BACKGROUND_ERROR. | 2 / 1 |
| N08 | Prior base de θ marcado como já aplicado; PRIOR_ERROR. | 1 / 0 |
| N09 | H0 do resultado difere do descritor pedido no nó 2; IDENTITY_ERROR. | 2 / 1 |

A soma contratual é 6×125+(0+3+2+2+1+2+2+1+2)=765. Há quinze tentativas de construção; N01 não chega ao run. As catorze entradas primárias em run, mais duas reentradas intencionais T01/N02, somam dezesseis. O contador externo de callbacks é incrementado e limitado antes de produzir a fixture; os contadores de construção/run são do harness confiável, não um profiler independente de toda chamada Python. Os limites descrevem esta fonte pinada e seu único percurso autorizado, sem promessa de contenção de código hostil arbitrário.

## Independência e proveniência do código carregado

As fórmulas fechadas acima são referências distintas da soma numérica do integrador. O harness calcula independentemente o hash dos descritores de nó e confere coordenadas, grade, unicidade e contadores. O hash canônico do resultado condicional usa deliberadamente o encoder público do candidato; portanto esse trecho testa a ligação/interface, não oferece uma segunda implementação independente desse encoder. N04 ainda testa a recusa a um hash errado. Não foi encontrado argumento de independência estatística ou física baseado apenas nessa concordância.

driver.py:90–159 fixa raiz, identidade, flags -I -S -B, interpretador e pins; load_bytes compila exatamente os bytes pinados, executa-os em módulo novo e relê a fonte. driver.py:162–244 registra hash do código compilado e dos métodos run, _accept, _evaluate e _level_result, com globals/filename correspondentes ao módulo carregado. Isso liga a execução futura à fonte lida; nesta revisão apenas a implementação desse mecanismo foi examinada. Fontes de prior/assembler são pins de contrato: não são executadas pelas fixtures. A biblioteca padrão e DLLs não têm fechamento integral pinado, limitação expressa no contrato.

Os pins não contêm dependência circular impossível: CONTROL_CONTRACT fixa hashes de cases e driver; o driver lê o contrato, sem precisar conter seu hash. O manifesto fixa o contrato e o restante do pacote. A decisão externa futura liga o manifesto. Hashes sintéticos da fixture são rotulados como tal e não apresentados como hashes de artefatos científicos executados.

## Consumo, prazo e aceite final

driver.py:247–327 cria RUN_CLAIM com O_EXCL antes de Popen e de qualquer carregamento do candidato; o worker exige esse claim, nonce e parent PID e grava WORKER_STARTED antes do consumo. execution_once/claim existente recusa novo lançamento. Não há retry, fallback ou segunda criança no código pinado. Há exatamente um processo filho conhecido, sem launcher WSL ou subprocesso científico.

O limite nominal é 30s contado da entrada em main, incluindo validação e persistência posteriores, sem incluir o arranque do interpretador antes de main. O prazo cooperativo é 23s, a espera pelo filho vai até 25s e a limpeza usa reserva limitada a 4s/tempo restante. Python, filesystem, kill, fsync e I/O podem exceder o tempo nominal; não há garantia absoluta de tempo real, quota de disco/RAM de SO nem de término de processo hostil. A limpeza opera no objeto Popen próprio e eventual fracasso permanece terminal. O limite de streams de 65536 bytes é conferido após coleta, não quota imposta durante a escrita.

Worker exige todos os quinze casos, 15 construções e 16 run, e verifica prazo após cada persistência. Supervisor exige exit0 do filho, ausência de WORKER_FAILURE, conjunto completo, total exato 765 e recibo final com hash. Depois da escrita final, há observações de prazo após I/O, releitura e flush de stdout. Ainda assim um RESULT/TERMINAL_RECEIPT ou linha PASS isolado pode anteceder falha tardia: o consumidor externo deve exigir o exit0 do supervisor e ausência de falha, conforme contrato. Exceção após prazo não reabre a unidade; resultado incerto também não permite repetição.

## Alternativas consideradas e decisão de revisão

A) Rever e, se ROOT decidir, qualificar esta coleção finita usando referências analíticas e os bytes pinados: opção coerente com a pergunta Q01 de engenharia e com a novidade desta coleta θ.

B) Integrar já o joint/assembler, guard real e store POSIX ou repetir a qualificação escalar: não é requisito para este recorte e confundiria capacidades distintas. As obrigações I02/FS/Q02 devem ser avaliadas nos respectivos contratos, sem extrapolar um eventual PASS local.

Resultado: aceite estático limitado da preparação, zero execução nesta revisão. Não há correção material solicitada no pacote congelado. A decisão específica de eventual consumo permanece com ROOT; não se criou nova barreira de permissão nem se concedeu autorização.
