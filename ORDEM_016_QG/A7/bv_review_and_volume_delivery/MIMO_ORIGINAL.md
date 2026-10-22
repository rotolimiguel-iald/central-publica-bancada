# ORDEM 016 · A7.b — Conferência de convenções BV

**Estudo**: comparar os dois contratos antibracket (Fröb F vs. bancada B) sob a identificação de antifields $f^{dag}_A = \epsilon_A\, b^{dag}_A$, com $\epsilon_A = (-1)^{|\phi^A|} = (+1,+1,-1,-1)$ para $(h,b,c,\bar c)$.

**Estado**: **DECLARADO** até auditoria local.

---

## 1. Veredito

**A identificação $f^{dag}_A = \epsilon_A\, b^{dag}_A$ é uma equivalência canônica.** Os sinais do vértice ghost e da correção de Wick são preservados: viram juntos, e a contribuição $d\cdot\mathrm{div}(c)$ para $A_1(Faf)/(i\hbar)$ é a mesma nos dois contratos. **Nenhum sinal precisa mudar.**

---

## 2. Canonicidade (prova geral)

O jacobiano da mudança $b^{dag}_A = \epsilon_A f^{dag}_A$ (pois $\epsilon_A^2 = 1$) dá
$$\frac{\partial b^{dag}_A}{\partial f^{dag}_A} = \epsilon_A, \qquad \text{logo} \quad \frac{d}{d f^{dag}_A} = \epsilon_A \frac{d}{d b^{dag}_A}$$
(para derivadas esquerda e direita; $\epsilon_A = \pm 1$ é escalar, sem sinal extra de Grassmann).

Substituindo em $(F,G)_F$:

$$(F,G)_F = \sum_A \Bigl[\frac{d_R F}{d\phi^A}\,\frac{d_L G}{d f^{dag}_A} - \frac{d_R F}{d f^{dag}_A}\,\frac{d_L G}{d\phi^A}\Bigr] = \sum_A \epsilon_A \Bigl[\frac{d_R F}{d\phi^A}\,\frac{d_L G}{d b^{dag}_A} - \frac{d_R F}{d b^{dag}_A}\,\frac{d_L G}{d\phi^A}\Bigr] = (F,G)_B$$

para **todo** $F,G$. Os $\epsilon_A$ de B **são** o jacobiano. $\square$

---

## 3. Verificação em geradores

Os brackets fundamentais:

$$(\phi^A, f^{dag}_B)_F = \delta^A_B$$

em B, com $f^{dag}_B = \epsilon_B b^{dag}_B$:

$$(\phi^A, f^{dag}_B)_B = \epsilon_B\,(\phi^A, b^{dag}_B)_B = \epsilon_B \cdot \epsilon_B\,\delta^A_B = \delta^A_B \quad \checkmark$$

(alternativamente, segue diretamente da prova geral acima).

---

## 4. Verificação em monômio com ghost

Seja $F = f^{dag}_c \cdot c$ (ghost × antifield) e $G = c$.

**Em F:** $(f^{dag}_c\, c,\, c)_F = -\frac{d_R(f^{dag}_c\, c)}{d f^{dag}_c} = -c$

**Em B:** $\tilde F = \epsilon_c\, b^{dag}_c \cdot c = -b^{dag}_c \cdot c$

$$(-b^{dag}_c\, c,\, c)_B = -\epsilon_c\,\frac{d_R(-b^{dag}_c\, c)}{d b^{dag}_c} = -(-1)(-c) = -c \quad \checkmark$$

Ambos dão $-c$.

---

## 5. Vértice ghost: sinais viram juntos

$$S_B = S_{free} + \langle hdag_B, Kg\,c\rangle - \langle \bar{c}dag_B, b\rangle$$
$$S_F = S_{free} + \langle hdag_F, Kg\,c\rangle + \langle \bar{c}dag_F, b\rangle$$

Com $\bar{c}dag_F = \epsilon_{\bar c}\, \bar{c}dag_B = -\bar{c}dag_B$ e $hdag_F = hdag_B$:

$$S_F = S_{free} + \langle hdag_B, Kg\,c\rangle - \langle \bar{c}dag_B, b\rangle = S_B \quad \checkmark$$

O sinal $+$ do vértice em F é o sinal $-$ de B **depois** do dicionário. $S_F = S_B$; os contratos são equivalentes; $q_F = q_B$.

Os alvos dos geradores conferem sob a identificação:

- $qh = Kg\,c$, $q\bar c = -b$, $qc = qb = 0$ — idênticos nos dois.
- $qc^{dag}_F = +Q\bar c + Kg^* hdag_F = -(-Q\bar c - Kg^* hdag_B) = -qc^{dag}_B$ — **exatamente** $c^{dag}_F = -c^{dag}_B$.

---

## 6. Correção de Wick / defeito estendido

| | B | F | via dicionário |
|---|---|---|---|
| Defeito $D_H$ | $+d\,\delta^j_i$ | $-d\,\delta^j_i$ | $cdag_F = -cdag_B \Rightarrow D_H$ vira |
| Coef. vértice ghost | $+cdag_B$ | $-cdag_F = +cdag_B$ | idêntico |
| **Produto** (contrib. $A_1$) | $(+d)(+1) = +d$ | $(-d)(-1) = +d$ | **idêntico** |

A contribuição $d\cdot\mathrm{div}(c)$ para $A_1(Faf)/(i\hbar)$ é a **mesma**. Os dois sinais viram juntos.

---

## 7. Controle extra (álgebra local, não gravidade em 1D)

$$q_1 h = ch' + 2hc', \qquad q_1 c = cc'$$

$q_1$ é derivação ímpar à esquerda [$q_1(AB) = (q_1A)B + (-1)^{|A|}A(q_1B)$] e comuta com $\partial_x$.

### $q_1^2 h = 0$ ✓

$$q_1(ch') = (q_1c)h' - c\,(q_1h)' = cc'h' - c(c'h' + ch'' + 2h'c' + 2hc'') = -2h'cc' - 2hcc''$$

$$2q_1(hc') = 2\bigl[(q_1h)c' + h\,(q_1c')\bigr] = 2\bigl[h'cc' + h\,cc''\bigr] = 2h'cc' + 2hcc''$$

$$q_1^2 h = (-2h'cc' - 2hcc'') + (2h'cc' + 2hcc'') = 0 \quad \checkmark$$

Usando $c^2 = 0$, $(c')^2 = 0$, $ch' = h'c$, $ch = hc$.

### Invertendo só $q_1 c = -cc'$

$$q'_1(ch') = (-cc')h' - c\,(q_1h)' = -2cc'h' - 2h'cc' - 2hcc''$$

$$2q'_1(hc') = 2\bigl[h'cc' + h(-cc'')\bigr] = 2h'cc' - 2hcc''$$

$$\boxed{q'^2_1 h = -2cc'h' - 4hcc'' \neq 0}$$

**O que falha:** a nilpotência $q_1^2 = 0$ quebra **no setor ghost-vértice** ($q_1 h = ch' + 2hc'$). O sinal de $q_1 c = cc'$ é fixado pela compatibilidade com a derivada de Lie de $h$ — o bracket $[c,c] = 2cc'$ tem o sinal correto para $\mathcal L_c^2 = 0$ agir em $h$. Inverter só $q_1 c$ equivale a inverter o bracket, quebrando a identidade de Jacobi com o Lie-derivativo.

Onde $q'^2_1 = 0$ **sobrevive**: $q'^2_1 c = 0$ e $q'^2_1 b = 0$ (trivial, pois $q_1 b = 0$). Um teste só com campo par ($b$) não fixa o sinal ímpar de $q_1 c$ — exatamente como o operador avisou.

---

## 8. Resumo

| Item | Resultado |
|---|---|
| Canonicidade $(F,G)_F = (F,G)_B$ | **SIM** — $\epsilon_A$ é o jacobiano |
| Geradores $(\phi^A, f^{dag}_B) = \delta^A_B$ | **SIM** nos dois |
| Monômio com ghost $(f^{dag}_c c, c)$ | $-c$ nos dois ✓ |
| Vértice ghost | $S_F = S_B$; sinais viram juntos ✓ |
| Defeito / Wick $d\,\mathrm{div}(c)$ | mesma contribuição ✓ |
| Controle $q_1^2 h = 0$ | ✓ com $q_1 c = cc'$; ✗ $q'^2_1 h = -2cc'h' - 4hcc''$ com $q'_1 c = -cc'$ |
| Sinal que precisa mudar | **nenhum** |

Sem redefinição de $\hat q$ ou $H$; sem liberdade de renormalização invocada.

**DECLARADO** até auditoria local.