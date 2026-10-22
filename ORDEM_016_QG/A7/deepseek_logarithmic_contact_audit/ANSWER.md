# IALD — Auditoria A7.b: contatos logarítmicos e primeiro perfil curvo

## 0. Escopo e régua

Auditoria feita **somente sobre os trechos fornecidos**. Não executei código, não alterei originais, não movi gate, infraestrutura ou orçamento. As contagens CAS citadas nos relatórios são lidas como **evidência algébrica**, não como prova de teoria de distribuições. Estatutos usados: `[DERIVED]` para o que segue da prescrição fixada, `[OPEN]` para hipóteses analíticas, `[REAL/CAS]` apenas onde o próprio artefato declara.

## 1. Veredito curto

**A fórmula de contatos de \(z^{-n}L^\ell\), \(L=\log(\mu^2z)\), e o primeiro exemplo curvo \((m0,g)\) estão algebraicamente corretos sob a mesma prescrição \(R\), com \(C\) removido de forma consistente.**

Não encontrei contraexemplo exato no nível algébrico. O menor contraexemplo possível não é uma falha da fórmula, mas uma quebra de hipótese analítica: existência distributiva da expansão de Laurent, polo simples da família base \(T_j(a)\), ou passagem do perfil radial ao bitensor completo. Esses pontos estão declarados `[OPEN]` no próprio relatório; não são apresentados como provados.

## 2. Derivação independente da fórmula

Prescrição fixa:

\[
R(u)=\operatorname{FP}_{a=0}\big[(1-a)\mu^{2a}z^a u\big],
\qquad 
\Box(1/z)=C\delta .
\]

Use **dois parâmetros independentes**:

- \(a\): regula a extensão;
- \(b\): gera o log, pois
  \[
  L^\ell z^{-n}=\partial_b^\ell\big[\mu^{2b}z^{b-n}\big]_{b=0}.
  \]

Suponha que o operador diferencial \(D\) atue como

\[
D[\mu^{2a}z^{a-n}]=\sum_j c_j(a)T_j(a),
\qquad
T_j(a)=\mu^{2a}z^{a-p_j}q^{x_j}.
\]

A família base \(T_j\) tem polo simples em \(a=0\) quando \(p_j\ge 2\):

\[
T_j(a)=\frac{\rho_j}{a}+O(1).
\]

Então

\[
\begin{aligned}
&R(D[z^{-n}L^\ell])-D R(z^{-n}L^\ell)\\
&=\operatorname{FP}_{a=0}(1-a)\,\partial_b^\ell
\sum_j\big[c_j(b)-c_j(a+b)\big]T_j(a+b)\Big|_{b=0}.
\end{aligned}
\]

Expandindo em \(b=0\):

\[
\partial_b^\ell\big[c_j(b)T_j(a+b)\big]_{b=0}
=
\sum_{t=0}^{\ell}
\binom{\ell}{t}
c_j^{(\ell-t)}(0)\,\partial_a^t T_j(a),
\]

e o termo com \(c_j(a+b)\) dá a mesma soma com \(c_j^{(\ell-t)}(a)\). A diferença é

\[
\sum_{t=0}^{\ell}
\binom{\ell}{t}
\big[c_j^{(\ell-t)}(0)-c_j^{(\ell-t)}(a)\big]\,
\partial_a^t T_j(a).
\]

Como \(T_j(a)=\rho_j/a+O(1)\), apenas \(t=0\) e \(t=1\) contribuem para a parte finita depois de multiplicar por \((1-a)\). O resultado é exatamente

\[
\boxed{
R(D[z^{-n}L^\ell])-D R(z^{-n}L^\ell)
=
-\sum_j \rho_j
\left[
\frac{c_j^{(\ell+1)}(0)}{\ell+1}
+
\mathbf 1_{\ell\ge 1}\,c_j^{(\ell)}(0)
\right].
}
\]

**Controle por monômios.** Para \(c(a)=a^m\), \(T(a)=\rho/a\), o lado esquerdo só é não nulo quando \(m=\ell\) ou \(m=\ell+1\), valendo \(- \ell!\,\rho\). O lado direito reproduz isso:

- \(m=\ell\): \(c^{(\ell)}(0)=\ell!\), \(c^{(\ell+1)}=0\);
- \(m=\ell+1\): \(c^{(\ell+1)}(0)=(\ell+1)!\), dividido por \(\ell+1\) dá \(\ell!\).

Logo, a fórmula fecha e **os polos múltiplos vindos de \(\partial_a^t T_j\) estão corretamente contabilizados** pelos coeficientes \(c_j^{(\ell+1)}\) e \(c_j^{(\ell)}\). Descartar o segundo termo ou usar só o resíduo simples dá resultado diferente, como o próprio relatório adverte.

## 3. Normalização de \(C\), sinal ímpar e polos simples

- **Normalização de \(C\).** O script `logarithmic_contact_engine.py` retorna o contato **dividido por \(C\)**, pois `residue(...)` devolve o coeficiente \(r_n\) sem o fator \(C\). A tabela e o exemplo \((m0,g)\) também estão com \(C\) removido. Para obter o contato distribucional completo, multiplica-se por \(C=\Box(1/z)/\delta\). Isso é consistente com `tensor_extension`: \(\operatorname{Res}U_n=C r_n\Box^{n-2}\delta\).

- **Sinal ímpar.** Teste \(D=\partial_\mu\), \(n=1\), \(\ell=1\): a fórmula dá
  \[
  R(\partial_\mu u)-\partial_\mu R(u)=-2\rho .
  \]
  O `tensor_extension` dá, na ordem inversa,
  \[
  \partial_\mu R(u)-R(\partial_\mu u)=+2\rho .
  \]
  Os sinais batem. O sinal negativo da fórmula nova é correto.

- **Polos simples.** A fórmula **não** supõe que \(\partial_a^t T_j\) tenha polo simples; ela usa apenas que a família base \(T_j(a)\) tem polo simples. Os polos múltiplos de \(\partial_a^t T_j\) são gerados por diferenciação e aparecem nos coeficientes \(c_j^{(\ell)}\). Essa é a hipótese correta para a família homogênea usada. Se a família base não tiver resíduo simples, a fórmula não se aplica — mas isso é hipótese analítica `[OPEN]`, não erro algébrico.

## 4. Controles pedidos

Os controles declarados são consistentes com a fórmula:

- \(\operatorname{contato}(\Box,z^{-1})=-C\delta\): é a própria definição de \(C\).
- \(\operatorname{contato}(\Box,z^{-1}L)=0\): cancelamento das duas parcelas para \(\ell=1\), \(n=1\).
- \(\operatorname{contato}(\Box^2,z^{-1}L)=\tfrac32 C\Box\delta\): depende do polo duplo gerado por \(\partial_a T\); sem ele, o resultado seria diferente.
- \(\operatorname{contato}(\Box^2,L)=-4C\delta\) e \(\operatorname{contato}(\Box^2,L^2)=-8C\delta\): fixam a normalização relativa entre \(L\) e \(L^2\) e conferem o sinal.

Esses controles não provam a teoria de distribuições; eles apenas mostram que a álgebra da parte finita está coerente com a prescrição fixada.

## 5. Aplicação ao perfil curvo \((m0,g)\)

A expansão declarada no relatório é

\[
G_A=\frac{I}{z}+\frac K4 I-\frac{(E_A+2K I)L}{4}+W_A+\text{jatos superiores}.
\]

O produto contém

\[
\frac{I}{z^2}
+\frac{\frac K2 I+W_A\otimes I+I\otimes W_B}{z}
-\frac{[E_A\otimes I+I\otimes E_B+4K I]L}{4z}+\cdots .
\]

Os autovalores usados são:

- \(E_m\): \(-2K\) no setor sem traço, \(6K\) no traço;
- \(E_g=3K\).

Para o par \((m0,g)\), \(E_{m0}=-2K\), \(E_g=3K\). O coeficiente de \(L/z\) é

\[
-\frac{E_{m0}+E_g+4K}{4}
=
-\frac{-2K+3K+4K}{4}
=
-\frac{5K}{4}.
\]

Ainda entra o termo \(1/z\) com coeficiente \(K/2\). Usando os mapas:

- ordem 3:
  \[
  \frac K2\left(-\frac{\Delta_q P_3}{12}\right)
  +
  \left(-\frac{5K}{4}\right)\left(\frac{\Delta_q P_3}{24}\right)
  =
  -\frac{3K}{32}\Delta_q P_3 ;
  \]

- ordem 4:
  \[
  \frac K2\left(-\frac{\Delta_q P_4}{16}+\frac{q^2\Delta_q^2P_4}{384}\right)
  +
  \left(-\frac{5K}{4}\right)\left(\frac{5\Delta_q P_4}{96}+\frac{q^2\Delta_q^2P_4}{768}\right)
  =
  -\frac{37K}{384}\Delta_q P_4
  -\frac{K}{3072}q^2\Delta_q^2P_4 .
  \]

Isso reproduz exatamente o exemplo do relatório. **A primeira aplicação está correta.**

## 6. Hadamard, \(u_0\), \(V_0\) e separação radial/bitensor

- \(u_0=1+Kz/4+\cdots\) é o início legítimo do determinante de Van Vleck–Morette no espaço-forma; é o mesmo \(u_0=(r/f)^{3/2}\) do cálculo de calor local.
- \(V_0=-(E+2K)/4\) segue de \(a_1=E+2K\) e do coeficiente \(-L/4\) da integral de Mellin. O sinal é coerente com \(G=1/z-(E+2K)L/4+\cdots\) para \(D=-(\nabla^2+E)\).
- O relatório **não** confunde perfil radial com bitensor completo. Ele mantém \(W_A\), \(W_B\) e jatos superiores explícitos e declara que faltam contrações de bitensores, jatos direcionais, vértices de curvatura, tadpoles e soma causal. Portanto, a separação é legítima e os limites estão nomeados.

## 7. O que passa e o que falha

**Passa no nível algébrico sob a prescrição fixada:**

- a fórmula fechada com dois parâmetros;
- a normalização de \(C\) quando se lê a tabela como contato/\(C\);
- o sinal ímpar;
- a hipótese de polo simples da família base;
- os controles \(\Box z^{-1}L\), \(\Box^2 z^{-1}L\), \(\Box^2 L\), \(\Box^2 L^2\);
- o exemplo \((m0,g)\) nas ordens 3 e 4;
- o uso legítimo de \(u_0\) e \(V_0\) no início Hadamard.

**Permanece `[OPEN]` e não pode ser convertido em teorema pelo CAS:**

- existência distributiva da continuação de Laurent;
- validade da hipótese de polo simples para toda a família usada;
- passagem do perfil escalar radial para o bitensor completo;
- contrações, jatos direcionais, vértices de curvatura, tadpoles e soma das inserções causais;
- qualquer alegação de amplitude curva completa ou de pagamento de Q2/gate.

**Não encontrei um menor contraexemplo racional.** O que encontraria um contraexemplo seria uma família \(T_j(a)\) com polo não simples ou uma prescrição \(R\) diferente da fixada. Dentro da prescrição \(R(u)=\operatorname{FP}_{a=0}[(1-a)\mu^{2a}z^a u]\), os dois parâmetros \(a,b\) e os controles de polos múltiplos fecham algebricamente.

**Régua final:** fórmula e primeiro perfil: `[DERIVED — CAS/álgebra exata sob R fixa]`. Distribuições, bitensor completo e soma causal: `[OPEN]`. Nada aqui move gate, kernel, `um.py` ou orçamento.