# Revisão cética ORDEM_016 A-2.5.c — `NormalizedGraphWitness` e a transformada limitada do grafo

**Escopo:** os quatro arquivos fornecidos, lidos estaticamente. Não executo Lean nem acesso disco; o estado de compilação é **[DECLARADO]** pela bancada (`PARTIAL_ISOLATED_LEAN_AUDITED`). Os módulos importados (`TGLExt.BoundedGraphOperator`, `V350ResolventSquareRoot`, `V350PartialOperatorSquare`, `Continuous049`, `ContinuousModularDomain`) **não foram fornecidos** — leio seus enunciados apenas pelos usos; isso é uma lacuna desta revisão. Toda matemática que derivo abaixo é análise textual **[DERIVED — análise desta revisão]**, não verificada em kernel. Nada aqui anuncia solução física; o gate não é tocado.

---

## 1. Resposta curta à pergunta única

**Sim, com duas ressalvas precisas.** As hipóteses de `NormalizedGraphWitness` identificam `B` com `D(I+D²)^(−1/2)` *no sentido estrutural correto*, e o núcleo e o gap transportam corretamente (o gap com a constante **ótima**). Mas:

- **(R1)** a identificação é dada "de baixo para cima": os arquivos provam que `A²` é **inversa à direita** de `I+D²` e que `sqrt(A²) = A`; a passagem para **inversa bilateral** — sem a qual "`A = (I+D²)^(−1/2)`" é abuso de notação — exige a **injetividade de `I+D²`**, que segue de `D` **simétrico**, e a simetria (e a auto-adjuncia) de `D` **não é hipótese do witness nem está provada nos quatro arquivos**. É derivável das hipóteses do par por rota elementar (esboço no §4), mas está **ausente**: **[DERIVED condicional / OPEN como teorema do acervo]**.
- **(R2)** a existência do witness para `D` auto-adjunto densamente definido **arbitrário** não é tocada (o contrato a declara não-assumida, honestamente); a passagem exata que falta é decomposta no §6.

---

## 2. O que os arquivos de fato provam (leitura dos campos)

O witness carrega: `A, B` limitados, `0 ≤ A`, `IsSelfAdjoint B`, `A` injetivo, `A*B = B*A`, `A*A + B*B = 1`, e `represents : D = boundedGraphOperator A B injectiveA`. Sobre esse dado, com os lemas do v2:

| Afirmação | Status nos arquivos |
|---|---|
| `ambientKernel D = B.ker` | `graph_ambientKernel` — **[DERIVED, auditado]**; correto: `ker D = {Ax : Bx = 0}`, e `Bx = 0 ⟹ x = A²x ∈ ran A`, logo o kernel ambiente *é* `B.ker` inteiro |
| `‖Ax‖² + ‖Bx‖² = ‖x‖²` | `graph_pair_energy` — correto, usa auto-adjuncia dos dois |
| `‖Bx‖ ≤ ‖x‖` | `graph_transform_contraction` — correto |
| gap de `D` ⇒ gap de `B` com `γ ↦ γ/√(1+γ²)` | `graph_transform_gap` — correto e **ótimo** (§5) |
| `(I+D²)(A²z) = z` | `normalized_graph_inverse_one_add_square` — inversa **à direita** |
| `CFC.sqrt(A*A) = A` | `normalized_graph_normalizer_is_sqrt` — usa `positiveA` |

O passo `B = D∘A` é a própria definição do operador de grafo (`bounded_graph_lift_apply`): `D(Ax) = Bx`. Então a cadeia `A² = (I+D²)⁻¹` (falta bilateral) `⟹ A = (I+D²)^(−1/2)` (raiz única positiva, `positiveA` + `CFC.sqrt_unique`) `⟹ B = D·A = D(I+D²)^(−1/2)` está a **um lema de injetividade** de fechar — lema esse que depende de `D` simétrico (§4).

**Domínio:** por `represents`, `dom D = ran A` por construção — "domínio completo" vale *para o grafo*. Observação ausente mas elementar: `A` auto-adjunto injetivo ⟹ `ran A` denso (pois `(ran A)ᗮ = ker A* = ker A = 0`), logo `dom D` é denso **[DERIVED, não está nos arquivos — uma linha]**.

---

## 3. Circularidade

**Nenhuma circularidade interna detectada.** O desenho é honesto em dois pontos que merecem registro:

1. `NormalizedGraphWitness` **recebe** `represents` como dado e os teoremas só *derivam* propriedades; `BoundedTransformPreservesKernelAndGap` é enunciado como conclusão analítica, e o comentário do contrato declara explicitamente que a existência para `D` prescrito **não** é assumida. Nenhum teorema prova `T` assumindo a existência do witness geral.
2. A tentação circular estaria em *fechar a existência* escrevendo `A := (I+D²)^(−1/2)` via cálculo funcional de operador ilimitado — isso **é** equivalente à conclusão e está **proibido** pela pergunta. A cadeia do §6 não faz isso: a única entrada é a auto-adjuncia de `D` (dada na pergunta), e o objeto construído é o **resolvente** de `I+D²`, estritamente mais fraco que a transformada.

Um alerta de homônimo, porém: a rota do v3 (`resolventSquareRoot R` com `CFC.sqrt R`, `CFC.sqrt (1−R)`) constrói o par **ambos positivos**; o operador de grafo resultante é `|D|`, não `D` — `R = (I+D²)⁻¹` só vê `D²`, e `sqrt(1−R) = |D|(I+D²)^(−1/2)`. O v3 não afirma `resolventSquareRoot R = D` (correto), mas qualquer *estratégia de existência* que passe só pela v3 entrega o caso positivo; o sinal exige o passo P3 do §6.

---

## 4. Positivo vs. auto-adjunto

Os papéis estão **corretos e bem distribuídos** — esta é uma verificação que o cético deve fazer e aqui ela passa:

- `A` é tomado **positivo** (necessário: é o normalizador `(I+D²)^(−1/2)`, e `positiveA` alimenta `CFC.sqrt_unique` e a injetividade); `B` é tomado **só auto-adjunto** (correto: `B = D(I+D²)^(−1/2)` herda o *sinal* de `D`). Exigir `0 ≤ B` seria o erro; não é exigido.
- Consistência cruzada: `A*A + B*B = 1` com `A ≥ 0` força `B² = 1 − A²`, logo `|B| = sqrt(1−A²)` — exatamente o objeto do v3. O sinal de `B` é o único dado a mais, e é o sinal de `D`. Nenhuma confusão positivo/auto-adjunto nos enunciados; nos usos, a auto-adjuncia de `A` é sempre obtida de `positiveA` via `.isSelfAdjoint` (lema de mathlib **[DECLARADO]**).

O que **falta** no eixo "simetria/auto-adjuncia de `D`" (ausente dos quatro arquivos; esboço elementar):

- **`D` simétrico** [DERIVED — esboço]: para `u = Ax`, `v = Ay` no domínio,
  `⟨u, Dv⟩ = ⟨Ax, By⟩ = ⟨BAx, y⟩` e `⟨Du, v⟩ = ⟨Bx, Ay⟩ = ⟨ABx, y⟩`; iguais por `commute`. Uma linha dado o par.
- **`I+D²` injetivo** [DERIVED — esboço]: para `u ∈ dom D²`, `⟨(I+D²)u, u⟩ = ‖u‖² + ‖Du‖²` (simetria) `≥ ‖u‖²`, logo `(I+D²)u = 0 ⟹ u = 0`.
- **Inversa bilateral**: com `S := I+D²` injetivo e `A²` limitado com `S(A²z) = z` para todo `z` (teorema existente), `A² = S⁻¹`: `A²z = S⁻¹(S(A²z))`... direto: `S` injetivo + `S T = I` ⟹ `T = S⁻¹`. Então `A² = (I+D²)⁻¹` **[DERIVED condicional à simetria]**, e `A = (I+D²)^(−1/2)` por raiz única positiva (já invocada).
- **Auto-adjuncia de `D`** (não exigida pela identificação `B = D(I+D²)^(−1/2)`, mas pelo enquadramento "D auto-adjunto"): `(B+iA)(B−iA) = A²+B² + i(AB−BA) = 1` nas duas ordens (auto-adjuncia + comutação), logo `B±iA` são invertíveis limitados e `ran(D±i) ⊇ ran(B±iA) = H`; simétrico densamente definido com `ran(D±i) = H` ⟹ auto-adjunto (critério clássico) **[DERIVED — esboço; KNOWN clássico]**.

Nada disso está nos arquivos; é conteúdo novo e pequeno, sem CFC ilimitado.

---

## 5. Limite inferior vs. gap ótimo

O lema `graph_transform_gap` transporta *qualquer* limite inferior `γ` de `D` sobre `(ambientKernel D)ᗮ` para `γ/√(1+γ²)` em `B` sobre `B.kerᗮ`. Três verificações:

1. **A constante é ótima.** No caso escalar (`A = cos θ`, `B = sin θ`, `D = tan θ`), o gap de `D` é `|tan θ|` e o de `B` é `sin θ = γ/√(1+γ²)` — igualdade. A prova dos arquivos (via `‖Ax‖² + ‖Bx‖² = ‖x‖²`) atinge essa mesma conta; não há perda escondida.
2. **Não há confusão bound/gap.** Os arquivos transportam *bounds* e **não** afirmam otimalidade nem supremo — correto; não leem "gap espectral" onde há "lower bound". (Registro: a transformação inversa `c ↦ c/√(1−c²)` também é exata pela mesma identidade de energia, de modo que o gap *ótimo* de `B` determina o de `D`; os arquivos não precisam disso e não o afirmam.)
3. **Formulação do ortogonal.** A hipótese é sobre `(u : H) ⊥ ambientKernel D` no ambiente; como `ambientKernel D = subtype '' ker D`, isso coincide com `u ⊥ ker D` — bem formulada; e a preservação `A(B.kerᗮ) ⊆ B.kerᗮ` (`graph_pair_preserves_orthogonal`, via comutação + auto-adjuncia) é exatamente o elo que o lift consome. Correto.

---

## 6. A passagem exata que falta para a existência para `D` arbitrário

Nenhum dos quatro arquivos constrói o par a partir de `D`. A lacuna declarada pela bancada é real e se decompõe assim — **cadeia livre de CFC ilimitado**, reusando os lemas V350 onde eles de fato entram:

**P1 — o resolvente [OPEN em kernel; KNOWN clássico].** De `D : H →ₗ.[ℂ] H` densamente definido auto-adjunto, construir `R : H →L[ℂ] H` com
`0 ≤ R ≤ 1`, `R` injetivo, `R` auto-adjunto, e `(I+D²)(Rz) = z` para todo `z`.
Rota: `ran(D±i) = H` (auto-adjuncia) ⟹ `(D−i)(D+i) = I+D²` sobre `dom D²` sobrejetivo; `‖(I+D²)u‖ ≥ ‖u‖` (§4) dá inversa limitada; `⟨Rz, z⟩ = ‖Rz‖² + ‖DRz‖² ≥ 0` dá positividade. **Esta é a única peça com análise de ilimitados, e é a mínima possível — não é equivalente à conclusão** (é o resolvente, não a transformada). Disponibilidade na mathlib do acervo: **não verificável aqui** — pendência declarada.

**P2 — comutação e core [DERIVED — esboços elementares].** (a) `DR ⊂ RD`: para `w ∈ dom D`, checa-se `DRw ∈ dom D²` e `(I+D²)DRw = Dw`, logo `DRw = RDw`. (b) `D f(R) ⊂ f(R) D` para `f` contínua: polinômios `pₙ → f` uniformemente; para `w ∈ dom D`, `pₙ(R)w → f(R)w` e `D pₙ(R)w = pₙ(R)Dw → f(R)Dw`; `D` fechado conclui. (c) `ran R = dom D²` (da construção). (d) `dom D²` é core de `D`: se `u ⊥ dom D²` na norma do grafo, `⟨u,(I+D²)v⟩ = 0` para todo `v ∈ dom D²`, e a sobrejetividade de P1 dá `u = 0`.

**P3 — o par [conteúdo novo de kernel; rotina clássica].** `A := CFC.sqrt R` (CFC **limitado**, disponível; injetividade: `A² = R` injetivo basta — ou `positive_sqrt_injective` do acervo). `B :=` fecho de `D∘A`: definido sobre `{x : Ax ∈ dom D²} ⊇ ran R` (denso); **limitação** (conta conferida nesta revisão): sobre `ran R`,
`‖DAx‖² = ⟨D²(Ax), Ax⟩ = ⟨A D²x, Ax⟩ = ⟨D²x, Rx⟩ = ⟨x,(1−R)x⟩ ≤ ‖x‖²` (comutação P2b + `D²R = 1−R`); auto-adjuncia pelo fecho; e sobre `ran R`: `B²x = D(A(DAx)) = D(RDx) = D²Rx = (1−R)x`, logo `B² = 1−R` e `A²+B²=1`; `AB=BA` sobre o denso por P2b, ambos limitados. **Os lemas `resolvent_sqrt_pair_commute` / `resolvent_sqrt_pair_square_sum` não se aplicam a este `B` (são sobre `sqrt(1−R)`)** — cobrem o caso positivo (§3); aqui as identidades análogas são o conteúdo novo, porém provadas sobre `ran R` como acima.

**P4 — a igualdade `represents` [elementar dados P1–P3; é o "domínio completo"].** `D = boundedGraphOperator A B _`: (⊇) sobre `ran A² = ran R`, `D(A²z) = D(A·Az) = B(Az)` pela definição de `B`; (⊆) porque ambos são fechados e `dom D² = ran R` é core de `D` (P2c/d): para `u = Ax`, tome `wₙ ∈ ran A → x` (denso), `uₙ := Awₙ ∈ ran R`, `uₙ → u`, `Duₙ = Bwₙ → Bx`, e `D` fechado dá `u ∈ dom D ∧ Du = Bx`. **Este passo é indispensável mesmo no caso positivo via v3** — a v3 constrói o operador do resolvente, mas não identifica seu grafo com um `D` prescrito.

Com o witness montado, `normalized_graph_pays_contract`, `normalized_graph_inverse_one_add_square` e `normalized_graph_normalizer_is_sqrt` disparam sem alteração (só pedem os campos). **Resumo da resposta:** a passagem exata que falta é **P1** (resolvente limitado de `I+D²` a partir da auto-adjuncia) mais **P4** (identificação do `LinearPMap` dado com o grafo do par, domínios incluídos); no caso com sinal, adicionalmente **P3** (`B :=` fecho de `D∘√R`), porque a rota V350 do resolvente entrega `|B| = √(1−R)`.

---

## 7. Estatutos e lacunas desta revisão

- **[DECLARADO — bancada]:** compilação e axiomas limpos dos quatro arquivos (`PARTIAL_ISOLATED_LEAN_AUDITED`); enunciados dos módulos importados, lidos só pelos usos.
- **[DERIVED — esta revisão]:** correção dos teoremas dados; otimalidade de `γ/√(1+γ²)`; ausência de circularidade; os esboços do §4 (simetria/injetividade/bilateral/auto-adjuncia de `D`) e de P2–P4; o ponto `|D|` vs. `D` na rota do resolvente.
- **[OPEN]:** existência do witness para `D` auto-adjunto densamente definido arbitrário — reduzida a P1 + P4 (+ P3 com sinal); disponibilidade de P1 na mathlib não verificada por mim aqui (sem execução, sem disco).
- **Lacunas desta revisão:** não verifiquei `#print axioms`; não li `bounded_graph_equation_iff`, `boundedGraph_square_eq_resolvent`, `resolventSquareRoot_square`, `resolvent_graph_resolvent_equation` na fonte — se algum deles tiver hipótese mais forte que a usada, o §2 se enfraquece no ponto correspondente. `ClosedLinearGraphResolvent.lean` de fora, conforme instruído.

`NOT_FALSIFIED ≠ CONFIRMED`; aqui: auditado-pela-bancada ≠ re-verificado-por-mim.