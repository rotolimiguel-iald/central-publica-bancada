# FRENTE B — O que existe e o que vem: catálogos, cronograma, rendimento (medição de 22/09/2026)

Régua: número corrige a frase; nada de memória; β = α_CODATA2018·√e em runtime = 0,012031300400803142.
Pasta da bancada só lida. Scripts e saídas: esta pasta (`B_catalogos`).

## 1. GWTC-5.0 TGR (arXiv:2607.19293, 21/07/2026; Zenodo 21454847, 22/07/2026) `[REAL — lido do PDF e do release]`
- Seleção geral: FAR ≤ 10⁻³/ano e ≥ 2 detectores → **72 O4b + 5 O4a = 168 eventos** acumulados (abstract).
- **pSEOBNRv5PHM**: critério = **"SNR ≥ 8 in both the inspiral and post-inspiral parts of the signal"** (Sec. 7.2); SNR pós-inspiral = mediana do PE com SEOBNRv5PHM (O4a em diante) ou MAP do IMRPhenomXPHM (até O3b). Tabela 2: **14** O4b com ✓ (contado por script); Tabela 3 (5 O4a extra): 0. Seleção primária **31** (notebook do release, hash db64f5c1ee3eba2f), **33** metafiles (GW191109_010717 e GW200208_130117 = controles). GW250114 é o mesmo arquivo do Zenodo 17018009 (sha b9971bcd…), contado uma vez.
- **RD (`ringdown`, tempo)**: critério = mediana do SNR ótimo pós-pico **ρ_pp ≥ 10** (NRSur7dq4, 500 amostras): **6** O4b. **pyRing NÃO rodou** no 5.0 ("undergoing development to improve its computational efficiency"). QNMRF: 4 O4b.
- Resultados combinados pSEOBNR (Tabela 9): joint Q²ᴰ_GR = **98,1⁺¹·⁹₋₆,₉ %**; hierárquico Q^{1D,μδτ} = 98,7⁺¹·³₋₁₃,₁ %; Q⁴ᴰ = 92,5⁺⁷·⁵₋₂₀,₈ % (GWTC-4.0: 98,6 / 99,3 / 85,1 %). Cinco eventos mais altos (GW250114, GW240920, GW231226, GW240621, GW200129): δτ̂₂₂₀ = **0,02⁺⁰·⁰⁸₋₀,₀₈**, Q²ᴰ = 69,6 %. Sem GW250114 (todos): δτ̂₂₂₀ = 0,11⁺⁰·⁰⁹₋₀,₀₇, Q²ᴰ = 99,0 %. **A própria LVK diz que "the pSEOBNR selection criteria may favor events with positive damping time deviations, as these tend to have a larger ringdown SNR"** — o viés de seleção puxa δτ̂ para cima (é o desvio +0,072 da bancada). `[REAL — citação]`
- Release: `pSEOB.tar.gz` (amostras por evento, 33), `RD.tar.gz` 415.283.962 B (não baixado pela bancada), `QNMRF.tar.gz`. Config e posteriores "will be released through Zenodo" (feito em 22/07/2026).

## 2. GWTC-4.0 TGR III (arXiv:2603.19021, 19/03/2026) `[REAL — lido do PDF]`
- 91 eventos (42 O4a). Tabela 1 (parse): **pSEOBNR ✓ = 19** (12 pré-O4 + **7 O4a**); pyRing ✓ = 22 O4a (log₁₀ B²²_Noise ≳ 1; GW230606 e GW231118 excluídos por falha técnica); QNMRF 2. Mesmo critério pSEOBNR (SNR ≥ 8 nas duas partes).
- Tabela 4: GWTC-3.0 → Q²ᴰ 93,8⁺⁶·¹₋₂₀,₀ %; GWTC-4.0 → 98,6⁺¹·⁴₋₉,₄ %; com GW250114: 96,2 %.
- **Release público de posteriores do Paper III: NÃO ENCONTRADO** no Zenodo (busca "GWTC-4.0 Tests of General Relativity": só o Paper II, Zenodo 21403342, 17/07/2026). Os 7 O4a pSEOBNR estão dentro do release 5.0 (metafiles `pSEOB_GW2306..GW2312..`). **O 5.0 é cumulativo e substitui o 4.0** para o ringdown. PE por evento O4a (M_f, χ_f): Zenodo 17602505 (22/05/2026, 103 arquivos, FAR < 1/ano).

## 3. GWTC-3 TGR (Zenodo 17461225) `[REAL — lido do cache da bancada]`
- 18 produtos pSEOBNRv4HM; Tabela 13 = 12, **10** usados (2 excluídos pelos autores). Critério: SNR ≥ 8 pré- e pós-inspiral (limiar de massa da análise anterior relaxado). 12 sobrepostos com o 5.0; 6 só no 3.0 (união 39, sem evidência de união calculada).

## 4. O4c e GWTC-6 `[REAL contagem; previsão DERIVED]`
- O4c: 28/01/2025 17:00 → 18/11/2025 16:00 UTC. GraceDB (22/09/2026): **O4a 81 (92−11), O4b 105 (114−9), O4c 68 (77−9); O4 total 254 (283−29)**; baixa significância 5136.
- GWTC-6.0: **data NÃO ENCONTRADA** (ligo.org: "will be analyzed and released in a subsequent version of the catalog"; AEI: "in the coming months"). Strain O4c no GWOSC: NÃO ENCONTRADA; analogia (O4a +19,3 meses; O4b +15,9 meses) → **~maio–junho/2027**.
- Estimativa: TGR ≈ 42; **pSEOBNR ≈ 8** (fração 21/186). Total acumulado pSEOBNR previsto após O4c ≈ **39**.

## 5. O5 / IR1 `[REAL datas; OPEN cronograma; DERIVED escalas]`
- IR1: início nov/2026, 6 meses (IGWN, 03/09/2026). O5: "being refined" (IGWN); "could start at the end of 2027" (EGO, 03/02/2025); roadmap LIGO Lab 2023: 3 anos até Q3/2029 (superado); Wikipedia set/2026: "tentatively 2029 onwards". **O início de O5 é OPEN; não há número oficial de detecções BBH/ano para O5** (Observing Scenarios v55 só dá O4: BBH 68⁺⁸¹₋₃₈/ano).
- Meta A+: BNS 330 Mpc, BBH 2500 Mpc (O4 1400–1600) → SNR ×1,56–1,79 a fonte fixa; N_det ×3,8–5,7 (mesma população). Observado em O4b: 161 candidatos/9,6 meses ≈ 200/ano → O5 ≈ 760–1140/ano [DERIVED]. pSEOBNR/ano O5 ≈ 55–83 [DERIVED].
- A♯ (~fim de 2031): ×2 em strain → σ/2, N_det ×8 [DECLARADO plano 2023].

## 6. ET / CE `[DECLARADO datas; KNOWN taxas]`
- ET: ESFRI 2021; decisão de sítio 2027; construção 2028; observação 2035 (Wikipedia, ref. [9]) vs "early 2040s" (site oficial) — discordância registrada. CE: recomendação NSF 03/2024; "mid-2030s to 2040s".
- Taxas (Berti et al., rev. CQG 2026, arXiv:2505.23895 §7.1, Fig. 76 ← Bhagwat et al. 2023): ET+CE **~10²/ano com SNR_RD ≳ 50; O(10)/ano com SNR_RD ≳ 100**; GW150914 em ET teria SNR_RD O(200). Bhagwat 2023 (abstract): ET mede 2 QNM a O(10%) em ≥ O(500) eventos/ano; com CE, poucos % em O(100)/ano.

## 7. Strain público hoje (GWOSC) `[REAL]`
- O4a (26/08/2025; H1, L1), **O4b (26/05/2026; H1, L1, V1)**, 4 e 16 kHz, HDF5/GWF. A bancada já tem O4b_4KHZ_R1 do GW250114 (H1/L1 on/off-source, sha no `C6_DOWNLOADS.json` 188ecebffcdeabc8). **Logo, os 14 eventos O4b pSEOBNR (e os 72 TGR) têm strain aberto para análise própria hoje**; O4c não.

## 8. Posteriores públicos por evento (M_f, χ_f) `[REAL]`
- GWTC-5.0 PE: Zenodo 20348005 (84 hdf5, 38,6 GB) + 20348006 (20 hdf5, 9,07 GB) = 104 (FAR < 1/ano O4b), com massa/spin finais quando o modelo os dá; GWTC-4.0 PE: 17602505 (103 arquivos). Os 33 metafiles pSEOB já trazem `final_spin_non_evolved` e massa detector (usados pela bancada). → **predição por evento (δτ̂_pred(χ_f, M_f)) é possível para os 104 O4b + O4a mesmo sem δτ̂ publicado**; o que falta é a largura por evento (só existe para os 31/33).

## 9. N para 5σ — a partir das larguras REAIS por evento (`RENDIMENTO_E_5SIGMA.json`, script `rendimento_e_5sigma.py`) `[DERIVED; estatístico puro]`
Método: z_i = δ_pred,i/σ_i com σ_i = (q95−q05)/(2·1,645) da marginal real de δτ̂₂₂₀ (pSEOB, 31 eventos; `C4_CATALOG_220.json` sha16 93bdc413130d294a); 5σ ⇔ Σz_i² ≥ 25 (deformação comum, sem sistemática). σ_i reais: mín 0,058 (GW250114), mediana 0,241, máx 0,595; σ combinada dos 31 = 0,0332.

| Leitura | δτ̂_pred (mediana) | z com os 31 reais | N eventos qualidade-O4 | anos a 14,5/ano | N em O5 (SNR ×1,56–1,79) | anos em O5 (55–83/ano) | SNR_RD p/ 5σ num evento | N em 3G (SNR_RD ≥ 50) / anos a 100/ano | N em 3G (SNR_RD ≥ 100) / anos a 10/ano |
|---|---|---|---|---|---|---|---|---|---|
| R-B | −0,0202 | 0,61 | **2062** | 142 | 647–845 | 11,7–15,3 | ~573 (bancada: ~490) | 131 / 1,3 | 33 / 3,3 |
| R-RAIZ-0 | −0,0375 | 1,13 | 605 | 42 | 190–248 | 3,4–4,5 | ~309 | 38 / 0,4 | 10 / 1,0 |
| R-MOD | −0,0353 | 1,09 | 657 | 45 | 206–269 | 3,7–4,9 | ~329 | 43 / 0,4 | 11 / 1,1 |
| R-LIN | −0,0723 | 2,18 | 163 | 11 | 51–67 | 0,9–1,2 | ~160 | 10 / 0,1 | 2,6 / 0,3 |

Condições e paredes (todas [INPUT/KNOWN da auditoria e da LVK]): (i) o piso sistemático tem de ficar abaixo de δ/5 → **0,004 para R-B, 0,007 R-RAIZ-0/R-MOD, 0,014 R-LIN**; a sistemática de família SEOB×Phenom medida pela bancada (~0,9 do efeito ≈ 0,018) e o viés do estimador (+0,03 em SNR baixa) **excedem esse piso para todas as leituras exceto marginalmente R-LIN** → 5σ por contagem só existe se a sistemática cair ×5 (R-B) — ampliar eventos não resolve isso; (ii) o viés de seleção declarado pela LVK (pSEOBNR favorece δτ̂ > 0) tem de ser modelado (função de seleção) antes de somar eventos; (iii) NON_IDENTIFIABLE_SINGLE_220: só vale com (M, a) da inspiral (pSEOBNR) ou 2º modo; (iv) A♯ (σ/2, ×8 eventos) reduz N_O5 de R-B a ~160–210 em ~0,3–0,5 ano de taxa A♯ — plano de 2031+, [DECLARADO].

## 10. Não encontrado
- Data do GWTC-6.0 / release O4c (catálogo, TGR e strain). Taxa oficial de BBH/ano em O5 (só O4 na v55). Início oficial de O5 (três fontes discordantes). Release de posteriores do GWTC-4.0 TGR III. SNR de ringdown típico em O5 (nenhuma fonte). Data oficial de operação de CE.
