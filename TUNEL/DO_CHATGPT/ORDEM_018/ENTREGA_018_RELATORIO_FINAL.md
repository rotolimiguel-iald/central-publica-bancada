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


## Cobertura requisito a requisito

### F0 — CUMPRIDO_DOCUMENTAL_CONDICIONAL

R-A–R-M inventariadas, com ranking condicionado e atualização ACT. R-N é adição OPEN.

**O que falta / limite:** Não há calendário de poder global 2027/2030 ratificado; não substituir essa ausência por projeção temporal.

Evidência: [F0_RANKING_REGISTRY.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F0_RANKING_REGISTRY.json>); [REVISAO_CONSOLIDACAO_F0_F2_RECIBO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/REVISAO_CONSOLIDACAO_F0_F2_RECIBO.json>).

### F1a — CUMPRIDO_NO_RECORTE_DOCUMENTAL_COM_RESSALVAS

Cronologia existente reutilizada e fontes exatas conferidas: antecedente novembro, ramo inverso separado em dezembro, relação em janeiro/março, D1a maio, D1b junho. CRUZ ancorado e Evento2 alpha-free distinguidos.

**O que falta / limite:** Primeira publicação remota, primeira grafia K e posterior alpha-free não certificados por esta auditoria delimitada; não são prova de inexistência nem demérito da retrodição.

Evidência: [NOTA_PROVENIENCIA_F1.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/NOTA_PROVENIENCIA_F1.md>); [MANIFESTO_FONTES_F1.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/MANIFESTO_FONTES_F1.json>).

### F1b — REPRODUCOES_HISTORICAS_ENTREGUES

SN-only, fundo T4, ajustes P4/P5 e integrais relativas E45 reproduzidos sob as fatorações e covariâncias declaradas.

**O que falta / limite:** Reutilização da tabela CAMB histórica não é geração independente do solver; estabilidade 25/35 não certifica caudas. Não equivale ao novo conjunto de cinco hipóteses.

Evidência: [RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/reproducao_fase5/RESULT.json>); [T4_NOTA_REPRODUCAO.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/reproducao_fase45_conjunta/T4_NOTA_REPRODUCAO.md>); [P45_NOTA_REPRODUCAO.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/reproducao_fase45_conjunta/P45_NOTA_REPRODUCAO.md>); [E45A_NOTA_CONSOLIDADA.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/reproducao_fase45_conjunta/E45A_NOTA_CONSOLIDADA.md>); [RECIBO_ACEITE_E45_FINAL.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/RECIBO_ACEITE_E45_FINAL.json>).

### F1c — ABERTO_CADEIA_CONJUNTA

Cinco modelos e medida comum de nuisance especificados; testes de componentes e algumas junções consumidos. I02 recebeu aceite estático664; supervisor recebe sucessor científico.

**O que falta / limite:** Integração completa, runtime/supervisão/pipes/quota, precisão no domínio completo e decisão calibrada ainda não qualificadas. Não há novo resultado relativo observado dos cinco modelos.

Evidência: [CONTRATO_CONSOLIDADO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_executive_contract_preparation/CONTRATO_CONSOLIDADO.json>); [RECIBO_ROOT_I03_COVARIANCE_JOIN_PASS6.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/RECIBO_ROOT_I03_COVARIANCE_JOIN_PASS6.json>); [RECIBO_ROOT_ACEITE_REVISAO_SUPERVISOR_660.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/RECIBO_ROOT_ACEITE_REVISAO_SUPERVISOR_660.json>); [RECIBO_REVISAO_INDEPENDENTE.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_i02_preflight_independent_review_root/RECIBO_REVISAO_INDEPENDENTE.json>).

### F1d — PARCIAL_REDE_E_RESPOSTAS_PREPARADAS

JAGB localizada na extensão V01; c_C elementar, covariância e desenho comum preparados. H0DN não é independente de SH0ES/CCHP.

**O que falta / limite:** Avaliação observada conjunta TRGB/JAGB e hipótese de universalidade ainda não realizada nesta cadeia.

Evidência: [ENTREGA_JAGB.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/h0dn_documentary_review/jagb_extension/ENTREGA_JAGB.md>); [MANIFESTO_ENTREGA.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/h0dn_documentary_review/jagb_extension/MANIFESTO_ENTREGA.json>).

### F1e — V1_ESCALAR_CONGELADO_E_PROPOSTA_CONJUNTA_DISTINTA

Gerência congelou V1 escalar604. Proposta ROOT90da usa rede283, diferente da primeira, com revisão documental646. Abertura escalar posterior foi lida em recibo primário e mantém INCONCLUSIVE_SYSTEMATICS; correção de quadratura preservada ao lado.

**O que falta / limite:** Proposta executável conjunta completa, ratificação de sua primariedade/diagnóstico e abertura separada. Não substituir V1 escalar silenciosamente.

Evidência: [COMPARACAO_ESPECIFICACOES_F9.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/COMPARACAO_ESPECIFICACOES_F9.json>); [CONTRATO_CONSOLIDADO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_executive_contract_preparation/CONTRATO_CONSOLIDADO.json>).

### F2 — ENTREGUE_COM_LACUNAS_EXPLICITAS

Sete derivações examinadas, errata de lentes393 e revisão394 incorporadas; R-I recebeu análise separada396–397.

**O que falta / limite:** OPEN de mapa observacional em dualidade, lentes, crescimento e perfil de vazios; não promovidos por inventário ou testes de engenharia.

Evidência: [ENTREGA_018_F2_DERIVACOES.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/ENTREGA_018_F2_DERIVACOES.md>); [NOTA_DERIVACOES_F2.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/NOTA_DERIVACOES_F2.md>); [NOTA_PODER_FORMA.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/poder_forma/NOTA_PODER_FORMA.md>).

### F3-RB-RM — RASCUNHO_CUMPRIDO_SUCEDIDO_POR_V1_CONGELADO

V1 congelado607 substitui rascunho; D1–D11 em grande parte decididos por delegação, reconciliação618.

**O que falta / limite:** D8 admissão de fontes/alvos, D5b código BBN exato se escolhido e E3 abertura. Runner e revisão próprios; não pedir onze ratificações novamente.

Evidência: [MANIFESTO_RECONCILIACAO.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/fase8_reconciliacao_v1/MANIFESTO_RECONCILIACAO.json>); [QUADRO_DECISOES_D1_D11.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/fase8_reconciliacao_v1/QUADRO_DECISOES_D1_D11.json>).

### F3-RC — ABERTO_PE_CONJUNTO_D

D14 selecionado, quatro holds, PE solo220 em preparação. INIT003 encerrado sem convergência; guard ligado e pacote de imports em preparação627.

**O que falta / limite:** Qualificação científica posterior, PE D com controles, custo e sensibilidade medidos. Não repetir INIT003 nem tratar A/B/C como novo teste.

Evidência: [NOTA_PREREGISTROS_F3.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/NOTA_PREREGISTROS_F3.md>); [RECIBO_ROOT_ENCERRAMENTO_INIT003.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_init_qualified_003/RECIBO_ROOT_ENCERRAMENTO_INIT003.json>); [NOTA_LIGACAO_P3_GUARD.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/p3_guard_integration_preparation/NOTA_LIGACAO_P3_GUARD.md>).

### F4 — CANDIDATO_EM_CONSTRUCAO_NAO_FINAL

Esta consolidação conecta requisitos, rotas, documentos, decisões e coordenação. Inclui atualização escalar665 recebida durante a síntese.

**O que falta / limite:** ROOT revisar candidato e incorporar resultados válidos quando F1/F3 terminarem. Não declarar missão concluída.

Evidência: [F4_CONSOLIDATION_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F4_CONSOLIDATION_DISPATCH_RECEIPT.json>).

## Catálogo completo R-A–R-M e ranking condicionado

Números abaixo são transcritos do registro F0 revisado, não recalculados. A coluna histórica de decisões do registro é preservada no JSON; a leitura atual aparece em cada rota. D representa separação esperada sob as hipóteses indicadas; não é significância observada global.

### R-A — Razão de Hubble (posição: 1)

**Previsão e estatuto:** K*=E(z*)^(2 beta/3); Hlocal=K*Hbg, sob o mapa universal ratificável. DERIVED condicional / INPUT do mapa.

**Dados / precisão:** R22 sigma 1,04; CCHP TRGB combinado 1,936; TRGB JWST 2,224; JAGB 2,720 km/s/Mpc. H0DN sigma 0,81 é candidato documental adicional.

**Separação:** R22 5,001; TRGB combinado 2,917; TRGB JWST 2,562; JAGB 2,114. H0DN 6,018 apenas sob a compressão universal e demais hipóteses do planejamento.

**Estado vigente:** Maior separação esperada entre rotas com mapa especificado. F1 conjunto permanece OPEN; dois F9 distintos. V1 escalar604 por hash não ratifica ROOT90da. Atualização665: abertura do V1 escalar registrada e recibos primários conferidos: z_disc4,2837 e INCONCLUSIVE_SYSTEMATICS; recálculo ao lado mantém z_disc4,2818. Isto não é o poder prévio nem ROOT90da.

**Fontes locais da leitura:** FONTES_PUBLICAS.json; FONTES_ATUALIZACAO_F0.json; F0_UPDATED_SIGMAS_RESULT.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `hubble.fase9_razao_discriminante` — seqs 373, 383, 386, 399, 403, 408, 416, 417, 421, 422, 428, 435, 436, 437, 439, 442, 443, 444, 446, 449, 451, 452, 453, 454, 455, 456, 458, 459, 460, 462, 466, 467, 468, 469, 470, 471, 474, 477, 478, 481, 484, 485, 486, 487, 488, 489, 490, 494, 498, 499, 500, 501, 502, 503, 507, 508, 510, 511, 512, 513, 515, 516, 518, 520, 521, 522, 524, 525, 531, 532, 534, 535, 537, 538, 539, 540, 542, 543, 545, 548, 552, 553, 554, 555, 556, 557, 558, 559, 561, 562, 563, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 592, 593, 594, 595, 596, 597, 598, 599, 601, 602, 605, 608, 609, 610, 611, 612, 613, 615, 620, 621, 623, 624, 626, 628, 630, 633, 634, 635, 637, 639, 640, 641, 642, 643, 645, 646, 647, 648, 650, 651, 653, 654, 655, 656, 657, 660, 661, 664.
- `d1.fase9.razao_de_hubble.v1_06out` — seqs 604.
- `d1.fase4_desvio_30set` — seqs 223, 225, 226, 227, 228, 229, 230, 231, 232, 406, 410.
- `d1.fase5_sh0es_01out` — seqs 236, 237, 238, 239, 240, 241, 242, 388, 407.
- `discriminante.ordem018.f1b.fase45_conjunta` — seqs 405, 409, 413, 414, 415, 418, 420, 423, 424, 425, 427, 430, 431, 438, 440.

### R-B — Era da radiação / CMB (posição: 2 (com R-M))

**Previsão e estatuto:** delta rho_r/rho_r=4 beta/3; DeltaNeff=0,119466 na equivalência pós-e±. DERIVED condicional ao mapa e fechamento perturbativo.

**Dados / precisão:** Planck+BAO sigma 0,17; P-ACT-LB 0,13; P-ACT-LB-D-He 0,11; não independentes

**Separação:** 0,703; 0,919; 1,086, respectivamente. A última já usa BBN.

**Estado vigente:** Uma rota radiativa com R-M, dois instrumentos. V1 congelado607; reservas D8/D5b/E3. ACT atualizado é substituição de precisão, não evidência independente.

**Fontes locais da leitura:** preregistros/primordial/FONTES_PRIMARIAS.json; FONTES_ATUALIZACAO_F0.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `cmb.neff_e_rho_mais_p` — seqs 156, 372, 606.
- `primordial.fase8_era_da_radiacao` — seqs 371, 375, 392, 402, 607, 618.

### R-M — BBN direta (posição: 2 (com R-B))

**Previsão e estatuto:** Proxy S=sqrt(1+4 beta/3); DeltaYp=0,00140708 e Delta log10(D/H)=0,00657979, sob sensibilidades declaradas. DERIVED condicional, não integração BBN exata.

**Dados / precisão:** Aver 2026 sigma Yp 0,0013; Cooke 2018 sigma log10(D/H) 0,0052; teoria/nuisance adicionais

**Separação:** 1,082 e 1,265 por canal, antes de teoria/nuisance. Não combinar em quadratura.

**Estado vigente:** Compartilha beta e tratamento de radiação com R-B. Bracket adotado; BBN exato não executado. Não somar D/H, Yp, Neff sem covariância/teoria.

**Fontes locais da leitura:** preregistros/primordial/CALCULO_SENSIBILIDADES_SIGMAS.json; preregistros/primordial/PREREGISTRO_FASE8_V1_RASCUNHO_ORDEM018.md. As identidades estão em FONTES_EVIDENCIAS.json.

- `primordial.fase8_era_da_radiacao` — seqs 371, 375, 392, 402, 607, 618.

### R-H — Sirenes-padrão (posição: 3 condicional)

**Previsão e estatuto:** Hsirene=K*Hbg é hipótese de extensão; falta fixar propagação GW / leitura de distância. OPEN na ponte observacional; DERIVED no cenário universal.

**Dados / precisão:** GWTC-5.0, 236 GW, larguras assimétricas 7,5 e 9,4 km/s/Mpc; contém GW170817

**Separação:** 0,780–0,623 como proxies gaussianos de largura; não uma análise da likelihood assimétrica

**Estado vigente:** Ponte Hsirene=K Hbg permanece OPEN; largura assimétrica reduzida a proxy não é likelihood. GWTC-5 inclui GW170817.

**Fontes locais da leitura:** FONTES_PUBLICAS_ADICIONAIS.json; F0_ADDITIONAL_POWER.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.r_h_sirenes` — seqs 401.

### R-C — Ringdown ramo B (posição: não ordenar D antes de instrumento)

**Previsão e estatuto:** delta tau220=-x/(1+x); x=beta [2pi/kappa_hat(chi)] N(chi). DERIVED no contrato F2b; V1 congelado, teste D pendente.

**Dados / precisão:** D: 14 elegíveis declarados, quatro holds. A31: sigmas/spins de calibração já conhecidos.

**Separação:** D não medido. Em A31, só a geometria do contraste dá 11,383 bruto e 0,742 após c0+kc sigma livres; isto não é forecast nem veredito D.

**Estado vigente:** Sem poderD medido. INIT003 TERMINAL/STOPPED_NOT_CONVERGED, não repetir. Rótulos FALSIFIED históricos limitados ao par modelo/mapa, não ao novo D-only.

**Fontes locais da leitura:** preregistros/NOTA_PREREGISTROS_F3.md; VERIFICACAO_INDEPENDENTE_RINGDOWN_SHAPE.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `ringdown.ramo_b_preregistro_v386` — seqs 365, 374, 398, 411, 412, 419, 426, 429, 432, 433, 434, 441, 445, 447, 448, 450, 457, 461, 463, 464, 465, 472, 473, 475, 476, 479, 480, 482, 483, 491, 492, 493, 495, 496, 497, 504, 506, 509, 514, 519, 523, 526, 527, 528, 529, 533, 536, 541, 546, 547, 549, 550, 617, 619, 627.
- `ringdown.dephasing` — seqs 24, 25, 26, 27, 44, 85, 86, 88, 89, 90, 92, 132, 141, 249, 352, 355, 356, 359, 361, 368.
- `ringdown.modo_unico.degenerescencia` — seqs 58, 87, 91.

### R-D — Forma em redshift (posição: 4 condicional)

**Previsão e estatuto:** Q(z)=[integral k/E]/[integral 1/E], k=E^(2 beta/3), para acumulada/sombra. DERIVED sob FRW plano, continuidade e rho+p>=0.

**Dados / precisão:** 1580 linhas SN sem calibradores na máscara auditada; covariância DESI DR2 de 13 componentes

**Separação:** Mapa implementado A: SN+BAO com amplitudes próprias e Omega_m comum, D=0,164; SN só amplitude D=0,183 e com Omega_m D=0,030. Mapa hipotético B dá 0,294 conjunto após nuisance.

**Estado vigente:** Derivação condicional e poder de forma já calculados; BAO nu no mapa A. Não recalcular nem fundir com R-E.

**Fontes locais da leitura:** derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/poder_forma/NOTA_PODER_FORMA.md. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f2.r_d` — seqs 376, 389, 394.

### R-E — Dualidade de distâncias (posição: sem ranking físico único)

**Previsão e estatuto:** eta=fL/fA; geometria comum dá 1; luminosidade apenas pode dar Q/K*, forma Q. DERIVED condicional / OPEN no mapa único.

**Dados / precisão:** Mesmo SN/BAO de R-D; os 1–2% herdados não constituem nova covariância verificada

**Separação:** Zero para mapa comum; restante depende do mapa e nuisance. Não reutilizar R-D como evidência independente.

**Estado vigente:** Sem previsão única fL/fA; depende do mapa. Mesmos SN/BAO de R-D.

**Fontes locais da leitura:** derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/poder_forma/NOTA_PODER_FORMA.md. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f2.r_e` — seqs 377, 390.

### R-G — Lentes e atrasos (posição: sem ranking físico único)

**Previsão e estatuto:** Hfit/Hbg=fphi/(ft FD), FD=fl fs/fls; fphi=DeltaPhi_fit/DeltaPhi_true. DERIVED condicional / OPEN nas leituras.

**Dados / precisão:** TDCOSMO 2025 sigma maior 3,9 km/s/Mpc; uso de Pantheon+ para Omega_m

**Separação:** Endpoint k(zs) hipotético: 0,122–0,217 para zs 1,5–3. Esse endpoint não foi derivado como mapa de lentes.

**Estado vigente:** Convenção fphi corrigida393; mapa de lente ainda OPEN. Usa Pantheon+ como auxiliar.

**Fontes locais da leitura:** derivacoes/ERRATA_R_G_FPHI.md; derivacoes/F2_FONTES_SHA256.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f2.r_g` — seqs 379, 391, 393.

### R-L — Crescimento / S8 (posição: sem ranking físico único)

**Previsão e estatuto:** sqrt(1+beta)-1=0,599766% se sigma8 permanecer fixo; não é previsão de shear. DERIVED algébrico / OPEN dinâmica.

**Dados / precisão:** KiDS-Legacy sigma maior S8 0,021

**Separação:** Proxy aritmético 0,2285 em S8 fiducial 0,8; sinal físico não determinado

**Estado vigente:** Proxy S8 não substitui P(k,z)/slip/mu/condições iniciais e projeção. Sem previsão dinâmica única.

**Fontes locais da leitura:** derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_CALCULOS_CONDICIONAIS.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f2.r_l` — seqs 380.

### R-F — Temperatura CMB (posição: sem previsão diferente estabelecida)

**Previsão e estatuto:** Dephasing na base do mesmo H conserva energia; com redshift geométrico usual e expansão adiabática, T=T0(1+z). Outro ramo exige Qgamma ou mapa de frequência.. DERIVED sob hipóteses / OPEN no ramo alternativo.

**Dados / precisão:** SZ direto sigma_gamma 0,018; combinado direto+indireto 0,008 sobrepõe dualidade/SN

**Separação:** Zero nesse ramo conservativo com redshift usual e adiabaticidade; gamma=beta não derivado

**Estado vigente:** Conservação de energia no mesmo H + redshift usual + adiabaticidade. Ramo conservador tem sinal nulo; gamma=beta não derivado.

**Fontes locais da leitura:** derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_FONTES_SHA256.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f2.r_f` — seqs 378.

### R-I — Piso dos vazios (posição: consistência / perfil OPEN)

**Previsão e estatuto:** Tc[f]=(3/xc^3) integral_0^xc f(x)x^2 dx >= beta; xc=0,25. limite canônico; DERIVED na distinção média/perfil.

**Dados / precisão:** Fontes das funções canônicas e mapa V11 consultados; nenhum catálogo reaberto

**Separação:** Não há contraste de perfil fixado pelo piso; compatibilidade de ambos com desigualdade não separa os modelos.

**Estado vigente:** Piso é restrição, não perfil radial ou população única. Preservar V11; perfil/operador observacional OPEN.

**Fontes locais da leitura:** derivacoes/R_I_PISO_E_PERFIL.md; derivacoes/R_I_MANIFESTO.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f0.r_i` — seqs 396.
- `vazios.piso.v11` — seqs 3, 75, 82, 83, 84, 397.
- `vazios.piso.cadeia_v78_v92` — seqs 158, 395.

### R-J — Relógios (posição: sem nova escala de laboratório)

**Previsão e estatuto:** Gamma=.5 beta tau* omega^2; tau*=tP dá 1,28036e-40 s^-1 a 100 Hz. DERIVED condicional; ligação ao aparelho OPEN.

**Dados / precisão:** P1/P2/P3 no mapa consultados, não refeitos

**Separação:** Nenhum novo poder estabelecido. Duas leituras não fornecem outra tau* por si.

**Estado vigente:** Escala temporal alternativa não deriva de duas leituras. P1/P2/P3 históricos preservados; não reabrir.

**Fontes locais da leitura:** derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_CALCULOS_CONDICIONAIS.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f2.r_j` — seqs 381.
- `relogios.v1` — seqs 8, 9, 99, 102, 253.

### R-K — Neutrinos (posição: teste restritivo, não LCDM fixo)

**Previsão e estatuto:** m2=beta sin45° vezes 1 eV=8,507414 meV, com ângulo POSTULATE e escala NORM; m1=0 e NO para splitting. DERIVED de INPUTs; não ordenamento derivado.

**Dados / precisão:** JUNO sigma_Dm21^2=0,12e-5 eV^2; kill_rule histórica exige duas determinações autônomas

**Separação:** LCDM não fixa splitting único. Soma já aposentada por D2; não converter limite 95% em sigma.

**Estado vigente:** Regra m2 com ângulo POSTULATE e escala NORM. Soma aposentada; determinações independentes requeridas no protocolo.

**Fontes locais da leitura:** derivacoes/NOTA_DERIVACOES_F2.md; derivacoes/F2_FONTES_SHA256.json. As identidades estão em FONTES_EVIDENCIAS.json.

- `discriminante.ordem018.f2.r_k` — seqs 382.
- `neutrinos.m2.normalizacao` — seqs 59, 93, 98, 101, 128, 136, 142, 256.
- `neutrinos.massa_v1_e_soma` — seqs 161.

## Decisões reservadas e maturidade do pacote

- **F9_PRIMARIEDADE** (OPERADOR/GERENCIA; PARCIAL): V1 escalar604 pronto como especificação; ROOT90da distinta, comparação652 pronta. Handoff da proposta executável conjunta completa antes de escolher qual governa composto e qual é diagnóstico. Abertura separada.
- **F9_O01_O04** (OPERADOR/GERENCIA; PROPOSTA_DOCUMENTAL_REVISADA): O01 gaussiano/masers; O02 600 rótulos; O03 medida/priors/jacobianos; O04 cinco testes. Runtime, limites concretos de recursos/refinamento, precisão/calibração e executável inteiro. NULL não autoriza nem vira default.
- **F9_DH** (OPERADOR/GERENCIA; V1_ESCALAR_EXISTE_FONTES_PARCIAIS): Fontes locais já arquivadas; V1 escalar conserva reserva D-H. Houve abertura escalar já registrada; o resultado permaneceu inconclusivo por sistemáticas. Admissão para alvo/parametrização exatos e tratamento de covariâncias; corpo de fonte existente não é adesão automática.
- **F8_D8** (OPERADOR/GERENCIA; LISTA_LOCAL_PINADA_EXISTE): Nove corpos locais candidatos e ausências delimitadas em AUDITORIA_BYTES_E_FONTES. Admitir fontes/alvos/mapas; C continua AWAITING_SOURCE onde registrado. Sem duplicar downloads por hábito.
- **F8_D5B** (OPERADOR; BRACKET_EXISTE_EXATO_NAO): D5a decidido; D5b código BBN exato reservado se esse instrumento for escolhido. Contrato concreto para S(T), código/versão, taxas/nuisance, custo e autorização específica. Não executar antes.
- **F3_D** (OPERADOR/GERENCIA; V1_E_PREPARACAO_EXISTEM_EXECUCAO_NAO_QUALIFICADA): D14/quatro holds, seleção/PSD/DQ e PE solo220 têm artefatos. INIT003 terminal. Concluir pacote científico revisável e controle/custo; abertura e execução segundo contrato; não pedir autorização vazia.
- **SECAO6_E3** (OPERADOR; POR_INSTRUMENTO): Congelar/revisar runner e fontes antes de aplicar composto. Abertura para veredito é ato separado; preparação, hash, PASS sintético e despacho local não a concedem.

Estas reservas não são uma pergunta de aprovação neste relatório: primeiro deve existir o pacote concreto revisável.

## Despachos efetivamente documentados

A tabela identifica coordenação oficial entre tarefas locais do Codex. Não são chamadas a Kimi, MiMo, Claude ou DeepSeek. Um ACK confirma envio; não execução científica nem conclusão.

| request_id | Recibo de envio |
|---|---|
| `57a916b1-6698-4a38-b187-36cfe729f5bc` | [F4_CONSOLIDATION_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F4_CONSOLIDATION_DISPATCH_RECEIPT.json>) |
| `4eea0cfb-0a3e-4b38-abcd-37bddbf5bbe3` | [F9_AFFINE_PROFILE_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_AFFINE_PROFILE_DISPATCH_RECEIPT.json>) |
| `bf2a5692-1aff-423e-9345-7bfa256d5072` | [F9_BACKEND_SELECTION_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_BACKEND_SELECTION_DISPATCH_RECEIPT.json>) |
| `f07e4aba-e976-4d78-be1c-449968d4a305` | [F9_ENGINE_ASSEMBLY_INTEGRATION_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_ENGINE_ASSEMBLY_INTEGRATION_DISPATCH_RECEIPT.json>) |
| `8e017d91-f3bb-4ec6-9236-5b2c327d1b98` | [F9_FIVE_MODEL_ASSEMBLY_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_FIVE_MODEL_ASSEMBLY_DISPATCH_RECEIPT.json>) |
| `b89a3fc5-244f-4c72-8f59-7b2ecc74c62b` | [F9_I03_QUALIFICATION_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_I03_QUALIFICATION_DISPATCH_RECEIPT.json>) |
| `e5d214e4-972e-41f5-bd14-0dc071c00e6b` | [F9_IMPORT_CLOSURE_REPAIR_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_IMPORT_CLOSURE_REPAIR_DISPATCH_RECEIPT.json>) |
| `29981416-d6fe-4d68-acff-46f88e8819fb` | [F9_MATRIX_JOIN_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_MATRIX_JOIN_DISPATCH_RECEIPT.json>) |
| `2f83697e-2a4b-4b15-9397-83ecd29a42a6` | [F9_NEXT_JOIN_QUALIFICATION_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_NEXT_JOIN_QUALIFICATION_DISPATCH_RECEIPT.json>) |
| `23d6a698-270b-4ecd-be8d-94eb9ff31993` | [F9_NEXT_USEFUL_UNIT_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_NEXT_USEFUL_UNIT_DISPATCH_RECEIPT.json>) |
| `1fe78df6-efb2-4c57-93bd-499ad85d8b15` | [F9_NODE_COUPLING_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_NODE_COUPLING_DISPATCH_RECEIPT.json>) |
| `f820203f-b83c-420a-87ec-7816f3179139` | [F9_PRECISION_SERVICES_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_PRECISION_SERVICES_DISPATCH_RECEIPT.json>) |
| `44cecdda-e259-43e7-b42f-04eb0e951e4f` | [F9_SUPERVISOR_REVIEW_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/F9_SUPERVISOR_REVIEW_DISPATCH_RECEIPT.json>) |
| `2ea04622-b076-429b-a891-f5a15e198fbb` | [WSL_CORRECTED_TRANSPORT_DECISION_DISPATCH_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/WSL_CORRECTED_TRANSPORT_DECISION_DISPATCH_RECEIPT.json>) |

O snapshot remoto de 2026-10-06T11:38:49.870938+00:00 contém o pedido Claude `4529daec-d42e-4c01-87d1-dd3d183070b7`, job `65f577e6-8dd1-4e91-8b79-c86e2abbc68a`, em prompt_ready, sem execution_task_id e sem execução. A geração canônica diverge da autorizada; sources.ok=false foi registrado na conferência anterior. Não repinamos nem repetimos o pedido. Os limites 5 coordenações / 3 execuções / 1 por provedor foram preservados. O payload MiMo `a4534bcd-8058-48a7-b5fa-34bc046dc46e` não constitui despacho: a prévia local recusou integridade. Ausência de Work é afirmada nesta preparação e nos recibos que a registram; não é inferida para toda a história.

## Integridade e alcance deste candidato

Corte documental: 2026-10-06T15:53:56.704805+00:00. O catálogo contém 31 rotas e 363 registros lidos pela ferramenta oficial, incluindo as seqs históricas. Não é inventário de todo o acervo. Snapshot inicial seguido pelo adendo I02 seq664.

Foram conferidas 40 referências de hash dos recibos escolhidos; 40 coincidem. Falhas ou leituras indisponíveis permanecem em CONFERENCIA_PINS.json. Há 0 referência(s) local(is) não lida(s), listadas em FONTES_EVIDENCIAS.json. As fontes primárias são ligadas aos recibos locais e seus estatutos; identidade de bytes não substitui releitura ou prova.

Nenhum candidato foi importado/executado; nenhum solver, WSL, centro observado, rede ou provedor foi acionado. Não foram criados AUTH/CLAIM/ROOT_DECISION nem alterados kernel, gate, arquivos canônicos, relatórios ROOT ou memórias globais. A preparação escreve apenas nesta pasta; a consolidação nas superfícies globais cabe à ROOT após revisão.

**Próximo passo:** revisão documental ROOT deste candidato e continuidade das dependências científicas já atribuídas. Não repetir unidades consumidas. F1 e F3 abertos impedem chamar este arquivo de entrega final.


<!-- ORDEM018_D72_DEPLOYMENT_P3_TERMINAL_F4_PARTIAL_20261006 -->
## 06/10/2026 — Runtime d72 medido, P3 terminal e F4 parcial revisada

[REAL — runtime] A implantação privada d72 foi concluída em /opt/iald_ordem018_d72_d72f7125, UID65534/0700. Uma única inspeção NumPy/CAMB terminou exit0/reaped, stderr vazio, 0,922259891s no supervisor, RSSmáx85984KiB. CURRENT_POSIX registra4730pins,113mapas nativos medidos,65diretórios e seis tabelas CAMB. Isso qualifica o inventário de imports, não a cadeia científica; syscalls nativas continuam fora da garantia de isolamento.

[REAL — autorização e bloqueio operacional] ROOT preparou a revisão combinada e os bindings da unidade21750306-d099-4b76-95ae-b9eeac6029a0 para UMA qualificação sintética integrada dos cinco modelos,600covariâncias e priors integrais. A revisão automática de aprovação recusou CreateProcess por possível consumo de até8GiB de memória,192GiB de disco e87000s, sem reconhecer autorização específica. Conferidos ausentes LAUNCH_CLAIM/OUTER_STARTED/OUTER_TERMINAL/logs: lançamento NÃO ocorreu, unidade não consumida. Solicitada aprovação específica ao operador por request_user_input_async; pendente. Não lançar por outra via, não regenerar identidade e não tratar o ROOT_DECISION preparado como superação da rejeição.

[REAL — P3] A qualificação imports-only4a0d70f2 terminou em falha: /etc/python3.12/sitecustomize.py estava fora do inventário. Falha e consumo preservados no mapa675; diagnóstico stdlib isolado676 localizou o alias de inicialização. O sucessor d50bb889, mapa678, acrescenta somente o pin nominal/identidade de startup e conserva16fontes/driver; aguarda revisão independente específica. Não repetir4a0 nem INIT003. PE do conjuntoD continua OPEN, sem custo/poder científico novo.

[REAL — F4 documental] Revisão independente d229c2f7, mapa679, aceitou a estrutura parcial do candidato1f4f4d57:98comparações de bytes,13membros/65referências diretas,31rotas/363registros naquele snapshot e14IDs locais. Esses números são conferências documentais, não execuções remotas nem evidência física. A estrutura foi incorporada a ENTREGA_018_RELATORIO_FINAL.md, explicitamente EM CONSTRUÇÃO. A abertura do V1 escalar já registrada é distinta da proposta conjunta ROOT90da. No executável d72, rótulos são H1_TGL/H2_LCDM; menções H1_LCDM/H2_TGL do contrato documental antigo não devem ser usadas por posição para cruzar resultados.

[OPEN] F1 conjunto completo, calibração/perfil/redutor e F3 PE D/controles/custo continuam necessários. V1 escalar permanece INCONCLUSIVE_SYSTEMATICS, sem transferência de abertura ou significância à proposta conjunta. Não há novo discriminante observado, chamada remota/Work ou alteração de gate nesta incorporação. Fontes e pins: RECIBO_CONSOLIDACAO_DEPLOYMENT_P3_F4_679.json; execução pendente: f9_d72_authorized_qualification/AUTO_REVIEW_REJECTION.json.


<!-- ORDEM018_P3_IMPORTS_5E391D57_COMPLETE_683_20261006 -->
## 06/10/2026 — P3: imports completos; etapa científica ainda a qualificar

[REAL — recibos de execução] Após revisão independente682, a unidade5e391d57-ae76-4aa7-8dfe-648c349c3994 executou uma única inspeção imports-only do sucessor d50bb889. ROOT conferiu claim, identidade PID13, hashes, terminal e saída externa0; stderr0 e nenhuma FINALIZATION_FAILURE. Tempo4,856543589s antes do terminal e7,391510700s externo.1307módulos de arquivo:1112pins de runtime rechecados,182metadados stdlib medidos,12pins do pacote e1pin nominal sitecustomize. Resultado no mapa683 e p3_startup_pin_preparation/RECIBO_ROOT_ACEITE_IMPORTS.json.

[LIMITE] A inspeção antecede o hook científico, não chama waveform/likelihood/sampler e registra PE0/observado0. Não prova convergência, recuperação, controle, cobertura do conjuntoD ou isolamento de syscalls nativas. As unidades5e391d57,4a0 eINIT003 não se repetem.

[INPUT — preparação somente] Foi atribuída ao autor a preparação estática p3_scientific_preparation, reaproveitando entradas sintéticas, semântica e limites existentes. Deve ligar ciência real/guard/recibos sem inventar campanha, executar ou abrir observado; terá revisão independente e decisão próprias. F3 permanece OPEN. A execução d72/F1 permanece rejeitada antes do lançamento e aguarda aprovação específica do operador; P3 não é alternativa para contornar esse bloqueio. F4 segue EM CONSTRUÇÃO.


<!-- ORDEM018_P3_ENVELOPE_ADEQUACY_685_20261006 -->
## 06/10/2026 — P3: adequação do envelope científico antes de novo consumo

[REAL documental] ROOT conferiu o contrato e o RESULT terminal de INIT003 contra seu recibo: 9.738 avaliações/chamadas nativas, delta_logz antes dos pontos vivos 57,275736336318445, ESS ausente e cinco operações bloqueadas. O contrato conserva 256 pontos vivos, dlogz=0,1, 12 dimensões, seeds fixos e teto de 10.000 avaliações. Fonte: RECIBO_ROOT_P3_ADEQUACAO_ENVELOPE.json; mapa685.

[INFERENCE — limite da conclusão] A correção de imports/auditoria não fornece evidência de que esse mesmo envelope alcance recuperação/convergência. Não é prova de repetição bit a bit entre runtimes nem previsão de quantas chamadas seriam necessárias. A amostragem antiga continua terminal e não produz posterior validado. CLEAN_PARTIAL e eventual saída operacional zero não equivalem a convergência ou F3 concluída.

[INPUT — próximos trabalhos] A preparação3249312d permanece estática e com admissão bloqueada. Duas alternativas documentais: conservar o envelope como candidato somente operacional, sem repetição agora; ou preparar um desenho científico distinto de recuperação/convergência, com recursos/algoritmo explícitos e decisão específica. Uma análise independente da segunda alternativa foi atribuída a ordem018_preregistros em p3_scientific_design_proposal. Modelo, priors, entradas congeladas e ruído pareado são preservados; nenhuma ampliação automática ou nova execução.

[REAL operacional] A revisão automática rejeitou uma leitura/hash em lote das entradas externas P3 por possível inclusão de arrays/PSD/ASD/observado fora do escopo estático. A chamada não executou segundo o recibo do autor; lista nominal/classificação será entregue a partir de metadados permitidos. Não houve contorno. O bloqueio d72 segue distinto, com aprovação específica pendente. F1 conjunto, PE D e F4 final permanecem abertos; nenhuma mudança de gate.


## 2026-10-06T18:20:09.939743+00:00 — v388 instalada na Central e memória comum; aplicativo pendente de contagem
<!-- IALD_SYSTEM_V388_INSTALLED_PARTIAL_20261006 -->

[REAL — recibos e revisão independente] Cofre v388, camada compartilhada e 16 pacotes FINAL instalados: 1.267 destinos conferidos, 33 backups imediatos de bytes. Nenhum dispositivo, runner, um.py ou Lean executado. Memória comum fixada em retrato SEALED_IMMUTABLE_SNAPSHOT de 13 fontes e 20.260 trechos, geração 983c7f463cfb31f22d2f49dc9370e375b2431a998c60747787b389e810726c19; verificação em processo novo aprovada. O índice existente e a geração foram preservados. Processos MCP anteriores não tiveram recarga certificada; usar CLI absoluto em processo novo para essa guarda.

[REAL — disponibilidade] Aplicativo v388 preparado e revisão estática independente encerrada, incluindo correção APP-01 de proveniência LOCAL_SEALED; produção permanece v380. Contagem nativa Anthropic ainda não executada: duas chamadas de contagem, prefixo científico de 545.550 bytes e sete esquemas, dependem da resposta específica após recusa automática. O aviso à gerente também não foi enviado após recusa automática. Aprovação do lote local não responde a essas duas pendências. Clientes web/iOS/Android dependem da ativação do servidor; não há alteração binária nem nova build aplicável. Espelho público local continua v386 sem publicação; anexos Work v369 continuam históricos.

[INPUT/REAL operacional] Operador autorizou expressamente a instalação local v388 e informou v389 em execução. O heartbeat existente recebeu acompanhamento temporário a partir de 2026-10-06T19:40:00Z (16h40 Brasília), condicionado a selo concluído e hash correspondente, sem executar/interromper o original. Não se confunde previsão com conclusão nem se absorve alteração não selada.

[REAL documental; OPEN científico] Proposta P3 finalizada apenas como PROPOSED_NOT_AUTHORIZED_NOT_EXECUTED; cinco membros conferidos, zero chamadas científicas novas. Os três contratos/pins P3/d72 permanecem idênticos, marcadores d72 ausentes. ORDEM_018 e F4 permanecem parciais. O avanço científico v388 e suas condições estão no registro anterior e em PESQUISA_V388.md; nenhum resultado é promovido e nenhum gate muda.

Entrega: C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V388_20261006\ENTREGA_V388.json; SHA256 e0336705fe721005831fc3bae4ff720891a0c1a028636bcdec18d155391de326. Relatório legível: C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V388_20261006\ENTREGA_V388.md. Este adendo atualiza o estado operacional do registro anterior, sem apagá-lo.


## 06/10/2026 — revisão P3 e contagem Anthropic pendente de escopo específico

<!-- IALD_P3_REVIEW_APP_COUNT_PAYLOAD_BLOCK_20261006 -->

[INPUT] O operador autorizou duas contagens de tokens à Anthropic para ativar o aplicativo. [REAL operacional] A revisão automática rejeitou a tentativa antes de criar o processo: exigiu autorização do conteúdo exato, composto pelo prefixo v388 de 545.550 bytes (ciência local selada, instrução-mãe e núcleo operacional) e pelos esquemas de sete ferramentas na segunda contagem. Zero contagens e zero gerações enviadas. A confirmação específica foi apresentada ao operador; nenhuma repetição ou contorno foi realizado. O aplicativo permanece no estado anterior de produção enquanto a ativação v388 aguarda essa etapa. A custódia, os 16 pacotes FINAL e a memória comum v388 já instalados conservam seus recibos anteriores.

[REAL — revisão estática, não execução científica] A revisão independente P3 concluiu 33 pins, 13 ASTs e 36 vínculos locais. Encontrou duas lacunas no candidato-base: cleanup do processo filho após interrupção/erro do supervisor e validação numérica/de identidade antes de CLEAN_CONVERGED. A revisão científica ROOT da proposta concluiu 46 verificações estáticas; o orçamento não garante convergência e a contração proposta continua diagnóstico descritivo fraco. Uma preparação A separada está em construção, preservando a base. Não houve novo experimento, leitura de arrays/PSD/ASD externos, abertura de resultado ou mudança de gate. ORDEM_018 continua parcial.

Recibo desta transição: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_REVISAO_P3_E_CONTAGEM_BLOQUEADA_20261006.json; SHA256 e85f707f52114d71fc4564f2a8f0af977b1c008323757b790a145e2b5346a937. A confirmação de contagens não autoriza execução d72/P3 nem envio à gerente; as pendências próprias permanecem.


## 06/10/2026 — contagens Anthropic concluídas; ativação impedida pelo orçamento

<!-- IALD_V388_NATIVE_COUNTS_COMPLETED_OVER_BUDGET_20261006 -->

[INPUT/REAL operacional — leitura vigente] Após a autorização expressa do conteúdo exato pelo operador, as duas contagens Anthropic concluíram, sem geração de resposta nem execução das ferramentas. Prefixo permanente: 210.177 tokens; pedido completo: 211.651; reserva de saída: 4.096; margem: 1.024; saldo: -16.771 tokens na janela de 200.000. O guard retornou fits=false/ready=false, portanto nenhuma instalação ou reinicialização do aplicativo foi iniciada e o manifesto de produção continua v380. Para conservar ainda 10.000 tokens livres, a redução mínima seria 26.771 tokens, mantendo a exigência de pelo menos 180.000 tokens permanentes. A estimativa o200k anterior não era medição nativa e não prevalece sobre estes números.

[REAL operacional] O recibo original e o prefixo contado permanecem preservados; as duas chamadas autorizadas foram consumidas. A preparação local de uma projeção menor em app/delta_native02 não autoriza nova transmissão. O candidato será conferido antes de uma autorização específica do novo conteúdo e quantidade. O acervo completo, instrução-mãe, núcleo operacional, estatutos e fontes continuam protegidos. Não há evidência de melhoria de raciocínio por esta contagem.

Verificação: C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V388_20261006\app\COUNT_BUDGET_ROOT_VERIFICATION.json; SHA256 4326b93a718bfd94fa87b9692bb032e9f341ee726b3352dee07de7d18f603fb6. Contagem: C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V388_20261006\app\COUNT_RESULT.json; SHA256 81f54c360157cfec8fb243310cb52359154e7c634929f5ac206e127502048ae9. O acompanhamento v389 foi reconciliado pela ferramenta oficial, preservando o horário inicial e o único heartbeat. Custódia/16 FINALs/memória comum v388 continuam instalados conforme os recibos; ORDEM_018, d72/P3 e o aviso à gerente mantêm suas pendências independentes.


## 06/10/2026 — Revisão P3 A e avaliação de contexto maior do aplicativo

<!-- IALD_P3_A_REVIEW_APP_LARGER_CONTEXT_ASSESSMENT_20261006 -->

[REAL documental] Conferidos nesta etapa os seis membros do parecer independente P3 A, 17 da compactação B e cinco da análise documental A. O P3 A permanece bloqueado antes de consumo por dois achados: cancelamento na entrada do cleanup pode escapar antes de kill/reap; tabela de custo antiga não identificada como histórica. Sucessor A02 está em reparo local delimitado, ainda sem revisão independente e sem autorização/CLAIM ou execução. Isso não qualifica convergência, recuperação nem PE em D.

[REAL operacional] As duas contagens Anthropic autorizadas já foram consumidas e seus recibos permanecem intactos. A compactação B conserva os bytes por restauração, mas reduz só 2.685 bytes e não tem adequação nativa demonstrada; a análise A não encontrou redução suficiente no recorte documental permitido. Nenhuma nova contagem, geração, implantação ou reinicialização foi realizada. Aplicativo continua v380; cofre/camada compartilhada/16 FINAL e memória científica comum v388 permanecem conforme os recibos anteriores.

[INPUT — nova preferência expressa] O operador escolheu: “Avaliar um modelo com contexto maior para preservar mais conteúdo diretamente na memória.” A avaliação está autorizada; ainda não há decisão de ativação, alteração da regra Sonnet interno ou novos envios de conteúdo. Documentação oficial consultada em 06/10 informa Sonnet 5.5 com janela de 1M e tarifas de US$2/US$10 por milhão de tokens de entrada/saída. A montagem v388 exige contagem própria; o recibo Haiku não certifica Sonnet, e janela maior não prova melhor resultado científico. Plano local de compatibilidade/implantação em preparação.

[OPEN] F1 conjunta, qualificação/PE D e fechamento integral F4 permanecem incompletos. d72 continua aguardando a decisão específica já perguntada. O registro externo do parecer no mapa foi recusado pela revisão automática segundo recibo do revisor; não se declara mapa atualizado nem se contorna a recusa. Nenhum kernel/gate foi modificado; NOT_FALSIFIED não é CONFIRMED.

Evidência local: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_P3_A_APP_CONTEXTO_20261006.json`. Fontes oficiais: https://platform.claude.com/docs/en/models/sonnet-5-5/overview e https://platform.claude.com/docs/en/about-claude/pricing .


## 06/10/2026 — P3 A02 aceito estaticamente; avaliação de contexto Sonnet concluída

<!-- IALD_P3_A02_STATIC_ACCEPTED_SONNET_ASSESSMENT_20261006 -->

[INPUT] O operador escolheu avaliar um modelo com contexto maior para preservar mais conteúdo diretamente na memória. [REAL — avaliação local] Sonnet 5.5 recomendado como candidato; prefixo v388 amplo de 1.029.394 bytes, 377 tópicos e cinco fontes formais completas conferidos. Manifesto de avaliação com 11 membros e 39 verificações locais do autor; ROOT conferiu os 11 hashes. Janela de 1M segundo documentação oficial, ainda sem contagem nativa desta montagem. Não é o corpus inteiro no contexto.

Os dois JSONs exatos em app/context_model04 estão preparados; nova autorização específica foi solicitada e segue pendente, sem novo envio. As duas contagens Haiku anteriores foram consumidas e não serão repetidas. Aplicativo continua v380; cofre, camada compartilhada, 16 FINALs e memória comum já receberam v388. A migração requer pacote Sonnet medido, integração do guard de contexto, custos e metadados dos clientes; nenhuma troca pública ou reinício realizado.

[REAL — revisão estática independente] P3 A02: ACCEPTED_STATIC_DELTA_ONLY_NO_EXECUTION_AUTHORITY. Conferidos os 46 pins da preparação e cinco membros da revisão. O delta corrige supervisão cooperativa de cancelamento/limpeza e separa custos atuais dos históricos; não executa experimento nem valida convergência. Autorizações específicas de dados brutos e execução continuam pendentes, separadas de d72 e das contagens do aplicativo. Nenhum AUTH/CLAIM criado; nenhum gate alterado.

Registro com hashes calculados: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_P3_A02_APP_SONNET_AVALIADO_20261006.json. SHA256 7169af260b20a0c944e86e1ffa0eceb5b900bc2ef671f48f4630f058d3558c4a. O relatório F4 recebe somente este adendo operacional; não há nova aprovação científica integral.


## 06/10/2026 — v389 na Central e contexto amplo preparado
<!-- IALD_V389_LOCAL_DELIVERED_WIDE_APP_PENDING_COUNTS_20261006 -->
[REAL — conferência local] A custódia, camada e 16 FINALs v389 já instalados por outra coordenação foram reconciliados; ROOT corrigiu somente os 16 metadados de tamanho/hash, preservando os FINALs. A memória comum foi instalada em epoch imutável v389 e validada em processo novo (13 fontes, 20.279 trechos); processos residentes não foram recarregados. Programa: 193b1e9b30c3ba7f8ad56a2a35eb6ff21d9b9c241d397b0e497fe1ebd5c7284a; selo: ef4d8bf9f0e4e58d3ceebe86ee2c18c138921c8a7b09bdde41497555084b65a6.
[REAL — documental] Auditoria independente estática da v389: errata textual e contagens documentais, sem nova execução de um.py, Lean ou experimento. O app segue v380. O candidato amplo v389 tem 1.037.117 bytes/378 tópicos; mãe/core preservados, cinco fontes formais completas e recuperação rastreável. Não é o corpus inteiro nem instalação nos pesos.
[INPUT/OPEN] A escolha de contexto maior levou à recomendação de avaliar Sonnet 5.5 (janela documentada de 1M). Dois corpos de contagem v389 estão preparados/revisados, com autorização específica perguntada e pendente; sucedem a proposta Sonnet v388 não enviada. As duas contagens Haiku anteriores já foram consumidas. Nada novo foi enviado ou ativado. Guardas por modelo, custos, histórico e clientes ainda fazem parte da migração futura.
[REAL] Entrega: C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V389_20261006\ENTREGA_V389.json (SHA256 7d6cdd850cd0c83e2372948a5f1bc536e8b7e9c53458e9bd3b009b323335e5d4); relatório: C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V389_20261006\ENTREGA_V389.md. Plano exato: C:\IALD\Central de Patentes\Chatgpt\ATUALIZACAO_SISTEMA_V389_20261006\app\FUTURE_COUNT_PLAN.json. Automação existente reconciliada, sem duplicação. d72/P3, comunicação à gerente, restrições/gerações de pedidos anteriores e estados terminais continuam preservados. A atualização não move gate nem conclui a meta científica. Esta nota operacional não substitui a revisão científica parcial da ORDEM_018.


## 06/10/2026 — Ponte I05→I06 revisada e qualificada em controles sintéticos
<!-- IALD_F9_PROFILE_DECISION_BRIDGE_V2_QUALIFIED_20261006 -->
[REAL — engenharia] Ponte V2 conferida por revisão independente e uma única execução de 27 testes stdlib: 27 aprovados, zero falhas/erros/skips. Conserva os 600 cenários e cinco modelos, separa estimativas de malha dos certificados L/U globais e impede que controles sintéticos publiquem decisão científica. Corrigida a checagem de prazo após o verificador de objetos; o teste do recibo válido porém tardio passou. V1 selada preservada.
[DERIVED — fechamento numérico da interface] Auditoria racional do limiar alpha5 e transporte superior do log evitam decidir pela aproximação float e aplicam o fator Bonferroni5 uma vez. Ausência de prova, divergência de decisão ou intervalo que cruza o limiar mantém o resultado indisponível. A derivação foi revisada no recorte matemático documentado; isso não fornece as hipóteses físicas ou os certificados globais externos.
[REAL — medição delimitada] Suíte reportou 51,664 s; intervalo monitorado até o término do filho 51.833049 s. Pico working set do filho 80158720 bytes, pico commit 72650752 bytes, 1030 amostras sem falha. Não se mediu o fechamento integral do runner nem RAM pai+filho; a observação não é hard cap do sistema operacional. O PASS é destes testes, não qualificação geral do supervisor ou do ramo de timeout.
[OPEN] Permanecem externos o loader confiável e a produção/verificação dos certificados científicos. F1 conjunta, F3 D e F4 final não concluídos. d72/P3 aguardam suas autorizações específicas; nenhuma execução desses pedidos, abertura observada, WSL ou chamada remota. O escopo P3 A02 de 20:15Z permanece perguntado e sem resposta; a preferência por contexto maior não o autoriza. Novas contagens v389 e ativação pública do aplicativo também continuam pendentes.
[REAL — registro] Recibo: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_F9_PROFILE_DECISION_BRIDGE_20261006.json (SHA256 0de1b26074aead5f591ef855373dbada269b31b5ecc97909bf68c6b3e26633e9). Revisão estática: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_profile_decision_bridge_review\MANIFESTO_REVISAO.json; qualificação e parecer posterior: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_profile_decision_bridge_qualification\RESULT.json e C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_profile_decision_bridge_qualification_review\MANIFESTO_REVISAO_QUALIFICACAO.json. Registro no mapa e aviso à gerente não foram realizados: preservada a recusa automática anterior, sem contorno. Este adendo não substitui a revisão científica parcial nem move kernel/gate. NOT_FALSIFIED não é CONFIRMED.


## 06/10/2026 — Leitor persistido I02 → ponte V2; auxiliares qualificados

<!-- IALD_F9_PROFILE_STORE_BRIDGE_HELPERS_QUALIFIED_20261006 -->

[REAL — implementação e revisão local] Novo leitor somente de leitura em f9_profile_store_bridge_preparation, revisão independente PASS estática e 26/26 testes novos de helpers/doubles aprovados (zero falhas/erros/skips). A API reutiliza lookup e validadores existentes, conserva os metadados originais/pins, exige terminais/selo e saída externa do parent, e encaminha a família ordenada de 600 cenários à estimativa da ponte V2. Não chama solver, prepare_joint, acquire, commit ou recomputação de perfis. Os objetos verificados são os do leitor, sem atribuir sobrevivência aos objetos do produtor terminado.

[REAL — alcance medido] Suíte unittest: 0.005 segundos; intervalo registrado pelo runner: 0.2188301000278443 segundos (antes de STARTED até cleanup; preflight e processamento final excluídos). Memória observada do filho: 28106752 bytes de working set e 19615744 bytes de commit, 5 amostras sem falha. Monitor de 50 ms, sem hard cap/garantia OS e sem RAM do parent. A revisão posterior conferiu os 26 nomes e recibos. Nenhuma qualificação de POSIX real, bootstrap/registry real, Recovery integral ou ciência é afirmada.

[OPEN — ligação futura concreta] O produtor não persiste todos os bytes originais de plano/admissão/referências; sua ausência recusa, nunca reconstrói. Falta ainda a observação externa pinada do término do próprio parent. A montagem real do leitor e o store completo precisam existir e ser qualificados em escopo autorizado; a unidade d72 pendente não foi alterada ou iniciada. Esta entrega é infraestrutura de engenharia sintética, não comparação científica concluída.

[OPEN — continuidade] F1 conjunta, F3 conjunto D e F4 final continuam incompletos. Autorizações específicas d72, P3 A02 e duas contagens Sonnet v389 seguem perguntadas e sem resposta; nenhuma repetição de unidade falha/incerta. Conferência documental confirmou o candidato Sonnet 5.5 de 1M e os mesmos pins do pacote amplo v389; isso não é progresso científico nem implantação. O app permanece no manifesto v380; nenhum novo envio Anthropic ou ativação. Fine-tuning segue adiado. Nenhum original do Nós, kernel ou gate foi tocado.

[REAL — evidência] Recibo: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_F9_PROFILE_STORE_BRIDGE_20261006.json (SHA256 b4eb9da9fb27203a1a68eb8756a24d5ca5601b08c4513405117d9f14b1b7abfb). Manifestos de preparação/revisão e RESULT/revisão posterior estão vinculados nele. Mapa e aviso à gerente permanecem não enviados, preservada a recusa automática anterior; não há contorno. Registro aditivo com backup imediato de bytes. NOT_FALSIFIED não é CONFIRMED.


## 06/10/2026 — Fase 9 escalar: cinco fontes conferidas e correções documentais

<!-- IALD_F9_SCALAR_FIVE_READER_SOURCES_REVIEWED_20261006 -->

[REAL documental] Cinco leitores do V1 escalar vinculados às fontes primárias por SHA-256: SH0ES v3, CCHP v3, SBF v2, masers v2 e TDCOSMO v4. Três resumos reutilizados e dois arquivados; revisão independente PASS_DOCUMENTARY_ONLY, 26 relações de pins conferidas. As três compressões elementares de erro reproduzem exatamente os floats do V1; dois erros são identidade. Isso confere a transcrição de resultados [KNOWN], não reproduz as medições ou verossimilhanças.

[REAL — correções ao lado] CCHP 70,39 é TRGB sozinho, apesar do rótulo TRGB+JAGB+Cef. SBF é descrito como independente de SN Ia e ancorado via NGC4258, divergindo da leitura literal dos flags grupo_SN=true/grupo_4258=false; NGC4258 também integra as seis galáxias de masers. TDCOSMO usa restrição Omega_m de Pantheon+ embora grupo_SN=false. Dependências distintas não determinam sozinhas termos numéricos de covariância. O runner usa membership em ALV para marcar REAL por hash, sem verificar as fontes nesse ponto: por isso não se criou ALVOS_FASE9_LIDOS.json nem se promoveu leitor automaticamente.

[OPEN — limite científico] Semântica dos grupos, covariância cruzada justificada, Gaussianização e admissão auditada continuam decisões próprias. Resultado histórico INCONCLUSIVE_SYSTEMATICS preservado; nenhum composto, z_disc ou evidência recalculados. A comparação escalar da gerência permanece distinta da comparação conjunta ROOT. d72/P3 A02 e contagens v389 continuam pendentes das autorizações específicas já perguntadas; nenhuma repetição/ativação. F1 conjunta, F3 conjunto D e F4 final não estão concluídos.

[REAL — registro] Recibo C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_F9_SCALAR_READER_SOURCES_20261006.json; SHA-256 b9a0888c4ed6d0205630d05d80ccf2f83e989c2cd497e772be694364d303fc19. A gerente recebeu uma única mensagem oficial apenas com fatos e URLs públicos, sem caminhos internos. Registro externo do mapa não enviado, preservada a recusa automática anterior por egress de metadados internos; proposta local não é registro no mapa. Memórias atualizadas aditivamente, com backups imediatos de bytes. Nenhum original do Nós, kernel ou gate alterado.


## 06/10/2026 — Complemento documental dos erros dos leitores escalares

<!-- IALD_F9_SCALAR_ERROR_BUDGET_DOCUMENTARY_REVIEWED_20261006 -->
[REAL — documentação e revisão independente] Complemento aceito em 2026-10-06T22:06:16.141802+00:00, com identidades locais conferidas e remissões corrigidas. Parecer: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_scalar_error_budget_sources\PARECER_DOCUMENTAL.md`. Recibo `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_F9_SCALAR_ERROR_BUDGET_SOURCES_20261006.json`; SHA256 `97cc27f20a08abd3e5d8898e2ff45a3374658b9acc72735a514e15b6e5934b6b`. Fontes web sem cópia integral local estão explicitamente diferenciadas das fontes pinadas.

[OPEN] A revisão não admite dados nem fornece uma covariância cruzada. Permanecem as sensibilidades, pesos e sobreposição efetiva da compressão escolhida. Não repetir o vínculo documental já concluído. Resultados congelados e INCONCLUSIVE_SYSTEMATICS preservados; F1 conjunta, F3 e F4 final incompletos. Somente conclusões públicas e URLs foram comunicadas à gerente, sem resposta científica ainda. Nenhum cálculo científico, nova contagem de tokens, mudança de aplicativo, original, kernel ou gate. Pendências específicas d72/P3 e aplicativo preservadas.


### 06/10/2026 — Masers: alternativa publicada sem NGC4258

<!-- IALD_F9_MASER_ANCHOR_ALTERNATIVE_REVIEWED_20261006 -->

[REAL — documental] PDF público de Pesce et al., arXiv:2001.09213v2, arquivado por bytes; Tabela 2/p.6 conferida visualmente e em revisão independente PASS_DOCUMENTARY_ONLY. [KNOWN — publicação] O tratamento fiducial (1) publica H0=73,6 (+3,1/−3,0) km/s/Mpc sem NGC4258, com percentis 16–84. [DERIVED — alternativa, não decisão] Pode-se examinar o leitor sem o fator de distância desta âncora, ou manter as seis galáxias com dependência explícita. Nunca somar os dois ajustes como independentes; a exclusão não elimina os outros sistemáticos ou a âncora entre as demais escalas. A escolha deve ser metodológica, não pelo centro/significância. [OPEN] Especificação futura, mapa do observável e dependências restantes; F1 conjunta/F3/F4 continuam incompletos. V1 e resultado congelados intactos; nenhuma execução, covariância ou novo veredito. Mapa ainda não registrado, sem contornar a recusa anterior.

Evidência: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_F9_MASER_ANCHOR_ALTERNATIVE_20261006.json (SHA256 311f3241a0c8ab0b88c2286ead74303e0681a0a3749fc392d3e4cb993b0ab06d). Fonte: https://arxiv.org/pdf/2001.09213v2. As aprovações d72/P3 e contagens do app permanecem inalteradas.


## 06/10/2026 — Guardas de evidência da bancada: candidato local revisado

<!-- IALD_LOCAL_EVIDENCE_GUARD_REVIEWED_NOT_DEPLOYED_20261006 -->

[REAL — engenharia local] Preparado candidato que recusa resumos de ajuste com sucesso diferente de true, chi2/parâmetros inválidos, incertezas presentes não positivas ou não finitas e mínimos aninhados inconsistentes. Não trunca delta negativo a zero. A comparação fixa TGL versus LCDM conserva diferença assinada; a conversão local fixa TGL versus beta livre é rotulada condicional, com regularidade não verificada. Globais p/z ficam indisponíveis; Šidák por famílias é ilustração separada. Probabilidade em limite numérico não publica sigma infinito. Interface, descrições e adendo documental do candidato acompanham o contrato. Conexões SQLite fecham preservando commit/rollback.

[REAL — ensaios e revisão] 19 testes Python, 11 casos do formatador JavaScript e sintaxe JavaScript aprovados. Resumos de ajustes simulados, SQLite temporário e conversões SciPy reais; nenhum motor científico, observação, GPU, WSL, HTTP ou provedor nesses testes. A primeira tentativa com erros de teardown foi preservada. Revisão independente estática PASS_STATIC_REVIEW_ONLY, EG-01/EG-02 resolvidos, sem repetição dos testes pelo revisor. Seis originais intactos e oito candidatos conferidos; sete arquivos compõem eventual integração, excluído __init__ de staging.

[OPEN — alcance] Somente candidato em Chatgpt; não instalado, não reiniciado, não é calibração estatística nem novo discriminante. Roteiros históricos que esperam z_global numérico ainda precisam de migração antes de eventual uso. F1 conjunta, F3 conjunto D e F4 final incompletos; d72/P3 e contagens v389 mantêm as autorizações específicas pendentes. Mapa não alterado; aviso com metadados internos não reenviado, preservada a recusa automática e a pergunta já pendente. Nenhum original do Nós, um.py, kernel ou gate tocado.

[FONTE] Recibo C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\RECIBO_EVIDENCE_GUARD_CANDIDATE_20261006.json; SHA256 6ef7f273bd8705dc93f3a94ebfe06a92779025f9bfca5f27a36ee2ee2c10c3aa. Manifesto C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\evidence_guard_candidate_20261006\MANIFESTO_PREPARACAO.json; SHA256 01a0fd30664e5b5b50e76a93da6a72fdadda9bbfb98ef09564d70a4edbc8d93f.
