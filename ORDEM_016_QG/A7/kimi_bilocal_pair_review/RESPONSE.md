# ORDEM_016 A-7.b — Contração de Ward da Hessiana bilocal com G(c) no extremo Y (primeira ordem em K)

**Estatuto deste texto [DECLARADO]:** derivação analítica escrita à mão sobre os dois anexos fornecidos; nenhuma execução de código é alegada; cada conta carrega um controle negativo que a falsifica em CAS. Prescrição da carta ancorada preservada sem troca silenciosa: `R(u) = FP_a[(1−a) μ^{2a} z^a u]`, `z = x·x`, `μ>0` fixo, `C_E = −4π²`. Espaço-forma auxiliar euclidiana 4D, `Ric = 3K g`, `Λ = 3K`, σ constante. A parte suave W não entra — e isto não escolhe estado com W=0. Escopo distinto de `nonlocal_source_adjoint_orientation`: aqui se constrói a **divergência do PAR nos dois extremos**, não a imagem Einstein da fonte, não tabela Fourier.

**Lacunas de entrada declaradas (antes de qualquer conta):** (i) a 087 e a carta ancorada não foram carregadas — só os dois scripts e a prescrição; (ii) os imports do segundo script (`word_value`, `AXES`, `node_weights`, `green_integer`, `weighted`, `green`, `transpose`, `frob`, `sandwich`, `M.LABELS`) são assinaturas, não conteúdo — não expando o vértice fantasma além do que está visível; (iii) a substituição `w = (x−y)²` não aparece nas linhas 1–29 do primeiro anexo; assumo que ocorre **entre** `derivative()` e `anchored()`, como manda o docstring ("imposed only after differentiation"); (iv) tomo `G(c)_{ab} = k_ab = D_a c_b + D_b c_a` como dado pelo próprio pedido; (v) os kernels dos anexos são lidos como a **parte singular** (parametrices), sem prefator físico global — a razão certo/errado que computo é independente dele.

---

## 1. A ordem de trabalho (o que "ANTES de impor Y=0" exige)

O pipeline tem quatro estágios e a ordem é o conteúdo:

```
(E1) kernels de dois extremos:  K = K(x, y; w, L),  w, L símbolos independentes
(E2) IBP formal em Y sobre k(c): derivadas passam de c aos kernels
(E3) execução das ∇^Y pela regra de dois extremos (§2), y ainda livre
(E4) separação fora-da-diagonal / contatos (§4)
(E5) só agora: w → (x−y)²
(E6) só por último: y → 0   (= anchored(f) do anexo 1)
```

Os dois erros gémeos que esta ordem bloqueia: (a) `dY = −dX`, que só vale se os coeficientes não dependem de `x, y` separadamente — falso a ordem K; (b) ancorar cedo: `∂^Y_a P1^{ab}|_{y=0} = −3x_b/2 ≠ 0` embora a **função** `P1(x,0)` seja radial. A derivada não comuta com a âncora; o anexo 1 existe exatamente para isso (docstring, linhas 3–5).

---

## 2. A regra de dois extremos e a identidade-mestra

Todo kernel completo de dois extremos no modelo truncado tem a forma `K = Σ coeficientes_RNC(x,y) × radial(w, L)`, com `w = (x−y)²`, `L = log w` (leitura do anexo 1: os termos `−5d L/4`, `+dd L/2` são lineares em `L`, e a regra da linha 18 traz `∂_L/w`). A linha 18 é a regra:

```
∂^X_j K = ∂K/∂x^j|_coef  + 2 r_j (∂_w + w⁻¹∂_L) K
∂^Y_j K = ∂K/∂y^j|_coef  − 2 r_j (∂_w + w⁻¹∂_L) K        (r = x − y)
```

**Identidade-mestra [DERIVADO neste texto]:**

```
(∂^X_j + ∂^Y_j) K = (∂/∂x^j + ∂/∂y^j) K|_coeficientes explícitos
```

a parte radial cancela **exatamente**; o que sobra é só curvatura explícita. Em coordenadas bicêntricas `r = x−y`, `s = x+y`: `∂_x + ∂_y = 2∂_s`, e isto responde à distinção pedida:

- **Mover derivada num tensor** = `∂_y` legítimo de IBP = `−∂_r (radial) + ∂_s (coeficientes)` + conexão de fibra em Y + medida. Tudo implementável.
- **Mover o ponto de ancoragem** = `∂_s` puro: variação do centro da carta RNC. Não é IBP nem derivada de fibra; é re-expansão da parametrix. A hipótese proibida `dY = −dX` é exatamente jogar fora o `2∂_s`: em K=0 os coeficientes são constantes e o erro é invisível (é por isso que a confusão nasce no plano); a ordem K ela perde `2∂_s(coeficientes)`.

Formas de erro fechadas, prontas para CAS [DERIVADO, falsificável pelo CN2 do §7]:

```
Err_j P1_{ab}    := (∂_x+∂_y)_j P1_{ab}    = (1/3)( r_j δ_{ab} − 2 δ_{aj} r_b + r_a δ_{bj} )
Err_j distance1  := (∂_x+∂_y)_j distance1  = (2/3)( x_j (r·y) − y_j (r·x) )   (simétrico x↔y ✓)
Err_j gX1_{ab}   = −(2 x_j δ_{ab} − δ_{aj} x_b − x_a δ_{bj})/3 ;  Err_j gY1 = idem com y
Err_j (constantes, e da parte L pura) = 0
```

(Verificação de consistência já feita no texto: `2∂_s P1` em `(r,s)` reproduz `Err_j P1` — `P1_{ab} = (r·s)δ_{ab}/6 − (s_a r_b + r_a s_b)/12 + (r_a s_b − s_a r_b)/4`.)

Conexão e medida em RNC a ordem K [DERIVADO do `gX1` do anexo, convenção `R_{acbd} = K(δ_{ab}δ_{cd} − δ_{ad}δ_{bc})`, que reproduz `Ric = 3K g` ✓]:

```
Γ^a_{bc}(y) = −(K/3)( y_b δ^a_c + y_c δ^a_b − 2 y^a δ_{bc} )     (zera em y=0; ∂Γ|₀ ≠ 0)
log √g(y)   = −(K/2) y·y ;   ∂^Y_j log √g = −K y_j ;   ∂²_jj' log √g|₀ = −K δ_{jj'}
```

---

## 3. A contração de Ward: fórmulas implementáveis (j=0 e j=1)

Com `k_{αβ} = 2∇_{(α} c_{β)}` e `B[h,k] = Σ_{i,j} ∫ dvol_X dvol_Y (D^i_X h)_A B^{A·(j)}_{ij}(X,Y) (D^j_Y k)`, a IBP em Y (covariante, `dvol = √g dy` absorvida por ∇; fronteiras fora do escopo) dá o operador sobre `c` **sem derivadas externas ocultas**:

### Caso j=0 (uma derivada movida: a do próprio vértice k)

```
B_{j=0}[h,c] = −2 ∫ (D^i_X h)_A [ ∇^Y_α B^{A(αβ)}_{i0} ](X,Y) · c_β(Y)  + fronteira
```

com a expansão da divergência:

```
∇^Y_α B^{Aαβ} = ∂B/∂y^α|_coef − 2 r_α (∂_w + w⁻¹∂_L) B
                + Γ^α_{ασ}(y) B^{Aσβ} + Γ^β_{ασ}(y) B^{Aασ}
```

(sinal da IBP: **−**; simetrização `(αβ)` absorvida pela contração.)

### Caso j=1 (duas derivadas movidas)

```
B_{j=1}[h,c] = +2 ∫ (D^i_X h)_A [ ∇^Y_α ∇^Y_γ B^{Aγ(αβ)}_{i1} ](X,Y) · c_β(Y)  + fronteiras
```

(sinal líquido **+** = (−1)².) Mantida a ordem natural das IBPs (γ primeiro, α depois), nenhum comutador é necessário; se a implementação reordenar, entrar

```
[∇_ρ,∇_σ] T^{abc} = R^a{}_{λρσ}T^{λbc} + R^b{}_{λρσ}T^{aλc} + R^c{}_{λρσ}T^{abλ},
R^a{}_{λρσ} = K(δ^a_ρ δ_{λσ} − δ^a_σ δ_{λρ})
```

que é O(K)·B₀ — **pertence à primeira ordem e não pode ser descartado**. A expansão em carta de `∇_α∇_γ B` gera ainda os **termos coincidentes da métrica**: `∂_ρ Γ^a_{bc}|₀ = −(K/3)(δ_{bρ}δ^a_c + δ_{cρ}δ^a_b − 2δ^a_ρδ_{bc})` multiplicando B₀, e `∂²log√g|₀ = −Kδ` se a IBP for feita em derivadas parciais.

### Onde recai cada derivada (a tabela pedida)

| alvo | conteúdo | ordem |
|---|---|---|
| propagador — parte radial | `±2r_α(∂_w + w⁻¹∂_L)` sobre `1/w, 1/w², L` | K⁰ e K¹ |
| propagador — coeficientes RNC | `∂_y` puro sobre `P1, distance1, gX1, gY1, S1` | K¹ (o que `dY=−dX` perde) |
| vértice de gauge (Y) | `k = sym∇c`: o Γ dentro de `∇_a c_b` dá termo ∝ Γ·c com **zero derivadas sobre c** (no anexo 2: `curve[yj]`/DG1); a derivada externa j=1 acrescenta um índice γ | K⁰ (fator `p_{yj}·G0`) e K¹ (`curve[yj]`) |
| fibra Y | Γ(y) nos índices contraídos e livres | K¹×B₀ |
| medida | `∂ log√g = −K y` (IBP parcial) | K¹ |
| métrica coincidente | `∂Γ|₀ ∝ K`, `∂²log√g|₀ = −Kδ` (só j=1) | K¹, local em Y |

No anexo 2 a perna fantasma não-integrada vive em `y_components(ny=1)` = `[(0,2, p[yj]·vec), (1,0, curve[yj])]`; a tarefa A-7.b é adicionar a **perna integrada**: o mesmo nó com o índice de derivação transferido ao kernel X e aos coeficientes, com o sinal `(−1)^{j+1}` e o `Err` do §2 no lugar do ingênuo `−p_xj`.

---

## 4. Fora da diagonal vs contatos de extensão (prescrição ancorada, intocada)

Todas as fórmulas acima valem **ponto a ponto para w ≠ 0** (a "identidade fora da diagonal"). Ao estender à diagonal pela família de Riesz `R(u) = FP_a[(1−a)μ^{2a} z^a u]`, os únicos contatos com **até duas derivadas** são [DERIVADO da família; a constante é a da carta, `C_E = −4π²`, não substituída]:

```
∂_j (1/w) = −2 x_j/w²                          (L¹_loc; SEM contato)
□ (1/w)   = C_E δ⁴(x)                          (o contato-mãe; verificado da família:
                                                4a(a+1)·res FP z^{a−1} → −4π² em a→−1)
∂_μ∂_ν (1/w) = FP[ −2δ_{μν}/w² + 8 x_μx_ν/w³ ] + (C_E/4) δ_{μν} δ⁴(x)
               (o traço reproduz □; isotropia SO(4) da prescrição fixa a forma tensorial)
∂^3+ de 1/w:  FP + derivadas de δ via □        (fora do escopo j ≤ 1)
```

Regra prática para o pipeline: derivada **primeira** do kernel singular é livre de contato; a **segunda** derivada com traço gera exatamente `(C_E/4)δ_{μν}δ⁴(X−Y)`. O `x^b/w` que aparece no §5 é `∼ 1/|x|`, L¹_loc em 4D, **sem** contato.

---

## 5. Um termo K não-nulo que `dY=−dX` perde (conta concreta)

Objeto: a **divergência Y do propagador fantasma de ordem K** do anexo 1 — `D₁^b(X,Y) := ∇^Y_a G₁^{ab}`, com `G₁^{ab} = P1^{ab}/w − distance1·δ^{ab}/w² + δ^{ab}/4 − 5δ^{ab}L/4`. Expansão pela regra de dois extremos [DERIVADO]:

```
∂^Y_a P1^{ab} = (y^b − 3x^b)/2 ;   ∂^X_a P1^{ab} = (3y^b − x^b)/2 ;   (∂^X+∂^Y) = −2 r^b ✓ (= Err contraído)
∂^Y_a distance1 = −(2/3)( xx·y^b − xy·x^b )
∂^Y_a(1/w) = 2r_a/w² ;  ∂^Y_a(1/w²) = 4r_a/w³ ;  ∂^Y_a L = −2r_a/w
```

**Avaliação na âncora, DEPOIS de diferenciar** (E5–E6 do §1; usando `P1(x,0) = (xx δ − XX^T)/6`, a anulação radial `x_a(xx δ^{ab} − x^a x^b) = 0`, `distance1(x,0) = 0`, `∂^Y distance1|₀ = 0`, `Γ(0)=0`):

```
regra certa (dois extremos):   D₁^b|_{Y=0} = −(3/2) x^b/w + 0 + (5/2) x^b/w =   x^b/w
regra proibida (−∂^X):         D₁^b|_{Y=0} = +(1/2) x^b/w + 0 + (5/2) x^b/w = 3 x^b/w
─────────────────────────────────────────────────────────────────────────────────
termo perdido pela substituição:  Δ = −2 x^b/w   (= Err_j P1 contraído, ancorado; Γ=0 na âncora)
```

Não-nulo, de classe `1/|x|`, integrável, sem contato — e é exatamente uma peça da **primeira quebra de Ward** que este A-7.b deve medir: é o que a hipótese `dY=−dX` esconderia dentro de um falso fator 3 no coeficiente. Conforme o pedido, este resto é **reportado, não cancelado** por contratermo.

---

## 6. Controle plano com sinais

Em K=0: `P1, distance1, gX1, gY1, Γ, ∂log√g → 0`; a regra colapsa a `∂^Y = −2r(∂_w + w⁻¹∂_L) = −∂^X` exato. Checagens:

1. Divergência fantasma plana: `∂^Y_a(δ^{ab}/w) = 2r^b/w² = −∂^X_a(δ^{ab}/w)` ✓ (sinais cruzados batem).
2. Sinal líquido da IBP j=0 seguida da troca plana de extremo: `(−1)·(−1) = +∇^X` — mover a derivada de Y para X no plano dá **sinal +**; j=1 dá `(+1)` de IBP dupla, e `(−1)²=+` de troca: qualquer implementação que produzir sinal ímpar no plano está errada.
3. Todo termo do §5 anotado K¹ morre em K=0; se o CAS produzir `x^b/w` residual com K=0, há contaminação de ordem errada.

## 7. Controle negativo verificável (o que deve FALHAR)

- **CN1:** rodar a divergência fantasma ordem K duas vezes — regra de dois extremos vs `dY=−dX`. A diferença na âncora **deve** ser `−2 x^b/w`. Se o pipeline reportar `0`, ele está aplicando a hipótese proibida em algum lugar (bug detectado pelo falsificador, não pelo olho).
- **CN2:** `(∂_x+∂_y) P1_{ab}` deve dar `(1/3)(r_jδ_{ab} − 2δ_{aj}r_b + r_aδ_{bj})`; se der `0`, o CAS tratou `P1` como função de `r` (bug de ancoragem).
- **CN3 (cruzado):** reescrever `P1` em `(r,s)` e tomar `2∂_s`: deve reproduzir CN2 termo a termo; discordância = erro algébrico na tabela de coeficientes.

## 8. Passos para o CAS (mapeamento aos anexos)

1. Reusar `derivative(f, side, j)` do anexo 1 **como está** — ela já é a regra certa; acrescentar fora dela: Γ-fibra (fórmula do §2), `∂log√g`, e (j=1) `∂Γ|₀`, comutador `R·B₀`.
2. No anexo 2, a perna integrada entra ao lado de `y_components`: para `ny=1`, substituir o ramo `(0,2, p[yj]·vec)` pela soma sobre os alvos da tabela do §3 (radial no propagador X com sinal trocado, `∂_y` dos coeficientes, `curve[yj]` do vértice preservado), e manter `transpose(BY)` do fantasma como está — a transposição do vértice ghost não é tocada pela IBP.
3. Executar `(E1)…(E4)`, separar FP/contato pela tabela do §4 com `C_E = −4π²` lido da carta, e **só depois** `w → (x−y)²`, `anchored(f)`.
4. Emitir o resto (quebra) como saída nomeada; proibido alimentá-lo a contratermos.

---

## 9. O que isto não faz / lacunas restantes

Não resolve loops, não fecha a identidade de Ward completa do par (falta a perna métrica `S1` contraída com os mesmos `Err` — a fórmula `Err_j S1` está pronta no §2 para implementação, mas não a expando aqui por delimitação), não deriva o vértice fantasma ordem 1 além do visível nos anexos (`word_value`/`AXES` não fornecidos), não fixa o prefator físico global dos kernels (a razão do §5 é insensível a ele), não toca a parte suave W nem escolhe estado. Todas as igualdades novas são **[DERIVADO manual / DECLARADO]**, com falsificadores CN1–CN3; a verificação exata independente (CAS +, quando couber, kernel) é pendência, não fato.