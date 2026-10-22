<!-- Cópia para a ORDEM 013-bis. ERRATA DO CRÍTICO DE COMPLETUDE (CRITICO.md), já incorporada na ordem e válida sobre este texto: (1) o limiar do LRT para 5σ unilateral na mistura ½δ₀+½χ²₁ é 25,0, não 23,9; (2) com σ_jit = 0,0228 o N a 90 % é 38, não 35 (o 35 era literal digitado); (3) UMA convenção de poder (90 %): os N sem rótulo aqui são N₅₀. Os caminhos «...\scratchpad\ordem013\bis\medir\...» são efêmeros: cada arquivo citado está nesta pasta, no mesmo caminho relativo, com o mesmo sha16 (salvo os saneados, listados em SANEADOS.json). -->

# SINTESE — O PORTAO DO PODER DA AMPLIACAO (ORDEM 013-bis, ringdown)

**Data:** 22/09/2026 · **Papel:** sintetizador da gerencia (Claude) · **Insumo:** cinco frentes A–E (medidas por script, so leitura da bancada) + reconciliacao propria.
**Regua:** o numero corrige a frase; nada fabricado; todo numero tem arquivo-fonte e sha16; NOT_FALSIFIED nunca vira CONFIRMED; a RG e o limite classico, nao um rival.
**beta em runtime:** ALPHA_FINE_CODATA_2018 × sqrt(e) = 0.012031300400803142 [REAL] (identico nas cinco frentes e na bancada).

**Decisao do operador (22/09/2026):** "concordo com tudo, com uma excecao quanto a congelar: os eventos, podemos amplia-los para alcancar o 5 sigma". Este documento e o **portao do poder** dessa ampliacao: diz, leitura a leitura e rota a rota, **quantos eventos, de que qualidade, com que dado e sob que condicao sistematica** o 5σ e alcancavel — e onde **nao** e, com o numero.

## 0. Fontes desta sintese (sha16 lidos por script)

| frente | arquivo | sha16 |
|---|---|---|
| A — poder vs N (posteriores reais) | `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir\A_poder_eventos\A_poder_eventos.json` | 1219a98f08b4e1eb |
| A — por evento | `...\A_poder_eventos\A1_por_evento.csv` | d02c185c876d6094 |
| B — catalogos e futuro | `...\B_catalogos\RENDIMENTO_E_5SIGMA.json` | 57ff7bacbe0d6085 |
| B — N5σ do catalogo | `...\B_catalogos\N5SIGMA_FROM_CATALOG.json` | 1e48703be9ff9a0f |
| C — piso sistematico | `...\C_piso_sistematico\C_piso_medicoes.json` | cfdb198d667df8f7 |
| C — sinais e catalogo | `...\C_piso_sistematico\C_piso_sinais_catalogo.json` | 92e26c7cdf3ed1f4 |
| D — realizacao unica / largura de δf̂ | `...\D_realizacao_unica\D_consolidado.json` | 225d97be61433ef5 |
| D — teste populacional | `...\D_realizacao_unica\d2_resultado.json` | d7402bae7f41da00 |
| E — instrumento e custo | `...\E_instrumento\MEDICAO_E.json` | 79b4c14add2f5268 |
| S — reconciliacao (este sintetizador) | `...\S_sintese\reconciliacao.json` (script `reconcilia.py`) | 12032689bb9723b8 |

Artefatos da bancada citados pelas frentes (so leitura, `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\`): C4_CATALOG_220.json 93bdc413130d294a · C4_CATALOG_COMBINATION.json f3d8c1959ded3efd · C5_FISHER.json 71189d65f52d3530 · C5_IMR_RECOVERY.json bda4441856c23a64 · C5_BIAS_ABLATION.json 6fd926f371e38aa7 · C5_OVERTONE_ABLATION.json 21b28ee843422f68 · C2_TRAJECTORY_RECOVERY.json 339be42bec67a48e · C1_LEITURAS.json 333a9d8b7d650aff · C4_JOINT_MODES.json 8b2e0fea734caed2 · C6_RESULTS.json 781a3741a68875eb.

## 1. Onde o dado de hoje esta (ponto de partida, NAO-CEGO)

Posteriores publicos ja vistos e ja combinados pela bancada, pela auditoria e pelas frentes: **nada aqui e teste**, e calibracao do portao.

| conjunto | z_comb R-B | R-MOD | R-RAIZ-0 | R-LIN | fonte | estatuto |
|---|---|---|---|---|---|---|
| GWTC-5.0 sel31 (filtro casado, offset comum fixo em 0) | 0,606 | 1,076 | 1,120 | 2,159 | A | [DERIVED] gaussiano, sem sistematica |
| GWTC-5.0 all33 | 0,615 | 1,097 | 1,136 | 2,190 | A | [DERIVED] |
| uniao 39 (33 + 6 so-GWTC-3, sem dupla contagem) | 0,654 | 1,167 | 1,205 | 2,322 | A | [DERIVED] |
| GWTC-3 (18 / 10 publicados) | 0,348 / 0,247 | 0,590 / 0,380 | 0,631 / 0,447 | 1,214 / 0,861 | A | [DERIVED] convencao legada |
| teto linear com os 45 O4 publicos SNR_rede ≥ 12 (fracao RD 0,509, fonte fixa) | 0,756 | 1,415 | 1,436 | 2,872 | E | [DERIVED] teto |
| tendencia com intercepto livre, sel31 (z_slope) | 0,048 | 0,158 | 0,054 | 0,100 | A (C: σ_a livre/fixo 20,5/1,63 etc.) | [DERIVED] inviavel |

Deslocamento observado (o traco dominante do dado): media ponderada δτ̂₂₂₀ = **+0,0668 ± 0,0336** nos 31 (A; C recalcula +0,0669 ± 0,0332; bancada KDE +0,072 [+0,015, +0,134]; RG no HPD 0,983) [REAL, NAO-CEGO]. Contra as predicoes com offset fixo em 0: R-B 2,59σ, R-MOD 3,06σ, R-RAIZ-0 3,11σ, R-LIN 4,15σ — o **mesmo** desvio que poe a RG a 2σ: **tensao sistematica, nao poder discriminante** (A, C). A frente C mede que o +0,07 **cresce com a largura do posterior** (Spearman 0,476, p 0,0068; c₀(σ→0) = −0,061 ± 0,068, k = +0,79 ± 0,37 por unidade de σ) e que a propria LVK o declara "biased towards positive values" (GWTC-3, sha16 9c5271fba4aaa144) e que o criterio pSEOBNR "may favor events with positive damping time deviations" (GWTC-5.0, B) [KNOWN]. **Leitura do sintetizador:** o +0,07 nao e um deslocamento fisico comum; e um nuisance c(σ) a modelar, e hoje c₀ nao separa 0 de −0,020 (0,6σ).

O unico evento com resolucao e o **GW250114** (σ(δτ̂) = 0,058, σ(δf̂) = 0,0136): z_i = 0,343 / 0,637 / 0,641 / 1,237 por leitura (A). No CSV da frente A (39 eventos) ha **1 evento com σ(δτ̂) ≤ 0,06, 1 com ≤ 0,10 e 3 com ≤ 0,15** (reconciliacao) [REAL]. A mediana do catalogo tem σ ≈ 0,24–0,25.

## 2. O PORTAO, leitura a leitura, rota a rota

Convencoes: N = numero de eventos para z = 5 (z escala com √N; valores esperados, variancia de z nao propagada); "GW250114-like" = σ(δτ̂) = 0,058; "mistura 31" = a mesma composicao de qualidade do GWTC-5.0; "mediana" = todos com σ = 0,24. Efeitos por leitura no GW250114 (C): R-B −0,0199 · R-MOD −0,0368 · R-RAIZ-0 −0,0371 · R-LIN −0,0715. **Piso sistematico comum exigido = |δ|/5:** R-B 0,0040 · R-MOD 0,0074 · R-RAIZ-0 0,0074 · R-LIN 0,0143 (C) [DERIVED]. Estatutos das leituras: R-B [DERIVED cond. relogio τ★ INPUT]; R-MOD [CONJECTURE da gerencia]; R-RAIZ-0 e R-LIN **EXCLUDED_IF_UNIVERSAL = True** na C1 (relogios v369) — so sobrevivem com particao nao-universal [INPUT do operador].

### 2.1 Rota I — posteriores publicos hoje (uniao GWTC-5.0 + GWTC-3 so-antigos)

| leitura | I-a: media com offset fixo em 0 | I-b: tendencia com intercepto livre | condicao sistematica | alcancavel quando | estatuto |
|---|---|---|---|---|---|
| R-B | z = 0,654 (39); N para 5σ = 2.277 (mistura-39) / 212 GW250114-like / 3.411 mediana | z_slope 0,067 (39); N ≈ 3,3×10⁵ | piso 0,0040 FALSO hoje: familia 0,029 (7×), QNM-sum 0,0125–0,062 (3–16×), catalogo +0,067 (17×) | **nao, com O4** (142 anos a 14,5 uteis/ano — B) | [DERIVED] |
| R-MOD | z = 1,167; N = 715 / 62 / 1.275 | z_slope 0,225; N ≈ 3,1×10⁴ | piso 0,0074 FALSO: familia 3,9×, QNM 1,7–8×, catalogo 9× | nao, com O4 (45 anos) | [DERIVED; CONJECTURE] |
| R-RAIZ-0 | z = 1,205; N = 671 / 61 / 1.064 | z_slope 0,074; N ≈ 2,7×10⁵ | piso 0,0074 FALSO (idem) | nao, com O4 (42 anos); excluida se universal | [DERIVED] |
| R-LIN | z = 2,322; N = 181 / 16 / 287 | z_slope 0,137; N ≈ 7,7×10⁴ | piso 0,0143: familia 2–7×, QNM 0,9–4×, estimador SNR40 0,58× OK — a mais proxima, ainda FALSA | nao, com O4 (11 anos); excluida se universal; lnB −8,22 no catalogo | [DERIVED] |
| R-A, R-RAIZ-EP4, R-RAIZ-REST, R-GLOBAL | z ~ 1e-41 … 0 | — | — | nunca (ln B = 0 por construcao) | [REAL lido] |

O teste de tendencia (I-b) e **inviavel em qualquer detector** para o setor 220: a alavanca e a variacao de pred_i com o spin final, e o catalogo tem spin estreito (q05/50/95 = 0,629/0,687/0,771): sd(pred) = 0,002 (R-B) a 0,007 (R-MOD) (A; C: 0,0016–0,0053 ponderado). Mesmo no CE seriam 1.083 / 101 / 870 / 254 eventos (A). O que separa o deslocamento comum nao e a alavanca de spin, e (i) massa/spin da inspiral, (ii) o nuisance c(σ), (iii) o modo 440 (efeito 4,1× o 220 no R-B: −0,082; C4_JOINT_MODES) — hoje sem informacao (δτ̂₄₄₀ do GW250114 ∈ [−0,35, +3,4]).

### 2.2 Rota II — catalogos futuros pre-registrados

**II-a O4c / GWTC-6.0** (B): O4c 28/01–18/11/2025, 68 significativos GraceDB; pSEOBNR estimado ≈ 8 (→ ≈ 39 acumulados) [DERIVED]; data do catalogo e do strain **NAO ENCONTRADA** (analogia O4a/O4b → ~mai–jun/2027). Com 39 acumulados de qualidade O4 (√(39/31) = 1,12): z = **0.68 (R-B) / 1.21 / 1.26 / 2.42** — nenhuma leitura muda de patamar. O ganho real do O4c nao esta no N do 220: esta em (a) eventos individuais de SNR alto (GW250207_115645 ja citado como "loud special event", B), (b) a calibracao c(σ) com mais pontos, (c) o modo 440 (C).

**II-b O5 (A+)** — o fator de SNR e uma **banda**, nao um numero: ×1,99 (PSD de referencia da C5, usado por A/C/E) vs ×1,56–1,79 (razao de alcance BBH, Observing Scenarios v55, usado por B) vs ×1,74–2,06 (razao BNS). Banda adotada pelo sintetizador: **1.56–2.06** [DERIVED]. Inicio de O5: **OPEN** (fim de 2027 / ate Q3-2029 / 2029 em diante — tres fontes discordam, B); duracao planejada ~3 anos; rendimento 55–83 pSEOBNR/ano (B, escala por alcance³, mesma fracao 18,5 %) [DERIVED].

| leitura | N para 5σ em O5: GW250114-like | N: mistura-31 | z ao fim de 3 anos de O5 (165–249 eventos, mistura) | anos de O5 para 5σ (B) | condicao | estatuto |
|---|---|---|---|---|---|---|
| R-B | 50–87 | 496–864 | **2.2–3.5σ** | 11,7–15,3 | piso 0,0040 (0,40 % de τ₂₂₀) | **nao em O5** [DERIVED] |
| R-MOD | 14–25 | 157–274 | 3.9–6.3σ | 3,7–4,9 | piso 0,0074 | marginal: so no topo da banda e com sistematica ×5 menor [DERIVED; CONJECTURE] |
| R-RAIZ-0 | 14–25 | 145–253 | 4.0–6.5σ | 3,4–4,5 | piso 0,0074; excluida se universal | marginal, idem [DERIVED] |
| R-LIN | 4–7 | 39–68 | 7.8–12.6σ | 0,9–1,2 | piso 0,0143 (a unica da ordem da discrepancia SEOB×Phenom atual, 1,3–5 %); excluida se universal; ja penalizada lnB −8,2 | estatisticamente sim em ~1 ano de O5; **so se a particao a mantiver viva** [DERIVED] |

Taxa de eventos GW250114-like (σ ≤ 0,06): 1 em O4a+O4b ≈ 1,45 ano-equivalente (21 pSEOBNR / 14,5 por ano) → **0,69/ano em O4**; em O5, escalando o volume por f³: **2,6–6,1/ano** → os 50–87 do R-B pedem **8–33 anos de O5** (reconciliacao) [DERIVED, cenario]. Com a mistura do catalogo o resultado e o mesmo em anos (11,7–15,3, B). **Conclusao II-b: o R-B nao fecha 5σ em O5 por contagem de eventos; fecha em ~2,2–3,5σ ao fim de O5 se a sistematica for zero — e ela nao e.**

### 2.3 Rota III — PE propria (rota b) sobre strain publico

Instrumento (E) [REAL]: lalsimulation 6.2.1 ja traz **pSEOBNRv4HM_PA** com DTau220/DOmega220/DTau440 (teste: dtau220 = −0,02 → razao de amortecimento 1,0208 vs 1,0204 esperado); bilby 2.8.2 + dynesty 3.1.0 em /opt/lal_env; pycbc 2.11.0 em /opt/pycbc_env — **nenhum ambiente tem tudo**; pyseobnr, pyRing, qnm ausentes; NRSur7dq4/SEOBNRv5 falham (LAL_DATA_PATH). Falta a cola: wrapper Bilby, pipeline de PE IMR por evento (nunca rodada na entrega), calibracao com (M, χ) **livres** (C5 fixou o remanescente: 2/240 celulas passam viés+cobertura; mistura de familias 0/24), e **uma convencao de deformacao** (tres na mesa: pSEOBNRv4HM_PA fracional no QNM 220; C7_NATIVE envoltoria do harmonico 22/44; C5 overtones compartilham Γ₂₂₀) [INPUT do operador].

Dado: 45 eventos GWTC-5.0 com SNR_rede ≥ 12 e strain publico (45/45; 39 com H1+L1; 25 com M_f ≥ 40 M☉) [REAL, GWOSC 22/09/2026]. Custo (E) [DERIVED]: PE pSEOBNRv4HM_PA 81–542 CPU-h/evento → N = 45: **3.656–24.375 CPU-h = 166–1.108 h de parede com 22 workers (7–46 dias)**; com IMRPhenomXPHM 56–375 h; ringdown-only C6-like ~1–9 CPU-h no total mas **NON_IDENTIFIABLE_SINGLE_220** (nao mede β).

| leitura | teto de poder com os 45 O4 (E, escala linear, fonte fixa) | faltam (eventos-equivalentes SNR_RD 40) | o que a rota III compra | alcancavel quando | estatuto |
|---|---|---|---|---|---|
| R-B | z_pop 0,756 | 146,5 | **nao poder** (o mesmo teto da rota I ×1,16); compra **controle de sistematica**: (M,χ) livres, convencao unica, c(SNR) por injecao, duas familias, 440 | nao com O4 | [DERIVED] |
| R-MOD | 1,415 | 39,4 | idem | nao com O4 | [DERIVED; CONJECTURE] |
| R-RAIZ-0 | 1,436 | 38,2 | idem | nao com O4 | [DERIVED] |
| R-LIN | 2,872 (5,64 so no teto irreal fracao = 1) | 7,0 | idem | nao com O4 (o teto irreal e excluido) | [DERIVED] |

**Veredito III:** a rota (b) e a rota **da condicao sistematica**, nao da estatistica. Se a ampliacao for feita, a PE propria vale como calibracao (injecoes RG em duas familias, (M,χ) livres, curva c(SNR)) e como medida do 440 — nao como N a mais.

### 2.4 Rota IV — teste populacional da largura de δf̂ (realizacao unica)

Estatuto do desenrolamento (D) [INPUT/CONJECTURE]: a GKSL fixa **so a media de ensemble** (δτ̂ = −x/(1+x), δf̂ = 0). A estatistica da realizacao unica **depende do desenrolamento**: browniano (Milburn) → δf̂ gaussiano com **sd 0,0228** (D, N = 600; bancada 0,0192 com N = 50; auditor 0,0226 com N = 1.500 — compatíveis) e δτ̂ medio −0,0059 (30 % do ensemble; bancada 38 %); Cauchy → sd 0,022 mas MAD 0,005 (sem variancia); saltos de Poisson ±π/2 → **85,7 % das realizacoes sao exatamente a RG** e 14 % outliers (MAD 0); deterministico → **sinal zero** nesta rota. Logo "a marca e um tremor de ~2 % em δf̂" vale **so** sob o browniano. sd_δf̂ e invariante a massa e a janela ≥ 6τ, escala com spin pelo envelope 0,7·√(2x)/(2Q) a ≤ 4 %, e soma em quadratura com o ruido (estavel 0,023 em SNR 20–100) (D) [DERIVED sob browniano].

| condicao | N para 5σ (LRT hierarquico, limiar 23,9; poder 50 % / 90 %) | fonte | estatuto |
|---|---|---|---|
| eventos GW250114-like (σ_δf̂ = 0,0136), σ_jit = 0,019 | **33 / 59** (A da 28 = E[z] = 5 ≈ poder 50 %) | D, A | [DERIVED sob browniano] |
| idem, σ_jit = 0,0228 (D) / 0,030 (R-RAIZ-0, R-MOD ≈ 0,031) | ≈ 20 / 35 ; 11 / 21 | D | [DERIVED] |
| idem, σ_jit = 0,010 | 241 / 406 | D | [DERIVED] |
| eventos com a precisao mediana do GWTC-5.0 (σ_δf̂ = 0,080) | 17.578 (poder 50 %) — inviavel; peso 1/σ⁴: o catalogo inteiro (31) vale 1,09 GW250114 | D | [DERIVED] |
| por σ_meas (3G-like, sem conversao SNR→σ_δf̂ nesta frente) | 0,005: 5/9 · 0,010: 16/27 · 0,020: 107/170 · 0,030: 403/671 | D | [DERIVED] |
| canal δτ̂ (largura), GW250114-like | ≳ 1,2×10³ (13,5× menos z por evento que δf̂) | D | [DERIVED] |
| desenrolamento de saltos: teste de outliers (fracao com |δf̂| > 3σ_i) | NAO CALCULADO (estatistica de mistura; pede pre-registro proprio) | D | [OPEN] |
| deterministico / R-GLOBAL / R-A / R-RAIZ-EP4 / R-RAIZ-REST / R-RAIZ-COHERENT macroscopico | sem sinal nesta rota | D | [DERIVED] |

Exploratorio NAO-CEGO nos 31 (D): var(medianas) / ⟨σ_i²⟩ = 0,99, χ² 23,1/30 (p 0,81), σ_jit MLE = 0, **limite 90 % σ_jit < 0,0243** (ha lugar para 0,019–0,023, nao ha sinal); z esperado se σ_jit = 0,019 existisse com os σ_i atuais: 1,43 — **o catalogo de hoje nao decide**. A (estimador de momentos): χ² 21,5/30, excesso −0,0016 — mesma conclusao.

Condicao sistematica da rota IV: o nulo **nao e σ_jit = 0, e σ_sys²** (espalhamento entre eventos por pipeline/inicio/modos/familia) — a calibrar por injecoes RG na mesma pipeline em duas familias; a **transferencia do jitter para o δf̂ do pSEOB e [OPEN]** (a precisao 0,0136 e do IMR completo; o pyRing da σ ≈ 0,17 no mesmo evento). Alcancavel quando: **O4 tem 1 evento GW250114-like em ~1,45 ano** → 59 pedem decadas em O4; em O5 (2,6–6,1/ano) → **10–23 anos** para 59, **6–13 anos** para 35 [DERIVED, cenario]. E o observavel de menor N, mas nao cabe em O5 sem 3G ou sem eventos muito mais precisos.

### 2.5 Rota V — 3G (ET / CE)

| leitura | 1 evento de fonte fixa (bancada Fisher): z ET / CE | N GW250114-like (A): ET / CE | N mediana (A): ET / CE | populacao 3G (B, taxas Berti/Bhagwat [KNOWN]) | quando | estatuto |
|---|---|---|---|---|---|---|
| R-B | 3,86 / 7,03 | 2,3 / 0,7 | 37 / 11 | 131 com SNR_RD ≥ 50 (~1,3 ano a 10²/ano) ou 33 com SNR_RD ≥ 100 (~3,3 anos) | ET 2035 vs "early 2040s"; CE "mid-2030s to 2040s" [DECLARADO, discordantes] | [DERIVED] cond. piso 0,0040 |
| R-MOD | 7,2 / 13,1 | 0,7 / 0,2 | 14 / 4 | 43 / 11 | idem | [DERIVED; CONJECTURE] |
| R-RAIZ-0 | 7,2 / 13,1 | 0,7 / 0,2 | 12 / 3,5 | 38 / 10 | idem | [DERIVED] |
| R-LIN | 13,9 / 25,3 | 0,2 / 0,05 | 3 / 1 | 10 / 2,6 | idem | [DERIVED] |
| largura δf̂ (rota IV em 3G) | — | 0,14 / 0,04 (A) | 8 / 1,9 (A) | σ_meas 0,005: 5–9 (D) | idem | [DERIVED sob browniano] |

Condicao sistematica em 3G: o piso continua 0,0040 (R-B): **0,40 % de τ₂₂₀ de erro coerente do modelo**; hoje a discrepancia SEOB×Phenom e 1,3–5,2 % (mesma fonte) a 9,7 % (outras fontes), QNM-sum 1,1–6,2 %, t₀ 7,5 % (so-ringdown) (C). Em 3G o problema **inverte**: a estatistica sobra, o modelo manda — o 5σ em 3G e alcancavel **so** com forma de onda validada contra NR a 0,4 % no amortecimento do 220 (ou 0,74 % / 1,43 % nas outras leituras).

### 2.6 A condicao sistematica, em uma tabela (C, razao componente/piso)

| componente (modo comum, nao encolhe com N) | valor em δτ̂ | R-B (piso 0,0040) | R-MOD/R-RAIZ-0 (0,0074) | R-LIN (0,0143) | fonte |
|---|---|---|---|---|---|
| familia SEOB×Phenom, mesma fonte, sem ruido (mediana) | 0,029 (Phenom→SEOB −0,042; SEOB→Phenom +0,013) | 7,3× | 3,9× | 2,0× | C5_IMR_RECOVERY bda4441856c23a64 |
| familia, outras fontes (cota) | ate 0,097 | 24× | 13× | 6,8× | C5_NONLINEAR_SOURCE_SUMMARY e51a7faeda45d16f |
| QNM-sum (220+440 @10M) vs IMR | +0,0125 … +0,062 | 3,2–16× | 1,7–8,4× | 0,9–4,3× | C5_BIAS_ABLATION 6fd926f371e38aa7; RECOLORED 0825d9e83c571554 |
| inicio t₀ (so-ringdown, 6M vs 10M) | +0,075 | 19× | 10× | 5,3× | C6_PYRING_START_COMPARISON 59dfef3554288c61 |
| vies do estimador SNR40 (encolhe com SNR, calibravel) | 0,0083 | 2,1× | 1,1× | 0,58× OK | C5_IMR_RECOVERY |
| vies do estimador SNR200 | 0,0011 | 0,28× OK | 0,15× OK | 0,08× OK | C5_IMR_RECOVERY |
| deslocamento do catalogo LVK | +0,067 ± 0,033 | 17× | 9× | 4,7× | C4_CATALOG_220 |
| PSD (H1/L1 vs design) | σ +7,5 %/+8,8 % — variancia, nao vies | — | — | — | C5_FISHER_EMPIRICAL 00fbe67f5aa5b382 |

**A condicao σ_sist,comum < |δ|/5 e FALSA para todas as leituras com dado e modelo de hoje** (C). A unica componente abaixo do piso e o vies do estimador em SNR_RD ≥ 200 (todas) e em SNR40 para R-LIN. Consequencia numerica: **ampliar N com o modelo atual converge para um 5σ do modelo (±0,03 a ±0,06, sinal dado pelo par natureza/modelo), nao da natureza.** O 5σ estatistico so vale se o orcamento coerente do amortecimento do 220 for demonstrado a 0,40 % (R-B), 0,74 % (R-MOD, R-RAIZ-0), 1,43 % (R-LIN) de τ₂₂₀.

## 3. Contradicoes entre frentes — resolvidas pelo numero ou declaradas abertas

1. **N para 5σ no R-B com dado O4: 150 (Fisher da bancada, SNR40) vs 212/213 (A, C) vs 2.062 (B) vs 2.108 (A) vs 3.411–3.699 (A, C).** RESOLVIDA: sao quatro populacoes diferentes. 150 = fonte fixa com σ = 0,0497 em SNR_RD 40 (otimista: SNR40 na janela de 10 tM equivale a 2,5–4,4× o GW250114, aud_4); 212 = σ real do GW250114 (0,058 ≙ SNR_RD ≈ 34; 150 × (0,058/0,0497)² = 204); 2.062–2.108 = mistura real do catalogo (B usa mean z²/evento 0,0121; A usa z_comb 0,606 — diferenca 2 %); 3.411–3.699 = todos com a mediana σ = 0,24. **Numero do portao: 212 GW250114-like ou ~2.100 de mistura O4.**
2. **SNR_RD para 5σ num so evento: ~490 (bancada) vs ~570 (B).** RESOLVIDA: mesma lei σ ∝ 1/SNR com ancoras diferentes (0,0497@40 → 501; 0,058@40 → 584). Banda 490–585.
3. **Fator de SNR do O5: ×1,99 (C5, usado por A/C/E) vs ×1,56–1,79 (alcances, B).** ABERTA como banda: adotei 1,56–2,06; N R-B GW250114-like em O5 = 50–87 (A dizia 54; C/E 39 com fonte fixa). O cronograma de O5 e OPEN (tres fontes discordam).
4. **Teto de E (45 eventos, z_pop 0,756) vs A (39 posteriores reais, 0,654).** RESOLVIDA: E e teto linear com fonte fixa e fracao RD de um unico evento; A e o dado. Razao teto/real 1,16–1,24 em todas as leituras — consistentes; o portao usa A.
5. **Fracao de eventos uteis: B (18,5 % pSEOBNR/TGR; 14,5/ano) vs A (nao assumiu taxa) vs E (45 com SNR ≥ 12).** RESOLVIDA por contagem: criterios diferentes (pSEOBNR = SNR ≥ 8 no inspiral E no pos-inspiral; E = SNR de rede). O que conta para o portao e a taxa de GW250114-like: 1 em 39 (σ ≤ 0,06) → 0,69/ano em O4 (reconciliacao). **A taxa por ano de eventos GW250114-like em O5 nao esta em nenhum artefato** — a minha (2,6–6,1/ano) e escala de volume [DERIVED, cenario].
6. **Jitter: A pede 28 eventos, D pede 33/59.** RESOLVIDA: 28 = E[z] = 5 (≈ poder 50 %); D calcula poder por MC: 33 (50 %) / 59 (90 %). O pre-registro usa 90 %: **59 (σ_jit 0,019) ou 35 (0,0228)**. Os tres valores de σ_jit (0,0192 / 0,0228 / 0,0226) sao compatíveis (N = 50 na bancada).
7. **Intercepto livre: A usa constante; C mostra que o +0,07 cresce com σ (k = +0,79 ± 0,37).** RESOLVIDA a favor de C: o nuisance certo e c(σ) = c₀ + k·σ; A e C concordam que o teste de tendencia e inviavel (N ≥ 3×10⁴).
8. **Transferencia do jitter ao δf̂ do pSEOB: A assume integral; D declara [OPEN].** ABERTA: os N da rota IV sao limites inferiores ate a injecao browniana na pipeline pSEOB.
9. **Jobs vivos: a gerencia contava 4; E ve 3 em ps.** RESOLVIDA por ps + AUDIT_RATE.json (14:02:16Z, PASS_ARITHMETIC_NOT_PRECISION): o 58182 terminou; o STATUS de 13:04Z estava velho. Nenhum produto dos 3 restantes (ETA 4,3 / 8,4 / 14,3 h; 78,7 GB RSS) e insumo da ampliacao (E) [DERIVED]; parar ou nao e do operador.
10. **R-LIN "a mais proxima do atingivel" (C) vs EXCLUDED_IF_UNIVERSAL (C1) e lnB −8,22 (catalogo).** NAO E CONTRADICAO, e a mesma parede vista de dois lados: a leitura mais barata em N e a que os relogios (v369) ja excluem se universal e a que o catalogo mais penaliza; so sobrevive por particao nao-universal — decisao do operador, e depois da C4 ja nao e cega.
11. **B: "5σ so os 5 melhores: N ≈ 647" vs A "212 GW250114-like".** RESOLVIDA: os "5 melhores" incluem σ 0,137–0,165 (4 eventos) alem do GW250114 — populacao intermediaria; ambos os numeros sao da mesma lei.
12. **sd(pred) da alavanca: A 0,0020 (nao ponderado) vs C 0,0016 (ponderado) no R-B.** Consistentes (definicoes diferentes); ambos dao N ≥ 3×10⁵.

## 4. O que a ORDEM 013-bis deve PRE-REGISTRAR

1. **Conjunto de calibracao vs conjunto de teste.** Os 31/33 do GWTC-5.0 e os 18 do GWTC-3 sao **NAO-CEGOS** (publicos, ja combinados, ja vistos pela bancada, auditoria e frentes A–D): entram como calibracao do portao e do nuisance, **nunca** como teste. Teste = eventos publicados **depois** do hash da 013-bis (GWTC-6/O4c, O5), com o δτ̂ e o δf̂ de cada novo evento sob offset oculto ate N_alvo.
2. **Observavel primario:** deformacao comum δτ̂₂₂₀ hierarquica sobre posteriores completos pSEOB (massa/spin da inspiral), com nuisance **c(σ) = c₀ + k·σ** (o +0,07 cresce com σ; intercepto constante nao o absorve) e funcao de selecao (a LVK declara viés de selecao para δτ̂ > 0). Estatistica: ln B (TGL-leitura vs RG) e z do filtro casado com offset em c(σ); ambos com hash antes do dado.
3. **Limiar:** 5σ unilateral (p = 2,87×10⁻⁷); para a rota IV, LRT > 23,9 na mistura de fronteira ½δ₀ + ½χ²₁ ou p por MC do nulo calibrado com os σ_i reais.
4. **Portao do poder (N_alvo) fixado antes da desblindagem, por leitura:** R-B 212 GW250114-like ou ~2.100 de mistura O4 (50–87 / 500–870 em O5); R-MOD 62 / 669 (14–25 / 157–274 em O5); R-RAIZ-0 61 / 618 (14–25 / 145–253); R-LIN 16 / 166 (4–7 / 39–68); rota IV: 59 eventos com σ_δf̂ ≤ 0,0136 (poder 90 %, σ_jit 0,019) ou 35 (0,0228). Registrar que **nenhum N_alvo do R-B cabe em O4 nem em O5** (O5 inteiro: 2,2–3,5σ) e que a ampliacao e **plurianual e condicionada**.
5. **Condicao sistematica como gate previo (fail-closed):** antes de somar qualquer evento ao teste, demonstrar por injecao (RG e TGL, duas familias SEOB×Phenom, (M,χ) LIVRES, ruido real off-source ao SNR do evento) que o orcamento coerente do amortecimento do 220 e < |δ|/5: 0,0040 (R-B) / 0,0074 (R-MOD, R-RAIZ-0) / 0,0143 (R-LIN). Enquanto o gate estiver vermelho, o veredito maximo permitido e **NOT_FALSIFIED_UNDERPOWERED** ou **INCONCLUSIVE_SYSTEMATICS** — nunca um σ.
6. **Nulos por injecao:** (a) curva c(SNR) do vies de δτ̂ (hoje +0,030@SNR20, 0,0083@40, 0,0011@200) na pipeline usada; (b) σ_sys do canal δf̂ (RG em duas familias, mesma pipeline) — hoje NAO ENCONTRADO; (c) 1.500 injecoes RG para FPR do 5σ; (d) split-null (metade dos eventos por sorteio com semente registrada).
7. **Convencao unica de deformacao pos-pico** [INPUT do operador]: escolher uma entre pSEOBNRv4HM_PA (fracional no QNM 220), C7_NATIVE (envoltoria 22/44) e C5 (overtones compartilham Γ₂₂₀), com o mapa TGL→δτ̂₂₂₀ de tgl_ringdown_prediction.py (fd0fc446e1c732f3) e o hash da convencao.
8. **A particao** [INPUT do operador, nao-cega apos a C4]: qual relogio (τ★ = GM_f/c³ ou outro), se e universal (se sim, R-RAIZ-0 e R-LIN saem do portao por v369), e se o 440 tambem se deforma (R-B preve δτ̂₄₄₀ = −0,082 = 4,1× o 220 — o discriminante que o 220 nao tem).
9. **Desenrolamento declarado** para a rota IV [INPUT: browniano = jitter de Milburn], com teste secundario robusto para saltos (fracao de outliers, estatistica de mistura a pre-registrar) e a declaracao de que o desenrolamento deterministico da sinal zero nesta rota; registrar que μ ≠ 0 comum em δf̂ (+0,0098 hoje) **nao e predicao da TGL** (δf̂ de ensemble = 0) — se persistir, e sistematica.
10. **Dados e cronograma como [OPEN]/[DECLARADO]:** GWTC-6.0 (data NAO ENCONTRADA; analogia mai–jun/2027), O5 (inicio OPEN), ET/CE (2035 vs early 2040s). A 013-bis pre-registra o **procedimento**, nao a data.
11. **Estatuto dos numeros:** todo N e valor esperado (z ∝ √N, sem variancia de z); Fisher de fonte fixa e teto; escalas O5/3G sao cenario; taxas 3G sao [KNOWN] de Berti/Bhagwat; R-MOD e [CONJECTURE]; relogio e [INPUT].
12. **O que fica registrado como NAO-CEGO hoje:** o +0,067 ± 0,033; o ajuste de tendencia (s = −1,9 ± 20,6); a regressao c(σ) (c₀ = −0,061 ± 0,068); o exploratorio de jitter (σ_jit < 0,0243 a 90 %, MLE 0); os lnB do catalogo (R-B −1,81 … R-LIN −8,22); o GW250114 inteiro.
13. **Rota III como calibracao, nao como N:** se a PE propria for autorizada, o pre-registro fixa que ela produz (a) a curva c(SNR), (b) σ_sys de δf̂, (c) o 440, (d) a comparacao de convencoes — e que os seus δτ̂ por evento sobre os 45 O4 publicos **nao** entram no teste (NAO-CEGO). Custo registrado: 166–1.108 h de parede (pSEOB) / 56–375 h (XPHM) para 45 eventos.
14. **Vereditos permitidos:** NOT_FALSIFIED_UNDERPOWERED · NOT_FALSIFIED_POWERED · INCONCLUSIVE_SYSTEMATICS · FALSIFIED_IN_READING (a 5σ contra a predicao com gate sistematico verde); CONFIRMED e PROVED proibidos.

## 5. Lacunas (NAO ENCONTRADO / OPEN, com quem as fecha)

- Taxa por ano de eventos GW250114-like (σ(δτ̂) ≤ 0,06) em O4c/O5: nenhum artefato; a minha e escala de volume [DERIVED]. Fecha-se com a funcao de selecao pSEOBNR × distribuicao de SNR_RD (Observing Scenarios nao da taxa BBH para O5).
- Data do GWTC-6.0 / strain O4c; inicio oficial de O5; datas de ET e CE (fontes discordantes) — [OPEN]/[DECLARADO].
- Transferencia do jitter browniano ao δf̂ da pipeline pSEOB (σ_jit,rec): so por injecao na pipeline LVK (pseobnr_injection do Zenodo 17018009, nao aberto) — [OPEN], o item mais importante da rota IV.
- σ_sys do canal δf̂ entre eventos (familia, modos, inicio): nao medido pela bancada (C5 so reporta a_hat/lnB) — [OPEN].
- Vies de δτ̂ por PSD mal estimada: so a variancia foi medida (7,5–8,8 %); a LVK cita "imperfect noise modelling" — [OPEN].
- Poder do modo 440 como discriminante (N para 5σ via 440): nao medido por ninguem — [OPEN].
- Numeros hierarquicos publicados da LVK (GWTC-3: μ = 0,13 ± 0,13, σ < 0,19 [KNOWN, em cache]; GWTC-4.0 0,17 ± 0,11 citado em aud_6, nao verificado; GWTC-5.0 secao pSEOBNR nao esta em cache).
- Conversao SNR_RD → σ(δf̂) para O5/3G (o Fisher da C5 e sobre a, nao sobre δf̂) — as linhas 3G da rota IV ficam em σ_meas.
- Sistematica de familia como funcao dos parametros da fonte numa populacao (so 3 fontes na C5) — [OPEN].
- RD.tar.gz do GWTC-5.0 (segundo metodo, 6 eventos) nao baixado; release TGR III do GWTC-4.0 nao existe no Zenodo.
- Instalabilidade de pyseobnr 0.3.7 / pyRing 0.0.12 / LAL_DATA_PATH em cache/vendor: nao testada.

## 6. Conclusoes do portao (o numero, sem suavizar)

1. **Com o dado de hoje (O4, 31–39 eventos) nenhuma leitura passa de 0,65σ (R-B) a 2,3σ (R-LIN)** com offset fixo em 0, e de 0,05–0,2σ com intercepto livre. O acervo publico esta esgotado ate o GWTC-6 [REAL/DERIVED].
2. **R-B (a leitura canonica) nao fecha 5σ por ampliacao de eventos em O4 nem em O5:** precisa de 212 eventos GW250114-like (O4 rende 0,69/ano) ou ~2.100 de mistura (142 anos a 14,5/ano); em O5, 50–87 GW250114-like (8–33 anos) ou 500–870 de mistura (11,7–15,3 anos); ao fim dos 3 anos de O5 chega a **2,2–3,5σ** — e isso com sistematica zero [DERIVED].
3. **R-MOD e R-RAIZ-0 chegam a 3,9–6,5σ ao fim de O5** so no topo da banda de SNR e com piso sistematico 0,0074 satisfeito (hoje violado por 1,7–13×); R-MOD e [CONJECTURE], R-RAIZ-0 e excluida se universal. **R-LIN fecha em ~1 ano de O5** estatisticamente, mas e excluida se universal e ja tem lnB −8,22 no catalogo [DERIVED].
4. **A condicao sistematica e o gate real, e esta vermelha para todas as leituras:** familia 0,029 (7× o piso do R-B), QNM-sum 0,0125–0,062, t₀ 0,075 (so-ringdown), catalogo +0,067; so o vies do estimador em SNR_RD ≥ 200 passa. Sem reduzir a sistematica ×5 (R-B) o N nao fecha nada — fecha um 5σ do modelo [DERIVED sobre REAL].
5. **A rota de menor N e a largura de δf̂ (59 eventos GW250114-like a 90 %),** mas e condicional ao desenrolamento browniano [INPUT], a transferencia ao pSEOB e [OPEN], o nulo e σ_sys (nao 0), e O4/O5 nao rendem 59 eventos dessa precisao em menos de 6–23 anos [DERIVED].
6. **Onde o 5σ e alcancavel:** 3G — 1–3 eventos GW250114-like (R-B) ou ~130 com SNR_RD ≥ 50 em ~1,3 ano (ET+CE, ≥ 2035 [DECLARADO]) — **desde que** o modelo de forma de onda seja validado a 0,40 % no amortecimento do 220 (hoje 1,3–9,7 %). Em 3G o gargalo e o modelo, nao o N.
7. **O que a ampliacao com O4c/O5 compra de fato:** a curva c(σ)/c(SNR), o σ_sys de δf̂, o 440 (4,1× o efeito) e eventos individuais de SNR alto — isto e, a **condicao** para que um 5σ futuro seja da natureza. E o que a 013-bis deve pre-registrar como objetivo da ampliacao, junto com o N_alvo por leitura.
8. **NOT_FALSIFIED em todas as leituras; nada confirmado; nada aqui move gate.** A RG e o limite classico: coincidir com ela e correspondencia recuperada; o que se mede e o tamanho da correcao β contra σ.

## 7. Arquivos desta sintese

- `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir\S_sintese\reconcilia.py` — reconciliacao (β runtime, sha16 das frentes, leis de escala, banda O5, taxa GW250114-like, piso/razoes)
- `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir\S_sintese\reconciliacao.json` — sha16 12032689bb9723b8
- `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir\S_sintese\escrever_sintese.py` — este escritor
- `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir\SINTESE.md` — este relatorio

Nada foi escrito na pasta da bancada nem no tunel; nenhum processo tocado; nenhum arquivo confidencial aberto; calculos leves.
