# ORDEM_016 A-7.b — Auditoria da interpretação covariante e distribucional do contato hc

**Estatuto desta entrega: prova escrita verificável, resultado [DECLARADO] até auditoria da bancada.** Nenhum código foi executado nesta unidade; toda verificação abaixo é derivada à mão a partir das três fontes fornecidas (`DERIVACAO.md`, `results.json`, `bilocal_curved_contact_primitive_check.py` + `oneform_second_curvature_engine_v2.py`). Nenhum coeficiente medido foi ajustado.

---

## 1. A regra de emparelhamento distribucional para ∫ h(X) A(X,Y) c(Y)

**Setup.** O contato é uma distribuição bilocal na diagonal, escrita como combinação de monômios de derivadas da delta covariante (bidensidade, "densidade de volume já incluída", `DERIVACAO.md` l. 87–88):

```
A(X,Y) = C_E · Σ_s  coef_s · e_s · ∂^{α(s)} ∂^{β(s)} δ̄(X,Y),
```

com `e_s` a estrutura de índices (pernas `a,b` de `h`, perna `r` do ghost `c`), `|α|+|β| = 5−2o`, `o ∈ {0,1}` — **grau total ímpar (5 em K0, 3 em K1)**.

**A identidade elementar que governa tudo.** Para a delta covariante escalar em coordenadas normais centradas em Y:

```
∂_X^μ δ̄(X,Y) = − ∂_Y^μ δ̄(X,Y)   (na diagonal, em RNC; a densidade corrige isto só a O(K), ver §1.3)
```

### 1.1 As três leituras do mesmo monômio

Para um monômio com `|α|` derivadas na perna X e `|β|` na perna Y, o emparelhamento com testes de suporte compacto dá, por integração por partes **em cada ponto separadamente**:

| leitura | fórmula | sinal |
|---|---|---|
| jato × jato | `∫ (∂^{α} h)·(∂^{β} c) dV` | `(−1)^{|α|+|β|}` |
| operador em c: `(A c)(X)` | `(−1)^{|β|} · e_s(∂^{α+β} c)(X)` | `(−1)^{|β|}` |
| operador em h (adjunto): `(Aᵀ h)(Y)` | `(−1)^{|α|} · e_sᵀ(∂^{α+β} h)(Y)` | `(−1)^{|α|}` |

Duas consequências que respondem diretamente ao ponto pedido:

1. **Agir em h e agir em c não são a mesma regra.** Na base medida (`δ_ab q_r (q²)^{2−o}`, `(δ_ar q_b + δ_br q_a)(q²)^{2−o}`, `q_a q_b q_r (q²)^{1−o}`), o ghost carrega exatamente uma derivada (`|β| = 1`) em todas as estruturas. Logo a forma "operador em c" carrega um fator `(−1)^{|β|} = −1` **se a escrita do monômio põe `q_r` na perna Y**; e não carrega nenhum fator se todas as derivadas estão escritas na perna X (o "contato no extremo X", `DERIVACAO.md` l. 46–49: os coeficientes são recuperados *depois da integração em Y* e a divergência que aparece é `div_X`). As duas escritas são equivalentes — diferem por `∂_Y δ̄ = −∂_X δ̄` — mas **os coeficientes numéricos do `results.json` pertencem a uma das duas, e a escolha não está fixada em nenhuma frase do `DERIVACAO.md`**. Esta é a hipótese ausente H-CONV (§6).

2. **O erro X↔Y é global e invisível internamente.** Como 5 e 3 são ímpares, identificar `∂_X` com `∂_Y` sem o sinal troca `(−1)^n = −1` em **todo** monômio — um sinal global do contato inteiro, que as 256 verificações internas do script **não detectam**, porque o `target` é construído dos mesmos coeficientes medidos (circularidade estrutural). O que quebra a circularidade é a âncora externa: a unidade plana (`bilocal_flat_contact_primitive`, importada como input do script, l. 20) verificou `N G = A_plano` no recorte plano com 180 verificações **contra a medida plana**, e a ponte `s0 B_bc = −A_hc` (`DERIVACAO.md` l. 104–105) tem o `−1` explícito. Com `B_bc = −C_E/2 ∫ h·N h` e `N` formalmente autoadjunta (ordem 4, par — autoadjuntividade possível): `s0 B[h;c] = −C_E ∫ h·N(Gc)`, e igualando a `−A[h,c] = −∫ h·(A c)` obtém-se `C_E·N G = A`. É essa identidade com sinal — não as 256 verificações — que fixa a leitura do sinal. A ordem `NG` é `4+1 = 5`, ímpar como `A` ✓.

### 1.2 O sinal da leitura do engine

Em ondas `c = V e^{ip·x}`, `∂^{w} c = i^{|w|} p^{w} c`. A convenção declarada (`PRE_REGISTER`, l. 24; engine, l. 37): remover **um** fator `i`, logo o jato vale `i^{|w|−1} p^{w} = (−1)^{(|w|−1)/2} p^{w}`: **ordem 5 → `+`, ordem 3 → `−`**, exatamente o fator `(−1)^{(n−2o−1)//2}` de `jet()`. Sob a leitura (i) — derivadas na perna X, o "contato no extremo X" — o operador em c é `+∂^{n}` (nenhuma transposição residual), e o sinal do engine é **o mesmo** da medida. Sob a leitura (ii) seria o oposto.

### 1.3 A densidade

`√g = 1 − Kz/2 + O(K²)` em RNC no espaço-forma (`Ric = 3Kg`, 4D): `∂√g|_0 = 0`, `∂_i∂_j√g|_0 = −K δ_ij`. Consequências: (a) a densidade **não toca sinais** (fator escalar real, mesmo nos dois modos); (b) ela **adiciona termos de curvatura** — o `−Kz/2 ×` parte plana de `DERIVACAO.md` l. 60–61 — que já estão nos coeficientes medidos; o script os herda via coeficientes e **não os recalcula** (correto: contar uma vez, não duplicar); (c) a identidade `∂_X δ̄ + ∂_Y δ̄` falha por termos `∂ log √g` que se anulam na origem em ordem 1 e entram só a O(K) — coerente com (b).

---

## 2. A conversão de Taylor em frame radial para jatos covariantes no ponto Y

**Proposição (exatidão, sem termos de correção).** Sejam `Y ∈ M`, `X = exp_Y(x)`, e `E_a(X)` o frame transportado paralelamente ao longo da geodésica radial (o "frame radial" dos testes, `DERIVACAO.md` l. 87–88). Para todo tensor `h`:

```
h_{a…}(X) = Σ_{n≥0} (1/n!) x^{i₁}…x^{iₙ} [∇_{(i₁}…∇_{iₙ)} h_{a…}](Y).
```

**Prova.** Seja `H(τ) := h_{a…}(exp_Y(τ x̂))`, `x̂ = x/|x|`, em componentes no frame radial. Como o frame é paralelo na direção radial, `dH/dτ = (x̂^i ∇_i h)(γ(τ))` em componentes; iterando, `dⁿH/dτⁿ = (x̂·∇)ⁿ h`, e em `τ = 0` o fator `x̂^{i₁}…x̂^{iₙ}` (totalmente simétrico) projeta na parte totalmente simetrizada dos operadores compostos. Taylor em `τ ∈ [0,|x|]` dá a fórmula. ∎

**Observações que respondem ao ponto:**
- A curvatura **não aparece** como termo de correção nesta conversão — ela apareceria no frame coordenado (a partir de O(Kx²) nos jatos de ordem ≥ 2). Aparece, em vez disso, (i) pelas conexões dentro dos jatos covariantes — que o engine inclui: a recursão `field()` aplica `connection(ko, c, i, target)` com `target` percorrendo as derivadas anteriores **e o índice de fibra** (`indices = rest + [a]`, engine l. 24–31), que é a estrutura correta do jato covariante de uma one-form, e com o sinal `−1` correto de `∇ = ∂ + Γ`; e (ii) pela densidade (§1.3), já nos coeficientes.
- As partes antissimétricas dos jatos (comutadores, `[∇,∇] ~ K`) são projetadas fora pela simetria dos `x`'s — e é por isso que a **completação totalmente simetrizada** (`symv`, média sobre permutações, script l. 38–40) é a única realização covariante fiel dos monômios: o polinômio de derivadas de delta é **comutativo**, e a média simetrizada é a sua imagem covariante que preserva essa comutatividade. Qualquer ordenação não simetrizada diferiria por termos de curvatura — ambiguidade genuína de O(K), capturável no espaço-forma (onde os comutadores são universais em K) mas **não** em variedade genérica (Weyl, ∇R ausentes aqui).
- O ghost `c(Y)` está no ponto: nenhuma conversão é necessária para ele. A conversão acima é exatamente o que "testes em frame" significa na medida. E a regra do `DERIVACAO.md` l. 62 ("os índices de Y não recebem conexão de X") é respeitada pelo engine: as conexões do jato são as do ponto Y.

---

## 3. O que as ondas paralelamente transportadas e as 4 polarizações provam — e o que não provam

**Proposição (completude).** A família `ψ_{p,V}(x) = V(x) e^{ip·σ(x)}` com `V` paralela-transportada (perfil radial com amplitude corrigida — os coeficientes `−1/6`, `1/120` de `initial()` são os da série sinc do modo no espaço-forma) gera, por polarização, **todos** os jatos locais simetrizados em Y nas ordens testadas: os jatos planos são `i^{|w|} p^{(w)} V_a` e `span{p^{⊗n} ⊗ V : p ∈ ℝ⁴, V ∈ ℝ⁴} = Symⁿ(T_Y M) ⊗ fibra`; as correções de curvatura são de grau estritamente menor em `p` (cada `K^o` remove `2o` momentos), de modo que a matriz de geração é triangular com diagonal `i^{|w|} ≠ 0` — a curvatura não quebra o span. Logo `p` simbólico genérico × 4 polarizações independentes (script l. 87–97) **bastam** para testar todos os jatos locais simetrizados até a ordem 5, no ponto Y, no espaço-forma. ∎

**O que isto não prova (enumerado sem rodeios):**

1. **Naturalidade sob mudança de ponto base Y → Y′.** O teste verifica o operador *em cada Y separadamente*; a naturalidade exige que a lei `Y ↦ D_Y` transforme covariantemente, o que nenhum teste de jatos num ponto vê. Aqui os dois modos se separam de forma decisiva:
   - **geodésico** (`ρ²` = distância ao quadrado): o regulador é intrínseco, logo o contato medido é um objeto intrínseco, e a sua representação por jatos covariantes simetrizados é natural **dada a unicidade da classe simetrizada** (que a completude garante). A identificação é substantiva aqui.
   - **coordenado** (`w = (X−Y)²`): depende da carta centrada em Y. Os coeficientes da carta foram **lidos como se fossem** jatos covariantes — uma hipótese de leitura, não um teorema. A obstrução já está medida no próprio `results.json`: `geodesic_minus_coordinate` em K1 é `(−35/144, −1/12, 7/72) ≠ 0` (`DERIVACAO.md` l. 90–93: diferença local de extensão, com origem identificada na segunda derivada do regulador, l. 17–18: o termo `−(2K/3)(δ_ij − X_iX_j/z)` presente em `ρ²`, ausente em `w`). Se o regulador coordenado fosse natural, coincidiria com o intrínseco. O caveat do script (l. 26, l. 104) declara exatamente isto — e está correto em declará-lo.
2. **Ordenações não simetrizadas** além do que o espaço-forma vê (Weyl = 0, ∇R = 0 aqui): em variedade genérica há ambiguidades de ordem invisíveis neste teste.
3. **O escopo declarado**: W suave, K², aridades não lineares, todos os diagramas, valores de contorno lorentzianos, e a Q2 completa (`results.json`: `full_Q2: false`) — fora.
4. **O sinal de leitura dos monômios** (§1.2): circularidade interna, ancorada externamente (§1.1).

---

## 4. Teste tensorial não axial, ordem 3 (com contraste de ordem 5), derivado à mão

**Escolha deliberadamente não axial**: `p = (1, 2, −1, 1)` (todas as componentes não nulas), `V = (1, −1, 2, 1)`, componente `(a,b) = (0,2)` (mista, fora dos eixos) e `(0,0)`. Invariantes: `p² = 7`, `p·V = 1 − 2 − 2 + 1 = −2`. Plano (`K = 0`) para isolar o sinal; cada estrutura é computada **dos dois lados**: (A) monômio de delta lido como operador em c (leitura (i), perna X); (B) jato simetrizado do engine (`symv`, sinal `(−1)^{(3−1)//2} = −1`).

**Estrutura K1-1** `δ_ab q_r q²` — operador `δ_ab □(∂·c)`:
(A) `∂_r □(V^r e^{ipx}) = −p²(ip_r)V^r e^{ipx}`; somando `r`: `−i p²(p·V) = 14i` → sem `i`: **`14 δ_ab`**.
(B) `symv((r,k,k), r, 0) = −p_r p² V_r` → `Σ_r`: `−p²(p·V) = 14`; × `δ_ab` ✓ **igual**.

**Estrutura K1-2** `(δ_ar q_b + δ_br q_a) q²` — operador `∂_b □ c_a + ∂_a □ c_b`:
(A) `−i p²(p_b V_a + p_a V_b)` → sem `i`: (0,2): `−7((−1)(1) + (1)(2)) = ` **`−7`**; (0,0): `−7·2 p_0 V_0 = ` **`−14`**.
(B) `symv((b,k,k),a,0) + symv((a,k,k),b,0) = −p²(p_b V_a + p_a V_b)` ✓ **igual, componente a componente**.

**Estrutura K1-3** `q_a q_b q_r` — operador `∂_a∂_b(∂·c)`:
(A) `(ip_a)(ip_b)(ip_r)V^r = −i p_a p_b(p·V)` → sem `i`: (0,2): `−(1)(−1)(−2) = ` **`−2`**; (0,0): `−(1)(1)(−2) = ` **`+2`**.
(B) `symv((a,b,r), r, 0)`: no plano todas as permutações coincidem, `= −p_a p_b p_r V_r` → `Σ_r`: `−p_a p_b(p·V)` ✓ **igual**.

**O contato medido (geodésico) nesses componentes**, com `(u₁,v₁,w₁) = (−65/288, −241/288, 401/144)` sobre `C_E = −4π²`:
- (0,0): `C_E[(−65·14 + 241·14)/288 + 802/144] = C_E·4068/288 = −4π²·1017/72` = **`−56,5 π²`**;
- (0,2): `C_E[1687/288 − 1604/288] = C_E·83/288` = **`−83π²/72`**.

**Detector de sinal (o papel deste teste):** sob a leitura errada (ii) — `q_r` na perna Y lido sem o `−1` da transposição — **todos** os valores acima aparecem com o sinal trocado (`+56,5π²`, `+83π²/72`), porque `|β| = 1` é ímpar em toda a base. Um único componente não axial, computado contra o motor da medida, decide a convenção. A bancada pode executá-lo sem tocar coeficiente algum.

**Contraste de ordem 5 (sinal relativo entre ordens):** estrutura K0-3 `q_a q_b q_r q²` — operador `∂_a∂_b □(∂·c)`: ondas dão `(ip_a)(ip_b)(−p²)(ip·V) = +i p² p_a p_b(p·V)` → sem `i`: `+p² p_a p_b(p·V)`; engine ordem 5: sinal `+`, `symv((a,b,r,k,k),r,0) = +p² p_a p_b(p·V)` ✓ — (0,2): `7·(−1)·(−2) = 14`. O sinal **+** da ordem 5 contra o **−** da ordem 3 confere que a convenção pega a paridade relativa correta entre as duas ordens.

---

## 5. Veredito e hipótese ausente

**Sim — a completação por derivadas covariantes totalmente simetrizadas representa o contato medido, com o mesmo sinal**, sob a leitura (i) ("contato no extremo X", derivadas na perna X), que é a leitura coerente com `DERIVACAO.md` l. 46–49 e com a âncora `s0 B = −A_hc` verificada na unidade plana. A correspondência estrutura-a-estrutura entre a base de monômios e o `target` do script é exata (conferida item a item em §4); a conversão Taylor→jatos é exata no frame radial (§2); a convenção de sinal do engine coincide com a regra de emparelhamento (§1.2); a densidade não toca sinais e entra corretamente uma só vez via coeficientes (§1.3).

**Duas qualificações, sem ajuste de nada:**
1. **H-CONV (hipótese ausente, não erro detectado).** O `DERIVACAO.md` nunca escreve em uma frase qual é a perna das derivadas `q`. Sob a leitura alternativa (ii) haveria um sinal global `−1` — e nenhuma das 256 verificações internas o veria. *Correção finita exata:* acrescentar ao `DERIVACAO.md` a frase da convenção e executar **um** componente do detector da §4 (p. ex. `(0,2)` de K1-3: `−2·C_E·w₁` contra o motor da medida) — custo de uma linha de prova e uma execução de um componente.
2. **Naturalidade do regulador coordenado: permanece [OPEN] e formal** — como o próprio script declara (l. 26, l. 104). A obstrução medida `(−35/144, −1/12, 7/72)` em K1 é o valor concreto dessa não-naturalidade; a representação covariante é substantiva **somente no modo geodésico** (regulador intrínseco + completude + unicidade simetrizada).

## 6. Lacunas declaradas desta auditoria

- O motor que produziu `bilocal_XY_extension_contact/results.json` **não** foi fornecido; o sinal foi auditado por regra derivada + detector, não por reexecução.
- O output do script auditado (`bilocal_curved_contact_primitive/results.json`) não foi fornecido; os 256 checks são os reportados no pedido.
- `spaceform_covariant_jet_engine.py` (semântica interna de `ZERO`, `mono`, `deriv`, `connection`) não foi fornecido; a análise do engine limita-se à interface documentada e à estrutura recursiva visível em `oneform_second_curvature_engine_v2.py`.
- A âncora de sinal da unidade plana (180 verificações) está fora do escopo das fontes; a cadeia de sinal é coerente **condicionada** a ela.

`[DERIVED: a regra de emparelhamento, a conversão Taylor→jatos, o teste não axial] · [INPUT: os coeficientes medidos, lidos, não ajustados] · [OPEN: naturalidade do regulador coordenado; H-CONV a fixar em uma frase + um componente] · [DECLARADO: este resultado até auditoria da bancada]`