# CÉTICO 1 — achado A-04 (lente estatistica_poder), ORDEM 013-bis l.131 e l.216

**Veredito: NÃO REFUTADO (refutado=false). Gravidade mantida: IMPORTANTE.**

## O número, refeito por script (não de memória)
Fonte: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C4_CATALOG_220.json` (sha16 `93bdc413130d294a`, só-leitura),
31 eventos (33 menos os dois controles GW191109_010717 e GW200208_130117), σ gaussiano = (q95−q05)/(2·1,645), pesos 1/σ².
Script/saída: `revisao/ceticos/cetico1_A04_recompute.txt`.

| grandeza | refeito aqui | REFEITOS_REVISAO.json | CRITICO_completude/REFEITOS.json |
|---|---|---|---|
| média ponderada δτ̂₂₂₀ (31) | +0,0669 ± 0,0332 | 0,06691 / 0,03322 | 0,06691 / 0,03322 |
| z contra 0 (RG, offset fixo 0) | 2,014 | 2,014 | 2,014 |
| N 5σ CONTRA A RG (viés persistente) | **191,1** | 191,06 | (não calculado) |
| N 5σ contra R-B / R-MOD / R-RAIZ-0 / R-LIN | 112,5 / 81,2 / 78,4 / 44,1 | 112,46 / 81,24 / 78,36 / 44,07 | 112,48 / 81,25 / 78,37 / 44,07 |

Mesma lei de escala (N = 31·25/z²) que a ordem já usa na l.131 para os 112/81/78/44 — logo o 191 é o mesmo cálculo,
aplicado à predição da RG (0) em vez da predição da leitura. Nada de novo entra; só falta o número ao lado.

## Por que não refuta
1. A ordem, na l.11, obriga: «nunca exclua uma leitura por um critério que excluiria a própria RG». A l.131 dá o N em que o
   critério exclui as leituras e **não** dá o N em que exclui a RG. A l.129 diz «o mesmo desvio que põe a RG a 2σ» (hoje), mas
   não a projeção a 5σ — é exatamente a projeção que a l.131 faz para as leituras. Assimetria interna: a régua pede a simetria.
2. Ambiguidade explorável pela bancada: 112 < 191 lê-se, sem o 191 ao lado, como «a leitura cai antes da RG, o teste
   discrimina». A diferença 112→191 vem de δ_RB = −0,020 (a predição relativa), que é o sinal do teste **relativo** da l.169
   (ln B leitura vs RG) — e esse sinal só é lícito com o nuisance c(σ) calibrado (E1). O offset fixo em 0, sozinho, falsifica a RG
   em ~191 e portanto não é teste de leitura nenhuma. Sem o número a frase «PROIBIDO» fica por decreto; com ele fica por medida.
3. A ordem é imutável depois de publicada; custo da correção: uma oração; risco de omiti-la: a bancada recebe o 112 como fato
   discriminante.

## Correção FINAL (texto exato para a l.131; e a l.216 ganha o parêntese)
l.131 — substituir o trecho «eventos de mistura O4 — **muito antes** dos ~2.100 / 669 / 618 / 166 do 5σ de detecção.» por:

«eventos de mistura O4 — **muito antes** dos ~2.100 / 669 / 618 / 166 do 5σ de detecção — **e, pelo mesmo critério e o mesmo
viés, CONTRA A PRÓPRIA RG em N ≈ 191** (31×25/2,014²; z_vs_0 = 2,014 nos 31) `[DERIVED sobre REAL — refeito pelo revisor e pelo
cético do arquivo da bancada]`. **O critério exclui a RG; logo, pela régua (§0), não exclui leitura nenhuma.** A diferença
112 → 191 é só δ_RB = −0,020, isto é, o sinal do teste RELATIVO à RG (§3, ln B) — que só vale com o nuisance c(σ) de E1 calibrado.»

l.216 — substituir «(é o falsificador espúrio a ~112 eventos)» por «(é o falsificador espúrio: 5σ contra o R-B a ~112 eventos
e contra a própria RG a ~191)».
