# CÉTICO 1 — achado «F7 / 53 arquivos > 25 MB fora de cache\» (ORDEM 013-bis l.103 e l.235)

**Veredito: refutado=false. Gravidade mantida: IMPORTANTE.**

## Medição por script (22/09/2026, os.walk + sha256 em `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`, só leitura)
- arquivos > 25 MiB no total: 112; em `cache\` de 1º nível: 59; fora: **53** = **2.707.750.193 bytes (2,71 GB)** — confere com aud_5.txt:37 e com a ordem l.103.
- dos 53, **53 estão sob alguma subpasta chamada `cache`** (C7_POSTERIOR_REPRODUCTION 32 · C7_GWTC3_REPRODUCTION 17 · C7_INDEPENDENT 2 · C7_INJECTION_REPRODUCTION 2).
- duplicatas byte a byte do cache canônico: **49 de `cache\public`, 4 de `cache\gwosc`; 0 sem canônico**.
- origem: `C7_GWTC3_REPRODUCTION\reproduce.py`:127-134 cria `ROOT\cache\run_<stage>_<stamp>\ORDEM_013_RINGDOWN\cache\` e copia de `--source-root`/download. Logo os 53 são **saídas de rodadas já executadas** (`run_full_2026…`), não insumos: removê-los NÃO quebra reproduções futuras (o script recopia). Este ponto do revisor («movê-los quebra») está errado no sentido; o resto está certo.

## Por que a ordem induz erro
- l.103 diz «fora de `cache\`: mover para dentro de `cache\`» — inexecutável como escrito (já estão dentro de uma `cache\`) e explorável: a bancada paga F7 sem tocar nada.
- l.109 e l.235 repetem «fora de `cache\`» sem definir o nível. ORDEM 013 l.299 tem a mesma ambiguidade herdada.

## Texto FINAL (substituir l.103; e acrescentar a definição em l.109 e l.235)
Ver StructuredOutput.
