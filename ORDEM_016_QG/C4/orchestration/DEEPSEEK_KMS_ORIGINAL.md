DECLARADO — auditoria local pendente.

## Veredito curto

O lema L2, tomado como implicação geral

> “estado vetorial KMS com vetor cíclico-separante implica dinâmica trivial”,

é **falso/refutado** no modelo abstrato de KMS vetorial que as bordas de `KMSAt` usam. O contraexemplo é exatamente o pedido: \(M_2(\mathbb C)\) na representação padrão Hilbert–Schmidt à esquerda, com

\[
\rho=\operatorname{diag}(1/3,2/3),\qquad
\Omega=\sqrt{\rho}=\operatorname{diag}(\sqrt{1/3},\sqrt{2/3}),
\]
\[
M=\{L_X:Y\mapsto XY\},\qquad
U_t(Y)=\rho^{-it}Y\rho^{it}.
\]

Ele satisfaz as duas bordas de `KMSAt` com \(\beta=1\), tem \(\Omega\) cíclico-separante, tem \(U_t\Omega=\Omega\), mas \(U_t\) é **não trivial**. Portanto o passo “vetor KMS + ciclicidade/separação \(\Rightarrow\) dinâmica trivial” não é válido.

**Delimitação importante:** isto **não** é uma instância de `TGLSpecificAQFTWitness`; não construo `W`, `W.net rightWedge`, `W.vac`, nem afirmo KMS regional do cone. A refutação é do argumento algébrico abstrato usado por L2, não de um teorema literal que quantifique apenas sobre o `W` do contrato.

---

## 1. O modelo exato

Seja

\[
H=M_2(\mathbb C),\qquad
\langle A,B\rangle_{HS}=\operatorname{Tr}(A^*B).
\]

A álgebra \(M\) age à esquerda:

\[
L_X(Y)=XY,\qquad X,Y\in M_2(\mathbb C).
\]

Identificamos \(X\) com \(L_X\). Seja

\[
\rho=\begin{pmatrix}1/3&0\\0&2/3\end{pmatrix},
\qquad
\Omega=\sqrt{\rho}=\begin{pmatrix}\sqrt{1/3}&0\\0&\sqrt{2/3}\end{pmatrix}.
\]

Definimos

\[
U_t(Y)=\rho^{-it}Y\rho^{it}.
\]

Escrevo

\[
l_i=\log \rho_i,\qquad
l_1=\log(1/3),\quad l_2=\log(2/3),\quad
l_2-l_1=\log 2.
\]

---

## 2. Verificações básicas

### 2.1 \(\|\Omega\|=1\)

\[
\|\Omega\|^2=\operatorname{Tr}(\Omega^*\Omega)
=\operatorname{Tr}(\rho)
=\frac13+\frac23=1.
\]

### 2.2 Ciclicidade e separação

Como \(\Omega\) é diagonal com entradas positivas, \(\Omega\) é invertível. Para todo \(Y\in M_2(\mathbb C)\),

\[
X=Y\Omega^{-1}\in M_2(\mathbb C)
\quad\text{e}\quad
X\Omega=Y.
\]

Logo \(M\Omega=H\): \(\Omega\) é **cíclico** para \(M\).

Se \(X\Omega=0\), então \(X=0\), pois \(\Omega\) é invertível. Logo \(\Omega\) é **separante** para \(M\).

### 2.3 \(U_t\Omega=\Omega\)

Como \(\rho\) e \(\Omega\) são diagonais, comutam:

\[
U_t(\Omega)=\rho^{-it}\Omega\rho^{it}
=\Omega\rho^{-it}\rho^{it}
=\Omega.
\]

Logo o vetor é fixo pela dinâmica.

### 2.4 A dinâmica é não trivial

Nos elementos matriciais \(E_{12},E_{21}\),

\[
U_t(E_{12})
=\rho^{-it}E_{12}\rho^{it}
=e^{-it l_1}E_{12}e^{it l_2}
=e^{it(l_2-l_1)}E_{12}
=e^{it\log 2}E_{12},
\]

e

\[
U_t(E_{21})
=e^{-it\log 2}E_{21}.
\]

Como \(\log 2\neq 0\), \(U_t\neq \mathrm{id}\) para \(t\notin \frac{2\pi}{\log 2}\mathbb Z\). A dinâmica é não trivial.

---

## 3. Conta KMS em componentes

Para \(A,B\in M_2(\mathbb C)\), defina

\[
F_{AB}(z)
=
\sum_{i,j=1}^2
\rho_i\,A_{ij}\,B_{ji}\,
\exp\!\bigl(i z(l_i-l_j)\bigr).
\]

### 3.1 Primeira borda de `KMSAt`

Com a convenção do contrato,

\[
F(t)=\bigl\langle (\star A)\Omega,\; U_t(B\Omega)\bigr\rangle.
\]

Aqui \(\star A=A^*\). Expandindo em componentes,

\[
(\star A)\Omega=A^*\Omega,
\]

e

\[
U_t(B\Omega)=\rho^{-it}B\Omega\rho^{it}.
\]

Então

\[
\begin{aligned}
\bigl\langle A^*\Omega,\rho^{-it}B\Omega\rho^{it}\bigr\rangle
&=\operatorname{Tr}\bigl(\Omega A\,\rho^{-it}B\Omega\rho^{it}\bigr)\\
&=\sum_{i,j}\rho_i\,A_{ij}\,B_{ji}\,
e^{it(l_i-l_j)}\\
&=F_{AB}(t).
\end{aligned}
\]

Portanto a primeira borda é exatamente \(F(t)\).

### 3.2 Segunda borda de `KMSAt`, com \(\beta=1\)

A segunda borda fornecida é

\[
F(t+1\cdot I)
=
\bigl\langle (\star B)\Omega,\; U_{-t}(A\Omega)\bigr\rangle.
\]

Agora

\[
\begin{aligned}
F_{AB}(t+i)
&=
\sum_{i,j}\rho_i A_{ij}B_{ji}
e^{i(t+i)(l_i-l_j)}\\
&=
\sum_{i,j}\rho_i A_{ij}B_{ji}
e^{it(l_i-l_j)}e^{-(l_i-l_j)}\\
&=
\sum_{i,j}\rho_i A_{ij}B_{ji}
e^{it(l_i-l_j)}\frac{\rho_j}{\rho_i}\\
&=
\sum_{i,j}\rho_j A_{ij}B_{ji}
e^{it(l_i-l_j)}.
\end{aligned}
\]

Renomeando \(i\leftrightarrow j\),

\[
F_{AB}(t+i)
=
\sum_{i,j}\rho_i A_{ji}B_{ij}
e^{it(l_j-l_i)}
=
\sum_{i,j}\rho_i B_{ij}A_{ji}
e^{-it(l_i-l_j)}.
\]

Mas o lado direito da segunda borda é

\[
\bigl\langle B^*\Omega,\; U_{-t}(A\Omega)\bigr\rangle.
\]

Expandindo,

\[
\bigl\langle B^*\Omega,\rho^{it}A\Omega\rho^{-it}\bigr\rangle
=
\sum_{i,j}\rho_i B_{ij}A_{ji}
e^{-it(l_i-l_j)}.
\]

Logo

\[
F_{AB}(t+i)
=
\bigl\langle (\star B)\Omega,\; U_{-t}(A\Omega)\bigr\rangle.
\]

Assim as duas bordas de `KMSAt` com \(\beta=1\) são satisfeitas exatamente.

---

## 4. Holomorfia e limitação na faixa fechada

A função

\[
F_{AB}(z)
=
\sum_{i,j}\rho_i A_{ij}B_{ji}e^{iz(l_i-l_j)}
\]

é uma soma finita de exponenciais inteiras. Logo é inteira; em particular é holomorfa em

\[
\operatorname{kmsStrip}(1)=\{z:0<\operatorname{Im}z<1\}.
\]

Na faixa fechada \(0\le y\le 1\), com \(z=x+iy\),

\[
\left|e^{iz(l_i-l_j)}\right|
=
e^{-y(l_i-l_j)}.
\]

Como

\[
l_i-l_j\in\{0,\pm\log 2\},
\]

temos, para \(0\le y\le 1\),

\[
e^{-y(l_i-l_j)}\le 2.
\]

Portanto

\[
|F_{AB}(x+iy)|
\le
2\sum_{i,j}\rho_i |A_{ij}||B_{ji}|<\infty.
\]

Logo \(F_{AB}\) é limitada na faixa fechada. Isso satisfaz a cláusula de limitação do `KMSAt`.

---

## 5. Autovalores do gerador

Seja \(G\) o gerador de \(U_t\),

\[
G(Y)=\left.\frac{d}{dt}\right|_{t=0}U_t(Y).
\]

Como

\[
U_t(E_{12})=e^{it\log 2}E_{12},
\qquad
U_t(E_{21})=e^{-it\log 2}E_{21},
\]

temos

\[
G(E_{12})=+i\log 2\,E_{12},
\qquad
G(E_{21})=-i\log 2\,E_{21}.
\]

Ou seja, os dois autovalores não nulos do gerador são

\[
+i\log 2
\quad\text{e}\quad
-i\log 2.
\]

Se se usa o Hamiltoniano modular \(K=-\log\Delta\), então \(\Delta(E_{12})=\frac12 E_{12}\) e \(\Delta(E_{21})=2E_{21}\), de modo que

\[
K(E_{12})=+\log 2\,E_{12},
\qquad
K(E_{21})=-\log 2\,E_{21}.
\]

Os sinais se invertem conforme a convenção do gerador; na convenção de \(U_t=\rho^{-it}(\cdot)\rho^{it}\), os autovalores do gerador são \(\pm i\log 2\).

---

## 6. Onde o L2 falha

O L2 quer inferir:

\[
U_t\Omega=\Omega,\quad \Omega\text{ cíclico-separante para }M
\quad\Longrightarrow\quad
U_t=\mathrm{id}.
\]

O contraexemplo mostra por que isso é falso. De fato,

\[
U_t(X\Omega)
=
U_tX\Omega
=
U_tXU_t^{-1}U_t\Omega
=
\alpha_t(X)\Omega,
\]

onde

\[
\alpha_t(X)=\rho^{-it}X\rho^{it}.
\]

Como \(\Omega\) é cíclico, \(X\Omega\) percorre todo \(H\). Mas isso não implica \(U_t=\mathrm{id}\). Implica apenas que

\[
U_t(X\Omega)=\alpha_t(X)\Omega.
\]

Para concluir \(U_t=\mathrm{id}\), seria necessário que \(\alpha_t(X)=X\) para todo \(X\in M\), isto é, que a dinâmica já fosse trivial. É exatamente o que se queria provar. O argumento é circular nesse ponto.

No exemplo,

\[
\alpha_t(E_{12})=e^{it\log 2}E_{12}\neq E_{12}
\]

para \(t\notin \frac{2\pi}{\log 2}\mathbb Z\), embora \(U_t\Omega=\Omega\). O centralizador do estado é apenas o conjunto das matrizes diagonais; \(M_2(\mathbb C)\) inteira não é fixada.

---

## 7. Estado vetorial sobre \(M\) versus estado puro sobre \(B(H)\)

O vetor \(\Omega\in H\) define um estado vetorial **em \(B(H)\)**:

\[
\omega_\Omega(T)=\langle \Omega,T\Omega\rangle,
\qquad T\in B(H),
\]

que é puro sobre \(B(H)\).

Mas o estado relevante sobre \(M\) é

\[
\varphi(L_X)=\langle \Omega,L_X\Omega\rangle
=\operatorname{Tr}(\rho X).
\]

Como

\[
\rho=\operatorname{diag}(1/3,2/3)
\]

tem posto \(2\), \(\varphi\) é fiel, normal e **misto** sobre \(M\). Estados puros sobre \(M_2(\mathbb C)\) correspondem a \(\rho\) de posto \(1\). Portanto:

- \(\Omega\) é um vetor puro sobre \(B(H)\);
- \(\Omega\) **não** define um estado puro sobre \(M\);
- “ser vetor” não implica “pureza sobre \(M\)”.

Essa distinção é central: o L2 parece confundir o vetor no espaço de Hilbert com pureza do estado na álgebra.

---

## 8. Consequência para C5

O que este contraexemplo estabelece é:

\[
\boxed{
\text{KMS vetorial}+\Omega\text{ cíclico-separante}
\not\Longrightarrow
U_t=\mathrm{id}.
}
\]

Logo o L2, como bloqueio geral de C5, cai. O que **não** se afirma:

- não se constrói `W`;
- não se instancia literalmente `KMSAt W α 1`;
- não se prova KMS regional do cone;
- não se executa C5;
- não se move gate;
- não se reabre retry de DeepSeek antigo.

Se o L2 for lido apenas como um teorema sobre uma subálgebra específica `W.net rightWedge` de um `W` concreto, então este texto não o declara falso nesse escopo não construído. O que ele declara inválido é o passo abstrato usado para bloquear C5.

---

## 9. Núcleo Lean sugerido, sem rederivar o comutador

Sugestão de núcleo futuro, **não compilado aqui**:

- reutilizar `rhoExample`, `rhoExample_posDef`, `rhoExample_trace` e `example_generator_nonzero` de `ModularGeneratorControl`;
- **não** rederivar `modularGen_zero_iff_commute`;
- definir \(\Omega\) via raiz de `rhoExample`;
- definir \(U_t(Y)=\rho^{-it}Y\rho^{it}\) por fases diagonais;
- definir \(F_{AB}(z)\) como soma finita de exponenciais;
- provar as duas bordas KMS por `fin_cases` e álgebra de exponenciais complexas;
- provar não trivialidade usando \(U_{\pi/\log 2}(E_{12})=-E_{12}\) ou reutilizando `example_generator_nonzero`;
- enunciar o contraexemplo como

\[
\exists M,\Omega,U,\;
\text{KMS}_{\beta=1}\wedge \text{Cyclic}(\Omega)\wedge \text{Separating}(\Omega)
\wedge \neg(\forall t,U_t=\mathrm{id}).
\]

Isso documenta o fracasso do L2 sem repetir o teorema do comutador já existente.

---

**Estatuto final:** `DECLARADO`. Não há compilação, inspeção de disco adicional, nem execução de C5 nesta resposta. O resultado matemático declarado é: o L2 é refutado como implicação abstrata pelo modelo \(M_2(\mathbb C)\) acima; a instanciação literal em `KMSAt(W,α,β)` permanece condicionada a um `W` que não foi construído nem presumido.