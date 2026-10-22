# ORDEM_016 — A-7.b: a identidade de consistência de ordem ℏ para a quebra Ward localizada (modelo truncado, prescrição local de produtos temporais)

**Regime desta resposta:** derivação algébrica formal feita à mão nesta etapa. Nenhuma execução de CAS, nenhuma escrita em arquivo, nenhuma recompilação é alegada aqui. As identidades pontuais citadas do artefato `localized_gauge_fixing_commutator_check.py` são **lidas** do código fornecido, não reexecutadas. Auxiliar euclidiano plano ℝ⁴; **nenhuma identificação automática** com a teoria lorentziana. Resultado: `DECLARADO` até auditoria local.

Estatutos usados: `[DERIVED]` (álgebra formal feita nesta resposta), `[REAL — artefato lido]` (identidades verificadas pelo script fornecido), `[KNOWN]` (literatura BV/WZ), `[INPUT]` (convenção/hipótese declarada), `[OPEN]` (lacuna nomeada).

---

## 1. Setup, convenções e o que já está pago

Campos: `h_{μν}` simétrico par, `b_μ` par, `c_μ`, `barc_μ` ímpares. Fontes `h†, c†` sem propagadores. Operadores:

- `(Gc)_{μν} = ∂_μ c_ν + ∂_ν c_μ` (1ª ordem);
- `(Ch)_ν = ∂_μ h_{μν} − ∂_ν tr(h)/2` (1ª ordem);
- `Q = C·G` (2ª ordem; no euclidiano, `Q = □`);
- `Z = L_c h`, `w = c·∂c` (polarizado: `w_i = (u·q)v_i − (v·p)u_i` para ondas ímpares `u,v` — marcadores de jato, sem propagadores).

BRST: `s0 h = Gc, s0 c = 0, s0 barc = −b, s0 b = 0`; `s1 h = Z, s1 c = w`, `s1 barc = s1 b = 0`.

**Torre de nilpotência (Jacobi/estrutural, sem normalização) `[DERIVED]`:**

1. `s0² = 0` (livre abelianizado);
2. **`s0 Z = −G w`** — lê-se de `s²h = 0`: `(s0 s1 + s1 s0)h = s0 Z + s1(Gc) = s0 Z + G w = 0`. `[REAL — artefato lido]`: verificada simbolicamente no script (`eq(s0Z[a,b]+gw[a,b])`, em duas ondas ímpares);
3. `s0 w = 0` (pois `s0 c = 0`);
4. `s1 w = 0` polarizado (Jacobi graduada do colchete de Lie) — alvo declarado do pré-registro (`Graded nilpotence polarized in two odd plane waves`), **não reexecutado aqui** `[OPEN — a auditar]`.

**Comutadores com o cutoff (identidades de operadores diferenciais):**

- `[C,χ]Z = (∂_μχ)·Zbar^{μ,·}`, com `Zbar_{μν} = Z_{μν} − η_{μν}tr(Z)/2` — `[REAL — artefato lido]` (bloco `comm` do script);
- `[Q,χ]w = (□χ)w + 2(∂χ·∂w)` — `[REAL — artefato lido]` (bloco `qc` do script);
- `[G,χ]w = (∂χ)·w` (1ª ordem) — `[DERIVED]`.

---

## 2. Ação truncada e a quebra BV clássica `I_χ`

Com κ reinstalado (no modelo, κ = 1 implícito; cada `Z, w` carrega um κ):

`S_χ = S0 + κV_χ`, `V_χ = Vgh_χ + Vaf_χ = ∫χ[barc·C Z + h†Z + c†w]` (pré-IBP).

`I_χ ≡ (S_χ, S_χ)/2 = (S0, κV_χ) + (κV_χ, κV_χ)/2` (a peça `(S0,S0) = 0`; o antibracket é **simétrico** para funcionais pares, logo a mista aparece uma só vez).

### Bloco A — setor de gauge-fixing (ordem κ¹) `[DERIVED, com peças REAL — artefato lido]`

`s0(∫χ barc C Z) + s1_χ(∫[b·Ch − b²/2ℓ + barc·Qc])`:

- `s0(∫χ barc CZ) = ∫χ[−b·CZ − barc·C(Gw)]` (usa `s0 barc = −b` e `s0Z = −Gw`);
- `s1_χ` do gauge-fixing `= ∫[b·C(χZ) + barc·Q(χw)]`.

Soma, usando `Qw = C(Gw)` (pois `Q = CG`):

**`A = ⟨b, [C,χ]Z⟩ − ⟨barc, [Q,χ]w⟩`** — exatamente a identidade-alvo do pré-registro (`s0 Vghost_chi + s1_chi S0_gf = <b,[C,χ]Z> − <barc,[Q,χ]w>`, "modulo defined integrated adjoints"). O sinal relativo entre as peças é o da convenção do pré-registro; a estrutura de comutadores é a verificada no script. Reescrevendo o segundo termo pela identidade de borda fantasma `[REAL — artefato lido]`:

`A = ∫ ∂_μχ · J^μ_gf + div`, **`J^μ_gf = b_ν Zbar^{μν} + (∂^μ barc_ν)w^ν − barc_ν ∂^μ w^ν`**, com `div = −∂_μ(∂^μχ · barc·w)` (bloco `boundary` do script).

### Bloco B — setor de fontes e cinético (ordem κ¹) `[DERIVED — coeficientes a auditar]`

`(S0, κVaf_χ) +` variação do setor `½⟨h,Hh⟩`:

`B = κ∫χ[E_h·Z − h†·Gw − (G*h†)·w − (Q*barc)·w]`, com `E_h = δS0/δh = Hh + C*b` (o Euler livre **inclui o setor b**, como exigido). Em χ uniforme, os termos de volume de A+B cancelam (conteúdo de `s0Z+Gw=0` e da definição de `E_h`); com χ variável restam as peças ∝ ∂χ das IBPs. A forma fechada dos coeficientes deste bloco fica `[OPEN — a auditar em CAS]`.

### Bloco C — interação × interação (ordem κ²) `[DERIVED — estrutura]`

`(κV_χ, κV_χ)/2`: dois vértices com χ². Com χ uniforme, anula-se pela nilpotência de `s1` (Jacobi de difeomorfismo, item 4 da torre); com χ variável sobra a peça bilinear `I^{(2)}(χ,χ) ∝ (∂χ)χ + (∂χ)(∂χ)`, genuinamente de **dois vértices**.

### Polarização

`I(χ_X, χ_Y) ≡ (S_{χ_X}, S_{χ_Y})/2`, com `I(χ,χ) = I_χ` e `I_{χ_X+χ_Y} = I_{χ_X} + 2I(χ_X,χ_Y) + I_{χ_Y}`. Os blocos A e B (lineares em χ) não polarizam; a peça polarizada é `κ²I^{(2)}(χ_X,χ_Y)`, com suporte em `∂χ_X·(…)χ_Y + (X↔Y)`.

---

## 3. A identidade de consistência de ordem ℏ (o resultado central)

Fixe `Γ = S_χ + ℏW + O(ℏ²)`, `W = W^{(2)} + W^{(3)} + …` (`W^{(n)} ∝ κⁿ`), e a diferencial BRST linearizada `s_χ ≡ (S_χ, ·)` (ímpar). **Não se impõe `I_χ = 0`.**

**Passo 1 (Jacobi puro):** para `S_χ` par, a Jacobi graduada dá `(S_χ,(S_χ,F)) = ½((S_χ,S_χ),F)`, i.e.,

> **`s_χ² = (I_χ, ·)`** — a diferencial BRST **não é nilpotente** quando χ varia; seu quadrado é a ação adjunta da quebra clássica. `[DERIVED — Jacobi, sem normalização]`

**Passo 2 (QME por ordens):** `(Γ,Γ)/2 = iℏΔΓ` expande em

- ordem ℏ⁰: `(S_χ,S_χ)/2 = I_χ ≠ 0` (registrada como quebra clássica — não se anula);
- ordem ℏ¹: `(S_χ,W) − iΔS_χ ≡ A_χ` — a **anomalia candidata**. Se `A_χ ≠ 0`, é a quebra quântica da Ward localizada.

**Passo 3 (identidade de consistência):** aplicando `s_χ` em `A_χ` e usando o Passo 1 e a identidade BV `(S_χ,ΔS_χ) = Δ(I_χ)` (que se anula sob a hipótese `ΔS_χ = 0` `[INPUT]`):

> ### **`s_χ A_χ = (I_χ, W)`**
>
> A quebra quântica não é BRST-fechada por si só: fecha **a menos da inserção da quebra BV clássica não nula** agindo adjuntamente sobre W. Com χ uniforme, `I_χ → 0` e recupera-se a condição de Wess–Zumino usual `sA = 0` `[KNOWN]`. Esta é a identidade pedida, com a inserção explícita. `[DERIVED — Jacobi puro]`

**Cascata por ordens (acoplamento e ℏ explícitos):**

| ordem | identidade | conteúdo |
|---|---|---|
| ℏκ² | `s0 A^{(2)}_χ = 0` | WZ na teoria livre abelianizada (Jacobi; sem normalização de 3 vértices) |
| ℏκ³ | `s0 A^{(3)}_χ + s1_χ A^{(2)}_χ = (I^{(1)}_χ, W^{(2)})` | **primeira ordem em que a quebra clássica entra**: o lado direito usa `I^{(1)} = ∫∂χ·J_gf + B` (Blocos A e B) |
| ℏκ⁴ | `s0 A^{(4)}_χ + s1_χ A^{(3)}_χ = (I^{(1)}_χ, W^{(3)}) + (I^{(2)}_χ, W^{(2)})` | aqui entra a **polarização de dois vértices** `I^{(2)}(χ_X,χ_Y)` |

**Forma polarizada em dois vértices** (bilinearizando `s_χ² = (I_χ,·)` na ordem pertinente):

`s_{χ_X} A_{χ_Y} + s_{χ_Y} A_{χ_X} = 2·(I(χ_X,χ_Y), W)` `[DERIVED — com o fator 2 da convenção I(χ,χ) = (S_χ,S_χ)/2 declarado]`.

---

## 4. O papel de `[G,χ]w` e o termo de fonte necessário

**Fatoração (verificada à mão, `[DERIVED]`):** com `Q = C·G` vale `[Q,χ] = C[G,χ] + [C,χ]G`. Aplicado a `w`:

- `C[G,χ]w = C(∂^μχ w^ν + ∂^νχ w^μ) = (□χ)w_ν + ∂^μχ ∂_μ w_ν + ∂^νχ ∂·w`;
- `[C,χ](Gw) = ∂^μχ[(Gw)_{μν} − η_{μν}tr(Gw)/2] = ∂^μχ∂_μ w_ν + ∂^νχ∂·w − ∂^νχ∂·w = ∂^μχ∂_μ w_ν`.

Soma: `(□χ)w + 2(∂χ·∂w)` ✔ — reproduz `[Q,χ]w`. **Conclusão:** `[G,χ]w = (∂χ)·w` é a metade de 1ª ordem do comutador fantasma total — a metade do **setor de simetria** (gauge), distinta da metade do setor de gauge-fixing `[C,χ]Gw`. Omiti-lo quebra a fatoração e falsifica o sinal do termo fantasma da quebra.

**Termo de fonte necessário:** `[G,χ]w` é um composto local **sem fonte própria** em `Vaf_χ` (que só fonta `Z` e `w` com χ inteiro). Na ordem ℏκ³, a inserção `(I^{(1)}_χ, W^{(2)})` insere precisamente esse composto em W. Com fontes postas a zero **após** derivações (como no setor externo atual), essa inserção **não está definida pelos dados h,c**. O termo de fonte necessário é, portanto, o acoplamento da fonte ao composto `∂χ·w` (ou, equivalentemente, reter o canal `barc–w` com ∂χ até o fim) — é **dado adicional**, não decorre da matriz local `h,c`.

---

## 5. O que decorre de Jacobi × o que exige normalização de inserções compostas

| Jacobi / estrutural (sem escolhas) | Exige normalização de inserções compostas |
|---|---|
| Torre `s0²=0`, `s0Z+Gw=0`, `s1w=0`, `s0w=0` | `W^{(2)}, W^{(3)}` (**não fornecidos** — não se identifica W com ação efetiva calculada) |
| `s_χ² = (I_χ, ·)` e a identidade-mãe `s_χ A_χ = (I_χ, W)` | Coeficientes locais de `(I_χ, W)` (contrações de `∂χ·J` com vértices de W) |
| Comutadores `[C,χ]`, `[Q,χ]`, `[G,χ]` e a fatoração `Q=CG` | `ΔS_χ` (medida; a anulação é `[INPUT]`, não `[DERIVED]`) |
| Forma da corrente `J_gf` e identidade de borda fantasma `[REAL — artefato lido]` | Diagramas mistos b–h e corrente fantasma (`remain` no script) |
| Cascata de ordens ℏκ², ℏκ³, ℏκ⁴ | Coeficientes de Schwinger de `T{J_X J_Y}` (decidem a simetria WZ polarizada) |
| — | O funcional de borda cuja divergência foi descartada |

---

## 6. O dado adicional para testar Wess–Zumino (além da matriz local `h,c`)

Não basta citar a QME. Para executar o teste WZ da identidade `s_χ A_χ = (I_χ, W)` na prescrição local é preciso calcular, especificamente:

- **D1** — as correntes de contato clássicas completas: `J^μ_gf` (forma verificada no script) **e** a corrente de fontes `J^{†μ}` do Bloco B (a auditar);
- **D2** — as inserções de dois vértices com cutoff: `T{(κV_{χ_X})(x)(κV_{χ_Y})(y)}` e seus coeficientes de contato (Schwinger), nos canais `(hh), (hc), (cc), (b,h), (barc,c), (h†,h), (c†,c)` — incluindo os **diagramas mistos b–h e barc–w** declarados em aberto no script (`actual quantum mixed b-h and ghost current diagrams remain`);
- **D3** — a fonte do composto de contato `∂χ·w ≡ [G,χ]w` (§4); sem ela o lado direito `(I^{(1)},W)` não existe como inserção definida;
- **D4** — a avaliação da medida `ΔS_χ` (termos `δ(0)·tr`), ou a demonstração de sua anulação na prescrição adotada;
- **D5** — o funcional de borda associado a `div = −∂(∂χ·barc·w)` (e sua contraparte no setor b), para garantir que "módulo divergência" não esconde termo de borda anômalo.

---

## 7. Convenção de sinais de antifields

Na convenção BV canônica, `s φ† = −δS/δφ`; aqui adotou-se `s0 h† = +E_h`. A transformação é `h†_BV = −h†_aqui`, `c†_BV = −c†_aqui`: `Vaf_χ` muda por um sinal global, `I_χ` é invariante (os blocos são quadráticos na estrutura), e a peça linear em fontes muda de sinal **consistentemente**. Nenhum loop físico muda — vértices de fonte entram aos pares em qualquer diagrama com fontes a zero no fim. `[DECLARADO]`

---

## 8. Lacunas e o que NÃO se afirma

1. `W` não foi fornecido e **não é identificado** com ação efetiva alguma; `A_χ` é definida formalmente.
2. Coeficientes fechados do Bloco B e de `I^{(2)}` ficam `[OPEN — a auditar em CAS]`; apenas a estrutura e os cancelamentos em χ uniforme são `[DERIVED]`.
3. A verificação `s1 w = 0` polarizada é alvo do pré-registro, não reexecutada aqui.
4. **Não se anuncia obstrução cohomológica**: não foi demonstrado que o setor externo `h,c` (fontes a zero após derivações) satisfaça consistência homogênea para χ variável; um resíduo isolado não é obstrução.
5. `ΔS_χ = 0` é hipótese `[INPUT]`, não teorema desta unidade.
6. Não se procurou resposta numérica desejada; não se refez a corrente em X/Y nem o tadpole com referência variável (unidades distintas em andamento).
7. Escopo: auxiliar euclidiano ℝ⁴, sem identificação automática com a teoria lorentziana; exponenciais apenas como marcadores de jatos.

**Síntese:** a identidade de consistência de ordem ℏ é `s_χ A_χ = (I_χ, W)`, com `I_χ = κ(∫∂χ·J_gf + B) + κ²I^{(2)}` a quebra BV clássica não nula inserida adjuntamente — o lado esquerdo é Jacobi puro (`s_χ² = (I_χ, ·)`), e o cálculo do lado direito, na ordem ℏκ³ e na polarização de dois vértices em ℏκ⁴, exige exatamente os dados D1–D5, dos quais a matriz local `h,c` não contém nenhum.