[DERIVED — consolidação de evidências existentes; hipóteses OPEN preservadas]

Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

Todas as entregas MEDIDA/CRÍTICA do inventário acompanham esta peça em `evidencias/historico`, sem substituir versões anteriores. O quadro de apoio da coordenação é fonte secundária; referências primárias preservam escopo e autoria.



- A1 — Aceita: O controle não comutante não satisfaz fidelidade H2; tensor condicional não prova localidade (ENTREGA_016_A1_contrato.md, sha256 `0db3563552d35fd146b09df56bed49be9bff58f48dfda46b1d50220c915741b1`).
- C2 — Aceita: Retirada a hipótese w<2π; a necessidade a partir da isotonia permanece nomeada (RELATORIO.md, sha256 `fa4bbdc5882c997102d0c7bcee67b7a4b388af02625070d038392361da12038c`).
- C4 — Aceita: Fase escalar trivial não dá a representação induzida completa (RELATORIO.md, sha256 `8faf20c70144da0703681d05678c53c86dd6bbbd7110671422ba590fa3c66e15`).
- C5 — Rejeitada: Impossibilidade de qualquer par modular regional em Hilbert de uma partícula não decorre das fontes (RESULTS.json, sha256 `d7875ecd474c482e4bfec7a440a12c3f09a07d9ae74871d7494eed07409e7cfe`).
- C6 — Rejeitada: Resíduo alegado na crítica MiMo foi refutado; Q2 integral continua aberta (ENTREGA_016_MEDIDA_C6_auditoria_MiMo_conexao.md, sha256 `a486b4f850a017cc6528b51c22d345edee5051a8d01c28e21422ee026b070775`).
- D1′ — Aceita: Orientação det C=+1 é indispensável ao caractere de fase (ENTREGA_016_D1prime_foton.md, sha256 `5672dcec2e1e993f4f1e91b73df01c366fc51b4f2f141e1ddd243c04d87e2056`).
- D2′ — Rejeitada: Positividade do tensor clássico não promove expectativa quântica renormalizada (ENTREGA_016_D2prime_Maxwell.md, sha256 `d95b84479c6657c1a5a4460b2f95c36396c2889df7b09477a86131e792996c2d`).
- D3′ — Aceita: Fixidez sozinha não implica ausência de momento; ponte depende do conteúdo H2 (ENTREGA_016_D3prime_forma_conjugada.md, sha256 `714a6504bf33e784902dc69be61ad28bd0ee64409b83c45eb1fae372dfbbd8ed`).
- D4 — Aceita: Escalar sem massa e helicidade zero recusado pelo tipo retipado (ENTREGA_016_D4_peso_do_nome.md, sha256 `bdc8f9576cd53b7704ce60ea8496c6f650ca7f5b6721bb4d68cf00c49e08cd5d`).
- D6 — Aceita parcialmente: Crítica Kimi de grafo/controles adjudicada; nove lemas escalares posteriores não foram revisados por ela (ENTREGA_016_D6_realizacao_escalar.md, sha256 `111a50879ead226f1fbdbafc62ca53b02137f31580125fe18fcad0b19bd4c3f8`).
- D1–D3 antigos — CANCELADOS: Cancelamento expresso do 016-003-ter; usar somente D1′–D3′ (ENTREGA_016_PARTE_D_quadro_final.md, sha256 `b2e74e08bed56216ec01e9615ce93888e8556f5559b6fe4b04dfc714b05b77d8`).



A consolidação registra também colisões originais com v371 e as adaptações explícitas de módulo/namespace em P2. Elas são engenharia de integração, não lemas novos. `T20` fortalecido da bancada não é silenciosamente recontado como teorema novo do kernel canônico.

Revisão local do empacotamento: os dois pareceres e a adjudicação estão em `evidencias/REVISAO_EMPACOTAMENTO.json`, `REVISAO_DELTAS.json` e `PACKAGING_ADJUDICATION.json`. Foram reforçados o bloqueio por hash divergente, o cruzamento recibo/log/índice e o pin externo da reprodução. A alegação preliminar de ponte D6 ausente foi retirada após leitura do consumidor; o escopo comum W0/R0 e as projeções dos fluxos ficaram explícitos. Dezesseis controles sintéticos do runtime e dois de pin da reprodução passaram; não são provas físicas.

Auditoria de nomes durante a integração: os auxiliares `.eq_N` que Lean elabora para definições já importadas são listados, mas excluídos da contagem de declarações novas. A reprodução redundante de resultados de janela em `HorizonDataReuse` é substituída por import do módulo canônico, conservando seus dois consumidores adicionais. As versões originais e os diffs permanecem. A adaptação não descarrega nenhuma hipótese física.

Errata da própria consolidação: o cabeçalho de um adaptador foi escrito com `//`, que não é comentário Lean; o compilador recusou, e a cópia v3 corrige para `--`. A recusa e o diff são preservados. Um controle H2 já havia sido corretamente recusado por `Type mismatch`; o leitor textual procurava a mesma expressão com minúscula e registrou falso negativo. A comparação foi normalizada sem alterar o log nem recompilar para obter outro resultado.
