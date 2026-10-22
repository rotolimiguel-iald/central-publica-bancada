# ORDEM_016, A-7.b — Operador adjunto dos jatos externos

## 1. Resultado principal: o operador adjunto

**Definição (adjunto exato sem perda).** Para os jatos externos $h_X$ (até ordem 2) e $c_Y$ (até ordem 1), com pesos exponenciais $\chi_X = e^{\lambda\cdot X}$ e $\chi_Y = e^{\eta\cdot Y}$:

$$\boxed{(\partial_X^I)^\dagger = (-1)^{|I|}\,(d+\lambda)^I}$$

$$\boxed{(\partial_Y^J)^\dagger = (d-\eta)^J}$$

onde $I = (i_1,\dots,i_{|I|})$ e $J = (j_1,\dots,j_{|J|})$ são palavras ordenadas, $d = \partial_x$ com $x = X-Y$, e $(d+\lambda)^I = \prod_k (d^{i_k}+\lambda^{i_k})$, $(d-\eta)^J = \prod_l (d^{j_l}-\eta^{j_l})$.

**Composição operador-adjunto único:**

$$\mathcal{A}^{I,J} = (-1)^{|I|}\,(d+\lambda)^I\,(d-\eta)^J$$

Este operador reduz sem perda: a integração por partes é exata, e todos os termos de $\lambda$ e $\eta$ (jets exponenciais completos) são preservados — não apenas a parte de gradiente.

---

## 2. Derivação

**Lado $X$ ($\partial_X = d$):**

$$\int e^{\lambda\cdot X}\,(\partial_X^i h)(X)\,g(x)\,dX = -\int h(X)\,\partial_X^i\!\left[e^{\lambda\cdot X} g(x)\right]dX = -\int e^{\lambda\cdot X}\,h(X)\,(d^i+\lambda^i)\,g(x)\,dX$$

Para $|I| = p$ integrações por partes: sinal $(-1)^p$, operador $(d+\lambda)^I$.

**Lado $Y$ ($\partial_Y = -d$):**

$$\int e^{\eta\cdot Y}\,(\partial_Y^j c)(Y)\,g(x)\,dY = -\int c(Y)\,\partial_Y^j\!\left[e^{\eta\cdot Y} g(x)\right]dY$$

Com $\partial_Y = -d$, o operador $(\partial_Y + \eta)^j$ age como $(-d+\eta)^j = (-1)^j(d-\eta)^j$, e o sinal $(-1)^q$ das $q$ integrações por partes **cancela** com o $(-1)^q$ de $(-d+\eta)^q$. Resultado: sinal $+1$, operador $(d-\eta)^J$.

**Sinal duplo do $Y$ é crucial:** a adjunção de $\partial_Y^j$ dá $(d^j - \eta^j)$, **não** $(d^j + \eta^j)$. Um erro de sinal aqui é o "sinal errado no extremo $Y$" que os testes devem detectar.

---

## 3. Sinais das duas contrações

| Contração | Propagador | Sinal | Nota |
|---|---|---|---|
| $c_X\,\bar{b}c_Y\,c_Y$ (ordem $C_X V_{gh,Y}$) | $\langle c(X)\bar{b}c(Y)\rangle = +\delta\,f$ | $\mathbf{+1}$ | Ghost externo à direita ($c_Y$); contração de posições adjacentes (1,2), sem permutação. |
| $b_X\,h_Y$ (corrente $J_b$) | $\langle b_\nu(X)h_{ab}(Y)\rangle = -(\delta_{bn}d_a+\delta_{an}d_b)\,f$ | $\mathbf{-1}$ | **Preservar** o sinal do propagador; a adjunção não adiciona sinal extra sobre ele. |

Para a ordem revertida $\bar{b}c(X) c(Y)$: propagador $-\delta f$ (sinal de ordem ímpar revertida). Mas na ordem $C_X V_{gh,Y}$ especificada, a contração relevante é $\langle c\,\bar{b}c\rangle = +\delta f$.

---

## 4. Potências/composições: casos específicos

### $I = (i)$ — um derivada

$$(\partial_X^i)^\dagger = -(d^i + \lambda^i)$$

### $I = (i,i)$ — duas derivadas iguais (multiplicidade 2)

$$(\partial_X^i\partial_X^i)^\dagger = (d^i+\lambda^i)^2 = d^{ii} + 2\lambda^i d^i + (\lambda^i)^2$$

O coeficiente **2** no termo cruzado $\lambda^i d^i$ é o fator de Leibniz/multiplicidade para derivadas iguais. O termo $d^{ii}$ (= $h''$ na linguagem do teste) **não pode ser omitido**.

### $I = (i,j)$, $i \neq j$ — duas derivadas distintas

$$(\partial_X^i\partial_X^j)^\dagger = (d^i+\lambda^i)(d^j+\lambda^j) = d^{ij} + \lambda^j d^i + \lambda^i d^j + \lambda^i\lambda^j$$

Sem fator de multiplicidade (derivadas distintas comutam).

### $J = (j)$ — uma derivada em $Y$

$$(\partial_Y^j)^\dagger = (d^j - \eta^j)$$

---

## 5. Fatores de Leibniz em produtos de dois propagadores

Quando o adjunto age num produto $G_1(x)\,G_2(x)$ de duas linhas de propagador, a derivada distribui-se por Leibniz.

**$I = (i)$ sobre $G_1 G_2$:**

$$(d^i+\lambda^i)[G_1 G_2] = (d^i G_1)G_2 + G_1(d^i G_2) + \lambda^i G_1 G_2$$

3 termos (2 de Leibniz + 1 de $\lambda$).

**$I = (i,i)$ sobre $G_1 G_2$:**

$$(d^i+\lambda^i)^2[G_1 G_2] = (d^{ii}G_1)G_2 + \underbrace{2(d^i G_1)(d^i G_2)}_{\text{multiplicidade 2}} + G_1(d^{ii}G_2) + 2\lambda^i[(d^i G_1)G_2 + G_1(d^i G_2)] + (\lambda^i)^2 G_1 G_2$$

O termo cruzado $(d^i G_1)(d^i G_2)$ tem coeficiente **2** — é o fator de Leibniz para duas derivadas iguais num produto.

**$I = (i,j)$, $i\neq j$, sobre $G_1 G_2$:**

$$(d^i+\lambda^i)(d^j+\lambda^j)[G_1 G_2] = \sum_{\text{Leibniz}} + \text{termos }\lambda$$

com 4 termos puros de derivada (cada derivada vai para $G_1$ ou $G_2$ independentemente): $(d^{ij}G_1)G_2$, $(d^i G_1)(d^j G_2)$, $(d^j G_1)(d^i G_2)$, $G_1(d^{ij}G_2)$ — sem fator de multiplicidade (derivadas distintas).

---

## 6. Testes polinomiais exatos

### Teste A — omissão de $h''$ (ordem 2, $I=(i,i)$, $J=0$)

**Identidade formal:** $(\partial_X^i)^2 = \left[-(d^i+\lambda^i)\right]^2 = (d^i+\lambda^i)^2$

Expandindo: $d^{ii} + 2\lambda^i d^i + (\lambda^i)^2$

**Detecção de omissão:** Se $d^{ii}G$ for omitido (o "$h''$"), a comparação lado-a-lado da integração por partes falha: o coeficiente de $d^{ii}G$ é **1** pelo lado direto e **0** pelo lado truncado. Qualquer polinômio $G$ com $d^{ii}G \neq 0$ detecta a omissão.

**Verificação numérica exata:** Tomar $G = f = 1/(x\cdot x)$, calcular $d^{ii}f = \partial_i^2(1/x^2)$ explicitamente e comparar com a expansão.

### Teste B — sinal errado no extremo $Y$ (ordem 1, $I=0$, $J=(j)$)

**Identidade formal:** $\partial_Y^j = (d^j - \eta^j)$ (não $(d^j + \eta^j)$)

**Detecção:** Para $\eta \neq 0$, os dois operadores diferem por $2\eta^j$. Qualquer polinômio de teste com $\eta^j \neq 0$ detecta o erro de sinal. Especificamente, para $G = f$:

- Correto: $(d^j - \eta^j)f = -\frac{2x^j}{(x^2)^2} - \frac{\eta^j}{x^2}$
- Errado: $(d^j + \eta^j)f = -\frac{2x^j}{(x^2)^2} + \frac{\eta^j}{x^2}$

Diferença: $2\eta^j/x^2 \neq 0$ para $\eta^j \neq 0$.

### Teste C — multiplicidade 2 ($I=(i,i)$)

Verificar que o coeficiente de $(d^i G_1)(d^i G_2)$ na expansão de $(d^i+\lambda^i)^2[G_1 G_2]$ é **exatamente 2**, comparando:
- **Iterativo:** aplicar $(d^i+\lambda^i)$ duas vezes, uma de cada vez
- **Multinomial:** expandir $(d^i+\lambda^i)^2$ diretamente

Ambos devem dar $2(d^i G_1)(d^i G_2)$ no termo cruzado.

### Teste D — comparação iterativa vs multinomial até ordem total 3

| $(I,J)$ | Ordem total | Iterativo | Multinomial | Concordam? |
|---|---|---|---|---|
| $(i),\,0$ | 1 | $-(d^i+\lambda^i)$ | $-(d^i+\lambda^i)$ | ✓ |
| $0,\,(j)$ | 1 | $(d^j-\eta^j)$ | $(d^j-\eta^j)$ | ✓ |
| $(i,i),\,0$ | 2 | $[-(d^i+\lambda^i)]^2$ | $(d^i+\lambda^i)^2$ | ✓ (com 2) |
| $(i,j),\,0$ | 2 | $-(d^i+\lambda^i)\cdot-(d^j+\lambda^j)$ | $(d^i+\lambda^i)(d^j+\lambda^j)$ | ✓ |
| $(i),\,(j)$ | 2 | $-(d^i+\lambda^i)(d^j-\eta^j)$ | idem | ✓ |
| $(i,i),\,(j)$ | 3 | $[-(d^i+\lambda^i)]^2(d^j-\eta^j)$ | $(d^i+\lambda^i)^2(d^j-\eta^j)$ | ✓ |
| $(i,j),\,(k)$ | 3 | $-(d^i+\lambda^i)\cdot-(d^j+\lambda^j)\cdot(d^k-\eta^k)$ | $(d^i+\lambda^i)(d^j+\lambda^j)(d^k-\eta^k)$ | ✓ |
| $(i),\,0$ c/ produto $G_1 G_2$ | — | Leibniz 2 termos + $\lambda$ | idem | ✓ |
| $(i,i),\,0$ c/ produto $G_1 G_2$ | — | Leibniz com cruzado×2 + $\lambda$ | idem | ✓ |

A comparação iterativa versus multinomial concorda em toda ordem total $\leq 3$ por construção: $(d+\lambda)^I$ e $(d-\eta)^J$ são operadores de coeficientes constantes que comutam entre si, logo a ordem de aplicação não importa e a expansão multinomial é exata.

---

## 7. Restrições declaradas

- **Não** se infere Q2, anomalia, completamento lorentziano ou QME pleno de um diagrama.
- **Não** se fornece número residual ou de cancelamento total: nenhum foi dado como entrada.
- **Não** se escolhe fator a partir de resíduo.
- **Não** se anuncia cancelamento total.
- Convenção de sinal do corrente é entrada explícita: $C_{\text{metric},X} = +(\partial_\mu \chi_X) J_{\text{raw}}^\mu/(16\kappa)$; para $C_b$ usar $+(\partial_\mu \chi_X) b_\nu \bar{Z}_{\mu\nu}$ sem reescalamento raw. Estas convenções afetam a normalização da corrente, não a estrutura do adjunto.
- Os coeficientes da corrente contêm $\lambda$; as derivadas do cutoff ($\lambda$, $\eta$) **não** são descartadas na adjunção. A adjunção usa os jatos exponenciais completos $(d+\lambda)$ e $(d-\eta)$, não apenas a parte de gradiente $d$.

---

## Resposta em uma linha

O operador adjunto que reduz sem perda os jatos externos é $\mathcal{A}^{I,J} = (-1)^{|I|}(d+\lambda)^I(d-\eta)^J$: o sinal $(-1)^{|I|}$ vem das integrações por partes no lado $X$; o lado $Y$ tem sinal $+1$ (cancelamento duplo de $\partial_Y = -d$ com $(-1)^q$), resultando em $(d-\eta)^J$ — não $(d+\eta)^J$. A contração $c\,\bar{b}c\,c$ tem sinal $+1$; a contração $b\,h$ preserva o sinal $-1$ do propagador. O fator de Leibniz para $I=(i,i)$ em produto de dois propagadores é 2 no termo cruzado, e o termo $d^{ii}$ (o $h''$) é obrigatório.