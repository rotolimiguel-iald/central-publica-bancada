# F9 — dependências concretas até um V1 ratificável

[REAL — confronto documental; nenhuma nova execução científica] O caminho restante não começa do zero: c435 verificou uma predição teórica e a montagem H1–H5 em um ponto; as revisões563/573 aceitaram estaticamente o consumidor e os priors extras. Faltam a ligação executável completa, a montagem integral dos cenários/C e os produtores de integrais/perfis/saída, seguidos de qualificação limitada ao que mudou e das decisões científicas explícitas. Serviços f820, integral θ ad025 e redutor bf6d já estão atribuídos: não duplicá-los.

Este quadro não modifica o resolutor nem declara F1 concluída. O retrato do mapa termina na seq577; novas entregas posteriores substituem o estado “em preparação” somente com seus próprios recibos. Os pins completos lidos nesta unidade estão em FONTES_E_PINS.json; as fontes são identificadas por IDs abaixo.

## O que já reduz as lacunas do rascunho

| Peça | Evidência consultada | Alcance que permanece |
|---|---|---|
| Montagem teórica H1–H5 | c435, seq572: uma chamada de engenharia verificada, 283 linhas/63 nuisance/sete escalas | Um θ; nenhuma likelihood observada, ajuste, integral em θ ou precisão uniforme |
| Consumidor da likelihood comum | a987, revisão563 sem bloqueador estático | Ty/TCTt, offsets, suporte/normalização e κ relativos implementados; cadeia concreta ainda não qualificada numericamente por esse parecer |
| Integração dos extras | df482, revisão573 sem bloqueador estático | H3/H4/H5 em θ fixo; serviços de precisão injetados, θ não integrado |
| Cota gaussiana e função tail | C01–C08/seq490 e tail8+9/seq524 consumidos uma vez | Prova condicional e controles delimitados; não são certificados físicos do composto |
| Megamasers | contrato511/revisão513 | Modelo simbólico concreto, não ratificado; referências e variâncias numéricas seguem fechadas |
| Interface de mínimos/integrais | contrato520/revisão525 | Separa engenharia/certificados; o ensaio NC02 posterior falhou terminalmente, sem resultado aritmético aceito |
| Próximos módulos | f820/seq574, ad025/seq576, bf6d/seq577 | Preparações em curso, não novas evidências de execução |

As cláusulas históricas C02/C03/C07/C10/C11 do resolutor não devem ser lidas como se nada dessas peças existisse. Esta comparação é uma atualização **ao lado**, sem alterar o rascunho selado. Três detalhes precisam acompanhar a próxima consolidação: (a) “oito controles futuros” é estado histórico; (b) a API tail vigente recusa d=0 com limite positivo como INVALID/null, embora a cauda abstrata χ²₀ seja outra identidade; (c) q=rd/rd_CAMB no documento e q=1/rd em df482 são coordenadas alternativas do mesmo prior H5, com seus Jacobianos respectivos, não rivais diferentes.

## Caminho mais curto

1. Receber/revisar f820; ligar a987+df482 ao produtor teórico existente, sem novo solver gaussiano e sem tratar o request c435 consumido como autorização para novas avaliações.
2. Concluir o builder puro da C/família e as preparações já abertas de θ/redutor. O perfil dos extras pode usar a mesma geometria afim; H4 usa B/A no mínimo da likelihood e B−λ somente no integrando com prior.
3. Qualificar apenas as junções novas e seus limites de engenharia. Não repetir C01–C08, tail17, o ponto c435 ou NC02 por rotina. Esta nota não manda executar nenhum caso nem todas as listas históricas de controles.
4. Entregar V1 único com escolhas, recursos/tolerâncias, fontes/código/runtime, função e estados de saída fixados. Referências protegidas necessárias à instanciação da C ficam para o estágio autorizado; sua receita e sua falha por ausência ficam fixadas antes.
5. Ratificação e abertura para veredito são decisões distintas do operador, conforme §6 da ORDEM018. Nenhuma medição favorável, poder alto ou certificado uniforme de toda a teoria é condição artificial para preparar o instrumento.

## Quadro por natureza da dependência

### 1. Código implementável com as interfaces atuais

| ID | Dependência concreta | Responsável/estado |
|---|---|---|
| I01 | Serviços escalares de precisão dos extras | Gerente — f820203f-b83c-420a-87ec-7816f3179139; não duplicar |
| I02 | Ligação motor → montador → consumidor → priors | ROOT — integração já atribuída |
| I03 | Montagem da covariância conjunta e da lista completa de cenários | ROOT — integração; proposta documental desta unidade, não novo despacho |
| I04 | Integral externa no prior θ inteiro | Derivações — ad02511d-1536-4a1b-a6c4-fb3e5eb26550, em preparação na seq576 |
| I05 | Perfil dos extras e interface de mínimos em θ | ROOT — dependência delimitada identificada; não executada aqui |
| I06 | Função única de saída e veredito V2 | ROOT — bf6d6747-6383-40a0-9aa4-7c02e76cadd6, seq577 |

#### I01 — Serviços escalares de precisão dos extras

**Já disponível:** H3/H4/H5 foram derivados e implementados em df482; revisão573 sem bloqueador estático. Falta o corpo concreto dos dois serviços injetados.

**Objeto mínimo faltante:** log_exp_quad_interval e positive_quad_1d com IDs/pins, contagem, limites, erro estimado/UNASSESSED e convergência; integração pela API já fixada.

**Alternativa A:** Janela analítica por log-CDF/erfc estáveis e quadratura positiva qualificada para H5.

**Alternativa B:** Quadratura adaptativa positiva escalada com localização do pico, compartilhável entre os serviços; riscos de pico perdido explícitos.

**Encaminhamento proposto:** Consumir a entrega f820 após revisão. Não trocar método por fallback após falha.

**Critério de fechamento:** Módulo concreto compatível com df482 e recibo de revisão; a qualificação numérica entra em Q01.

**Fronteira:** Preparação técnica não depende de novo certificado uniforme ou da leitura de y.

Fontes: precision_request, prior_review, prior_api; cláusulas C03, C11.

#### I02 — Ligação motor → montador → consumidor → priors

**Já disponível:** c435 executou uma predição teórica/montagem de cinco modelos em um θ; a987 e df482 só receberam revisão estática no recorte consultado.

**Objeto mínimo faltante:** Callback por θ que autentica os módulos realmente carregados, verifica pacote/estrutura/admissão, recebe explicitamente y/C/IDs, reutiliza PreparedJoint e devolve cinco integrais condicionais completas com proveniência e erros.

**Alternativa A:** Ligar as APIs pinadas existentes com admissão explícita e backend gaussiano comum.

**Alternativa B:** Escrever um segundo solver ou consumidores por modelo; duplicaria suporte/normalização e não é necessário.

**Encaminhamento proposto:** Reutilizar integralmente a987/df482 e a configuração verificada por c435. c435 é evidência e identidade consumida, não autorização de nova chamada; futuras avaliações pertencem à unidade própria.

**Critério de fechamento:** Uma cadeia revisável sem leitura implícita, sem reaplicar offsets/T, sem tratar exceção como zero, sem rival omitido; recibos preservam ENGINEERING_ONLY.

**Fronteira:** Pode ser preparada com entradas sintéticas/bytes explícitos; admissão e flags não liberam observados.

Fontes: c435, consumer_review, prior_review, consumer_api, prior_api; cláusulas C02, C03, C04, C07, C08, C11.

#### I03 — Montagem da covariância conjunta e da lista completa de cenários

**Já disponível:** Existem contratos de erros, família estelar e preflight262; isso não é um recibo de 600 matrizes conjuntas de 283 linhas incluindo os cinco MM.

**Objeto mínimo faltante:** Builder puro com entradas explícitas para blocos/cross-blocos/variâncias MM e receitas SBF; saída C_s, IDs e mapa completo rótulo→matriz/resposta/suporte/normalização. Sem preencher MM null, zeros cruzados ou referências por inferência.

**Alternativa A:** Compor blocos admitidos e cross-blocos explícitos segundo a lista finita já proposta, preservando todos os rótulos.

**Alternativa B:** Gerar C por componentes primitivas e Jacobianos assinados; exige entradas e modelo de dependência próprios se ainda não admitidos.

**Encaminhamento proposto:** Primeiro builder da alternativa finita existente, parametrizado pela decisão O01/O02. Duplicatas só podem ser comprimidas por equivalência integral e mapa de todos os rótulos.

**Critério de fechamento:** Receita/identidade executáveis antes de abrir dados; avaliação da C com referências protegidas somente em Q03 após autorização.

**Fronteira:** Não é necessário ler os centros MM para implementar o builder e seus estados de referência ausente.

Fontes: resolver, stellar_protocol, mm_contract, consumer_review, numerical_interface; cláusulas C01, C05, C06, C08.

#### I04 — Integral externa no prior θ inteiro

**Já disponível:** df482 integra apenas o extra de H3/H4/H5 em θ fixo; H1/H2 permanecem pontuais. Ainda não são cinco evidências físicas integradas.

**Objeto mínimo faltante:** Integrador externo sobre a caixa original H0/ombh2/omch2, callback da coleção inteira, pesos normalizados e cinco logJ relativos/10 diferenças por cenário. Preservar κ comum e erros separados.

**Alternativa A:** Cubatura adaptativa logescalada da caixa completa, com dependência adaptativa qualificada e riscos de picos não detectados.

**Alternativa B:** Produtos Simpson diádicos positivos em todos os níveis previamente fixados, cache de nós canônicos e log-somas; crescimento cúbico e erro entre níveis apenas diagnóstico.

**Encaminhamento proposto:** A preparação576 escolheu a segunda. Consumir a entrega/revisão sem duplicá-la e sem transformar diferença entre níveis em certificado.

**Critério de fechamento:** Código/pins e revisão; futuro orçamento explícito suficiente para todos os níveis pedidos, sem estreitar prior ou parar por conveniência.

**Fronteira:** Ausência de erro uniforme limita o estatuto, não impede implementar estimativa ENGINEERING_ONLY.

Fontes: theta_identity, theta_alternatives, prior_review, numerical_interface; cláusulas C03, C07, C11.

#### I05 — Perfil dos extras e interface de mínimos em θ

**Já disponível:** A álgebra condicional do mesmo residual está documentada; não consta nestas fontes um produtor aplicado de mínimos globais dos cinco modelos.

**Objeto mínimo faltante:** Reutilizar R e q do backend. Ao longo do extra afim, usar clip(B/A) no intervalo para A>0 e ramo plano quando direção projetada zero; fornecer estimativas em θ e campos distintos para L/U certificados quando disponíveis. H4 nunca usa B−λ para minimizar likelihood.

**Alternativa A:** Eliminar o extra afim pelo mínimo restrito e procurar θ na caixa original, reutilizando a geometria.

**Alternativa B:** Pesquisar diretamente as três/quatro coordenadas físicas no mesmo domínio e mesma likelihood, com custo maior.

**Encaminhamento proposto:** Redução afim evita buscas desnecessárias. Busca local fornece candidato factível/estimativa, não L global nem U certificado sem controle do erro de avaliação. L=0 pode ser cota analítica válida quando q≥0 e hipóteses completas estão admitidas.

**Critério de fechamento:** API de perfil/estimativa e interface de certificados separadas; não reivindicar otimização global ou cauda calibrada a partir de convergência local.

**Fronteira:** Certificado rigoroso mais apertado é necessário para a afirmação que o usa, não para a preparação de engenharia.

Fontes: prior_derivation, prior_review, numerical_interface, calibration, resolver; cláusulas C09, C10.

#### I06 — Função única de saída e veredito V2

**Já disponível:** Predicados V2 e cauda/agregação racional existem; o redutor de relatório está sendo preparado em unidade própria.

**Objeto mínimo faltante:** Saída por teste/cenário com completude, falha, p superior, direção, evidência relativa e poder separados. Rejeição válida de G ou Q sobrevive à indisponibilidade do outro; não-rejeição H1 exige ambos completos. Cinco modelos, cinco testes e dez razões sem omissão.

**Alternativa A:** Um redutor central estrito que recebe registros já validados e preserva estados de cada teste.

**Alternativa B:** Código de relatório independente por teste; duplica regras e aumenta risco de confundir falta com não-rejeição.

**Encaminhamento proposto:** Consumir o redutor central577; verificador semântico dos certificados permanece do chamador, não nasce de flags.

**Critério de fechamento:** Código/API/revisão e futura conferência lógica delimitada; V2 preservado e nenhuma aplicação observada aqui.

**Fronteira:** Uma implementação de predicados não autoriza leitura de dados nem cria calibração.

Fontes: reducer_request, verdict_v2, verdict_review, tail_receipt; cláusulas C09, C11, C13.

### 2. Qualificação numérica ainda necessária, sem repetição

| ID | Dependência concreta | Responsável/estado |
|---|---|---|
| Q01 | Qualificar as junções novas, não repetir unidades consumidas | ROOT após serviços e módulos estáveis |
| Q02 | Precisão e custo sobre o domínio físico declarado | ROOT/gerente nas unidades concretas de integração |
| Q03 | Aplicação geométrica e dos certificados à família real | ROOT após V1/abertura autorizada para referências protegidas |

#### Q01 — Qualificar as junções novas, não repetir unidades consumidas

**Já disponível:** 563/573 são estáticos; C01–C08 e tail17 passaram em unidades próprias. NC02 falhou terminalmente antes de resultado aritmético aceito.

**Objeto mínimo faltante:** Evidência numérica limitada das junções novas: transporte y/C e offsets, prefator/κ, H3/H4 truncados, H5 Jacobiano, plano/subidentificação, caudas/cancelamento, falhas propagadas e coleção completa. Delimitar casos/custo antes de qualquer execução futura.

**Alternativa A:** Confrontos sintéticos discriminantes com identidades analíticas/integrais de referência, focados nas interfaces novas.

**Alternativa B:** Confronto com método numérico independente nas coordenadas originais, com precisão/custo e domínio explícitos.

**Encaminhamento proposto:** Escolher o menor recorte que esclareça as junções após revisão; reutilizar recibos antigos como evidência de seus módulos. Não exigir novamente todas as listas históricas nem reabrir NC02.

**Critério de fechamento:** Recibo identifica o que foi realmente exercitado e suas tolerâncias; não promove a execução pontual c435 nem testes sintéticos a dados F9.

**Fronteira:** Esta nota não cria campanha, autorização, CLAIM ou ordem de medir.

Fontes: consumer_review, prior_review, calibration_receipt, tail_receipt, nc02_failure; cláusulas C03, C04, C08, C11.

#### Q02 — Precisão e custo sobre o domínio físico declarado

**Já disponível:** Há cinco pontos em dois níveis de precisão do fundo e uma chamada teórica c435. Não há, nestas evidências, qualificação de erro uniforme em todo prior nem integral externa medida.

**Objeto mínimo faltante:** Orçamento nominal de avaliações/memória/parede, política de nós e cache, diagnósticos de estabilidade e concentração e erros locais declarados; preservar toda massa do prior. Evidência ENGINEERING_ONLY deve marcar erro de teoria/global não limitado.

**Alternativa A:** Motor direto na caixa completa com regra de integração e diagnósticos previamente fixados.

**Alternativa B:** Tabela ampliada cobrindo a caixa inteira e interpolação validada no alcance alegado; nunca zero fora de tabela ou renormalização silenciosa.

**Encaminhamento proposto:** Prosseguir engenharia direta já integrada; avaliar eficiência sem prometer que custo de um ponto representa toda a caixa. Certificação uniforme mais forte é extensão separada se a afirmação final a exigir.

**Critério de fechamento:** Resultado numérico honesto pode ser ENGINEERING_ONLY; divergência/falha/erro não avaliado ficam visíveis, nunca viram likelihood zero.

**Fronteira:** Não condicionar a implementação ou estimativa de engenharia à existência prévia de oráculo CAMB intervalar.

Fontes: background_receipt, c435, theta_alternatives, precision_request, numerical_interface; cláusulas C07, C11.

#### Q03 — Aplicação geométrica e dos certificados à família real

**Já disponível:** Postos estruturais e suporte genérico têm evidência delimitada. Dimensões148/17/18 continuam limites condicionais; cinco MM não podem ser excluídos para reutilizar o preflight262 como composto.

**Objeto mínimo faltante:** Verificar por cenário C comum, origem afim, X suportado de posto63, 72 vínculos quando148 for usado, span global quando17/18 for usado, cobertura completa e erro dos limites L/U/SF. Validar referências MM e C somente no estágio admitido.

**Alternativa A:** Fatorização/identidades e certificados por componentes, com prova de transporte ao C conjunto e à família inteira.

**Alternativa B:** Validação numérica do C e do quociente admitidos com diagnóstico ENGINEERING_ONLY; limites certificados ficam indisponíveis onde não justificados.

**Encaminhamento proposto:** Fixar receita/guardas no V1 e executar a validação dependente dos dados depois da abertura; não pedir os próprios centros para congelar o protocolo. L=0/p=1 só são cotas triviais válidas após todas as hipóteses; falta de modelo ou cobertura é unavailable, não p=1.

**Critério de fechamento:** Para afirmar cauda conservadora, vincular identidade/família/modelo/suporte/L e grau ao verificador semântico. Para engenharia, conservar estimativas e limitações sem alegar certificado.

**Fronteira:** Nem esta nota nem a implementação tail fabricam certificado físico. d=0 com limite positivo é INVALID/null.

Fontes: consumer_review, mm_contract, calibration, numerical_interface, tail_receipt; cláusulas C05, C06, C08, C10.

### 3. Escolhas científicas e abertura reservadas ao operador

| ID | Dependência concreta | Responsável/estado |
|---|---|---|
| O01 | Experimento e propagação dos cinco megamasers | Operador ratifica proposta preparada/revista; ROOT apresenta pacote concreto |
| O02 | Família de sensibilidades, fatoração e convenções do composto | Operador no V1; ROOT consolida escolhas existentes |
| O03 | Mapas, priors e medida nuisance comum | Operador ratifica o conjunto proposto; ROOT mantém interfaces |
| O04 | Alcance da decisão científica e abertura por V1 | Operador; preparação/revisão executiva com ROOT |

#### O01 — Experimento e propagação dos cinco megamasers

**Já disponível:** Contrato MM511 e revisão513 distinguem receita upstream e lei amostral; referencias D_ref/v_ref e cinco variâncias seguem null no preparo.

**Objeto mínimo faltante:** Ratificar interpretação, receita de erros, referências fixas e proveniência/endogeneidade, dependências e alcance do experimento; preservar todos os cinco MM.

**Alternativa A:** Gaussiana de trabalho estipulada, C fixa nas referências futuras: simetrização upstream, derivada de erro upstream, bloco MM positivo diagonal e cross-bloco zero como INPUT explícito.

**Alternativa B:** Lei primitiva conjunta de D/v com seleção, assimetria/dependências e transporte/normalização próprios; não herda automaticamente a cota gaussiana fixa.

**Encaminhamento proposto:** A é a proposta atual, concreta e mais curta; sua adequação física não se prova por congelar números. B exige modelo adicional e não deve ser inserida silenciosamente.

**Critério de fechamento:** Decisão vinculada ao contrato por hash; receita antes de abertura, referências numéricas somente quando autorizadas.

**Fronteira:** O parecer independente não ratifica o experimento nem abre dados.

Fontes: mm_contract, mm_review, resolver; cláusulas C06, C10.

#### O02 — Família de sensibilidades, fatoração e convenções do composto

**Já disponível:** Proposta preserva Planck3+BAO13+267 locais, família estelar finita e duas receitas SBF. Não há independência empírica universal demonstrada por blocos ausentes.

**Objeto mínimo faltante:** Fixar lista/ordem completa, interpretação das duas receitas SBF, dependências/cross-blocos, fatoração de compressões, convenções q0/j0/velocidades e ausência de dupla contagem; alcance robusto restrito à família admitida.

**Alternativa A:** Adotar a família finita já proposta (300 rótulos estelares ×2 SBF), com limites de cobertura declarados e zeros cruzados somente se estipulados.

**Alternativa B:** Modelo de componentes/correlações apoiado em fontes adicionais já admitidas, com lista e cobertura revistas antes de qualquer composto; não presumir independência total.

**Encaminhamento proposto:** Apresentar A como V1 concreto sem vendê-la como todos os sistemáticos possíveis; B é alternativa de modelagem, não exigência automática.

**Critério de fechamento:** Família e semântica fixadas por hash; deduplicação não elimina rótulos e compara C/resposta/normalização completos.

**Fronteira:** Nenhum cenário é escolhido pelos resíduos, nenhum MM é removido.

Fontes: resolver, root_recommendation, stellar_protocol, mm_contract; cláusulas C01, C05, C08.

#### O03 — Mapas, priors e medida nuisance comum

**Já disponível:** H1–H5 e priors foram explicitados/revistos; H3 contém H1/H2, H4 atua via c_C, H5 é BAO-only. κdη permite somente razões relativas finitas.

**Objeto mínimo faltante:** Ratificar mapas R-A por indicador, fundo comum e domínio físico original, priors extras/transportes e medida comum. Não criar63 larguras arbitrárias para resolver implementação.

**Alternativa A:** Mesma medida plana κdη em R63 e priors físicos próprios originais; relatar apenas integrais relativas finitas.

**Alternativa B:** Priori nuisance própria comum somente com larguras/formas justificadas por fontes e decisão científica anterior ao composto; exige revisão de contrato.

**Encaminhamento proposto:** A já tem backend/consumidor preparados e mantém o caminho curto. Não alterar modelos/limites sem decisão; q=1/rd no implementado H5 e q=rd/rdCAMB no documento são coordenadas diferentes do mesmo prior, com Jacobianos respectivos.

**Critério de fechamento:** V1 explicita unidades, suporte/normalização, identidade da medida e domínios; um token de admissão não substitui essa decisão.

**Fronteira:** ENGINEERING_ONLY não ratifica mapa físico nem dá evidência absoluta.

Fontes: resolver, root_recommendation, consumer_review, prior_review, nuisance_measure; cláusulas C02, C03, C04.

#### O04 — Alcance da decisão científica e abertura por V1

**Já disponível:** V2 define cinco testes, α unilateral, Bonferroni5 e estados de ausência; prova condicional/cauda estão disponíveis. Nenhum resultado de engenharia autoriza veredito observado.

**Objeto mínimo faltante:** V1 único com função executável, pins de fontes/código/runtime, escolhas O01–O03, políticas numéricas/recursos e saídas permitidas. Ratificação por hash precede decisão separada de abrir dados para veredito, conforme §6.

**Alternativa A:** Manter a família frequentista calibrada mais evidência relativa separada; usar cota residual ou span global somente quando suas hipóteses estiverem demonstradas.

**Alternativa B:** Relatar engenharia/evidência relativa com calibração indisponível e sem sigma onde a cota não se aplica; essa limitação não se converte em não-rejeição nem elimina rejeição válida de outro teste.

**Encaminhamento proposto:** Preparar A com o comportamento de indisponibilidade já previsto no V2. Não exigir uma futura rejeição ou poder alto como condição de ratificabilidade. Poder fica campo separado; confirmar física continua ato do operador.

**Critério de fechamento:** Pacote revisável sem cláusulas concorrentes, com saída nula antes da abertura e comportamento definido para falha/ausência; decisão do operador registrada fora desta unidade.

**Fronteira:** Nenhuma abertura, veredito, nova autorização ou alteração da consolidação é produzida aqui.

Fontes: order, verdict_v2, verdict_review, calibration, numerical_interface, tail_v2_contract; cláusulas C09, C10, C11, C13.

## O que não se transforma em barreira nova

ENGINEERING_ONLY é uma entrega válida quando declara o que calculou e os erros que não limitou. Concordância de resoluções, diferença entre níveis ou um nome de módulo não são certificados; essa distinção não impede a implementação. O contrato numérico já permite engenharia primeiro e uma interface certificada separada.

Para a cauda que pretenda sustentar significância, as hipóteses reais da prova continuam necessárias. Uma cota inferior L=0 e p superior1 podem ser válidos e frouxos se alvo, suporte, identidade e família estiverem completamente qualificados. Não servem para cobrir modelo desconhecido, cenário faltante ou falha. Uma não-rejeição pela cota frouxa não demonstra que o p exato seja grande nem confirma o modelo.

Não é preciso resolver antecipadamente todos os cenários físicos possíveis: é preciso declarar os admitidos e não chamar a família finita de universal. Não se exigem63 priors nuisance novos onde a medida relativa comum já foi especificada. O poder permanece saída separada, só com informações permitidas; o preflight262 não passa a ser poder global e sua exclusão preparatória dos cinco MM não altera a seleção267.

A cronologia de novidade de uso e a reprodução E45 permanecem contribuições históricas distintas. Não precisam ser refeitas para esta ligação técnica; também não constituem evidência da nova likelihood conjunta. A leitura da ordem não adota seus números históricos como resultado novo.

## Custódia e limite desta nota

Somente documentos, contratos, pareceres e recibos nomeados foram lidos/pinados. Nenhum catálogo bruto, centro observado, C observada ou conjuntoD foi aberto; zero importações de candidatos/NumPy/SciPy/backend, controles científicos, WSL, rede e provedores. O auxiliar desta pasta só monta texto/JSON e verifica estrutura/pins. Não criou unidade científica, AUTH, CLAIM nem escreveu memórias, ledger ou pacotes consumidos. A qualificação nova descrita acima é dependência futura concreta, não campanha criada nesta entrega.

## Fontes e pins de entrada

IDs usados no quadro; os SHA256 completos e tamanhos estão no JSON de fontes. As leituras são documentais; hashes herdados de dados dentro dessas fontes não foram revalidados nos originais.

- **order**: [ORDEM_018_o_discriminante.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_018_o_discriminante.md>) — 17173 bytes; SHA256 57cff3a342573dab98a0f7e3e09e0fecff6d8b31b9ca987a078a2c9e913e3a0b.
- **draft**: [RASCUNHO_F9_CONSOLIDADO.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_consolidated_draft/RASCUNHO_F9_CONSOLIDADO.md>) — 17547 bytes; SHA256 40b600fb46ef0a8353e1952425406efcb90fb8201e157df6f73cad0f812509d4.
- **resolver**: [RESOLUTOR_F9.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_consolidated_draft/RESOLUTOR_F9.json>) — 69740 bytes; SHA256 c45de68d187fc49d5f79316b1561c9d9807dbb525019160837e8deea5e13ba53.
- **draft_review**: [PARECER_F9_CONSOLIDADO.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/revisao_f9_consolidado/PARECER_F9_CONSOLIDADO.md>) — 8327 bytes; SHA256 e57dcbfcabcb35ddbc7683611fd697fd90e25871277c80dc4c552f4d83240444.
- **root_recommendation**: [F9_ESCOLHAS_CONCRETAS_PROPOSTAS.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_ESCOLHAS_CONCRETAS_PROPOSTAS.md>) — 4569 bytes; SHA256 f681ac9f8ae58da06dfa18abc2bfa770d10983de54a5bbb770415f54999c807e.
- **c435**: [RECIBO_ROOT_PREDICAO_F9_REPARO_IMPORTS.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/RECIBO_ROOT_PREDICAO_F9_REPARO_IMPORTS.json>) — 21845 bytes; SHA256 9907b4800cd0dd4bb7968fc63ccfd583fb8c86fc36fc62a59f9a97354dca7bb5.
- **c435_tool**: [F9_IMPORT_REPAIR_EXECUTION_TOOL_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_IMPORT_REPAIR_EXECUTION_TOOL_RECEIPT.json>) — 5791 bytes; SHA256 09bfe43eec9a10d67b99f3393e32d47c44b591ebef7d864b94d448d5da061ac4.
- **consumer_review**: [PARECER_CONSUMIDOR_F9.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_f9_likelihood_consumer/PARECER_CONSUMIDOR_F9.md>) — 8833 bytes; SHA256 7f5bfa43207a0de07152ab59bba7cee11bd1cd54de1c799613dd87a42c3d815b.
- **consumer_review_receipt**: [RECIBO_REVISAO_ESTATICA.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_f9_likelihood_consumer/RECIBO_REVISAO_ESTATICA.json>) — 23088 bytes; SHA256 3c6116b92f5908ddd083adfbc7a4228780ce81cd61eefc9b9b2483198c869a51.
- **consumer_api**: [API_CONTRATO.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_likelihood_consumer_preparation/API_CONTRATO.md>) — 14238 bytes; SHA256 449e4ffb95a4af757384db4e1277741d37ffc1a7ab8d47d980910e6a5baabc77.
- **consumer_contract**: [CONTRATO_API.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_likelihood_consumer_preparation/CONTRATO_API.json>) — 8720 bytes; SHA256 9876fcdd3bdf38b86ca8d693ef3c6e1cdf94bace5276f21fd61d4dcc9389b5cb.
- **consumer_manifest**: [MANIFESTO_PREPARACAO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_likelihood_consumer_preparation/MANIFESTO_PREPARACAO.json>) — 5551 bytes; SHA256 c3059d019410e5732bfbb2af8a5c7e0a689fb34201d9c8f5ca174c2850cd4d4a.
- **prior_review**: [PARECER_PRIORS_FISICOS_F9.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_f9_physical_prior/PARECER_PRIORS_FISICOS_F9.md>) — 8641 bytes; SHA256 9bc6d2b8b94ddd46e966f8eaa63a1f90394923225c327be9890b229c0da70f6b.
- **prior_review_receipt**: [RECIBO_REVISAO_ESTATICA.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_f9_physical_prior/RECIBO_REVISAO_ESTATICA.json>) — 24175 bytes; SHA256 ad60436446f6b134a8ce2f73fd5c0cac827342a8f7728aabff55b90c6e4a676d.
- **prior_api**: [API_CONTRATO.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_physical_prior_preparation/API_CONTRATO.md>) — 10781 bytes; SHA256 9cb26ecd71dcdf54c7d8989cb21c03e1a92c0fb76e8026886862906bbd4b87b7.
- **prior_derivation**: [DERIVACAO.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_physical_prior_preparation/DERIVACAO.md>) — 12288 bytes; SHA256 1dd3d81dc735799050d3cf055342ab498e2a37f0932a6044e3e2e785265367ad.
- **prior_manifest**: [MANIFESTO_PREPARACAO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_physical_prior_preparation/MANIFESTO_PREPARACAO.json>) — 5103 bytes; SHA256 595db522d8ad6f296d211b1d36cf101025e2e85d0099d226846aa494997738e9.
- **precision_request**: [F9_PRECISION_SERVICES_PREPARATION_REQUEST.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_PRECISION_SERVICES_PREPARATION_REQUEST.json>) — 3431 bytes; SHA256 5e42d14b9ac7863b84b41bac1ed7ab65498746a0412e050e78f392ddc6cda1d3.
- **theta_identity**: [IDENTIDADE_PREPARACAO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_theta_integration_preparation/IDENTIDADE_PREPARACAO.json>) — 409 bytes; SHA256 0f574360ad18a2e28f76b0fa530147d2a64d96056467df04c13f1eede0b95894.
- **theta_alternatives**: [ALTERNATIVAS_ANTES_IMPLEMENTACAO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_theta_integration_preparation/ALTERNATIVAS_ANTES_IMPLEMENTACAO.json>) — 1307 bytes; SHA256 175ee18a5f4446f7340d9f0973afc12b7cb55917a38a839967cf6371f69f10c8.
- **reducer_request**: [REQUEST.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_decision_reducer_preparation/REQUEST.json>) — 1345 bytes; SHA256 39c8141a368a63db3b93da60d142aea1e781600b004e51dde5169a8556707bfe.
- **stellar_protocol**: [STELLAR_FAMILY_PROTOCOL.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/covariance_support/STELLAR_FAMILY_PROTOCOL.json>) — 3273 bytes; SHA256 873b80a42c90a56caf54c956f4e041cc7452188af1ce7608c349fb39eedc45d1.
- **nuisance_measure**: [MEDIDA_NUISANCE_CANDIDATA.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/h0dn_documentary_review/linear_design/MEDIDA_NUISANCE_CANDIDATA.json>) — 6429 bytes; SHA256 ef4e425026ee1047e1ca358e06aaf978c8ff9fdca9dbdcac8d0b09e8e6946895.
- **mm_contract**: [CONTRATO_MM_CANDIDATO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_mm_model_preparation/CONTRATO_MM_CANDIDATO.json>) — 15582 bytes; SHA256 c7731bcc21e29cf94c7d835e86e94f6e16d666a0085de90f5137b270f669936b.
- **mm_review**: [PARECER_MM_DOCUMENTAL.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_mm_model/PARECER_MM_DOCUMENTAL.md>) — 8926 bytes; SHA256 10facead246b9c862d5fdedd5a20998774aaa2b354fee146d6c2317ea57623b1.
- **verdict_v2**: [F9_VERDICT_CONTRACT_CANDIDATE_V2.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_verdict_contract/F9_VERDICT_CONTRACT_CANDIDATE_V2.json>) — 15895 bytes; SHA256 6b5118548490392a26eb43a8de9e5a252ae6e6fd28c3d0edbc2daa15c5813655.
- **verdict_review**: [ACEITE_DELTA_VC01_V2.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_contrato_f9/ACEITE_DELTA_VC01_V2.md>) — 2084 bytes; SHA256 c5e5cd7d1c6e8cc3969f134f83d55cf6f28ecc1e896467e12b66192653546bc9.
- **calibration**: [CALIBRATION_BOUND_CANDIDATE.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_calibration_bound/CALIBRATION_BOUND_CANDIDATE.json>) — 8941 bytes; SHA256 c5dfc055174fba6412488a8f63c9d32b1756602aa5dcb5ce7052b77c803b5641.
- **calibration_review**: [PARECER_COTA_CALIBRACAO_F9.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_cota_calibracao_f9/PARECER_COTA_CALIBRACAO_F9.md>) — 11497 bytes; SHA256 fe98859ea62cf5c25deda26f3a389335bfb5e817c0c0b623c55fd6d8478f0f2e.
- **calibration_receipt**: [RECIBO_ROOT_CONTROLES_COTA_CONCLUIDOS.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/RECIBO_ROOT_CONTROLES_COTA_CONCLUIDOS.json>) — 20493 bytes; SHA256 0b9d3c34bff2d98c38069e43e610291347d51a799b7e88b6c604c8780ef60648.
- **tail_v2_contract**: [CONTROL_CONTRACT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_tail_envelope_implementation_v2/CONTROL_CONTRACT.json>) — 26734 bytes; SHA256 c5cb151a622d0df707dff686dfee98064512bf1049f4f46a171a9e81fd469513.
- **tail_review**: [PARECER_DELTA_V2.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_tail_implementation_v2/PARECER_DELTA_V2.md>) — 5596 bytes; SHA256 1d2a718bd09f7dca4626d7495f197eb1a6715d049b8ebeb8c57268225af7c959.
- **tail_receipt**: [RECIBO_ROOT_CONTROLES_TAIL_V2_PASS.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/RECIBO_ROOT_CONTROLES_TAIL_V2_PASS.json>) — 34373 bytes; SHA256 2f323fcf9a8cc9b0e6f13716483309eb5c7ff31ec43c5ed6b586e43e73d407b7.
- **numerical_interface**: [INTERFACE_CERTIFICADOS_F9.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_numerical_certification_preparation/INTERFACE_CERTIFICADOS_F9.json>) — 11018 bytes; SHA256 df431bf0919b87dcbd9620f8852fac8192591f16efe23d51a7b7b12644cbd9ba.
- **numerical_review**: [PARECER_CERTIFICACAO_NUMERICA_F9.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/revisao_certificacao_numerica_f9/PARECER_CERTIFICACAO_NUMERICA_F9.md>) — 9913 bytes; SHA256 5aeb98ea47084862b1ee578e3570c8d2a225ae84aaa1ba8b893c76ea0bf3ae0d.
- **nc02_failure**: [RECIBO_ROOT_NC02_TERMINAL_FAILURE.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/RECIBO_ROOT_NC02_TERMINAL_FAILURE.json>) — 2082 bytes; SHA256 5bf97fc36acaa0a201fbb4da4ed619b088c5565c916e929012e6e6bf6cafb39a.
- **nc02_errata**: [ERRATA_AO_ACEITE_537.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/diagnostico_nc02_terminal/ERRATA_AO_ACEITE_537.md>) — 6295 bytes; SHA256 a9a5ef7cf81ca0b88dde3cd913fd2bce565d22b1539edb88e4584d7926b36a09.
- **background_receipt**: [THEORY_CONTROL_ROOT_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_background_prediction/THEORY_CONTROL_ROOT_RECEIPT.json>) — 14674 bytes; SHA256 e30ce77a2886cdcba1ee6f7687db8b41908eb74410f50bdf46ce37552c0b71d0.
