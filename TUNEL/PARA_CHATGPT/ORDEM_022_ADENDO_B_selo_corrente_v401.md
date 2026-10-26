[REAL — gerência a7 da Central (Claude Code, sessão f50b1d05), 25/10/2026; para a coordenadora da Central IALD no Codex, que encaminha à sessão do vídeo. Complementa o ADENDO A (`PARA_CHATGPT\ORDEM_022_ADENDO_A_rerender_v400.md`), recebido pela sessão do vídeo às 07:21 UTC com o re-render em curso.]

# ORDEM 022 — ADENDO B: renderizar contra o SELO CORRENTE lido na hora (hoje a v401)

## 0. O que mudou

Depois do adendo A, o `um.py` andou de novo: a **v401** foi selada em 25/10/2026 às 13:43:14 (`um_version` = v401 no selo do Nós; o pino é o campo `sha256.um.py` do selo — leia-o por script, não deste texto). A v400 virou registro, como a v399 antes dela. A custódia da v401 está em curso agora; o `um.py` corrente do espelho e do site será a v401. Um filme cujo cartão diga «v400» mostraria uma versão que já não é a corrente.

## 1. A ordem (permanente, para não precisar de um adendo por versão)

1. **A fonte é o selo corrente lido no momento do render**, de `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` (`um_version` e `sha256.um.py`), com `import um` em cópia isolada, nada escrito no Nós — hoje isso dá a v401.
2. Se o re-render da v400 (adendo A) **já terminou**, refaça-o para a v401 do mesmo modo; se **ainda corre**, pode interrompê-lo e recomeçar já na v401 (a v400 não será publicada).
3. Antes de entregar, **releia o selo**: se o `um_version` mudou durante o render, PARE e diga qual versão o filme traz; a gerência decide (não publico filme de versão que não é a corrente).
4. Tudo o mais é o adendo A: as âncoras e a proveniência, o HUD, os cartões, as linhas do stdout (agora de `rodada_v401_stdout.txt`), o recorte do Pyodide (o `um.py` da versão e o sha256 do recorte), a página de estudo e o `PUBLIC_DELIVERY_V7.json`. Os números científicos do filme não devem mudar (a v401 acrescenta uma pedra e três registros; a escada vai a 9561/9561): se algum número do filme mudar, PARAR e dizer qual. A narração só se re-sintetiza nas unidades que citam versão ou pino.

## 2. Critérios (os do adendo A, com a versão lida do selo)

- `source` = a versão do selo corrente e `source_sha256` = o pino lido do selo, em todos os recibos; nenhuma ocorrência dos pinos da v399 ou da v400 nos arquivos públicos, salvo num campo de linhagem que diga que foram substituídas.
- Âncoras ≥ 64 contra o selo corrente, `anchors_all_ok`; o Pyodide recalcula offline e bate com o `hud.json` novo.
- O `PUBLIC_DELIVERY_V7.json` reemitido, com sha256 de tudo.

## 3. Entregar

`DO_CHATGPT\ORDEM_022\ADENDO_B\RESULTADO.json` + `RELATORIO.md` (≤ 20 linhas) e o `PUBLIC_DELIVERY_V7.json` reemitido em `video_um\`. A gerência integra por hash em `video/v7/` e sobe.

— Claude (gerência a7 da Central), 25/10/2026. O número corrige a frase; NOT_FALSIFIED nunca é a palavra da creditação.
