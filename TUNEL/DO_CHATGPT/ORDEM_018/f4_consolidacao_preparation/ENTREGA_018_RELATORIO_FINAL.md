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
