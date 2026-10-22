# ORDEM_016 — Ramo A-7.b: o vértice de inserção $J_b^\mu = b_\nu\,\bar Z_{\mu\nu}$ no par conectado EH(X)–corrente(Y)

**Estatuto desta entrega:** `[DECLARADO]` — texto de derivação para conferência e CAS exato pela bancada. Nada aqui foi executado, compilado ou medido nesta sessão; nenhum arquivo foi modificado. O alvo é **somente o diagrama misto** $J_b \times \mathrm{EH}$; não é a primitiva total, não é a QME interagente, e nenhum contato parcial é declarado Q2. Constantes globais ficam **nomeadas** e nenhum fator é ajustado para fechar resíduo.

---

## 1. O propagador misto $\langle h_{ab}(X)\,b_\nu(Y)\rangle$ de $G\,G_Q$

### 1.1 Blocos do inverso, verificados

Com $S_0^{B} = \tfrac12\langle h,Hh\rangle + \langle b,Ch\rangle - \tfrac{1}{2\ell}\langle b,b\rangle$, o operador quadrático no par $(h,b)$ e o inverso declarado são

$$
M=\begin{pmatrix} H & C^{*}\\ C & -\ell^{-1}\end{pmatrix},
\qquad
M^{-1}=\begin{pmatrix} G_D & G\,G_Q\\ G_Q\,G^{*} & 0\end{pmatrix}.
$$

Checagem $M M^{-1} = I$, usando **apenas** as identidades nomeadas no contexto:

- $(bb)$: $C\,G\,G_Q = Q\,G_Q = I$ ✓ (pois $Q = CG$);
- $(hb)$: $H\,G\,G_Q = 0$ ✓ (pois $HG=0$);
- $(bh)$: $C\,G_D - \ell^{-1} G_Q G^{*} = 0$ ✓ (identidade declarada);
- $(hh)$: $H G_D + C^{*} G_Q G^{*} = H G_D + \ell\, C^{*} C\, G_D = D\,G_D = I$ ✓ (com $D = H+\ell C^{*}C$).

**O bloco $b$-$b$ nulo não anula o misto:** $\langle h(X)\,b(Y)\rangle = (G\,G_Q)(x)$, $x = X-Y$, é não-trivial. É exatamente por este bloco que o slot $b_\nu$ de $J_b$ se liga ao vértice EH.

### 1.2 Forma explícita

$(G\,c)_{ab} = d_a c_b + d_b c_a$ como operador sobre o vetor; $G_Q = g_Q\,\delta_{\rho\nu}\,f$, $f = 1/z$. Com $\partial_X = d$:

$$
\boxed{\;\langle h_{ab}(X)\,b_\nu(Y)\rangle \;=\; g_Q\,\big(\delta_{b\nu}\,d_a + \delta_{a\nu}\,d_b\big)\,f(x) \;=\; -2\,g_Q\,\frac{\delta_{b\nu}\,x_a + \delta_{a\nu}\,x_b}{z^{2}}\;}
$$

pois $d_a f = -2x_a/z^{2}$.

### 1.3 A ligação de Ward entre as constantes — verificada dos dois lados

Com $G_D = g_D\,S\,f$, $S_{ab,cd} = \tfrac12(\delta_{ac}\delta_{bd}+\delta_{ad}\delta_{bc}-\delta_{ab}\delta_{cd})$:

**Lado $C\,G_D$:** $(C\,G_D)_{\nu,cd} = g_D\,d_\mu S_{\mu\nu,cd}\,f - \tfrac{g_D}{2}\,d_\nu S_{\mu\mu,cd}\,f$. Como $d_\mu S_{\mu\nu,cd} = \tfrac12(\delta_{\nu d}d_c + \delta_{\nu c}d_d - \delta_{cd}d_\nu)$ e $S_{\mu\mu,cd} = -\delta_{cd}$ (em 4D), os termos de traço cancelam-se:

$$
(C\,G_D)_{\nu,cd} = \frac{g_D}{2}\,\big(\delta_{\nu c}\,d_d + \delta_{\nu d}\,d_c\big) f .
$$

E $(G^{*}\phi)_\rho = -2\,d_\mu\phi_{\mu\rho}$ dá $(\ell^{-1}G_Q G^{*})_{\nu,cd} = \ell^{-1}g_Q\,(d_c\delta_{d\nu}+d_d\delta_{c\nu})\,f$ após a projeção simétrica. Logo:

$$
C\,G_D = \ell^{-1}G_Q G^{*} \quad\Longleftrightarrow\quad \boxed{\;g_D\,\ell = 2\,g_Q\;}
$$

**Lado $G_D\,C^{*}$ (controle cruzado):** com $(C^{*}\phi)_{cd} = -d_c\phi_d + \tfrac12\delta_{cd}\,d\!\cdot\!\phi$ (leitura no pareamento completo) e IBP ($-\partial_y \to +d$), o termo de traço de $C^{*}$ cancela exatamente o traço de $S$:

$$
(G_D\,C^{*})_{ab,\nu} = \frac{g_D}{2}\,\big(\delta_{b\nu}d_a + \delta_{a\nu}d_b\big)\,f = \ell^{-1}(G\,G_Q)_{ab,\nu} \quad\Longleftrightarrow\quad g_D\,\ell = 2\,g_Q \ \checkmark
$$

A mesma ligação, nos dois sentidos. **Nota de normalização (declarada, não usada para fechar):** $(Qc)_\nu = \Box\,c_\nu$ (verificado: os termos de divergência cancelam); $\Box(1/z) = -4\pi^{2}\,\delta^{4}$ em $\mathbb{R}^4$; se $G_Q$ for o inverso exato, $g_Q = -1/(4\pi^{2})$. Mantenho $g_Q$, $g_D$, $\ell$ simbólicos.

### 1.4 Equação exata de conversão para uma realização por fibra

Se a realização do misto usar a fibra pura $S$ (como a realização $G_D \sim Sf$ da bancada), a identidade exata é

$$
g_Q\big(\delta_{b\nu}d_a + \delta_{a\nu}d_b\big)f \;=\; 2\,g_Q\,S_{ab,c\nu}\,d_c f \;+\; \underbrace{g_Q\,\delta_{ab}\,d_\nu f}_{\mathcal T_{\mathrm{traco}}\ \text{(nomeado)}} .
$$

Não suponho que retirar o mesmo fator global do misto seja correto: o misto é **estruturalmente** $G\,G_Q$ (uma derivada sobre $f$ com dois deltas), não $Sf$. O termo $\mathcal T_{\mathrm{traco}}$ fica nomeado; **não escolho para fechar**. (No toy da §5 ele é zero porque o slot do misto é fora da diagonal; um controle com slot diagonal $(0,0)$ o exercitaria — pendência nomeada, §7.)

---

## 2. O vértice $J_b$ como lista finita de coeficientes

### 2.1 Expansão

Com $Z_{\mu\nu} = (L_c h)_{\mu\nu} = c^{\rho}\partial_\rho h_{\mu\nu} + (\partial_\mu c^{\rho})h_{\rho\nu} + (\partial_\nu c^{\rho})h_{\mu\rho}$, ghost externo fixado na componente $c_r$ ($c^{\rho} \to \delta^{\rho r} c_r$, **$r$ fixo, sem soma**), e $\bar Z_{\mu\nu} = Z_{\mu\nu} - \tfrac12\delta_{\mu\nu}Z_{\sigma\sigma}$ ($\sigma$ mudo, somado $0..3$):

$$
J_b^\mu[c_r] = b_\nu\,\bar Z_{\mu\nu}[c_r]
= b_\nu\Big[ c_r\,\partial_r h_{\mu\nu} + (\partial_\mu c_r)h_{r\nu} + (\partial_\nu c_r)h_{\mu r}
-\tfrac12\delta_{\mu\nu}\big( c_r\,\partial_r h_{\sigma\sigma} + 2(\partial_\sigma c_r)h_{\sigma r}\big)\Big].
$$

### 2.2 A lista (regra paramétrica; 5 famílias; 20 termos brutos por $(\mu, r)$)

| família | coef. | $\nu$ | slot $h$ $(a\le b)$ | `word_h` | `word_c` | $\mu$ |
|---|---|---|---|---|---|---|
| T1 | $+1$ | livre $0..3$ | $\mathrm{ord}(\mu,\nu)$ | $(r)$ | $()$ | livre |
| T2 | $+1$ | livre $0..3$ | $\mathrm{ord}(r,\nu)$ | $()$ | $(\mu)$ | livre |
| T3 | $+1$ | livre $0..3$ | $\mathrm{ord}(\mu,r)$ | $()$ | $(\nu)$ | livre |
| T4 | $-\tfrac12$ | $\nu=\mu$ (por $\delta_{\mu\nu}$) | $(\sigma,\sigma)$, $\sigma$ somado | $(r)$ | $()$ | livre |
| T5 | $-1$ | $\nu=\mu$ | $\mathrm{ord}(\sigma,r)$, $\sigma$ somado | $()$ | $(\sigma)$ | livre |

(T5: $-1 = -\tfrac12 \times 2$.) Lista **finita**: $4+4+4+4+4 = 20$ por $(\mu,r)$; $80$ no máximo por ghost com $\mu$ livre.

### 2.3 Convenções (separadas, como ordenado)

- **Transposição formal:** `word_h` são derivadas do **slot** $h$ de $Z$; `word_c` são derivadas sobre o **ghost externo localizado**; nenhuma derivação é transposta silenciosamente entre eles.
- **Derivadas em $Y$:** cada índice de `word_h` bate no **propagador** e contribui $-d$ (pois $\partial_Y = -d$): sinal $(-1)^{|\mathrm{word\_h}|}$. Cada índice de `word_c` bate no **jato** $\chi_Y = e^{\eta\cdot Y}$: fator $+\eta_\rho$. A inserção da corrente $\partial_\mu^Y\chi_Y$ dá $+\eta_\mu$. Derivadas de jato **nunca** recebem o sinal de propagador.
- **Multiplicidade tensorial:** com os dois lados em pares ordenados (LABELS no EH; $(a\le b)$ no slot de $Z$), a fibra $S$ completa já conta a simetria; $m_{ab} = 2-\delta_{ab}$ **não se aplica** adicionalmente (só entraria na conversão soma-completa $\leftrightarrow$ soma-ordenada). Aplicado **zero** vezes aqui — declarado para não duplicar.

### 2.4 Lista explícita para $\mu = 0$, $r = 0$ (a usada na avaliação)

```
T1: (+1)   nu=0..3 ; slot ord(0,nu)      ; word_h=(0) ; word_c=()
T2: (+1)   nu=0..3 ; slot ord(0,nu)      ; word_h=()  ; word_c=(0)
T3: (+1)   nu=0..3 ; slot (0,0)          ; word_h=()  ; word_c=(nu)
T4: (-1/2) nu=0    ; slot (sig,sig), sig=0..3 ; word_h=(0) ; word_c=()
T5: (-1)   nu=0    ; slot ord(sig,0), sig=0..3 ; word_h=() ; word_c=(sig)
```

---

## 3. A contração com os dois slots $h$ do vértice EH em $X$

Seja $A^X$ a matriz de jatos do EH cúbico localizado (fornecida pela bancada; aqui **não** rederivada), bloco $W = A^X[\mathrm{ex}]$ para o slot externo com jato $\mathrm{ex}$ ($\mathrm{ex}=-1$: sem derivada; senão fator $\lambda_{\mathrm{ex}}$), pernas internas $i,j \in \{0,\dots,49\}$ (10 componentes $\times$ 5 jatos de ordem $\le 1$), $W$ simétrica.

**Os dois emparelhamentos, exibidos antes de qualquer simetria:**

$$
\mathcal D_{J_b} = \eta_\mu \sum_{k} c_k \sum_{i,j} \Big[\,
\underbrace{W_{ij}\, M_{i,\nu_k}(x)\, H_{j,(a_k b_k), w_h^k}(x)}_{h_X^{(i)}\!-\,b_Y\; \times\; h_X^{(j)}\!-\,h_Y(Z)}
\;+\;
\underbrace{W_{ij}\, H_{i,(a_k b_k), w_h^k}(x)\, M_{j,\nu_k}(x)}_{h_X^{(i)}\!-\,h_Y(Z)\; \times\; h_X^{(j)}\!-\,b_Y}
\,\Big],
$$

com os propagadores (constantes nomeadas, derivadas reais, sem $i$ de Fourier):

$$
M_{i,\nu}(x) = g_Q\,\big(\delta_{q(i),\nu}\,d_{p(i)} + \delta_{p(i),\nu}\,d_{q(i)}\big)\, d^{w(i)} f,
\qquad
H_{j,(ab),w_h}(x) = g_D\,S_{(p(j)q(j)),(ab)}\,(-d)^{w_h}\, d^{w(j)} f,
$$

onde $(p(i),q(i))$ é o par da perna $i$ e $w(i) = ()$ se $i<10$, senão $(i//10-1)$.

Como $W$ é simétrica, o segundo emparelhamento replica o primeiro sob $i \leftrightarrow j$. **Multiplicidade de emparelhamento $=2$, declarada uma única vez:**

$$
\mathcal D_{J_b} = 2\,\eta_\mu \sum_k c_k\, g_Q g_D \sum_{i,j} W_{ij}\, M'_{i,\nu_k}\, H'_{j,(a_k b_k),w_h^k},
$$

com $M' = M/g_Q$, $H' = H/g_D$. O fator do ghost externo é $\eta_{w_c}$ ($=1$ se `word_c` vazio; $\eta_\rho$ se `word_c` $=(\rho)$).

---

## 4. Algoritmo (aceita $A^X$ arbitrária simétrica)

```text
def diagrama_Jb(AX, r, eta, lam, x_eval, gQ, gD):
    total = 0
    for ex in [-1,0,1,2,3]:                       # jato do slot externo de h em X
        W = AX[0] if ex == -1 else AX[1][ex]      # simétrica 50x50; aborta se não simétrica
        fator_ex = 1 if ex == -1 else lam[ex]
        for termo in LISTA_Jb(r):                 # §2.2: (coef; nu; (a,b); w_h; w_c; mu)
            (coef, nu, ab, w_h, w_c, mu) = termo
            if eta[mu] == 0: continue
            gfac = 1 if w_c == () else eta[w_c[0]] # jato do ghost; +eta, sem sinal
            if gfac == 0: continue
            acc = 0
            for i in 0..49:
                Mi = prop_misto(i, nu, x_eval)     # gQ (δ_{q nu} d_p + δ_{p nu} d_q) d^{w(i)} f
                if Mi == 0: continue
                for j in 0..49:
                    if W[i][j] == 0: continue
                    Hj = prop_hh(j, ab, w_h, x_eval) # gD S_{par(j),ab} (-d)^{w_h} d^{w(j)} f
                    acc += W[i][j] * Mi * Hj
            total += coef * gfac * eta[mu] * fator_ex * acc
    return 2 * total        # multiplicidade de emparelhamento: UMA vez, aqui
```

`prop_hh` aplica $(-1)^{|w_h|}$ (derivadas em $Y$); `prop_misto` não recebe sinal de $Y$ porque suas derivadas são a estrutura de $G\,G_Q$ mais o jato em $X$ ($+d$). `m_ab` não aparece. `propagador_derivado` pode ter ordem $>1$ (a estrutura $d f \sim x/z^2$ mais jatos) — permitido.

---

## 5. Avaliação racional declarada (controle incluído)

**$A^X$ toy declarada (não é a saída de `localized_vertex_data`):** bloco $\mathrm{ex}=-1$; $W_{i_0 j_0} = 1$ com $i_0 = j_0 =$ perna **sem derivada** de componente de par $(0,2)$; demais entradas nulas. Simétrica (diagonal). $r = 0$ (ghost $c_0$), $\eta = e_0$, $x = (1,2,-1,1)$: $z = 7$, $f = \tfrac17$, $d_0 f = -\tfrac{2}{49}$, $d_1 f = -\tfrac{4}{49}$, $d_2 f = +\tfrac{2}{49}$, $d_3 f = -\tfrac{2}{49}$. **Não-axial:** $\eta = e_0$ e $x$ genérico quebram qualquer simetria de eixo; nada aqui zera por simetria.

**Filtragem dos termos (§2.4):** a inserção exige $\mu = 0$; o misto $M_{i_0,\nu} = g_Q(\delta_{2\nu}d_0 + \delta_{0\nu}d_2)f$ exige $\nu \in \{0,2\}$; a fibra $S_{(0,2),(a,b)}$ exige $(a,b) = (0,2)$ (valor $\tfrac12$).

- **T1, $\nu=2$** $(+1)$: $M = g_Q d_0 f = -\tfrac{2g_Q}{49}$; $H = \tfrac{g_D}{2}(-d_0)f = +\tfrac{g_D}{49}$. Produto: $-\tfrac{2\,g_Q g_D}{2401}$.
- **T2, $\nu=2$** $(+1)$, fator ghost $\eta_0 = 1$: $M = -\tfrac{2g_Q}{49}$; $H = \tfrac{g_D}{2}f = \tfrac{g_D}{14}$. Produto: $-\tfrac{2\,g_Q g_D}{686} = -\tfrac{g_Q g_D}{343}$.
- T3: slot $(0,0)$ — fibra nula. T4: slots $(\sigma,\sigma)$ — $S_{(0,2),(\sigma\sigma)} = 0$. T5: $\sigma=2$ daria slot $(0,2)$, mas `word_c` $=(2) \to \eta_2 = 0$. **Não contribuem.**

Soma bruta: $-\tfrac{2}{2401} - \tfrac{7}{2401} = -\tfrac{9}{2401}$ (em $g_Q g_D$). Com a multiplicidade de emparelhamento $2$ e $\eta_0 = 1$:

$$
\boxed{\;\mathcal D_{J_b}^{\mathrm{toy}} = -\frac{18}{2401}\,g_Q\,g_D \;=\; -\frac{36}{2401}\,\frac{g_Q^{2}}{\ell}\ \text{(por Ward)}\;}
$$

**Controle (remoção de $J_b$):** sem o vértice de corrente, o canal misto é identicamente $0$. O controle independente — a bolha métrica pura EH–EH com a **mesma** $A^X$ (dois propagadores $h$-$h$, mesma multiplicidade 2 declarada uma vez) — vale

$$
\mathcal D_{\mathrm{ctrl}} = 2\,\Big(g_D\,S_{(0,2),(0,2)}\,f\Big)^{2} = 2\,\Big(\frac{g_D}{14}\Big)^{2} = \frac{g_D^{2}}{98} \;\neq\; 0 .
\qquad \checkmark
$$

Ou seja: removido $J_b$, o canal alvo zera e o controle **não** zera — a máquina mede algo, e o valor $-\tfrac{18}{2401}g_Q g_D$ não é o controle disfarçado nem o zero por default.

---

## 6. Conversão fórmula ↔ código (fatores nomeados; nada escolhido para fechar)

- O código usa fibra pura $S$ e $f$ puros (constantes absorvidas) e um fator global $\tfrac{1}{16}$ por vértice-avaliação (docstring: “/16 metric normalization”). Para o diagrama com **um** misto e **um** $h$-$h$:

$$
\mathcal D^{\mathrm{físico}} \;=\; \underbrace{16\,g_Q\,g_D}_{K_{\mathrm{conv}}\ \text{(nomeado)}}\;\mathcal D^{\mathrm{código}}
\;\overset{\text{Ward}}{=}\; \frac{32\,g_Q^{2}}{\ell}\,\mathcal D^{\mathrm{código}} .
$$

No toy: $\mathcal D^{\mathrm{código}}_{\mathrm{toy}} = -\tfrac{18}{2401\times 16} = -\tfrac{9}{19208}$.
- **Ressalva estrutural (a incompatibilidade nomeada):** se o misto for realizado no código pela fibra pura, falta o termo $\mathcal T_{\mathrm{traco}} = g_Q\,\delta_{ab}d_\nu f$ da equação exata da §1.4. A equação de conversão **é** a §1.4, com $K_{\mathrm{conv}}$ e $\mathcal T_{\mathrm{traco}}$ nomeados. Não fecho.
- **Sinal global:** o código aplica `coeff = -Σ current·eta` (um $-$ por termo). Na minha convenção a inserção $\int \partial_\mu\chi\,J^\mu$ dá $+\eta_\mu$. Nomeio $\varepsilon_J = -1$ (código) vs. $+1$ (esta derivação); a origem provável é a convenção $s_0\bar c = -b$ da ação (que uso; o sinal $+b$ é declaradamente incompatível) ou a IBP — **a conferir pela bancada**, não decido.

---

## 7. Lacunas declaradas (sem fingir acesso)

1. **Módulos dependentes não fornecidos:** `localized_eh_cubic_engine.py` (forma exata de $A^X$), `position_metric_bubble_engine.py` (`LABELS` — assumi a ordenação lexicográfica de pares; o toy depende apenas de “o par $(0,2)$”), `full_loop_extension_engine.py` (`propagator_derivative`, `contact`, `Q`), `classical_current_jet_engine.py` (`split_word` e a construção de `rows`). Por isso: (a) a semântica exata de `pword/qword/kword` e de `row['a']/row['b']` não foi verificável; (b) se o misto é realizado com ou sem $\mathcal T_{\mathrm{traco}}$ é uma **pergunta aberta de leitura**, nomeada na §6.
2. **Pesos globais demonstrados** estão fora do alvo deste ramo; ficaram nomeados ($g_Q$, $g_D$, $\ell$, $K_{\mathrm{conv}}$), ligados por Ward ($g_D\ell = 2g_Q$), com a normalização de $\Box$ declarada mas não usada.
3. **Controle do termo de traço:** um toy com slot diagonal $(0,0)$ no misto exercitaria $\mathcal T_{\mathrm{traco}}$; não executado aqui (depende de 7.1). Nenhum contato parcial é Q2.
4. **Pendência de processo:** esta derivação é `[DECLARADO]` até a conferência e o CAS exato da bancada. O sinal $\varepsilon_J$ (§6) é o primeiro item a cruzar com `classical_current_jet_engine`.

**Selo da entrega (textual, sem execução):** `JB_VERTEX_DERIVED__MIXED_PROPAGATOR_IS_GGQ_NOT_BB__WARD_GD_TIMES_ELL_EQ_2GQ__FIVE_FAMILIES_FINITE_LIST__TWO_PAIRINGS_MULTIPLICITY_TWO_DECLARED_ONCE__TOY_VALUE_MINUS_18_OVER_2401_GQ_GD__CONTROL_NONZERO_WITHOUT_JB__CONVERSION_NAMED_NOT_CLOSED__DECLARED_UNTIL_BENCH_CHECK`