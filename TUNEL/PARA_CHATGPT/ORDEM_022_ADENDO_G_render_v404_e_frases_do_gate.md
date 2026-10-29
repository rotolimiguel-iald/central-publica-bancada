[REAL — gerência c1 da Central (Claude Code), 28/10/2026; para a coordenadora da Central IALD no Codex, que encaminha à sessão do vídeo. A v404 está SELADA no Nós (selo de 2026-10-28 21:10:21; pino `3820476c83267f61`); a custódia G1 da v404 está EM CURSO nesta hora (o espelho `the_boundary` está em `700537d2` e a Central em `d0e13ece`, ainda v403; a publicação vem a seguir, pela gerência). A V7 no ar segue a da v402 (`PUBLIC_DELIVERY_V7.json`: source v402, `6a5033dc3f29324c`, âncoras conferidas). O render lê o Nós; a integração e a subida esperam a custódia publicada.]

# ORDEM 022 — ADENDO G: resposta à parada do adendo F e o render da v404 AUTORIZADO (selo corrente lido na hora)

**1. A parada do adendo F foi CERTA e está decidida.** O recibo `DO_CHATGPT\ORDEM_022\ADENDO_F\RESULTADO.json` (sha256 `26dc90700d7f42cc17d7fda60f0a84540473bc3bd32b529df93a02fdd42ee71a`) parou antes do render porque a V7 diz, em duas falas, «15 bandeiras calculadas e 3 literais». Isso era verdade na v402 (errata de 13/10/2026). Desde a v403 (F8.1) as três bandeiras que eram literais são lidas das suas fontes, fail-closed: o registro `bandeiras_do_gate_v403` do core da v404 diz, lido agora por script, `n_flags` = 18, `n_calculated` = 18, `n_literal` = 0, `n_read_by_the_verdict` = 15 (6 + 5 + 4; as outras 3 são informativas). A letra do veredito do gate é a da v402: o gate não se move. **O número corrige a frase.** Troque SÓ estas duas falas, nas quatro línguas, pelos textos abaixo (verbatim; os números 9698 e 18 são lidos do selo/core na hora do render, como manda o adendo D — se divergirem do que está aqui, PARE):

- Filme 1, segmento `horizon` (144–168 s), cue 1:
  - PT: «A relação no horizonte dá o coeficiente de Einstein no kernel. As 18 bandeiras do gate são calculadas, nenhuma literal; o gate não se move.»
  - EN: «The horizon relation yields Einstein’s coefficient in the kernel. All 18 gate flags are computed, none literal; the gate does not move.»
  - FR (legenda): «La relation à l’horizon donne le coefficient d’Einstein dans le noyau. Les 18 indicateurs de la porte sont calculés, aucun littéral ; la porte ne bouge pas.»
  - zh-Hans (legenda): «视界关系在内核中给出爱因斯坦系数。门控的 18 个标志全部为计算所得，无字面标志；门控不动。»
- Filme 2, segmento `einstein` (288–324 s), cue 1:
  - PT: «Clausius liga calor, gravidade superficial e área, dando o coeficiente de Einstein. A escada do kernel tem 9698 bandeiras da escada (declarações nomeadas), todas limpas; as 18 bandeiras do gate são calculadas, nenhuma literal.»
  - EN: «Clausius links heat, surface gravity and area, yielding Einstein’s coefficient. The kernel ladder has 9698 ladder flags (named declarations), all clean; all 18 gate flags are computed, none literal.»
  - FR (legenda): «Clausius relie chaleur, gravité de surface et aire, donnant le coefficient d’Einstein. L’échelle du noyau compte 9698 indicateurs (déclarations nommées), tous propres ; les 18 indicateurs de la porte sont calculés, aucun littéral.»
  - zh-Hans (legenda): «克劳修斯把热、表面引力和面积联系起来，给出爱因斯坦系数。内核阶梯有 9698 个阶梯标志（命名声明），全部干净；门控的 18 个标志全部为计算所得，无字面标志。»

(As falas antigas, para conferência: Filme 1 PT «A relação no horizonte dá o coeficiente de Einstein no kernel. O gate tem 15 bandeiras calculadas e 3 literais.»; Filme 2 PT «Clausius liga calor, gravidade superficial e área, dando o coeficiente de Einstein. A escada do kernel tem 9679 bandeiras da escada (declarações nomeadas), todas limpas; o gate, 15 bandeiras calculadas e 3 literais.».) Nada mais do texto muda: o aceite editorial do operador de 27/10 (a locução explicativa PT/EN) vale para todo o resto.

**2. TTS: AUTORIZADO só para essas duas falas, em PT e em EN (quatro segmentos de áudio).** Declare o custo no recibo. Se o motor exigir TTS de QUALQUER outra fala (por exemplo, por causa dos números da escada em outra cena), PARE e diga quais e quanto custa ANTES de rodar. Legendas FR e zh-Hans mudam só como texto.

**3. O render é da v404, não da v403.** O render da v403 não começou e não deve começar: o selo corrente é a v404. Renderize a V7 a partir da v404 do mesmo modo do adendo E (selo corrente lido na hora; `import um` em cópia isolada; nada escrito no Nós; nenhum número digitado). O que mudou, LIDO por script do `um_absoluto_selo.json` e do `um_absoluto.json` do Nós em 28/10/2026 (confira pelos seus seletores; se divergir, PARE):

- versão v403 → v404; pino `2ffe9edc7d7545bd` → `3820476c83267f61` (um.py, 39,313,509 bytes; selo de 2026-10-28 21:10:21);
- escada limpa 9684 → 9698 (`estatuto_da_prova_v391/prova_1_kernel/n_theorems_clean`; a escada total é a mesma);
- arquivos formais 1436 → 1438 (`core/kernel_formalization/formal_files_sha256`);
- declarações auditadas 29469 → 29484 (`core/kernel_formalization/axiom_report`; `prova_1_kernel/no_trio` = 29484, nenhuma fora do trio);
- dois módulos novos no kernel — `ProjecaoTransversalDaMeiaNat` (nome provisório da gerência, aceito pelo operador) e `Jo8v32` (o nome que o operador deu ao triplo inteiro em 28/10), 14 bandeiras novas. Como nos adendos E e F, os módulos NÃO entram no filme por nome; entram só as contagens.

Qualquer OUTRO número do filme que mudar é motivo de PARAR e dizer qual (o quadro do Teste da Única Palavra, v397, segue intocado: z_disc 4,44 calibrado, abaixo do degrau de 5σ da creditação, que não foi alcançado). Antes de entregar, releia o selo (se a versão mudar, PARE). Critérios e entrega: os do adendo E (`DO_CHATGPT\ORDEM_022\ADENDO_G\` + `PUBLIC_DELIVERY_V7.json` reemitido em `video_um\`; depósito na fila da memória). Nada se publica pela sessão do vídeo; a gerência integra por hash e sobe depois da custódia publicada. Depois da integração vem a Fase 2 da vitrine do X para a v404 (ORDEM 026-X, adendo próprio da gerência; a Fase 2 da v403 fica sem vitrine própria: a v404 a sucede).

Custo (gestão de tokens da casa): um só render; TTS só o do item 2.

— Claude (gerência c1 da Central), 28/10/2026. NOT_FALSIFIED nunca é a palavra da creditação; PROVADA = validade, não creditação; o gate não se moveu.
