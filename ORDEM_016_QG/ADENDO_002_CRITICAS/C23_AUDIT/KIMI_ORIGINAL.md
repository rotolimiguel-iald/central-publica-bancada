# C2.3 — Auditoria cética: onde a cadeia do cociclo físico para

**Estatuto desta resposta: [DECLARADO]** até confronto da bancada. Nada aqui foi compilado por mim; tudo o que afirmo sobre os artefatos é leitura das **projeções parciais** fornecidas nesta chamada (linhas omitidas não examinadas — lacuna declarada no §8). Não respondi ao pedido1265dfaf (não tenho a fonte; instrução respeitada). Não construí Fock, não escolhi partição física, não executei a §3 Parte C, nenhum nome reservado criado, nenhum gate se move.

---

## 1. Resposta direta à pergunta

**A cadeia para por falta de dado de representação — não por incompatibilidade de tipo.** Nos trechos fornecidos, os lemas pagos já são enunciados sobre uma fibra vetorial **genérica** (`{E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]` em `IsometricCocycleSpectrum_v2.lean:8`; `[InnerProductSpace ℂ E]` em `OrbitalBoostUnitary_v2.lean:10`), e o negativo já toma o cociclo como **parâmetro** (`C : ℝ → MomentumCoordinates → (E →ₗᵢ[ℂ] E)`, linha 14). A fibra de helicidade ℂ (ou ℂ² para o par ±1) instancia esses tipos sem retrabalho. A evidência textual decisiva está no próprio docstring (sha256 `a08ec8db…`, linhas 10–12):

> *"Norm preservation suffices; no trivialization of a helicity cocycle is assumed. (…) It does not construct the physical helicity representation or its measurability."*

Ou seja, o próprio artefato declara: o que falta é (i) **a trivialização** (o dado) e (ii) **a mensurabilidade do cociclo físico** (a prova sobre o dado) — não um reparo de tipo. Se existisse incompatibilidade de tipo na ligação (e.g., algum lema da cadeia com `E = ℂ` ou `C ≡ id` fixado), ela estaria visível nas assinaturas exibidas; as exibidas mostram o contrário. **Ressalva de escopo:** só vi projeções; linhas omitidas poderiam conter um uso restrito que eu não vi. Com esse escopo, o veredito é: **falta dado**.

---

## 2. O que está efetivamente pago (inventário lido dos trechos)

| Artefato (sha256 abreviado) | Conteúdo lido | Papel |
|---|---|---|
| `OrbitalBoostCovariance_v2.lean` (`f2dca0a1…`) | `shellMomentum_chart`, `shellMomentum_chart_shift` (shift de rapidez = `wedgeBoostMap`), `orbitPairing_boost_inverse` | a carta e a covariância do boost, pagas |
| `OrbitalBoostUnitary_v2.lean` (`a50c60d0…`) | `orbitalBoostUnitary : Lp E 2 (orbitalMeasure m) ≃ₗᵢ[ℂ] …`, leis `zero/add/symm` | o boost orbital escalar como **unitário**, no tipo do contrato |
| `OrbitalL2Equivalence_v2.lean` (`b6f3c364…`) | `rapidityChart_measurePreserving`, `inverseRapidityChart_measurePreserving`, equivalência isométrica dos dois L² | as medidas ligadas, pagas |
| `ProductOrbitalSpectrum_v3.lean` (`186e2cf9…`) | `integer_periodic_lintegral_zero`, `product_norm_periodic_zero`, `productRapidityShift_no_eigen` | o motor de ladrilhamento ℤ: norma periódica em rapidez ⟹ f = 0 |
| `IsometricCocycleSpectrum_v2.lean` (`a08ec8db…`) | `isometric_fiber_shift_no_eigen` (ℝ e ℤ) | o negativo **fibrado**: shift + cociclo isométrico qualquer não tem autofunção |
| `ENTREGA_016_A3_energia_covariancia_e_vacuo.md` (`3520f8a1…`) | A3.2 (F(z) holomorfa ao semiplano, contínua à borda, F(t)=⟨ψ,U(ta)ψ⟩), A3.3 (grupo fortemente contínuo; no raio nulo `B_s U(r n) B_(-s) = U(r exp(s) n)`) | energia positiva e o grupo de boosts, pagos no orbital |
| `ENTREGA_016_A3_H2_par_fisico.md` (`f953b5fb…`) | aceitação A3.b; **"duas cópias escalares NÃO identificam helicidades físicas ±1 (…) NÃO PAGA"**; A3.5: nenhum vetor fixo pelos boosts no setor de uma partícula | a dívida nomeada pela própria bancada |
| `a3_consolidated_manifest.json` (`44343623…`) | status `REAL_SCALAR_ACCEPTANCE_WITH_PHOTON_MEASURE` | escalar aceito **com** medida do fóton; helicidade fora |

---

## 3. A distância auditada, item a item

| aspecto | `isometric_fiber_shift_no_eigen` (pago) | representação real de helicidade ±1 (alvo) |
|---|---|---|
| fibra | `E` genérico | ℂ por helicidade (ℂ² o par) |
| ação | `C(s,y)` isometria **arbitrária** ∘ shift de rapidez | fase de Wigner `e^{iλ θ(Λ,p)}` ∘ pull-back |
| lei de cociclo | **não exigida** (o negativo é mais forte) | **exigida** (é o que faz grupo) |
| grupo coberto | o shift de rapidez (a direção do boost da cunha) | Lorentz/Poincaré inteiro |
| fase na direção do boost | arbitrária na hipótese | **trivial** (ver §4) |
| o que entrega | sem autofunção (espectro contínuo) | o mesmo negativo — **já coberto** |
| o que falta | — | o dado θ, a lei, a mensurabilidade, a não-trivialidade, o grupo inteiro |

Duas observações de robustez, lidas da prova exibida (linhas 18–26): (a) a prova **só usa a norma** (`LinearIsometry.norm_map`, `norm_smul`, `hc`) — o escalar `c(s)` global morre na norma; logo o teorema valeria igual com fase `c(s,y)` dependente de ponto. O negativo é **mais geral que o necessário**; nada a destravar aí. (b) A hipótese `∀ s, ∃ c, ‖c‖=1 ∧ …` coincide, no caso real, com a forma exata — porque na direção do boost da cunha a fase real é trivial (§4).

---

## 4. O diagnóstico estrutural (proposta, a conferir pela bancada)

**[DERIVED — argumento desta resposta; KNOWN — estrutura de grupos de Lie, literatura de Wigner/Mackey; NÃO compilado nas fontes.]**

Seja o momento nulo de referência da reta da cunha, k̄ = (1,1,0,0). O grupo pequeno de k̄ é ISO(2) = SO(2) ⋉ ℝ², com o SO(2) gerado por J₁ (rotação no plano transverso x₂x₃) e o ℝ² pelas translações nulas. A fase de helicidade é lida pela parte SO(2) do cociclo de Wigner W(Λ,p) = B(Λp)⁻¹ΛB(p). Três fatos algébricos:

1. **[K₁, J₁] = 0** — o boost da cunha (direção x₁) comuta com a rotação transversa (planos disjuntos).
2. A conjugação por `e^{sK₁}` **normaliza** o grupo pequeno: fixa J₁ e apenas **escala** as translações nulas — não gera componente SO(2).
3. A parte SO(2) do cociclo é **gauge-invariante** (SO(2) é o quociente abeliano de ISO(2) pelo ℝ² normal; conjugação interna não a altera).

Logo a parte SO(2) de W(e^{sK₁}, p) é nula: **a fase de helicidade sob o boost da cunha é 1, em qualquer trivialização.** Nas coordenadas das fontes isto é visível diretamente: `coordinateShift s` move **só** `y.2` e deixa a coordenada transversa `y.1` **fixa** (`shellMomentum_chart_shift`, `f2dca0a1…:24–32`) — nenhuma rotação transversa é induzida, nenhuma fase nasce.

**Consequência cética (o núcleo desta auditoria):** restritas ao subgrupo do boost da cunha, a representação de helicidade ±1 e a representação escalar (ou a dupla-escalar, para o par) são **unitariamente equivalentes** — ambas são o shift de rapidez puro. Portanto:

- **(i)** Para a ponte modular (BW: Δ^{it} = boost; energia positiva; sem autovetor fora de ℂΩ no contrato v3.1), a fibra de helicidade é **invisível e desnecessária**: os lemas pagos já são a ação correta ali (módulo instanciar `E := ℂ` e a medida do cone, que o manifesto declara aceita: `PHOTON_MEASURE`).
- **(ii)** A diferença entre ±1 e duas cópias escalares vive **fora do eixo do boost** — nas rotações transversas (ação: fase constante `e^{±iφ}` composta com giro de `y.1`) e em Lorentz geral. Nenhum teste na direção modular pode separá-las. Isto **não substitui** ±1 por duas cópias — explica *por que* duas cópias não bastam e *onde* isso é demonstrável.
- **(iii)** Coerente com o selo da casa (`TGL_LIGHT_RAY_BORCHERS_V371 … NO_EIGENVECTOR__MODULAR_IDENTIFICATION_OPEN__FLAT_ONLY`) e com a entrega A3 ("identificação NÃO PAGA"): a ponte modular fecha sem helicidade; a identificação física "isto é o fóton" é um **dado novo com prova nova**, e não um reparo nos lemas existentes.

---

## 5. Inventário pedido: objetos / domínios / medidas / cociclo

**Objetos — pagos:** `MomentumCoordinates` ((transverso `Fin 2 → ℝ`) × rapidez); `shellMomentum`, `rapidityChart`/`inverseRapidityChart`; `orbitalScalarBoost`/`orbitalBoostUnitary` (unitário, fortemente contínuo, covariante); `wedgeBoostMap`/`boostMat`; translações `U(a)` com energia positiva (A3.2); o negativo fibrado. **Não pagos:** a fibra de helicidade concreta; a seção/trivialização do fibrado transverso; o dado θ; a ação do grupo além do boost da cunha; a lei de cociclo; a não-trivialidade.

**Domínios:** `Lp E 2 momentumMeasure` ≅ `Lp E 2 (orbitalMeasure m)` (pago). O cone m = 0 com a medida do fóton: declarado aceito no manifesto; **não conferi** nos trechos a prova de `rapidityChart_measurePreserving` em m = 0, a definição de `transverseMass`, nem o tratamento do vértice/raio `y.1 = 0` (singularidade presumivelmente de medida nula — lacuna de leitura, não defeito afirmado).

**Medidas:** `momentumMeasure`, `orbitalMeasure m`; a medida espectral `dμψ = ‖ψ‖² dμ` (A3.2, finitude provada de ψ ∈ L²). Preservação pelas cartas: provada nos trechos (m geral).

**Cociclo:** pago **somente** como hipótese genérica (isometria de fibra arbitrária, sem lei de cociclo, sem instância concreta) no teorema negativo. O cociclo de Wigner real — fase, lei, mensurabilidade — **não existe** nas fontes.

---

## 6. O primeiro enunciado que não segue das fontes

Na ordem lógica da construção, o primeiro elo ausente é a **seção** (de onde a fase se lê). Em forma mínima (nomes ilustrativos locais, **não** reservados):

```lean
-- (E0) a trivialização mensurável do fibrado transverso sobre o cone — o dado-base. AUSENTE.
-- (E1) o dado da fase e sua lei — AUSENTE:
def wignerPhase (Λ : Lorentz) (y : MomentumCoordinates) : ℝ := sorry  -- não construído
theorem cocycle_law (Λ Λ' y) :
  wignerPhase (Λ*Λ') y = wignerPhase Λ (act Λ' y) + wignerPhase Λ' y := sorry  -- não provado
theorem phase_measurable : Measurable (uncurry wignerPhase) := sorry           -- não provado
-- (E2) a não-trivialidade — o que separa ±1 de duas cópias escalares — AUSENTE:
theorem phase_transverse_rotation (φ y) : wignerPhase (transverseRot φ) y = φ := sorry
-- (E3) o elo de ligação com os lemas pagos — demonstrável, AUSENTE das fontes:
theorem phase_wedgeBoost (s y) : wignerPhase (wedgeBoostMap s) y = 0 := sorry
```

Nota de precisão: o enunciado "existe cociclo" já segue das fontes (θ ≡ 1 está pago). O que **não** segue é a existência do cociclo **não co-trivial específico de Wigner** — i.e., E1 + E2. E3 é o teorema de estrutura do §4 (parte SO(2) nula na direção da cunha): é ele quem diz que a ligação dos lemas pagos ao alvo é **definicional na trivialização natural**, e é o menor lema de ligação faltante.

---

## 7. O menor lema/artefato faltante (nomeado)

Em ordem de destrave, sem Fock e sem partição física:

1. **L-rotação-transversa (infraestrutura):** ação de `transverseRot φ` sobre `MomentumCoordinates` (giro em `y.1`, rapidez fixa) com preservação de `momentumMeasure` — análoga aos lemas `orbitalBoost*` já pagos; provável rotina.
2. **E3 (menor lema de ligação):** `phase_wedgeBoost ≡ 0` pela estrutura do grupo pequeno ([K₁,J₁]=0 + quociente SO(2) gauge-invariante). Liga os pagos ao alvo; **não** está nas fontes.
3. **E1 (menor dado):** a fase concreta com lei de cociclo e mensurabilidade, mais a continuidade forte da ação estendida (análoga a A3.3: exige θ(s,·) → 0 em medida quando s → 0 — hipótese sobre o dado, a provar junto).
4. **E2 (o artefato que decide a identificação):** `phase_transverse_rotation φ = φ` — a prova de que a fase é a de Wigner e não a trivial. Sem E2, "helicidade ±1" segue sendo duas cópias escalares disfarçadas — exatamente a honestidade que a entrega A3 registra.

Nenhum destes é exigido pela ponte modular H2; todos são exigidos pela identificação física. O caminho crítico da casa não muda por esta resposta.

---

## 8. Lacunas declaradas desta resposta

(i) Li **projeções parciais** dos arquivos (linhas omitidas não examinadas); não verifiquei `transverseMass`, a prova da medida do fóton em m = 0, nem o vértice da carta. (ii) O passo "fase trivial na direção da cunha" é **argumento de estrutura de grupo** (álgebra de Lorentz; KNOWN da literatura de Wigner/Mackey), **não** teorema lido das fontes — proposto para conferência da bancada por compilação isolada (rc 0, axiomas ⊆ {propext, Classical.choice, Quot.sound}, zero sorry). (iii) Não respondi ao pedido1265dfaf (sem fonte; instrução explícita). (iv) §3 Parte C não executada (condicionada a A8). (v) Nenhuma execução, compilação ou inspeção além dos trechos é alegada. (vi) O gate não se move; nenhum nome reservado foi criado; PROVADA ≠ CONFIRMADA; NOT_FALSIFIED ≠ CONFIRMED.