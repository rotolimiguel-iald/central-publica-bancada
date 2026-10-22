# ORDEM_016 A-7.b — Completude do primeiro jato externo X: extensão (h_X, D_X h_X) e base mínima de verificação

**Estatuto desta entrega.** Demonstração escrita e especificação textual. **Nada foi executado, compilado ou medido nesta chamada**; nenhum código, kernel, gate ou prescrição foi alterado — tudo aqui é *ao lado*. Onde algo depende de uma convenção interna dos motores que não pude fixar só pela leitura, o ponto está **nomeado como verificação**, não como conclusão. Resultado final: **[DECLARADO]**, até revisão local independente.

Escopo respeitado: completo **apenas** o domínio do primeiro jato externo em **X**; não repito o pedido de divergência-Y nem a auditoria da fonte adjunta; **não** somo fonte Einstein nem contatos; **não** infiro Q2 completo de coeficientes fora da diagonal; o termo suave de Hadamard **W** não aparece nos kernels singulares, e isso **não** autoriza W = 0 (seleção de estado segue INPUT/aberta).

---

## 1. Leitura do estado atual (o que o anexo faz, e onde ele para)

- `ghost_ward_point(point, T)`: `T` é o jato de teste em X — hoje **10 números** (as componentes simétricas de `h_AB(X)` no frame local, via `tensor(a,b)`/`LABELS`). O vértice usado é `AX = G.vertex(T)[0]`, a peça com **duas pernas internas derivadas** (W2). É exatamente a imposição declarada no pedido: `D h_X = 0`.
- `metric_ward_point(point, T)`: `AX = [W2(h), −potential(h)]` — o potencial é a peça **O(K)** (vem das segundas derivadas do jato, fixadas pela condição de espaço-forma `Ric = 3Kg`).
- As palavras de derivada (`word`) agem **só em Y** (`J.matrix`, `Bval`, `d2vertex`), até ordem 2 — o Ward integrado em Y. O segundo extremo entra por `k_ab = D_a c_b + D_b c_a` (`Bval`/`BY`).
- `coord(...)` separa as potências de `L = log` por `coeff(B.L, k)`, k ∈ {0,1}, e o `assert s.diff(f,B.L,2)==0` é o **controle de truncamento** em L já existente.

A forma geral declarada no pedido — `V(h, Dh) = V0(h) + Σ_A V1_A(D_A h)`, com no máximo um jato externo por extremo — é o que o domínio atual não cobre: `V0(h)` está em AX; **`Σ_A V1_A(D_A h)` não está**.

---

## 2. A extensão do domínio do jato em X (resposta, parte 1)

### 2.1 O espaço de jatos [DERIVADO]

O primeiro jato externo em X, lido no **frame ortonormal local** (índices de frame a, b, c ∈ {0..3}):

```
J¹(X) = Sym²(frame)  ⊕  frame ⊗ Sym²(frame)
        h_ab             D_a h_bc
dim   = 10          +    4·10 = 40      ⇒   50 números independentes
```

Simetria de pares: `h_ab = h_ba` e `D_a h_bc = D_a h_cb`. Os 10 componentes seguem `LABELS`; os 40 seguem `(a, (b,c))` com `(b,c)` em `LABELS`. Nada mais entra: o pedido fixa que cada extremo depende de no máximo um jato do campo externo — logo `D²h` não pertence ao vértice (ao potencial, ver §2.3).

### 2.2 O vértice estendido, e o que **não** muda

O vértice em X passa a ser o funcional linear nos dois argumentos:

```
AX(h, Dh) = V0(h)  +  Σ_A V1_A(D_A h)
```

- **Ghost.** `V0(h) = W2(h)` (já usado). A peça derivativa é o termo do próprio docstring do motor: `−(∇_μ c̄_ν)[ c^ρ ∇_ρ h_μν − ½ g_μν c^ρ ∇_ρ (tr h) ]`, isto é, `V1_ρ` tem uma perna `c^ρ` indiferenciada e uma `∇ c̄` derivada — a forma do **W1** existente em `G.vertex(A)[1]`.
  - **Verificação nomeada (não concluída aqui):** o W1 do motor é avaliado em `h`, com a forma `−h_μν + ½δ_μν tr h` — a **mesma estrutura** do termo derivativo, mas lida em `h` em vez de `D_ρ h`. Duas possibilidades: (i) o motor absorveu `∇h` por integração por partes ("after one exact integration by parts", diz o cabeçalho) e o canal derivativo já está parcialmente dentro — então a extensão é de **leitura** (o AX recebe os 50 números e os repassa); (ii) o canal está ausente do AX — então a extensão é de **conteúdo**: avaliar o canal W1 nos 40 números `D_A h`. O teste que decide: aplicar o vértice a um jato com `h = 0`, `Dh ≠ 0` e verificar se a resposta é nula (caso i, parcial) ou não (caso ii). **Não afirmo qual vale.**
- **Métrica.** `vertex_data(A)` já **retorna** a estrutura completa: `(W2, W1[j], WC2[j])` — W2 com derivada externa ausente, `W1[j]` o coeficiente de momento com uma derivada externa `j`, `WC2[j]` os coeficientes de conexão (2×W1). A peça `V1_j(D_j h)` do lado métrico mora nesse par `(W1[j], WC2[j])` — a extensão é **ligá-los** ao AX avaliado nos 40 números. **Verificação nomeada:** confirmar que `WC2` é exatamente a conversão derivada parcial → covariante (conexão do jato), e não um termo físico adicional.
- **O que não muda:** `C(order, word, BY)`, `Bval/BY`, `d2vertex`, os loops de ordem e os cortes de palavra. As palavras são derivadas **em Y**; o jato de X entra **uma vez**, no sanduíche `Gᵀ · AX · G`. A extensão é aditiva: `AX := vertex_first_jet(T10, DT40)` no lugar de `G.vertex(T)[0]` — e nada mais é tocado.

### 2.3 Índices de frame, potencial O(K), simetria de pares

- **Frame.** Os 50 números são componentes de frame em X. A conversão já existente (`PointJets.framed`: a perna superior do ghost em X transforma pela coframe com sinal −) aplica-se ao AX estendido; o índice extra `A` de `D_A h_bc` transforma como **vetor em X**, pela mesma regra já usada para o índice `ξ` do motor. Nenhum índice novo de transformação é inventado.
- **Potencial O(K).** O potencial do EH vem das segundas derivadas do jato; na gauge do espaço-forma (`Ric = 3Kg`) essas segundas derivadas estão fixadas, logo o potencial é função de `h` apenas — **não** de `Dh`. Declarado como verificação nomeada: que nenhum termo `O(K)·D h` nasce no potencial; os termos `O(K)` com estrutura de frame já moram no motor via `frame2` (a variação do frame radial, ramo `len(word)==2`). A base (§4) não muda com K: K é marcador de ordem **dos coeficientes escalares** (`coef = coef⁽⁰⁾ + K·coef⁽¹⁾`), não um elemento tensorial novo.
- **Simetria de pares.** `h` e `Dh` são simétricos no par; o motor conta cada par fora da diagonal duas vezes e divide por `m = multiplicity(a,b)` (1 se a=b, senão 2). Isso é o que o controle de §2.5 protege.

### 2.4 Implementação textual: AX para jato derivativo puro [ESPECIFICAÇÃO — não executada]

A peça **derivativa pura** (o que falta ao AX), ghost:

```python
def ghost_vertex_derivative_jet(DT):
    """Peça V1 do vértice ghost em X: os 40 canais D_A h_BC.

    DT : tupla de 40 Fractions, ordem (A, LABELS[(B,C)]),
         DT[10*A + k] = D_A h_(LABELS[k]) (X),  A,B,C índices de frame.
    Retorna W1_ext : lista de 4 matrizes esparsas 20x20 (Fractions),
         W1_ext[rho] = coeficiente de c^rho · ∇^mu c̄^nu  no canal D_rho h.
    Forma (docstring do motor):  v = −( D_rho h_mu_nu − ½ δ_mu_nu D_rho tr h ).
    Estatuto: especificação escrita; NÃO executada nesta chamada.
    """
    W1_ext = [empty(20) for _ in range(4)]
    for rho in range(4):
        tr = sum(DT[10*rho + LABELS.index((l, l))] for l in range(4))
        for mu in range(4):
            for nu in range(4):
                k = LABELS.index((min(mu, nu), max(mu, nu)))
                v = -(DT[10*rho + k] - F(1, 2)*int(mu == nu)*tr)
                if v:
                    W1_ext[rho][rho][4*(mu+1) + nu] = v
    return W1_ext

def vertex_first_jet(T10, DT40):
    """Vértice ghost em X com o primeiro jato externo completo.
    V(h, Dh) = V0(h) + Σ_A V1_A(D_A h).  Reduz ao atual quando DT40 = 0."""
    W2, _W1 = G.vertex(tuple(T10))          # V0(h): inalterado
    return W2, ghost_vertex_derivative_jet(DT40)
```

E no ponto de Ward (única linha conceitual alterada):

```python
AX = vertex_first_jet(T10, DT40)      # antes: G.vertex(tuple(T))[0]
# C(order, word, BY) passa a receber o par (W2, W1_ext); a regra do produto
# em Y é INALTERADA — DT40 entra uma vez, no sanduíche Gᵀ·AX·G.
```

Lado métrico, mesma espinha: `AX = [vertex_data(T10)[0] + Σ_j W1_j(D_j h), −potential(T10)]`, com `WC2[j]` entrando como a conversão de conexão dos jatos internos — **sujeito à verificação nomeada** de §2.2. O "jato derivativo puro" é exatamente a chamada com `T10 = 0`, que isola os 40 canais e serve de controle de separação: **a resposta com (h = 0, Dh ≠ 0) deve ser inteiramente carregada pela peça nova; a resposta com (h ≠ 0, Dh = 0) deve reproduzir bit a bit o motor atual** (regressão exata sobre `Fraction`).

### 2.5 Controle de multiplicidade de h_01 [ESPECIFICAÇÃO — não executada]

Alvo: o fator `2/m` com `m = multiplicity(a,b)` no loop de Ward. O risco real: um canal fora da diagonal extraído com m errado sai **2×** maior ou menor, silenciosamente.

- **C1 (par cego à ordem).** `T = tensor(0,1)` vs `T' = tensor(1,0)`: respostas idênticas, exatas sobre Q. (O jato físico é o mesmo; o motor deve ser cego à ordem dos índices.)
- **C2 (homogeneidade).** Resposta a `2·tensor(0,1)` = 2 × resposta a `tensor(0,1)`, exata.
- **C3 (convenção 2/m).** A resposta ao jato fora da diagonal unitário, extraída com `m = 2` (fator 1), deve coincidir exatamente com a soma das duas metades `tensor(0,1)/2` e `tensor(1,0)/2` processadas como dois canais `m = 1` (fator 2 cada): `2·val[(0,1),T]/2` vs `2·val[(0,1),T/2] + 2·val[(1,0),T/2]`. Igualdade exata sobre `Fraction` é a prova de que a convenção de multiplicidade e a contagem de pares são consistentes.
- **C4 (o controle morde).** Adulterar `m(0,1)` para 1 deve mudar a saída do canal por **fator exato 2**. Se a adulteração não muda nada, o controle não discrimina → **REFUSED**, não PASS.

---

## 3. Por que não transportar T_X como função de Y [demonstração escrita]

**Afirmação.** Na identidade de Ward em Y com X fixo, o jato de teste deve obedecer `∂_Y T_X ≡ 0`. Transportar `T_X` para Y (por transporte paralelo ao longo de XY) é erro de objeto — em quatro passos:

1. **A Ward deriva o integrando.** A identidade é `D^μ_Y [ O_μ(X,Y) · T_X ]`. O operador medido é `O_μ(X,Y)`; o jato `T_X` é um **elemento livre** de J¹(X) — 50 números independentes. "Derivar mantendo X fixo" significa que a regra do produto só gera termos sobre os propagadores e os vértices de Y. Se `T(Y) = PT_{X→Y} T_X`, então `D_Y T = −Ω(Y)·T(Y) ≠ 0`, e nasce um termo `∫ Ω·T·O` que **não pertence ao operador** — pertence à regra de transporte escolhida.
2. **O termo espúrio não é universal.** Ω é O(K) e o transporte depende do caminho: no espaço-forma, a holonomia acumula ∼ K·área, logo `T(Y)` é **multivalorado** a O(K) — nem sequer é uma função de Y. Um coeficiente lido contra um objeto multivalorado não é coeficiente de operador nenhum.
3. **Rompe a fatoração e duplica o frame.** A leitura de coeficientes pressupõe `coeficiente(X) ⊗ base(X,Y)` com `∂_Y coeficiente = 0`. Além disso, o motor **já** inclui a variação do *frame* em Y (`frame2`, ramo `len(word)==2` — as segundas derivadas do frame radial). Um `T(Y)` transportado injetaria a variação do *jato* no mesmo lugar: dupla contagem da estrutura O(K), misturada com o potencial real.
4. **No código, é omissão ou mudança de objeto.** `C(order, word, BY)` deriva `J.matrix` e `BY`, nunca `AX`. Transportar T sem modificar `C` é omitir um termo da regra do produto; modificar `C` para admiti-lo é deixar de medir `O(X,Y)`. ∎

**Corolário operacional.** `T_X` permanece um ponto livre de J¹(X) (50 números). Toda dependência em Y vive nos propagadores, nos vértices de Y e no frame de Y — como está.

---

## 4. A base covariante mínima (resposta, parte 2)

### 4.1 Dados e relações explícitas

- **Dados:** `δ_ab`, `r_a = (X−Y)_a` (no frame), `z = r²`, `L = ln(μ² z)` (μ fixo), `K` a ordem 1.
- **Relações algébricas:** `r^a r_a = z`; `δ^a_a = 4`; `r^a δ_ab = r_b`; `δ^{ab}δ_ab = 4`; `δ^{ab} r_a r_b = z`. Qualquer produto de δ's e r's com as simetrias dadas reduz-se às listas de §4.2 (enumeração por grau em r).
- **Relações diferenciais usadas pelo Ward em Y** (≤ 2 derivadas): `D_a z = 2 r_a + O(K)`; `D_a L = 2 r_a / z + O(K)`; `D_a r_b = δ_ab + O(K)`. Os O(K) **não são computados aqui**: pertencem ao motor de frame. [DECLARADO: a única forma compatível com isotropia e simetria a,b é `δ_ab z − r_a r_b` vezes um coeficiente ∝ K — coeficiente a confirmar contra o motor, não cravado.]
- **Independência dos escalares:** as famílias `{z^p L^q}` são linearmente independentes sobre Q (padrão; [KNOWN/DERIVADO]). Operacionalmente já está no motor: `coeff(B.L,k)` separa q = 0,1 e o `assert` garante que nenhum `L²` foi omitido.
- **Divisão do trabalho tensor/escalar:** a base tensorial é **polinomial** em r; toda singularidade mora nos coeficientes escalares (`z^p`, `L`). É isso que permite ao teorema de invariantes (§4.3) decidir a completude da parte tensorial.

### 4.2 As três listas [DERIVADO por enumeração; completude via teorema de invariantes — KNOWN externo]

Enumeração por grau em r, com as simetrias declaradas. O número é o comprimento da lista; a lista é a prova auditável.

**Canal ghost, coeficiente de h_jk (saída vetorial i):** `T_{i;jk}`, sim j↔k.

```
grau 1:  A1 = δ_jk r_i ;  A2 = δ_ij r_k + δ_ik r_j
grau 3:  A3 = r_i r_j r_k
```
**3 tensores** × {1, L} = **6 canais**.

**Canal ghost, coeficiente de D_c h_jk:** `T_{i;c,jk}`, sim j↔k.

```
grau 0:  B1 = δ_ic δ_jk ;  B2 = δ_ij δ_ck + δ_ik δ_cj
grau 2:  B3 = δ_jk r_i r_c ;  B4 = δ_ic r_j r_k ;
         B5 = (δ_ij r_k + δ_ik r_j) r_c ;  B6 = (δ_cj r_k + δ_ck r_j) r_i
grau 4:  B7 = r_i r_c r_j r_k
```
**7 tensores** × {1, L} = **14 canais**.

**Operador métrico (par → par):** `T_{ab;cd}`, sim a↔b e c↔d.

```
grau 0:  M1 = δ_ab δ_cd ;  M2 = δ_ac δ_bd + δ_ad δ_bc
grau 2:  M3 = δ_ab r_c r_d ;  M4 = r_a r_b δ_cd ;
         M5 = (δ_ac r_b + δ_bc r_a) r_d + (δ_ad r_b + δ_bd r_a) r_c
grau 4:  M6 = r_a r_b r_c r_d
```
**6 tensores** × {1, L} = **12 canais** — sem simetria de troca de pares. Se o operador for adicionalmente simétrico sob `(ab)↔(cd)` (auto-adjunção), M3 e M4 combinam-se num só: **5 × 2 = 10**. Qual das duas vale é propriedade do operador — [INPUT/verificação nomeada], não assumida.

**Independência interna de cada lista** [DERIVADO]: graus distintos em r são independentes (homogeneidade); dentro do mesmo grau, os tensores listados têm padrões de contração de índices distintos (δ's em pares diferentes). A independência é assim derivada, não só afirmada — e é **confirmável** pela matriz de avaliação de §5/§6.

### 4.3 Completude — o que ela cobre e o que não cobre

- **Cobertura** [KNOWN externo]: pelo teorema clássico de invariantes de O(n) (Weyl; Spencer–Rivlin para tensores equivariantes), todo tensor O(4)-equivariante polinomial em r, com as simetrias de par fixadas, é combinação das listas acima. As listas são, portanto, **completas por construção** para a parte tensorial — o conteúdo da prova de completude é o teorema de invariantes mais a enumeração exibida, **não** o ajuste de coeficientes.
- **O que a completude não cobre** (declarado, sem exceção): (i) o termo **suave de Hadamard W** — ausente dos kernels singulares por natureza, não por evidência; **não autoriza W = 0**; (ii) a parte diagonal/de contato — fora do pedido; (iii) **Q2 completo** — os coeficientes fora da diagonal a O(K¹) **não** o determinam, e nada aqui o infere; (iv) K².

### 4.4 Como a base *verifica* não-omissão

A completude da base é teorema; a verificação de que **o operador calculado não omitiu termo** é outra coisa, e reduz-se a quatro testes, todos com controle negativo:

1. **Equivariância:** o motor, rodado em pontos relacionados por um O(4) racional (rotações de 90°, reflexões), deve dar respostas relacionadas pela mesma transformação. Se falha, há termo não-equivariante — a base não é o problema, o cálculo é.
2. **Isotropia dos coeficientes:** pontos com o mesmo z e direções diferentes devem dar os mesmos coeficientes escalares. Falha ⇒ dependência angular não capturada ⇒ termo omitido.
3. **Truncamento:** `assert L² = 0` (existente) + o análogo em potências de z: nenhuma potência fora das declaradas pelo ansatz. Falha ⇒ forma funcional omitida.
4. **Ajuste + holdout:** §5.

---

## 5. Reconstrução por amostras racionais — prova da base ≠ ajuste

Separação exigida pelo pedido, agora operacionalizada:

- **Prova da base (offline):** completude (teorema de invariantes + enumeração, §4) e independência (derivada em §4.2, confirmada pelo rank da matriz de avaliação). **Nenhum número do motor entra aqui.**
- **Ajuste (online, sobre Q):** avaliar o operador (motor estendido de §2) e a base nos mesmos pontos; resolver os coeficientes escalares sobre `Fraction`; L entra como símbolo (potências separadas, nunca avaliadas numericamente).
- **Amostras:** pontos com coordenadas inteiras/racionais, z > 0, direções não coplanares; número de pontos ≥ número de coeficientes + margem; o conjunto fica registrado.
- **Holdout (o que prova a identidade):** pontos novos, fora do conjunto de ajuste. A identidade candidata só é **DECLARADA** se os coeficientes ajustados a reproduzirem exatamente neles. **Um ajuste que apenas interpola a amostra não prova identidade** — endossado verbatim do pedido.
- **Controles negativos (o teste morde ou é REFUSED):** (a) remover um tensor da base deve degradar o holdout; (b) perturbar um coeficiente ajustado deve degradar o holdout; (c) dois pontos com mesma direção e z distintos testam a separação z vs L; (d) a regressão `DT40 = 0` deve reproduzir bit a bit o motor atual.

---

## 6. Dimensões derivadas vs. matriz a testar

- **Derivadas** (pela lista explícita + homogeneidade em grau de r + padrões de índices, §4.2): 3 e 7 tensores por potência de L (canais ghost), 6 (ou 5, com troca de pares) no canal métrico. São **corolários da lista**, não afirmações soltas.
- **Entregue para teste (não afirmado):** o rank da **matriz de avaliação** `M[p_α, s] = (valor do tensor B_s no ponto p_α)`, com pontos racionais em direções genéricas. O teste: `rank M = #(lista)` — confirma a independência derivada; `rank M < #(lista)` — aponta qual relação foi perdida. A mesma matriz serve à prova de independência (offline) e à recusa de adulterações (C4 de §2.5, controles de §5).
- **Não derivadas aqui, não afirmadas:** dimensões de qualquer setor além dos três listados (ex.: operadores com mais índices livres, ordens K², o setor de contato). Se entrarem em pedido futuro, entram por enumeração nova, não por extrapolação.

---

## 7. Guard-rails e lacunas declaradas

1. **Verificações nomeadas, não concluídas:** (a) se o W1 do motor ghost já absorve `∇h` por integração por partes ou se o canal derivativo falta de fato ao AX (o teste decisivo está em §2.2); (b) o papel exato de `WC2[j]` no motor métrico (conexão do jato vs. termo físico); (c) ausência de termos `O(K)·Dh` no potencial; (d) o coeficiente O(K) das relações diferenciais de §4.1 (forma δ_ab z − r_a r_b declarada, coeficiente a confirmar contra o motor).
2. **Proibições respeitadas:** Q2 completo não é inferido; W suave não é fixado a zero; sem fonte Einstein e sem contatos; divergência-Y e fonte adjunta não revisitadas.
3. **Ordem:** tudo a O(K¹); K² fora.
4. **Estatuto final:** esta entrega é **[DECLARADA]** — especificação e demonstração escritas, com os pontos de decisão marcados — e aguarda a **revisão local independente**. Nenhum arquivo, kernel, gate ou hash foi criado, alterado ou alegado como executado.