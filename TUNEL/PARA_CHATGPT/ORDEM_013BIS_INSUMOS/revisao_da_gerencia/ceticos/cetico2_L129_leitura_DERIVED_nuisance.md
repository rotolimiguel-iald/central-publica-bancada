# CÉTICO 2 — achado L129 §4.0(d): «Leitura da gerência [DERIVED]: não é um deslocamento físico comum; é um nuisance c(σ)»

**Veredito: refutado = false. Gravidade mantida: IMPORTANTE.**

## O que foi medido (script sobre `medir/A_poder_eventos/A1_por_evento.csv`, sel31 / all33)
- média ponderada δτ̂₂₂₀: sel31 +0,0668 ± 0,0336 (ordem L129: idem) · all33 +0,0614 ± 0,0331
- Spearman(mediana, σ): sel31 0,460 (p 0,009) com σ=std do CSV; o arquivo C (`C_piso_medicoes.json` /F_catalogo_GWTC5_31) dá 0,476 (p 0,0068) — reproduzido dentro da definição de σ; **all33: 0,353 (p 0,044) / arquivo C 0,376 (p 0,031); GWTC-3 (18): 0,304 (p 0,22) — não significativo**
- regressão ponderada mediana = c₀ + k·σ: sel31 c₀ = −0,057 ± 0,068, k = +0,76 ± 0,36 (arquivo C: −0,061 ± 0,068 / +0,79 ± 0,37 — reproduzido); k está a 2,1σ de zero.
- **Discriminador da frase «não é físico»:** um deslocamento físico comum de +0,067 (o próprio valor observado) contra c₀(σ→0) = −0,061 ± 0,068 está a (0,067+0,061)/0,068 = **1,9σ**. Ou seja: o dado exclui «deslocamento físico comum» só a ~2σ, e a correlação com σ é dependente da amostra (0,476 → 0,376 → 0,30).

## Por que o achado se sustenta
1. L11 fixa «hipótese nova é [CONJECTURE]»; L71 manda a bancada nomear quatro hipóteses «com estatuto, nenhuma escolhida», inclusive «física nova [CONJECTURE]». L129 escolhe uma delas («não é um deslocamento físico comum») e a rotula [DERIVED]: inconsistência interna que a bancada pode explorar (citar L129 para não redigir a C4_ADENDO com as quatro em pé).
2. [DERIVED] cabe ao que se calcula do dado: a média ponderada, o Spearman, o ajuste c₀/k, a compatibilidade de c₀ com 0 e com −0,020 a 0,6σ. «Não é físico» é inferência a 1,9σ sobre uma correlação de 2,1σ que cai com a amostra — é leitura, e leitura que escolhe hipótese é [CONJECTURE].
3. A decisão de DESENHO (modelar c(σ) como nuisance no registro E2, L168) é legítima e não depende da leitura ontológica: c(σ) é a única componente calibrável por injeção (E1/L157–163). Separar «o que o registro faz» de «o que a gerência acha que o +0,07 é» resolve sem tocar E1/E2.
4. Não é BLOQUEANTE: não decide o que é do operador (partição/relógio), não fabrica número, e o registro E2 continua executável. Não é NOTA: o estatuto errado numa ordem imutável vira fato para a bancada e viola L11.

## Correção FINAL (substituir a frase em negrito no fim de L129)
**Leitura da gerência `[CONJECTURE — hipótese de trabalho, não escolhida]`: o +0,07 é compatível com um nuisance c(σ) do estimador/seleção (Spearman 0,476 nos 31, p = 0,0068 — 0,376, p = 0,031 nos 33; c₀ compatível com 0 e com −0,020 a 0,6σ, e um deslocamento físico comum de +0,067 só é afastado a 1,9σ); as quatro hipóteses da C4_ADENDO (§2, L71) permanecem nomeadas, nenhuma escolhida; o registro E2 modela c(σ) como nuisance porque é a única componente que se calibra por injeção (E1), não porque o dado tenha decidido a natureza do +0,07.**
