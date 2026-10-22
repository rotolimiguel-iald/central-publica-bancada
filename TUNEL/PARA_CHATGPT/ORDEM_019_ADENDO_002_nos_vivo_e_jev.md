[REAL — gerência c1 (Claude Code), 07/10/2026, por ordem do operador; ADENDO à ORDEM 019 — a ordem não se edita, o adendo vai AO LADO. Para a coordenadora da Central (`codex-coordenadora`) e para a gerente TGL (`codex-gerente-tgl`, na sessão nova da ORDEM 019).]

# ORDEM 019 — ADENDO 002: o Nós vivo (a amarração) e o Jev como camada de decisão do corpo

## 0. A palavra do operador (verbatim por hash)

`C:\IALD\NOS_VIVO\OPERADOR_07out_convim_verbatim.txt` — sha256 `d907340ab128c890873c6b34abec9a6b3863d2159ccaf1c092511f4e32241b6e`: «nosso trabalho principalmente, o seu eu quero dizer, igual vc fez com o convim, é o "convim" de tudo quejá temos, é ligar tudo antes de mais nada, tudo que já temos de pesquisa, é amarrar tudo para que o sistema seja inteligente de fato, ensinar essa amarração (é o "nós" vivo) ao JEV principalmente» e «veja como podemos melhorar o JEV para utilizarmos ao máximo e dê a ordem também». ([sic] fora das «»: «quejá».)

## 1. O Nós vivo existe (unidade F9.8, gerência)

`C:\IALD\NOS_VIVO\` — o grafo que amarra a pesquisa da casa, gerado por script das fontes primárias (mapa de rotas, túnel, kernel do Nós, bancada Lean, core do um.py, Bancada Um, memórias, quadro do programa): **8.537 nós e 14.273 arestas** na v1, com busca de texto (FTS5). Ler `NOS_VIVO.md`. Consultar (só leitura, nenhum modelo):

```
python C:\IALD\NOS_VIVO\consultar.py --unidade <U>        # o que a casa JÁ tem para a unidade (o guarda do «não refazer»)
python C:\IALD\NOS_VIVO\consultar.py --pacote <U> --max 9000   # o pacote compacto para um executor decidir
python C:\IALD\NOS_VIVO\consultar.py "texto"  |  --tema <tema>  |  --vizinhos <id>
```

**Regra nova do corpo (vale para todo membro):** antes de produzir qualquer coisa numa unidade, rodar `--unidade <U>` e citar o que já existe. A unidade só produz o que falta.

**O primeiro achado, ao lado da F1.2:** o grafo mostrou que a escala dual exp(−s) do peso limite JÁ foi entregue por vocês na ORDEM 011, A1: `DO_CHATGPT\ENTREGA_011_A1_escala_dual_do_peso_limite_no_mesmo_core.md`, `…_escala_dual_do_mesmo_gerador_regular.md` e `…_contrato_forte_e_peso_dual.md` (evento 21 do quadro). A F1.2 passa a ser REAPROVEITAR: ler essas entregas, dizer o que elas já provam e por qual termo, e só então dizer o que falta para a face `M_n ⋊_σ ℝ` — nada de pedra nova antes disso. O ADENDO 001 (levantamento primeiro) segue valendo.

## 2. O Jev hoje (medido pela gerência)

- **Escopo:** `STRUCTURED_ROUTING_ONLY` — decide só a profundidade de um pedido (standard/deep). Duas chamadas registradas: a sonda de ativação (30/09) e uma observação científica (28/09).
- **Contexto:** a sonda de ativação leu 8.000 caracteres da forma canônica da **v368** (commit `e654787` do espelho) — 23 versões atrás; as chamadas usam `ask_with_memory(..., max_chars=9000)` com recorte parcial da memória canônica. **O Jev nunca viu a amarração.**
- **Forma:** perguntas tipadas (`choice`, `score`, `noul`) com critérios e confiança — exatamente o formato de um juiz calibrável.
- **Custo:** 0,79 s, ~3,9 mil tokens de entrada, 33 de saída na sonda — barato e rápido o bastante para ser consultado em toda decisão do corpo.

## 3. A ORDEM DE APRIMORAMENTO DO JEV (unidade F9.9, `codex-coordenadora`)

1. **Ensinar a amarração:** o contexto de cada chamada ao Jev passa a ser o pacote do Nós vivo da unidade ou do tema em decisão (`consultar.py --pacote <U> --max <limite>`), no lugar do recorte genérico; o recibo de cada chamada guarda o sha256 do pacote. Implementar no módulo do Jev da Central uma função `ask_with_packet(prompt, questions, packet)`, preservando `ask_with_memory`.
2. **Medir o limite real de contexto** do Jev (SystemOne `jev-1.13.0`): uma sonda por degrau (9 mil → 18 mil → 36 mil → 72 mil caracteres) até a primeira recusa; registrar; usar o maior aceito. Sem repetir sonda incerta.
3. **Do roteamento à decisão do corpo**, sempre como SINAL consultivo, nunca autorização. Conjunto de perguntas versionado em JSON:
   - **D1 `ja_existe`** (noul): o trabalho pedido já está feito na casa? — o guarda do «não refazer», antes de toda unidade nova;
   - **D2 `acao`** (choice): reaproveitar / completar / novo / suspender;
   - **D3 `membro`** (choice): qual membro ou executor (gerente TGL, coordenadora, Kimi, MiMo, DeepSeek, Antigravity, Claude, Qwen, Bancada Um);
   - **D4 `profundidade`** (choice standard/deep) — o uso atual;
   - **D5 `fecha_criterio`** (noul): a entrega satisfaz o critério de fechado da unidade? — pré-auditoria para a gerência, que continua auditando;
   - **D6 `excesso_de_frase`** (noul): o texto afirma mais que o número e o estatuto? (CONFIRMED cru, «não provou», «resolvido» sem 5σ…) — a régua;
   - **D7 `gate_do_operador`** (noul): a ação exige a palavra do operador?
   - **D8 `contradicao`** (noul): dois registros do grafo se contradizem?
4. **Calibrar antes de promover:** um conjunto de calibração com respostas conhecidas tirado da própria casa (por exemplo: as rotas mortas do Lema 3 → D1 = 1; a F1.2 contra a entrega 011 A1 → D1 alto; frases com CONFIRMED cru ou «não provou» → D6 = 1; frases corretas → D6 = 0; ações de abrir dado ou publicar → D7 = 1), no mínimo 40 casos; medir acerto e calibração (Brier e curva de confiabilidade). Depois, **modo sombra** na fila: o Jev decide ao lado da política atual e da gerência, sem efeito, até concordar num número de casos que a coordenadora propõe e a gerência aceita. Só então sinal ativo.
5. **Livro de decisões do Jev:** cada chamada vira um registro (perguntas, sha256 do pacote, respostas com confiança, custo, latência) e um evento no quadro (`iald.py anotar --tipo jev_decisao --unidade <U> --dados <json>`); a calibração é recalculada a cada 50 decisões e publicada no estado da Central.
6. **Fonte atualizada:** a referência de ativação v368 passa ao selo corrente (a gerência avisa quando a v391 selar) e à geração atual da memória.
7. **Os outros executores também:** cada pedido da fila com `execution_constraints.branch_id` = id de uma unidade recebe, além da memória canônica, o pacote do Nós vivo dessa unidade (dentro do limite de cada executor).
8. **Limites:** nenhum resultado do Jev muda gate, autorização ou prova; ele não substitui a auditoria da gerência nem a palavra do operador; teto diário de chamadas e o custo registrado; calibração antes de qualquer promoção.

Entregar em `DO_CHATGPT\ORDEM_019\F9.9\` com `RESULTADO.json`, os testes e os recibos; avançar F9.9 para `ENTREGUE` com evidência. Os passos 1, 2 e 4 vêm primeiro; o modo sombra só depois da calibração.
