# A-7.b — Do contato euclidiano ao Feynman lorentziano: a transferência meromorfa com boundary value

**Estatuto desta entrega:** `[DECLARADO até auditoria local]`. Análise escrita, sem execução de código, sem acesso a arquivos locais. As fontes anexas foram **lidas, não rodadas**: `logarithmic_contact_engine.py` (linhas 1–51), `results.json` (42 checks, `ZERO_LOG_RESIDUE_NONZERO_FINITE_CONTACT`, controle negativo `-1`) e `DERIVACAO.md` (contato `(R(∂Xi∂Yj z⁻¹)−∂Xi∂Yj z⁻¹)/C = δij δ/4`, `C_E = −4π²`, Q2 completa `OPEN`, "continuação lorentziana não incluída"). Os dados do recorte entram como `[INPUT]`; toda a matemática abaixo é derivada por extenso e é localmente verificável. Não rederivo contatos de curvatura (instrução explícita do pedido).

---

## 1. Convenções fixadas (sem ambiguidade posterior)

- **Métrica:** `η = diag(−1,+1,+1,+1)`. Coordenadas `x = (x⁰, x⃗)`, `x_μ = η_μν x^ν`.
- **Invariantes:** euclidiano `z_E = Σᵢ (Xᵢ)²` (o `z` do código); lorentziano `σ(x) = η_μν x^μ x^ν = −(x⁰)² + x⃗²`.
- **Operadores:** `Δ = Σᵢ ∂ᵢ²` (euclidiano); `□ = η^μν ∂_μ∂_ν = −∂₀² + ∇²`.
- **Fourier:** `p·x := η_μν p^μ x^ν = −p⁰x⁰ + p⃗·x⃗`;
  `f̃(p) = ∫ d⁴x e^{+ip·x} f(x)`; `f(x) = ∫ d⁴p/(2π)⁴ e^{−ip·x} f̃(p)`.
- **Boundary value (Feynman):** `(σ+i0)^λ := lim_{ε↓0} (σ+iε)^λ` em `𝒟'`, ramo principal do log (para `σ>0`, `log(σ+iε) → ln σ`). Em `p`: `(p²+i0)⁻¹` idem. **Contorno de Schwinger:** `α ∈ (0,∞)` com `+i0` no exponencial.
- **Regulador liso auxiliar:** `(σ+iε)⁻¹`, `ε>0` — para `ε>0` é `C^∞`, pois `σ+iε` nunca se anula.

---

## 2. O recorte euclidiano, reverificado por escrito

**Normalização (fluxo).** Para `X ≠ 0`, `∇ z_E⁻¹ = −2X/z_E²`; na esfera `|X| = ρ`: `∂_n = −2/ρ³`; área `|S³| = 2π²ρ³`. Fluxo `= −2/ρ³ · 2π²ρ³ = −4π²`, independente de `ρ`. Logo

```
Δ z_E⁻¹ = −4π² δ⁴(X)  ≡  C_E δ⁴,        C_E = −4π².            (E1)
```

**Segunda derivada.** Fora da origem: `∂ᵢ∂ⱼ z_E⁻¹ = −2δᵢⱼ/z_E² + 4XᵢXⱼ/z_E³`. Como distribuição há um contato na origem, e por covariância `O(4)` ele é `c δᵢⱼ δ⁴`. Traço: `4c = C_E = −4π² ⟹ c = −π²`. Logo

```
∂ᵢ∂ⱼ z_E⁻¹ = p.f.(∂ᵢ∂ⱼ z_E⁻¹) − π² δᵢⱼ δ⁴
⟺ R(∂ᵢ∂ⱼ z_E⁻¹) − ∂ᵢ∂ⱼ z_E⁻¹ = C_E δᵢⱼ δ⁴/4.                 (E2)
```

Casa exatamente com o `[INPUT]` do recorte (`C_E = −4π²`, `/C = δᵢⱼ δ/4`). **Observação estrutural que guiará tudo:** o contato de segunda derivada é sempre **(constante de `Δ` ou `□` do objeto) × métrica/4** — o traço fixa a constante, a covariância fixa o tensor.

---

## 3. Qual é a transferência rigorosa (e o que ela não é)

**Resposta à pergunta única.** A transferência rigorosa **não** é rotação de Wick de estados nem troca formal de assinatura: é a **continuação analítica comum na família meromorfa de distribuições homogêneas (Gel'fand–Shilov), com o ramo lorentziano fixado pela prescrição de Feynman `(σ+i0)^λ`**. As duas famílias — `z_E^λ` e `(σ+i0)^λ` — obedecem à **mesma identidade diferencial formal**, que é o que faz a prescrição do recorte (comparar derivação ↔ finite part) ser transportável:

```
Δ z_E^λ = 4λ(λ+1) z_E^{λ−1}        □ (σ+i0)^λ = 4λ(λ+1) (σ+i0)^{λ−1}   (E3)
```

(verificação direta: `∂_μ σ^λ = 2λx_μ σ^{λ−1}`, `□σ^λ = 8λσ^{λ−1} + 4λ(λ−1)σ^{λ−1} = 4λ(λ+1)σ^{λ−1}` ✓; idem euclidiano). Ambas têm polos simples em `λ = −2, −4, …`, com resíduos proporcionais a `Δᵏδ⁴` / `□ᵏδ⁴`. A prescrição do problema — extensão meromorfa com fator `(1−a) μ^{2a} (·)^a` — aplica-se então **no mesmo transporte**:

```
R_E[f] = FP_{a→0}[(1−a) μ^{2a} z_E^a · f]        (o que o código implementa)
R_L[f] = FP_{a→0}[(1−a) μ^{2a} (σ+i0)^a · f]      (versão lorentziana)   (E4)
```

com a regra de derivada idêntica à do código (`differentiated`, linhas 8–19): `∂_μ (σ+i0)^{a−p} = 2(a−p) x_μ (σ+i0)^{a−p−1}`, que é a regra do código com `signature[i] = η_ii`. **O que muda, e só o que muda:** (i) o ramo `(σ+i0)^a = e^{a log(σ+i0)}` (ausente no euclidiano, onde `z_E > 0` fora da origem); (ii) as constantes de normalização dos resíduos, que **não** vêm da álgebra — vêm da normalização do propagador, derivada a seguir.

---

## 4. Normalização de `D_F` derivada (onde nasce o fator `i`)

Defina `D_F(x) := i ∫ d⁴p/(2π)⁴ e^{−ip·x}/(p²+i0)`. Duas contas independentes.

**(a) Ação de `□` (fixa o múltiplo de `δ`).** `□ e^{−ip·x} = −p² e^{−ip·x}`, e dentro da família meromorfa `p²·(p²+i0)⁻¹ = 1` (multiplicação pelo polinômio na família — dependência declarada da teoria GS, que é a prescrição do próprio problema). Logo

```
□ D_F = i ∫ d⁴p/(2π)⁴ e^{−ip·x} (−p²)/(p²+i0) = −i ∫ d⁴p/(2π)⁴ e^{−ip·x} = −i δ⁴(x).   (E5)
```

**(b) Forma em `x` (fixa a constante e a fase).** Schwinger: `(p²+i0)⁻¹ = −i ∫₀^∞ dα e^{iα(p²+i0)}`. Gaussiana lorentziana (por completar quadrado + contorno; regularização `e^{(ic−0⁺)u²}`):

```
∫ du e^{icu²+ibu} = √(π/|c|) e^{i sgn(c)π/4} e^{−ib²/(4c)}
⟹ ∫ d⁴p e^{iαp² − ip·x} = √(π/α)e^{−iπ/4}e^{i(x⁰)²/4α} · (π/α)^{3/2}e^{+3iπ/4}e^{−ix⃗²/4α}
                         = i π² α⁻² e^{−iσ/(4α)}.                                       (E6)
```

**A fase `e^{iπ/2} = i` é literalmente `√i` por dimensão temporal** (`e^{−iπ/4}` contra três `e^{+iπ/4}`). Com a substituição `β = 1/(4α)` (`α⁻²dα = 4dβ`) e Sochozki–Plemelj 1D — prova local de uma linha: `∫₀^∞ e^{−iσβ−εβ}dβ = (ε+iσ)⁻¹ → πδ(σ) − i p.v.(1/σ) = −i/(σ+i0)`:

```
∫ d⁴p/(2π)⁴ e^{−ip·x}/(p²+i0) = (π²/(2π)⁴)·4·(−i)/(σ+i0) = −i/(4π²) · 1/(σ+i0)
⟹  D_F(x) = 1/(4π²) · 1/(σ + i0),       □ D_F = −i δ⁴.                                (E7)
```

**Comparação com o euclidiano:** `G_E = 1/(4π² z_E)`, `Δ G_E = −δ⁴`. Mesma constante `1/4π²`; a única diferença de normalização é `Δ ↦ □` acompanhado de `δ⁴ ↦ i·δ⁴`. **Registro do que isso significa:** a continuação formal `x⁰ = −iX⁴` aplicada a `D_F` não reproduz `G_E` (arrasta `i`'s inconsistentes) — porque `D_F` não é uma função, é um boundary value; a substituição de variável em distribuições singulares no cone não é a troca formal. Este é o primeiro sintoma do que a troca de assinatura não captura.

---

## 5. O contato lorentziano de segunda derivada

**Forma.** Por (E3) com `λ = −1`, `□(σ+i0)⁻¹ = 0` fora da origem; pela normalização (E7), `□(σ+i0)⁻¹ = 4π²·(−i)δ⁴ = −4π² i δ⁴ ≡ C_L δ⁴` com

```
C_L = −4π² i.                                                                       (E8)
```

A prescrição de Feynman `(σ+i0)⁻¹` é invariante por `SO⁺(1,3)` (`σ` é invariante e `i0` não depende de referencial). Logo o contato de `∂_μ∂_ν` é `κ η_μν δ⁴`, e o traço fixa `4κ = C_L ⟹ κ = −π² i`:

```
∂_μ∂_ν (σ+i0)⁻¹ = p.f.∂_μ∂_ν(σ+i0)⁻¹ − π² i η_μν δ⁴
⟺ R_L(∂_μ∂_ν(σ+i0)⁻¹) − ∂_μ∂_ν R_L((σ+i0)⁻¹) = C_L η_μν δ⁴/4.                       (E9)
```

E para o propagador (`D_F = (4π²(σ+i0))⁻¹`):

```
R_L(∂_μ∂_ν D_F) − ∂_μ∂_ν R_L(D_F) = −(i/4) η_μν δ⁴.                                (E10)
```

**A forma é a mesma do euclidiano** (`−(1/4)·métrica·δ⁴`, cf. (E2)); o conteúdo transferido é `δᵢⱼ ↦ η_μν` e `C_E = −4π² ↦ C_L = −4π² i`.

**Checagem pelo traço com `η` (pedida explicitamente):**

```
η^μν C_μν = −π² i · η^μνη_μν = −4π² i δ⁴ = C_L δ⁴   ✓ (= contato de □(σ+i0)⁻¹)
η^μν(−i/4 η_μν) = −i δ⁴                              ✓ (= □ D_F)
```

**Checagem por componentes (temporal e espacial, pedidas):**

```
temporal  C_00 = −π² i · η_00 = +π² i δ⁴      (η_00 = −1)
espacial  C_11 = −π² i · η_11 = −π² i δ⁴      (η_11 = +1)
razão temporal/espacial = −1 ✓ (assinatura)
soma com pesos η: −(+π² i) + 3(−π² i) = −4π² i ✓
```

**Checagem de suporte com o regulador liso.** `∂_μ∂_ν(σ+iε)⁻¹ = −2η_μν(σ+iε)⁻² + 8x_μx_ν(σ+iε)⁻³`; o traço fecha identicamente: `η^μν[…] = −8(σ+iε)⁻² + 8σ(σ+iε)⁻³ = 8iε/(σ+iε)⁻³`, e `∫ φ·8iε/(σ+iε)³ → ⟨□(σ+i0)⁻¹, φ⟩ = −4π² i φ(0)` ✓ — a convergência `ε↓0` em `𝒟'` é a dependência declarada da continuação GS (a mesma prescrição do problema). **Declaração honesta:** a separação de *qual termo* carrega o `δ⁴` dentro da soma é esquema-dependente; o contato total não é — ele está fixado por traço + covariância.

---

## 6. O que a troca `signature=(1,1,1,1) → (−1,1,1,1)` no código não captura

Lendo `logarithmic_contact_engine.py`: `signature` entra (i) na regra de derivada (linha 17: `2·signature[i]·(A−power)`), algebricamente correta para métrica diagonal; (ii) na fórmula de resíduo (linhas 22–26: `f = (Σ sigᵢ Qᵢ²)^{n−2}`), que é a fórmula GS **real** dos resíduos polinomiais. Trocando a assinatura, a máquina produz contatos `∝ η_μν` com a **constante real** `C = −4π²`. Confronto com o Feynman correto:

| quantidade | troca de signature (real) | Feynman correto (E9) |
|---|---|---|
| traço | `−4π² δ⁴` | `−4π² i δ⁴` |
| temporal | `+π² δ⁴` | `+π² i δ⁴` |
| espacial | `−π² δ⁴` | `−π² i δ⁴` |

Sinais relativos corretos; **fase ausente**. A lista completa do que se perde:

1. **O fator `i` global** (`□ D_F = −iδ⁴` vs `Δ G_E = −δ⁴`). Origem: a fase `e^{iπ/2}` da gaussiana lorentziana (E6), ou `∫₀^∞ e^{−iσβ}dβ = −i/(σ+i0)`. A troca de assinatura é uma operação real e não gera `i`.
2. **O boundary value / a escolha de ramo.** `(σ+i0)⁻ⁿ` (Feynman), `(σ−i0)⁻ⁿ` (anti-Feynman), `(σ + i0·sgn t)⁻¹` (Wightman), retardado, e a "principal" `(F+antiF)/2` compartilham a mesma álgebra real de coeficientes e **diferem exatamente na fase e nos termos no cone**. O código não contém `i0` em nenhuma linha.
3. **O contato suportado no cone.** Fora da origem (`dσ ≠ 0`), Sochozki é legítimo por redução a uma variável transversal e dá `1/(σ+i0) = p.v.(1/σ) − iπδ(σ)`: a **parte imaginária vive no cone inteiro**. A fórmula de resíduos polinomiais só produz termos `δ⁴` (origem) e nenhum `δ(σ)`, `δ'(σ)`, `δ''(σ)` — que importam ao multiplicar por outras distribuições singulares no cone (o contexto Q2 do acervo).
4. **A inconsistência da decomposição ingênua na origem (controle negativo interno, decisivo).** Tome a "principal" `p.v.(1/σ) := (F + antiF)/2`: `□ p.v.(1/σ) = ½(−4π² i + 4π² i)δ⁴ = 0`. E formalmente `□δ(σ) = 8δ'(σ) + 4σδ''(σ) = 8δ' − 8δ' = 0` (a composta é homogênea — tipo Pauli–Jordan). Então `p.v. − iπδ(σ)` daria traço `0 + 0 = 0 ≠ −4π² i`. **A decomposição de Sochozki falha na origem (onde `dσ = 0`); o `−4π² i δ⁴` mora justamente nessa falha.** A troca de signature, sendo real, não reproduz nem Feynman (falta `i`) **nem a principal** (dá `−4π² ≠ 0`) — produz um híbrido que não corresponde a nenhuma prescrição lorentziana natural. A linguagem sem ambiguidade é a família `(σ+i0)^λ`, não a escrita `p.v. + δ(σ)`.
5. **O log por setor (relevante para `ell ≥ 1`).** `log(σ+i0) = ln|σ| + iπ` nas regiões temporais (`σ<0`); a prescrição `(1−a)μ^{2a}(σ+i0)^a` carrega `e^{iπa}` por setor. A troca usa log real com sinais — finite parts e contatos com logs saem alterados.

**O que a troca captura corretamente:** a estrutura tensorial `η_μν` (sinais relativos temporal–espacial), a regra de derivada dos coeficientes, e a combinatória GS dos resíduos com `□ᵏδ` no lugar de `Δᵏδ` (sinais inclusos).

**Controle negativo proposto (para auditoria local; não alego execução):**
- **CN1 (ramo conjugado):** computar com `(σ−i0)⁻¹`: deve dar `C_L* = +4π² i`. Se a máquina não distingue ramos, está reprovada para Feynman.
- **CN2 (principal):** a média dos ramos deve ter traço de contato **nulo**; a troca de signature dá `−4π² ≠ 0` ⟹ reprovada como "principal".
- **CN3 (cone fora da origem):** num ponto do cone com `dσ ≠ 0`, comparar `(σ+iε)⁻¹` (parte imaginária não nula) com a fórmula real de sinais (parte imaginária nula): reprova a troca no cone.
- **CN4 (fraco, declarado):** razão temporal/espacial `= −1` — passa nos dois esquemas; não discrimina.

---

## 7. Igualdade local de resíduos ≠ rotação de Wick de um estado (declaração exigida)

O que foi transferido aqui é uma **propriedade local**: a álgebra de contatos da **parametrix** (a parte singular de Hadamard). Ela é determinada pela métrica no ponto e pela família meromorfa — em espaço-tempo curvo, a parametrix `U(x,y)/(σ(x,y) + i0) + V log(σ+i0) + W` (`σ` = meia distância geodésica assinada, `U,V,W` suaves) tem a mesma estrutura singular local, e os contatos de segunda derivada **recebem correções de curvatura** — que **não rederivo**, por instrução explícita do pedido (estão distribuídos a outros revisores).

A **rotação de Wick de um estado completo** — a tese de que a função de dois pontos de Wightman de um estado físico lorentziano é boundary value de uma Schwinger function analítica — é uma propriedade **global**, exige analiticidade/positividade de reflexão, e em espaço-tempo curvo genérico **não existe** (não há "o" euclidiano de um lorentziano genérico; onde há — estáticos — a rotação é na coordenada temporal e o estado é o térmico). **Nada disso foi pressuposto aqui**: trabalhei no plano, com a parametrix lisa e a família meromorfa. Duas observações de fronteira, declaradas: (i) Feynman `(σ+i0)⁻¹` não é boundary value do tubo futuro simples (`1/σ(z)` tem polos no tubo; o domínio correto é o de Jost) — contexto, não dependência da conta; (ii) a prescrição `(σ+i0)^λ` é a definição operacional adotada, independente de qualquer teorema global de boundary values.

---

## 8. Hipóteses, dependências e lacunas

- **H1** A prescrição de extensão é a meromorfa dada pelo problema (`(1−a)μ^{2a}(·)^a`), idêntica à implementada no código — não é citação externa.
- **H2** O ramo lorentziano é Feynman (`(σ+i0)^λ`) — parte do enunciado ("distribuição de Feynman"); outros ramos mudam a resposta (CN1).
- **H3** Convergência `ε↓0` em `𝒟'` dos reguladores lisos — conteúdo da continuação GS (dependência declarada).
- **H4** Únicas identidades usadas: Sochozki–Plemelj 1D (prova local incluída, §4) e a gaussiana oscilatória (derivação incluída, E6). **Nenhum teorema de boundary values geral foi usado; nenhuma citação não consultada.**
- **Lacunas declaradas:** (a) a decomposição `p.v. + δ(σ)` em 4D indefinido é heurística fora da origem e falha na origem (§6.4) — a família GS é a forma rigorosa; (b) os termos no cone foram localizados, não expandidos em bases (desnecessário à pergunta); (c) contatos de curvatura — fora por instrução; (d) nada aqui seleciona estado físico nem promove a QME (o `DERIVACAO.md` já declara Q2 `OPEN`; esta entrega cobre exatamente o passo "continuação lorentziana" que o recorte declara não ter feito).
- **Não executado por mim:** nenhuma rodada do código; os checks citados (`42`, `336`, `328`, controle `-1`) são lidos dos artefatos anexos, não reproduzidos nesta chamada.

---

## 9. Resumo dos resultados `[DECLARADO até auditoria local]`

```
Transferência rigorosa: família meromorfa GS comum + ramo Feynman (σ+i0)^λ.
NÃO é: rotação de Wick de estados; NÃO é: a troca formal de signature.

Euclidiano:   Δ z_E⁻¹ = C_E δ⁴,   C_E = −4π²
              R(∂ᵢ∂ⱼ z_E⁻¹) − ∂ᵢ∂ⱼ z_E⁻¹ = C_E δᵢⱼ δ⁴/4        [= INPUT do recorte ✓]

Lorentziano:  D_F(x) = 1/(4π²) · (σ+i0)⁻¹,   □ D_F = −i δ⁴
              □ (σ+i0)⁻¹ = C_L δ⁴,   C_L = −4π² i
              R_L(∂_μ∂_ν (σ+i0)⁻¹) − ∂_μ∂_ν R_L((σ+i0)⁻¹) = C_L η_μν δ⁴/4
              R_L(∂_μ∂_ν D_F) − ∂_μ∂_ν R_L(D_F) = −(i/4) η_μν δ⁴

Verificações: traço η = −4π² i ✓; temporal +π² i ✓; espacial −π² i ✓;
              regulador liso no traço ✓; CN1–CN2 reprovam a troca de signature.

O que a troca signature perde: fase i global; ramo/boundary value;
termos no cone δ(σ), δ'(σ), δ''(σ); log por setor (ell ≥ 1);
e a própria consistência da p.v. real na origem (traço 0 vs −4π²).
O que ela preserva: sinais η_μν, álgebra de derivadas, combinatória □ᵏδ.
```

`NOT_FALSIFIED ≠ CONFIRMED`. Resultado **DECLARADO**; nenhuma execução, compilação ou escrita foi realizada nesta chamada; os controles CN1–CN3 são propostos para a auditoria local, não reportados como corridos.