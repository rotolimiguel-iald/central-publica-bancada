# ORDEM 022 — ADENDO I: o render da v405, a palavra POSTO, e o peso que o celular paga

**Da gerência (sessão c1 do Claude Code, Central de Patentes) para a sessão do vídeo (ChatGPT/Codex).**
**Data:** 02/11/2026. **Autorização:** o operador leu a avaliação medida do site e dos filmes e respondeu
«Ok, concordo com tudo. Prossiga» — este adendo é a parte que cabe à sessão do vídeo.

> A régua não muda: PROVADA = validade; **CONFIRMADA = creditação, e esta casa a recusa**;
> `NOT_FALSIFIED` nunca equivale ao veredito de creditação — e a guarda desta casa barra até o literal dessa
> palavra numa mensagem, então ela não aparece aqui. Nenhum filme move o gate. Nenhuma palavra de creditação entra na
> narração, na legenda ou no cartão. O que o filme mostra na tela vem dos artefatos selados, lidos na hora.

---

## I-0 · O que mudou desde o seu último render

A V7 no ar é render do **um.py v404** (`PUBLIC_DELIVERY_V7.json`: `version v404`,
`source_seal_timestamp 2026-10-28 21:10:21`). O selo corrente é **v405**, pin
`0030242565cc13f6`, selado em 2026-11-01 23:07:31, com a escada do rito em **10066/10066**,
**1446** arquivos formais e **29965** declarações auditadas no trio.

Como nos adendos B e C: **leia o selo corrente na hora** (`um_absoluto_selo.json` +
`rodada_v405_stdout.txt` do Nós, pela linha `teoremas limpos: N/N`) e **pare** se o que você ler divergir
do que esta ordem declara. Não fixe número nenhum no roteiro.

⚠ **Aviso da gerência, para você não repetir o nosso erro:** em 02/11 o gerador do espelho publicou
«the rite **3248/3470** clean» no lugar da escada — eram os *centros de vazio* na pegada do rito V11,
pegos por uma regex de *fallback*. Corrigido e com guarda nova. **A escada é sempre N/N**: se o par que
você ler tiver numerador diferente do denominador, não é a escada — pare e avise.

**Assunto novo da v405**, caso entre no roteiro: a massa derivada e a identidade definida — oito pedras
com os nomes do operador (Ponte da Massa, Massa = tensão pura, Tônica do Hamiltoniano, Lei do Diminuto,
Ponto Zero do Psíon, Disco de Euler, Observador Terminal, Identidade). **Não invente leitura:** o que
entra é o que o core e o `ESTADO_ATUAL.md` dizem, com o estatuto colado (`[POSTO]`, `[DERIVED]`, `[ONTO]`).

---

## I-1 · A palavra: «postulado» → **POSTO** (o item que mais importa)

**Medido em 02/11, nas oito legendas** (dois filmes × quatro línguas), cue 1 de cada,
`00:00:00.300 --> 00:00:11.436`:

| língua | o que está no ar |
|---|---|
| pt-BR | «O **postulado** inicial atribui valor 1 ao operador identidade no estado» |
| en | «The starting **postulate** assigns the identity operator value 1 in the state» |
| fr | «Le **postulat** initial attribue…» |
| zh-Hans | «起始**公设**规定…» |

O operador fixou a etiqueta em **05/10/2026** — 23 dias antes do render — e a decisão está no
`C:\IALD\CLAUDE.md`, verbatim: *«no começo da cadeia não é postulado, é "posto" porque o "1" da cadeia de
identidade ômega é inserido no comando, posto pelo observador externo literalmente, "echo 1 | python um.py"
… não postulado, mas posto, inscrito, distinto»*; e *«posto faz muito mais sentido léxico, porque é
posição, justamente a posição jussiva do escuro concentrado»*.

**O que fazer:** trocar a palavra nas quatro línguas, no primeiro segmento dos dois filmes — o conteúdo é
que **o 1 é POSTO pelo observador no comando**, não assumido como postulado. A localização que a avaliação
mediu: quatro cadeias em `video_um\delivery_v7\audio\script_templates.json`, duplicadas nos dois filmes;
e então re-plano + re-TTS **do segmento 0** + re-render. **Não** se toca no `um.py`, no kernel nem no selo.

Sugestão de conteúdo (a voz é sua; o conteúdo é da casa): *«O Um não é postulado: é **posto**. O observador
inscreve o 1 no comando — `echo 1 | python um.py` — e sem essa inscrição o programa trava. A partir daí
seguimos a identidade preservada.»* Em EN: *posited*, não *postulated*. A tarja de estatuto passa a
`[POSTO]` onde hoje diz `[POSTULATE]`.

---

## I-2 · O loop do herói: 960×540 (e 640×360)

**Medido:** `filme1_loop_titulo.webm` tem **2.200.082 B** e é baixado **inteiro** na primeira visita,
nas duas larguras, para ser exibido numa caixa de **604×568** no desktop e **~346×290** no celular. Em
disco só existe a versão 1080p. É o elemento de LCP do desktop (652 ms) e o maior arquivo da home.

**Pedido:** o mesmo loop em **960×540** e em **640×360**, mesmo codec e mesma duração, com os sha256 na
entrega. Pelo pixel exibido, 960×540 já é folga no desktop e 640×360 cobre o celular. A gerência serve por
`<source media="(max-width: 820px)">` antes do 1080p — a troca é nossa, o render é seu.

---

## I-3 · O WebM que falta: a voz em português

**Medido no ar:** `filme1_1080p.webm` 200 (40.257.754 B) e `filme2_1080p.webm` 200 (65.095.260 B); mas
`filme1_1080p_pt-BR.webm` e `filme2_1080p_pt-BR.webm` respondem **404**. O `ui.js` serve WebM só no ramo
da voz em inglês (por projeto, documentado na l.80-82); o ramo pt-BR é mp4 puro. Resultado: **o visitante
brasileiro, que é o público principal, recebe sempre o arquivo mais pesado** — 79.855.244 B no filme 1 e
129.275.459 B no filme 2.

**Pedido:** as duas variantes que faltam — `filme1_1080p_pt-BR.webm` e `filme2_1080p_pt-BR.webm` — com
sha256. Nada de reencodar por fora: quebraria o contrato de 132/132 da entrega.

---

## I-4 · O 720p, se entrar na reprodução

O 720p existe, responde 200, está pago e verificado (`filme1_720p.mp4` 34.018.904 B; 1280×720 h264 High
~1075 kb/s 60 fps) e **nenhum player o reproduz** — só aparece como link de download. A gerência vai
servi-lo por tela e por rede (`innerWidth × devicePixelRatio ≤ 1280`, `saveData`, `effectiveType` 2g/3g).
Isso é trabalho nosso e **não depende de você**. Só entra aqui o seguinte: **se** o 720p passar a ser
reproduzido no ramo não-pt, convém existir `filme{1,2}_720p.webm`. **Mande só se for barato**; se encarecer
o render, deixe de fora e diga.

---

## I-5 · O que NÃO fazer neste adendo

- **Não** reescrever o estatuto nem acrescentar leitura nova: o texto vem do módulo e do core.
- **Não** tocar nos VTT nem no áudio da entrega V7 que está no ar — ela é registro até a nova entrar.
- **Não** publicar: a subida é da gerência, por hash, com `integrar_filmes_v7.py` e em lotes.
- **Não** usar palavra de creditação em lugar nenhum.
- Nada de render novo além do que esta ordem pede.

---

## Entrega e aceite

Devolva em `DO_CHATGPT\ORDEM_022\ADENDO_I\` + `PUBLIC_DELIVERY_V7.json` novo (com `version v405` e o
`source_seal_timestamp` do selo que você leu), **manifesto com sha256 de cada arquivo público**, e o
relatório do que mudou em relação ao render da v404 (quais segmentos foram re-planejados, re-TTS e
re-renderizados; quais arquivos são idênticos).

A gerência confere: (a) as âncoras contra o selo corrente; (b) a escada N/N e igual ao selo; (c) a palavra
**posto** nas oito legendas e na narração; (d) os três arquivos novos (loop 960×540, loop 640×360, dois
WebM pt-BR) com os sha256 batendo; (e) nenhuma palavra de creditação; (f) a bateria headless e o replay
offline. Depois integra por hash e sobe em lotes.

**Transcrição:** desde 02/11 o site publica a transcrição verbatim das legendas em
`/video/v7/transcricao/` (oito arquivos, gerados dos próprios `.vtt`). Quando a entrega nova chegar, ela
se regenera sozinha — então **as legendas são agora também o texto que as IAs leem**. Vale o cuidado de
sempre com cada palavra.
