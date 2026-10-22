## Parecer técnico — ORDEM_016 A-7.b  
### Variação BRST localizada da primitiva de quarta ordem  
\[
B_\chi=-\frac{C_E}{2}\int \chi\, h\cdot N h
\]

**Estatuto:** derivação algébrica com os coeficientes lidos do artefato `bilocal_curved_contact_primitive/results.json`.  
**Não** afirmo execução de código, prova em kernel, medida nova ou QME completa.  
Os parâmetros \(b,c,t\) permanecem livres. \(K^2\), \(W\), aridades superiores e contratermos não são calculados aqui.

---

## 1. Convenções e operador \(N\)

Espaço-forma euclidiano auxiliar 4D, \(\nabla\) Levi-Civita, \(\chi\) de suporte compacto, \(h_{ab}=h_{ba}\).  
Escrevo
\[
N=N_4+K\,N_2,
\]
com \(N_4\) de ordem 4 e \(N_2\) de ordem 2 nas fontes. O adjunto formal \(N^*\) é definido por
\[
\int u\cdot Nv=\int (N^*u)\cdot v,
\]
sem termos de fronteira, usando \(\nabla_\mu\chi=\partial_\mu\chi\) e integração por partes.

Para um monomial
\[
T_{ab}{}^{cd}\nabla_{\mu_1}\cdots\nabla_{\mu_p}v_{cd},
\]
o adjunto é
\[
(-1)^p\,T_{cd}{}^{ab}\nabla_{\mu_p}\cdots\nabla_{\mu_1}u_{ab},
\]
**mais a troca de fibra** \((ab)\leftrightarrow(cd)\).  
Simetrizar as palavras de derivadas **não** garante automaticamente essa troca de fibra; ela precisa ser conferida termo a termo.

---

## 2. Cinco tensores de ordem 4

Defina \(\Delta=\nabla^i\nabla_i\) e \(\operatorname{tr}h=h^i{}_i\). Os cinco blocos são:

\[
(O_1h)_{ab}=c_1\,\Delta^2 h_{ab},
\]
\[
(O_2h)_{ab}=c_2\,\delta_{ab}\,\Delta^2\operatorname{tr}h,
\]
\[
(O_3h)_{ab}=c_3\Big(
\nabla_a\nabla_b\Delta\operatorname{tr}h
+\delta_{ab}\nabla^c\nabla^d\Delta h_{cd}
\Big),
\]
\[
(O_4h)_{ab}=\frac{c_4}{2}\Big(
\nabla_a\nabla^i\Delta h_{ib}
+\nabla_b\nabla^i\Delta h_{ia}
\Big),
\]
\[
(O_5h)_{ab}=c_5\,\nabla_a\nabla_b\nabla^i\nabla^j h_{ij}.
\]

Logo
\[
N_4=\sum_{r=1}^5 O_r.
\]

### Coeficientes lidos do artefato

No modo `geodesic` e no modo `coordinate` os cinco de ordem 4 são os mesmos:

\[
c_1=\frac{99}{1280}-\frac{c}{2},\qquad
c_2=-b-\frac{139}{3840},\qquad
c_3=b,\qquad
c_4=c,\qquad
c_5=-b-\frac{c}{2}+\frac{217}{1920}.
\]

Aqui \(b,c\) são parâmetros livres, **não** escolhidos.

---

## 3. Quatro tensores de ordem 2

O bloco \(N_2\) apareceu como a parte \(K\cdot(\text{ordem }2)\). Os quatro blocos são:

\[
(K_1h)_{ab}=-d_1\,\Delta h_{ab},
\]
\[
(K_2h)_{ab}=-d_2\,\delta_{ab}\,\Delta\operatorname{tr}h,
\]
\[
(K_3h)_{ab}=-d_3\Big(
\nabla_a\nabla_b\operatorname{tr}h
+\delta_{ab}\nabla^i\nabla^k h_{ik}
\Big),
\]
\[
(K_4h)_{ab}=-\frac{d_4}{2}\Big(
\nabla_a\nabla^i h_{ib}
+\nabla_b\nabla^i h_{ia}
\Big).
\]

Assim
\[
N_2=\sum_{s=1}^4 K_s.
\]

### Coeficientes lidos do artefato

Modo `geodesic`:

\[
d_1=-\frac{11b}{3}-\frac{7c}{6}-\frac{t}{2}+\frac{1277}{1152},
\]
\[
d_2=\frac{19b}{3}+\frac{c}{2}+\frac{t}{2}+\frac{883}{576},
\]
\[
d_3=-\frac{4b}{3}+\frac{c}{3}-\frac{t}{2}-\frac{401}{288},
\]
\[
d_4=t.
\]

Modo `coordinate`:

\[
d_1=-\frac{11b}{3}-\frac{7c}{6}-\frac{t}{2}+\frac{1181}{1152},
\]
\[
d_2=\frac{19b}{3}+\frac{c}{2}+\frac{t}{2}+\frac{785}{576},
\]
\[
d_3=-\frac{4b}{3}+\frac{c}{3}-\frac{t}{2}-\frac{43}{32},
\]
\[
d_4=t.
\]

---

## 4. Conferência da transposição de fibra

### Ordem 4

- \(O_1\): \((O_1h)_{ab}=c_1\Delta^2h_{ab}\).  
  Transposta: \(c_1\Delta^2h_{cd}\). É autoadjunto.

- \(O_2\): \((O_2h)_{ab}=c_2\delta_{ab}\Delta^2\operatorname{tr}h\).  
  Transposta: \(c_2\delta_{cd}\Delta^2\operatorname{tr}h\). Autoadjunto.

- \(O_3\): separe
  \[
  O_{3a}h=\nabla_a\nabla_b\Delta\operatorname{tr}h,\qquad
  O_{3b}h=\delta_{ab}\nabla^c\nabla^d\Delta h_{cd}.
  \]
  Então
  \[
  (O_{3a})^*=O_{3b},\qquad (O_{3b})^*=O_{3a}.
  \]
  Portanto \(O_3=O_{3a}+O_{3b}\) só é autoadjunto se ambos tiverem **o mesmo** coeficiente \(c_3\). No ansatz do artefato, ambos têm \(c_3=b\). Se um tivesse coeficiente diferente, \(N\neq N^*\), ainda que as palavras de derivadas estejam simetrizadas.

- \(O_4\): os dois termos são transpostos um do outro por integração por partes e pela simetria \(h_{ab}=h_{ba}\). Com o mesmo \(c_4\), é autoadjunto.

- \(O_5\): \((O_5h)_{ab}=c_5\nabla_a\nabla_b\nabla^i\nabla^j h_{ij}\).  
  A transposta devolve \(c_5\nabla^i\nabla^j\nabla_c\nabla_d h_{ij}\); pela simetria do par \(cd\) e pela comutatividade das derivadas na forma simetrizada, é autoadjunto.

### Ordem 2

- \(K_1\): autoadjunto.
- \(K_2\): autoadjunto.
- \(K_3\): separe
  \[
  K_{3a}h=-\nabla_a\nabla_b\operatorname{tr}h,\qquad
  K_{3b}h=-\delta_{ab}\nabla^i\nabla^k h_{ik}.
  \]
  Vale \((K_{3a})^*=K_{3b}\) e \((K_{3b})^*=K_{3a}\). Logo exigem o mesmo \(d_3\). No artefato, ambos têm \(d_3\).
- \(K_4\): autoadjunto com o mesmo \(d_4\).

**Conclusão:** no ansatz fornecido, \(N=N^*\), porque \(c_3\) e \(d_3\) são coeficientes únicos para os pares transpostos. Mas a checagem é independente da simetrização das derivadas: se \(c_{3a}\neq c_{3b}\) ou \(d_{3a}\neq d_{3b}\), então \(N\neq N^*\).

---

## 5. Comutador \([N,\chi]\)

Para um monomial
\[
D=\nabla_{\mu_1}\cdots\nabla_{\mu_p},\qquad p\le 4,
\]
vale
\[
[D,\chi]h=
\sum_{\varnothing\neq S\subseteq\{1,\dots,p\}}
\left(\prod_{i\in S}\nabla_{\mu_i}\chi\right)
\left(\prod_{j\notin S}\nabla_{\mu_j}h\right),
\]
mantendo a ordem original das palavras. As derivadas em \(h\) carregam a conexão de Levi-Civita nos índices derivados. Como \(\chi\) é escalar, \(\nabla_\mu\chi=\partial_\mu\chi\).

Portanto \([N,\chi]\) contém termos com 1, 2, 3 e 4 derivadas de \(\chi\). Para \(N=N^*\),
\[
[N,\chi]^*=[\chi,N]=-[N,\chi]:
\]
logo \(h\cdot[N,\chi]h=0\) na forma quadrática real.

### Fator \(1/2\)

Como
\[
B_\chi=-\frac{C_E}{2}\int \chi\,h\cdot Nh,
\]
temos
\[
s_0B_\chi
=-\frac{C_E}{2}\int \chi\big((s_0h)\cdot Nh+h\cdot N(s_0h)\big).
\]
Com \(N=N^*\),
\[
h\cdot N(s_0h)=(s_0h)\cdot Nh.
\]
Logo
\[
s_0B_\chi
=-C_E\int \chi\,(s_0h)\cdot Nh.
\]
O fator \(1/2\) é cancelado pela duplicação simétrica. O termo de comutador \(h\cdot[N,\chi]h\) é nulo, então não altera esse cancelamento.

---

## 6. \(s_0B_\chi\) e \(s_1B_\chi\)

Com
\[
s_0h=Gc,\qquad s_1h=\operatorname{Lie}_c h,\qquad s\chi=0,
\]
obtém-se
\[
s_0B_\chi=-C_E\int \chi\,(Gc)\cdot Nh,
\]
\[
s_1B_\chi=-C_E\int \chi\,(\operatorname{Lie}_c h)\cdot Nh.
\]

Escreva \(\chi=1-(1-\chi)\). Então
\[
s_0B_\chi
=-C_E\int (Gc)\cdot Nh
+C_E\int (1-\chi)(Gc)\cdot Nh.
\]
O primeiro termo é \(-A_{hc}\), com
\[
A_{hc}=C_E\int (Gc)\cdot Nh.
\]
O segundo termo é suportado onde \(\chi\neq1\), isto é, **fora da região \(\chi=1\)**. Se o expandirmos via \([N,1-\chi]\), aparecem exatamente as derivadas \(\nabla^k\chi\), \(k=1,\dots,4\), todas suportadas fora de \(\chi=1\). No interior \(\chi=1\), elas somem; logo a variação lá é exatamente \(-A_{hc}\). O mesmo vale para \(s_1B_\chi\).

---

## 7. Controle 1D: \(N=d^4\)

Em 1D,
\[
N=\frac{d^4}{dx^4},\qquad N^*=N.
\]
O comutador é a regra de Leibniz:
\[
[d^4,\chi]
=4\chi' d^3+6\chi''d^2+4\chi'''d+\chi''''.
\]
A variação é
\[
s_0B_\chi
=-\frac{C_E}{2}\int \chi\big((s_0h)h''''+h(s_0h)''''\big).
\]
Integrando por partes duas vezes,
\[
\int \chi\,h(s_0h)''''=\int \chi\,(s_0h)h''''.
\]
Logo
\[
s_0B_\chi=-C_E\int \chi\,(s_0h)h''''.
\]
O fator \(1/2\) está correto.

---

## 8. Controle tensorial misto não diagonal

Tome \(O_4\) em 2D e \(h_{01}=h_{10}=1\), demais componentes nulas. O termo
\[
\int h^{ab}\nabla_a\nabla^i\Delta h_{ib}
\]
vira, por integração por partes,
\[
\int h_{ib}\nabla_a\nabla^i\Delta h^{ab}
=\int h_{cd}\nabla_a\nabla^c\Delta h^{ad}.
\]
Isso é exatamente a transposta do outro termo de \(O_4\). O par fecha.

Contraexemplo para a advertência: se em \(O_3\) tomarmos apenas
\[
O_{3a}h=\nabla_a\nabla_b\Delta\operatorname{tr}h
\]
com coeficiente \(1\) e \(O_{3b}=0\), a forma quadrática ainda é simétrica,
\[
h\cdot O_{3a}h=h\cdot O_{3b}h
\]
por integração por partes, mas o **operador** não é autoadjunto: \((O_{3a})^*=O_{3b}\).  
Portanto simetrizar derivadas não basta; a transposição de fibra é uma condição separada.

---

## 9. Ordem seguinte sem afirmar \(B_3\)

Dado
\[
A_1=-s_0B,\qquad s_0A_2+s_1A_1=0,
\]
defina
\[
C=A_1+A_2+s_1B.
\]
Então
\[
s_0C
=s_0A_1+s_0A_2+s_0s_1B
=0-s_1A_1-s_1s_0B.
\]
Como \(s_0B=-A_1\),
\[
s_0C=-s_1A_1+s_1A_1=0.
\]
Logo \(C\) é \(s_0\)-fechado na ordem seguinte. Isso **não** afirma existência de \(B_3\) nem conhece \(A_2\) explicitamente; usa apenas a equação de descida. \(A_2\) é definido a menos de termo \(s_0\)-fechado, então a classe de \(C\) é bem-definida. Não se infere a QME completa dessa identidade.

---

## 10. Pseudocódigo auditável

```text
Entrada: h, chi, K, coeficientes c1..c5, d1..d4, derivada covariante D.

1. Construir N:
   N = c1*O1 + c2*O2 + c3*O3 + c4*O4 + c5*O5
       + K*(d1*K1 + d2*K2 + d3*K3 + d4*K4)

2. Construir N*:
   Para cada monomial T_{ab}^{cd} D_{mu1}...D_{mup} v_{cd}:
       N* += (-1)^p T_{cd}^{ab} D_{mup}...D_{mu1} u_{ab}
   Conferir termo a termo a troca (ab)<->(cd).

3. Verificar N - N* == 0.
   Se falhar, reportar pares c3a vs c3b, d3a vs d3b.

4. Construir [N,chi]:
   [N,chi]h = N(chi*h) - chi*(N*h)
   Expandir por Leibniz sobre cada palavra de derivadas.
   Manter a ordem dos índices e a conexão em h.

5. Conferir fator 1/2:
   s0B = -C_E/2 * ( <s0h,Nh> + <h,N s0h> )
   Se N=N*, verificar s0B = -C_E * <chi*s0h,Nh>.

6. Controle 1D:
   N = d^4
   Verificar [d^4,chi] = 4 chi' d^3 + 6 chi'' d^2 + 4 chi''' d + chi''''.

7. Controle misto:
   h_01 = h_10 = 1
   Calcular <h,O4h> e <h,O4*h>;
   verificar igualdade por integração por partes.

8. Ordem seguinte:
   Dado A1 = -s0B e s0A2 + s1A1 = 0,
   retornar C = A1 + A2 + s1B;
   verificar s0C == 0.
```

---

## 11. Lacunas declaradas

- \(b,c,t\) permanecem livres; nada foi ajustado.
- \(W\) suave, \(K^2\) e aridades superiores não foram calculados nesta unidade.
- A identificação do contato medido e a Q2 completa não são resolvidas por esta derivação.
- Não se afirma \(B_3\), QME completa ou fechamento não linear/UV.
- Os coeficientes \(c_i,d_i\) foram lidos do artefato indicado; não foram reextraídos nem reexecutados.
- Estatuto dos resultados: **DECLARADO** até auditoria da bancada.