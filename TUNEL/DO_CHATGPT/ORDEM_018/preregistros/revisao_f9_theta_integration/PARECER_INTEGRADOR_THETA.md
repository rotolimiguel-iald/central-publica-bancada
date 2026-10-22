# Parecer independente — integrador externo θ da F9

[REAL — revisão exclusivamente estática] **Não identifiquei bloqueador material no pacote ad02511d-1536-4a1b-a6c4-fb3e5eb26550, no escopo declarado de callback/controlador confiáveis.** Pode seguir à decisão de ROOT sobre integração e futura qualificação numérica. Este parecer não autoriza execução, não abre observados e não certifica a precisão de uma integral.

Foi consultado o mapa até a entrega580 antes do exame. O manifesto recebido foi relido por bytes; a custódia de membros/fontes e a comparação dos literais de linhagem estão no recibo desta pasta. A fonte candidata permaneceu somente leitura. O quadro F1e579 foi usado como referência de escopo, não como uma exigência de campanha adicional.

## Prior, geometria e normalização

[DERIVED — confronto algébrico] O alvo é a média das cinco integrais condicionais já produzidas por df482 em θ fixo. A caixa [50,90]×[0,015;0,030]×[0,08;0,18] tem Jacobiano 40·(3/200)·(1/10)=3/50 na transformação afim do cubo unitário; a densidade física 50/3 cancela esse Jacobiano. Os limites originais estão em theta_integrator.py:17 e o transporte em137–141. Endpoints usam diretamente o limite original; os pontos interiores usam a transformação afim do nó diádico.

Não há novo fator50/3 no somatório, estreitamento do prior, ajuste de caixa ou integração duplicada dos extras. A verificação do callback em248–250 exige que df482 ainda não tenha aplicado/integrado o prior base. H3/H4/H5 permanecem integrados pelo módulo anterior, com seus Jacobianos próprios. Não se importou nem avaliou essa matemática.

O integrador não monta pseudoinversa, não altera X/C e não escreve outro backend. A integral nuisance, suporte e prefator vêm de df482/a987. Em258–270 verifica r entre63 e283, p=63, prefator finito e normalização exatamente comum entre os nós. O hash fixo da admissão do consumidor é conferido em272–276. A mesma medida euclidiana no suporte transformado e κdη permanecem; apenas logκ é omitido. Isso permite razões relativas na mesma admissão, não evidência absoluta.

Na frase inicial de DERIVACAO.md, “J_i … o log-callback” deve ser lido como integral positiva J_i cujo log é transportado. As fórmulas subsequentes e o código usam log J corretamente; é imprecisão de redação, não defeito da regra ou motivo de reexecução.

## Simpson positivo, log-somas e diagnósticos

[DERIVED — leitura de código] Para n=2^L, _integer_weight em144–145 implementa1 nos extremos,4 nos índices ímpares e2 nos pares interiores. O peso em329–338 é o produto dos três numeradores dividido por(3n)^3. Cada regra1D normaliza uma constante, e o produto conserva essa normalização e positividade. Não foram enumerados nós ou calculadas regras nesta revisão.

_level_result em340–378 primeiro encontra o maior termo log ponderado e depois soma exp(termo−máximo) com math.fsum. O máximo garante ao menos um termo escalado1 quando há massa amostrada positiva; o código não exponencia diretamente os logs absolutos. Nós no complemento do suporte são omitidos da soma apenas pelo −inf legitimamente rotulado. Termos arredondados para zero são contados; não são certificados de massa perdida.

Os mesmos nós/pesos servem aos cinco modelos. O retorno conserva os níveis completos, gaps de log, concentração do maior nó, fração de peso nas fronteiras e maiores valores amostrados. A fração de fronteira é contribuição na regra discreta, não probabilidade física de uma superfície de medida zero.

A diferença dos dois últimos níveis não recebe fator Richardson1/15 nem estatuto de erro certificado. indicator_satisfied é uma comparação heurística; global_convergence e unresolved_peak_mass_bound permanecem null. Um pico entre nós pode escapar mesmo com gaps pequenos. Essa limitação está dita na API e na saída; não acrescento certificado de picos como pré-requisito para ENGINEERING_ONLY.

A saída fornece cinco logJ relativos e diferenças contra H2, incluindo o zero de referência. Essa base permite obter as dez diferenças par a par na camada de relatório usando os mesmos valores; este módulo não se apresenta como a função completa de veredito F1e.

## Identidade dos nós, cache e limite antes do callback

_node_key em130–134 divide simultaneamente numeradores e denominador por2 enquanto possível. Assim, uma tripla diádica tem representação comum nos vários níveis. _theta recebe essa representação canônica, e _descriptor em200–208 associa unidade, admissão do consumidor, referência do callback, admissão da montagem e configuração global antes de calcular node_id.

Como todas as grades mais grossas pertencem à grade final, o número de callbacks únicos é N=(2^last_level+1)^3, não a soma dos tamanhos de cada nível. O construtor exige dois ou mais níveis inteiros consecutivos, teto explícito e required≤cap em168–176 **antes de qualquer callback**. run percorre todos os níveis do intervalo em384–388 sem parada antecipada por gap. Ao fim exige completed=required=attempts.

Em312–327, um nó já completo volta do cache; um nó tentado e incerto é recusado. A tentativa, o nó ativo e o incremento são registrados antes da chamada. Só depois de aceitar a coleção inteira de cinco modelos o cache recebe a tupla de logs. Portanto uma família parcial não é reutilizada. O cache matemático entre níveis não cria cinco chamadas de fundo por nó.

Os limites6/300000 são tetos de schema, não orçamento científico concedido. O módulo puro não promete limite de memória ou parede do SO. O futuro controlador deve impor esses limites, reservar duravelmente a unidade+nó antes de ciência e validar qualquer cache persistente. Essa divisão de responsabilidade é explícita e adequada ao escopo desta preparação.

## Configuração global e fundo novo versus durável

O plano exige hashes de admissão da montagem e configuração global; descritor e recibo repetem os mesmos hashes, conferidos em222–223. O esclarecimento da API83–91 corresponde às fontes: a987 vincula prediction_admission_sha256 à admissão do montador; o montador vincula engine_configuration_sha256 e runtime_sha256 ao pacote do fundo. prediction_worker seleciona point_id na lista p['points'] do protocolo. Logo a grade exige uma configuração global finita e uma admissão comum preparadas antes dos callbacks. A configuração pontual consumida por c435 não serve por simples reaproveitamento de seu hash.

A inspeção das fontes não executou runtime_check ou prediction_worker. O módulo θ não cria essa configuração, não lê arquivos para autenticar objetos, não concede execução e não substitui o controlador durável. Igualdade de referências não prova por si só a autenticidade de código/recibos: o contrato diz quem deve conferir o conteúdo real, a cobertura dos pontos e a cadeia de admissão.

Cada recibo deve conservar uma execução original de fundo bem-sucedida1/1. NEW_EXECUTION declara uma chamada nova; VERIFIED_DURABLE_CACHE declara zero chamadas novas, com conferência exata em226–234. O mesmo hash de pacote de fundo não pode ser associado a dois θ distintos em279–280. Um novo objeto de integração para cenário diferente pode reutilizar o mesmo fundo qualificado, se física/configuração/runtime/θ forem compatíveis; não pode reutilizar a likelihood de outra C/admissão.

As contagens de entrada/retorno ao wrapper de callback são observadas pelo módulo. As de solver são declaradas nos recibos e assim rotuladas em423–424. Não encontrei alegação indevida de instrumentação nativa.

## Falhas, schema e fronteira de confiança

O callback devolve exatamente conditional_result e receipt. O resultado deve ter o schema, request df482, θ solicitado, cinco modelos e todos os estatutos/proveniência esperados. O hash canônico usa um marcador explícito de −inf somente nos cinco campos de log-integral admitidos; outros não finitos são recusados. O limite4MiB é de aceitação da serialização construída, não retenção física de memória, conforme API45.

Os retornos finitos e zeros legítimos estão coerentes com o código produtor df482/a987. Falhas de engenharia não viram zero. Se um nível inteiro tem apenas zeros amostrados, ele permanece diagnóstico e os refinamentos fixados continuam. Se algum modelo ainda não tem massa positiva na grade final, há falha terminal sem razão0/0 nem evidência parcial. É prudência de representação, não prova de massa global nula.

run entra uma vez em RUNNING e termina COMPLETED ou FAILED_TERMINAL; captura também interrupções por BaseException e relança, preservando contagens e nó ativo quando aplicável. Não há retry, fallback ou nova escolha de nível. Uma nova instância não garante idempotência entre processos: isso cabe ao controlador, e a API o exige expressamente. Nenhum CLAIM foi criado pelo preparo ou por esta revisão.

A normalização, os pins e os diagnósticos são conferidos dentro da fronteira do callback confiável; não se trata de sandbox contra um callback malicioso ou que falsifique metadados. Também não é certificado de adequação do experimento MM, que continua CONDITIONAL_UNRATIFIED.

## Conclusão delimitada

O objeto revisado realiza a peça I04 do quadro F1e como candidato de engenharia e tem interfaces compatíveis com a987/df482. Ainda são necessárias a ligação concreta sob configuração global, serviços numéricos admitidos e qualificação das junções novas, nas unidades decididas por ROOT. Não se deve repetir c435, ffd6, NC02 ou os controles de cauda por causa deste aceite.

Não localizei achado material que exija reparar o módulo antes da decisão de ROOT. Isso não é garantia de ausência de bugs, autorização de execução ou prova de convergência. p, sigma, veredito e evidência absoluta permanecem null; nenhum dado observado, C observada, centro, solver, WSL, teste ou importação de candidato foi usado. Memórias, ledger, pacotes selados e autorizações ficaram intactos.
