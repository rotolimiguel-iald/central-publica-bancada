# ORDEM_016 · A‑7.b — Defeito de Wick/BV de aridade UM
## Memória científica comum · resposta **DECLARADO** (até auditoria local)

---

## §0 · Escopo, fonte, o que NÃO tenho

**Estatuto desta unidade:** `DECLARADO`. Memória formal comum; **não** é execução de CAS, **não** é acesso a caminho externo, **não** é aprovação física. Nenhum arquivo foi modificado. Nada aqui presume fechamento de Q2 nem validação empírica.

**Fonte citada (Frob, arXiv:1803.10235v3):** **NÃO TENHO O TEXTO** no contexto fornecido. **Declaro** que a identidade de aridade 1 `q̂ T₁(F) = T₁(s₀F) + T₁(A₁(F))` foi reconstruída a partir do arcabouço padrão BV / renormalização algébrica (consistência de Wess–Zumino, BPHZ, quantização deformacional de campo vetorial cohomológico). **Os sinais abaixo são as MINHAS convenções declaradas**, sujeitas a conferência local contra a fonte Frob. Onde a fonte divergir, o arbítrio é a auditoria local + os controles §8.

**Relação com o pedido escalar a46 e com grafos de duas inserções:** esta unidade **não** repete a46 (Leibniz/Euler escalar), **não** pede recalcular grafos de 2 inserções, e **não** presume fechamento Q2. É **aridade 1**: uma laçada, primeira ordem em ℏ.

---

## §1 · Convenções (declaradas ANTES de calcular)

**(C1) Campos e paridades.** φ^A, A = 1..22. Paridade ε_A = |φ^A|:
- h_ij (simétrico): ε = 0 — **10** comp. em 4D.
- b_i (Lautrup–Nakanishi): ε = 0 — **4**.
- c^i (ghost): ε = 1 — **4**.
- barc_i (antighost): ε = 1 — **4**.

Total **14 pares / 8 ímpares = 22 campos** ✓ (confere com o enunciado). Antifields φ†_A de paridade ε_A + 1 (mod 2).

**(C2) Derivadas.** δ^L/δφ^A (esquerda), δ^R/δφ^A (direita), com δF = δφ^A (δ^L_A F) = (δ^R_A F) δφ^A, e a regra de conversão
`δ^R F/δφ^A = (−1)^{ε_A(|F|+1)} δ^L F/δφ^A`.
Os derivados graduados **gradu‑comutam**: `∂^L_A ∂^L_B = (−1)^{ε_A ε_B} ∂^L_B ∂^L_A`.

**(C3) BRST linear.** qφ^A = (Qφ)^A = Q^A{}_B φ^B, com
- q h_ij = d_i c_j + d_j c_i  (d_i = ∇_i covariante; em fundo plano d = ∂),
- q c^i = 0, q b_i = 0, q barc_i = −b_i.

**Matriz Q** (ímpar, Q² = 0): bloco h→c não‑nulo; bloco barc→b não‑nulo (q barc = −b); c→0, b→0.

**(C4) Antifields / Hessiana livre.** `S_free = ½⟨φ,Pφ⟩` (P Hessiana livre **gradu‑simétrica**), `S_af = ⟨φ†,Qφ⟩`. Com `s = (S,·)` (antibracket BV, convenção `(φ^A,φ†_B)=δ^A_B`):

> **q φ†_A = −(Pφ)_A − (Q^T φ†)_A**  *(declarado: "equações livres Pφ" + "ação adjunta nos antifields")*

Identidades clássicas mantidas em fundo curvo: **Q² = 0**, **Q graded‑simetria de P** (CME: `Q^T P + P Q = 0` no sentido gradu), e covariância local de P, Q (comutadores de ∇ dão curvatura, que é parte das identidades, não anomalia).

**(C5) Contração de Wick / parametrix.** H = H^{AB}(x,y) é uma **bidistribuição só sobre campos** (antifights **não** contraem), **gradu‑simétrica**: `H^{AB}(x,y) = (−1)^{ε_A ε_B} H^{BA}(y,x)`. Pode ser parametrix **localmente covariante**; **NÃO** assumo bisolução exata.

**(C6) Operador de contração.**
> **C_H = ½ H^{AB} ∂^L_A ∂^L_B**  (só derivadas de campo)

Bem‑definido: H gradu‑simétrica + derivadas gradu‑comutam ⇒ simétrico sob A↔B. **Mapa:** `T₁ = exp(ℏ C_H)` (ordenação de Wick: contrai pares dentro de F; F cúbico ⇒ T₁F = F + ℏ·(linear) + O(ℏ²)).

**(C7) Conjugação graduada / ε.** `ε_A := (−1)^{paridade(φ^A)}`. `(Q^T)_C{}^B` é a **transposta graduada** de Q (a convenção exata de Q^T carrega o sinal de Grassmann; fixada abaixo pelo controle T1).

---

## §2 · Defeitos suaves E e D (definidos separadamente, como pedido)

> **E^{AB} := (P H)^{AB} = P^A{}_C H^{CB}** — defeito de **bisolução** (a contração não resolve a eom livre na perna esquerda).
>
> **D^{AB} := (Q H + ε H Q^T)^{AB} = Q^A{}_C H^{CB} + ε_A H^{AC}(Q^T)_C{}^B** — defeito de **equivariância** (a contração não é invariante por Q; o ε_A = (−1)^{ε_A} absorve a reordenação Grassmann ao passar Q pelo campo de paridade ε_A).

Ambos são **suaves** (bidistribuições localmente covariantes). E medem exatamente as duas falhas do parametrix: `PH` (não é bisolução de P) e `QH+εHQ^T` (não é bisolução de Q / não equivariante).

---

## §3 · A fórmula de aridade 1

**Estrutura do mapa.** `q̂ = q + ℏ q̂₁ + O(ℏ²)` é o BRST **quântico**, definido **independentemente** (contra‑termo de ordem 1 de operadores compostos / renormalização), **NÃO** por conjugação `T₁ q T₁^{-1}` (que trivialmente daria A₁ ≡ 0 — proibido pelo enunciado). `T₁ = e^{ℏC_H}`.

Expandindo `q̂ T₁(F) − T₁(qF) = T₁(A₁(F))` a O(ℏ):

```
(q + ℏq̂₁)(F + ℏC_H F) − (qF + ℏ C_H qF) = A₁(F) + O(ℏ)
⟹  ℏ[ (q C_H − C_H q)F + q̂₁ F ] = ℏ A₁(F)
```

> **A₁(F) = [q, C_H](F) + q̂₁(F)**   *(definição a O(ℏ); A₁ mede a falha de equivariância de T₁)*

**Cálculo de [q, C_H].** Como C_H é operador de coeficientes constantes em φ, e `q = q^M ∂_M`:

`[q, ∂^L_A] = −(∂_A q^M)∂_M = −Q^C{}_A ∂^L_C + P_{CA} ∂^†_C`   (pois `∂_A q^{φ†_C} = −P_{CA}`)

e daí
`q C_H F − C_H q F = ½ H^{AB}([q,∂_A]∂_B F + ∂_A[q,∂_B]F)`.

Separando em peça‑Q (vira **D**) e peça‑P (vira **E**, via ∂^†):

```
peça-Q:  −½ H^{AB}(Q^C{}_A ∂_C∂_B + Q^C{}_B ∂_A∂_C)F  =  −½ D^{AB}(∂^L_A ∂^L_B F)
peça-P:  +½ H^{AB}P_{CA} ∂^†_C ∂_B F + ½ H^{AB}P_{DB} ∂_A ∂^†_D F
       =  +½ E^{AB}(∂^†_A ∂^L_B F) + ½ (HP)^{AB}(∂^L_A ∂^†_B F)
```

Usando simetria graduada (`HP = ±(PH)^T`) as duas meias do E combinam.

### ★ FÓRMULA (ODE / aridade 1) — convenção declarada, sinais fixados pelo controle T1 (§8)

$$
\boxed{\;
A_1(F)\;=\;[q,C_H](F)+\hat q_1(F)\;=\;
-\tfrac12\,D^{AB}\big(\partial^L_A\partial^L_B F\big)
\;+\;\tfrac12 E^{AB}\big(\partial^\dagger_A\partial^L_B F\big)
\;+\;\tfrac12 (HP)^{AB}\big(\partial^L_A\partial^\dagger_B F\big)
\;+\;\hat q_1(F)\;}
$$

combinada (via simetria graduada, `HP=±(PH)^T`) na forma compacta **que o controle T1 confirma**:

$$
\boxed{\;
A_1(F)\;=\;-\tfrac12\,D^{AB}\,\partial^L_A\partial^L_B F
\;+\;E^{AB}\,\partial^\dagger_A\,\partial^L_B F
\;+\;\hat q_1(F)\;}
$$

- **D** = `QH + εHQ^T` (não‑equivariância); **E** = `PH` (não‑bisolução).
- **∂^†_A = δ/δφ†_A** = operador **antifield‑Euler** (explícito).
- **Fator ½** no termo‑D (par único); o termo‑E carrega ½+½ = **1** após combinar as duas ordens.
- **Sinais Grassmann:** ε_A = (−1)^{ε_A} dentro de D; transposta graduada (Q^T); graduação de ∂^L, ∂^†. **Convencional** — arbitrado por T1.
- **q̂₁** = liberdade de renormalização localmente covariante (§6).

---

## §4 · Onde `PH` entra mesmo se `QH + εHQ^T = 0`

Fixe **D = 0** (parametrix equivariante, `QH+εHQ^T=0`). Então

$$
A_1(F)\big|_{D=0}\;=\;E^{AB}\,\partial^\dagger_A\partial^L_B F\;+\;\hat q_1(F),
\qquad E=PH .
$$

O termo **E = PH sobrevive**. Fisicamente: mesmo uma propagação **equivariante** (compatível com a identidade de Slavnov–Taylor em nível de Q) tem anomalia por **não ser bisolução da eom livre** (P) — termos de contato / defeito do parametrix, **visíveis só em funcionais com antifields** (canal antifield‑Euler `∂^†`). O **controle T1 (§8) é exatamente esta testemunha**: Q = 0 (⇒ D = 0), P ≠ 0 (⇒ E = PH = h ≠ 0), e `[q,C_H]F = h ≠ 0`.

Canal: o `∂^†_A` vem do `−(Pφ)_A` em `qφ†_A`; a contração em `Pφ` produz `PH = E`. **Portanto E entra pela ação adjunta de q sobre antifields** — nunca pela contração direta de F.

---

## §5 · As três separações (pedido explícito)

**(a) Mudança de ESTADO por bisolução suave.** `H → H + H_b` com `P H_b = 0` **e** `Q H_b + ε H_b Q^T = 0`. Ambos os defeitos nulos para H_b ⇒ **A₁ não muda** (o termo de defeito zera); muda só o **estado** (escolha de vácuo/polarização entre bisoluções). Não é anomalia, é gauge do estado.

**(b) Mudança de PARAMETRIX por suave não‑bisolução.** `H → H + H'` com `E' = PH' ≠ 0` e/ou `D' = QH'+εH'Q^T ≠ 0` suaves. Desloca
`A₁ → A₁ − ½D'^{AB}∂^L_A∂^L_B F + E'^{AB}∂^†_A∂^L_B F`, i.e., **altera A₁ por termos locais de contato**. É o efeito físico do parametrix inexato.

**(c) Liberdade de renormalização localmente covariante.** `q̂₁` (e contra‑termos finitos locais covariantes) é a ambiguidade residual padrão: pode-se adicionar funcionais locais covariantes sem violar a consistência. É a única liberdade que **não** é fixada pelos defeitos.

Resumo: **estado** (bisolução, inerte em A₁) · **parametrix** (E,D, dão termos locais) · **renormalização** (q̂₁, ambiguidade covariante). A fórmula os torna manifestos.

---

## §6 · Aplicação a `F_af`

$$
F_{af}=\int\chi\Big[h^\dagger_{ij}(L_c h)_{ij}+c^\dagger_i c^j\nabla_j c^i\Big],\quad
(L_c h)_{ij}=c^k\nabla_k h_{ij}+h_{kj}\nabla_i c^k+h_{ik}\nabla_j c^k .
$$

**Contratos permitidos:** ⟨hh⟩,⟨hb⟩,⟨bh⟩,⟨c barc⟩,⟨barc c⟩ ≠ 0; ⟨hc⟩=⟨cc⟩=⟨h barc⟩ = 0. Antifields não contraem.

**(i) C_H F_af = 0.** Monômios: `h†(c∇h)`, `h†(h∇c)`, `h†(h∇c)`, `c†(c∇c)`. Pares de **campo** disponíveis: (c,h) → ⟨hc⟩=0; (h,c) → ⟨hc⟩=0; (c,c) → ⟨cc⟩=0. **Nenhuma contração direta** ⇒ `C_H F_af = 0`. ✔

**(ii) A anomalia sobrevive via `C_H(q F_af) ≠ 0`** (pois `A₁ = [q,C_H]F_af = −C_H(qF_af)` quando `C_H F_af = 0`, e `C_H(qF_af)` **não** precisa anular). Canais que sobrevivem, **apesar de `C_H F_af = 0`**:

| canal | origem em `q F_af` | contração | defeito | antifield‑Euler |
|---|---|---|---|---|
| **A** | `q(h†) ⊃ −(Ph)` × `(L_c h)` | **⟨hh⟩** | **E^{hh}** = (PH) | **δ/δh†_ij** |
| **B** | `q(h†) ⊃ −(Ph)` (com **b** do gauge‑fixing) × `(L_c h)` (com h) | **⟨hb⟩/⟨bh⟩** | **E^{hb}** = (PH) | **δ/δh†_ij** |
| **C** | `q(c†) = δS/δc^i ⊃ barc` × `(c∇c)` | **⟨barc c⟩** | setor ghost | **δ/δc†_i** |

Todos são do **canal E = PH / ghost** — **nenhum exige D ≠ 0** (ilustra §4). O termo‑D `−½D^{AB}∂^L_A∂^L_B F_af` existe em geral (derivadas de campo de 2ª ordem de F_af) e **zera se D = 0**.

**Termos que NÃO sobrevivem:** `h†·q(L_c h) ⊃ h†(c∇∇c + ∇c∇c)` → pares (c,c) → ⟨cc⟩ = 0 ⇒ nulo (o 2‑jato de c **não** entra).

### ★ LISTA FINITA DE JATOS para `A₁(F_af)` (tipos + ordens)

**Operadores antifield‑Euler presentes:** `δ/δh†_ij`, `δ/δc†_i`. *(Ausentes: `δ/δb†`, `δ/δbarc†` — F_af não os contém.)*

**Tipos de campo e ordens de derivada necessárias:**

| tipo | jatos que aparecem | origem |
|---|---|---|
| **h_ij** | 0‑jato (em `h∇c`), **1‑jato** `∇h` (em `c∇h`), **2‑jato** `∇∇h` (parte principal de `(Ph)`) | (Ph)·(L_c h), canal A |
| **b_i** | 0‑jato e **1‑jato** `∇b` (gauge‑fixing em `(Ph) = ∇_(i b_j)+…`) | canal B |
| **c^i** | 0‑jato (em `c∇h`, `c∇c`), **1‑jato** `∇c` (em `h∇c`, `∇_j c^i`) | canais A, C |
| **barc_i** | 0‑jato e **1‑jato** `∇barc` (de `q(c†)=δS/δc^i`) | canal C |
| **curvatura** | `R^a{}_{bcd}·h_ij`, `R·c` (comutadores de ∇ em fundo curvo) | identidades clássicas covariantes |

**Ordem máxima de derivada: 2** (só sobre **h**, via `(Ph)`). `∇∇c` **não** entra (canal ⟨cc⟩ = 0).

**Distribuições de defeito a entregar simbolicamente** (jatos desconhecidos = o H concreto): `E^{hh}`, `E^{hb}`, `E^{bh}`, `E^{bb}` (= PH) e `D^{AB}` (= QH+εHQ^T) para A,B ∈ {h,b,c,barc}, cada uma com seu conteúdo de derivadas (0‑, 1‑, 2‑jato) e covariância local. **Não** substituo A₁ por traço de calor: A₁ é o funcional **local** da fórmula; o heat kernel é só a *representação* de H, não a anomalia.

---

## §7 · Controles

**T1 — sinal de [q,C_H] + testemunha PH≠0 (aridade 1, um par antifield‑Euler).**
Álgebra graduada: campo **x** (par, ε=0), antifield **x†** (ímpar). BRST: `q x = 0`, `q x† = −x` (Q = 0 nos campos, P = 1, puro antifield‑Euler). Contração `H^{xx} = h`. `C_H = ½h ∂_x∂_x`. Tome **F = x† x**:
- `C_H F = ½h ∂_x∂_x(x†x) = 0` (só um x) ⇒ `C_H F = 0` ✔
- `qF = (qx†)x + (−1)^{|x†|}x†(qx) = (−x)x + (−1)x†·0 = −x²`
- `C_H(qF) = C_H(−x²) = −½h∂_x∂_x(x²) = −h`
- **`[q,C_H]F = q(C_H F) − C_H(qF) = 0 − (−h) = +h`**

Defeitos: **D = 0** (Q=0); **E = PH = 1·h = h**.
Fórmula: `A₁ = −½D ∂∂F + E ∂^†∂F = 0 + h·(∂^†_{x†}∂_x(x†x)) = h·1 = +h` ✔✔ **Casa com [q,C_H]F = h.**

⇒ **Sinal fixado:** `A₁ ⊃ +E^{AB} ∂^†_A ∂^L_B F` (coef. **+1** após combinar ½+½). **E PH ≠ 0 dá testemunha não‑nula com D = 0** ✔ (é o pedido).

**T2 — bisolução equivariante zera.** Se `D = 0` e `E = 0` (H bisolução: PH=0 e QH+εHQ^T=0), a fórmula dá `[q,C_H] = 0`; com `q̂₁ = 0` (sem contra‑termo), **A₁ = 0** ✔. Consistente: A₁ (parte de defeito) é construída **só** de D e E.

**T3 — PH ≠ 0 com testemunha.** É o próprio T1 (E = h ≠ 0 ⇒ A₁ = h ≠ 0) ✔. Acrescente‑se, se desejado, um D ≠ 0: dois campos com Q ≠ 0 e H não equivariante, onde `−½D^{AB}∂_A∂_B` dá contribuição não‑nula; confirma o canal D.

---

## §8 · Dado faltante para aplicar ao setor não‑mínimo completo 22×22

Para levar a fórmula ao setor completo (22 campos + 22 antifields) **falta**:

1. **O parametrix H explícito 22×22**: todos os blocos não‑nulos `⟨hh⟩,⟨hb⟩,⟨bh⟩,⟨c barc⟩,⟨barc c⟩` (e confirmar `⟨bb⟩=⟨barc barc⟩=⟨hc⟩=⟨cc⟩=⟨h barc⟩=0`), com conteúdo de jatos e covariância local (forma de Hadamard).
2. **A matriz P explícita** (operador quadrático livre **com gauge‑fixing**), que decide se `(Ph)_ij ⊃ ∇_(i b_j)` (canal B) e o operador de ghost `(Pc)`.
3. **A matriz Q explícita** no bloco (b, barc): `q barc = −b`, `q b = 0`, `q h = dc+cd`, `q c = 0`.
4. **A transposta graduada `(Q^T)` e `ε_A` para as 22 espécies** (para fechar D exatamente; a convenção de Q^T é a que T1 fixa em aridade 1, mas o bloco 22×22 exige o mesmo cuidado).
5. **Dados de fundo curvo** (curvatura R, condições de contorno/falloff) para P, Q covariantes e para `E = PH`, `D = QH+εHQ^T` localmente covariantes.
6. **O q̂₁ escolhido** (ou a decisão de reportar A₁ só módulo contra‑termos locais covariantes).

Sem (1)–(4) a fórmula **aplica‑se formalmente**, mas as componentes numéricas de E, D permanecem **simbólicas** (é o que entrego em §6).

---

## §9 · Veredito (DECLARADO)

- **Fórmula de aridade 1 entregue** (utilizável), com **fatores ½**, **sinais Grassmann** (ε_A, transposta graduada) e **termos antifield‑Euler explícitos** (∂^†_A), **em termos de D = QH+εHQ^T e E = PH** e das derivadas funcionais de F.
- **PH entra mesmo com D = 0** — demonstrado pela fórmula e pela **testemunha T1** (Q=0, E=h≠0, [q,C_H]=h≠0).
- **Três separações** manifestas: estado (bisolução, inerte) · parametrix (E,D → termos locais) · renormalização (q̂₁).
- **`F_af`:** `C_H F_af = 0` mas `C_H(qF_af) ≠ 0`; **termos sobreviventes** = canais **A (⟨hh⟩, E^{hh})**, **B (⟨hb⟩, E^{hb})**, **C (⟨barc c⟩)** — todos no canal E/ghost, **nenhum exige D ≠ 0**; o termo‑D existe formalmente e zera com D = 0.
- **Lista FINITA de jatos** para `A₁(F_af)`: 0‑jato (h,b,c,barc) · 1‑jato (∇h,∇c,∇b,∇barc) · **2‑jato só de h** (∇∇h) · curvatura (R·h, R·c) · antifield‑Euler (δ/δh†, δ/δc†). `∇∇c` **não** entra (canal ⟨cc⟩ = 0).
- **Fonte Frob arXiv:1803.10235v3: NÃO TENHO O TEXTO — declarado.** Sinais são convenções minhas, sujeitas a auditoria local contra a fonte; o arbítrio são os controles T1–T3.

**Pendências (para auditoria local, não executadas aqui):** conferir os sinais da transposta graduada `(Q^T)` e do coeficiente combinado do termo‑E contra a fonte Frob e contra um segundo controle manual; verificar que `q̂₁` não absorve o termo‑E (o canal PH é genuíno, não contra‑termo); e, no 22×22, computar E, D a partir do H e do P, Q concretos (itens §8.1–8.4).

`NOT_FALSIFIED ≠ CONFIRMED` · `PROVADA ≠ CONFIRMADA` · **nada aqui é aprovação física nem fechamento Q2.**