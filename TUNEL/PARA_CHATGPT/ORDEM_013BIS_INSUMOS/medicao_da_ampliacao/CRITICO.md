<!-- Cópia para a ORDEM 013-bis. ERRATA (deste crítico), já incorporada na ordem e válida sobre este texto: (1) o limiar do LRT para 5σ unilateral na mistura ½δ₀+½χ²₁ é 25,0, não 23,9; (2) com σ_jit = 0,0228 o N a 90 % é 38, não 35 (o 35 era literal digitado); (3) UMA convenção de poder (90 %): os N sem rótulo aqui são N₅₀. Os caminhos «...\scratchpad\ordem013\bis\medir\...» são efêmeros: cada arquivo citado está nesta pasta, no mesmo caminho relativo, com o mesmo sha16 (salvo os saneados, listados em SANEADOS.json). -->

# CRITICO DE COMPLETUDE — o que falta para a ORDEM 013-bis ampliar os eventos ate 5σ sem fabricar poder

**Data:** 22/09/2026 · **Papel:** critico de completude da gerencia (Claude) · **Insumo:** `SINTESE.md` (sha16 97335078a239800f) + saidas das frentes A–E + reconciliacao S, e os artefatos da bancada em so-leitura.
**β em runtime:** ALPHA_FINE_CODATA_2018 × √e = 0.012031300400803142 [REAL] (identico ao das frentes).
**Escrita:** so em `...\medir\CRITICO.md` (este) e `...\medir\CRITICO_completude\` (script + JSON). Nada tocado na bancada, no tunel, em processos ou em confidenciais. Calculo leve (numpy, `nice 19`).

## 0. Fontes lidas por script (sha16)

| arquivo | sha16 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_220.json` (bancada) | 93bdc413130d294a |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_COMBINATION.json` (bancada) | f3d8c1959ded3efd |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C5_FISHER.json` (bancada) | 71189d65f52d3530 |
| `...\medir\A_poder_eventos\A_poder_eventos.json` / `A1_por_evento.csv` | 1219a98f08b4e1eb / d02c185c876d6094 |
| `...\medir\B_catalogos\RENDIMENTO_E_5SIGMA.json` / `N5SIGMA_FROM_CATALOG.json` / `gwtc5_tgr_table2_3_parsed.json` | 57ff7bacbe0d6085 / 1e48703be9ff9a0f / 4119e5f8279dfd15 |
| `...\medir\C_piso_sistematico\C_piso_medicoes.json` / `C_piso_sinais_catalogo.json` | cfdb198d667df8f7 / 92e26c7cdf3ed1f4 |
| `...\medir\D_realizacao_unica\D_consolidado.json` / `d2_resultado.json` | 225d97be61433ef5 / d7402bae7f41da00 |
| `...\medir\E_instrumento\MEDICAO_E.json` | 79b4c14add2f5268 |
| `...\medir\S_sintese\reconciliacao.json` | 12032689bb9723b8 |
| `...\medir\CRITICO_completude\refazer.py` → `REFEITOS.json` | 5d8233286a39fe70 → 68237923e4597d4b |
| `...\medir\CRITICO_completude\REFEITOS_2.json` (gerado por `refazer_2.py`) | e9ade58136442241 |

## 1. Numeros refeitos (meu valor vs o da sintese) — a partir do `C4_CATALOG_220.json` da bancada, nao das frentes

Convencao minha: σ_i = (q95−q05)/(2·1,645) da marginal dtau220 do arquivo da bancada; pred_i = mediana de `shift_05_50_95` por leitura; filtro casado z = √Σ(pred_i/σ_i)²; intercepto livre = Fisher da inclinacao com pesos 1/σ_i².

| numero | meu (script) | sintese | bate? | estatuto |
|---|---|---|---|---|
| media ponderada δτ̂₂₂₀ (31) | +0,0669 ± 0,0332 (z 2,01 vs 0) | +0,0668 ± 0,0336 (A) / +0,0669 ± 0,0332 (C) | **sim** | [REAL, NAO-CEGO] |
| z_comb R-B / R-MOD / R-RAIZ-0 / R-LIN (31, offset 0) | 0,613 / 1,087 / 1,132 / 2,182 | 0,606 / 1,076 / 1,120 / 2,159 (A, σ = std) | **sim** (≤ 1,2 %; diferenca = definicao de σ) | [DERIVED] |
| N5 mistura-31, R-B / R-MOD / R-RAIZ-0 / R-LIN | 2.062 / 657 / 605 / 163 | ~2.100 / 715 / 671 / 181 (A, uniao 39 na tabela 2.1); 2.062–2.108 (§3.1) | **sim** dentro da banda que a propria sintese declara | [DERIVED] |
| z_obs contra a predicao (offset 0), R-B … R-LIN | 2,62 / 3,09 / 3,14 / 4,19 | 2,59 / 3,06 / 3,11 / 4,15 | **sim** | [REAL, NAO-CEGO] |
| z_slope intercepto livre (31) e N5 | R-B 0,0489 → 3,24×10⁵; R-MOD 0,160 → 3,02×10⁴; R-RAIZ-0 0,0545 → 2,61×10⁵; R-LIN 0,101 → 7,60×10⁴ | 3,3×10⁵ / 3,1×10⁴ / 2,7×10⁵ / 7,7×10⁴ (A, 39) | **sim** — o poder da tendencia FOI calculado com os σ_i reais (A, C e eu) | [DERIVED] |
| GW250114: σ(δτ̂) / σ(δf̂); N5 GW250114-like R-B | 0,0580 / 0,01364; 213,2 | 0,058 / 0,0136; 212 | **sim** | [REAL] / [DERIVED] |
| eventos com σ(δτ̂) ≤ 0,06 / 0,10 / 0,15 / 0,20 (33 da bancada) | 1 / 1 / 3 / 9 | 1 / 1 / 3 (S, 39) | **sim** | [REAL] |
| pSEOBNR em O4b (Tabela 2/3 GWTC-5.0 parseada) | 14 (RD 6, QNMRF 4) | 14 / 6 / 4 (B) | **sim** | [REAL lido] |
| N5 variancia de δf̂, GW250114-like, σ_jit 0,019: poder MC (LRT > 25) | N = 33 → 48,6 %; N = 59 → 90,2 % (4.000 draws) | 33 / 59 (D) | **sim** | [DERIVED sob browniano] |
| idem, σ_jit 0,0228 | N = 20 → 49 %; **N = 35 → 86,5 %; 90 % so em N = 38** (8.000 draws: 37 → 89,2 %, 38 → 91,2 %) | 20 / **35** (S, tabela 2.4 e §3.6) | **NAO**: o «35» e literal digitado em `reconcilia.py:140`, nao MC; 90 % pede 38 | [DERIVED] |
| limiar do LRT na mistura ½δ₀+½χ²₁ para 5σ unilateral | **25,0** (z² = 25; p = 2,87×10⁻⁷); 23,9 ≙ z = 4,89, p = 5,1×10⁻⁷ | **23,9** (§2.4 e §4.3) | **NAO**: 23,9 nao existe em nenhum JSON; `d2` usa 25,0 | [DERIVED] |
| poder no N = 28 «= E[z] = 5 ≈ 50 %» (A) | 38,5 % (LRT ≠ score z) | «≈ poder 50 %» | **nao** (afirmacao imprecisa; irrelevante para o N_alvo, que usa D) | [DERIVED] |
| anos de O5 para N5 R-B mistura (B) | taxa baixa (g³ = 3,81): 11,7–15,6; **taxa alta (5,69): 7,8–10,5** | «11,7–15,3» rotulado como banda de taxa «×4,6..5,7» | **parcial**: o codigo de B divide os dois limites por g_lo³ (`rendimento_e_5sigma.py:61`); a banda da sintese e de N, nao de taxa | [DERIVED] |
| z R-B ao fim de 3 anos de O5 (mistura) | banda BBH coerente 2,21–3,09; com PSD C5 (×1,987) e volume BBH max: 3,44 | 2,2–3,5 | **parcial**: o 3,5 usa o fator de SNR de BNS (×2,06) sobre contagem de BBH | [DERIVED, cenario] |

## 2. Lacunas, por gravidade

### BLOQUEANTES (a ordem nao pode pre-registrar o 5σ sem fechar isto)

**B1. O nuisance do catalogo LVK e o 5σ espurio tem N.** Se o deslocamento +0,067 (Spearman 0,48 com σ; LVK: «biased towards positive») persistir como vies comum na pipeline publica, a ampliacao com offset fixo em 0 chega a **5σ CONTRA a leitura** em **N ≈ 112 (R-B) / 81 (R-MOD) / 78 (R-RAIZ-0) / 44 (R-LIN)** eventos de mistura O4 — muito antes dos N5 de deteccao (2.062 / 657 / 605 / 163). A sintese diz «converge para um 5σ do modelo» mas nao da o N; o N mostra que **a rota I-a e um falsificador espurio a ~100 eventos**. A ordem deve: (i) proibir o offset fixo em 0 como estatistica de teste; (ii) exigir c(σ) ou c(SNR) **calibrado por injecao RG na pipeline que produziu os posteriores** (o que a gerencia nao controla nos posteriores LVK); (iii) manter FALSIFIED_IN_READING condicionado ao gate sistematico verde (a sintese ja o faz no item 4.14 — deve citar o N). [DERIVED sobre REAL, NAO-CEGO]

**B2. O custo de calibrar o nuisance ao piso nao esta em lugar nenhum.** Para fixar c a σ_c = |δ|/5 com σ por injecao = 0,0497 (Fisher SNR40, C5): **157 injecoes por celula (R-B)**, 46 (R-MOD/R-RAIZ-0), 12 (R-LIN). A PE pSEOBNRv4HM_PA custa 81–542 CPU-h (E, [DERIVED sobre KNOWN]): **12,7k–85k CPU-h por celula; 10 celulas minimas (5 bins de SNR × 2 familias, sem varrer massa/spin) = 127k–851k CPU-h = 241–1.612 dias de parede a 22 workers** para o R-B. A sintese orca so a PE cientifica dos 45 eventos (166–1.108 h de parede); **a calibracao, que e o que a rota III compra, custa 10–100× isso**. Em SNR 20 o σ por injecao dobra e o N de injecoes quadruplica. Sem esse orcamento a rota III como «condicao sistematica» e uma frase, nao um plano. [DERIVED]

**B3. O rendimento que decide o cronograma e UMA contagem.** «GW250114-like» (σ ≤ 0,06) = 1 evento em 1,45 ano → IC90 de Poisson **[0,035; 3,27]/ano** (nao 0,69/ano); os «8–33 anos de O5» do R-B viram **3–370 anos**. A fracao pSEOBNR/TGR (18,4 %) e [REAL lido] e o 14 de O4b confere na tabela parseada, mas a extrapolacao a O4c/O5 supoe fracao constante e volume euclidiano (f³; a z ≳ 1 o volume comovel cresce menos). A ordem nao pode fixar «anos» por essa taxa — deve fixar **N_alvo e o criterio de qualidade**, e deixar o calendario como [OPEN]. [DERIVED, cenario]

**B4. O criterio de qualidade e pos-analise.** «GW250114-like» esta definido por σ(δτ̂) ≤ 0,06, uma largura de posterior — que a frente C mostra correlacionada com o proprio vies (+0,07 cresce com σ). Selecionar por σ e selecionar pelo resultado da analise. O pre-registro precisa de corte **pre-analise**: SNR de rede / SNR_RD, M_f, χ_f. Pelo ajuste de B (σ = 3,03·SNR^−0,86, resid. log 0,24), σ ≤ 0,06 ≙ **SNR_rede ≳ 95** e σ ≤ 0,10 ≙ SNR ≳ 53. Ninguem mediu quantos eventos por ano passam esse corte (GWOSC: 5 com SNR ≥ 30 no GWTC-5.0, 1 acima de 78). [DERIVED]

### IMPORTANTES (numeros errados ou convencoes inconsistentes na sintese)

**I1. Limiar 23,9 → 25,0.** O item 4.3 do pre-registro traz um numero sem fonte; para 5σ unilateral na mistura ½δ₀+½χ²₁ o limiar e **25,0** (e o `d2` ja usa 25,0). 23,9 e 4,89σ. Corrigir antes do hash.

**I2. «35 eventos a 90 % com σ_jit 0,0228» → 38.** Literal em `reconcilia.py:140`; meu MC (8.000 draws) da 86,5 % em 35 e 91,2 % em 38. O par correto e **20 (50 %) / 38 (90 %)**.

**I3. Convencoes de poder diferentes entre rotas.** As rotas I–III fixam N_alvo por E[z] = 5 (≈ 50 % de poder; no LRT, 38–49 %); a rota IV usa 90 %. Para 90 % no filtro casado o fator e (5+1,28)²/25 = **1,578**: R-B 212 → **335** GW250114-like; 2.062 → **3.254** mistura; O5 50–87 → **79–137**. A ordem deve escolher UMA convencao (90 %, como no piso dos vazios) e reescrever a tabela 4.4.

**I4. A condicao sistematica esta quantificada como componente BRUTA vs piso, nao como residuo pos-calibracao.** A tabela 2.6 compara |vies| com |δ|/5. O gate util e σ(c_calibrado) < |δ|/5 (B2 diz quanto custa). Alem disso o piso |δ|/5 e **convencao**, nao derivacao: deixa passar um vies de 1σ_stat; a convencao usual e ≤ σ_stat/3 (|δ|/15 = 0,0013 no R-B). Declarar como [INPUT].

**I5. Custo da rota (b) e estimativa, nao medida.** `cpu_h_por_evento` = t_onda [REAL, 0,0975 s] × n_avaliacoes **literal 3×10⁶–2×10⁷ [KNOWN ordem de grandeza]** (`medir_E.py:263`), sem o «+30–100 % de overhead» que o proprio E declara; nenhuma PE IMR foi rodada. Fator 6,7 de incerteza. Uma PE piloto (1 evento, 1 familia) mediria — e pesada, logo decisao do operador.

**I6. Anos de O5 (B) rotulados como banda de taxa e calculados a taxa fixa.** Ver tabela §1: «11,7–15,3» e a taxa baixa; a taxa alta da 7,8–10,5. E o fator de SNR ×2,06 do topo da banda e de BNS, nao de BBH (topo coerente 3,09σ, nao 3,5σ).

**I7. Nulo da rota IV: calibrado so em parte.** D calibrou por MC (4.000) o score-z do nulo com os 31 σ_i reais (q99 = 2,10) — bem. O limiar do LRT e assintotico; meu MC sob H0 (N = 59, σ homogeneo, 2×10⁵ draws) da caudas **abaixo** da mistura (LRT > 9: 9,4×10⁻⁴ vs 1,35×10⁻³; > 12,25: 1,5×10⁻⁴ vs 2,3×10⁻⁴) — conservador, portanto, mas **ninguem calibrou a 2,9×10⁻⁷ (≥ 10⁸ draws) nem com σ_i heterogeneos e posteriores nao-gaussianos**. E o nulo fisico e σ_sys² (nao 0): so o limite exploratorio σ_jit² + σ_sys² < 0,0243² a 90 % existe; σ_sys separado [OPEN] (sintese ja declara).

**I8. Transferencia do jitter ao δf̂ do pSEOB [OPEN] torna os N da rota IV limites inferiores** (sintese §3.8) — mas a tabela 4.4 os fixa como N_alvo sem essa marca. Marcar.

### NOTAS

- N1. §2.2 «39 acumulados» = 31 + 8 pSEOBNR (O4c estimado); a «uniao 39» de §1 = 33 + 6 GWTC-3. Mesmo numero, populacoes diferentes; com a uniao 39 + 8 → 47, z R-B = 0,72.
- N2. N5 Fisher SNR40: 150 (bancada, δ = −0,0199) vs 157 (C/eu, δ = −0,01985 mediana do GW250114). Mesma lei; a sintese ja o resolve (§3.1).
- N3. B usa mean z²/evento (0,01212) e A usa z_comb 0,606: diferenca de 2 % e de definicao de σ (gauss q05–q95 vs std). Meu 0,613 reproduz B exatamente.
- N4. A afirmacao «A da 28 = E[z] = 5 ≈ poder 50 %» e imprecisa (38,5 % no LRT). Nao afeta o N_alvo.
- N5. O IC90 de Poisson tambem vale para os 8 pSEOBNR estimados do O4c (fracao × 68): nao e contagem, e projecao.
- N6. `fisher_mass_spin_free = NON_IDENTIFIABLE_SINGLE_220` (C5) esta corretamente propagado: nenhuma rota so-ringdown de um modo entra no portao.

## 3. Respostas diretas ao mandato

- **Numero na sintese sem fonte?** Sim, dois: o limiar **23,9** (I1) e o par **20/35** (I2). Os demais numeros centrais rastreiam a arquivos e batem (§1).
- **Contradicao nao resolvida?** Tres nao percebidas: 23,9 vs 25,0 (d2); 35 vs MC; banda de anos de O5 rotulada como taxa (I6). As 12 da §3 da sintese estao bem resolvidas ou bem declaradas abertas.
- **Condicao sistematica quantificada por leitura?** Sim, como componente bruta/piso (C, 8 itens × 4 leituras). Falta o residuo pos-calibracao e o seu custo (B2, I4).
- **Rendimento medido ou chutado?** A fracao pSEOBNR/TGR (18,4 %) e medida [REAL lido; 14 de O4b conferido na tabela parseada]. O rendimento que importa ao portao (GW250114-like) e **uma contagem** = chute com IC de duas ordens (B3), e o criterio e pos-analise (B4).
- **Tendencia com intercepto livre com σ reais?** Sim: A (39), C (31/33) e eu (31/33) → N ≥ 2,6×10⁵ (R-B). Inviavel em qualquer detector; conclusao solida.
- **Largura de δf̂ com nulo calibravel?** Parcialmente (I7): score-z calibrado por MC nos 31; LRT assintotico e conservador no MC homogeneo; σ_sys [OPEN]; cauda 5σ nao calibrada.
- **Custo da rota (b) em horas-maquina com fonte?** Tem fonte mas e [DERIVED sobre KNOWN] com fator 6,7 (I5), e **omite a calibracao** (B2).

## 4. O que a ORDEM 013-bis deve dizer como NAO PAGO / OPEN

1. **NAO PAGO — calibracao do nuisance c ao piso:** 157 injecoes/celula (R-B) × ≥ 10 celulas × 81–542 CPU-h = 127k–851k CPU-h; sem isso nenhum σ da rota I ou III e da natureza. [DERIVED]
2. **NAO PAGO — PE IMR piloto** que mede o custo real por evento (hoje literal 3×10⁶–2×10⁷ avaliacoes). [OPEN, decisao do operador]
3. **OPEN — taxa de eventos GW250114-like** (1 contagem; IC90 0,035–3,3/ano) e o **corte de qualidade pre-analise** (SNR_rede ≳ 95 pelo ajuste de B; a definir e a contar em GWOSC). [DERIVED/OPEN]
4. **OPEN — σ_sys do canal δf̂** entre eventos (familia, t₀, modos) e a **transferencia do jitter browniano ao δf̂ do pSEOB**; os N da rota IV (33/59 a 0,019; 20/38 a 0,0228) sao limites inferiores. [OPEN]
5. **OPEN — calibracao do nulo do LRT a 2,9×10⁻⁷** com σ_i heterogeneos (MC ≥ 10⁸ ou p por MC do nulo no N_alvo). [OPEN]
6. **OPEN — modo 440** como discriminante (N para 5σ nao medido). [OPEN]
7. **OPEN — cronograma**: GWTC-6/strain O4c, inicio de O5, ET/CE. A ordem pre-registra procedimento e N_alvo, nunca data. [DECLARADO]
8. **A DECLARAR — convencao de poder** (uma so; 90 % ⇒ N_alvo ×1,578 nas rotas I–III) e **convencao do piso** (|δ|/5 e [INPUT]; |δ|/15 seria a usual).
9. **A DECLARAR — o falsificador espurio**: com offset fixo em 0 e vies LVK persistente, 5σ contra o R-B em ~112 eventos; FALSIFIED_IN_READING so com gate sistematico verde e nuisance calibrado.
10. **Vereditos hoje**: NOT_FALSIFIED em todas as leituras; nada confirmado; nenhum gate movido; a RG e o limite classico. O 5σ e alcancavel por contagem so em 3G (ET/CE ≥ 2035 [DECLARADO]) e ali o gargalo e o modelo (0,40 % de τ₂₂₀), nao o N.

## 5. Arquivos deste critico

- `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir\CRITICO_completude\refazer.py` (sha16 5d8233286a39fe70) → `REFEITOS.json` (68237923e4597d4b): catalogo 31/33 refeito do arquivo da bancada; limiar do LRT; poder MC do LRT (σ_jit 0,019/0,0228/0,03; N 20–59); FPR sob H0 (N = 59, 2×10⁵); Poisson da taxa; banda O5; custo de calibracao por injecao; N do 5σ espurio.
- `...\CRITICO_completude\refazer_2.py` (sha16 8bca898420e4636d) → `REFEITOS_2.json` (e9ade58136442241): poder MC em N = 36–42 (σ_jit 0,0228); fator N90/N5; SNR equivalente ao corte σ ≤ 0,06/0,10; anos de O5 por taxa.
- `...\medir\CRITICO.md` — este relatorio.
