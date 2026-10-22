# REVISÃO ADVERSARIAL — lente ESTATÍSTICA E PODER (ORDEM 013-bis §4.0, E0–E6)

**Data:** 22/09/2026 · **Revisor:** Claude (subagente da gerência) · **Objeto:** `bis\ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` (287 linhas) · **Escrita:** só nesta pasta. Bancada só leitura; nenhum processo tocado.
**Refeito por script:** `refazer_estatistica.py` → `REFEITOS_REVISAO.json` (a partir de `C4_CATALOG_220.json` da bancada, sha16 `93bdc413130d294a`, `C4_JOINT_MODES.json` `8b2e0fea734caed2`, `d2_resultado.json` `d7402bae7f41da00`). β em runtime = 0,012031300400803142.

## 1. O que bate (refeito ou conferido no arquivo-fonte)

| número da ordem | linha | meu valor | fonte |
|---|---|---|---|
| z_comb união39 0,654/1,167/1,205/2,322 | 123 | A (σ = std) 0,6543/1,1674/1,2050/2,3220; com σ gauss nos 31: 0,613/1,087/1,132/2,182 (≤ 1,2 %) | A_poder_eventos.json; meu script |
| GW250114 σ(δτ̂) 0,058, σ(δf̂) 0,0136, z_i 0,343/0,637/0,641/1,237 | 123 | 0,05795 / 0,01364; 0,342/0,636/0,640/1,233 (gauss) | C4_CATALOG_220 rows[31] |
| 1/1/3 eventos com σ ≤ 0,06/0,10/0,15; mediana 0,24 | 123 | 1/1/3 (9 ≤ 0,20); 0,2414 | meu script |
| N50 GW250114-like 212/62/61/16; mistura ≈2.100/669/618/166; crítico 2.062/657/605/163 | 125 | 213,2/61,9/61,1/16,4 (gauss); mistura 2.062/656/605/163 (gauss) | meu script |
| fator 1,578 = (5+1,28)²/25 | 125 | 1,5783 (z₀,₉₀ = 1,2816); lógica correta para z gaussiano unilateral de variância 1 sob a alternativa | meu script |
| N90 R-B 335 GW250114-like | 125 | 334,6 (de 212,0) / 336,5 (de 213,2) | — |
| spin q05/50/95, sd(pred) 0,002–0,007, z_slope 0,048/0,158/0,054/0,100, N ≥ 3×10⁴–3×10⁵, CE 101–1.083 | 127 | A lever/scaling: idem | A_poder_eventos.json |
| +0,0668 ± 0,0336; 2,59/3,06/3,11/4,15σ; Spearman 0,476 p 0,0068; c₀ −0,061 ± 0,068; k +0,79 ± 0,37; subamostras | 129 | +0,0669 ± 0,0332 (gauss; z 2,01); 2,63/3,09/3,14/4,19 (gauss); Spearman(31) 0,4762 p 0,00677; WLS c₀ −0,06105 ± 0,06831, k 0,7917 ± 0,3693; c₀ vs −0,020: 0,60σ | meu script |
| 112/81/78/44 | 131 | 112,46 / 81,24 / 78,36 / 44,07 | meu script (31×25/z_obs²) |
| pisos 0,0040/0,0074/0,0074/0,0143; família 0,029 (7,3×); −0,042/+0,013; até 0,097; t₀ +0,075; 0,0083@40 (2,1×); 0,0011@200 | 133 | 0,003969/0,007368/0,007413/0,014295; C_piso_sinais_catalogo e C_piso_medicoes conferem | frente C |
| IC90 Poisson [0,035; 3,3]/ano; 1 em 1,45 ano | 135 | [0,0354; 3,272]/ano (Garwood, 1 contagem, 21/14,48 = 1,45 a) | meu script |
| 79–137 e 783–1.363 (×1,578) | 135 | 78,9–137,3; 782,8–1.363,6 | — |
| 2,2–3,1σ (BBH) e 3,4 (×1,99) | 135 | 2,19–3,06 (BBH coerente); 3,40 (C5 ×1,987 + volume BBH máx) | meu script |
| jitter: sd 0,0228; Cauchy 0,022/MAD 0,005; saltos 85,7 %; limiar 25,0; N90 59/38/21; 17.578; 1,09; 13,5×; σ_jit < 0,0243; z 1,43 | 137 | D_consolidado/d2: idem; limiar = z²(p = 2,87×10⁻⁷) na mistura ½δ₀+½χ²₁ = 25,000 (refeito); 23,9 ≙ 4,89σ; Σ(σ₀/σᵢ)⁴ = 1,0899 | meu script |
| pyRing σ ≈ 0,17 (δf̂) | 137 | (0,4291+0,1304)/3,29 = 0,170 em df220 do C4_PYRING | C4_PYRING.json |
| 440: −0,082/−0,197/−0,074/−0,137; 4,1× | 141 | −0,08193/−0,19675/−0,07355/−0,13702; razão 440/220: 4,13 / 5,34 / 1,98 / 1,92 | C4_JOINT_MODES |
| δτ̂₄₄₀ ∈ [−0,35; +3,4] | 141 | aud_6.txt:101 (recalculado pelo auditor 6) | auditoria |
| σ ≈ 3,03·SNR^−0,86; SNR ≳ 95 / ≳ 53 | 149 | A = 3,0266, p = −0,860; 95,5 / 52,7 | B RENDIMENTO_E_5SIGMA |
| 81–542 CPU-h; fator 6,7 | 182 | 3×10⁶–2×10⁷ × 0,0975 s / 3600 = 81,25–541,7; 6,67 | MEDICAO_E (t_onda 0,0975) |
| −0,013 [−0,103; +0,087] | 182 | q05/50/95 dtau220 GW250114 = −0,10335/−0,01340/+0,08731 | C4_CATALOG_220 |
| 157/46/12 injeções; 127k–851k CPU-h; 241–1.612 dias | 183 | 157,0/45,6/12,1; 127,6k–850,7k; 241,7–1.611 | meu script |
| 3G z 3,86/7,03; ~130 / ~33 | 139 | C5_FISHER same_source: 3,8556/7,0277; B: 131,2 / 32,8 **com âncora 0,058@SNR_RD 40** | ver achado A-05 |

## 2. Achados (ordenados por gravidade) — o detalhe está no StructuredOutput; aqui o resumo

- **IMPORTANTE A-01 (l.135):** os limites inferiores de N_alvo em O5 (50 GW250114-like; 496 mistura) e o topo «6,3σ» de R-MOD/R-RAIZ-0 usam o fator ×2,06 (razão de alcance **BNS**) que a própria linha exclui ao dar «2,2–3,1σ» só com BBH. Coerente: 66–87 (C5: 54) / 662–864 (C5: 535); R-MOD 3,9–5,4σ (C5 6,0), R-RAIZ-0 4,0–5,7σ (C5 6,3).
- **IMPORTANTE A-02 (l.149):** «resíduo 0,24 dex» é 0,244 em **ln** (`rendimento_e_5sigma.py:33` usa `np.log`) = 0,106 dex.
- **IMPORTANTE A-03 (l.149):** o corte «σ ≤ 0,06 ≙ SNR_rede ≳ 95» exclui o próprio GW250114 (SNR_rede 76,9; ajuste em 76,9 dá σ = 0,072) e **nenhum** evento do GWTC-5.0 (máx 78,6) — logo a taxa «1 em 1,45 ano» (l.135) seria ZERO pelo critério pré-análise que a ordem manda registrar. Dizer que o ajuste é mediana (metade dos eventos em SNR 95 tem σ > 0,06; dispersão 0,24 em ln), que a âncora está 0,22 abaixo da reta, e mandar contar em vários cortes (≥ 50, ≥ 75, ≥ 95).
- **IMPORTANTE A-04 (l.131 e l.216):** falta o número que a régua da l.11 exige: com o mesmo viés e a mesma estatística, a **RG** é «falsificada» a 5σ em **N ≈ 191** de mistura O4 (31×25/2,014²). É a prova de que o offset fixo em 0 não é teste; deve constar ao lado de 112/81/78/44.
- **IMPORTANTE A-05 (l.139):** «~130 com SNR_RD ≥ 50 / ~33 com ≥ 100» usa a âncora σ = 0,058 @ SNR_RD **40** (B, «pós-fusão ~40»); com a equivalência de Fisher que a própria ordem cita (0,058 ≙ SNR_RD ≈ 34, l.125) dá **96 / 24** (N90 152); e «z = 3,86/7,03 com um só evento de fonte fixa» é a fonte de referência da C5 que em O4 teria SNR40 na janela de 10 t_M — 4,2–4,4× o GW250114 (aud_4). Nenhuma base de SNR está declarada: viola a errata 4 (l.48) da própria ordem. E são N50 numa ordem cuja convenção é 90 % (→ ~207 / ~52 / ~16).
- **IMPORTANTE A-06 (l.125/131/137/139):** convenção de poder mista: (b) declara 90 %, mas «≈2.100/669/618/166» (l.131), «17.578» (l.137; N90 não simulado), «~130/~40/~10» e «5–9» (l.139) são N50 ou pares sem rótulo. Toda N deve levar «(50 %)» ou «(90 %)».
- **IMPORTANTE A-07 (l.133):** «soma-de-QNM … +0,0125 a **+0,062**»: 0,062 é literal em `reconcilia.py:147`; a frente C mede 0,0115–0,0548 (`modelo_QNM_vs_IMR_span_6M_12M`) e C5_BIAS_ABLATION não tem 0,06x em δτ̂. Corrigir para 0,0125–0,055 (3,2–13,8× o piso do R-B). Além disso os dois JSON da frente C dão o **sinal** oposto para a mesma grandeza (medicoes: dtau_SEOB −0,0111; sinais: +0,0111) — a bancada tem de declarar a convenção (δτ̂ = â·δ_RB).
- **IMPORTANTE A-08 (l.133 e l.161):** «+0,030 @SNR20» é média de N = 50 trajetórias sintéticas com sd 0,094 → **+0,030 ± 0,013** (mediana +0,015): 2,3σ. Citado sem erro e usado em E1.4 como controle da forma funcional.
- **IMPORTANTE A-09 (l.135 e l.139):** «R-LIN fecha em ~1 ano de O5», «~1,3 ano», «~3,3 anos» são pontos sem banda no parágrafo que termina «nunca anos» e na ordem que proíbe (§5) «5σ em N anos» como promessa. Ou banda + [DERIVED, cenário] ou retirar.
- **NOTA A-10 (l.125):** «σ = 0,0497 em SNR40 é 2,5–4,4× o GW250114» mistura O4 (4,2–4,4×) e O5 (2,5–2,6×) do aud_4; «com o σ real dá 212»: o reescalonamento do Fisher dá 204; 212/213 é o cálculo direto (std/gauss). «≈2.100» e «≈3.250» não são o mesmo N × 1,578 (3.254 = 2.062 × 1,578; 2.100 × 1,578 = 3.314).
- **NOTA A-11 (l.137):** os N90 da rota IV vêm de MC com σᵢ homogêneo (0,0136), limiar assintótico, 4.000 draws (erro MC ~0,5 % em 90 %); o FPR sob H0 no MC homogêneo fica abaixo da mistura (conservador); «compatíveis» 0,0192 (N = 50) vs 0,0228 são 1,9σ do EP 0,0019. Dizer.
- **NOTA A-12 (l.129):** Spearman só dos 31 (seleção); nos 33 é 0,376 p 0,031 — citar os dois.
- **NOTA A-13 (l.141 e l.188):** a razão 440/220 é 4,1× só no R-B; R-MOD 5,3×, R-RAIZ-0 2,0×, R-LIN 1,9× — dar por leitura.
- **NOTA A-14 (l.143):** «todo N é valor esperado (z ∝ √N)» contradiz a convenção de 90 % da l.125 (N90 não é o N de E[z] = 5).
- **NOTA A-15 (l.154 e l.189):** E0.8 «vereditos hoje» e E4.2 (ln B do 440 nos públicos) são recontagens NÃO-CEGAS — dizer que reemitem a C4 e não são teste.
- **NOTA A-16 (l.182):** «0,095 s por forma de onda» — E mediu 0,0975 s; 81–542 só reproduz com 0,0975.
- **NOTA A-17 (l.183):** 157 injeções/célula vale para σ_inj = 0,0497 (célula SNR40); para a σ típica do catálogo (0,24) seriam ~3.650/célula — dizer que o orçamento é o piso, não o teto.

## 3. Sem achado BLOQUEANTE nesta lente
Nenhum número da §4.0 é fabricado; os hashes citados conferem; NOT_FALSIFIED não vira CONFIRMED; a partição fica no operador; o «E[z] = 5 ≈ 50 %» só aparece para o filtro casado gaussiano (onde é exato) e a rota IV usa MC — a correção do crítico foi incorporada. O limiar 25,0 e o «38» estão certos.
