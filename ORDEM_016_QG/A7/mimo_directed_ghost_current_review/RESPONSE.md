# A-7.b — Kernel de duas contrações dirigidas: $J_{\text{ghost}}^\mu$ contra $V_{\text{ghost}}^{\chi_X}$

**Estatuto:** `[DECLARADO]` — cálculo nesta memória; derivação conferida e CAS exato pendentes da bancada.

---

## 1. Setup e convenções

**Campos Grassmann rotulados** (paridade ímpar marcada):

| Ponto | Campo | Índice livre | Paridade |
|---|---|---|---|
| $X$ | $h_{\alpha\beta}$ | $(\alpha,\beta)$ | par (externo) |
| $X$ | $\bar{c}_\nu^{v}$ | $\nu_v$ | ímpar |
| $X$ | $c_{\rho}^{v}$ | $\rho$ | ímpar |
| $Y$ | $\bar{c}_{\nu_c}$ | $\nu_c$ | ímpar |
| $Y$ | $c^{(1)}_{\mu_c}$ | $\mu_c$ | ímpar |
| $Y$ | $c^{(2)}_{\rho}$ | $\rho$ | ímpar |

**Propagadores:**
$$\langle c_\alpha(X)\,\bar{c}_\beta(Y)\rangle = +\delta_{\alpha\beta}\,f(x),\qquad \langle\bar{c}_\alpha(X)\,c_\beta(Y)\rangle = -\delta_{\alpha\beta}\,f(x)$$

com $x = X - Y$, $z = x\cdot x$, $f = 1/z$. Derivadas:
$$\partial_{X,i}f = -\frac{2x_i}{z^2},\qquad \partial_{Y,i}f = +\frac{2x_i}{z^2}$$

Fatores globais GQ retirados e declarados.

---

## 2. Estrutura dos operadores

### $J_{\text{ghost}}^\mu$ em $Y$ (Leibniz par)

$$J_{\text{ghost}}^\mu = \underbrace{(\partial_\mu\bar{c}_\nu)\,c^\rho\,\partial_\rho c^\nu}_{\text{(a)}} - \underbrace{\bar{c}_\nu\,(\partial_\mu c^\rho)(\partial_\rho c^\nu)}_{\text{(b1)}} - \underbrace{\bar{c}_\nu\,c^\rho\,\partial_\rho\partial_\mu c^\nu}_{\text{(b2)}}$$

Três campos ímpares em $Y$: $\bar{c}_{\nu_c}$, $c^{(1)}$ (um dos dois $c$), $c^{(2)}$ (o outro).

### $V_{\text{ghost}}^{\chi_X}$ em $X$ — setor $h$-externo

$$V_{\text{ghost}}^{\chi_X}\Big|_{h\text{-ext}} = -(\partial_\mu\bar{c}_\nu^v)\,Z_h^{\mu\nu} \;-\; \bar{c}_\nu^v\,(\partial_\mu\chi_X)\,Z_h^{\mu\nu}$$

com o **tensor de vértice** (simétrico em $\mu\nu$):

$$\boxed{Z_h^{\mu\nu} = h_{\mu\nu} - \tfrac{1}{2}\,\delta_{\mu\nu}\,\mathrm{tr}\,h}$$

Dois campos ímpares em $X$: $\bar{c}_\nu^v$, $c_\rho^v$.

---

## 3. As duas contrações dirigidas

Com $h$ externo em $X$ e um $c_r$ externo em $Y$, os dois campos ímpares de $X$ contraem com dois dos três ímpares de $Y$:

| Emparelhamento | $\bar{c}(Y) \leftrightarrow$ | $\bar{c}^v(X) \leftrightarrow$ | Externo em $Y$ |
|---|---|---|---|
| **P1** | $c_\rho^v(X)$ | $c^{(1)}_{\mu_c}(Y)$ | $c^{(2)}_{r}(Y)$ |
| **P2** | $c_\rho^v(X)$ | $c^{(2)}_{r}(Y)$ | $c^{(1)}_{\mu_c}(Y)$ |

### Sinal de Grassmann

Reordenação para $c_\rho^v(X)\,\bar{c}_\nu^v(X)\,c_r(Y)$ (fixo, $c$ externo à direita):

- **P1:** $c_\rho^v(X)$ cruza $\bar{c}_\nu^v(X)$, $\bar{c}(Y)$, $c^{(1)}(Y)$ → $(-1)^3 = -1$
- **P2:** $c_\rho^v(X)$ cruza $\bar{c}_\nu^v(X)$, $c^{(1)}(Y)$ → $(-1)^2 = +1$; $\bar{c}_\nu^v(X)$ cruza $c^{(2)}(Y)$ → $(-1)^1 = -1$; **produto: $-1$**

**Ambos os emparelhamentos: sinal $= -1$.**

---

## 4. Vértice e kernels escalares

Ambas as contrações produzem o mesmo vértice:

$$V_1^{\mu_c,r} = V_2^{\mu_c,r} = Z_h^{\mu_c,\,r} = h_{\mu_c r} - \tfrac{1}{2}\delta_{\mu_c r}\,\mathrm{tr}\,h$$

Os kernels escalares diferem na **estrutura do propagador**:

$$\boxed{K_1^{\mu_c,r} = -\,Z_h^{\mu_c,r}\;\partial_{X,\mu_c}f(x)\;\cdot\;f(Y{-}X)}$$

$$\boxed{K_2^{\mu_c,r} = -\,Z_h^{\mu_c,r}\;f(x)\;\cdot\;\partial_{X,\mu_c}f(Y{-}X)}$$

**Observação estrutural:** $\partial_{X,\mu_c}f(Y{-}X) = -\partial_{X,\mu_c}f(x)$, logo $K_1 + K_2 = 0$ para este diagrama. O cancelamento é **exato neste diagrama isolado**; não projeta cancelamento total (outros diagramas, outras contrações).

### Fórmula tensorial completa

$$\mathcal{K}^{\mu_c,r} = -Z_h^{\mu_c,r}\Big[\partial_{X,\mu_c}f(x)\,f(Y{-}X) + f(x)\,\partial_{X,\mu_c}f(Y{-}X)\Big]$$

---

## 5. Pseudocódigo executável

```python
# Coeficientes: (hslot, word_h; cslot, word_c) -> kernel scalar
# hslot: componente de h_{alpha beta}; cslot: índice do c externo
# word_h, word_c: estrutura de derivadas nos jatos

def kernel_two_contractions(mu_c, r, h_tensor, x, lam, eta):
    """K1 e K2 para (mu_c, r) livres."""
    z = sum(xi**2 for xi in x)
    f  = 1/z
    dfdx = [-2*xi/z**2 for xi in x]        # d_X f(x)
    dfdY = [+2*xi/z**2 for xi in x]        # d_Y f(x) = -d_X f(x)

    # Vértice Z_h^{mu_c, r}
    trh = sum(h_tensor[i][i] for i in range(4))
    V = h_tensor[mu_c][r] - F(1,2)*(mu_c==r)*trh

    # P1: propagadores  d_X f(x) * f(Y-X)
    prop1 = dfdx[mu_c] * f
    # P2: propagadores  f(x) * d_X f(Y-X) = f(x) * (-dfdx[mu_c])
    prop2 = f * (-dfdx[mu_c])

    sign = F(-1)  # ambos os emparelhamentos
    K1 = sign * V * prop1
    K2 = sign * V * prop2
    return K1, K2
```

---

## 6. Controle racional: $h_{11}=1$, $c_0$, $x=(1,2,-1,1)$, $\lambda=0$, $\eta=e_0$

**Vértice:** $t = \mathrm{tr}\,h = 1$.

$$Z_h^{00} = h_{00} - \tfrac{1}{2}\delta_{00}\,t = 0 - \tfrac{1}{2} = -\tfrac{1}{2}$$

**Propagadores** ($z = 7$):
$$\partial_{X,0}f = -\frac{2}{49},\qquad f = \frac{1}{7}$$

| | Antes da adjunção | Depois da adjunção |
|---|---|---|
| $K_1^{00}$ | $(-1)(-\frac{1}{2})(-\frac{2}{49})(\frac{1}{7}) = -\frac{1}{343}$ | $(-d_0$ em $K_1) \to +\frac{1}{343}\cdot d_0$ |
| $K_2^{00}$ | $(-1)(-\frac{1}{2})(\frac{1}{7})(+\frac{2}{49}) = +\frac{1}{343}$ | $(+d_0$ em $K_2) \to +\frac{1}{343}\cdot d_0$ |

**Adjunção:** $d_Y$ de $c$ dá $-(\eta_i - d_i) = -(1 - d_0) = -1 + d_0$ no kernel; $d_X$ de $h$ dá $-(\lambda_i + d_i) = -d_0$. Não contar $\eta$ duas vezes.

**Soma:** $K_1 + K_2 = 0$ (antes e depois da adjunção), como previsto.

**Coeficientes racionais do vértice** em $(\mu,\nu)=(0,0)$:
$$\underbrace{-h_{00}}_{-1} + \underbrace{\tfrac{1}{2}\delta_{00}t}_{+1/2} + \underbrace{h_{00}}_{+1} + \underbrace{-\tfrac{1}{2}\delta_{00}t}_{-1/2} = -\tfrac{1}{2}$$

---

## 7. Controles adversariais

### C1 — Inverter ordem $c/\bar{c}$ no vértice

O sinal de Grassmann muda de $-1$ para $+1$ em ambos os emparelhamentos.

| | Original | Invertido |
|---|---|---|
| $V_1^{00}$ | $-Z_h^{00} = +\frac{1}{2}$ | $+Z_h^{00} = -\frac{1}{2}$ |
| $V_2^{00}$ | $-Z_h^{00} = +\frac{1}{2}$ | $+Z_h^{00} = -\frac{1}{2}$ |
| $K_1^{00}$ | $-\frac{1}{343}$ | $+\frac{1}{343}$ |
| $K_2^{00}$ | $+\frac{1}{343}$ | $-\frac{1}{343}$ |

**A inversão inverte o sinal global do kernel.** O cancelamento $K_1+K_2=0$ persiste (estrutural), mas o sinal de cada contribuição inverte — o que distingue a ordem Grassmann correta da invertida.

### C2 — Omitir uma das duas pernas $c_Y$

Sem $c^{(2)}(Y)$, o emparelhamento P2 desaparece ($c^{(2)}$ é o externo de P2).

| | Completo | Sem $c^{(2)}(Y)$ |
|---|---|---|
| $K_1^{00}$ | $-\frac{1}{343}$ | $-\frac{1}{343}$ |
| $K_2^{00}$ | $+\frac{1}{343}$ | $0$ |
| Soma | $0$ | $-\frac{1}{343} \neq 0$ |

**A omissão quebra o cancelamento.** O zero da soma depende da presença das DUAS pernas $c$ em $Y$ — a estrutura de três campos ímpares é essencial.

---

## 8. Resumo declarado

| Item | Valor |
|---|---|
| Vértice | $Z_h^{\mu\nu} = h_{\mu\nu} - \frac{1}{2}\delta_{\mu\nu}\,\mathrm{tr}\,h$ |
| $K_1$ (P1: $\bar{c}(Y)\!\leftrightarrow\! c(X)$, $c^{(1)}(Y)\!\leftrightarrow\!\bar{c}(X)$) | $-Z_h \cdot \partial_{X,\mu_c}f(x) \cdot f(Y{-}X)$ |
| $K_2$ (P2: $\bar{c}(Y)\!\leftrightarrow\! c(X)$, $c^{(2)}(Y)\!\leftrightarrow\!\bar{c}(X)$) | $-Z_h \cdot f(x) \cdot \partial_{X,\mu_c}f(Y{-}X)$ |
| Sinal Grassmann | $-1$ em ambos |
| Soma | $K_1 + K_2 = 0$ (este diagrama) |
| Fatores GQ | retirados e declarados |
| Simetria global | não incluída (proibido) |
| Cancelamento total | **NÃO projetado** — este diagrama isolado |

**Lacunas declaradas:** (i) CAS exato e derivação conferida pendentes da bancada; (ii) os diagramas com $b\,h\,c$ e $\bar{c}\,c\,c$ (pesos globais) não incluídos; (iii) este cálculo não constitui Q2 nem prova de cancelamento total.