# CÉTICO 1 — achado «viés do estimador +0,030 @SNR20» (ORDEM 013-bis, linhas 71, 133, 161)

**Veredito: NÃO REFUTADO (refutado=false). Gravidade mantida: IMPORTANTE.**

## O que refiz por script (22/09/2026)
Fonte bruta (só leitura): `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C2_TRAJECTORY_RECOVERY.json`
(sha16 registrado pela gerência em `C_piso_medicoes.json/sources_sha16`: 339be42bec67a48e), `rows[reading=R-A]`
(e as cópias idênticas R-GLOBAL, R-RAIZ-EP4, R-RAIZ-REST: γ≈0 = RG pura), `comparisons[detector_noise=SYNTHETIC_COLORED_OU_PLUS_WHITE].fits[*].dtau`,
N = 50, 0 falhas do otimizador, 0 na borda, GR_reference_SNR = 20, 128 amostras a 4096 Hz.

| estatística | valor medido |
|---|---|
| média | **+0,0303** |
| mediana | **+0,0152** |
| sd REAL das 50 (não o equivalente gaussiano por quantis) | **0,0930** (quantis dão 0,0942 — coerentes) |
| erro padrão da média | **0,0131** |
| t = média/se | **2,31** |
| bootstrap 20.000 reamostras, P(média ≤ 0) | **0,0086** |
| positivos | 29/50 |
| q05 / q95 / min / max | −0,103 / +0,185 / −0,140 / +0,266 |

Os pontos 0,0083 @SNR40 e 0,0011 @SNR200 conferem: `medir\C_piso_sistematico\C_piso_medicoes.json/B_familia_resumo/R-B/same_SNR40_bias_dtau_abs`
{n 8, median 0,00830, mean 0,00905, min 0,0028, max 0,0203} e `same_SNR200_bias_dtau_abs` {n 8, median 0,00106}.
São medianas de |viés| (valor absoluto, sem sinal) de 8 células da C5_IMR_RECOVERY (injeção SEOBNRv4HM recuperada pela mesma família, a = 0).

## Por que o achado está certo, e um agravante
1. A ordem cita «+0,030» nas linhas 133 e 161 (e «+0,030» na 71) **sem erro, sem N e sem mediana**. O número é a média de 50
   trajetórias a 2,3σ de zero; a mediana é metade (+0,015). A própria medição da gerência já tinha o σ por evento
   (`E_C2_vies_GR_com_ruido.sigma_evento_equiv = 0,0942`) e não propagou o erro padrão para a ordem.
2. Com se = 0,013, o ponto SNR20 é **3,3× o piso do R-B (0,0040)**: como «controle da forma funcional» c(SNR) (E1.4, linha 161)
   ele não resolve nada ao nível em que a ordem exige resolução na §4.0 (f). Para se ≤ 0,0040 bastam N ≥ (0,093/0,004)² ≈ 540;
   N ≥ 1000 dá se ≈ 0,0029 e custa segundos (ajuste de projeção variável em 128 amostras).
3. Agravante que o revisor não disse: os três pontos da «mesma forma funcional» vêm de **dois estimadores diferentes** —
   SNR20 é o ajuste de projeção variável da C2 sobre ruído OU+branco sintético (128 amostras); SNR40/200 são |viés| mediano
   de 8 células da recuperação IMR da C5 (família SEOBNRv4HM sobre PSD O4). A ordem não pode mandar ajustar UMA curva c(SNR)
   por três pontos de duas pipelines sem dizê-lo. A correção final abaixo nomeia as duas fontes.
4. Não é questão de gosto: a ordem será imutável e a bancada leria «+0,030» como fato calibrado.

## Correção FINAL (texto exato)
**Linha 133**, substituir
`viés do estimador +0,030 @SNR20, **0,0083 @SNR40 (2,1× o piso do R-B), 0,0011 @SNR200 (OK para todas)**.`
por
`viés do estimador **+0,030 ± 0,013 @SNR20** (média de N = 50 trajetórias sintéticas da C2, mediana +0,015, sd 0,093 — [REAL no escopo sintético, 2,3σ de zero; o erro padrão é 3,3× o piso do R-B, logo este ponto ainda não resolve o piso]), **0,0083 @SNR40 (2,1× o piso do R-B), 0,0011 @SNR200 (OK para todas)** (medianas de |viés| em 8 células da C5_IMR_RECOVERY, mesma família, a = 0 — estimador DIFERENTE do da C2).`

**Linha 161**, substituir
`4. O viés do estimador da bancada por SNR (já medido: +0,030 @20; 0,0083 @40; 0,0011 @200) como controle da mesma forma funcional.`
por
`4. O viés do estimador da bancada por SNR como controle da forma funcional (já medido: **+0,030 ± 0,013 @20**, média de N = 50 na C2, mediana +0,015; **0,0083 @40 e 0,0011 @200**, medianas de |viés| de 8 células da C5 — dois estimadores distintos, ditos). **Antes de servir de controle, o ponto SNR20 é refeito com N ≥ 1000 na mesma pipeline da C2** (se ≤ 0,003 < piso do R-B) e, se couber, um ponto SNR40 na C2 para ligar as duas pipelines; o erro padrão de cada ponto entra no ajuste de c(SNR).`

**Linha 71** (recibo C4_ADENDO), substituir
`(a bancada mediu +0,030 em ruído sintético SNR 20 com efeito nulo) [REAL no escopo sintético]`
por
`(a bancada mediu +0,030 ± 0,013 em ruído sintético SNR 20 com efeito nulo, N = 50, mediana +0,015) [REAL no escopo sintético, 2,3σ]`

## Estatuto
Todos os números acima: [REAL — recalculados por script a partir dos fits brutos da bancada em 22/09/2026]. Nenhum gate movido.
