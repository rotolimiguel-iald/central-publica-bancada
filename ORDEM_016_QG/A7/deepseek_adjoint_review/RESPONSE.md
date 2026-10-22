**ESTATUTO: DECLARADO.**  
Auditoria textual dos anexos fornecidos, sem execução de código, sem alteração de kernel, gate, originais ou prescrição. Os scripts são tratados como candidatos; não os tomo como teoremas nem como resultados verificados. A resposta abaixo não move o gate nem infere anomalia, nulidade de Q2 ou quebra de Ward a partir deste componente isolado.

---

## 1. Veredito curto

O motor anexo **não calcula o funcional completo da fonte singular avaliada em \(E(T)\) para a identidade de Ward bilocal**. Até primeira \(K\), ele calcula, no máximo, o **símbolo local de bulk** desse funcional, com o ghost fixado em \(Y=0\), assumindo (i) auto-adjunção formal de \(E\) com testes compactos, (ii) remoção implícita do corte compacto, e (iii) ausência de derivadas em \(Y\). O alcance é de um **contato local \(Y=0\)**, não da identidade bilocal completa.

A parte algébrica do operador Einstein, do levantamento de índices e do fator \(\sqrt g\) em `density` parece estruturalmente correta até primeira \(K\), na convenção em que a curvatura do espaço-forma auxiliar é marcada por `L` no kernel e por coeficiente 1 no operador de teste. O que falta é o que a própria pergunta exige separar: auto-adjunção com termos de fronteira, comutação com \(R\), remoção do cutoff, ancoragem em \(Y\) e derivadas \(Y\) adicionais.

---

## 2. O que a implementação realmente paga

### 2.1 Operador Einstein local

Em `einstein_test_field_engine.py`, as peças implementadas são:

- `gamma(c,a,b)` = símbolo de Christoffel em RNC até primeira \(K\);
- `derivative(f,i,q)` = \(\partial_i + q_i\) para o coeficiente do campo \(\exp(q\cdot x)\);
- `gradient_tensor` = derivada covariante de tensor covariante, com termos de conexão contra a ordem plana;
- `C = div h - grad(tr h)/2`;
- `GC = 2\nabla_{(a} C_{b)}\);
- `divC = \nabla^a C_a\);
- `boxes` = \(\Box h_{ab}\) covariante até primeira \(K\);
- `trace` = \(g^{ab}h_{ab}\) até primeira \(K\);
- montagem final:
  \[
  E = -\Box\,\mathrm{Itr} + \mathrm{Itr}\,GC + 2K\,h + K\,g\,\mathrm{tr}\,h,
  \qquad
  \mathrm{Itr}=h-\frac12 g\,\mathrm{tr}\,h.
  \]

Essa montagem corresponde à linearização do tensor de Einstein a menos de fator global, com os termos \(2K h\) e \(K g\,\mathrm{tr}\,h\) entrando na ordem correta. Em particular, para \(h=h_0+K h_1\), o código separa `[E0,E1]` de modo compatível com:

\[
E(h)=E^{(0)}(h_0)+K\bigl[E^{(1)}(h_0,h_1)\bigr]+O(K^2).
\]

### 2.2 `density`

`density(h)` implementa, para tensor covariante \(h_{ab}\),

\[
h_{ab}\mapsto \sqrt g\,g^{ac}g^{bd}h_{cd}
\]

até primeira \(K\). No espaço-forma auxiliar, \(\mathrm{tr}\,h=-z+O(K^2)\) e \(\sqrt g=1-z/2+O(K^2)\), de modo que a expressão

```python
h[1] + inv1*h[0] + h[0]*inv1 - Z*h[0]/2
```

é a expansão correta de \(\sqrt g\,g^{ac}g^{bd}h_{cd}\) até primeira \(K\), com `inv1` representando \(g^{ab}-\delta^{ab}\). Aqui não vejo erro algébrico local.

### 2.3 Composição com `kernel(T,v,p,order)`

`source_adjoint` faz:

```python
test = density(einstein(parallel_tensor(T), -i p))
A,B = kernel(test[order-r], v, p, r)
result = fourier(A,p)/i + fourier(B,p)
```

A composição paga:

- aplicação de \(E\) ao teste \(T(x)\exp(-ip\cdot x)\);
- levantamento dos dois índices e inclusão de \(\sqrt g\);
- convolução formal com o vértice implementado por `kernel`;
- Fourier com fase \(\exp(-ip\cdot X)\);
- ghost fixado em \(Y=0\), conforme a docstring de `kernel`.

O `assert` de parte imaginária nula após `FL -> realLog` é um controle de consistência da convenção de fase, não uma prova de auto-adjunção nem da identidade de Ward.

---

## 3. O que a implementação NÃO paga

### 3.1 Auto-adjunção formal

A docstring de `einstein_source_adjoint_engine.py` diz:

> “Uses formal self-adjointness of E with compact test support.”

Mas o código **não deriva** essa auto-adjunção, **não calcula os termos de fronteira** e **não verifica** se os contatos de corte são nulos. A passagem para ondas planas e a remoção do corte compacto dependem exatamente disso. Portanto, o resultado é um símbolo de bulk, não o funcional completo com condições de contorno.

### 3.2 Controles ausentes

Não vejo no trecho anexo:

- controle \(E(Gv)=0\) para gauge \(h=Gv\);
- limite plano \(K\to 0\);
- controle curvo não axial;
- teste de independência do ponto-base;
- verificação de que a comutação \(E\leftrightarrow R\) é válida.

Esses controles são exigidos pela própria pergunta e não estão implementados no motor.

### 3.3 \(Y\) não é ancorado

`kernel` fixa o ghost em \(Y=0\). A identidade de Ward bilocal exige termos com derivadas em \(Y\). O motor paga apenas o contato local em \(Y=0\). Portanto, ele não pode detectar quebras que apareçam em \(\partial_Y\) ou em contatos bilocais fora de \(Y=0\).

### 3.4 Corte compacto

O motor calcula o símbolo de bulk. Ele não implementa a remoção explícita do corte compacto nem separa contatos de cutoff. A frase da docstring “does not discard cutoff contacts or smooth W globally” reconhece a pendência, mas não a resolve.

### 3.5 \(W\) suave

O setor suave \(W\) é excluído explicitamente. Isso é correto para o setor singular, mas significa que o resultado **não escolhe estado com \(W=0\)** e **não é o funcional completo da teoria**. Ele é apenas o setor singular até primeira \(K\).

### 3.6 Q2 e anomalia

Nada no trecho calcula o traço completo da identidade de Ward, o coeficiente \(Q_2\) ou uma anomalia. Este componente é local e truncado. **Não se pode inferir anomalia ou nulidade de \(Q_2\) a partir dele.**

---

## 4. Alcance para a identidade de Ward bilocal

A quantidade calculada é:

\[
\text{símbolo local de bulk, primeira }K,\text{ do funcional }
\langle c, E(T)\rangle
\]

com:

- \(T\) transporte radial de tensor constante;
- \(q=-ip\) no teste;
- ghost \(Y\) colapsado em \(Y=0\);
- Fourier \(\exp(-ipX)\);
- corte compacto removido formalmente, não verificado.

Ela serve como **certificado local de consistência** de que:

- \(E\) está corretamente linearizado até primeira \(K\);
- o levantamento de índices e o fator \(\sqrt g\) estão corretos nessa ordem;
- a composição com o vértice local `kernel` é algebraicamente coerente na convenção de Fourier adotada.

Ela **não serve** como prova da identidade de Ward bilocal completa, porque faltam:

1. auto-adjunção com termos de fronteira;
2. contatos e derivadas em \(Y\);
3. remoção/ancoragem do cutoff;
4. comutação com \(R\);
5. prova de que os contatos de \(Y=0\) esgotam a contribuição relevante.

---

## 5. Correções necessárias

1. **Explicitar a curvatura \(K\) no teste.** Se `metric1` e `parallel_tensor` são usados com coeficiente 1, declarar que \(K=1\) ou introduzir o símbolo `L` também no operador de teste. Caso contrário, a expansão pode misturar ordens.

2. **Implementar os controles formais antes de usar ondas planas:**
   - \(E(Gv)=0\) para \(v\) compacto;
   - limite \(K\to0\);
   - controle curvo não axial;
   - auto-adjunção:
     \[
     \int_{\mathcal D} h\cdot E(k)-E(h)\cdot k
     =
     \text{termos de fronteira},
     \]
     com os termos de fronteira explicitamente calculados.

3. **Ancorar \(Y\).** `kernel` deve receber \(Y\) e calcular derivadas em \(Y\), ou provar que os termos \(Y\neq0\) não contribuem para a quantidade desejada. Sem isso, o alcance é apenas \(Y=0\).

4. **Separar as etapas:**
   - aplicar \(E\) ao teste;
   - comutar \(E\) através de \(R\);
   - remover o corte compacto;
   - ancorar \(Y\).
   
   O código atual faz a primeira etapa e assume as outras.

5. **Não inferir anomalia ou \(Q_2\).** Este componente é local e truncado. Qualquer conclusão sobre a identidade bilocal completa exige os termos faltantes.

---

## 6. Controle falsificável proposto

Sem usar saída numérica esperada da bancada, proponho o seguinte controle:

1. Escolher \(v(x)\) compactamente suportado, com suporte longe da origem.
2. Definir \(h=Gv\) (gauge puro) em RNC até primeira \(K\).
3. Calcular \(E(h)\) pelo motor para \(K=0\) e para \(K\neq0\).
4. O resultado de volume deve ser nulo; eventuais termos não nulos devem ser explicitamente identificados como contatos de fronteira.
5. Repetir com uma perturbação não axial, por exemplo \(h_{12}=f(x)\) com \(f\) polinomial, e comparar o símbolo obtido com o cálculo independente do operador de Einstein linearizado em RNC.
6. Variar o corte compacto e verificar que, após subtração dos contatos declarados, o resultado é independente do corte.
7. Incluir dependência em \(Y\) e verificar que \(\partial_Y\) produz os contatos esperados da identidade de Ward bilocal.

**Critério de falha:** se \(E(Gv)\) não for nulo a menos de contatos declarados, ou se o limite \(K\to0\) não recuperar o operador plano, ou se o resultado depender do corte de modo não controlado, a implementação está incorreta ou incompleta.

---

## 7. Conclusão declarada

**DECLARADO:** até primeira \(K\), a parte local do operador Einstein e o `density` parecem corretos na inspeção algébrica. A composição com `kernel` calcula um símbolo de bulk com ghost em \(Y=0\). Isso **não é** o funcional completo da fonte singular para a identidade de Ward bilocal. O alcance é limitado a um contato local, assumindo auto-adjunção formal e corte removido. Faltam os controles \(E(Gv)=0\), limite plano, caso curvo não axial, comutação com \(R\), derivadas \(Y\) e remoção explícita do cutoff. Nada aqui autoriza inferir anomalia, quebra de Ward ou nulidade de \(Q_2\).