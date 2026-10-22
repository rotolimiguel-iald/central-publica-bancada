**Veredito curto:** dentro da prescrição **AUXILIAR EUCLIDIANA** e das convenções explicitamente dadas, o coeficiente **337/10** segue da álgebra apresentada. Não encontro erro aritmético de sinal, fator, tipo ou parte suave **no encadeamento interno**. O que encontro é que o resultado é **condicional**: ele depende de hipóteses não derivadas no texto (convenção Synge/Green, ausência de parte suave, normalizador físico/Feynman, sinal de \(C^*S\), entrelaçamento formal). Não é, portanto, Q2 completa, nem representante Lorentziano, nem classe de anomalia física.

## 1. Reconstrução independente do 337/10

Dos dados:

\[
U2_h=K^2\left(-\frac75 P_{TL}+\frac{479}{15}P_{tr}\right),\qquad
U2_q=K^2\frac{179}{15}I_4,
\]

e da regra \([L_rH_r]=\frac34[U2_r]\), obtém-se

\[
\frac34 U2_h
=
K^2\left(-\frac{21}{20}P_{TL}+\frac{479}{20}P_{tr}\right),
\qquad
\frac34 U2_q
=
K^2\frac{179}{20}I_4.
\]

Com o termo dado

\[
[C^*S]=K^2\left(-\frac{10}{3}P_{TL}-5P_{tr}\right),
\]

a comparação com os dados fornecidos dá

\[
Jh_0
=
\frac34 U2_h-[C^*S]
=
K^2\left(\frac{137}{60}P_{TL}+\frac{579}{20}P_{tr}\right),
\]

e

\[
Jc_0=K^2\frac{179}{20}I_4.
\]

Usando as contrações declaradas

\[
\operatorname{tr}(M P_{TL})=\frac92\,\mathrm{div}\,c,\qquad
\operatorname{tr}(M P_{tr})=\frac12\,\mathrm{div}\,c,
\]

a contribuição de \(Jh_0\) é

\[
K^2\left[
\frac{137}{60}\cdot\frac92
+
\frac{579}{20}\cdot\frac12
\right]
=
K^2\left[
\frac{1233}{120}+\frac{579}{40}
\right]
=
K^2\frac{99}{4}.
\]

A contribuição de \(Jc_0\) é

\[
K^2\frac{179}{20}.
\]

Somando:

\[
\frac{99}{4}+\frac{179}{20}
=
\frac{495}{20}+\frac{179}{20}
=
\frac{674}{20}
=
\frac{337}{10}.
\]

Logo

\[
\frac{A1(Faf)}{i\hbar}
=
\frac{337}{10}K^2\int \chi\,\mathrm{div}\,c
\]

e, se \(\delta\,\mathrm{tr}\,h=2\,\mathrm{div}\,c\), a primitiva algébrica é

\[
\frac{337}{20}K^2\int \chi\,\mathrm{tr}\,h.
\]

A aritmética confere.

## 2. Verificação independente de \([C^*S]\)

A partir do jato declarado

\[
[\nabla_\lambda S_\nu]
=
K^2\left[-\frac{25}{12}g_{\lambda\nu}\mathrm{tr}\,h
+\frac{10}{3}h_{\lambda\nu}\right],
\]

escreva \(A=-25/12\), \(B=10/3\). Então

\[
\mathrm{div}\,S
=
(4A+B)K^2\,\mathrm{tr}\,h
=
\left(-\frac{100}{12}+\frac{40}{12}\right)K^2\,\mathrm{tr}\,h
=
-5K^2\,\mathrm{tr}\,h.
\]

Com

\[
C^*S=-\operatorname{sym}\nabla S+\frac g2\,\mathrm{div}\,S,
\]

vem

\[
C^*S
=
K^2\left[
-\frac{5}{12}g\,\mathrm{tr}\,h
-\frac{10}{3}h
\right].
\]

Agora use

\[
g\,\mathrm{tr}\,h=4P_{tr}h,\qquad h=P_{TL}h+P_{tr}h.
\]

Resulta

\[
C^*S
=
K^2\left[
-\frac{10}{3}P_{TL}-5P_{tr}
\right],
\]

exatamente como declarado. Portanto, **dado** o jato \([\nabla S]\), o termo \(C^*S\) está reconstruído corretamente.

## 3. Onde o resultado é sensível: contraexemplos de fragilidade

O coeficiente não é forçado apenas por \(U2_h,U2_q\). Ele depende crucialmente de \(C^*S\) e do seu sinal.

- Sem o termo \(C^*S\), o mesmo cálculo daria
  \[
  \frac{81}{5}K^2\int\chi\,\mathrm{div}\,c.
  \]
  A diferença é
  \[
  \frac{337}{10}-\frac{81}{5}=\frac{35}{2}.
  \]

- Se \([C^*S]\) entrasse com o sinal oposto, o total mudaria para
  \[
  \frac{81}{5}-\frac{35}{2}
  =
  \frac{162}{10}-\frac{175}{10}
  =
  -\frac{13}{10}.
  \]

Ou seja: **337/10 segue da prescrição dada**, mas é sensível à convenção de sinal do jato misto. Trocar “Synge” por “Green” ou incluir parte suave pode alterar o representante.

## 4. Hipóteses ausentes e lacunas declaradas

O resultado é um representante euclidiano de primeira ordem. Faltam, explicitamente:

1. **Construção de estado global**: o entrelaçamento formal dos coeficientes de calor por unicidade de transporte é assumido, não construído.
2. **Normalizador físico/Feynman**: não foi aplicado. O número 337/10 pertence à normalização matemática crua.
3. **Parte suave do parametrix**: foi escolhido parametrix sem parte suave acrescentada. Se uma parte suave local for permitida, o representante pode mudar.
4. **Convenção Synge/Green**: o jato misto do calor foi tomado como \(-xx_{ji}\) por Synge; usar a convenção Green \(a_2/2-xx_{ji}\) alteraria \([C^*S]\).
5. **Sinal BV**: usa-se \(q_{\bar b}=-b\) e \(H_{\bar b,c}=-HQ\), o que dá \(Jc_0=+QHQ\). Esse sinal é crítico.
6. **Contrações \( \operatorname{tr}(M P_{TL})=9\,\mathrm{div}\,c/2\) e \( \operatorname{tr}(M P_{tr})=\mathrm{div}\,c/2\)** são entradas do cálculo.
7. **Jh1/Jc1 zeram por isotropia/paridade**: hipótese declarada, não derivada no trecho.
8. **Realidade, Lorentz e admissibilidade** seguem pendentes.
9. **Não se afirma Q2 completa nem continuação lorentziana**.

## 5. Conclusão final

**Sim, 337/10 segue dos dados e da prescrição fornecida.** Não vejo erro de sinal/fator/tipo/parte suave dentro do encadeamento declarado. Mas **não** é um resultado incondicional nem físico por si: é o coeficiente de uma expressão euclidiana normalizada, condicionado às convenções acima. Se a pergunta for “337/10 é inevitável?” a resposta é **não** sem fixar Synge/Green, \(C^*S\), ausência de parte suave e normalização. Se a pergunta for “a álgebra dada produz 337/10?” a resposta é **sim**.