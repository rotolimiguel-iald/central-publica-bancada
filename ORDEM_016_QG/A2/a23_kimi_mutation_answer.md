# A2.3.a — Controle adversarial do `halfline_isotony` novo

Leitura feita sobre as cinco fontes custodiadas (`LightRayGaussianDensity_v2`, `LightRayGaussianOrthogonality_v2`, `LightRayDensitySeparation_v2`, `LightRayCoreExtension_v2`, `LightRayGaussianTransform_v5`) e sobre os dados matemáticos declarados na ordem. **Estatuto da minha leitura:** a evidência de compilação (rc0, axiomas no trio) é da bancada, não minha; não compilei, não executei, não escrevi arquivo, não movi gate. Onde a fonte não mostra o corpo de um lema (`product_core_mem_rapidity_standard`, `rapidityStandardSubspace`, os lemas de unicidade em `LightRayRealFourierUniqueness_v2`), a leitura é estrutural, ancorada na assinatura tipada e nos dados declarados (norma `exp(−a e^ξ sin y)`, torção `m_a(ξ+iπ)=conj m_a(ξ)`, `c=2πw`). Isso é dito aqui uma vez e vale para tudo abaixo.

---

## 1. O que a unidade acrescenta, e o alcance exato do teorema

**O que é novo, de fato, nesta unidade** (não é repetição da auditoria anterior):

1. **A densidade real virou teorema** (`gaussian_core_real_dense`, linhas 16–41): antes havia totalidade complexa; agora `K ⊆ closure(span_ℝ {productCore 0 b r})`, por projeção ortogonal real (`starProjection` sobre `ClosedSubmodule ℝ`) composta com a separação (`gaussian_core_real_orthogonal_separates`, linhas 46–56 de `Orthogonality_v2`), que por sua vez descansa no peso espectral **positivo** gaussiano (`gaussian_spectral_positive`) com reflexão correta (`gaussian_spectral_reflection`) e na unicidade de Fourier real (`weighted_real_fourier_separates_standard`). A perna que essa densidade pisa é a **positividade do peso** — é ela que carrega o "separa" em `weighted_real_fourier_separates_standard` (linha 68: `mul_eq_zero` resolve a favor de `H=0` porque `g p ≠ 0`).
2. **`halfline_isotony` sem `hdensity`** (linhas 44–48): a hipótese de densidade que `halfline_isotony_of_gaussian_density` (linhas 36–51 de `CoreExtension_v2`) ainda declara explicitamente é descarregada pelo teorema de densidade. A prova de isotonia é: transporte algébrico nos núcleos (`U_gaussian_core`: `U a (productCore 0 b r) = productCore a b r`) + pertença dos núcleos transportados (`product_core_mem_rapidity_standard a b r ha hb`) + `C := K.comap (U a)` fechado + `closure_minimal`. A `comap` é o ponto técnico correto: em vez de empurrar o closure por `U a`, puxa-se `K` pelo mapa e usa-se minimalidade.

**Alcance exato da conclusão:**

```
halfline_isotony : ∀ (a : ℝ), 0 ≤ a → ∀ f ∈ K → U a f ∈ K,
   K := (rapidityStandardSubspace (2·π²)).toClosedSubmodule
```

Ou seja: **invariância do subespaço padrão real pelo semigrupo {U(a)}_{a≥0}, na largura π**. Nada mais. Em particular, o teorema **não** afirma:

- a lei de grupo modular `Δ^{it} U(a) Δ^{-it} = U(e^{−2πt} a)` (a face de Borchers da meio-lateralidade) — ausente do enunciado;
- qualquer álgebra de von Neumann, localidade ou rede — o objeto é um subespaço de Hilbert real;
- isotonia bilateral (`a ≤ 0`) — nem como corolário (ver Probe 1);
- a unicidade da largura — **o alvo A2.3.d não é pago por esta unidade nem pelos probes abaixo**, e não deve ser promovido por nomenclatura: provar que "a proposição com `w=π/2` é falsa" (Probe 2) não é provar que "π é a única largura física"; são enunciados diferentes.

---

## 2. Onde as hipóteses moram — os dois mecanismos independentes

A pertença a `K` tem duas pernas logicamente independentes, e é isso que define o desenho dos controles. No lado espectral, `K_c = Fix(J T_c)` com `T_c = M_{e^{−cp}}`, `J H(p) = conj H(−p)`; no lado rapidez (via `F`, convenção `e^{−2πiξp}`, deslocamento `F[f(·+iy)] = e^{−2πyp} Ff`, logo `c = 2πw`):

- **Perna A — domínio ponderado:** `f ∈ dom(T_c)`, i.e. `e^{−cp}·Ff ∈ L²`; na face da faixa, `f` admite extensão analítica a `0 < Im z < w` com fatias `L²`. O multiplicador tem norma `|m_a(ξ+iy)| = exp(−a e^ξ sin y)`, que é **contração na faixa `0 ≤ y ≤ π` sse `a ≥ 0`**. Para `a < 0`, `|m_a(ξ+iy)| = e^{|a| e^ξ sin y}` explode duplamente exponencialmente em `ξ→+∞` para todo `y ∈ (0,π)`, e o decaimento gaussiano `e^{−bξ²}` do núcleo **não** resgata. É aqui que `ha : 0 ≤ a` é gasta — não na álgebra do transporte (que vale para todo `a`), mas na integrabilidade.
- **Perna B — ponto fixo (torção de borda):** `f(ξ+iw) = conj f(ξ)` a.e. O multiplicador satisfaz `m_a(ξ+iy) = conj m_a(ξ)` sse `e^{iy} = −1` (para `a ≠ 0`), i.e. **somente em `y = π (mod 2π)`** — e já em `y=π/2` a falha é visível *na norma*: `|m_a(ξ+iπ/2)| = e^{−a e^ξ} ≠ 1 = |conj m_a(ξ)|`. É aqui que a largura `π` (`c = 2π²`, hard-coded na fonte) é gasta.

Leitura geométrica (declarada como leitura, não como teorema novo): a faixa de altura π é a meia-travessia de Tomita (`Δ^{1/2}` ↔ deslocamento `iπ` na normalização do boost), e as duas condições se saturam num ponto único — a torção exige `w ∈ π + 2πℤ`, a contração exige `w ≤ π`, interseção `{π}`. O teorema está travado na geometria modular correta; os probes abaixo verificam que ele **carrega** essa travessia (que `0 ≤ a` e `w = π` são hipóteses de verdade, não apenas de prova).

Nota pedida pela ordem: **`a = 0` é identidade** (`U 0 = id`, `multiplier 0 = 1`), logo um "controle" com `a=0` passa trivialmente e é vacuoso. O controle de sinal usa `a < 0`.

---

## 3. Os três probes não-vacuosos

### PROBE 1 — sinal: `U(−1)` tira o núcleo de `K` (falha na Perna A, com a Perna B intacta)

- **Proposição-alvo (bem formada):** `U (-1) f₀ ∈ K`, onde `f₀ := productCore 0 1 0 le_rfl zero_lt_one` — o núcleo gaussiano puro (`multiplier 0 = 1`), que **existe** como termo (a restrição `0 ≤ a` vive nos lemas de pertença, não no operador `U`, que é multiplicação por fase unitária para todo `a : ℝ`). A proposição é falsa; o probe prova `¬ (U (-1) f₀ ∈ K)` ou, na versão numérica, mede a divergência.
- **Ponto matemático que deve falhar:** a pertença ao **domínio ponderado**. A torção *não* falha: `e^{iπ} = −1` independentemente do sinal de `a`, logo `m_{−1}(ξ+iπ) = conj m_{−1}(ξ)` vale e a borda fecha. O que morre é a integrabilidade da faixa — e isso separa as pernas.
- **Testemunha e a conta (uma linha):** na fatia `y = π/2`, `|m_{−1}(ξ+iπ/2)| = e^{+e^ξ}` (pois `sin(π/2)=1`, `a=−1`) e `|f₀(ξ+iπ/2)|² = e^{−2ξ²}`. Integrando da norma ao quadrado: `e^{2e^ξ − 2ξ²} ≥ e^{e^ξ}` para `ξ ≥ 3` (porque `e^ξ ≥ 2ξ²` para `ξ ≥ 3`, com razão crescente). O integrando **não tende a zero**; a norma da fatia diverge. Logo `U(-1) f₀` não admite a extensão de faixa com fatias `L²` que a pertença a `dom(T_{2π²}) ⊇ K` exige.
- **Dependência tipada (declarada para a bancada):** a ponte "faixa diverge ⟹ `∉ dom(T_c)`" é uma direção de Paley–Wiener de faixa (`e^{−cp}Ff ∈ L² ⟹` extensão analítica com fatias `L²`); a cadeia compilada provou a direção *contrária* (núcleos têm faixa, logo estão no domínio). Se essa direção reversa não estiver na árvore, o Probe 1 formal nasce condicionado a ela — a alternativa é a análise direta de `e^{−2π²p}·F[U(−1)f₀] ∉ L²` (mais pesada). A **versão numérica** (norma da fatia `y=π/2` crescendo sem limite sob truncamento, contra a mesma fatia finita para `U(+1) f₀`) não depende de lema nenhum e já morde. O ponto tipado que *recusaria* a prova ingênua é `product_core_mem_rapidity_standard (-1) 1 0 ha hb` com `ha : 0 ≤ −1` — mas essa recusa é S1 (ver §4), **não** é o probe.
- **O que distingue:** que `0 ≤ a` é hipótese da *verdade*, não só da prova — a conclusão é falsa sem ela, com testemunha explícita. E que a isotonia é genuinamente *meio*-lateral: se valesse para `a<0`, o grupo inteiro preservaria `K` e o teorema seria outro (e errado). O sinal é o conteúdo físico (energia positiva ↔ semigrupo); o probe documenta que a prova não prova demais.

### PROBE 2 — largura `π/2`: `U(1)` tira o núcleo de `K_{π²}` (falha na Perna B, com a Perna A intacta)

- **Proposição-alvo:** o análogo do teorema com `K' := rapidityStandardSubspace (π²)` (largura `w = π/2`, `c = 2πw = π²`). **Testemunha do lado de dentro:** `g₀(ξ) = exp(−(ξ − iπ/4)²)` — o núcleo torcido na meia-altura da nova largura. Ponto fixo: `g₀(ξ+iπ/2) = exp(−(ξ+iπ/4)²) = conj g₀(ξ)` ✓; domínio: a transformada é gaussiana com inclinação `e^{π²p/2}` e `e^{−π²p}·Fg₀` decai ✓. Logo `g₀ ∈ K'`.
- **Ponto matemático que deve falhar:** a **equação de ponto fixo** para `U(1) g₀`. Com `e^{iπ/2} = i`: `m_1(ξ+iπ/2) = e^{−e^ξ}` (real positivo), enquanto `conj m_1(ξ) = e^{−i e^ξ}`. Já em `ξ=0`: `e^{−1} ≈ 0,368` contra `e^{−i} ≈ 0,54 − 0,84i` — e por norma: `e^{−e^ξ} ≠ 1 = |conj m_1(ξ)|` para todo `ξ`. Então `(U 1 g₀)(ξ+iπ/2) = e^{−e^ξ}·conj g₀(ξ) ≠ e^{−ie^ξ}·conj g₀(ξ) = conj((U 1 g₀)(ξ))`. A borda **não** fecha: `U 1 g₀ ∉ Fix(J T_{π²})`, portanto `∉ K'`.
- **E a Perna A sobrevive (é o que torna este probe ortogonal ao Probe 1):** na faixa `0 < y < π/2`, `sin y ≥ 0`, `|m_1| ≤ 1`, as fatias de `U(1)g₀` são `L²` — `U(1) g₀ ∈ dom(T_{π²})`. O domínio passa e o ponto fixo morre. Equação pontual entre funções explícitas, avaliável sem infraestrutura nova além da parametrização em `c`.
- **Dependência tipada:** a fonte hard-coda `2*Real.pi^2` (linhas 17, 37, 45); o probe exige a versão parametrizada dos lemas de pertença/balanço (a família `continuous_standard_fixed_iff`, `continuous_standard_balance` já é parametrizada em `c` — linhas 15–20 de `DensitySeparation_v2` — o que favorece a generalização). O ponto tipado que falha é o análogo de `product_core_mem_rapidity_standard` para `c = π²` **aplicado a `U(1)g₀`** — não na formação do termo, mas na *prova* da equação de borda.
- **O que distingue:** que a largura `π` é hipótese da *verdade* — a mesma prova, na largura errada, tem conclusão falsa com testemunha explícita; e que a Perna B é conteúdo real independente da Perna A.

### PROBE 3 — largura `3π/2`: falha dupla (Perna B na borda, Perna A na faixa alta)

- **Proposição-alvo:** o análogo com `K'' := rapidityStandardSubspace (3π²)` (`w = 3π/2`). **Testemunha do lado de dentro:** `h₀(ξ) = exp(−(ξ − 3iπ/4)²)`; ponto fixo na altura `3π/2`: `h₀(ξ+3iπ/2) = exp(−(ξ+3iπ/4)²) = conj h₀(ξ)` ✓.
- **Pontos que falham (dois, e é essa a informação):** (i) **Torção na borda:** `e^{3iπ/2} = −i`, logo `m_1(ξ+3iπ/2) = e^{+e^ξ}` (real, norma `e^{e^ξ} ≠ 1`) `≠ conj m_1(ξ)` — o ponto fixo morre como no Probe 2. (ii) **Integrabilidade na faixa:** a faixa `0 < y < 3π/2` atravessa a região `y ∈ (π, 3π/2)` onde `sin y < 0`, e aí `|m_1(ξ+iy)| = e^{e^ξ |sin y|}` explode em `ξ→+∞` — e.g. na fatia `y = 5π/4`, `|m_1|²·|h₀|² ≥ e^{√2·e^ξ − 2ξ²}`, divergente. Logo `U(1) h₀` falha **as duas** pernas.
- **O que distingue (além de cumprir a alternativa da ordem):** que as duas pernas têm *regiões de falha distintas* no espaço `(a, w)` — em `w < π` morre só a borda; em `w > π` morrem borda e faixa; em `a < 0` com `w = π` morre só a faixa. O mapa das falhas é o desenho exato do alcance do teorema: **`(a ≥ 0) ∧ (w = π)` é o ponto único onde as duas pernas podem valer juntas** — sem que isso seja A2.3.d (que fala de unicidade da escolha física, outro enunciado, segue aberto e não promovido).

---

## 4. A pergunta sobre o teste superficial — sim, seria superficial, e aqui está por quê

Uma "aplicação do teorema antigo a tipos incompatíveis" falharia por **três modos de superficialidade**, nenhum dos quais toca a proposição:

- **S1 — recusa na produção da hipótese:** `halfline_isotony (-1) h ...` com `h : 0 ≤ -1` — `norm_num`/o elaborador recusa a *prova da hipótese*. Nada se segue sobre `U(-1) f₀ ∈ K`.
- **S2 — falha de formação do alvo:** `U_gaussian_core (-1) b r ha hb` exige formar `productCore (-1) b r ha hb` (linha 26–27 de `CoreExtension_v2`), que pede `ha : 0 ≤ -1` — a *equação* nem é um termo bem formado.
- **S3 — mismatch de constante/objeto:** o teorema fala de `rapidityStandardSubspace (2π²)`; "aplicá-lo à largura π/2" não é uma aplicação — é outro enunciado sobre outro objeto, que não existe para ser recusado.

E a régua da ordem, aplicada: **falha de compilação de argumento não é prova de falsidade da proposição.** Em S1/S2, a proposição `U(-1) f₀ ∈ K` está *bem formada* (`U` aceita todo `a : ℝ`; `K` aceita todo vetor) e é **falsa** — mas quem estabelece isso é o Probe 1 (testemunha + divergência da norma de faixa), não a recusa do elaborador, que é muda sobre ela. A tipagem `0 ≤ a` nos lemas é conservadora por construção (a prova usa a contração); só o probe com contra-testemunha separa "hipótese necessária à prova" de "hipótese necessária à verdade". Os Probes 1–3 são enunciados bem formados, com testemunhas e pontos de falha nomeados — é isso que os torna controles, e não exercícios de elaboração.

---

## 5. Declarado fora do alcance dos probes

- Os probes **não pagam A2.3.d** (unicidade da largura): eles refutam o teorema *em outras larguras*, o que é mais fraco que provar unicidade física da escolha. Não promover por nomenclatura.
- Não tocam a lei de grupo modular `Δ^{it} U(a) Δ^{−it} = U(e^{−2πt} a)`, nem constroem álgebra/localidade — o objeto segue sendo o subespaço padrão real.
- A dependência do Probe 1 formal (direção reversa de Paley–Wiener de faixa, ou a não-pertença direta via Fourier com peso) está nomeada; a versão numérica não depende dela.
- Minha leitura dos lemas sem fonte fornecida (`product_core_mem_rapidity_standard`, `weighted_real_fourier_separates_standard` em seu corpo, `rapidityStandardSubspace`) é estrutural, ancorada nas assinaturas e nos dados declarados; a evidência de compilação é da bancada.
- Gate intocado; nada compilado, executado ou escrito por mim; a bancada escreve e compila os probes.

**Resumo operacional para a bancada:** Probe 1 — `¬ (U (-1) (productCore 0 1 0 le_rfl zero_lt_one) ∈ rapidityStandardSubspace (2·π²))`, falha: domínio/faixa (testemunha da divergência em `y=π/2`, uma linha: `2e^ξ − 2ξ² ≥ e^ξ` para `ξ ≥ 3`), torção intacta; dependência: Paley–Wiener de faixa ou análise ponderada direta. Probe 2 — `g₀ := exp(−(ξ − iπ/4)²) ∈ K_{π²}` e `¬ (U 1 g₀ ∈ K_{π²})`, falha: ponto fixo, por norma já em `ξ=0`, domínio intacto; dependência: parametrização em `c`. Probe 3 — `h₀ := exp(−(ξ − 3iπ/4)²) ∈ K_{3π²}` e `¬ (U 1 h₀ ∈ K_{3π²})`, falha dupla (borda + fatia `y=5π/4`). Os três juntos verificam que `0 ≤ a` e `w = π` são hipóteses de verdade, com mecanismos de falha ortogonais — que é precisamente o alcance e os sinais do novo `halfline_isotony`.