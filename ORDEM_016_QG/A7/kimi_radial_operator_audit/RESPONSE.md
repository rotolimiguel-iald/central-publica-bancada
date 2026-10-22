# ORDEM_016 · A7.b — Do perfil radial bilocal ao operador covariante autoadjunto sobre tensores simétricos (ordem K⁰ e K¹)

**Unidade:** bolha métrica bilocal com vértices derivados · uma chamada
**Estatuto global da resposta:** [DERIVED — regra e álgebra desenvolvidas neste texto, checáveis por álgebra exata] com [KNOWN] (RNC, Weitzenböck, Lichnerowicz, Hadamard), [DECLARADO] (coeficientes do pipeline e convenções) e [OPEN] (auditoria local pendente). **Não se alega:** execução dos engines anexados, confirmação física, alteração de kernel ou de gate, prova do setor curvo. Os coeficientes numéricos do perfil (cinco p⁴, quatro Kp²) **não foram anexados** a esta chamada; a regra é dada sobre as classes de estrutura, e preenchê-los é passo do pipeline, não desta resposta. Restrições do operador honradas: Ward = 0 e transversalidade **não** são impostos à bolha isolada; nenhum coeficiente é escolhido por Ward; a fonte BV curva não é tratada como gauge pura; L = log z é mantido simbólico.

---

## 1. O dicionário local: RNC em curvatura constante K, com coeficientes exatos

Espaço-forma euclidiano 4D: R_{abcd} = K(g_{ac}g_{bd} − g_{ad}g_{bc}), Ric = 3Kg, R = 12K, ∇R = 0. Em coordenadas normais geodésicas (RNC) centradas em Y = 0, com z = |X|² = x_a x^a:

```
g_μν(x)   = δ_μν − (K/3)(z δ_μν − x_μ x_ν) + O(K²)                      [KNOWN]
e^a_μ(x)  = δ^a_μ − (K/6)(z δ^a_μ − x^a x_μ) + O(K²)                    [DERIVED — checar eᵀe = g]
(e⁻¹)^μ_a = δ^μ_a + (K/6)(z δ^μ_a − x^μ x_a) + O(K²)
√g(x)     = 1 − Kz/2 + O(K²)          (det g = 1 − Kz; tr(zI − xxᵀ) = 3z)
```

**Momento eikonal.** A fase φ(X) = −p·x (p covector constante nas coordenadas; A(X) = A₀ e^{−ipX}, B(Y) = B₀ e^{+ipY}) lida no tetrad dá

```
p_X(x) = (e⁻¹)·(−p) = −p − (K/6)(z p − x(p·x)) + O(K²)                [DERIVED]
```

— confere com o anexo (`p_X = −p − K(zI − xx)p/6`, PROXIMO l.14) e com o fator 1/6 embutido no denominador do `position_metric_bubble_engine.py` (wp6, denominador `6·d0·d0`).

**Conexão de frame.** Do Christoffel RNC Γ̃^μ_{iν} = −(K/3)(δ_{μi}x_ν + δ_{μν}x_i − 2x_μδ_{iν}) [KNOWN, conferido aqui por diferenciação direta de g_μν] segue

```
(Γ_i)_{ab}(x) = (K/2)(x_a δ_{ib} − x_b δ_{ia}) + O(K²)                 [DERIVED]
```

antissimétrica em (ab) (rotação infinitesimal do tetrad), linear em x, O(K). Atuando num tensor simétrico: (Γ_i·A)_{cd} = (Γ_i)_c{}^e A_{ed} + (Γ_i)_d{}^e A_{ce}. O fator 1/2 é o denominador `2` do termo wc2 no engine (l.152). O numerador de momento se decompõe como

```
−i∇^cov = p_X − iΓ^frame + (derivação de fibra de base)               [DERIVED — a regra de leitura]
```

isto é: **fase** (p_X, jatos F3) e **fibra** (Γ, jatos F4) são separadas pelo cálculo radial e re-compõem a ∇ covariante — identidade [KNOWN]: em frame ortonormal, derivada de frame + conexão de spin = derivada covariante total.

---

## 2. A regra calculável em cinco passos

### Passo 0 — dados e normalizações [DECLARADO — lidos dos anexos]

Dois propagadores por bolha: denominadores `d0 = 2z³` (G0, plano) e `d1 = 24z²` (G1 e GL, ordem K); retorno de `contracted_node` já multiplicado por `z²/16` (normalização rawbubble/A0 = angularmean/16); strip global de `4κ/(4π²)`; rótulos de derivada = rótulos tangentes ortonormais, um em cada ponta; vértices Γ–Γ com ≤ 1 derivada por campo (matrizes 50×50: 5 posições (d = −1, 0..3) × 10 componentes de fibra).

### Passo 1 — média angular em S³(v), z = v² [DERIVED — checável]

```
⟨x_i x_j⟩       = v² δ_ij / 4
⟨x_i x_j x_k x_l⟩ = v⁴ (δ_ijδ_kl + δ_ikδ_jl + δ_ilδ_jk) / 24
⟨x_{i1}···x_{i2m}⟩ = v^{2m} / (2ᵐ (m+1)!) · Σ_{pareamentos} δδ···δ
```

Monômios ímpares anulam. Cota de grau a provar/medir **antes** da cubatura [DECLARADO, do anexo]: ≤ 8 no plano, ≤ 6 em ordem K. Avaliar em nó inteiro v e multiplicar por z² dá o valor na esfera sem raízes (anexo l.28). **Controle de paridade:** o perfil final deve ser par em p (simetria X↔Y da bolha); todo monômio residual p-ímpar (Kp¹, Kp³) indica erro de implementação, não física — ver §5, controle escalar, onde o cancelamento é explícito.

### Passo 2 — bases de estruturas bilineares [DERIVED]

Sobre tensores simétricos, as formas bilineares isotrópicas simétricas em (A ↔ B):

```
p⁴ (cinco):   E1 = p⁴ A_ab B^ab
              E2 = p² (p·A)_c (p·B)^c
              E3 = (pp·A)(pp·B)
              E4 = p² [(pp·A) trB + (pp·B) trA]
              E5 = p⁴ (trA)(trB)

Kp² (quatro): F1 = K p² A_ab B^ab
              F2 = K (p·A)_c (p·B)^c
              F3 = K [(pp·A) trB + (pp·B) trA]
              F4 = K p² (trA)(trB)

Kp⁰ (dois):   C1 = K A_ab B^ab        ← ordem zero; ver §3, decisão
              C2 = K g_ab trA trB ... (C2 = K (trA)(trB))
```

### Passo 3 — dicionário p → −i∇^cov, com a ordem de derivadas explicitada [DERIVED]

Cada monômio é convertido na **convenção de ordenação OS** [DECLARADO — convenção desta unidade, não teorema]: repartição simétrica de derivadas (2+2 para p⁴; 1+1 para Kp²), adjunção formal exata por construção. Os operadores (símbolo principal de **4ª ordem**, subprincipal K de **2ª ordem**, ordem zero K):

```
E1 → D1 B_ab = ∇⁴ B_ab                      (∇⁴ := (∇²)²; autoadjunto: ∇² o é)
E2 → D2 B_ab = ½[∇_a ∇² (∇^c B_cb) + ∇_b ∇² (∇^c B_ca)]
E3 → D3 B_ab = ∇_a ∇_b (∇^c ∇^d B_cd)
E4 → D4 B_ab = ½[∇_a∇_b ∇²(trB) + g_ab ∇²(∇^c∇^d B_cd)]
E5 → D5 B_ab = g_ab ∇⁴ (trB)

F1 → K ∇² B_ab
F2 → (K/2)[∇_a (∇^c B_cb) + ∇_b (∇^c B_ca)]
F3 → (K/2)[∇_a∇_b (trB) + g_ab (∇^c∇^d B_cd)]
F4 → K g_ab ∇² (trB)

C1 → K B_ab
C2 → K g_ab (trB)
```

Cada D_i, F_i é formalmente autoadjunto **verificável por IBP** (regra IBP2 abaixo); dentro de um termo já O(K), os comutadores custam O(K²) e estão fora do escopo. Autoadjunteza exata dos D_i em ordem K: ver §3.

### Passo 4 — regra das quatro fontes de ordem K, com jatos de Taylor e fatores [DERIVED, casado com os engines]

A ordem K do perfil vem de quatro origens **fisicamente distintas, a manter separadas até o fim**:

| fonte | objeto | regra de Taylor | fator | conferência no engine |
|---|---|---|---|---|
| F1-prop | jatos K dos dois propagadores (G1) | j = N−2, coef (−1)^{N−1}(p·x)^{N−2}/(N−2)! | 1 | `curve`, termo `frob(C1,VY)` |
| F2-vol | √g_X = 1 − Kz/2 | j = N−2 | −z/2 | `curve`, termo `−F(z·c0, 2 d0 d0)` |
| F3-coframe | p_X = −p − (K/6)(zp − x(p·x)) | j = N−2 | 1/6 | wp6, denominador `6·d0·d0` |
| F4-conexão | −iΓ^frame, Γ linear em x | j = N−1, coef (−1)^N(p·x)^{N−1}/(N−1)! | 1/2 (∝ K/2) | wc2, denominador `2·d0·d0` |

com N = N_X + N_Y (derivadas externas nas duas pontas; aqui N ∈ {2,3,4} com ≤ 2 por ponta). **Regra de leitura externa (J2):** toda “divergência” do cálculo radial é derivada de frame; a conversão a ∇^cov absorve Γ — mas como o cálculo separa fase e fibra, **os jatos de conexão entram obrigatoriamente com j = N−1** (uma potência de p a menos que a fase correspondente). É por isso que a conexão afeta o **subprincipal** (ver §3).

### Passo 5 — adjunção e integração por partes [DERIVED]

```
IBP1: ∫ √g A(∇_i X) = −∫ √g (∇_i A) X          (sem borda; contatos/borda = outras unidades)
IBP2: (M ∇ⁿ)† = (−1)ⁿ ∇ⁿ Mᵀ  (na fibra)
IBP3: [∇², ∇ᵏ] = k·K·∇ᵏ⁻¹ + estruturas Riem (tabela pelo exemplo, §3.2)
Adjunção: 𝔓_final = ½(𝔓_repr + 𝔓†_repr), com 𝔓_repr na ordenação OS declarada.
```

Termos de conexão externos, ao IBP, propagam Γ entre as pontas; como Γ = O(K), cruzamentos Γ×Γ são O(K²) — fora. A convenção OS é **declarada antes de comparar coeficientes**: outra ordenação desloca b_i e c_i por quantidades exatas (exemplo em §3.2).

---

## 3. Decisão: os quatro coeficientes Kp² bastam? — **Não.**

### 3.1 Jatos que faltam [DERIVED; a decisão]

**J1 (obrigatório) — jatos Kp⁰ (ordem zero).** O operador tem dois coeficientes de ordem zero em K (C1, C2 da §2, Passo 2) que **não são determinados pelos quatro monômios Kp²**. Eles vêm do mesmo `contracted_node`, na parcela `curve` com n = 2 (Taylor (p·x)⁰): dos jatos G1 dos propagadores, do volume (−z/2 × plano com j = 0) e do coframe (wp6 com n = 2). Sem J1, a matriz de fibra de ordem zero fica indeterminada e a autoadjunteza formal exata do operador de 4ª ordem em ordem K não pode nem ser enunciada: reordenar os D_i (p⁴) produz, via comutadores, termos F (Kp²) **e** C (Kp⁰). Extração: repetir a contração guardando os coeficientes de grau total 2 (não só 4) em ordem K — o engine já os computa; basta não descartá-los.

**J2 (obrigatório) — jatos da leitura externa/divergência.** O símbolo subprincipal com divergências (F2, F3) é sensível à conversão frame → covariante: os jatos Γ^frame·B **sem potências de p** alimentam C1, C2 (via regra de leitura do Passo 4), e os jatos com um p alimentam F2/F3. Os quatro Kp² “obtidos assim” incluem F4-conexão, mas a **decisão sobre o que é divergência covariante vs. termo de ordem zero** exige J1 + a regra de leitura aplicada consistentemente; sem isso, b₂ e b₃ misturam origens.

**J3 (controle) — jatos ímpares Kp¹, Kp³.** Devem anular por paridade (Passo 1). Não anulando, o defeito é de implementação (medida, média angular ou contagem de Taylor), a corrigir antes de qualquer coeficiente.

**J4 (declarado fora de escopo) — K²p⁰, parte finita/estado/cutoff** (anexo l.36): devidos depois; não cobertos por esta regra.

### 3.2 Exemplo concreto, checável por álgebra exata [DERIVED]

Seja o deslocamento de ordenação (3,1) → (2,2) no símbolo principal: D := ∇_a ∇² T_b vs D′ := ∇² ∇_a T_b, com T_b = ∇^c B_{cb}. Comutador vetorial em curvatura constante [KNOWN Weitzenböck + DERIVED os coeficientes]:

```
[∇², ∇_μ] A_ν = −6K ∇_μ A_ν + 2K (g_{μν} ∇·A − ∇_ν A_μ)
```

(cheque: −R_μ^λ∇_λA_ν = −3K∇_μA_ν, −R_ν^λ∇_μA_λ = −3K∇_μA_ν, 2R^λ{}_μ{}^σ{}_ν∇_λA_σ = 2K(g_{μν}∇·A − ∇_νA_μ) — soma confere). Aplicado a D − D′ = [∇_a, ∇²]T_b:

```
D − D′ = 6K ∇_a(∇^c B_cb) − 2K g_ab (∇^d∇^c B_dc) + 2K ∇_b(∇^d B_da)
       = 6K·(F2) − 2K·(F3, 2ª peça) + 2K·(F2′ + O(KB))
```

**Leitura:** trocar a ordenação do símbolo principal desloca os coeficientes de F2 e F3 por inteiros exatos (6, −2, 2). Logo: (i) os quatro Kp² só têm significado **depois** de declarada a ordenação; (ii) a mesma mecânica, na ordem seguinte, alimenta C1/C2 — confirmando J1 como dado independente obrigatório. Versão tensorial do comutador (também checável):

```
[∇², ∇_a] B_cd = −3K∇_a B_cd − K∇_c B_ad − K∇_d B_ac
                  + K(g_ac (∇·B)_d + g_ad (∇·B)_c)          (curvatura constante)
```

---

## 4. Prescrição de extensão: símbolo radial, resíduo log, parte finita

Separar o integrando (após média angular, em nó v, dvol = 2π²v³dv, z = v²) como

```
u(v) = Σ_n u_n(p,K) v^{−n} + Σ_n ℓ_n(p,K) v^{−n} L,   L = log z (simbólico, NUNCA apagado)
```

A prescrição anexada FP_a[(1−a)μ^{2a} z^a u] desenvolve, para o termo log-divergente u = c·v^{−4} [DERIVED — leitura da prescrição]:

```
∫₀^Λ 2π² (1−a) μ^{2a} v^{2a−1} c dv = 2π² c (1−a) e^{2a ln(μΛ)} / (2a)
       = 2π²c [ 1/(2a) + ln(μΛ) − 1/2 + O(a) ]
```

Separação declarada:

- **polo (resíduo de divergência):** 2π²c/(2a) — a contraparte do contratermo; não é parte finita nem log físico;
- **resíduo log:** 2π²c·ln(μΛ) — carrega log μ² e, recomposto com a dependência local, a forma c·log(μ²z). **Os termos ℓ_n·L produzem polos duplos** (d/da do polo simples) e logs cruzados — exatamente o aviso do anexo (l.29–30). **Proibição registrada:** nenhum termo L pode ser apagado à bolha isolada; o cancelamento (se houver) é teste da **soma** com tadpole/ghost/fonte antifield — outras unidades. L fica simbólico até lá;
- **parte finita:** o perfil radial polinomial em p (os coeficientes dos monômios, que viram o operador diferencial) **mais** a convenção da prescrição (−1/2 por polo simples, oriunda do fator (1−a)) **mais** termos u_0 integrados. A convenção é [DECLARADO]: variantes dela movem a parte finita, **não** o resíduo log nem os polos.

O **símbolo radial** é, por definição aqui, o conteúdo analítico-polinomial em p do perfil após média angular: {cinco p⁴, quatro Kp², dois Kp⁰} — é ele que o dicionário da §2 converte em operador. Resíduo log e parte finita não-algébrica **não** entram no operador diferencial local; entram na forma efetiva (resíduo log → termos log(−∇²/μ²); parte finita → ambiguidade de esquema, a isolar na soma das unidades).

---

## 5. Controles escalar / vetorial / tensorial (checáveis à mão)

**Escalar (fluxo completo).** Bolha com vértices de uma derivada, propagador H = (1/4π²z)(1 + c_K Kz) com c_K **simbólico** [DECLARADO — o jato exato é Hadamard/KNOWN, desnecessário à demonstração]. Plano: ∂H∂H × Taylor j=2 → média ⟨x_ix_j⟩ = zδ_ij/4 → B_flat = p²/(2z³). Ordem K: (i) duas pernas: 2c_K·Kz × (j=0) → +2c_K K/z²; (ii) volume: −(Kz/2) × (j=0) → −K/(2z²); (iii) coframe: termo ∝ −(K/6)zp_j × ⟨x_ix_j⟩ → −K p_i/(6z²) de uma perna e **+K p_i/(6z²)** da outra (sinais de fase opostos) → **cancela** (controle J3 ✓); (iv) conexão: ausente. Resultado: B = p²/(2z³) + (2c_K − 1/2)K/z² → operador **−∇² + (2c_K − 1/2)K**. Demonstra: o coeficiente Kp⁰ do perfil **é** o termo de massa do operador e **não** vem dos monômios Kp² — J1 é indispensável, no brinquedo e em geral.

**Vetorial:** o comutador da §3.2 (coeficientes −6K, +2K) — checável pela decomposição de Weitzenböck em duas linhas.

**Tensorial (âncora KNOWN):** Lichnerowicz em curvatura constante:
Δ_L h_ab = −∇²h_ab − 2R_{acbd}h^{cd} + R_{ac}h^c{}_b + R_{bc}h^c{}_a = **−∇²h_ab + 8K h_ab − 2K g_ab (tr h)**.
Ou seja, um operador físico canônico usa exatamente C1 e C2 com coeficientes (8, −2) — qualquer mapeamento que determine só os quatro Kp² perde esse conteúdo. Checável por substituição direta de R_{acbd} = K(g_{ab}g_{cd} − g_{ad}g_{cb}) e Ric = 3Kg.

---

## 6. Lacunas e pendências declaradas

1. **Coeficientes concretos do perfil** (cinco a_i, quatro b_i, dois c_i): **não anexados** a esta chamada — [DECLARADO]; a regra é simbólica; o preenchimento exige rodar o pipeline e a auditoria local. Validação prévia obrigatória [do anexo]: **plano contra `metric_bubble_v2` antes da curva**; os resultados locais curvos não anexados preservam a independência — o setor K=0 comparado a momentos **não** é usado aqui como prova do setor curvo.
2. **Jatos Kp⁰ (J1):** a extração está no engine (parcela n = 2 de `curve`), mas sua tabulação e conferência são passo do pipeline — [OPEN].
3. **Interpretação da prescrição FP** (fator (1−a), convenção −1/2 na parte finita): leitura [DERIVED] do enunciado; variantes movem só a parte finita — a isolar na soma das unidades.
4. **IBP sem borda:** contatos e termos de superfície pertencem às unidades de contatos BV — fora deste escopo.
5. **K², estado/vácuo, cutoff físico, soma com calor livre/tadpole quártico/fonte antifield/ghost/contatos BV:** devidos depois (anexo l.36 e enunciado); o resíduo Ward da bolha isolada é esperado (a fonte BV curva não é puramente gauge) e **não** foi zerado nem usado para escolher coeficientes.
6. **Não executado nesta chamada:** nenhuma rodada dos engines; toda a álgebra é derivada no texto e checável; nenhum hash, prova, medida ou veredito novo foi produzido; kernel e gate intocados.

**Síntese [DERIVED]:** a regra é — RNC em curvatura constante com os coeficientes exatos (e = 1 − KM/6, √g = 1 − Kz/2, p_X = −p − K(zp − x(p·x))/6, Γ_i = (K/2)(x∧δ)_i); média angular com paridade; bases E1–E5 / F1–F4 / C1–C2; dicionário p → −i∇^cov com fase e fibra separadas e quatro fontes de K com seus jatos de Taylor (N−2, N−2, N−2, N−1) e fatores (1, 1/2, 1/6, 1/2); ordenação OS declarada + adjunção ½(𝔓+𝔓†); FP com símbolo radial / resíduo log / parte finita separados e L jamais apagado. **Decisão:** os quatro Kp² **não bastam** — faltam os jatos Kp⁰ (J1, duas estruturas de fibra), os jatos de divergência/leitura externa que alimentam ordem zero e subprincipal (J2) e os controles de paridade (J3); exemplos concretos dados e checáveis.