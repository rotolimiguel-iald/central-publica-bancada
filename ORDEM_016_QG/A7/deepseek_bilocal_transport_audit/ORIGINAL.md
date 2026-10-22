**A7.b — revisão crítica do transporte bilocal com extensão radial**  
**Estatuto: DECLARADO até auditoria local.** Não há nova execução externa; o modelo finito e eventual CAS servem apenas como controle de sinal/álgebra, não como prova distribucional.

## 1. Definições na convenção dada

\[
t=i\hbar,\qquad E_H=e^{tB_H}=e^{t(B_F-B_W)},\qquad B_H=B_F-B_W .
\]

\[
Q_W:=q+tR_{W,\rm total}=q+i\hbar\,[q,C_x+C_y+B_W],
\]
\[
Q_{\rm in}:=q+tR_x+tR_y=q+i\hbar([q,C_x]+[q,C_y]).
\]

O contato temporal composto, antes da multiplicação \(m\), é

\[
C:=E_H[q,B_F].
\]

## 2. A identidade pré-\(m\) está correta sob as hipóteses nomeadas

No produto tensorial graduado, antes de multiplicar os campos,

\[
Q_W E_H-E_H Q_{\rm in}
=
tE_H\bigl([q,B_H]+[q,B_W]\bigr).
\]

Como \(B_H=B_F-B_W\),

\[
[q,B_H]+[q,B_W]=[q,B_F],
\]

logo

\[
\boxed{
Q_W E_H-E_H Q_{\rm in}
=
tE_H[q,B_F]
=
i\hbar\,E_H[q,B_F].
}
\]

Portanto, **sim**, a identidade transporta corretamente as duas correções \(A_1=t[q,C_x]\) e \(A_1=t[q,C_y]\). O termo espúrio dependente de \(W\), \(-[q,B_W]\), escondido em \(B_H=B_F-B_W\), é cancelado por \(+[q,B_W]\). Sem \(R_x\) ou sem \(R_y\), resta respectivamente

\[
tE_H R_x \quad\text{ou}\quad tE_H R_y,
\]

ambos não nulos no modelo finito. As duas entradas são necessárias.

**Precisão importante:** só a fonte \([q,B_F]\) perdeu \(W\). O fator \(E_H=e^{t(B_F-B_W)}\) **não** perdeu \(W\). Logo não se deve afirmar invariância total de \(A_2\).

## 3. Simetrização

Como

\[
S_2=\frac12\bigl(T_1(F)\star T_1(G)+T_1(G)\star T_1(F)\bigr),
\]

o representante \(A_2\) deve ser lido na parte simetrizada/antisimetrizada apropriada. Para \(F,G\) pares, a simetrização é a troca simples dos argumentos. Denote

\[
X_{\rm anti}(F,G)
=
\frac12\Bigl(
X(F,G)-(-1)^{|F||G|}X(G,F)
\Bigr).
\]

## 4. Representante antes da extensão radial

Na convenção dada,

\[
T_{c2}=\frac{i}{\hbar}(T_2-S_2)=-\frac1t(T_2-S_2).
\]

Assim o fator \(-1/t\) já está dentro de \(T_{c2}\). O transporte de Ward do contato temporal, antes de estender, dá

\[
\boxed{
T_1(A_2)_{\rm before}
=
-m\,C_{\rm anti}
-T_1((F,G))_{\rm sym}
}
\]

com

\[
C_{\rm anti}
=
\left(E_H[q,B_F]\right)_{\rm anti}.
\]

Se em vez disso se usa o objeto cru \(E_H\), sem absorver o \(1/t\), a forma equivalente é

\[
T_1(A_2)_{\rm raw}
=
t\,m\,C_{\rm anti}
-T_1((F,G))_{\rm sym}.
\]

Não misture as duas convenções: o \(t=i\hbar\) e o \(-1/t\) de \(T_{c2}\) não podem ser cancelados sem que o \(-1\) seja preservado.

## 5. Extensão radial \(\mathcal R\): transportar antes ou depois

Seja \(\mathcal R\) a extensão radial já fixada. Defina:

- **transportar antes de estender**:
\[
T_1(A_2)^{\rm before}_{\mathcal R}
=
-m\,\mathcal R(C_{\rm anti})
-T_1((F,G))_{\rm sym}.
\]

- **transportar depois de estender**:
\[
\boxed{
T_1(A_2)^{\rm after}_{\mathcal R}
=
-m\,\mathcal R(C_{\rm anti})
+
\frac{i}{\hbar}\,
m\,[Q_W,\mathcal R]\,E_{H,\rm anti}
-
T_1((F,G))_{\rm sym}.
}
\]

Portanto a diferença exata é

\[
\boxed{
\Delta_{\mathcal R}
=
T_1(A_2)^{\rm after}_{\mathcal R}
-
T_1(A_2)^{\rm before}_{\mathcal R}
=
\frac{i}{\hbar}\,
m\,[Q_W,\mathcal R]\,E_{H,\rm anti}.
}
\]

Aqui

\[
[Q_W,\mathcal R]
=
[q,\mathcal R]
+
i\hbar\,[R_{W,\rm total},\mathcal R].
\]

Se, e somente se, em um domínio declarado se demonstrar que esse comutador age como zero sobre \(E_{H,\rm anti}\), o termo de extensão desaparece. **Isso não está fixado pela identidade acima.** O modelo finito de controle não decide esse ponto distribucional.

## 6. O que já se compensa

Já se compensa exatamente:

\[
[q,B_H]+[q,B_W]=[q,B_F].
\]

Ou seja, a dependência explícita em \(W\) vinda do colamento \(B_H=B_F-B_W\) cancela contra a correção cruzada \(+[q,B_W]\). O que resta é o contato de Euler/Feynman \([q,B_F]\), ainda vestido por \(E_H=e^{t(B_F-B_W)}\).

Não se compensa automaticamente:

- o fator \(E_H\), que ainda depende de \(W\);
- o contato composto \(\delta\times\text{propagador}\) dentro de \([q,B_F]\);
- o comutador \([Q_W,\mathcal R]\), que mede a diferença entre estender antes ou depois do transporte de Ward.

## 7. Restrição de suavidade

A identidade

\[
Q_W E_H-E_H Q_{\rm in}=tE_H[q,B_F]
\]

é uma igualdade de operadores no produto tensorial graduado **antes da multiplicação \(m\)** e **onde todos os produtos estão definidos**. Ela é exata para kernels suaves \(W=G-H\) e contrações pares de segundo grau com coeficientes independentes dos campos.

Ela **não** é automaticamente uma igualdade distribucional para o contato composto quando \(B_F\) contém propagador singular. Nesse caso, produtos do tipo

\[
\delta(x-y)\,\Delta_F(x,y)
\]

ou derivados de delta multiplicando propagador precisam da mesma extensão radial \(\mathcal R\). O CAS finito não prova isso.

## 8. Dado mínimo ainda necessário

Se o \(\mathcal R\) ordinário não fixa o contato composto, falta pelo menos:

1. **A extensão do contato composto**  
   \[
   \mathcal R\!\left(E_H[q,B_F]\right)_{\rm anti},
   \]
   não apenas \(\mathcal R(z^{-n})\), mas a ação de \(\mathcal R\) sobre o produto delta–propagador e sobre as inserções de Euler.

2. **A avaliação de**  
   \[
   [Q_W,\mathcal R]\,E_{H,\rm anti},
   \]
   incluindo os símbolos \(q_i\) de derivada de delta, via
   \[
   \mathcal R D_w-D_w\mathcal R=CE\,C_w.
   \]
   Aqui \(q_i\) é símbolo de derivada de delta, não momento de Fourier.

3. **A subtração local**  
   \[
   T_1((F,G))_{\rm sym}
   \]
   na mesma convenção de sinal e simetrização.

O \(\tau\) da família \(f_a,g_a\) não deve ser escolhido para cancelar o contato. A soma \(3q^2/8\) com gradientes cruzados é apenas diagnóstico de Leibniz, não substitui a extensão do composto.

## 9. Conclusão A7.b

A identidade bilocal transporta corretamente as duas correções \(A_1\) para o contato temporal **no nível pré-multiplicação e antes da extensão distribucional**. O resultado exato que resta, na convenção dada, é

\[
\boxed{
T_1(A_2)^{\rm after}_{\mathcal R}
=
-m\,\mathcal R\!\left(E_H[q,B_F]\right)_{\rm anti}
+
\frac{i}{\hbar}\,m\,[Q_W,\mathcal R]\,E_{H,\rm anti}
-
T_1((F,G))_{\rm sym}.
}
\]

A primeira parcela é o contato composto estendido. A segunda é a diferença entre transportar antes e depois de estender. Se \([Q_W,\mathcal R]\) não estiver fixado pela extensão radial, esse é o dado mínimo pendente. Não se deve substituir o contato por zero nem declarar invariância total de \(A_2\).  
**Q2 permanece OPEN. Gate intocado.**