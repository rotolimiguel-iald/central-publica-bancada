# ORDEM_016 A‑7.b — bancada científica autorizada
## Extensão radial de pares e normalização de inserções compostas: contatos escalares da inserção Euler antes da escolha de esquema

**Status desta entrega: `[DECLARADO]` até verificação local.** Nenhuma execução de código, recibo, hash, build ou prova formal é alegado. Toda a álgebra abaixo é derivação manual (caneta), com a normalização vinda do operador. Nenhum original é alterado. Nada se afirma sobre Q2 (completa ou parcial) e nada se afirma de QME gravitacional. Auxiliar estritamente euclidiano $\mathbb{R}^4$; **nenhuma continuação lorentziana é presumida**.

Escopo negativo desta unidade (não repetido aqui, por definição): sinais de Wick, correntes $X/Y$, identidade abstrata BV, enumeração de grafos Euler.

---

## 0. Interpretação do termo "inserção Euler" (lacuna declarada de passagem)

Adoto `[DEF/INTERPRETAÇÃO]`: **inserção Euler** = inserção do operador de Euler/dilatação $\mathcal E = x\cdot\partial_x$ (gerador radial) num par de linhas de propagador $f,g$. Toda a contagem de contatos do §3 está condicionada a esta leitura. Se "inserção Euler" significar outra coisa (Euler do grafo, vértice Euler–Heisenberg, inserção de $\mathcal E$ só como contador de grau de escala), **a contagem muda** e o ponto fica como lacuna de passagem, não de resultado.

---

## 1. Dados, convenções e checagem da normalização

$d=4$ euclidiano, $z = x\cdot x = \sum_\mu x_\mu x_\mu$, $\Box = \sum_\mu \partial_\mu^2$.

$$f = \frac1z,\qquad g = \frac1z,\qquad CE = -4\pi^2,\qquad \Box\frac1z = CE\,\delta^{(4)}(x)\ \ [\text{DEF/INPUT}]$$

Família meromorfa: $z^{a-n}$, $n\ge 1$, com resíduos no pólo. Regulador de **par** distribuído simetricamente:

$$f_a = g_a = z^{a-1},\qquad f_ag_a = z^{2a-2}.$$

$R$ (INPUT do operador):

$$R(t) = \mathrm{FP}_{a=0}\big[(1-a)\mu^{2a}z^a\,t\big],\qquad C_D(t) = R(Dt) - D\,R(t).$$

Regra de resíduos (INPUT, normalizada por $CE$), $n\ge2$:

$$\boxed{\ \frac{\mathrm{Res}[z^{a-n}]}{CE} = -\frac{(q\cdot q)^{n-2}}{4^{n-1}(n-1)!(n-2)!}\ }\qquad q_\mu \leftrightarrow \partial_\mu\delta\ (\text{sem }i),\qquad x_j \to -\partial_{q_j}.$$

Denotarei $\rho_n := \mathrm{Res}_{a=0}[z^{a-n}]$:

$$\rho_2 = -\frac{CE}{4} = \pi^2,\quad \rho_3 = -\frac{CE}{32}(q\cdot q) = \frac{\pi^2}{8}(q\cdot q),\quad \rho_4 = -\frac{CE}{768}(q\cdot q)^2 = \frac{\pi^2}{192}(q\cdot q)^2,\quad \rho_5 = \frac{\pi^2}{9216}(q\cdot q)^3 .$$

### 1.1 Duas checagens internas da normalização fornecida (não são ajuste)

**(a) $n=2$ reproduz $CE$.** À mão: $\partial_\mu z^p = 2p\,x_\mu z^{p-1}$, logo

$$\Box z^{p} = 4p(p+1)z^{p-1},\qquad \Rightarrow\qquad \Box z^{a-1} = 4a(a-1)z^{a-2}.$$

Como $z^{a-2} = \frac{\rho_2}{a} + F + O(a)$ com $\rho_2 = -CE/4$,

$$\Box\frac1z = \lim_{a\to0}4a(a-1)z^{a-2} = -4\rho_2 = CE .\qquad\checkmark$$

Este é o **único** ponto onde $CE$ é testado: a identidade *consome* $CE$, não o deriva.

**(b) Coerência $z = \Box_q$ sobre os polinômios de $\delta$.** Com $x_j\to-\partial_{q_j}$, $z = \sum_j x_jx_j \to \Box_q$. Usando $\Box_q(q\cdot q)^m = 4m(m+1)(q\cdot q)^{m-1}$:

$$z\,\rho_{n+1} = -\frac{CE}{4^{n}n!(n-1)!}\cdot 4n(n-1)(q\cdot q)^{n-2} = -\frac{CE\,(q\cdot q)^{n-2}}{4^{n-1}(n-1)!(n-2)!} = \rho_n\quad\checkmark$$

Ex.: $z\rho_4 = \rho_3$, $z\rho_3 = \rho_2$. A normalização fornecida é **internamente coerente** com a regra $x_j\to-\partial_{q_j}$ — sem calibração nenhuma.

---

## 2. Receita implementável (fórmulas, não código)

**(L1) Slope $k$.** Para $z^{ka-n}$: $\mathrm{Res}_{a=0}[z^{ka-n}] = \rho_n/k$ (o pólo vem de $z^{\zeta-n}$ em $\zeta = ka$; resíduo em $a$ = resíduo em $\zeta$ dividido por $k$).

**(L2) Parte finita de $c(a)z^{ka-n}$.** Se $c(a) = c_0 + c_1a + O(a^2)$ e $z^{ka-n} = \frac{\rho_n/k}{a} + F_{k,n} + O(a)$, então

$$\boxed{\ \mathrm{FP}_{a=0}\big[c(a)\,z^{ka-n}\big] = c_0\,F_{k,n} + \frac{c_1}{k}\,\rho_n\ }$$

**(L3) Escala.** $\partial_{\ln\mu}R(t) = 2\,\mathrm{Res}[z^a t]$ — a anomalia de escala é **inteiramente** fixada pelo resíduo.

**(L4) Contatos.** $x_j P(q) = -\partial_{q_j}P(q)$; $zP(q) = \Box_q P(q)$. Para a parte finita: $F_{k,n} = F^{\rm nl}_n + \tau_n(q\cdot q)^{n-2}$, onde $\tau_n$ é a **liberdade de contato** e $F^{\rm nl}_n$ é a parte não local (única uma vez fixado o contato).

**(L5) Slopes diferentes dão a mesma parte finita.** $g(2a) = \frac{A}{2a}+B+\ldots$ se $g(a) = \frac{A}{a}+B+\ldots$: $F_{2,n} = F_{1,n}$. A diferença entre esquemas é **só** no contato.

---

## 3. Contagem de contatos escalares: grau de escala $+$ O(4)

Grau de escala $sd$ do objeto singular; liberdade de extensão em derivadas de $\delta$ até ordem $sd-d$; O(4) mantém só $\Box^k\delta$.

| objeto | $sd$ | $sd-d$ | contatos escalares permitidos |
|---|---|---|---|
| $fg = z^{-2}$ | 4 | 0 | $\{\delta\}$ — **1** |
| $(\partial_\mu f)g = -2x_\mu z^{-3}$ | 5 | 1 | nenhum escalar (só $\partial_\mu\delta$, vetorial) |
| $\Box f\cdot g$, $\nabla f\cdot\nabla g \sim z^{-3}$ | 6 | 2 | $\{\Box\delta\}$ — **1** |
| $(\partial_\mu f)(\partial_\nu g) \sim x_\mu x_\nu z^{-4}$ | 8 | 4 | escalares $\{\delta,\ \Box^2\delta\}$ — **2** |
| $z^{-4}$ | 8 | 4 | $\{\delta,\ \Box^2\delta\}$ — **2** |

Em símbolo: $\delta \leftrightarrow 1$, $\Box\delta \leftrightarrow (q\cdot q)$, $\Box^2\delta \leftrightarrow (q\cdot q)^2$.

---

## 4. Leibniz no integrando, polos e os três $\mathrm{FP}$

Identidade exata (para todo $a$ genérico; verificada termo a termo):

$$(\Box f_a)g_a + f_a(\Box g_a) + 2\nabla f_a\cdot\nabla g_a = \Box(f_ag_a) = 8(a-1)(2a-1)\,z^{2a-3},$$

com

$$(\Box f_a)g_a = 4a(a-1)z^{2a-3},\qquad f_a(\Box g_a) = 4a(a-1)z^{2a-3},\qquad 2\nabla f_a\cdot\nabla g_a = 8(a-1)^2 z^{2a-3}.$$

Laurent (usando L1: $k=2$, $n=3$, $\mathrm{Res}_a = \rho_3/2$):

$$z^{2a-3} = \frac{\rho_3}{2a} + F + O(a),\qquad \rho_3 = \frac{\pi^2}{8}(q\cdot q),\qquad F = \mathrm{FP}[z^{2a-3}] = F^{\rm nl} + \tau\,(q\cdot q).$$

Aplicando L2:

**(I)** $c(a) = 4a(a-1) = -4a + 4a^2 \Rightarrow c_0 = 0,\ c_1 = -4$:

$$\boxed{\ \mathrm{FP}\big[(\Box f_a)g_a\big] = -2\rho_3 = \frac{CE}{16}(q\cdot q) = -\frac{\pi^2}{4}(q\cdot q)\ }$$

**(II)** troca de linhas $f\leftrightarrow g$:

$$\mathrm{FP}\big[f_a(\Box g_a)\big] = -2\rho_3 = -\frac{\pi^2}{4}(q\cdot q).$$

**(III)** $c(a) = 8(a-1)^2 = 8 - 16a + 8a^2 \Rightarrow c_0 = 8,\ c_1 = -16$; polo $= 4\rho_3$:

$$\boxed{\ \mathrm{FP}\big[2\nabla f_a\cdot\nabla g_a\big] = 8F - 8\rho_3 = 8F - \pi^2 (q\cdot q)\ }$$

**(Soma)**

$$-2\rho_3 - 2\rho_3 + (8F - 8\rho_3) = 8F - 12\rho_3 .$$

**(Lado direito)** $c(a) = 8(a-1)(2a-1) = 8 - 24a + 16a^2 \Rightarrow c_0 = 8,\ c_1 = -24$; polo $= 4\rho_3$:

$$\mathrm{FP}\big[\Box(f_ag_a)\big] = 8F - 12\rho_3 .$$

**Leibniz preservada na parte finita**: $\;8F - 12\rho_3 = 8F - 12\rho_3$ $\checkmark$. A soma dos três $\mathrm{FP}$ coincide exatamente com o $\mathrm{FP}$ do lado direito, com **o mesmo** $F$.

> **Ponto estrutural (o que isto mostra):** $(\Box f)g$ e $f(\Box g)$ **não têm polo** (o fator $a$ explícito o mata) e seus $\mathrm{FP}$ são **independentes de $\tau$**. Toda a liberdade de contato do par fica, por Leibniz, **no termo de gradiente** $2\nabla f\cdot\nabla g$. A EOM de uma linha ($\Box f = CE\delta$) é exata e **não contém** $z^{-2}$: ela não fixa o contato do par.

---

## 5. $\mathrm{FP}(\Box$ regularizado$)$ vs $R(\Box$ não regularizado$)$

**Aviso de categoria (pedido):** $R$ aplicado a *produto de derivadas* ≠ $R$ aplicado a *produto diferenciado*. $R(\nabla f\cdot\nabla g)$ envolve $z^{-3}$ sem $x_\mu$; $R(\nabla(fg)) = R(-4x_\mu z^{-3})$ envolve $x_\mu$ sobre o polinômio de $\delta$, e pela regra $x_\mu\to-\partial_{q_\mu}$ produz contatos vetoriais. **Não** se substitui a derivada de uma linha pela derivada total do par.

$L := R(\Box(fg))$, com $\Box(fg) = 8z^{-3}$ **não regularizado**:

$$R(8z^{-3}) = 8\,\mathrm{FP}\big[(1-a)\mu^{2a}z^{a-3}\big] = 8\big[F_3 + (2\ln\mu - 1)\rho_3\big],$$

pois $(1-a)\mu^{2a} = 1 + a(2\ln\mu - 1) + O(a^2)$ e $z^{a-3} = \frac{\rho_3}{a}+F_3+O(a)$.

Comparação (com $F = F_3$ por L5):

$$\boxed{\ \Delta := R(\Box(fg)) - \mathrm{FP}[\Box(f_ag_a)] = 4(4\ln\mu + 1)\,\rho_3 = \frac{\pi^2}{2}(4\ln\mu + 1)(q\cdot q)\ }$$

ou seja, $\Delta = \frac{\pi^2}{2}(4\ln\mu+1)\,\Box\delta$ na convenção $q\cdot q\leftrightarrow\Box\delta$.

Com contatos independentes $F = F^{\rm nl}+\tau(q\cdot q)$, $F_3 = F^{\rm nl}+\tau_3(q\cdot q)$:

$$\Delta = 8(\tau_3 - \tau)(q\cdot q) + 4(4\ln\mu+1)\rho_3 .$$

**Leitura:** $\Delta$ é **puro contato local**; sua parte $\propto\ln\mu$ está **fixada pelo resíduo** (L3) e **não é ajustável**; sua parte finita é **livre** e é exatamente $\tau_3-\tau$. Isto é a distinção pedida: *resíduo fixa a anomalia de escala; o esquema fixa o contato finito*.

Estruturalmente, $C_D(t) = R(Dt) - DR(t)$ é sempre **local** ($D$ e $R$ diferem só sobre o suporte singular $\{0\}$), e pela regra L3 sua parte em $\ln\mu$ é $2\,\mathrm{Res}[z^at]$.

---

## 6. Uma derivada externa distribuída nas linhas

Por **troca de linhas**, $(\partial_\mu f_a)g_a = f_a(\partial_\mu g_a) = 2(a-1)x_\mu z^{2a-3}$; a soma é $\partial_\mu(f_ag_a) = 4(a-1)x_\mu z^{2a-3}$ — mas **não** se substitui uma pela total.

L2 ($c_0=-2$, $c_1=2$; $x_\mu$ atua por $-\partial_{q_\mu}$ nos contatos):

$$\mathrm{FP}\big[(\partial_\mu f_a)g_a\big] = -2x_\mu F + x_\mu\rho_3 .$$

Com $x_\mu \rho_3 = -\partial_{q_\mu}\!\left(\tfrac{\pi^2}{8}q\cdot q\right) = -\tfrac{\pi^2}{4}q_\mu$ e $x_\mu(\tau\,q\cdot q) = -2\tau q_\mu$:

$$\mathrm{FP}\big[(\partial_\mu f_a)g_a\big] \supset \left(4\tau - \frac{\pi^2}{4}\right)q_\mu \ \leftrightarrow\ \left(4\tau - \frac{\pi^2}{4}\right)\partial_\mu\delta .$$

O contato é **vetorial** ($\partial_\mu\delta$), de grau de escala $sd-d = 1$, e é **único** por linha; a troca de linhas obriga os dois a serem iguais, e a soma carrega $2\times$.

---

## 7. Duas derivadas externas distribuídas

Três canais: $(2,0)$, $(1,1)$, $(0,2)$.

$$(\partial_\mu\partial_\nu f_a)g_a = 2(a-1)\big[\delta_{\mu\nu}z^{2a-3} + 2(a-2)x_\mu x_\nu z^{2a-4}\big]$$

$$\mathrm{FP} = \delta_{\mu\nu}\big(-2F + \rho_3\big) + x_\mu x_\nu\big(8F_4 - 6\rho_4\big),\qquad F_4 = \mathrm{FP}[z^{2a-4}].$$

$$(\partial_\mu f_a)(\partial_\nu g_a) = 4(a-1)^2 x_\mu x_\nu z^{2a-4},\qquad \mathrm{FP} = 4x_\mu x_\nu F_4 - 4x_\mu x_\nu\rho_4 .$$

Contraste escalar ($\mu=\nu$, $x\cdot x = z\to\Box_q$): usando $z\rho_4 = \rho_3$ (checcado em 1.1b) e $zF_4 = F$,

$$\mathrm{FP}[\nabla f\cdot\nabla g] = 4F - 4\rho_3\quad\checkmark\ \ \text{(coincide com (III)/2)}.$$

**Condição de consistência do esquema:** $zF_4 = F$ (isto é, multiplicar a extensão por $z$ coincide com estender $z\cdot$integrande) vale **somente** se o contato for compatível com $z\to\Box_q$. Se não, aparece um contato adicional — é exatamente o aviso *"não multiplicar $\delta$ por $f$ sem definir extensão"*.

Dois canais escalares independentes aparecem aqui ($\delta$ e $\Box^2\delta$, §3), e mais uma vez a soma $(2,0)+(0,2)+2(1,1)$ fecha por Leibniz no integrando, com toda a liberdade concentrada nos contatos.

---

## 8. A resposta à pergunta

### 8.1 Contatos escalares independentes, antes do esquema

Para uma inserção Euler ($\mathcal E = x\cdot\partial_x$) num par $f=g=1/z$ em $\mathbb R^4$, com até duas derivadas externas:

1. **$\tau_0\,\delta^{(4)}(x)$** — setor do par $z^{-2}$ ($sd-d = 0$);
2. **$\tau_1\,\Box\delta^{(4)}(x)$** — setor $z^{-3}$ ($\Box$ numa linha, ou $\nabla f\cdot\nabla g$);
3. **$\tau_2\,\Box^2\delta^{(4)}(x)$** — setor $z^{-4}$ (duas derivadas externas).

Se os índices externos ficam abertos, juntam-se os **não escalares** $\tau_v\partial_\mu\delta$ (1 derivada) e $\tau_{v2}\partial_\mu\partial_\nu\delta$, $\delta_{\mu\nu}\Box\delta$ (2 derivadas) — excluídos de um canal estritamente escalar por O(4).

> **Caso puro de Euler (sem derivadas externas):** $\mathcal E(fg) = -4z^{-2}$, $(\mathcal E f)g = f(\mathcal E g) = -2z^{-2}$. Há **exatamente um** contato escalar independente: $\tau\,\delta$.

### 8.2 Constraints lineares (Leibniz, troca de linhas, escala, O(4), resíduo)

| # | constraint | efeito |
|---|---|---|
| C1 | **Troca de linhas** $f\leftrightarrow g$ | coeficiente de linha 1 = coeficiente de linha 2; combinação antissimétrica $(\Box f)g - f(\Box g)$ tem extensão nula. Reduz 2 parâmetros → 1 |
| C2 | **Leibniz** | $\tau[(\Box f)g] + \tau[f(\Box g)] + \tau[2\nabla f\cdot\nabla g] = \tau[\Box(fg)]$ — mesma soma dos $\mathrm{FP}$ do §4; fixa o *reparto*, não o *valor* |
| C3 | **Grau de escala / Euler** | $x\cdot\partial$ desloca o grau em 1; só $\Box^k\delta$ com $2k \le sd-d$; proíbe contatos de grau superior |
| C4 | **O(4)** | só $\Box^k\delta$ no canal escalar |
| C5 | **Resíduo** | fixa a parte $\propto\ln\mu$ (L3) e a *forma* local $\Box^{n-2}\delta$; **não** fixa a parte finita |

### 8.3 Elas fixam $\tau$?

**Não.** C1+C2+C3+C4 reduzem o número de parâmetros a **um por potência singular independente** ($\tau_0,\tau_1,\tau_2$), mas **nenhum deles é determinado** por Leibniz, troca de linhas, grau de escala ou resíduos. A determinação exige **esquema** (ou uma normalização física/EOM, que é um ato posterior, não uma consequência). No esquema analítico do operador $R$ os $\tau$ ficam fixados *por escolha* de $R$ (o fator $(1-a)$ subtrai exatamente um resíduo; $\mu$ entra via L3) — isso é **escolha**, não derivação.

---

## 9. Controles $\tau = 0,\ 1,\ \tfrac12$ (diagnósticos; nenhum adotado)

| $\tau$ | $(\Box f)g$ | $2\nabla f\cdot\nabla g$ | soma $=\mathrm{FP}[\Box(f_ag_a)]$ | $\Delta$ (vs $R$) |
|---|---|---|---|---|
| $0$ | $-\frac{\pi^2}{4}(q\cdot q)$ | $8F^{\rm nl} - \pi^2(q\cdot q)$ | $8F^{\rm nl} - \frac{3\pi^2}{2}(q\cdot q)$ | $4(4\ln\mu+1)\rho_3 + 8\tau_3(q\cdot q)$ |
| $1$ | idem | $8F^{\rm nl} + 7\pi^2(q\cdot q)$ | $8F^{\rm nl} + \frac{13\pi^2}{2}(q\cdot q)$ | $+\,8(\tau_3-1)(q\cdot q)$ no termo finito |
| $\tfrac12$ | idem | $8F^{\rm nl} + 3\pi^2(q\cdot q)$ | $8F^{\rm nl} + \frac{9\pi^2}{2}(q\cdot q)$ | $+\,8(\tau_3-\tfrac12)(q\cdot q)$ |

Observações: (i) os **resíduos** ($\rho_2,\rho_3,\rho_4$), o **polo**, a **parte não local** e o **running em $\ln\mu$** são idênticos nos três controles; (ii) $(\Box f)g$ é **insensível** a $\tau$; (iii) a soma muda — logo os três valores são **inequivalentes** e **nenhum é preferido** por Leibniz/troca/resíduo. **$\tau=0,1,1/2$ são diagnósticos; nenhum é adotado.**

---

## 10. Separação obrigatória: resíduos × admissibilidade de normalização EOM

1. **O que os resíduos dão (e só isso):** o pólo; o coeficiente da anomalia de escala ($\partial_{\ln\mu}R = 2\,\mathrm{Res}$); a *forma* local admissível ($\Box^{n-2}\delta$); as relações de coerência $z\rho_{n+1} = \rho_n$.
2. **O que eles não dão:** a parte finita local ($\tau$); e **não definem $\delta\cdot f$**. A igualdade de polinômios em $q$ (resíduo a resíduo) **não** define o produto $\delta\cdot f$; esse produto exige extensão. Por isso $\mathrm{FP}[(\Box f_a)g_a]$ é a **definição** do composto $(\Box f)g$, não a sua derivação.
3. **EOM:** $\Box f = CE\,\delta$ é **exata para uma linha** e não envolve $z^{-2}$; portanto ela **não** fixa os contatos do par. Impor, por exemplo, $\Box R(fg) = R(\Box(fg))$ é **fixar** $\tau$ (= escolher esquema), não derivar.
4. **Proibições respeitadas:** nenhum coeficiente é ajustado para cancelar um resíduo conhecido (em particular não se escolhe $\tau$ para zerar $\Delta$); concordância de modelos não é usada como prova; nada de QME gravitacional.

---

## 11. Hipóteses, limites, lacunas

**Hipóteses.** (H1) $d = 4$ euclidiano; (H2) regulador analítico $z^a$ com distribuição do regulador **simétrica** entre as linhas ($f_a=g_a=z^{a-1}$); (H3) unicidade da extensão quando $sd<d$; (H4) O(4) para o canal escalar; (H5) par idêntico $f=g=1/z$; (H6) convenção do operador $q_\mu\leftrightarrow\partial_\mu\delta$, $x_j\to-\partial_{q_j}$, verificada internamente em §1.1.

**Limites.**
- **(L-a)** A escolha do par regulador é **ela mesma** um esquema: com reguladores independentes $z^{a}f\cdot z^{b}g$ (e $b\to a$ no fim) os contatos mudam; é fonte adicional de liberdade $\tau$, não contabilizada em §8.1.
- **(L-b)** As derivadas acima são manuais — `[DECLARADO]` até verificação local (CAS/receipt); nenhum código foi fornecido nem executado.
- **(L-c)** Sem continuação lorentziana; resultados estritamente euclidianos.
- **(L-d)** $F^{\rm nl}_n$, $F_4$ ficaram simbólicos: dão a parte não local padrão (tipo $\mathrm{Pf}$) uma vez fixado $\tau$; fórmulas fechadas podem ser extraídas da família meromorfa, mas não foram recalculadas aqui.
- **(L-e)** Nada de QME gravitacional, nada de Q2, nada de confirmação, nada de proveniência externa.

**Lacunas declaradas.** (i) o significado de "inserção Euler" (§0); (ii) a verificação local das expressões; (iii) a compatibilidade $zF_4 = F$ entre extensões de ordens vizinhas (é condição de esquema, não teorema); (iv) o caso de linhas desiguais ($f\ne g$, massas diferentes) não foi tratado; (v) contatos tensoriais de dois índices só esboçados; (vi) nenhuma palavra sobre a unidade anterior (Wick/$X,Y$/BV/enumeração Euler) — fora de escopo por definição.

---

## 12. Síntese operacional

$$\boxed{\ \mathrm{FP}[(\Box f_a)g_a] = \mathrm{FP}[f_a(\Box g_a)] = -2\rho_3 = \frac{CE}{16}(q\cdot q) = -\frac{\pi^2}{4}\Box\delta\ }$$
$$\boxed{\ \mathrm{FP}[2\nabla f_a\cdot\nabla g_a] = 8F - 8\rho_3,\qquad \mathrm{soma} = 8F - 12\rho_3 = \mathrm{FP}[\Box(f_ag_a)]\ }$$
$$\boxed{\ R(\Box(fg)) - \mathrm{FP}[\Box(f_ag_a)] = 4(4\ln\mu+1)\rho_3 + 8(\tau_3-\tau)(q\cdot q)\ }$$

**Resposta à pergunta:** antes da escolha de esquema, Leibniz + troca de linhas + grau de escala + O(4) permitem, para uma inserção Euler num par, **exatamente um contato escalar independente por potência singular** — $\tau\delta$ no setor do par, $\tau'\Box\delta$ no setor $z^{-3}$, $\tau''\Box^2\delta$ no setor $z^{-4}$ — e as constraints **não** fixam $\tau$: elas só obrigam a simetria de linhas e a soma de Leibniz. Os resíduos fixam a anomalia de escala ($\propto\ln\mu$) e a forma dos contatos; a parte finita é liberdade de esquema. Os controles $\tau = 0, 1, 1/2$ são diagnósticos e nenhum deles é adotado.

**Pendência de ação externa (não disponível nesta etapa):** verificação local por CAS/receipt das expressões dos §§4–7 e, se for o caso, a fixação de $\tau$ por uma normalização declarada — ato posterior, nunca derivado aqui.

`DECLARADO até verificação local · sem execução · sem QME · sem Q2 · originais intactos`