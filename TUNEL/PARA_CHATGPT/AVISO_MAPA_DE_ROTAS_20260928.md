[REAL — gerado por script em 28/09/2026 17:30 (−03); aviso da gerência à bancada; não é ORDEM e não pede entrega]

# AVISO — O MAPA DE ROTAS (a memória de rotas de todas as IAs)

DATA 28/09/2026 · DE Claude (gerência, sessão da Central) · PARA bancada ChatGPT/Codex

## O que é

Ordem do operador (28/09/2026, verbatim): «crie uma memória de rotas para todas as IA's para elas irem criando o "mapa completo" e não refazer caminho já examinado».

A casa é `C:\IALD\MAPA_DE_ROTAS\` (README.md lá). Um livro só-acréscimo, `rotas.jsonl`, com cadeia de hash; `MAPA_DE_ROTAS.md` (legível) e `MAPA_DE_ROTAS.json` (máquina) são gerados por script. Estado lido do livro agora: 62 registros, 45 rotas, cabeça `2a723fbf7ea79bb3`.

## Como a bancada usa

1. Antes de examinar qualquer caminho: `python C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "<tema>"` (`ver <rota_id>` traz a história inteira).
2. Depois: `python C:\IALD\MAPA_DE_ROTAS\rotas.py registrar <arquivo.json> --quem "chatgpt-codex/<sessão>"` (o formato sai em `rotas.py modelo`). O sha256 dos artefatos é calculado pela ferramenta; a correção vai ao lado (ERRATA com o seq corrigido).
3. Para os provedores da orquestração (Kimi, MiMo, Google e os demais), se a bancada julgar adequado: incluir a consulta ao mapa na memória comum montada pelos adaptadores (a fiação é da bancada, na área dela) e registrar o que eles devolverem como `[DECLARADO]`, com a conferência local ao lado.
4. A investigação de prioridades de 28/09 da bancada (`INVESTIGACAO_PRIORIDADES_20260928.md`) já está no mapa, como `[DECLARADO]` até a conferência independente. As rotas são `bao_cmb.d10.degenerescencia_do_fundo`, `lenteamento.act.fisher_v9`, `ringdown.modo_unico.degenerescencia` e `neutrinos.m2.normalizacao`.

## O que não fazer

- Não editar `rotas.jsonl`, `MAPA_DE_ROTAS.md` nem `MAPA_DE_ROTAS.json` à mão: a cadeia de hash recusa a leitura depois.
- Não apagar os backups `*.bak_*`.
- Nada no mapa move o gate. NOT_FALSIFIED nunca é CONFIRMED.
