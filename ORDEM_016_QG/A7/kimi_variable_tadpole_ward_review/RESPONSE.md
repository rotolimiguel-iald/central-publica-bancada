# ORDEM_016 — A-7.b: a identidade de Ward do tadpole finito quártico com W variável

**Estatuto desta unidade: [DECLARADO até verificação].** Derivação algébrica exibida passo a passo; os motores anexos (`metric_principal_vertices.py`, `metric_quartic_vertices.py`) são a autoridade numérica e não foram substituídos nem executados aqui. Escopo: 4D, K=Λ=0, g = δ + h (euclidiano, como os motores), setor ΓΓ de Einstein–Hilbert, um vértice quártico, módulo divergência com cutoff constante. Não se trata de contatos de dois vértices nem do tadpole logarítmico curvo; não se inventa A2, não se escolhe a ordenação T1, não se calcula a Q2 integral. W(X,Y) é dado formal suave e simétrico — nenhuma propriedade de estado ou bissolução é usada.

---

## 1. Convenções, registros e jatos

**Ação e corrente.** Trabalha-se com a forma ΓΓ de Einstein,

```
S_ΓΓ[g] = (1/2κ²) ∫ √g g^{μν} ( Γ^ρ_{σμ} Γ^σ_{νρ} − Γ^ρ_{μν} Γ^σ_{ρσ} ),
```

que difere de √g R pela divergência [KNOWN]:

```
√g R = (forma ΓΓ) + ∂_ρ C^ρ,   C^ρ = √g ( g^{μν} Γ^ρ_{μν} − g^{μρ} Γ^σ_{μσ} ).
```

Com cutoff constante (domínio e borda fixos, campos e jatos com suporte no interior), ∫∂C = 0 e as identidades de Ward de S_ΓΓ e de S_EH coincidem. A expansão da corrente em jatos globais (W polinomial sem decaimento) fica marcada **OPEN** (§7).

**Ghost e seu abaixamento.** O parâmetro é o campo vetorial `c^a(x)` (ghost), com jato `c(x) = ĉ e^{iqx}`. Seu abaixado é `c♭_a := g_{ab} c^b`. Os dois objetos são distintos, e a distinção é operacional:

```
(Lie_c g)_{ab} = c^ρ ∂_ρ g_{ab} + g_{ρb} ∂_a c^ρ + g_{aρ} ∂_b c^ρ = ∇_a c♭_b + ∇_b c♭_a.
```

**Dois registros, sem equivalência imposta:**

- **Registro I (c fixo):** `Lie_c g` é *afim linear* em g, logo `D_g(Lie_c g)[h] = Lie_c h` e `D²_g(Lie_c g) = 0`.
- **Registro II (v = c♭ fixo):** então `c = g⁻¹v` varia com g, e a derivada dessa mudança **não se descarta**:

```
D_g c[h] = − g⁻¹ h c ,
D_g(Lie_c g)[h] = Lie_c h − Lie_{g⁻¹hc} g ,
D²_g(Lie_c g)[h₁,h₂] = − Lie_{g⁻¹h₂c} h₁ − Lie_{g⁻¹h₁c} h₂ + Lie_{g⁻¹h₂g⁻¹h₁c} g  ≠ 0 .
```

A nota-fonte (`DERIVACAO.md`) trabalha com `ε = M⁻¹v`, v fixo — Registro II na família de métricas constantes; a identidade é derivada aqui no Registro I e a passagem é contabilizada explicitamente (§2.3).

**W e seus jatos.** Polarização declarada com fator de simetrização **1** (sem ½; com ½ os dois lados escalam juntos, pois a identidade é homogênea em W):

```
W(X,Y) = ζ(X) ⊗ η(Y) + η(X) ⊗ ζ(Y) ,
ζ, η suaves; valores e primeiras derivadas independentes no ponto.

W00 := W(x,x)              (jato de valor)
W10 := ∂_X W |_{Y=X}       (jato na 1ª perna)
W01 := ∂_Y W |_{Y=X}       (jato na 2ª perna)
W11 := ∂_X ∂_Y W |_{Y=X}   (jato cruzado)
```

Com a polarização acima: `W10 = ∂ζ⊗η0 + ∂η⊗ζ0`, `W01 = ζ0⊗∂η + η0⊗∂ζ`, `W11 = ∂ζ⊗∂η + ∂η⊗∂ζ`.

**Conversão Fourier ↔ jatos reais.** O motor `gamma2(H,p)` retira i/2: `Γ̂^ρ_{μν} = (i/2) γ2^ρ_{μν}(H,p)` sob `exp(+ipx)`. Um jato real `H(x) = H0 + (k·x) H1` dá `Γ_real = (1/2) γ2(H1,k)`. Como **todo** termo ΓΓ tem exatamente duas pernas diferenciadas (§3), a conversão multiplica todos os monômios pelo mesmo fator `(i/2)² → (1/2)²`, i.e., um **sinal global −1** em H, C e Q — exatamente o "outro −1 na ordem 2" que a nota-fonte absorveu na convenção de unidades. Sendo homogêneo, o sinal cancela entre os dois lados da identidade de Ward; o que importa é a unicidade da convenção ao ligar W10, W01, W11. A mesma homogeneidade em c absorve a convenção do acervo para o gauge: `G(c) := gauge_matrix(q,ĉ) = q_a ĉ_b + q_b ĉ_a` (símbolo real, sem i e sem o 2 canônico) e o transporte `L(c; h, k) := lie_matrix(h, k, q, ĉ) = (ĉ·k) h + q_a (hĉ)_b + q_b (hĉ)_a`, ambos já implementados nos motores.

---

## 2. A cadeia de Ward por diferenciação, antes de contrair

### 2.1 Identidade mestra e três diferenciações (Registro I, c fixo)

A invariância de difeomorfismo da ação (módulo ∂C, com jatos de suporte) dá a identidade funcional

```
𝓦⁰[g; c] := S′(g)[ Lie_c g ] = 0     ∀g, c .
```

Diferenciando em g com **c fixo** (apenas S e o argumento `Lie_c g` variam; `D_g(Lie_c g)[h] = Lie_c h`, `D²=0`):

```
(W1)  S″[h₁, Lie_c g] + S′[Lie_c h₁] = 0
(W2)  S‴[h₁,h₂, Lie_c g] + S″[h₁, Lie_c h₂] + S″[h₂, Lie_c h₁] = 0
(WQ)  S⁗[h₁,h₂,h₃, Lie_c g] + S‴[h₁,h₂, Lie_c h₃] + S‴[h₁,h₃, Lie_c h₂] + S‴[h₂,h₃, Lie_c h₁] = 0 .
```

Avaliando no fundo plano γ (on-shell: S′ = 0; vale para **toda** métrica constante M não degenerada, que é plana com K=Λ=0 — esta é a dependência no fundo em sua forma mais fraca), com a notação dos motores

```
H[h₁,h₂] := eh_quadratic_8k      (Hessiana ×8κ)
C[h₁,h₂,h₃] := eh_cubic_16k      (vértice cúbico ×16κ)
Q[h₁,h₂,h₃,h₄] := eh_quartic_32k (vértice quártico ×32κ, polarizado, sem ÷4!)
G(c) := gauge_matrix(q,ĉ)        (perna gauge, momento q)
L(c; h, k) := lie_matrix(h,k,q,ĉ) (transporte, momento k+q),
```

a cadeia fica:

```
(W1)  H[ h₁, G(c) ] = 0
(W2)  C[ h₁, h₂, G(c) ] = − ( H[ L(c;h₁), h₂ ] + H[ h₁, L(c;h₂) ] )
(WQ)  Q[ h₁, h₂, h₃, G(c) ] = − ( C[h₁,h₂, L(c;h₃)] + C[h₁,h₃, L(c;h₂)] + C[h₂,h₃, L(c;h₁)] ) .
```

**Leitura dos termos "quadráticos" e "cúbicos":** em (W2), o vértice cúbico com uma perna de gauge não é um objeto novo — é a soma dos *transportes* da Hessiana (termos quadráticos) pelas duas pernas restantes. Em (WQ), o vértice quártico com uma perna de gauge é a soma dos três transportes do cúbico. Cada ordem é o transporte da anterior; **não há termos residuais de ordem inferior** em (WQ) precisamente porque `D²_g(Lie_c g) = 0` com c fixo.

### 2.2 Decomposição do transporte

Com h de momento k e c de momento q:

```
L(c; h, k) = (ĉ·k) h        ← peça ESCALAR (não é gauge; vive só com k ≠ 0)
           + q_a(hĉ)_b + q_b(hĉ)_a   ← peça GAUGE = G(hĉ) .
```

Esta decomposição é o pivô de tudo o que segue: com pernas de jato zero, só a peça gauge sobrevive; com jatos de W (k ≠ 0), a peça escalar liga.

### 2.3 Registro II e a família de métricas constantes (a derivação da nota-fonte)

A nota obtém sua nulidade assim: para cada M constante, `H_M[ h, G_M v ] = 0` com `G_M v := Lie_{M⁻¹v} M = (pv+vp)` (a escolha ε = M⁻¹v escreve a imagem de gauge de todo M na forma canônica, v fixo). Derivando **duas vezes em M** nas direções constantes E_a, E_b (momento zero):

```
D²_M[ H_M[h, G_M v] ] = (D²H)[h, G_M v]              ← a peça Q com duas pernas de jato zero
 + (DH[E_a])[h, D(G_M v)[E_b]] + (DH[E_b])[h, D(G_M v)[E_a]]   ← peças C
 + H_M[ h, D²(G_M v)[E_a,E_b] ] .
```

Aqui **a derivada da mudança ε(M) entra**: `Dε[E] = −M⁻¹ E ε`, e `D(G_M v)[E] = Lie_ε E − G(Eε)`; em `D²(G_M v)` aparece uma peça `G((E_aE_b+E_bE_a)ε)` que é gauge de M e morre contra H_M, e peças de transporte que se reorganizam nos termos C. O ponto de disciplina: a decomposição "o que é Q puro vs. transportes" **difere** entre os Registros I e II, embora a nulidade total seja a mesma — registra-se sem impor equivalência. Com fundo curvo (fora de escopo), S′ ≠ 0 reintroduz o lado direito de (W1) e a cadeia ganha termos de equação de movimento; não se transporta a conclusão.

---

## 3. O vértice quártico e suas seis escolhas × duas ordens

Cada monômio de S_ΓΓ é `√g · g⁻¹ g⁻¹ g⁻¹ · (∂g)(∂g)`: três métricas inversas não diferenciadas e **exatamente duas pernas diferenciadas**. O motor `eh_quartic_32k` varre as `combinations(range(4),2)` = **6 escolhas não ordenadas** do par não-γ (as pernas A,B de `second_coefficient_4`, o coeficiente de segunda variação das três inversas) × as **2 ordens** dos dois γ restantes — 12 atribuições, já somadas, polarizadas, sem divisão adicional por 4!.

No tadpole da nota (pernas externas A(p), B(−p) com momento; internas E_a, E_b com momento zero), das 12 atribuições sobrevivem apenas as 2 com par não-γ = (E_a, E_b): qualquer γ em perna interna morre (`gamma2(E,0)=0`). **Com W variável, as 12 atribuições vivem:** uma perna interna com jato k pode ser γ (e a perna externa correspondente deixa de o ser), e o grau total de derivação (2) é mantido por termo: W10/W01 movem uma derivada de uma perna externa para uma interna; W11 põe uma em cada interna e nenhuma nas externas.

---

## 4. A identidade de Ward do tadpole com W variável

**Definição (símbolo, momentos livres; a conservação é propriedade da função de Green, não do vértice formal — os motores não a impõem):**

```
𝓣_W[h₁,h₂] := (1/16) Σ_{a≤b} { W00^{ab} · Q[h₁,h₂,E_a,E_b]
              + W10_μ^{ab} · Q[h₁,h₂,E_a^{(μ)},E_b] + W01_ν^{ab} · Q[h₁,h₂,E_a,E_b^{(ν)}]
              + W11_{μν}^{ab} · Q[h₁,h₂,E_a^{(μ)},E_b^{(ν)}] }
```

(10 componentes independentes, 55 pares a≤b; o fator ½ fora-diagonal contido em W, como na nota; sem ÷4!.)

### 4.1 Forma I — bruta, termo a termo nos jatos

Substituindo a perna externa 2 pela perna de gauge G(c) (a escolha da nota) e aplicando (WQ) a cada configuração de jatos — que são independentes no ponto, logo dão **quatro identidades independentes**:

```
𝓣_W[h₁, G(c)] = −(1/16) Σ_{a≤b} {
   W00^{ab} [ C(h₁,E_a, L(c;E_b,0)) + C(h₁,E_b, L(c;E_a,0)) + C(E_a,E_b, L(c;h₁,p)) ]
 + W10_μ^{ab} [ C(h₁,E_a^{(μ)}, L(c;E_b,0)) + C(h₁,E_b, L(c;E_a,μ)) + C(E_a^{(μ)},E_b, L(c;h₁,p)) ]
 + W01_ν^{ab} [ C(h₁,E_a, L(c;E_b,ν)) + C(h₁,E_b^{(ν)}, L(c;E_a,0)) + C(E_a,E_b^{(ν)}, L(c;h₁,p)) ]
 + W11_{μν}^{ab}[ C(h₁,E_a^{(μ)}, L(c;E_b,ν)) + C(h₁,E_b^{(ν)}, L(c;E_a,μ)) + C(E_a^{(μ)},E_b^{(ν)}, L(c;h₁,p)) ] } ,
```

com `L(c; E^{(k)}) = (ĉ·k)E + G(Eĉ)` decomposto como em §2.2.

### 4.2 Forma II — com o transporte passado para W (módulo borda)

Os dois primeiros cúbicos de cada linha são `L(c)` agindo nas pernas internas antes da contração. Como `L(c)` é derivação no pareamento, integração por partes na contração (módulo borda, cutoff constante) move a ação para W:

```
⟨W, C(h₁, E_X, L(c)E_Y)⟩ + ⟨W, C(h₁, L(c)E_X, E_Y)⟩ = −⟨ (𝓛_c W), C(h₁, E_X, E_Y)⟩ + Borda ,
𝓛_c W := (Lie_c^X + Lie_c^Y) W ,
```

donde

```
𝓣_W[h₁, G(c)] = (1/16) Σ_{a≤b} { (𝓛_c W)^{ab} · C[h₁, E_a, E_b] − W^{ab} · C[E_a, E_b, L(c;h₁,p)] } + Borda .
```

Em jatos, `𝓛_c W` tem duas peças: **fluxo** `(ĉ·(W10+W01))` (a derivada total na diagonal; módulo borda W01 ≡ −W10, logo a combinação física é W10 − W01) e **rotação** dos índices livres por `∂c` sobre W00 (presente mesmo com jatos nulos, mas morta contra `C(·,0,0) = 0`, §5).

### 4.3 Os registros pedidos, lado a lado, sem equivalência

| registro | W00 | W10/W01/W11 | 𝓛_c W | 𝓣_W[h₁,G(c)] |
|---|---|---|---|---|
| (i) **W fixo sob s0** (covariância constante da nota) | livre (anisotropia permitida) | 0 | 0 | **= 0** (§5) |
| (ii) **W transportado** por Lie_c^X+Lie_c^Y | livre | ≠ 0 | fluxo + rotação | **≠ 0 em geral**; vale a Forma I/II |

Os registros **não são equivalentes**: no (i), os jatos são mortos por definição; no (ii), as peças de fluxo e rotação existem e só morrem no caso degenerado (jatos nulos e `C(·,0,0)=0`) — coincidência numérica em zero por razões distintas, não identidade dos regimes.

### 4.4 Os termos que invalidam a extrapolação 𝓣_W·G = 0

- **I1 — o terceiro cúbico acorda.** `C(E_a^{(k3)}, E_b^{(k4)}, L(c;h₁,p))`: com (k3,k4) = (0,0) morre trivialmente (cada termo cúbico tem dois γ; dois momentos nulos os matam). Com jatos não nulos, contribui. Era invisível na análise constante.
- **I2 — a peça escalar do transporte.** `(ĉ·k)E` não é gauge e só existe com k ≠ 0; entra nos dois primeiros cúbicos.
- **I3 — quebra da anulação simétrica.** Com jatos zero, `C(h₁,E_a,G(E_b ĉ)) + C(h₁,E_b,G(E_a ĉ)) = 0` (soma simétrica a↔b, verificada na nota). Com jatos (k3 ≠ k4, ou W10 ≠ W01 pesando as fibras por argumento), a soma perde a simetria e não anula.
- **I4 — o transporte de W (Forma II).** `⟨𝓛_c W, C⟩` só morre se W for bi-invariante sob a ação diagonal; W genérico não o é.
- **I5 — mudança de registro.** Com v = c♭ fixo, `D²_g(Lie_c g) ≠ 0` injeta termos Hessianos `H[·, D²ω]` na quártica, e a imagem de gauge de ordem ≥ 2 inclui `−2Γ·v`: a nulidade não se transporta trocando o registro sem pagar o termo de mudança.

---

## 5. Recuperação da nulidade constante (a nota-fonte)

Com jatos nulos (W00 arbitrário, **sem isotropia**):

1. `Q[A, G(c), E_a, E_b] = 0` — verificado na nota para as 55 fibras; aqui segue de (WQ) + os itens 2–3.
2. `C(h₁,E_a,L(c;E_b,0)) + C(h₁,E_b,L(c;E_a,0)) = 0`: com k=0, `L(c;E,0) = G(Eĉ)` (só peça gauge); a soma simétrica a↔b anula-se (a "soma dos transportes das duas pernas internas igualmente nula" da nota).
3. `C(E_a, E_b, L(c;h₁,p)) = 0`: dois momentos nulos matam os dois γ de cada termo cúbico.

Logo `𝓣_W[h₁,G(c)] = 0` para todo W00 constante — a nulidade da nota, **derivada da degenerescência de gauge da Hessiana em toda a família plana constante** (§2.3), não de extrapolar três momentos. A identidade (WQ) é a "identidade entre a expressão cúbica e quártica" que a v2 da nota exige ao lado das duas nulidades.

---

## 6. Controle esparso variável (especificação; resultados esperados [DECLARADO])

Objetos esparsos (entradas inteiras; os motores são exatos), fundo γ=δ:

```
h₁ = A := basis(3,3),  momento p = e_0
ghost: ĉ = e_2, momento q = e_1   ⇒  G(c) = gauge_matrix(q,ĉ)  (entradas 12 e 21)
W = ζ⊗η + η⊗ζ (sem ½):  ζ(X) = basis(0,0) + (μ·X)·basis(0,1), μ = e_2
                        η(Y) = basis(1,1) + (ν·Y)·basis(2,2), ν = e_3
⇒ W00: 4 entradas; W10 = e_2 ⊗ (ζ̃η0 + η̃ζ0); W01 = e_3 ⊗ (ζ0η̃ + η0ζ̃); W11 = e_2e_3 ⊗ (ζ̃η̃ + η̃ζ̃)
```

**Teste A (a identidade, por jato, momentos livres).** Para cada J ∈ {00, 10(μ), 01(ν), 11(μ,ν)}: computar `LHS_J = Σ W_J^{ab} eh_quartic_32k(A,p; G(c),q; E_a,k3; E_b,k4)` e `RHS_J = −Σ W_J^{ab} [ eh_cubic_16k(A,p; E_a,k3; L(c;E_b,k4)) + eh_cubic_16k(A,p; E_b,k4; L(c;E_a,k3)) + eh_cubic_16k(E_a,k3; E_b,k4; L(c;A,p)) ]`, com `L` via `lie_matrix`. Esperado: **LHS_J = RHS_J como inteiros exatos, separadamente para cada J** (jatos independentes).

**Teste B (recuperação constante).** Em J=00, varrer as 55 fibras (a≤b): esperado `LHS_00 = 0`, `RHS_00 = 0` (termo a termo: soma simétrica nula + terceiro cúbico morto).

**Teste C (a invalidação).** Esperado: pelo menos um de LHS_10, LHS_01, LHS_11 ≠ 0, e o termo I1 (`eh_cubic_16k(E_a,E_b, L(c;A,p))`) ≠ 0 — o termo que era trivialmente zero no caso constante.

**Teste D (estrutura ΓΓ).** Com k3=k4=0, das 12 atribuições (6×2) só as 2 com par não-γ = pernas internas são não nulas; com jatos, as 12 ligam. Esperado: nulos exatos no primeiro caso, não nulos no segundo.

**Controles negativos (o teste deve poder falhar):**

- **CN1 (peça escalar):** redefinir `L(c;E,k)` omitindo a peça `(ĉ·k)E`. Esperado: a identidade em J=10/01/11 **quebra com resíduo inteiro não nulo** (é exatamente ali que a peça vive); se não quebrar, o controle não morde → REFUSED.
- **CN2 (mistura de identidades):** usar a identidade com gauge na perna *interna* (válida por (WQ) com h₂ = E_a) no lugar da identidade com gauge na perna externa. Esperado: desigualdade O(1) — as duas identidades são distintas e a mistura é erro, detectável.

Critério: inteiros exatos; qualquer desvio ≠ 0 → REFUSED; nulos esperados devem ser exatamente 0. Nenhum número destes testes é afirmado aqui — a especificação e os valores esperados ficam [DECLARADO] até execução.

---

## 7. Localização da corrente

A corrente [KNOWN] está exibida em §1: `C^ρ = √g (g^{μν} Γ^ρ_{μν} − g^{μρ} Γ^σ_{μσ})`. Com cutoff constante e jatos de suporte compacto, `∫∂C = 0` e a forma ΓΓ herda as identidades de √g R, incluindo a borda da integração por partes da Forma II. **OPEN:** a expansão explícita de C^ρ em jatos com W polinomial global (sem decaimento), i.e., a contabilidade da borda para o tadpole variável nesse regime — não computada nesta unidade.

---

## 8. O que não foi feito (lacunas declaradas)

Não se inventou A2; não se escolheu a ordenação T1; não se calculou a Q2 integral; não se tratou curvatura de fundo, cutoff variável, outras aridades, contatos de dois vértices, tadpole logarítmico, nem normalização lorentziana; não se impôs equivalência entre W fixo sob s0 e W transportado por Lie_c^X+Lie_c^Y; não se transportou a conclusão constante ao caso variável. Kernel, gate e prescrição intactos. O alvo desta unidade — **este somando e sua lei de transporte** — está entregue: a identidade de Ward (WQ) derivada antes de contrair, sua restrição ao tadpole em jatos (Forma I/II), os cinco termos que invalidam a extrapolação 𝓣_W·G = 0, a recuperação da nulidade constante e um controle esparso com dois controles negativos, tudo [DECLARADO até verificação] pelos motores anexos.