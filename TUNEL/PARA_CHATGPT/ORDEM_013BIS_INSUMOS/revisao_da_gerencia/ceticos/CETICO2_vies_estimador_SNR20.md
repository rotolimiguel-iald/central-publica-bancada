# CÉTICO 2 — achado «viés do estimador +0,030 @SNR20» (ORDEM 013-bis, linhas 133 e 161; também linha 71)

**Veredito: NÃO refutado (refutado=false). Gravidade mantida: IMPORTANTE. O achado é MAIS forte do que o revisor mediu.**

## 1. O que a ordem diz (lida com numeração)
- L71: «viés do estimador em SNR baixo (a bancada mediu +0,030 em ruído sintético SNR 20 com efeito nulo) [REAL no escopo sintético]»
- L133: «Dependente de SNR (…): viés do estimador +0,030 @SNR20, **0,0083 @SNR40 (2,1× o piso do R-B), 0,0011 @SNR200 (OK para todas)**.»
- L161 (E1.4): «O viés do estimador da bancada por SNR (já medido: +0,030 @20; 0,0083 @40; 0,0011 @200) como controle da mesma forma funcional.»

## 2. Fontes lidas por script
- Bancada (só leitura) `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C2_TRAJECTORY_RECOVERY.json` — guarda os 50 `fits` por trajetória. Linha R-GLOBAL (γ=0, RG), ruído `SYNTHETIC_COLORED_OU_PLUS_WHITE`, SNR 20: **N=50, média +0,0303, mediana +0,0152, sd 0,0930, EP 0,0131 → z=2,3**; q05/95 −0,1026/+0,2074. (R-A, R-RAIZ-EP4, R-RAIZ-REST dão o mesmo, γ≈0.)
- `medir\D_realizacao_unica\D_consolidado.json` → `C2_RG_ruido_lido` = R-GLOBAL da C2 (d4_consolida.py:20). Confere.
- `medir\C_piso_sistematico\C_piso_medicoes.json` `B_familia_resumo/R-B/same_SNR40_bias_dtau_abs` n=8 mediana 0,00830; `same_SNR200` mediana 0,00106. Confere — MAS são `abs(absolute_bias) × |δ_R-B|` de células da **C5_IMR_RECOVERY** (PE bayesiana IMR, N=206 draws/célula, viés em |a| ∈ [0,14; 1,02] no SNR40, i.e. 14–102 % do efeito), não do estimador da C2.

## 3. Refeito por script (cópia fiel do estimador de `trajectory_recovery.py`, só N e SNR mudam; `c2_refeito\refazer_snr20.py`)
| N | SNR | média | EP | z | mediana | sd |
|---|---|---|---|---|---|---|
| 50 (semente da bancada, mesma sequência) | 20 | **+0,030314** (reproduz a bancada) | 0,0131 | 2,3 | +0,0152 | 0,0930 |
| 2000 | 20 | **+0,0103** | 0,0023 | 4,6 | +0,0044 | 0,1009 |
| 2000 | 40 | +0,0026 | 0,0011 | 2,3 | +0,0014 | 0,0496 |
| 2000 | 200 | +0,00013 | 0,00022 | 0,6 | +0,00011 | 0,0099 |

Leitura: o «+0,030» é flutuação de N=50 (1,5 EP acima do valor de N=2000); o viés do estimador da C2 em SNR20 é **≈ +0,010**, escala ≈ 4/SNR² (0,0103 → 0,0026 → 0,00013). O ponto @SNR40 do estimador C2 (0,0026) já fica ABAIXO do piso R-B (0,0040) — ao contrário do que a L133 conclui com o 0,0083 da C5, que é outro estimador.

## 4. Por que o achado vale (e vale mais)
1. A ordem cita um número de 2,3σ sem erro nem N, duas vezes, e o rotula [REAL] (L71) — a régua manda pôr o erro.
2. O número está errado por ~3× (medido, não estimado): +0,010 ± 0,002, não +0,030.
3. A «mesma forma funcional» c(SNR) da L161 costura três pontos de DOIS estimadores (C2: VP no domínio do tempo, sinal com sinal, γ=0; C5: PE IMR, |viés| em a × |δ|, células com a=0 e a=1) — não é uma curva. A bancada pode explorar a inconsistência.
4. Não é BLOQUEANTE: E1.4 é «controle», o teste real é E1.1–E1.3; a correção abaixo é suficiente e a ordem não se desestrutura.

## 5. Correção final (texto pronto)
Ver campo `correcao_ajustada` da saída estruturada (também reproduzida ao fim deste arquivo).

### Texto de substituição
**L133 (trecho «Dependente de SNR … (OK para todas)»):**
Dependente de SNR (calibrável, encolhe com SNR, não com N) — dois estimadores distintos, que NÃO formam uma curva única: (i) estimador C2 da bancada (projeção variável no domínio do tempo, RG γ=0, ruído OU+branco sintético), viés com sinal: **+0,030 ± 0,013 @SNR20 (N = 50, mediana +0,015, 2,3σ) — refeito pela gerência com N = 2000: +0,0103 ± 0,0023 @20, +0,0026 ± 0,0011 @40, +0,00013 ± 0,00022 @200 (≈ 4/SNR²)** `[REAL no escopo sintético]`; (ii) recuperação PE IMR da C5 (mesma família, |viés em a| × |δ_R-B|, mediana de 8 células, N = 206 draws/célula): **0,0083 @SNR40 (2,1× o piso do R-B; viés em a de 14–102 % do efeito), 0,0011 @SNR200 (OK para todas)** `[REAL nos arquivos da bancada; DERIVED na conversão]`.

**L161 (E1.4):**
4. O viés do estimador por SNR como controle da forma funcional, **refeito pela bancada com N ≥ 1000 por ponto (SNR 20/40/200) no estimador C2 antes de servir de controle** (hoje: +0,030 ± 0,013 @20 com N = 50; a gerência mediu +0,0103 ± 0,0023 com N = 2000 — `revisao\ceticos\c2_refeito\`), separado da recuperação IMR da C5 (|viés| em a × |δ|: 0,0083 @40; 0,0011 @200), **sem costurar os dois estimadores numa só curva c(SNR)**.

**L71 (trecho entre parênteses):**
(a bancada mediu +0,030 ± 0,013 em ruído sintético SNR 20 com efeito nulo, N = 50; refeito com N = 2000: +0,010 ± 0,002) [REAL no escopo sintético]
