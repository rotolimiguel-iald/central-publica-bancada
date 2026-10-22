## Resposta à unidade A3 (pergunta única) — revisão cética da ponte operador → pontual

**Declaração de regime:** não executei Lean; não compilei nada. A evidência local (`OrbitTranslationFaithfulness_v2.lean`, SHA256 `6c2104…` conforme declarado no pedido) reporta rc0 e sete declarações auditadas — trato isso como `[DECLARADO pela evidência local]`, não como verificação minha. Nomes Mathlib citados adiante são **sugestões não verificadas**. Nada aqui move gate, bandeira ou selo.

---

### 1. Veredito direto

**Não, as sete declarações anexadas não bastam sozinhas.** Elas provam exatamente a metade *pontual*: `∀ p ∈ órbita, phase(orbitPairing a p) = 1 ⟹ a = 0`. A hipótese física da fidelidade é *operacional*: `U(a) = I` em `L²(μ_L)`, que é uma afirmação **a.e.**. Entre as duas há uma ponte de teoria da medida que **não está** no arquivo. A ponte existe, é pequena e padrão (4 lemas novos + 1 colagem + composição por caso), e com ela as sete declarações **fecham os três casos sem alteração**. Abaixo: a revisão cética, o contraexemplo que torna a ponte *necessária* (não ornamental), e a sequência mínima de lemas com hipóteses.

---

### 2. Revisão cética: onde a inferência quebra sem a ponte

**2.1. O defeito exato (como o pedido nomeia).** Os teoremas anexados (`null_orbit_faithful`, `massive_orbit_faithful`, `doubled_null_character_faithful`) consomem a fase **em todos os pontos da órbita**, e a prova avalia essa fase em **momentos sobre eixos** (`axisMomentum r (±r) j`, `(m+r, √(…))`, `(m,0)`). Na medida invariante `d³p/p₀` (equivalente a Lebesgue em ℝ³, resp. ℝ³∖{0}), esses conjuntos são curvas/planos: **medida zero**. Igualdade a.e. do multiplicador **não se avalia** em conjuntos de medida zero. Logo a hipótese dos teoremas é *estritamente mais forte* que a hipótese operacional, e a inferência direta é inválida.

**2.2. Contraexemplo à formulação insuficiente** `[DERIVED — construído nesta revisão]`. Tome, na órbita m=0 parametrizada por ℝ³∖{0}, a medida **com buraco de suporte**
`μ' = 1_V · (d³p/|p|)`, onde `V = (ℝ³∖{0}) ∖ W` e `W` é um tubo aberto em torno do semieixo `{p₂=p₃=0, p₁>0}` (o raio usado pela prova para `j=0`). Escolha `a ≠ 0` com `a⁰ − a¹ ≠ 0`. Então:

- no raio, a fase é `exp(i r (a⁰−a¹))`, que vale `−1` em `r = π/(a⁰−a¹)` — ponto **dentro** de `W` (isto é exatamente o mecanismo de `phase_positive_ray_faithful`);
- mas `W` é `μ'`-nulo, logo `M_a = 1` `μ'`-a.e., logo **`U(a) = I` em `L²(μ')` com `a ≠ 0`**.

A fidelidade **falha** sob `μ'`, precisamente porque o suporte não é pleno: o operador não enxerga o aberto onde a fase difere de 1. Conclusão cética: *suporte pleno + continuidade não são detalhes técnicos — são as hipóteses que carregam o teorema.* Sem elas, a inferência é falsa; com elas, é trivial. É por isso que a medida pretendida `d³p/p₀` (densidade estritamente positiva) **entra como hipótese de trabalho, não como pano de fundo**.

**2.3. Segundo modo de falha (mais banal, igualmente fatal).** Alterar `M_a` num conjunto de medida zero (por exemplo, impor `M_a = −1` nos pontos de eixo) não muda o operador `U(a)`. Se alguém lesse a hipótese dos teoremas anexados como "vale a.e. e portanto nos eixos", estaria cometendo o erro que a ponte existe para bloquear.

---

### 3. A ponte: sequência mínima de lemas

**Já anexados** `[REAL — kernel, conforme evidência local; não reexecutado por mim]`: **L1** `phase_positive_ray_faithful`, **L2** `phase_difference`, **L3** `pairing_axis`, **L4** `axis_in_shell`, **L5** `null_orbit_faithful`, **L6** `massive_orbit_faithful`, **L7** `doubled_null_character_faithful`.

**Novos** (a construir pela sessão Codex; cada um pequeno e separadamente verificável):

**N1 — Leitura operacional** `[DEF]`. Espaço `L²(H_m⁺, μ_L)`, `μ_L = d³p/p₀` na parametrização `p ↦ (p₀ = √(m²+|p|²), p)` (m>0), resp. `p ↦ (|p|, p)` sobre ℝ³∖{0} (m=0, vértice excluído). `(U(a)f)(p) = phase(orbitPairing a p)·f(p)`. Hipótese de fidelidade: `U(a) = I` como operadores, i.e., `∀ f ∈ L²: M_a f = f` a.e., com `M_a(p) := phase(orbitPairing a p)`.

**N2 — Lema do multiplicador identidade** `[KNOWN — padrão de teoria da medida; OPEN no kernel]`.
*Hipóteses:* `(X, Σ, μ)` σ-finito; `M` mensurável, `|M| = 1` a.e.; `Mf = f` a.e. para todo `f ∈ L²(μ)`.
*Tese:* `M = 1` μ-a.e.
*Prova:* σ-finitude dá `X = ⋃ₙ Eₙ` com `μ(Eₙ) < ∞`. Cada `1_{Eₙ} ∈ L²` (norma² = `μ(Eₙ)`). Da hipótese com `f = 1_{Eₙ}`: `(M−1)·1_{Eₙ} = 0` a.e., i.e. `∫_{Eₙ} |M−1|² dμ = 0`, logo `M = 1` a.e. em `Eₙ` (integrando não-negativo). União enumerável de nulos é nula. ∎ — *Este é o passo "testes L² de suporte finito" pedido: só se testam funções características de conjuntos de medida finita.*

**N3 — σ-finitude de `μ_L`** `[DERIVED — cálculo elementar; OPEN no kernel]`.
*Hipótese:* a parametrização acima.
*Tese:* `μ_L` é σ-finita.
*Prova:* cobrir por `Kₙ = {|p| ≤ n}`. m>0: `μ_L(Kₙ) = ∫_{|p|≤n} d³p/√(m²+|p|²) ≤ (4π/3)n³/m < ∞`. m=0: `μ_L(Kₙ) = ∫_{|p|≤n} d³p/|p| = 2πn² < ∞`. ∎ (O vértice excluído é nulo e não interfere.)

**N4 — Suporte pleno (positividade da densidade)** `[DERIVED — elementar; OPEN no kernel]`.
*Hipótese:* `dμ_L = ρ d³p` com `ρ(p) = 1/p₀`, **contínua e estritamente positiva** na parametrização (ℝ³ para m>0; ℝ³∖{0} para m=0).
*Tese:* todo aberto relativo não-vazio da órbita tem `μ_L > 0`.
*Prova:* a parametrização é homeomorfismo órbita ↔ domínio; um aberto não-vazio `U` contém uma bola `B`; `μ_L(U) ≥ ∫_B ρ d³p > 0` porque `ρ > 0` contínua tem mínimo positivo em `B̄`. ∎ — *Esta é a hipótese que o contraexemplo de §2.2 viola.*

**N5 — Continuidade do multiplicador** `[DERIVED/KNOWN; OPEN no kernel]`.
*Tese:* `p ↦ M_a(p)` é contínua na órbita.
*Prova:* nas coordenadas da parametrização, `orbitPairing a p = a⁰·p₀(p) − (a¹p₁+a²p₂+a³p₃)`; `p₀ = √(m²+|p|²)` contínua (m>0); `p₀ = |p|` contínua em ℝ³∖{0} (m=0 — note-se: contínua mesmo no vértice, mas o vértice está fora da órbita de qualquer modo). `phase = exp(i·)` contínua; composição contínua. ∎ — *Não se pede diferenciabilidade; a não-suavidade de `|p|` no vértice é irrelevante.*

**N6 — Colagem a.e. → pontual** `[KNOWN — elementar; OPEN no kernel]`.
*Hipóteses:* `Y` topológico, `μ` Borel de **suporte pleno**, `F : Y → ℂ` **contínua**, `F = 1` μ-a.e.
*Tese:* `F ≡ 1`.
*Prova:* `{F ≠ 1}` é aberto (pré-imagem do aberto ℂ∖{1}) e μ-nulo; suporte pleno ⟹ é vazio. ∎

**N7 — Teorema-ponte (por caso)** `[DERIVED, condicional a N2–N6]`.
*Tese:* `U(a) = I` em `L²(H_m⁺, μ_L)` ⟹ `∀ p ∈ órbita: phase(orbitPairing a p) = 1`.
*Prova:* N3+N2 ⟹ `M_a = 1` a.e.; N5+N4+N6 ⟹ pontual em toda a órbita — **inclusive nos pontos de eixo**, que é onde L5/L6 avaliam. ∎

**N8 — Fecho** `[DERIVED, condicional]`:
- m>0: N7 + L6 ⟹ `a = 0`.
- m=0, helicidade 0: N7 + L5 ⟹ `a = 0`.
- m=0, helicidades +1⊕−1: o espaço é `L² ⊕ L²` e `U(a)` age **diagonalmente com o mesmo caráter escalar** (para translações não há fase de Wigner; os fatores de helicidade entram só nos boosts). `U(a) = I` no setor duplo ⟹ ação escalar `= I` em cada fator ⟹ N7 + L7 ⟹ `a = 0`. (O próprio L7 já registra que só descarrega a fidelidade pontual do caráter, **não** a representação de boost das helicidades — fora do escopo desta pergunta.)

**Tamanho da ponte:** 4 lemas novos de conteúdo (N2–N5), 1 colagem (N6), 1 composição (N7), 1 fecho (N8). Nenhum postula a fidelidade; nenhum deduz Lorentz, energia positiva ou KMS deste resultado.

---

### 4. Notas de formalização (sugestões **não verificadas**, para a sessão Codex)

- A afirmação "∫|g|² = 0 ⟹ g = 0 a.e." provavelmente via `MeasureTheory.lintegral_eq_zero_iff` (nome **não verificado**); σ-finitude via instâncias `MeasureTheory.SFinite`/`IsFiniteMeasureOnCompacts` (**não verificado**); suporte pleno possivelmente corresponde a `MeasureTheory.Measure.IsOpenPosMeasure` (**não verificado**); continuidade via `Continuous.comp` sobre `Complex.exp` e somas/produtos (**não verificado**).
- Recomendo enunciar N6 como lema geral independente (é reutilizável fora desta órbita) e N7 como o único ponto que menciona `U(a)`, `μ_L` e `phase∘orbitPairing` juntos — assim os três fechos (N8) ficam de uma linha sobre L5/L6/L7, **reaproveitando o arquivo anexado byte a byte**, sem edição.
- Controle negativo obrigatório (régua da casa): o contraexemplo de §2.2 deve ser formalizável como probe — uma hipótese `U(a) = I` sobre medida com buraco de suporte **não** deve habitar o tipo de N7; se habitar, a formalização está fail-open.

---

### 5. Estatutos e lacunas

- `[KNOWN]` a matemática de suporte (N2, N6 são exercícios clássicos de teoria da medida); `[DERIVED]` a instanciação à órbita (N3–N5, N7, N8); `[OPEN]` toda a formalização Lean — **nada compilado por mim**; as sete declarações permanecem `[REAL — evidência local declarada]`.
- **Escopo honesto:** provada a fidelidade das **translações** na órbita futura nos três setores. Seguem fora: representação de Lorentz (inclusive boosts de helicidade no setor ±1), energia positiva (já embutida na definição da órbita futura — não deduzida aqui), KMS, e qualquer elo com H2. A fidelidade de translação **não** implica fidelidade da representação de Poincaré — os boosts exigem ponte própria, não esta.
- **Lacuna que resta, nomeada:** a ponte está *projetada* e justificada elo a elo, mas o estatuto operacional é `OPEN — a compilar`; a sessão Codex deve tratá-la como dívida de kernel, não como teorema. O gate, como sempre, não se move por este documento.