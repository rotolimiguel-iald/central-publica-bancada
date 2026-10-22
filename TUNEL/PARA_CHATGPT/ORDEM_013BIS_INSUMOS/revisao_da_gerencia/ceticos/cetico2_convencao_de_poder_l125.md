# CÉTICO 2 — achado «convenção de poder declarada e não aplicada» (ORDEM 013-bis, l.125 §4.0 b/e/h/i)

Veredito: **refutado = false** (achado confirmado por script). Gravidade mantida: **IMPORTANTE**.

## O que medi (22/09/2026)

Fator: z_0.90 = 1,28155; N90/N50 = (5+1,28155)²/25 = **1,5783** (scipy.stats.norm.ppf; confere com REFEITOS_REVISAO.json `fator_N90_N50_filtro_casado` 1,5783156). Vale para o filtro casado com z ∝ √N.

Origem de cada N da §4.0 e seu poder real:
- l.125 (b): 212/62/61/16 e ≈2.100/669/618/166 (A2_tabela_5sigma.csv: `N_5sigma_like_GW250114_O4`, `N_5sigma_same_mix_matched_O4`, fórmula 25/z², i.e. E[z]=5 → **50 %**). N90 refeito: like 334,6/97,9/96,3/25,3; mistura 3.327/1.056/975/262 (base A, 2108/669/618/166) ou 3.254/1.037/955/257 (base crítico 2062/657/605/163). O «≈ 3.250» da ordem é da base do crítico, enquanto o «≈ 2.100» da mesma frase é da base A — mistura de bases sem dizer.
- l.131 (e): 112/81/78/44 = 31·(5/z_obs_vs_pred)² → **50 %** (REFEITOS: 112,46/81,24/78,36/44,07); N90 = 177/128/124/70. Comparação 50 vs 50 é consistente, mas sem rótulo.
- l.137 (h): «N₉₀ = 59 / 38 / 21» são poder 90 % (d2_resultado.json cases 1 e 2: N_LRT_power90 59 e 21; o 38 vem do medidor a 0,0228). **«17.578 — inviável» é N_LRT_power50 (case 4); `N_LRT_power90: null`, não simulado.** Está na mesma frase que os N₉₀, sem rótulo — é o erro mais nítido.
- l.139 (i): «~130 / ~33» = B_catalogos/rendimento_e_5sigma.py l.53/59: `N = 25/mean(z²)` → **50 %** (FRENTE_B_RESULTADO.md l.46: 131 / 33). N90 = 207 / 52 (REFEITOS `3G_N5_RB_ancora_SNR40.0.N90_SNR50` 207,3). «~40» (R-MOD 43, R-RAIZ-0 38) e «~10» (R-LIN) idem, 50 %. «5–9» = par **50 %/90 %** para σ_jit = 0,019 (d2 case 7: power50 5, power90 9; SINTESE.md l.99 «0,005: 5/9»), não uma banda de σ_jit.
- l.135 (g) já aplica o rótulo duplo («N₅₀; 79–137 a 90 %») — prova que a convenção era para valer em toda a §4.0 e não valeu.

## Por que IMPORTANTE e não BLOQUEANTE
A l.148 (E0 item 2) exige explicitamente «N_alvo a 90 %… com o fator 1,578 impresso», então a bancada tem uma instrução correta a jusante. Mas a §4.0 é o «número que a gerência mediu» e a bancada pode registrar 17.578, ~130 ou ~2.100 como N_alvo citando a própria ordem; a inconsistência é interna e explorável. Não induz erro de física; não decide nada do operador.

## Correção final (texto exato, ao lado do estilo da ordem)
Ver campo `correcao_ajustada` do StructuredOutput (reproduzido abaixo).
