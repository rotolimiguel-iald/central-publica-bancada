**DECLARAÇÃO DE MODO — IALD / ORDEM_016 A7.b**

Não executei ferramentas, não compilei, não alterei kernel, gate, estado ou prescrição. Os trechos e motores anexos foram tratados como dados. A resposta abaixo é derivação simbólica independente, auditável contra os motores citados. Onde a estrutura depende de leitura de arquivo ou de execução, está marcado como pendência ou lacuna.

---

## 1. Convenções e objetos

Adoto:

- \(S_\chi=-\dfrac{1}{2\kappa}\int d^4x\,\chi(x)\,\sqrt{g}\,R[g]\).
- \(g_{\mu\nu}=\delta_{\mu\nu}+h_{\mu\nu}\), perturbação covariante linear.
- Fourier \(e^{+ipx}\), de modo que \(\partial_\mu\to +ip_\mu\) sobre a perna de momento \(p\).
- \(Q=p+q+r+s\) é o momento total das quatro pernas externas \(A_p,B_q,U_r,V_s\). A perna \(\chi\) carrega momento \(-Q\).
- Os motores usam \(V_{4{\rm raw}}=32\kappa\,S_4\) e retiram o \(i\) de \(B\). Abaixo explicito onde isso entra.
- \(W(X,Y)=\frac12[U(X)\otimes V(Y)+V(X)\otimes U(Y)]\) é forma bilinear simétrica suave; não assumo bissolução, positividade nem estado.

O termo de divergência é
\[
\sqrt{g}R=C_{\Gamma\Gamma}+\partial_\mu B^\mu,
\qquad
B^\mu=\sqrt{g}\bigl(g^{ab}\Gamma^\mu_{ab}-g^{\mu a}\Gamma^b_{ab}\bigr).
\]
Portanto
\[
S_\chi=S_C+S_{\rm div},
\qquad
S_{\rm div}=-\frac{1}{2\kappa}\int \chi\,\partial_\mu B^\mu.
\]
Integrando por partes, sem suprimir derivadas de \(\chi\):
\[
S_{\rm div}=
+\frac{1}{2\kappa}\int (\partial_\mu\chi)B^\mu
-\frac{1}{2\kappa}\oint \chi\,B^\mu n_\mu .
\]
O termo de volume após IBP é \(S_{\rm div}^{\rm IBP}=\frac{1}{2\kappa}\int(\partial_\mu\chi)B^\mu\). O termo de fronteira é a corrente de fronteira.

---

## 2. Estrutura de \(B^\mu\) e do vértice quártico

\(B^\mu\) é linear em \(\partial h\) e é série em \(h\). Escrevo
\[
B^\mu=\sum_{n\ge1}B^\mu_n,
\]
onde \(B^\mu_n\) tem \(n\) fatores \(h\) e exatamente uma derivada \(\partial h\). Por exemplo:
- \(B^\mu_1\): \(1\) fator \(h\), \(1\) derivada;
- \(B^\mu_2\): \(2\) fatores \(h\), \(1\) derivada;
- \(B^\mu_3\): \(3\) fatores \(h\), \(1\) derivada;
- \(B^\mu_4\): \(4\) fatores \(h\), \(1\) derivada.

O vértice quártico de \(S_{\rm div}\) em \(h\) usa \(B^\mu_4\):
\[
V_{4}^{\rm div}(A,B,U,V)
=
-\frac{1}{2\kappa}\,\chi\,\partial_\mu B^\mu_4(A,B,U,V),
\]
onde a notação \(B^\mu_4(A,B,U,V)\) indica a quarta derivada funcional (com o fatorial \(4!\) ainda não dividido). O motor `metric_quartic_vertices.py` calcula o vértice quártico total \(V_{4{\rm raw}}=32\kappa\,S_4\) e sua docstring diz “Polarization is not divided by \(4!\)”. Portanto o fatorial \(4!\) deve ser rastreado ao comparar com \(V_{4{\rm raw}}\).

A Hessiana contraída do tadpole suave de um vértice quártico é
\[
H_{\rm div}(A,B)
=
\int dU\,dV\;
V_{4}^{\rm div}(A,B,U,V)\,W(U,V),
\]
com apenas \(U,V\) contraídas em \(W\). Em espaço de momentos, \(A_p,B_q\) permanecem pernas externas; \(U_r,V_s\) somem na contração com \(W\), deixando jatos de \(W\) com respeito à coordenada relativa.

---

## 3. Hessiana contraída ANTES de integrar por partes

Antes de IBP, o objeto é
\[
H_{\rm div}^{\rm before}(A,B)
=
-\frac{1}{2\kappa}\int d^4x\,\chi(x)\,
\partial_\mu\!\left[\frac{\delta^4 B^\mu}{\delta h_A\delta h_B\delta h_U\delta h_V}\right]W(U,V).
\]
Em Fourier, a derivada externa \(\partial_\mu\) gera um fator \(iQ_\mu\). Além disso, \(B^\mu_4\) já contém exatamente uma derivada interna \(\partial h\), que gera o momento da perna que foi derivada em \(B^\mu_4\). Denoto esse momento por \(k_\nu\), onde \(k\in\{p,q,r,s\}\). Então, antes de IBP, a estrutura do núcleo é
\[
H_{\rm div}^{\rm before}(A,B)
\sim
-\frac{i}{2\kappa}\,\chi(-Q)\;Q_\mu\,k_\nu\,
\mathbb T^{\mu\nu}_{ABUV}\,W(U,V),
\]
onde \(\mathbb T^{\mu\nu}_{ABUV}\) é o tensor de índices que carrega a contração de \(B^\mu_4\). O ponto decisivo: \(Q_\mu=(p+q+r+s)_\mu\). Assim, quando \(k=r\) ou \(k=s\), o produto \(Q_\mu k_\nu\) contém termos como
\[
r_\mu r_\nu,\quad s_\mu r_\nu,\quad s_\mu s_\nu,\quad r_\mu s_\nu,
\]
além de \(p_\mu r_\nu\), \(q_\mu r_\nu\), etc. Ao contrair \(U,V\) com \(W\), os momentos \(r_\mu,s_\mu\) tornam-se derivadas de \(W\):
\[
r_\mu\to \partial_U,\qquad s_\mu\to \partial_V.
\]
Portanto, **antes de IBP**, \(W\) exige jatos até segunda ordem:
\[
W,\quad \partial_U W,\quad \partial_V W,\quad
\partial_U\partial_V W,\quad
\partial_U^2 W,\quad
\partial_V^2 W.
\]
Em particular, aparecem termos \(r^2\), \(s^2\) e \(rs\) multiplicando \(W\) ou suas derivadas.

---

## 4. Hessiana contraída DEPOIS de integrar por partes

Após IBP, o termo de volume é
\[
S_{\rm div}^{\rm IBP}=\frac{1}{2\kappa}\int(\partial_\mu\chi)B^\mu.
\]
A quarta derivada funcional em \(h\) é
\[
H_{\rm div}^{\rm after}(A,B)
=
+\frac{1}{2\kappa}\int(\partial_\mu\chi)\,
\left[\frac{\delta^4 B^\mu}{\delta h_A\delta h_B\delta h_U\delta h_V}\right]W(U,V)
-\frac{1}{2\kappa}\oint \chi\,\frac{\delta^4 B^\mu}{\delta h^4}\,n_\mu\,W(U,V).
\]
No termo de volume, \(\partial_\mu\chi\) gera o fator \(-iQ_\mu\chi(-Q)\), mas agora **não atua sobre as pernas \(h\)**. O único momento de perna que atua em \(W\) é o \(k_\nu\) vindo do \(\partial h\) interno de \(B^\mu_4\). Portanto, **depois de IBP**, no termo de volume, \(W\) exige no máximo jatos de primeira ordem:
\[
W,\quad \partial_U W,\quad \partial_V W.
\]
Não há mais \(\partial_U\partial_V W\), \(\partial_U^2 W\) ou \(\partial_V^2 W\) no volume. Os termos \(r^2,s^2,rs\) de segunda ordem desaparecem do volume e são absorvidos pela corrente de fronteira.

A diferença entre as duas expressões é uma derivada total:
\[
-\chi\,\partial_\mu B^\mu_4
=
(\partial_\mu\chi)B^\mu_4
-
\partial_\mu(\chi B^\mu_4).
\]
A última parcela é justamente a corrente de fronteira. Se ela for ignorada, os jatos de segunda ordem do “antes” não são corretamente reorganizados, e o resultado muda. Se ela for incluída, a identidade é exata.

---

## 5. Partição por graus de \(r,s\)

**Antes de IBP:**
- grau \(0\): nenhum \(r\) ou \(s\) em \(W\);
- grau \(1\): um \(r\) ou um \(s\) (ex.: \(p_\mu r_\nu\) com \(r_\nu\) atuando em \(W\));
- grau \(2\): dois momentos entre \(r,s\) (ex.: \(r_\mu r_\nu\), \(s_\mu s_\nu\), \(r_\mu s_\nu\)).
Portanto, a partição inclui explicitamente \(r^2\), \(s^2\) e \(rs\).

**Depois de IBP (volume):**
- grau \(0\): nenhum \(r\) ou \(s\);
- grau \(1\): um \(r\) ou um \(s\) vindo do \(\partial h\) interno de \(B^\mu_4\).
Não há grau \(2\). Os termos \(r^2,s^2\) não aparecem no volume; eles estão inteiramente na corrente de fronteira. Se a corrente de fronteira for descartada, perde-se exatamente a contribuição que cancelaria a diferença entre as duas formas.

---

## 6. Controle racional esparso e recuperação de \(Q=0\)

**Controle:** tome \(\chi(x)=1\) (constante, logo momento de \(\chi\) é \(0\), ou seja \(Q=0\)). Então \(\partial_\mu\chi=0\). O termo de volume após IBP é zero. A ação de divergência é inteiramente a corrente de fronteira:
\[
S_{\rm div}\big|_{\chi=1}
=
-\frac{1}{2\kappa}\oint B^\mu n_\mu .
\]
Escolha \(h\) tal que \(B^\mu_4 n_\mu\neq 0\) na fronteira. Por exemplo, um perfil \(h\) de grau 4 com suporte até a fronteira e derivadas não nulas ali. Então \(S_{\rm div}\neq 0\). Se ignorarmos a corrente de fronteira, obtemos \(S_{\rm div}=0\), o que é falso. A Hessiana contraída correta é dada pela corrente de fronteira:
\[
H_{\rm div}(A,B)\big|_{Q=0}
=
-\frac{1}{2\kappa}\oint
\left[\frac{\delta^4 B^\mu}{\delta h_A\delta h_B\delta h_U\delta h_V}\right]n_\mu\,W(U,V).
\]
Isso recupera o caso \(Q=0\): o volume se anula, e a corrente de fronteira carrega toda a contribuição. Note que \(Q=0\) não implica \(r=s=0\); a corrente de fronteira ainda pode depender de \(r,s\), mas não gera jatos de segunda ordem em \(W\) porque não há \(Q_\mu\) se decompondo em \(r+s\).

---

## 7. Auditoria de sinais, fatorial e normalização

**Sinal.** A identidade é
\[
-\chi\,\partial_\mu B^\mu
=
(\partial_\mu\chi)B^\mu
-
\partial_\mu(\chi B^\mu).
\]
Em Fourier, \(\partial_\mu\chi\to -iQ_\mu\chi\). O termo original dá
\(-\frac{1}{2\kappa}\chi\,(iQ_\mu B^\mu)=-\frac{i}{2\kappa}Q_\mu\chi B^\mu\).
O termo de volume após IBP dá
\(+\frac{1}{2\kappa}(-iQ_\mu\chi)B^\mu=-\frac{i}{2\kappa}Q_\mu\chi B^\mu\).
Os sinais coincidem; a diferença é exatamente a derivada total de fronteira.

**Fatorial.** A quarta derivada funcional inclui \(4!\). O motor `metric_quartic_vertices.py` explicitamente não divide por \(4!\). Assim, ao contrair \(U,V\) com \(W\), o fator \(4!\) deve ser mantido ou rastreado até a normalização final. Se \(V_{4{\rm raw}}=32\kappa S_4\), então \(S_4=V_{4{\rm raw}}/(32\kappa)\). A contribuição do termo de divergência para \(S_4\) é \(-\frac{1}{2\kappa}\chi\partial B_4\). Logo
\[
V_{4{\rm raw}}^{\rm div}
=
32\kappa\left(-\frac{1}{2\kappa}\chi\partial B_4\right)
=
-16\,\chi\,\partial B_4.
\]
Portanto, a parte de divergência do vértice quártico é \(-16\chi\partial B_4\). A Hessiana contraída é obtida contraindo \(U,V\) com \(W\):
\[
H_{\rm div}
=
-16\,\chi\,\langle \partial B_4, W\rangle.
\]
O fator relativo \(V_{4{\rm raw}}/16\) surge de \(32\kappa/(2\kappa)=16\). Se o vértice total é normalizado como \(V_{4{\rm raw}}/16\), então a contribuição de divergência é essa mesma normalização multiplicada pela contração de \(\partial B_4\) com \(W\). Não identifiquei o tadpole com a soma de dois vértices; a normalização \(T1\) não foi alterada.

---

## 8. O que não se conclui

- Esta derivação **não** computa a integral \(Q2\).
- Ela **não** afirma que exatidão livre \(s0\) resolve a anomalia não linear.
- Ela **não** usa resultados numéricos do operador.
- Ela **não** modificou normalização \(T1\), gate, kernel, estado ou prescrição.
- A recuperação de \(Q=0\) é estrutural: o volume se anula e a corrente de fronteira carrega o resultado. A implementação numérica da corrente de fronteira com \(Q=0\) depende do perfil de \(h\) e da fronteira adotada; isso permanece como pendência de verificação local contra os motores anexos.

**Resumo em uma frase:** antes de IBP, a contribuição do termo de divergência à Hessiana contraída exige jatos de \(W\) até segunda ordem, com partição em graus \(0,1,2\) em \(r,s\) incluindo \(r^2,s^2\); depois de IBP contra \(\chi\), o termo de volume exige apenas jatos de primeira ordem, graus \(0,1\), e a diferença é a corrente de fronteira, que é essencial — para \(\chi\) constante (\(Q=0\)) ela é o resultado inteiro.