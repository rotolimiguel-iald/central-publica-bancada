# CÉTICO 2 — achado F7 (ORDEM 013-bis l.103, l.110, l.235): os 53 arquivos > 25 MB «fora de cache\»

Data: 22/09/2026. Bancada só-leitura; medição por script (find + sha256sum), arquivos ao lado:
`big_fora_cache_raw.tsv` (53 caminhos+bytes), `big_fora_cache_sha.tsv`, `cache_canon_sha.tsv` (59 > 25 MiB no cache de topo), `duplicatas_53.json`.

## Veredito: refutado = false (achado CONFIRMADO em número e em mecanismo). Gravidade IMPORTANTE mantida.

## Números refeitos [REAL]
- `find . -type f -size +25M ! -path "./cache/*"` em `ORDEM_013_RINGDOWN\`: **53 arquivos, 2.707.750.193 B = 2,71 GB** (bate com aud_5.txt:60 e com a ordem l.103).
- **53/53 contêm `/cache/` no caminho** (subpastas `cache` aninhadas): C7_POSTERIOR_REPRODUCTION 32 · C7_GWTC3_REPRODUCTION 17 · C7_INDEPENDENT 2 · C7_INJECTION_REPRODUCTION 2.
- sha256 contra o cache de topo: **49 duplicatas byte a byte de `cache\public\`** (releases Zenodo 17461225 etc.) + **4 duplicatas de `cache\gwosc\`** (on_source 1420877824 H1/L1 em C7_INDEPENDENT; offsource 1420873728 H1/L1 em C7_INJECTION_REPRODUCTION). **Zero sem canônico.** Exatamente o que o achado alegou.
- Mecanismo: `C7_*/reproduce.py:127-145` cria `ROOT/cache/run_<stage>_<stamp>/ORDEM_013_RINGDOWN/cache/` e **copia** (`shutil.copyfile`) os insumos externos de `--source-root` (o cache canônico) para dentro do run a cada execução. Logo: (a) as cópias são produto do próprio script, regeradas em toda rodada — removê-las **não** quebra reprodução futura (ao contrário do que o achado sugere em «movê-los quebra»: quebrar seria só para reler o run já feito, e isso o hash registrado cobre); (b) sem mudança no script, o próximo `--run` recria 2,7 GB e a aceitação de l.110 volta a falhar.
- A fonte da regra, ORDEM 013 l.299, diz «nenhum arquivo acima de 25 MB fora de `cache\`» **sem** dizer «de topo»; aud_5.txt:37 já lia «cache\ de topo», mas a 013-bis (l.103, l.110, l.235) herdou a frase ambígua. A bancada pode pagar F7 sem tocar em nada dizendo «estão em cache\».

## Ajustes ao texto proposto pelo revisor
1. Não pedir «os scripts passam a apontar para o cache canônico» — já apontam (`--source-root`). Pedir o que falta: **não deixar a cópia no run** (copiar → usar → apagar no `finally`, ou hardlink/`--source-root` lido no lugar), senão a violação renasce a cada rodada.
2. «Remover» tem de respeitar a régua do backup: hash registrado ANTES de apagar; os run_* já citados em entregas (C7 recibos) ganham o `DUPLICATAS_REMOVIDAS.json` no lugar do byte.
3. Definir `cache\` uma vez em §6 (l.235), e F7/aceitação referirem a definição.
