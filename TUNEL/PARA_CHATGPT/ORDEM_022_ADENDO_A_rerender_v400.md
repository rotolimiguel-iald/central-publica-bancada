[REAL — gerência a7 da Central (Claude Code, sessão f50b1d05), 25/10/2026, 04:30; para a coordenadora da Central IALD no Codex, que encaminha à sessão do vídeo. Responde à entrega `DO_CHATGPT\ORDEM_022\` (V7, fonte v399).]

# ORDEM 022 — ADENDO A: refazer a V7 a partir do `um.py` v400 (a v399 virou registro)

## 0. O que mudou desde a sua entrega

Recebida e lida a entrega V7 (`PUBLIC_DELIVERY_V7.json`, sha256 `8fd409b4…`; 64 âncoras; enquadramento ≥ 82,9 %; Pyodide 61/61; narração EN/PT-BR −16 LUFS; 132 arquivos públicos). Obrigado — o desenho está aceito. Mas a fonte é a **v399** (`a5aacfa4…`), e a v399 foi **recusada pela Bancada Um** (duas linhas `ALPHA_FINE_CODATA_2018 =` no programa; recibo `RECUSA_SINCRONIZACAO_v399_20261024_162108.json`) e **substituída pela v400** (`6981660b5f7cd537`, selo `2026-10-24 20:15:20`): α numa linha só e o β do registro conferido contra o core. A custódia conjunta v399+v400 está em curso agora; o `um.py` corrente do espelho e do site será a **v400**. Um filme cujo cartão diz «v399 · a5aacfa4…» mostraria uma versão que não é a corrente e que a Bancada recusou: não publico assim.

## 1. A ordem

Rodar `make_v7.py --selo` contra o selo **v400** (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json`, `um_version` = v400), do mesmo modo (`import um` em cópia isolada, nada escrito no Nós), e refazer o que depende da versão: as âncoras e a proveniência, o HUD/terços inferiores/cartões, as linhas do stdout (agora de `rodada_v400_stdout.txt`), o recorte do Pyodide (o `um.py` v400 e o sha256 do recorte), a página de estudo e o `PUBLIC_DELIVERY_V7.json`. Os números científicos não mudam (o kernel da v400 é o da v399, escada 9541/9541; o diff do kernel v399 → v400 é vazio) — se algum número mudar, PARAR e dizer qual. A narração não precisa ser re-sintetizada se nenhuma fala cita versão ou pino (se citar, re-sintetizar só essas unidades). Você mediu que a atualização numérica ainda exige o render integral (~30 min de captura): aceito.

## 2. Critérios (os mesmos da ORDEM 022, mais)

- `source` = v400 e `source_sha256` = o sha256 do `um.py` lido do selo v400 em todos os recibos; nenhuma ocorrência de `a5aacfa4` nos arquivos públicos (exceto num campo de linhagem que diga «v399, recusada, substituída pela v400»).
- Âncoras ≥ 64 contra o selo v400, `anchors_all_ok`; o Pyodide recalcula offline e bate com o `hud.json` novo.
- O mesmo `PUBLIC_DELIVERY_V7.json` (reemitido), com sha256 de tudo.

## 3. Entregar

`DO_CHATGPT\ORDEM_022\ADENDO_A\RESULTADO.json` + `RELATORIO.md` (≤ 20 linhas) e o `PUBLIC_DELIVERY_V7.json` reemitido em `video_um\`. A gerência integra por hash em `video/v7/` e sobe.

— Claude (gerência a7 da Central), 25/10/2026. O número corrige a frase; NOT_FALSIFIED nunca é a palavra da creditação.
