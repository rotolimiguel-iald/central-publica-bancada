# ORDEM 018 — consolidação F4

**RELATÓRIO EM CONSTRUÇÃO — NÃO É ENTREGA FINAL.**

[REAL documental] Candidato preparado para revisão da ROOT, por solicitação oficial `57a916b1-6698-4a38-b187-36cfe729f5bc`; preparação `1f4f4d57-6e55-4244-baad-ff0ccf3faa21`. F1 e F3 continuam incompletos. Esta síntese não executa novamente ciência, não concede abertura de dados e não altera o gate.

## Resultado que orienta a investigação

O sistema já permite reunir previsões, fontes, covariâncias e resultados em uma cadeia auditável. A utilidade concreta aparece quando a bancada separa uma comparação sensível de outra cega por construção, ou revela uma degenerescência que o gráfico sozinho ocultaria. A investigação anterior da bancada, registrada em `infra.bancada_oficial.investigacao_28set`, seq55, encontrou esses casos no ACT, no fundo BAO e no modo único de ringdown. Não mediu um ganho quantitativo de produtividade nem produziu uma nova significância física.

No ranking condicional F0 revisado, **R-A, razão de Hubble, é a prioridade atual por separação esperada**. O cenário R22 chega a D≈5,001 e a compressão H0DN a D≈6,018 sob as hipóteses fixadas de fundo, mapa universal, erros e covariância. Isso não é detecção observada da TGL nem resultado do futuro ajuste conjunto. H0DN reutiliza informação SH0ES/CCHP; não é uma segunda confirmação independente.

**R-B/R-M, resposta radiativa medida por CMB e BBN, vem em seguida como rota física complementar.** O pré-registro primordial V1 já existe e está congelado. O incremento esperado ΔN_eff≈0,119466 dá D≈0,996 com σ=0,12 no planejamento arquivado. As sensibilidades marginais de hélio e deutério também são da ordem de uma unidade, com aproximações declaradas. Não se somam esses números: β, informação cosmológica, relação BBN e dados auxiliares podem se sobrepor.

**R-C, ringdown em regime extremo, permanece uma rota a medir, sem poderD estabelecido.** Um regime extremo não garante maior detectabilidade: nuisance, degenerescências, ruído e escolha do observável determinam a capacidade de distinguir modelos. O conjunto D requer o PE conjunto solo220 previsto no contrato, seus controles e custo. O fato de dados estarem em RAM ou renderizados na GPU não substitui essa inferência.

Há, portanto, duas prioridades compatíveis: finalizar o teste conjunto de R-A com seus rivais explícitos; preservar R-B/R-M como teste radiativo já especificado, respeitando suas reservas. O ringdown segue sua dependência científica própria, sem receber um valor de sigma emprestado de outro domínio. Não há nesta consolidação uma pontuação multimodal global observada ≥5σ.

## O que efetivamente foi obtido em Hubble

F1a conferiu fontes e dependências, reutilizando a cronologia existente. O antecedente holográfico do valor 0,012 em novembro de 2025 foi localizado; o ramo inverso de H0 em dezembro é distinto e seu best-fit foi registrado como incompatível com o valor teórico. A relação com √e aparece em janeiro e a fatoração explícita em março; D1a aparece em maio e D1b em junho. O MCMC-CRUZ histórico usava âncoras EM/numéricas; a variante alpha-free tem alterações de fonte verificadas, mas nenhum posterior foi localizado no inventário delimitado daquela auditoria. Não transferir os resultados do ramo ancorado à variante alpha-free. A auditoria não certificou toda a história de seleção da lei nem a primeira publicação remota.

Essa distinção preserva a novidade de uso: uma retrodição sem ajuste pode discriminar modelos. Conhecer um dado ou derivar uma hipótese com IA não desqualifica automaticamente o teste. O ponto verificável é a dependência efetiva dos parâmetros e a definição do teste, com a história dos ramos preservada.

F1b reproduziu os resultados históricos dentro do respectivo modelo estatístico. As covariâncias internas completas foram usadas onde previstas; independência entre blocos e a diagonal de CC continuam hipóteses explícitas da reprodução. Reutilizar uma tabela CAMB pinada não equivale a gerar essa tabela independentemente.

| Objeto histórico | Resultado lido dos recibos | Limite de interpretação |
|---|---|---|
| SN-only P5 | H0=73,53291178 ±1,01700384; 1657 linhas, 77 calibradoras, 37 hosts | Reprodução da seleção Pantheon+SH0ES; não é um segundo R22 independente. |
| T4 sem escada | χ²: ΛCDM 29,01668; TGL 39,40980; β livre 28,94598 | O resultado desfavorável à leitura TGL nesse recorte é preservado; CC diagonal/fatoração histórica. |
| P4 d1b | lnB(TGL/ΛCDM)≈8,02037; lnB(TGL/β livre)≈2,24314 na grade35 | Integrais relativas reduzidas sob medida nuisance comum. |
| P5 sombra | lnB(TGL/ΛCDM)≈13,83694; lnB(TGL/β livre)≈2,86052 na grade35 | Mesmo tipo de integral, outro experimento estatístico; não multiplicar com P4. |
| P5 sombra, leitura histórica | ΛCDM a 5,26σ; TGL a −0,38σ | Esses números pertencem a P5. Não combiná-los com lnB≈8,02/2,25 de P4. |

A comparação das grades25/35 é evidência de estabilidade numérica na região calculada; não fornece sozinha um limite rigoroso das caudas. Onze novas unidades E45 custaram 904,881 s e tiveram pico informado de 165,594 MiB, com uma unidade antiga reutilizada; são custos daquele cálculo histórico, não previsão de custo do novo composto.

## Dois F9 diferentes

**Atualização recebida durante a preparação, 06/10/2026:** a nova errata das instruções do operador e o manifesto local `work/v388_selo/v388_incorporacao_manifesto.json` registram a abertura do **V1 escalar**: z_disc=+4,28, z_delta=−1,42, lnB(TGL/ΛCDM)=9,17, com veredito oficial `INCONCLUSIVE_SYSTEMATICS` enquanto faltam fontes dos cinco leitores por hash. Portanto o poder prévio5,91 não se realizou como discriminação observada≥5. A favorabilidade bayesiana registrada não converte lnB em sigma. Esta atualização é leitura documental do resultado da gerência; não recalculamos a função nem abrimos os dados brutos. O manifesto de incorporação é fonte secundária: o resultado primário fica distinguido na conferência específica, quando acessível.

**Conferência primária posterior, ao lado:** ROOT forneceu os localizadores exatos e esta preparação leu e conferiu os bytes de `RESULTADO_FASE9_V1_20261006_110507.json` e `RECALCULO_AO_LADO_v388.json`. O primeiro contém z_disc=4,283735613863391, z_delta=−1,4243571651630185 e lnB(TGL/ΛCDM)=9,166739752963847. O segundo conserva o resultado congelado e corrige ao lado lnB(TGL/β livre): n25=2,2406094687539877, n35=1,942091946689592 e n200=1,9692166174194288; z_disc com logdet=4,281761262135909. A diferença n25/n35 de0,29851752206439564 nesta abertura não é a pequena variação E45 histórica de P4/P5. O recálculo ao lado não é um novo veredito. [REAL — conteúdo documental e hashes conferidos; sem reprodução independente nesta preparação]. Fontes, trechos e hashes completos estão em ADENDO_ABERTURA_VERIFICADA.json e CONFERENCIA_PINS.json.

As expressões abaixo sobre reserva/abertura são a regra do contrato congelado; não devem ser lidas como negação dessa abertura escalar posterior. A autorização/execução desse instrumento não é transferida à proposta conjunta ROOT90da, que permanece aberta. A rota de selo `umpy.v388.selo_beta_corre_e_fase9_aberta`, seq665, registra a incorporação, enquanto a rota específica do V1 ainda só retornou604 na consulta desta preparação.

| Aspecto | V1 escalar congelado da gerência, seq604 | Proposta conjunta ROOT90da, comparação seq652 |
|---|---|---|
| Unidade observacional | Cinco leitores-resumo de H0, um por programa | 267 componentes locais H0DN V01+JAGB e16 de fundo:283; nuisance63 |
| Fundo | BG1 sem escada, resumido; erro de fundo comum | Planck comprimido3+DESI DR2 completo13, previsão de fundo no prior |
| Cefeidas | Shift no leitor SH0ES, com tratamento próprio do CCHP misto | Resposta elementar c_C na rede, não um shift uniforme do resumo |
| Covariância | Cruzamentos entre programas estimados/declarados | Família finita de600 rótulos condicionais, nove blocos e36 cruzes |
| Decisão | Função escalar congelada | Cinco testes separados, calibração condicional, Bayes relativo e poder distintos |
| Estado | Especificação congelada; D-H e abertura reservados | Consolidação documental revisada, executável completo ainda não qualificado/ratificado |

Os cenários escalares de poder 5,91; 4,27 sem Cefeidas; 5,20/BG2 e 5,11/BG3 pertencem ao V1 da gerência. Não são poder do contrato conjunto. Os cinco modelos conjuntos são: H1 ΛCDM; H2 TGL com β fixo em runtime; H3 β livre diagnóstico; H4 deslocamento de Cefeidas; H5 régua BAO livre, mantendo rstar padrão no CMB. H5 não é uma implementação de Early Dark Energy. A RG continua limite clássico, e não rival estatístico desses cinco modelos cosmológicos.

Antes de um composto futuro, o handoff deve dizer qual especificação é primária e qual é diagnóstico. A preparação conjunta atende ao pedido F1 original; não substitui silenciosamente o V1 escalar. Priors, amostra, fatoração, resposta e regra de decisão mudam o experimento e precisam permanecer ligados à sua identidade.

## Engenharia disponível e o que ela ainda não demonstra

Os recibos a seguir são aproveitados como dependências concluídas. Eles não serão repetidos para produzir um placar maior e não substituem F1 científico.

| Unidade consumida | Evidência | Alcance |
|---|---|---|
| Q01 escalar, d8aac6d3 | PASS9, seq605/608 | Serviço escalar; sem inferência conjunta. |
| Q01 theta, 4e9a80ad | PASS15, seq621/623/624 | Callback/grade; T06 preserva integral real2 versus amostrada1: não certifica erro uniforme. |
| Priors extras, 4f5a24b4 | PASS11, seq633–635 | Junção sintética de priors; divergência marshal entre processos permanece sem causa estabelecida. |
| Junção matricial, 755c3b08 | PASS5, seq645 | X283×63 e dois suportes sintéticos; não qualifica todos os600 rótulos nem o prior físico completo. |
| I03, 27c6d5e9 | PASS6, seq653–655 | Dois casos comparados à referência racional, rank211; quatro recusas esperadas. |
| Supervisor f7e2 / revisão2edbb481 | Aceite estático seq660/661 | Fonte stdlib/diffs cooperativos; não execução científica nem proteção nativa completa. |
| I02_99e2 / revisão0300b3d4 | Aceite estático seq664 | Admissões comparadas antes de claims/cache/background no callback, com validação posterior preservada. |

I02 foi revisto sob módulos pinados e objetos confiáveis. Não garante resistência a mutação hostil/concorrente; construir DurableStore previamente pode sincronizar disco. A integração científica exige runtime, guard, operações POSIX, quota agregada, pipes/ACK/watchdog e recibos externos próprios. As qualificações e a cobertura de todo o domínio não são inferidas de testes parciais.

A precisão do fundo já foi avaliada em pontos delimitados e um acoplamento de cinco modelos consumiu uma chamada real do solver. Isso também não certifica o domínio inteiro. As unidades falhas ou incertas anteriores continuam terminais; não se reabrem pela existência deste relatório.

## Primordial e ringdown: estado reconciliado

O rascunho F3 radiativo foi cumprido e sucedido pelo **V1 primordial congelado, seq607**, reconciliado na seq618. As decisões D1/D2/D3/D4/D6/D7/D9/D10/D11 e o bracket D5a estão registrados. Não há onze perguntas a fazer novamente. As reservas efetivas são D8 (admissão de fontes/alvo), D5b (BBN exato, se escolhido) e E3 (abertura/execução). Os nove corpos locais já pinados são candidatos à admissão, não permissão automática. O mapaC preserva AWAITING_SOURCE onde assim consta.

Uma única entrada de β por instrumento deve ser preservada: correção do fluido total e parametrização efetiva N_eff não se empilham. TGL-S é o ramo primário do contrato; TGL-L é co-leitura de baixa sensibilidade. ω_b não pode ser inferido do mesmo D/H sob S=1 e reinserido como prior independente para testar S≠1. O bracket de tabelas não é execução de um código BBN exato com S(T). F6, conferência dos axiomas antes de citações no livro, permanece tarefa específica da gerência; não bloqueia retrospectivamente a existência do V1.

R-C possui seleção D14 e quatro holds; A/B/C são calibração, não novos testes independentes. **INIT003 terminou sem convergência e não será repetido.** Seu recibo registra GR wall857,915 s, CPU857,333 s, 9738 chamadas e ΔlogZ≈57,276; a campanha durou958,936 s. RB foi interrompido, sem RESULT final; o último progresso não é custo total. D não foi aberto. Exit0 do supervisor não significou sucesso científico: a auditoria encontrou tentativa de cache recusada que fora absorvida pelo importador, sem interrupção imediata da amostragem.

Guard/checkpoints já existem nos candidatos P3; a comparação619 e o empacotamento627 são reutilizados. Falta completar o pacote científico e sua qualificação, para então realizar o PE D previsto, controles e custo. O custo de INIT003 não prevê a campanha D convergida. A estimativa histórica de63–78 CPUh é [DECLARADO], não custo medido de D. Um contraste geométrico A31 ou ajuste A/B/C não preenche essa lacuna.

## Calendário, sobreposição e falsificações históricas

Não foi verificado um cronograma que entregue 5σ global em2027 ou2030. Para R-B, a meta marginal de planejamento é σ(N_eff)≤0,023893, sob as hipóteses do canal. O forecast Simons Enhanced arquivado refere-se a2025–2034, ruído-meta e Planck, com σ≈0,045; não é forecast de2030. O número histórico CMB-S4≈0,03 pressupõe consistência BBN, enquanto a alternativa com Yp livre é≈0,09. A situação operacional arquivada de CMB-S4 impede transformá-lo em promessa de levantamento. A suposição teórica BBN e a reutilização de dados BBN são questões diferentes.

Em R-D, reduzir idealmente a covariância inteira para alcançar uma separação escolhida não informa duração de observação ou número realista de objetos. Nenhuma das13 rotas ganhou aqui um calendário inventado. R-N, ondas gravitacionais primordiais estocásticas, aparece no adendo como **OPEN sem previsão quantitativa**, fora do conjunto original A–M.

Não somar: R-A com H0DN/SH0ES/CCHP reutilizados; P4 com P5; R-D com R-E sobre SN/BAO; ACT atualizado com sua versão anterior; CMB+BBN que compartilhe ω_b, Yp ou relações; GWTC-5 com GW170817 incluído; canais D9/D10 que usem os mesmos dados. A unidade estatística é a likelihood especificada com covariância e seleção, não o nome de uma sonda no painel.

Rótulos históricos FALSIFIED/EXCLUDED/UNDERPOWERED conservam seu alvo exato: par hipótese–mapa–dados, escala temporal, canal e versão. Não são apagados por uma nova representação; tampouco são transferidos à teoria inteira ou ao novo contrato por homonímia. O catálogo por seq fornece essa história. NOT_FALSIFIED não vira CONFIRMED; nenhum rito de natureza altera o gate matemático.
