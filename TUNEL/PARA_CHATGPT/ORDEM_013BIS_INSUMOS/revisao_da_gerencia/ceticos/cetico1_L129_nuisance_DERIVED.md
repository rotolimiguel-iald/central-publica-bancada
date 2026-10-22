# CÉTICO 1 — achado L129 §4.0(d): «Leitura da gerência [DERIVED]: não é um deslocamento físico comum; é um nuisance c(σ) a modelar»

**Veredito: refutado = false. Gravidade mantida: IMPORTANTE.**

## O que foi medido (script, não memória)

Fonte: `medir/C_piso_sistematico/C_piso_sinais_catalogo.json`, bloco `b_F_catalogo_GWTC5_31` (N = 31).

| quantidade | valor lido | usado na ordem L129 |
|---|---|---|
| WLS c₀(σ→0) | −0,06105 ± 0,06832 | −0,061 ± 0,068 ✓ |
| WLS k | +0,7917 ± 0,3693 | +0,79 ± 0,37 ✓ |
| Spearman(mediana, σ) recalculado dos 31 | 0,4762, p = 0,00677 | 0,476, p = 0,0068 ✓ |
| subamostras σ<0,15 / <0,20 / <0,25 | −0,0002±0,050 / +0,032±0,041 / +0,038±0,036 | ✓ |

Distâncias em σ, calculadas do mesmo bloco:
- hipótese «deslocamento físico comum, sem forma» (k = 0): k/σ_k = **2,14σ**;
- hipótese «c₀ = +0,0668» (o offset físico igual à média do catálogo): (0,0668 − c₀)/σ_c₀ = **1,87σ**;
- c₀ = 0: 0,89σ; c₀ = −0,020: 0,60σ (a própria L129 diz «não separa 0 de −0,020»).

## Por que o achado se sustenta

1. Os números da L129 estão certos, mas a frase «não é um deslocamento físico comum» **não é derivada deles**: a alternativa física (k = 0, c₀ ≈ +0,067) é desfavorecida a ~2σ, não excluída. Um [DERIVED] a 2σ não é derivação; é leitura. A própria L129 admite que c₀ não separa 0 de −0,020 a 0,6σ — o ajuste não tem poder para decidir a natureza do +0,07.
2. Inconsistência interna: L71 (Parte A, recibo do `C4_ADENDO_DTAU_POSITIVO.md`) manda manter «hipóteses nomeadas com estatuto, nenhuma escolhida», entre elas «física nova [CONJECTURE]». A L129 escolhe uma (sistemática/nuisance) e a rotula [DERIVED]. A bancada pode ler a L129 como revogação da L71.
3. A fonte (`medir/SINTESE.md:39`) chama isto de «Leitura do sintetizador», **sem estatuto**; a ordem promoveu a leitura a [DERIVED] sem medição nova. L11: «hipótese nova é [CONJECTURE]».
4. O uso operacional (E1 L157–163, E2 L168) **não depende** do rótulo: modelar c(σ) como nuisance é a única rota que se calibra por injeção (CRITICO.md:48 B1, :50 B2). A correção preserva tudo isso e só corrige o estatuto.

## Por que não é BLOQUEANTE

Não move gate, não fabrica número, não decide o que é do operador (partição), e a estatística de E2 já trata c(σ) como nuisance com calibração. É erro de estatuto que a bancada pode explorar (citar a gerência como tendo «derivado» que o +0,07 não é físico) — IMPORTANTE.

## Correção FINAL (substituir na L129 a frase em negrito, do «**Leitura da gerência» até «(0,6σ).**»)

**Leitura da gerência `[CONJECTURE — hipótese de trabalho, não escolhida]`: o +0,07 é compatível com um nuisance c(σ) (Spearman 0,476; c₀ compatível com 0 e com −0,020 a 0,6σ; a alternativa «deslocamento físico comum, k = 0» fica a 2,1σ — desfavorecida, não excluída); as quatro hipóteses da L71 (§3 C4) permanecem nomeadas, nenhuma escolhida; o registro E2 modela c(σ) como nuisance porque é a única que se calibra por injeção. Hoje c₀ não separa 0 de −0,020 (0,6σ).**

Ajuste de forma ao texto do revisor: acrescentei o «2,1σ» medido (k/σ_k = 2,14), para que a frase carregue o número que a distingue de uma derivação, e mantive a última sentença original da ordem.
