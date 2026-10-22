**ORDEM_016 A-7.b — auditoria independente delimitada**  
**Estatuto:** `[DECLARADO]` — derivação simbólica a partir das convenções fornecidas.  
**Régua:** R⁴ euclidiano; nenhuma continuação lorentziana implícita.  
**Ações externas:** nenhuma. Nenhum arquivo foi lido, alterado ou executado. Nenhum CAS foi executado; portanto não há hash, saída computacional ou verificação numérica nova nesta rodada.  
**Memória comum obrigatória:** preservada a distinção `REAL`, `DERIVED`, `POSTULATE`, `CONJECTURE`, `ONTO`, `KNOWN`, `OPEN`, `INPUT`, `DECLARADO`. `NOT_FALSIFIED ≠ CONFIRMED`.

---

## 0. Notação e premissas usadas

- \(X,Y\in\mathbb R^4\), \(x=X-Y\), \(z=x\cdot x\).
- \(D_i=\partial/\partial X_i\), \(Q_i=\partial/\partial x_i\).
- Marcadores: \(\chi_X=e^{\lambda\cdot X}\), \(\chi_Y=e^{\eta\cdot Y}\), \(L=\lambda+\eta\).
- \(h_{ij}=h_{ji}\) par; \(c_i\) ímpar; \(s_0h_{ij}=D_i c_j+D_j c_i\), \(s_0c=0\).
- \(P_{(ij),r}=R(F_{ij,r})+A_{ij,r}\).
- \(R=\mathrm{FP}[(1-a)\mu^{2a}z^a]\). Linear, par sob \(x\to -x\), comuta com multiplicadores lisos no domínio usado, **não** comuta em geral com derivadas.
- \(C_i(F)\equiv R(Q_iF)-Q_iR(F)\).
- \(A(q)\) é polinômio em derivadas de \(\delta\), não momento de Fourier. A tabela \(A\) já tem o deslocamento \(q\to q-\lambda\) aplicado. \(C_i(F)\) ainda não tem esse deslocamento.

O funcional é
\[
\mathcal F=\sum_{i\le j,r}\int d^4X\,d^4Y\;
\chi_X\chi_Y\,h_{ij}(X)c_r(Y)\,P_{(ij),r}(X-Y;\lambda,\eta).
\]

---

## 1. IBP em \(X\) na variação de \(h\)

Aplicando \(s_0\):
\[
s_0\mathcal F=\sum_{i\le j,r}\int \chi_X\chi_Y\,
(D_i c_j+D_j c_i)c_r\,P_{ij,r}.
\]
Integrando por partes em \(X\) (bordas no infinito omitidas):
\[
\boxed{
s_0\mathcal F=
-\sum_{i\le j,r}\int \chi_X\chi_Y
\Big[
c_j c_r(\lambda_i+Q_i)P_{ij,r}
+
c_i c_r(\lambda_j+Q_j)P_{ij,r}
\Big]
}
\]
com \(D_i\chi_X=\lambda_i\chi_X\), \(D_iP=Q_iP\).

---

## 2. Multiplicidade diagonal e fora da diagonal

- Para \(i=j\): \(s_0h_{ii}=2D_i c_i\). O termo diagonal carrega fator \(2\).
- Para \(i<j\): os dois termos \(D_i c_j\) e \(D_j c_i\) são mantidos separados. Não se iguala \(P_{ij,r}\) a \(P_{ji,r}\) antes da auditoria.
- A fórmula do passo 1 já é explícita nessa separação.

---

## 3. Contato adicional ao passar derivada através de \(R\)

Usando a definição fornecida:
\[
(\lambda_i+Q_i)R(F)
=
R((\lambda_i+Q_i)F)-C_i(F).
\]
Substituindo \(P=R(F)+A\):
\[
\boxed{
\begin{aligned}
s_0\mathcal F
=&-\sum_{i\le j,r}\int \chi_X\chi_Y
\Big\{
c_j c_r\big[
R((\lambda_i+Q_i)F_{ij,r})
-C_i(F_{ij,r})
+(\lambda_i+Q_i)A_{ij,r}
\big]\\
&\qquad\qquad
+
c_i c_r\big[
R((\lambda_j+Q_j)F_{ij,r})
-C_j(F_{ij,r})
+(\lambda_j+Q_j)A_{ij,r}
\big]
\Big\}.
\end{aligned}
}
\]
O termo \(C_i(F)\) é o contato que aparece porque \(R\) não comuta com \(Q_i\).

---

## 4. Deslocamento \(q\to q-\lambda\) ao mover \(\chi_X\)

Escrevendo \(X=Y+x\),
\[
\chi_X\chi_Y=e^{L\cdot Y}e^{\lambda\cdot x}.
\]
O operador \(A\) já está tabelado com \(q\to q-\lambda\). O mesmo deslocamento deve ser imposto a \(C_i(F)\) quando ele age sobre o ghost e o peso local. Denoto por
\[
[\cdots]_{q\to q-\lambda}
\]
o bracket local avaliado nessa convenção. O setor não local \(R((\lambda_i+Q_i)F)\) deve ser lido como operador de convolução com \(e^{\lambda\cdot x}\); seu resíduo não local é exatamente \(R((\lambda_i+Q_i)F)\).

---

## 5. Intercâmbio \(X\leftrightarrow Y\)

Na orientação trocada:
\[
\lambda\leftrightarrow\eta,\qquad x\to -x,\qquad Q_i\to -Q_i,
\]
e, como \(c\) é ímpar,
\[
c_j c_r\longmapsto -c_j c_r
\]
(equivalentemente, \(c_jc_r\to c_rc_j=-c_jc_r\)).
Como \(R\) é par sob \(x\to -x\),
\[
R(G(-x))=R(G)(-x).
\]
As duas orientações **não** são igualadas antes do cálculo. A troca de índices \(i\leftrightarrow j\) também não é imposta a \(P_{ij,r}\) ou \(F_{ij,r}\) sem hipótese adicional.

---

## 6. Média das duas orientações e adjunto com \(L=\lambda+\eta\)

A descida correta é a média das duas orientações:
\[
\boxed{
\delta_{\rm avg}\mathcal F
=
\frac12\left(
\delta_{\lambda,\eta}\mathcal F
+
\delta_{\eta,\lambda}^{\dagger}\mathcal F
\right)
}
\]
onde \(\dagger\) inclui a transposição de ghosts e \(x\to -x\).

No setor não local, a soma das derivadas
\[
(\lambda_i+Q_i)\quad\text{e}\quad(\eta_i-Q_i)
\]
produz
\[
(\lambda_i+\eta_i)=L_i.
\]
Assim o resíduo não local médio é
\[
\boxed{
\mathcal N_{\rm nl}
=
\sum_{i\le j,r}\int dY\,e^{L\cdot Y}
\Big[
c_j c_r\,L_i R(F_{ij,r})
+
c_i c_r\,L_j R(F_{ij,r})
\Big]
}
\]
a menos de sinal global e fator \(1/2\) herdados da média. O setor local médio é
\[
\boxed{
\mathcal L_{\rm loc}
=
-\sum_{i\le j,r}\int dY\,e^{L\cdot Y}
\Big\{
c_j c_r
\big[
-C_i(F_{ij,r})+L_i A_{ij,r}
\big]_{q\to q-\lambda}
+
c_i c_r
\big[
-C_j(F_{ij,r})+L_j A_{ij,r}
\big]_{q\to q-\eta}
\Big\}
+\text{transposto}.
}
\]
Os coeficientes não são escolhidos: \(-1\) vem do IBP, \(1/2\) da média, \(L\) da soma \(\lambda+\eta\), e \(C_i\) da definição fornecida.

---

## 7. Condição exata no núcleo não local

Para eliminar a parte \(R(F)\) da descida média, deve valer
\[
\boxed{
L_i R(F_{ij,r})=0
\quad\text{e}\quad
L_j R(F_{ij,r})=0
\qquad
\forall\, i\le j,\ r.
}
\]
Como \(R\) comuta com derivadas constantes e é injetora no setor racional fora da diagonal, isso equivale à condição sobre o núcleo não local \(F\):
\[
\boxed{
L^\mu \partial_{x^\mu} F_{ij,r}(x;\lambda,\eta)=0
}
\]
no suporte fora da diagonal. Em linguagem de Fourier:
\[
\boxed{
\tilde F_{ij,r}(k;\lambda,\eta)\ \text{só pode ter suporte em}\ L\cdot k=0.
}
\]
Ou seja: o núcleo não local precisa ser **invariante ao longo de \(L=\lambda+\eta\)**. Se \(L=0\), a condição é vazia e a eliminação exigiria uma identidade de Ward adicional.

---

## 8. Controle escalar com \(L\neq0\)

Toy unidimensional: \(x\in\mathbb R\), \(\lambda=1,\ \eta=0\Rightarrow L=1\), \(A=0\).

- Se \(F(x)=e^{ix}\), então
  \[
  L\partial_x F=i e^{ix}\neq0.
  \]
  O resíduo não local é \(\propto i R(e^{ix})\), que não é polinômio local em \(\partial_x\delta\). Trocar \(L\to -L\) (por exemplo \(\lambda=0,\ \eta=-1\)) inverte o sinal do resíduo. Isso distingue a dependência correta em \(L\).

- Se \(F(x)=1\), então
  \[
  L\partial_x F=0.
  \]
  O resíduo não local desaparece e a descida se reduz ao contato local de \(A\) e \(C_i\). Isso mostra que a condição é \(L\partial_x F=0\), não \(F=0\).

---

## 9. Contraexemplo que detecta usar somente a variação de \(A\)

Tome
\[
A=0,\qquad F(x)=e^{ix},\qquad L\neq0.
\]
A descida correta contém o termo não local
\[
L_i R(F)\neq0.
\]
Um cálculo que ignore \(F\) e use apenas a variação de \(A\) daria zero e concluiria falsamente que a descida é local. Portanto, esse é o teste que detecta o erro de zerar \(R(F)\) sem verificar a condição \(L^\mu\partial_{x^\mu}F=0\).

---

## 10. O que uma coincidência com a variação de um contato \(hc\) demonstra — e o que NÃO identifica

Se a descida média coincidir com a variação BRST de um contato local \(hc\), módulo derivadas totais, isso demonstra que:
\[
\delta_{\rm BRST}\mathcal F
=
\delta_{\rm BRST}(\text{contato }hc)+\text{local},
\]
isto é, o núcleo bilocal é BRST-trivial no complexo local nesta ordem. Não gera nova obstrução local.

**O que isso NÃO identifica:**
- não identifica a anomalia bilinear \(a_2(I_1,V_1)\);
- não identifica a inserção efetiva \(J_2\);
- não identifica a classe de cohomologia.

Para isso seria necessário calcular o polinômio de anomalia completo, incluindo \(a_1\) — **não supor \(a_1=0\)** — e verificar a cohomologia de BRST no setor relevante. A coincidência só fixa o representante módulo termos exatos; a classe pode permanecer não nula se o contato \(hc\) não for fechado ou se houver outras contribuições.

---

## 11. Lacunas declaradas

1. A tabela explícita de \(A(q-\lambda)\) não foi lida além do trecho fornecido.
2. O sinal global e os fatores de \(1/2\) foram derivados das convenções, mas **não** verificados por CAS nesta rodada.
3. Nenhuma afirmação sobre \(a_2\), \(J_2\) ou classe de cohomologia é feita.
4. R⁴ euclidiano; nenhuma continuação lorentziana.
5. Se a condição \(L^\mu\partial_{x^\mu}F=0\) não for satisfeita, a descida **não** pode ser representada apenas por polinômio local em derivadas de \(\delta\).

**Veredito da rodada:** `DECLARADO` — fórmula auditável entregue; condição não local isolada; controle escalar e contraexemplo especificados. Nenhuma execução, hash, medida ou prova nova foi alegada.