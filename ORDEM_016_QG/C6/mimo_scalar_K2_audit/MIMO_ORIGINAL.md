# C6 — Parametrix escalar sem massa até K² e distância bilocal em RNC

**Escopo desta unidade.** Auxiliar euclidiano de dimensão 4, forma-espacial de curvatura constante K; sem horizonte, sem estado físico; parametrix singular de Hadamard/heat com **termo suave adicional = 0**; prescrição parcial **R_bal rotulada + linha suave**, não Rraw. Uma pergunta: a construção do código coincide com a prescrição anterior, ou introduz termo suave não autorizado? Resposta e recorrências abaixo. Nada foi executado; tudo é derivação analítica sobre os trechos fornecidos, com números **lidos** do código e reconstruídos à mão. A crítica tensorial anterior não se repete (uso dela apenas o que é insumo escalar).

---

## A. Distância bilocal em RNC `[DERIVED]`

Carta RNC centrada em *o*, pontos em x, y. Notação: A=|x|², B=|y|², C=x·y, w=|x−y|²=A+B−2C. Lei dos cossenos de curvatura constante (com κ²=K): cos(κc)=cos(κa)cos(κb)+K·C·sinc(κa)sinc(κb). Expandindo em K e resolvendo ordem a ordem:

- K⁰: d₀ = w ✓
- K¹: d₁ = −(AB−C²)/3
- K²: d₂ = −(A+B−4C)(AB−C²)/45

Verifiquei d₁ e d₂ por conta própria (coeficiente de κ⁶: d₂ = d₀d₁/6 − d₀³/360 − 2·RHS₆ = [−(A+B−4C)(AB−C²)]/45, resíduo **0**). Confere com `distance1` e `distance2` do motor. **Testes de sanidade:** y=0 ⇒ d₁=d₂=0 (centrado num ponto, r²=|x|² exato); x,y colineares com *o* ⇒ AB−C²=0 ⇒ r²=w exato (pontos sobre a mesma geodésica). A expansão é identidade da lei dos cossenos, truncada em K² — não há gauge nem liberdade.

```
r² = w + K d₁ + K² d₂ + O(K³)
d₁ = −(AB−C²)/3 ;  d₂ = −(A+B−4C)(AB−C²)/45
```

## B. Parametrix escalar independente até K² `[DERIVED]`

Operador radial em curvatura constante, n=4: ∇²f = f″ + (3√K·cot(√K r))f′, com 3√K cot(√Kr) = 3/r − Kr − K²r³/15. Em z=r²:

```
∇² = 4z∂²_z + (8 − 2Kz − (2/15)K²z²)∂_z ≡ ∇²₀ + K L₁ + K² L₂
∇²₀ = 4z∂²+8∂ ; L₁ = −2z∂ ; L₂ = −(2/15)z²∂
```

**Série da distância:** OK. **Coeficiente de transporte U0:** para escalar, U0=Δ^{1/2}=(√Kr/sin√Kr)^{3/2}. Expandindo: ln U0 = u²/4 + u⁴/120 ⇒ U0 = 1 + Kz/4 + 19K²z²/480 (duas rotas independentes: razão sin/u e exp de log; resíduo 0). **Coeficiente do log:** B(z) = −U1/4 + U2·z/16. Recorrência:

- h₀ = 1/z: ∇²₀h₀ = 0 ✓
- h₁: ∇²₀h₁ = 2z h₀′ = −2/z ⇒ h₁ = 1/4 − (1/2)ln z. O log é **forçado** pela fonte 2K/z; o 1/4 é U0.
- h₂: ∇²₀h₂ = 2z h₁′ + (2/15)z²h₀′ + def ⇒ h₂ = 19z/480, sem log nesta ordem.

Com H = U0/z − (K/2)ln z (termo suave adicional zero):

```
∇²H|_{K²} = 19/60 + 1 + 2/15 = 29/20  ⇒  defeito Euler = 29K²/20 (constante)
```

Coeficiente K² bilocal de H (o `base` do código):

```
K²[H] = d₁²/w³ − d₂/w² − d₁/(2w) + 19w/480
```

que é exatamente o `base` de `scalar_second_curvature_engine.py`: `distance1**2`, `−distance2`, `−distance1/2`, `19/480·w` — os quatro termos casam coeficiente a coeficiente, com as potências de w (3, 2, 1 no denominador; +1 no numerador). Onde cada um nasce: os três primeiros e o 19/480 vêm de U0/z (ver expansão abaixo); o `−d1/2` vem de −(K/2)ln r² = −(K/2)ln w − K²d₁/(2w)+O(K³).

```
U0/z = 1/w + K(1/4 − d₁/w²) + K²(d₁²/w³ − d₂/w² + 19w/480)   [os d₁/(4w) cancelam]
```

## C. Coincide com a prescrição? — **SIM, no composto** `[DERIVED]`

Prescrição: H = U0/r² − U1 ln(r²)/4 + U2 r² ln(r²)/16. O que o `curved_parametrix_euler_defect_check` declara (u1, a2) dá, para e=0: u1 = 2K + (29/60)K²r², a2=U2 = 29K²/15. Substituindo:

```
−u1 ln r²/4 + a2 r² ln r²/16 = −(K/2)ln r² + K²r²ln r²·[−29/240 + 29/240] = −(K/2)ln r²
```

Os termos de log em K² **cancelam identicamente** (U2/16 = u1^{(1)}/4 = 29K²/240). Logo o composto da prescrição é exatamente `U0/r² − (K/2)ln r²`, que é o que o motor implementa. Onde o split (U1 com parte em z, U2 ≠ 0) é convenção de parametrização do log (gauge U1→U1+4λz, U2→U2+16λ não muda B(z)); o invariante é **B(z) = −K/2** até K². O motor está no gauge em que as duas peças de log K² são nulas; o check está em outro gauge; o composto coincide. **Nenhum termo suave não autorizado:** os 19/480·w são o coeficiente de U0=Δ^{1/2}/z (transporte), não um termo de estado; e o `−d1/2` é a expansão do log da distância bilocal, não um termo liso acrescentado.

## D. Defeito Euler `[DERIVED, conferido com o excerto]`

- Massless (e=0): def = ∇²H = **29K²/20**, constante (∂_r = 0 e direcionalmente independente; `eq(...coeff(K,2),r)=0` e `direction_independent=True` no check).
- Com potencial e (forma geral do check): a2 = e²/2 + 2Ke + 29K²/15, def = 3a2/4.
- Um W suave para bisolução exata exigiria L W = −3a2/4 = −29K²/20 (`L_W_required_for_bisolution`); o código **não** o adiciona — corretamente: adicioná-lo seria termo de estado. "Termo suave adicional zero" implica defeito ≠ 0; isso é a situação padrão de Hadamard (parametrix não é função de Green), **não** um erro.

Resíduos que computo e exibo: lei dos cossenos residual = 0 nos coeficientes K⁰…K³; cancelamento de log = 0 (29/240 − 29/240); radial residual = 29/20 exato. **Não identifiquei erro de coeficiente no código.** A única "leitura falsa" possível tem resíduo exibível: quem ler a prescrição literalmente como U1=2K (só) e U2=29K²/15 (só) introduz um termo espúrio +29K²z ln z/240, que em ∇²H gera singularidade de log (29/30)K² ln z — artefato de leitura, não do código.

## E. Derivada Y do defeito suave no gráfico Eφ·dφ `[DERIVED]`

O defeito K² é **constante** (29K²/20), sem dipolo (∂_r = 0; sem dependência direcional). Logo **∂_Y(defeito) = 0 nesta ordem** e pode ser descartado no gráfico Eφ·dφ **se a derivada cai no defeito**. Ressalvas obrigatórias: (i) se a derivada cai em φ (E·∂φ), o **valor** 29K²/20 entra e não se descarta; (ii) a constância vale nesta ordem e neste truncamento — em O(K³) o defeito ganha dependência em r e o descarte deixa de ser licenciado; (iii) se o gráfico usa o defeito em pontos separados (bilocal), o descarte não está coberto por estas verificações.

## F. Valor coincidente × afirmação bilocal `[REAL/OPEN]`

- **Valor coincidente:** lim_{r→0}∇²H = 29K²/20 — estabelecido (e o ∂_r nulo da constante, e a independência direcional).
- **Afirmação bilocal:** o jet K² de H (os quatro termos) e a expansão de r² são genuinamente bilocais e foram derivados analiticamente acima; o que **não** está estabelecido é "o defeito é constante em (x,y) para toda separação e toda ordem" — isso é afirmação mais forte do que os checks (que são de coincidência e do truncamento K²). Além disso, os valores de ordem 0 e 1 são comparados com o `KERNELS.json` antigo (coincidem); **em ordem 2 não há valor antigo para comparar** — a coincidência em K² com a prescrição anterior é analítica/estrutural (item C), não casamento de valores.

## G. Lacunas declaradas

Os motores `labelled_bilocal_jet_engine`, `balanced_log_pair_engine` e `smooth_line_compatibility_check_v2.multiply` **não estão nos trechos carregados**; a semântica dos rótulos `(3,0)`, `(2,0)`, `T.F`, `T.ONE` e o tratamento da linha suave em R_bal não podem ser auditados aqui. O que é auditável e foi auditado: o conjunto de coeficientes, a estrutura analítica, as expansões geométricas (densidade √g = 1 − Kz/2 + 13K²z²/120 e inversa (1/3), (1/15) conferem com curvatura constante) e o drift (−2x_j, −(4/15)xx·x_j, reconstruídos à mão). Os jatos K⁰/K¹ delegados a `L.scalar` ficam fora desta unidade.

---

## Veredito C6

**A construção coincide com a prescrição singular Hadamard/heat até K² (no composto); não introduz termo suave não autorizado.** U0=Δ^{1/2}=1+Kz/4+19K²z²/480; B(z)=−K/2; os termos de log K² cancelam identicamente (U2/16=u1^{(1)}/4=29K²/240); K²[H]=d₁²/w³−d₂/w²−d₁/(2w)+19w/480, com r²=w+Kd₁+K²d₂. **Defeito Euler = 29K²/20 = 3a2/4** (a2=29K²/15 no massless; e²/2+2Ke+29K²/15 com potencial) — não nulo, como manda a teoria, e não escondido pelo código. ∂_Y do defeito suave pode ser descartado em Eφ·dφ **nesta ordem e só se a derivada cai no defeito**; valor coincidente ≠ afirmação bilocal. `[DERIVED + REAL nos números lidos; rótulos/motores não auditáveis = lacuna declarada]` Nada disto confirma física; `NOT_FALSIFIED` não é `CONFIRMED`.