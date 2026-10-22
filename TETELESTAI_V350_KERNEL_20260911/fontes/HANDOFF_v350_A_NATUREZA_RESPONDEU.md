# HANDOFF v350 — A NATUREZA RESPONDEU (v339→v350, RODADA COMPLETA) — para a sessão irmã (custódia `the_boundary`)

> Data: 10/09/2026 21:06 · Casa: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`
> Escriba: Claude (sessão Central de Patentes, d554e796) · Operador: Luiz Antonio Rotoli Miguel
> Régua: PROVADA = lastro suficiente e verificável; CONFIRMADA = juízo, proibido; gate NÃO se moveu; β jamais literal; hash jamais de memória; NOT_FALSIFIED nunca é CONFIRMED.
> Gerado POR SCRIPT (`handoff_v350.py`): todo hash e número abaixo foi lido do disco agora.

## 0. A ORDEM DO OPERADOR (verbatim, 10/09/2026)

> *"Concordo com tudo, era isso mesmo, reconheci todos e concordo com sua ordem tb"* (a lista dos cinco testes que aguardavam o
> instrumento) · *"prossiga"* · *"Prossiga"* · *"Siga para a rodada completa e Handoff."*

**O que foi feito:** com o instrumento instalado nesta máquina (WSL 2 + lalsuite 7.26, bilby, gwpy, camb em `/opt/lal_env`; pycbc em
`/opt/pycbc_env`), os cinco testes da lista correram, cada um como rito pré-registrado (hash antes do dado; smoke de pré-inscrição
preservado desde a v348) com resultado lido por hash pelo `um.py`. **Nenhum falsificou, nenhum confirmou, todos ganharam número.**
Três desenhos antigos foram retirados como identidade ou sem poder (o «100σ» de dezembro, v340; a busca de picos de 2025, v348; o
E_res/E_total → α² de janeiro/fevereiro, v350). Três bugs de pipeline foram autopsiados por hash e emendados por V2 pré-inscrita (a
envoltória do ringdown, v346; os priors da PE, v347; a distância do worker CAMB de maio, v349). A v350 rodou **intermediária** e depois
**COMPLETA** (sem a chave: 20:22:12→21:04:40; selo `rite_checkpoints.reading = RODADA_COMPLETA__NENHUM_RITO_REAPROVEITADO`) — **os mesmos bytes**; a custódia é da rodada completa.
**A v339 (o fecho) tinha handoff mas custódia PENDENTE: este handoff a inclui** (o espelho ainda está na v336).

## 1. A REGRA DA CUSTÓDIA: backup da versão anterior FORA do repositório, antes de sobrescrever

Espelho hoje: um.py sha16 `f1f330e24120f9be` (9,852,172 bytes; selo do espelho: `f1f330e24120f9be`). Antes de copiar, criar `C:\IALD\Artigo\the_boundary_BACKUPS\um_v336_f1f330e24120f9be\`
com TODOS os arquivos de resultado do espelho (byte a byte) + `BACKUP_MANIFEST.json` por script; conferir hash a hash; só então sobrescrever.
**Sementes v339–v349:** os `um.py.bak_*` de bytes em `Nós\` (mapa abaixo) + os stdouts; a v350 intermediária e a completa são o MESMO
`um.py` (leve os dois stdouts e as capturas por etapa).

Mapa versão → backup de bytes (sha16 conferido contra o diário): v339 → `um.py.bak_20260910_110345` · v340 → `um.py.bak_20260910_120535` · v341 → `um.py.bak_20260910_122257` · v342 → `um.py.bak_20260910_134214` · v343 → `um.py.bak_20260910_145404` · v344 → `um.py.bak_20260910_152456` · v345 → `um.py.bak_20260910_160826` · v346 → `um.py.bak_20260910_180441` · v347 → `um.py.bak_20260910_185712` · v348 → `um.py.bak_20260910_195507` · v349 → `um.py.bak_20260910_200917` · v350 → `(atual)`

## 2. O ESTADO MEDIDO `[REAL — lido do selo e do rito agora]`

| o quê | valor |
|---|---|
| **`um.py`** sha256 | `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c` |
| sha16 | **`c9fc7fa432c6cf16`** (11,626,190 bytes) |
| selo `sha256.um.py` == disco | SIM |
| teoremas limpos (`rodada_v350_stdout.txt`) | **5594/5594** (v339: 5594/5594; kernel INTOCADO desde a v339) |
| autoteste | `FAIL_CLOSED_SELFTEST_PASSED` |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| identidade | `1=1=VERDADEIRO=HAJA_LUZ` (`identity_true = True`) |
| contorno (v314+) | 8 ritos; falsificação limpa: NENHUMA ; `contorno_broken_v314 = []` — os ritos GW/eco/ringdown/PE/busca/D1/H2 estão FORA do contorno e não gateiam |
| rodada | **COMPLETA** — `rite_checkpoints`: {"switch_on": false, "reused": 0, "computed_and_saved": 0} |
| relatório de axiomas | 6657 termos; **fora do trio: 0** [] |
| capturas por etapa | `capture_stage = principal` · em disco: 11 arquivos |
| kernel em `Nós\tgl_kernel` | `TGLExt/` 671 módulos + `TGL/` 27 (Lean 4.31.0) — sem alteração desde a v339 |
| pipelines dos testes (`Nós\eco_ancorado_v1\`) | 39 arquivos; sha16 do conjunto `eba0915891f5afe3` |

**Confira antes de tudo.** Se não bater, **pare** e escreva no `DA_IRMA.md`.

## 3. O ARCO v339→v350

| versão | `um.py` sha16 | teoremas | rodada | o que entrou |
|---|---|---|---|---|
| v339 | `2de6295cdf2da077` | 5594/5594 | COMPLETA (HANDOFF_v339; custódia PENDENTE — este handoff a inclui) | o fecho: os 21 módulos restantes da bancada; erratas ao lado; matemática escrita 067–087 [DERIVED] |
| v340 | `40cf787fae8f4e1e` | 5594/5594 | intermediária | rito GW_ANGULAR_V1: o «100σ» de dezembro retirado como identidade + teto; negativo honesto; β não entra |
| v341 | `b811cd1eb3f4eb68` | 5594/5594 | intermediária | rito GW_ECHO_COUPLED_V1: amplitude do eco √β com sinal −1 vem do kernel; atraso [INPUT] (MAY); nulos por injeção |
| v342 | `1fb02a6de8bda71d` | 5594/5594 | intermediária | estimador corrigido + nulo de descasamento → INCONCLUSIVE_SYSTEMATICS; «estimador se escolhe por injeção, nunca pelo número da fonte»; o piso é físico |
| v343 | `2724e21207214537` | 5594/5594 | intermediária | correspondência colapso ↔ salto [ONTO, tipada]; lei KMS (2π/κ) como candidata; protocolo ECHO_ANCHORED_V1 pré-registrado `1e94f77689b5017e` |
| v344 | `8cec44bdbe5bb379` | 5594/5594 | intermediária | teste decisivo EXECUTADO com gwfast/IMRPhenomD (instrumento com proveniência conferida) → MAY/KMS INCONCLUSIVE_SYSTEMATICS |
| v345 | `f0a2ca985cf8a6c9` | 5594/5594 | intermediária | WSL + lalsuite: duas famílias de template (IMRPhenomXAS + SEOBNRv4), nulo de família → INCONCLUSIVE_SYSTEMATICS |
| v346 | `ee5b5c8b4fa4a396` | 5594/5594 | intermediária | RINGDOWN vs RG e lei de dephasing: V1 recusada pelo gate (autópsia: borda da grade), emenda V2 (filtro casado) → ramo GM/c³ INCONCLUSIVE_SYSTEMATICS (poder 0.18σ) |
| v347 | `1d08245f0cf0438c` | 5594/5594 | intermediária | PE bayesiana com termo de eco (bilby): V1 inconclusiva (um evento, borda do prior), emenda V2 → MAY INCONCLUSIVE_SYSTEMATICS, KMS INCONCLUSIVE_SYSTEMATICS; resposta pareada às injeções ~0 = piso do estimador |
| v348 | `d1caf3b16412919e` | 5594/5594 | intermediária | busca de ecos de longo atraso (protocolo de 2025) → NOT_FALSIFIED_UNDERPOWERED: picos a 3σ não veem √β; desenho retirado |
| v349 | `76e245bec46b9f3c` | 5594/5594 | intermediária | D1 via CAMB do canônico de maio: V1 expôs bug de distância do worker (autópsia por hash); emenda V2 → Δχ² 9.70 (D1_TENSION_2_TO_5_SIGMA), β livre -0.0171 ± 0.0075 (D1_BETA_TENSION) |
| v350 | `c9fc7fa432c6cf16` | 5594/5594 | intermediária (5594/5594) e depois **COMPLETA** — mesmos bytes | reprodução de H2 com pycbc → H2_IDENTITY_RETIRED: o «α²» de jan/fev era o quadrado do nível de ruído do gerador |

## 4. O QUE A NATUREZA RESPONDEU (vereditos do selo, lidos agora; nenhum é CONFIRMED)

| rito | veredito do selo |
|---|---|
| v340 GW angular | `TGL_GW_ANGULAR_V1__DECEMBER_100SIGMA_RETIRED_AS_CAPPED_IDENTITY__SQRT_ENVELOPE_NOT_TAUTOLOGICAL_BUT_NOISE_GIVES_SAME_VALUES__PHASE_COHERENCE_WITHIN_PS…` |
| v341 eco acoplado (MAY) | `TGL_GW_ECHO_COUPLED_V1__AMPLITUDE_SQRT_BETA_FROM_KERNEL__DELAY_LAW_MAY_2026_INPUT__INCONCLUSIVE_SYSTEMATICS__POWER_2P5_OF_5_SIGMA__TEMPLATE_MISMATCH_I…` |
| v343 eco KMS | `TGL_GW_ECHO_KMS_V1__AMPLITUDE_SQRT_BETA_FROM_KERNEL__DELAY_LAW_KMS_MODULAR_PERIOD_CANDIDATE__INCONCLUSIVE_SYSTEMATICS__POWER_3P0_OF_5_SIGMA__TEMPLATE_…` |
| v344 ancorado V1 (gwfast) | `TGL_ECHO_ANCHORED_V1__RESULT_READ_BY_HASH__INSTRUMENT_GWFAST_IMRPHENOMD__MAY_INCONCLUSIVE_SYSTEMATICS__KMS_INCONCLUSIVE_SYSTEMATICS__POWER_MAY_3P1_KMS…` |
| v345 ancorado V2 (lalsuite, 2 famílias) | `TGL_ECHO_ANCHORED_V2__RESULT_READ_BY_HASH__INSTRUMENT_LALSUITE_TWO_FAMILIES__MAY_INCONCLUSIVE_SYSTEMATICS__KMS_INCONCLUSIVE_SYSTEMATICS__POWER_MAY_3P2…` |
| v346 ringdown V2 | `TGL_RINGDOWN_DEPHASING_V2__RESULT_READ_BY_HASH__INCONCLUSIVE_SYSTEMATICS__DELTA_TAU_0P1766__BRANCH_B_PRED_M0P0194__POWER_0P2_OF_5_SIGMA__BRANCH_A_INVI…` — δτ = 0.1766 ± 0.1089; ramo B previsto -0.0194; poder 0.18σ; ramo planckiano invisível por construção |
| v347 PE com eco V2 | `TGL_ECHO_PE_V2__RESULT_READ_BY_HASH__BILBY_DYNESTY_LALSUITE__MAY_INCONCLUSIVE_SYSTEMATICS__KMS_INCONCLUSIVE_SYSTEMATICS__POWER_MAY_1P2_KMS_1P1_OF_5_SI…` — MAY a = -0.2671 ± 0.8566; KMS a = 1.0892 ± 0.8992; resposta pareada às injeções ≈ 0 (deveria ser 1): piso do estimador |
| v348 busca de longo atraso | `TGL_ECHO_SEARCH_V1__RESULT_READ_BY_HASH__NOT_FALSIFIED_UNDERPOWERED__N_ON_1_B_EXP_3P0__E_DET_0P0__LOUD_EVENTS_0__GATE_UNTOUCHED` — N_on 1 vs fundo 3.00; eficiência para √β 0.0000 |
| v349 D1 via CAMB V2 | `TGL_D1_CAMB_V2__RESULT_READ_BY_HASH__BESTFIT_D1_TENSION_2_TO_5_SIGMA__DELTA_CHI2_9P70__MCMC_D1_BETA_TENSION__BETA_M0P0171_PM_0P0075__GATE_UNTOUCHED` — Δχ² 9.70; β livre -0.0171 ± 0.0075 |
| v350 reprodução de H2 | `TGL_H2_REPRODUCTION_V1__RESULT_READ_BY_HASH__H2_IDENTITY_RETIRED__SYNTHETIC_0P0099__REAL_WHITENED_0P994__OFF_0P996__Z_VS_ALPHA2_2252P2__GATE_UNTOUCHED` — sintético 0.0099 = noise²; real branqueado 0.9937 vs fora da fonte 0.9956 |

**Estatutos:** amplitude do eco √β e sinal −1 `[REAL, kernel: Smat_reflection]`; leis do atraso MAY `[INPUT]` e KMS `[CANDIDATO]`; lei de dephasing
`[REAL na forma]` com τ★ `[INPUT]`; Kerr, PhenomD/SEOBNR/XAS, CAMB, Planck/DESI/SH0ES `[KNOWN]`; a TGL analítica por cima do CAMB `[DECLARADO]`;
atraso de 0,1–2 s e E_res/E_total → α² `[CONJECTURE, 2025/2026, retirados]`. **Cosmologia jamais vira prova matemática. Nenhum rito de
natureza move o gate.**

## 5. O QUE MUDA NO REPOSITÓRIO, AO LADO (os blocos anteriores ficam intactos)

1. **v339, o fecho** (ainda não custodiado): tudo o que o `HANDOFF_v339_O_FECHO.md` pede (bloco README «The close», ESTADO_ATUAL, ledger,
   runners, CI dos 671 módulos, `O_FECHAMENTO_ESTRUTURA.md`) — o kernel não mudou desde então; faça-o primeiro.
2. **v340–v350, a natureza responde:** onze ritos ADITIVOS no `um.py` (todos `does_not_gate_core = True`, `in_contour_roster_v314 = False`),
   cada um com protocolo pré-registrado e leitor por hash; parágrafos AO LADO no artigo PT/EN (v340–v350); a `TGLCollapseEchoCorrespondence`
   tipada (v343); os campos novos do selo (`gw_*`, `echo_*`, `ringdown_*`, `d1_camb_*`, `h2_*`).
3. **O cache de resultados é PARTE da reprodução:** os leitores lêem `cache/gw/*_RESULT.json` e `cache/d1_camb/*.json` por hash (caminho
   `../cache` relativo ao `um.py`). Sem eles o rito emite `AWAITING_RESULT_FILE` e o selo muda. **Leve os JSON (pequenos; lista abaixo)** —
   não os `.npz` de janelas (111 MB e 9 MB; regeneráveis pelos extratores a partir do `strain_cache` de maio).
4. **Os pipelines** (`Nós\eco_ancorado_v1\`: extratores, ringdown V1/V2, eco ancorado V1/V2, PE V1/V2, busca, D1 driver + worker corrigido +
   diagnóstico, H2, logs, smokes de pré-inscrição, evidência de pré-inscrição da v347) vão para `pipelines/` no espelho, com o `wsl_setup_lal.sh`
   e o `verify_wheels_pypi.py`. **O `tgl_camb_worker.py` e o `tgl_mcmc_camb_v2.py` de maio (em `projetos_pyhton\IALD`) NÃO foram alterados;
   a cópia corrigida é `tgl_camb_worker_v2fix.py`.**
5. **Erratas ditas (em nome próprio, no diário):** o carimbo do smoke da v347 sobrescrito e recuperado por mtime + hash recomputado
   (`preregistro_v347_evidencia.json`); a carga 1600 no WSL por threads BLAS; o ivw das injeções da v347 dominado por uma corrida na borda;
   o hash da emenda da v349 que carregava números da V1 (corrigido para o pré-inscrito, dito); duas paradas do índice do Atlas por formatação.

**O que a irmã altera no espelho (por script onde houver gerador; à mão só o texto novo, AO LADO):** `README.md`: bloco novo
**«Nature answers — v340→v350: five pre-registered tests, none falsified, none confirmed, three designs retired, three pipeline bugs autopsied»**
abaixo do bloco v339; `ESTADO_ATUAL.md`: versão v350, rito 5594/5594, rodada completa, os vereditos da tabela acima com estatutos; portas
regeneradas por script (inclusive `cache/` e `pipelines/`); runners repinados; `A_PROVA_DA_QG_TGL_arvore.md`, `memoria/`, stdouts v340–v350 e as
capturas para `rodadas/`. O DOI Zenodo continua o da v331 — **nova versão é ato do operador**.

## 6. O QUE LEVAR (existência e sha256 lidos agora; copiar com `rb`/`wb`)

| arquivo (em `Nós\`) | bytes | sha256 (32) |
|---|---|---|
| `um.py` | 11,626,190 | `c9fc7fa432c6cf16dadcb926ee44f6b7` |
| `um_absoluto.json` | 3,343,133 | `9b51fdd53626b9dc71b1aa7e14860727` |
| `um_absoluto_selo.json` | 50,381 | `bb5635209fb8e8dec032dc802cd05e91` |
| `um_absoluto_pt.pdf` | 1,771,011 | `23662a77e2e417abf39729a2739a447a` |
| `um_absoluto_en.pdf` | 1,739,545 | `c0b6ec5ca4bc47cffb7fd3c9952a49c7` |
| `um_absoluto_pt.txt` | 535,535 | `a1fb49ec129b0859e93eac0d60558a16` |
| `um_absoluto_en.txt` | 537,339 | `426b59afa09fb16fd096fb8ff3bea908` |
| `um_absoluto_forma_canonica.md` | 145,233 | `1621f540a2a2c459e0bda8348c64dcba` |
| `um_absoluto_manifest.md` | 991,383 | `2231b3f1a8fb708ea3d2d8e4fe95b9d0` |
| `A_PROVA_DA_QG_TGL_arvore.md` | 52,602 | `95b174ff8d3cc1c0134cde6a93cbf3e1` |
| `MEMORIA_DA_LINHAGEM.md` | 594,141 | `28a3cf99248ec57cda10a7f6a4d7f64b` |
| `DESENHO_DO_FECHAMENTO_QG.md` | 113,267 | `6d48f4253b2a5291064fb25fd6373e03` |
| `O_FECHAMENTO_ESTRUTURA.md` | 5,546 | `0539524c261320a9bde35a861ba4116b` |
| `HANDOFF_v339_O_FECHO.md` | 12,816 | `dea7efe9f25aa4faeb678cb66633f32d` |
| `rodada_v340_stdout.txt` | 190,746 | `06528c8309f32ff38cd9bd08db67724c` |
| `rodada_v341_stdout.txt` | 191,002 | `2533e80edf8c9559f127900e8f946bdd` |
| `rodada_v342_stdout.txt` | 191,037 | `7aa3928f7024f60b67e76cbbf88804ec` |
| `rodada_v343_stdout.txt` | 191,744 | `3168955269500bf67ae4b3b94380d183` |
| `rodada_v344_stdout.txt` | 191,994 | `80f86b60c1796e4f55e94cce66d8c795` |
| `rodada_v345_stdout.txt` | 192,251 | `bc4c9ca1ae5edb4571ad07178c823096` |
| `rodada_v346_stdout.txt` | 192,687 | `98a4797dce8d0146678fec8b3de9c010` |
| `rodada_v347_stdout.txt` | 193,100 | `0d43d614fa7fb8a0b9c075472ddb9086` |
| `rodada_v348_stdout.txt` | 193,277 | `08627c735ee8aa3f566cfba464661acb` |
| `rodada_v349_stdout.txt` | 193,654 | `a48d514923cb3f4e60c1d2980bc03226` |
| `rodada_v350_stdout_INTERMEDIARIA.txt` | 193,851 | `6ad2c2b765e3eceb1bb3e8c4fe34001c` |
| `rodada_v350_stdout.txt` | 192,640 | `881ae5695a117b571e86271603312898` |
| `tgl_kernel_audit_capture.txt` | 772,396 | `9619c7c0fc779b0931cb01f9735f97a3` |
| `tgl_kernel_audit_capture_selftest_restored.txt` | 772,405 | `75877c50a69bc87f05b6404d418f7034` |
| `tgl_kernel_audit_capture_selftest_tampered.txt` | 772,414 | `ccd48ea85a0ba30d40bea5c18b6c09ae` |
| `tgl_kernel_build_capture.txt` | 1,922,464 | `452ea6ee9b1d6b2e728a3bed63bf946b` |
| `tgl_kernel_build_capture_selftest_restored.txt` | 1,922,588 | `51d3f5cda57a0a757132fc4a04112da7` |
| `tgl_kernel_build_capture_selftest_tampered.txt` | 1,922,655 | `cbc3e5eaba66ea81a1c70d7dbc7283e3` |
| `tgl_kernel_probe_degenerate_capture.txt` | 890 | `c6e51d86b4f9a9a1d25722e64bce7a11` |
| `tgl_kernel_probe_finite_full_capture.txt` | 367 | `13cbfe4f09dc65e667c02a542a899c5d` |
| `tgl_kernel_probe_pp_no_optimality_capture.txt` | 489 | `256e72de22a5b52a61ac422f4b721aea` |
| `tgl_kernel_probe_prop_only_capture.txt` | 789 | `915851081e73ca0905cc3c1f63c954cc` |
| `tgl_kernel_probe_trivial_capture.txt` | 2,457 | `0650d8f8fb1048f0ddad0dd4716e933a` |

| cache de resultados (em `A Ponte e o Um\cache\`) | bytes | sha256 (32) |
|---|---|---|
| `cache/gw/ECHO_ANCHORED_V1_RESULT.json` | 362,930 | `709744d4e1d1c6d3448f0724e6b1b88a` |
| `cache/gw/ECHO_ANCHORED_V2_RESULT.json` | 364,990 | `6fd0e16ebdf4435b42d7dd154bad6ce6` |
| `cache/gw/ECHO_PE_V1_RESULT.json` | 751,503 | `b73cfffbc2301ea6112c32c04e83d2c2` |
| `cache/gw/ECHO_PE_V2_RESULT.json` | 1,693,653 | `3072349afb00ab2c50d8d7740350f666` |
| `cache/gw/ECHO_SEARCH_V1_RESULT.json` | 49,325 | `30f3f422ff67d34c57b8c09a6cc1d868` |
| `cache/gw/GWOSC_ECHO_WINDOWS_V1.manifest.json` | 104,397 | `5201e7b05cc4d5cca804b4cf3e3a3813` |
| `cache/gw/GWOSC_WINDOWS_V1.manifest.json` | 22,475 | `215b930648db9c6e967e54a4896f8185` |
| `cache/gw/H2_REPRODUCTION_V1_RESULT.json` | 148,108 | `8c7ef7a1d31af375a1e523bbdbf24a3f` |
| `cache/gw/RINGDOWN_DEPHASING_V1_RESULT.json` | 209,114 | `502c80fe2a37427e66723dabc43e5076` |
| `cache/gw/RINGDOWN_DEPHASING_V2_RESULT.json` | 247,065 | `ff15f023dd91d8c77fb003b2efd10c91` |
| `cache/d1_camb/D1_CAMB_DIAGNOSTICO.json` | 2,375 | `050a5b5b79487b1386948c0a882fa158` |
| `cache/d1_camb/D1_CAMB_RESULT.json` | 3,887 | `31691fc4aab39cf35a6cd767d5322dad` |
| `cache/d1_camb/D1_CAMB_V2_RESULT.json` | 4,176 | `9986e4b0f05a6ebe99cd0ea022f7ae21` |

Mais: `Nós\eco_ancorado_v1\` inteira (39 arquivos); `Nós\tgl_kernel\` inteira (sem `.lake/`) para `Lean\tgl_kernel\` e para o cofre
da Central (`vault\originals_copy\tgl_kernel_v350\` + `CUSTODY_MANIFEST.json` — bytes iguais aos da v339); e da Central: `memory\TGL_INDICE_VIVO.md`
(sha16 `8163f05add0cddf1`) e `memory\TGL_ATLAS.md` (sha16 `ab1ca0674b638edd`). **Não levar:** `.lake/`, os `.npz` do cache, `cache/lensing`,
backups `.bak_*`, nada de `E:\`, nenhum confidencial, nenhum dos quatro prompts, nada de `strain_cache` (dados públicos GWOSC, regeneráveis).

## 7. AS PORTAS E O QUE É DO OPERADOR

Regenerar `PORTA.md`/`PORTA.json`/`llms.txt` **por script**; aditivo; hash lido do artefato. **Commit/push, Zenodo, o site e qualquer
DECLARAÇÃO são atos do operador** — deixe staged/commitado e diga no `DA_IRMA.md` (datado) o sha16 lido do espelho, o caminho do backup e o
que entrou no README/ESTADO_ATUAL.

## 8. DEPOIS

A lista dos cinco está fechada. O que fica, dito com número: o ringdown pede ~28× mais precisão para o ramo GM/c³; a PE com primário livre não
tem poder para o eco a atrasos ≤ 2,5 períodos (o piso do estimador: fixar o primário por informação independente); o fundo comprimido lê a
TGL com β fixo a Δχ² ≈ +10 e β livre a 3,9σ de α√e, com a aproximação analítica declarada; a folha «eco» está limpa dos desenhos de 2025/2026.
**O mapa está fechado; o território é da natureza.** A gerência aguarda a ordem seguinte; nada roda sem ela.

*Cosmologia jamais vira prova matemática. O gate não se move por este documento. CONFIRMADA continua proibido.*
