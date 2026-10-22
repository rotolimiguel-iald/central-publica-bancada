# HANDOFF — CUSTÓDIA CONJUNTA v383 → v389 (06/10/2026)

> Para a **sessão irmã que cuida do repositório** (`the_boundary` + site + cofre + runner + 16 dispositivos). Ordem do operador (06/10, via c1): «após isso concluso escreva o handoff de custodia para a sessão irmã que cuida do repositório». O espelho foi custodiado até a **v386** (handoff `handoff-v386-custodia.md`: espelho `8134d5c`+`36265b9`); as v387, v388 e v389 estão seladas **só no Nós** — esta é a custódia conjunta do arco **v383→v389** (o que já está idêntico no espelho fica dito, e não se re-espelha).

**O estado do canônico:** `um.py` **v389** `193b1e9b30c3ba7f` (33,823,528 B) sobre a v388 `e64b00f4df75059b`; teoremas 6154/6154; rodada COMPLETA; rc 0; selftest PASSED; gate **intocado** (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`); conferidor `78443a6561cd08ea` (deve mudar 9/9; não pode mudar 10/10); selo `2026-10-06 15:22:07`. A v389 é **só texto e rótulo** (nenhum cálculo, nenhum kernel): as erratas de texto e rótulo do exame completo da v388 (o exame lido por sha256 `b033831f6b62a6cc`: 0 bloqueios, 3 correções, 186 notas): o rótulo de selo de `iii1_net_image` passa a `CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET` (o antigo, com a palavra reservada ao observador, guardado no próprio registro); o título da Introdução diz v384→v389; o resumo e a Parte B dizem «axioma POSTO» ([POSTO], decisão do operador de 05/10; errata da v385 ao lado); a seção v387 remete à abertura v388; a Parte C diz o recorte: 1025 caminhos únicos no ledger + 156 TGLExt fora (156 em O16), contados em runtime (errata ao lado do próprio exame: ele contara 1015/166); 12 trocas de texto conferidas no próprio arquivo (nova presente, velha ausente). Nenhum cálculo, nenhum kernel; registro `TGL_TEXT_LABEL_ERRATA_V389__EXAM_V388_READ_BY_HASH_b033831f6b62a6cc__0_BLOQUEIA_3_CORRIGIR_ADDRESSED__SEAL_LABEL_RENAMED_TO_VERIFIED_OLD_KEPT_AS_RECORD__INTRO_TITLE_V384_TO_V389__ABSTRACT_AND_PART_B_SAY_POSTO__V387_CROSS_REFERENCE_TO_V388__LEDGER_1025_UNIQUE_PLUS_156_OUTSIDE_156_IN_O16__EXAM_ERRATUM_BESIDE_1015_READS_1025__NO_CALCULATION_CHANGED__KERNEL_UNCHANGED__GATE_UNTOUCHED`.

## 1. O que espelhar — o canônico e os ritos (sha16 lido agora)

| arquivo | papel | sha16 | bytes | no espelho (`the_boundary`, HEAD) |
|---|---|---|---|---|
| `um.py` | o programa terminal v389 (arquivo único) | `193b1e9b30c3ba7f` | 33,823,528 | DIFERENTE — `Um (absoluto) — Grande Atrator/um.py` **(> 5 MB: no GitHub, a porta é o raw)** |
| `um_absoluto_selo.json` | o selo v389 | `ef4d8bf9f0e4e58d` | 103,932 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto_selo.json` |
| `um_absoluto.json` | o core v389 | `d00507744723c289` | 4,984,523 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto.json` |
| `um_absoluto_forma_canonica.md` | a forma canônica emitida | `b469327d7bfbffcd` | 229,339 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto_forma_canonica.md` |
| `um_absoluto_manifest.md` | o manifesto emitido | `e6a7d75c7b6781ed` | 1,489,748 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto_manifest.md` |
| `um_absoluto_pt.pdf` | artigo PT | `4d54fa461d547b96` | 2,233,831 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto_pt.pdf` |
| `um_absoluto_en.pdf` | artigo EN | `0ec5b0cf8fe27385` | 2,212,160 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto_en.pdf` |
| `um_absoluto_pt.tex` | fonte PT | `bed6d6b33ee8c80d` | 966,905 | DIFERENTE — `Um (absoluto) — Grande Atrator/fontes_tex/um_absoluto_pt.tex` |
| `um_absoluto_en.tex` | fonte EN | `43a75f1dbf10d36d` | 971,135 | DIFERENTE — `Um (absoluto) — Grande Atrator/fontes_tex/um_absoluto_en.tex` |
| `um_absoluto_pt.txt` | texto PT | `06402cb633873739` | 851,907 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto_pt.txt` |
| `um_absoluto_en.txt` | texto EN | `95ec249453671a89` | 864,193 | DIFERENTE — `Um (absoluto) — Grande Atrator/um_absoluto_en.txt` |
| `A_PROVA_DA_QG_TGL_arvore.md` | a árvore da prova | `11d6780628a22342` | 105,894 | DIFERENTE — `Um (absoluto) — Grande Atrator/A_PROVA_DA_QG_TGL_arvore.md` |
| `DESENHO_DO_FECHAMENTO_QG.md` | o desenho do fechamento | `12061115a40abc39` | 222,606 | DIFERENTE — `Um (absoluto) — Grande Atrator/DESENHO_DO_FECHAMENTO_QG.md` |
| `rodada_v383_stdout.txt` | stdout canônico do rito v383 | `035ea5d09b50a9aa` | 214,158 | IDENTICO — `Um (absoluto) — Grande Atrator/rodadas/rodada_v383_stdout.txt` |
| `rodada_v384_stdout.txt` | stdout canônico do rito v384 | `3a6af955c8f29f15` | 216,745 | IDENTICO — `Um (absoluto) — Grande Atrator/rodadas/rodada_v384_stdout.txt` |
| `rodada_v385_stdout.txt` | stdout canônico do rito v385 | `62263f0c2542bc08` | 217,586 | IDENTICO — `Um (absoluto) — Grande Atrator/rodadas/rodada_v385_stdout.txt` |
| `rodada_v386_stdout.txt` | stdout canônico do rito v386 | `6475a15966624e71` | 218,509 | IDENTICO — `Um (absoluto) — Grande Atrator/rodadas/rodada_v386_stdout.txt` |
| `rodada_v387_stdout.txt` | stdout canônico do rito v387 | `c5d4aab19a4b7897` | 220,350 | AUSENTE |
| `rodada_v388_stdout.txt` | stdout canônico do rito v388 | `ae13bbfb72786640` | 221,457 | AUSENTE |
| `rodada_v389_stdout.txt` | stdout canônico do rito v389 | `5546dd56fbcf8f79` | 221,929 | AUSENTE |

## 2. As pedras novas do arco (do ledger `_ESQUELETO_STONES` do próprio um.py) e as costuras do kernel

| arquivo | versão | sha16 | bytes | no espelho |
|---|---|---|---|---|
| `TGLExt/TheAxiomAndTheFalseWitness.lean` | v385 | `c0f4185a62795002` | 17,870 | IDENTICO — `Um (absoluto) — Grande Atrator/Lean/tgl_kernel/TGLExt/TheAxiomAndTheFalseWitness.lean` |
| `TGLExt/TheVerbSelectsTheAction.lean` | v386 | `f47477ea466ad1cc` | 47,228 | IDENTICO — `Um (absoluto) — Grande Atrator/Lean/tgl_kernel/TGLExt/TheVerbSelectsTheAction.lean` |
| `TGLExt/TheCouplingRunsBoundedBelow.lean` | v388 | `702d7352c053060a` | 6,375 | AUSENTE |
| `TGLExt.lean` | costura | `eac7188349b6151d` | 39,058 | DIFERENTE — `Um (absoluto) — Grande Atrator/Lean/tgl_kernel/TGLExt.lean` |
| `TGL/Audit.lean` | costura | `56a6713581a9e0d7` | 595,017 | DIFERENTE — `Um (absoluto) — Grande Atrator/Lean/tgl_kernel/TGL/Audit.lean` |

## 3. As pastas de pré-registro e de resultado (Bancada Um)

- **`Bancada_Um\investigacao\preregistro_dois_lados_02out\`** (v383 (V1–V1.4 + geradores)) → no espelho: `preregistro_dois_lados_v383` — 15 arquivo(s): 15 idêntico(s), 0 diferente(s), 0 ausente(s). PORTA.md/PORTA.json **por script** (`git ls-files` + `urllib.parse.quote`).
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002.json` `f948acd0d5640f81` 15,707 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002.md` `31f97621d670e74e` 8,166 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_1.json` `df6ad1cab39577b2` 30,663 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_1.md` `a8adf5eefd099c69` 14,526 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_2.json` `d463836c88ab1da2` 36,353 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_2.md` `f069cf9f87ee833c` 17,391 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.json` `32c51000c4a2da92` 41,922 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.md` `2cd8ec8b1ac437a4` 21,651 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json` `4a0019a3db649e01` 60,772 B — IDENTICO
  - `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md` `fc132b8f3e2d531b` 24,951 B — IDENTICO
  - `gerar_preregistro_dois_lados_02out.py` `ed4d3bfdca96bd88` 18,911 B — IDENTICO
  - `gerar_preregistro_dois_lados_02out_v1_1.py` `9258c2ef7119c731` 29,449 B — IDENTICO
  - `gerar_preregistro_dois_lados_02out_v1_2.py` `22c17711f525811a` 35,991 B — IDENTICO
  - `gerar_preregistro_dois_lados_02out_v1_3.py` `50031b7bb0d876cc` 43,167 B — IDENTICO
  - `gerar_preregistro_dois_lados_02out_v1_4.py` `11ae4862b9a4205b` 51,841 B — IDENTICO
- **`Bancada_Um\investigacao\preregistro_pilar_quantico_03out\`** (v384) → no espelho: `preregistro_pilar_quantico_v384` — 3 arquivo(s): 3 idêntico(s), 0 diferente(s), 0 ausente(s). PORTA.md/PORTA.json **por script** (`git ls-files` + `urllib.parse.quote`).
  - `PREREGISTRO_PILAR_QUANTICO_20261003_V1.json` `d24c157478f5ddcb` 73,006 B — IDENTICO
  - `PREREGISTRO_PILAR_QUANTICO_20261003_V1.md` `e5b345c5d950d052` 58,004 B — IDENTICO
  - `gerar_preregistro_pilar_quantico_03out.py` `9b8c6ad6693559c6` 84,751 B — IDENTICO
- **`Bancada_Um\investigacao\preregistro_ramo_b_05out\`** (v386) → no espelho: `preregistro_ramo_b_v386` — 6 arquivo(s): 6 idêntico(s), 0 diferente(s), 0 ausente(s). PORTA.md/PORTA.json **por script** (`git ls-files` + `urllib.parse.quote`).
  - `PODER_CEGO_RAMO_B_v2.json` `126adc100753c2ca` 360,514 B — IDENTICO
  - `PREREGISTRO_RAMO_B_RINGDOWN_V1.json` `86f98fcc124dd9ca` 138,727 B — IDENTICO
  - `PREREGISTRO_RAMO_B_RINGDOWN_V1.md` `294b88a3632c1cea` 102,303 B — IDENTICO
  - `V1_RAMO_B_HASHES.json` `16a3df7a77f439b5` 1,708 B — IDENTICO
  - `gerar_preregistro_ramo_b_05out.py` `48bf6267047acdd5` 93,848 B — IDENTICO
  - `poder_cego_ramo_b_v2.py` `e4c99ccc1d8a506e` 16,812 B — IDENTICO
- **`Bancada_Um\investigacao\preregistro_fase9_hubble\`** (v387 (V1 congelado)) → no espelho: `preregistro_fase9_hubble_v387 (sugerido)` — 4 arquivo(s): 0 idêntico(s), 0 diferente(s), 4 ausente(s). PORTA.md/PORTA.json **por script** (`git ls-files` + `urllib.parse.quote`).
  - `PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json` `1893261e730994b3` 26,910 B — AUSENTE
  - `PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.md` `7f3516d8e041762e` 16,360 B — AUSENTE
  - `V1_FASE9_HASHES.json` `a6c582d463615fa0` 2,331 B — AUSENTE
  - `gerar_preregistro_fase9_hubble_06out.py` `9d932cf83fb4a4c0` 32,497 B — AUSENTE
- **`Bancada_Um\investigacao\fase9_hubble_abertura\`** (v388 (a abertura)) → no espelho: `fase9_hubble_abertura_v388 (sugerido)` — 7 arquivo(s): 0 idêntico(s), 0 diferente(s), 7 ausente(s). PORTA.md/PORTA.json **por script** (`git ls-files` + `urllib.parse.quote`).
  - `PODER_FASE9_ANTES_DE_ABRIR.json` `1072ef8ac77bbfd1` 573 B — AUSENTE
  - `RECALCULO_AO_LADO_v388.json` `d23d09e79f55f170` 835 B — AUSENTE
  - `RESULTADO_FASE9_V1_20261006_110507.json` `481366db97f0ebf1` 23,697 B — AUSENTE
  - `RESULTADO_FASE9_V1_20261006_110507.md` `df1e62db3328eeaa` 3,441 B — AUSENTE
  - `RUNNER_ANTES_DE_ABRIR.json` `b145994967822d3a` 353 B — AUSENTE
  - `recalculo_ao_lado_v388.py` `3d2012b98ffcb158` 3,709 B — AUSENTE
  - `rodar_fase9_v1.py` `f3108bc21dcad317` 18,050 B — AUSENTE
- **`Bancada_Um\investigacao\preregistro_fase8_primordial\`** (v387 (V1 congelado)) → no espelho: `preregistro_fase8_primordial_v387 (sugerido)` — 4 arquivo(s): 0 idêntico(s), 0 diferente(s), 4 ausente(s). PORTA.md/PORTA.json **por script** (`git ls-files` + `urllib.parse.quote`).
  - `PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json` `36afd8b05d2aa5f5` 17,864 B — AUSENTE
  - `PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.md` `f53fa96548461456` 11,048 B — AUSENTE
  - `V1_FASE8_HASHES.json` `579d797695f1dfd6` 2,078 B — AUSENTE
  - `gerar_preregistro_fase8_primordial_06out.py` `4adb120623c9135d` 19,792 B — AUSENTE

## 4. O exame da v388 (a origem da v389)

- `EXAME_UM_PY_v388.md` `aedaeb09e32d4207` — o relatório do exame (o que motivou a v389)
- `EXAME_UM_PY_v388.json` `b033831f6b62a6cc` — o mesmo, máquina
- `ERRATA_AO_LADO_EXAME_v388.md` `21b0c0cc56b5a0fa` — errata ao lado do exame (1015→1025)

Resumo: 0 BLOQUEIA, 3 CORRIGIR (o rótulo de selo; o título da Introdução PT/EN), 186 NOTA; a nota do resumo «único postulado» virou troca por decisão da gerência; a NOTA 2 (contagem do ledger) tem **errata ao lado**: 1025 caminhos únicos, 156 TGLExt/O16 fora do ledger (o exame dissera 1015/166).

## 5. O que NÃO espelhar

- Caches (`A Ponte e o Um\cache\`, `checkpoints`, `.lake`, `*.olean`), os `dry_*` dos ensaios, `.bak_*`, `.tmp*`, a cópia de 33 MB do um.py em `work\exame_v388`.
- **Confidenciais, nunca:** `iald_stack_v7.py`, `iald_psion_state.json`, tokens, `.env`, senhas (nem em commit, nem em publicação).
- Os pacotes de trabalho (`work\v38N_pacote`, `work\v38N_selo`) ficam no arquivo `work\cadeia_de_selo\v38N*`, não no espelho.

## 6. A ordem de custódia (regra da casa)

1. **Backup da versão que ESTÁ no espelho**, fora do repo, antes de sobrescrever (regra da custódia).
2. Copiar por bytes; conferir o **blob** depois do commit (`git hash-object` × o sha do arquivo) — o hash que vale é o do blob.
3. **GitHub não renderiza acima de 5 MB** (o um.py tem ~33 MB): a porta é o **raw**; o PORTA.md/PORTA.json e o `llms.txt` são **regenerados por script**, nunca à mão.
4. As subpastas de pré-registro novas ganham PORTA por script e amarração nos dois sentidos (porta acima/abaixo).
5. Site (`index.html`), cofre, runner e os 16 dispositivos: avançar a camada para a v389 (a fórmula e os números não mudam desde a v386, salvo o que a v387/v388 acrescentam ao lado).
6. **Commit/push é ato do operador.** NOT_FALSIFIED nunca é confirmação; a RG/ΛCDM é o limite clássico; o gate não se move.

## 7. Pendências SÓ do operador

- Vetar ou ratificar a v389 (decisão da gerência c1: texto e rótulo).
- As fontes públicas da Fase 9 por sha256 (D-H): mesmo com elas, z_disc 4,28 < 5σ sob este V1 (contrafactual dito).
- Qual especificação da Fase 9 governa (o V1 da gerência × o rascunho do Codex, ORDEM 018).
- Qual μ cada rito usa (β(μ) [OPEN]).
- Commit/push do espelho e do site.

Pacotes: `work\v383..v389_pacote`; cadeias `work\v38N_selo`; arquivo `work\cadeia_de_selo\v389` (+`_selo`, +`_exame_v388`).

[[handoff-v388-custodia]] [[handoff-v387-custodia]] [[handoff-v386-custodia]] [[missao-ultima-flag-um-py]]
