# A-7.b — Critério de adjunção formal para a variação BRST do setor local $h,c$

**Estatuto:** `[DECLARADO — resultado desta unidade científica; aguarda auditoria local]`. Nenhuma execução externa, CAS ou leitura de disco foi alegada. Convenções fixadas pelas fontes fornecidas (BV069, `s0barc = −b`, `Q = CG`, Euclidiano).

---

## 1. Hipóteses explícitas

| # | Hipótese | Estatuto |
|---|---|---|
| H-A | Coeficientes de $a_{(ij),r}(D)$ constantes em $x$; dependência espacial via $e^{L\cdot x}$ | `[INPUT — convenção do ansatz]` |
| H-B | $h_{ij} = h_{ji}$ simétrica; entrada diagonal com multiplicidade 1, fora-diagonal com ambas as entradas (multiplicidade 2 na variação $s_0$) | `[INPUT — dado do operador]` |
| H-C | Fantasmas $c_i$ ímpares (Grassmann); $h,b$ pares; antifields são fontes sem propagadores | `[INPUT — dado]` |
| H-D | Adjunta formal com peso $e^{L\cdot x}$: $\langle f, g\rangle = \int e^{L\cdot x}fg$ | `[DERIVED da estrutura]` |
| H-E | $s_0 h_{ij} = \partial_i c_j + \partial_j c_i$, $s_0 c = 0$ (álgebra de gauge abeliana neste nível) | `[INPUT — dado]` |
| H-F | Auxiliar plano Euclidiano $\mathbb{R}^4$; **nenhuma** identificação automática com a teoria lorentziana | `[DECLARADO — restrição do operador]` |

---

## 2. Derivação de $B_{jr}$ com multiplicidade diagonal

### 2.1 O ansatz e sua variação

$$A = \int e^{L\cdot x} \sum_{i\leq j}\sum_r h_{ij}\, a_{(ij),r}(D)\, c_r$$

Variação $s_0$:

$$s_0 A = \int e^{L\cdot x}\!\Big[\sum_i 2(\partial_i c_i)\,a_{(ii),r}\,c_r + \sum_{i<j}(\partial_i c_j + \partial_j c_i)\,a_{(ij),r}\,c_r\Big]$$

**Origem da multiplicidade diagonal:** $s_0 h_{ii} = 2\partial_i c_i$ — o fator 2 vem de que as duas contribuições fora-diagonal ($\partial_i c_j$ e $\partial_j c_i$) colapsam para a mesma componente quando $i = j$.

### 2.2 Integração por partes (IBP)

Para cada derivada $\partial_k$ atuando em um fantasma, IBP com o peso:

$$\int e^{L\cdot x}\,(\partial_k f)\,g = -\int e^{L\cdot x}\,f\,(D_k + L_k)\,g + \text{borda}$$

**Sinal da IBP:** $(-1)$ de $\int(\partial_k f)g = -\int f(\partial_k g)$. **Peso de base:** $L_k$ de $\partial_k(e^{L\cdot x}) = L_k\,e^{L\cdot x}$. São contribuições distintas — ver §5.

Aplicando IBP aos três setores:

| Setor | Termo original | Após IBP |
|---|---|---|
| Diagonal ($i=m$) | $2(\partial_m c_m)\,a_{(mm),r}\,c_r$ | $-2\,c_m\,(D_m+L_m)[a_{(mm),r}\,c_r]$ |
| Fora-diag. 1ª peça ($i<m$, fantasma $c_m$) | $(\partial_i c_m)\,a_{(im),r}\,c_r$ | $-c_m\,(D_i+L_i)[a_{(im),r}\,c_r]$ |
| Fora-diag. 2ª peça ($m<j$, fantasma $c_m$) | $(\partial_j c_m)\,a_{(mj),r}\,c_r$ | $-c_m\,(D_j+L_j)[a_{(mj),r}\,c_r]$ |

### 2.3 Coleta pelo índice do fantasma

Reunindo os termos com fantasma externo $c_m$:

$$s_0 A = -\int e^{L\cdot x}\sum_{m,r} c_m\,\underbrace{\Big[2(D_m{+}L_m)a_{(mm),r} + \sum_{k\neq m}(D_k{+}L_k)a_{(mk),r}\Big]}_{\displaystyle -B_{mr}}\,c_r$$

$$\boxed{B_{mr} = -\Big[\sum_k (D_k + L_k)\,a_{(mk),r} + (D_m + L_m)\,a_{(mm),r}\Big]}$$

onde o primeiro somatório corre sobre **todo** $k$ (incluindo $k=m$) e o segundo termo é a **multiplicidade diagonal explícita**. Equivalentemente:

$$B_{mr} = -\sum_k (1 + \delta_{km})\,(D_k + L_k)\,a_{(km),r}$$

com fator $(1 + \delta_{km})$: diagonal → 2; fora-diagonal → 1.

`[DERIVED — IBP + estrutura simétrica de $h$; sinal e peso separados]`

---

## 3. Critério graduado de anulação: $B - B^\dagger = 0$

### 3.1 Definição de adjunta formal

Com peso $e^{L\cdot x}$, a adjunta formal de um operador escalar $O(D)$ é:

$$\langle f, Og\rangle = \langle O^\dagger f, g\rangle \implies O^\dagger = O(-D - L)$$

Para o operador matricial $B$:

$$B^\dagger = B^T(-D - L), \qquad (B^\dagger)_{ij} = B_{ji}(-D-L)$$

`[DERIVED — definição de adjunta com peso]`

### 3.2 A forma quadrática $\int c\,B\,c$ para $c$ ímpar

Seja $Q = \int e^{L\cdot x}\sum_{ij} c_i\,B_{ij}\,c_r$. Usando:

1. **Adjunta:** $\langle c_i, B_{ij}c_j\rangle = \langle B^\dagger_{ij}c_i, c_j\rangle$
2. **Anticomutatividade:** $\langle f,g\rangle = -\langle g,f\rangle$ para $f,g$ ímpares

$$Q = \sum_{ij}\langle c_i, B_{ij}c_j\rangle = \sum_{ij}\langle B^\dagger_{ij}c_i, c_j\rangle = -\sum_{ij}\langle c_j, B^\dagger_{ij}c_i\rangle = -\sum_{ij}\langle c_i, B^\dagger_{ji}c_j\rangle$$

Comparando com $Q = \sum_{ij}\langle c_i, B_{ij}c_j\rangle$:

$$Q = -\sum_{ij}\langle c_i, (B^\dagger)^T_{ij}c_j\rangle$$

Se $B = B^\dagger$, então $Q = -\sum\langle c_i, B_{ij}c_j\rangle = -Q$, logo $2Q = 0 \implies Q = 0$.

$$\boxed{\int c\,B\,c = 0 \iff B = B^\dagger = B^T(-D-L) \iff B - B^\dagger = 0}$$

**O "graduado" é essencial:** para $c$ par (bosônico), a condição seria $B = -B^\dagger$ (antissimetria). Para $c$ ímpar (fermiônico), é $B = +B^\dagger$ (simetria formal). A anticomutatividade dos fantasmas converte a antissimetria natural da forma quadrática na condição de simetria adjunta.

`[DERIVED — consequência de H-C (paridade) + H-D (adjunta)]`

---

## 4. Derivação da substituição $q \leftrightarrow D$ a partir de $A(q)\,\partial_X\delta(X-Y)\,\chi_X\chi_Y$

### 4.1 O kernel bilocal

$$\partial_X\delta(X-Y) = \int\frac{d^4q}{(2\pi)^4}\,(iq_\mu)\,e^{iq\cdot(X-Y)}$$

Segue diretamente de $\delta(X-Y) = \int \frac{d^4q}{(2\pi)^4} e^{iq\cdot(X-Y)}$ e $\partial_{X^\mu} e^{iq\cdot(X-Y)} = iq_\mu e^{iq\cdot(X-Y)}$.

`[DERIVED — transformada de Fourier da delta; sem suposição]`

### 4.2 Atuação no campo e substituição

$$\int d^4Y\;A(q)\,\partial_X\delta(X-Y)\;g(Y) = \int\frac{d^4q}{(2\pi)^4}A(q)\,(iq_\mu)\,e^{iq\cdot X}\,\tilde{g}(q)$$

Comparando com a transformada de Fourier inversa de $\partial_\mu g$:

$$\partial_\mu g(X) = \int\frac{d^4q}{(2\pi)^4}(iq_\mu)\,e^{iq\cdot X}\,\tilde{g}(q)$$

A substituição é:

$$\boxed{q_\mu \leftrightarrow -i\,D_\mu \quad (D_\mu = \partial/\partial X^\mu)}$$

ou equivalentemente $D_\mu \leftrightarrow iq_\mu$. **Derivada, não assumida:** o fator $i$ vem da transformada de Fourier de $\partial_X\delta$; o sinal negativo da convenção $e^{iqX}$.

### 4.3 Separação dos três ingredientes

| Ingrediente | Origem | Contribuição |
|---|---|---|
| **Sinal de IBP** | $\int(\partial f)g = -\int f(\partial g)$ | $(-1)$ no total |
| **Peso de base** | $\partial_k(e^{L\cdot x}) = L_k\,e^{L\cdot x}$ | $+L_k$ em $(D_k + L_k)$ |
| **Derivadas do cutoff** | $\partial_\mu\chi \neq 0$ quando $\chi$ depende de $x$ | Termos $\propto \partial_\mu\chi$; **não** absorvidos pela adjunta |

`[DERIVED — separação explícita; as três contribuições não se misturam]`

---

## 5. Situação na identidade BV inhomogênea

### 5.1 A identidade

Com quebra clássica localizada por $\chi$ e $I_\chi = \frac{1}{2}(S_\chi, S_\chi) \neq 0$:

$$(S, S) = 2\,I_\chi$$

A nilpotência BRST é **quebrada** pela localização: $s^2 \neq 0$ no setor local, mas a obstrução é **controlada** por $I_\chi$.

`[KNOWN — estrutura BV padrão]`

### 5.2 O que uma falha da matriz $h,c$ ($B \neq B^\dagger$) **PODE** concluir

1. A variação BRST do bilinear $h,c$ não se anula por simetria adjunta — o ansatz $A$ **não** é uma deformação BRST-trivial **no setor $h,c$ isoladamente**.
2. O termo localizado contribui de forma **não-exata** para a corrente de gauge no setor externo $(h, c)$.

### 5.3 O que **NÃO PODE** concluir

1. **Anomalia cohomológica completa:** a falha pode ser absorvida por outros setores ($b$, antifields). A obstrução cohomológica exige varredura de **todos** os setores.
2. **Causalidade por $I_\chi$:** a falha pode vir da forma específica do ansatz, **não** da localização. Mesmo $I_\chi = 0$ pode dar $B \neq B^\dagger$ se o ansatz for inadequado.
3. **Violação do QME completo:** a identidade inhomogênea $(S,S) = 2I_\chi$ significa que variações BRST "exatas" **podem** ser não-nulas quando $I_\chi \neq 0$ — uma falha do teste $B - B^\dagger$ **não** implica violação da consistência quântica.
4. **Conclusão sobre o setor interno:** os kernels de contato atuais são no setor externo $h,c$ com fontes zeradas **após** derivações. A consistência homogênea para $\chi$ variável **não foi demonstrada** — não se anuncia obstrução cohomológica por um resíduo isolado. `[OPEN — lacuna declarada]`

`[DERIVED + OPEN — a distinção pode/não-pode é consequência da estrutura inhomogênea]`

---

## 6. Contraexemplos polinomiais

### Contraexemplo 1: Omissão de $L$

**Configuração:** $B = D^2 + b$ (1×1, $b$ constante), $L \neq 0$.

- **Critério errado** (sem $L$): $B^\dagger_{\rm err} = B(-D) = D^2 + b = B$ → falso positivo ("a forma se anula").
- **Critério correto:** $B^\dagger = B(-D-L) = D^2 + 2LD + L^2 + b \neq B$ → detecção correta de não-anulação.

**Verificação direta** (para $c$ ímpar):

$$Q = \int e^{Lx}\,c\,(c'' + bc)\,dx = \int e^{Lx}\,c\,c''\,dx = -L\int e^{Lx}\,c\,c'\,dx$$

onde usamos $(c')^2 = 0$ e $c^2 = 0$. Como $\int e^{Lx}\,c\,c'\,dx$ é genericamente não-nulo para $c$ ímpar, $Q \neq 0$ quando $L \neq 0$. **A omissão de $L$ mascara a não-anulação.**

`[DERIVED — cálculo explícito com contraexemplo]`

### Contraexemplo 2: Confusão entre simetria ordinária e adjunta

**Configuração:** $B = D$ (1×1).

- **Simetria ordinária:** $B^T = D = B$ → falso positivo ("simétrico").
- **Adjunta formal:** $B^\dagger = -D - L \neq B$ → detecção correta.

**Verificação:** $\int e^{Lx}\,c\,c'\,dx$ é genericamente não-nulo para $c$ ímpar (como no contraexemplo 1). A simetria matricial $B = B^T$ **não** implica simetria adjunta $B = B^\dagger$ quando há operadores diferenciais.

**Distinção dos dois erros:** o contraexemplo 1 dá falso positivo ao omitir $L$ (a operação errada é o adjunto); o contraexemplo 2 dá falso positivo ao usar $B^T$ (a propriedade errada é a simetria). São erros **independentes**.

`[DERIVED — dois contraexemplos distintos com verificação explícita]`

---

## 7. Lacunas nomeadas

| # | Lacuna | Estatuto |
|---|---|---|
| G-1 | Consistência homogênea para $\chi$ variável no setor interno **não** foi demonstrada | `[OPEN]` |
| G-2 | Os kernels atuais são só no setor externo $h,c$ com fontes a zero **após** derivações; o setor misto $b$-$h$ e as correntes quânticas de fantasma restam | `[OPEN]` |
| G-3 | O critério $B - B^\dagger = 0$ testa **apenas** o setor $h,c$; uma falha não conclui anomalia global (§5.3) | `[DERIVED — limitação do escopo]` |
| G-4 | A substituição $q \leftrightarrow -iD$ foi derivada no auxiliar Euclidiano; a passagem à teoria lorentziana **não** é automática | `[DECLARADO — restrição do operador]` |
| G-5 | Com o sinal IBP prévio do código-fonte (BV069: `s0 Vghost + s1 S0_gf = <b,[C,χ]Z> - <barc,[Q,χ]w>`), os termos $(S_\chi,S_\chi)$ envolvem contrações de loops mistos não calculados aqui | `[OPEN]` |

---

## Resumo das identidades verificáveis

| Identidade | Onde verificar | Estatuto |
|---|---|---|
| $B_{mr} = -\sum_k(1+\delta_{km})(D_k+L_k)a_{(km),r}$ | §2.3 | `[DERIVED]` |
| $B = B^\dagger \Rightarrow \int cBc = 0$ ($c$ ímpar) | §3.2 | `[DERIVED]` |
| $q_\mu \leftrightarrow -iD_\mu$ | §4.2 | `[DERIVED]` |
| $B = D^2+b$, $L\neq 0$: $B = B^T(-D)$ mas $B \neq B^T(-D-L)$ | §6, CE-1 | `[DERIVED]` |
| $B = D$: $B = B^T$ mas $B \neq B^\dagger$ | §6, CE-2 | `[DERIVED]` |

**Resultado DECLARADO até auditoria local.** Nenhum cálculo alheio foi usado para escolher o resultado; a convenção BV069 (`s0barc = −b`) foi seguida do código-fonte fornecido.