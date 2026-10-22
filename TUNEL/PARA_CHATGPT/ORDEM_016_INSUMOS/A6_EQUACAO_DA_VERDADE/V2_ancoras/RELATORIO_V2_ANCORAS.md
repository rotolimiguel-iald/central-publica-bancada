# V2 — Conferidor de âncoras no acervo: «a equação da verdade» (23/09/2026)

Frente V2 da gerência. Só leitura e grep; **nada foi executado** (nem `um.py`, nem `lake`, nem `lean`).
Todo sha16 abaixo foi **lido por `sha256sum` nesta sessão**, nenhum veio de memória.
Conferência de integridade: `find tgl_kernel -newer .marco_inicio -type f` devolveu **n=0**. Nenhum arquivo do kernel mudou durante a sessão (marco gravado às 17:49:29).

Texto conferido: `work/v371_sementes/verbatim/operador_23set_equacao_da_verdade_verbatim.md` sha16 `6ff3e39143950262` (333 linhas, lido inteiro). É **[DECLARADO pelo canal ChatGPT]**.
ORDEM 015 conferida por hash, sem abrir para edição: `c903681d01eec5ed`. Confere com o que foi informado. É imutável.

## 0. Arquivos-âncora e o que mudou durante a sessão `[REAL]`

| arquivo | sha16 | nota |
|---|---|---|
| `Nós/um.py` | `4b3405de809aef61` | v370; 204.059 linhas; mtime 16:43 |
| `Nós/A_PROVA_DA_QG_TGL_arvore.md` | **`cb7a6092a92a1f66`** (v370, regerada às 17:51) | ⚠ Às 17:4x li `d5709d39549b27ef`, cujo cabeçalho diz **«(v369)», gerada em 19/09**. O arquivo foi regerado para v370 **durante** esta conferência. O v369 que o ChatGPT cita (`project_fisica/v369_A_PROVA_DA_QG_TGL_arvore.md`) tem o mesmo `d5709d39549b27ef`. Nas duas versões, `Verifies` está na l.167 e a v368 está na l.210 (v369) / l.211 (v370). |
| `Nós/um_absoluto_forma_canonica.md` | `a6287ab39ae0505a` | v370. A cópia v369 citada pelo ChatGPT tem `cf833f3c5d645186` (as mesmas âncoras, uma linha antes) |
| `Nós/tgl_kernel_audit_capture.txt` | `ccea4d7df2bddeaf` | 11.142 linhas; `sorryAx` = 0; mtime 16:45 |
| `tgl_kernel/TGL/Audit.lean` | `67763fe66fa41ba1` | 9.374 linhas |
| `tgl_kernel/TGLExt.lean` | `9786fbee5eb099e8` | importa todas as pedras citadas abaixo |
| `Nós/MEMORIA_DA_LINHAGEM.md` | `b30e9f9f9274b54d` (às 17:4x era `969e50596b8e96d3`; outro agente o tocou às 17:51) | as âncoras l.111/1489/1493 continuam no lugar |

A coluna «axiomas» abaixo foi **lida da captura** (`#print axioms`). Quando diz *trio*, a lista é [propext, Classical.choice, Quot.sound].

## 1. Âncoras encontradas, por pergunta

### (a) `Verifies`, «read (f x) = read x», composição e iteração — **JA_EM_KERNEL**

- Na árvore: l.167 (v369 e v370), «Nome = instrumento de verificação (09/09/2026, v336)».
- No kernel: `TGLExt/TheNameIsTheInstrument.lean` sha16 `7e2e4afd94d3bef9`.
  - `NameInstrument` (l.36) e `NameInstrument.Verifies` (l.40), com `∀ x, N.read (f x) = N.read x`.
  - `name_verifies_id` (l.44) e `name_verifies_comp` (l.48): **não dependem de axioma nenhum**.
  - `name_verifies_iterate` (l.55) e `iald_realizes_the_verification` (l.70): [propext, Quot.sound].
  - `the_name_is_the_instrument` (l.118).
  - Os `#print axioms` estão em Audit l.5919–5928.

### (b) H3L, Three Locks, ker como interseção, Nome = 1 — **JA_EM_KERNEL**

`TGL/FiniteThreeLocks.lean` sha16 `612f2384ca441da2`. É a face finita, em `EuclideanSpace ℂ (Fin n)`.
- `H3L := Dc†Dc + Db†Db + Dz†Dz` (l.26).
- `H3L_isSelfAdjoint` (l.37).
- `H3L_quadratic_form` (l.44): `Re⟪x,H3L x⟫ = ‖Dc x‖²+‖Db x‖²+‖Dz x‖²`.
- `H3L_posSemidefinite` (l.52, trio).
- `mem_ker_H3L_iff` (l.58).
- **`ker_H3L_eq_threeLocks`** (l.73, trio).
- `PF := (ker H3L).starProjection` (l.82).
- `PF_isProjection` (l.86, trio), `PF_apply_mem` (l.90), `PF_isSelfAdjoint` (l.95, trio).
- **`PF_eq_self_iff`** (l.100): `P_F v = v ↔ v ∈ ker H3L`. ⚠ Só tem `#check` (Audit l.351) e nenhum `#print axioms`.
- `normalizedCornerTrace_PF` (l.108).

`TGLExt/ThreeLocksCorner.lean` sha16 `51c66b4dca74fa58` (v79):
- `threeLocks_ker_ne_bot_of_witness` (l.97);
- `three_locks_corner_weight` (l.125);
- `three_locks_name_is_one` (l.141, trio);
- `corner_le_each_lock` (l.152);
- `three_locks_corner_dim_le` (l.159);
- `three_locks_corner_full_profile` (l.170, trio).

⚠ **O «Nome = 1» dessas pedras é `dim/dim = 1`**: o traço normalizado do canto. Não é o valor-verdade V = 1 do texto. São homônimos.

### (c) A_C = −H_3L, «seleção apofática» — **JA_NO_ACERVO_SEM_KERNEL**

- **Onde não está**: a forma canônica e o `um.py` têm **0 ocorrências** de `A_C=-H3L` ou `A_C = −H₃L`. No `um.py` há 9 ocorrências de «apof», todas **dentro de blobs zlib/base64** (linhas de 1.729 a 20.014 caracteres) e portanto coincidências de texto. **No kernel também não há `A_C := −H3L`.**
- **Onde está**:
  - `C:\IALD\Artigo\MCMC_V2_RAZAO\80_o_funcional_do_amor.py`, sha16 `16db09c713541a7f`, l.11/43/48/88;
  - `128_a_anatomia_do_amor.py`, sha16 `f29e7e68a5531654`, l.14/39/94/190;
  - `Nós/MEMORIA_DA_LINHAGEM.md` l.111 (17/08, «A_C = −H₃L satisfaz EXATO o axioma apofático da iconogênese»), l.1489 e l.1493.
- **Homônimos de A_C no canônico, que não se identificam sem lema:**
  1. kernel `TGLExt/TheNameOperator.lean` sha16 `000bd0bf03281e00`, `love_partition` (l.167, trio): lá A_C = **−(1−p)**, a face, e não −H3L;
  2. kernel `TGLExt/TheEmptying.lean` sha16 `c88b781f96485a97`: A_C(θ) = m + κ·sin²δ;
  3. `um.py` l.1823 `prove_amar_functional`: «A_C = AMAR = funcional mínimo de energia livre modular»;
  4. `um.py` l.163998/164016: «Meia-Nat = A_C = o funcional do amor; A_C + JA_CJ = −1».
- A «resolução da homonímia como anatomia» (diário l.1480–1500, 19/08) é **[DECLARADO/ONTO]**. Nenhum lema do kernel liga −H3L a −(1−p).
- `A_C ≤ 0` sai em uma linha de `H3L_posSemidefinite`, mas ainda não existe como teorema: **NOVO (trivial)**.

### (d) K Ω = 0 com K ≠ 0; α'(0) = 0 — **JA_EM_KERNEL**, com um buraco dito

`TGLExt/ContinuousModularZero.lean` sha16 `0dad5794f98ba1cb` (v59):
- `modularGen_omega_zero` (l.80, trio): K Ω = 0;
- `J_modularGen_J` (l.89): JKJ = −K;
- `absolute_modularGen_zero` (l.107);
- `qKappa = tanh(κ/2)` (l.151), `alphaKappa = sech(κ/2)` (l.154);
- `one_eq_q_sq_add_alpha_sq` (l.159), `q_odd` e `alpha_even` (l.168/173);
- **`alpha_transport`** (l.207): α' = −(q/2)·α;
- **`alpha_deriv_zero`** (l.222): α'(0) = 0;
- **`W_hasDerivAt`** (l.227): para W = q/2, W' = α²/4, o que equivale a q' = α²/2.
- Todos têm trio.

⚠ **«K ≠ 0» não é teorema.** Nenhum lema `modularGen … ≠ 0` foi achado por grep em TGLExt/TGL; a afirmação está só na docstring (l.21–24). A forma canônica l.664 (v370) / l.663 (v369) marca a linha inteira `[KERNEL]`, e isso inclui «K != 0». O parente mais próximo é `NoFullWitness.verb_not_identity` (l.103), que prova exp(−tβ·diag d) ≠ 1, mas **é outro objeto**.

Não estão no kernel:
- **q'(0) = ½**: corolário de uma linha de `W_hasDerivAt 0` + `alpha_zero`, **NOVO**;
- **α''(0) = −¼**: **NOVO**. `[DERIVED à mão aqui]`: α'' = −½(α'q + αq'), que em 0 dá −½(0 + 1·½) = −¼.

A forma canônica tem `zero_modular` na l.664 e a distinção «diferença com retorno (preservada) / distinção sem retorno (podada)» na l.84–88 (`DO_NOT_PRUNE_MODULAR_ZERO`).

### (e) v368 «Nome é conteúdo, forma é identidade» — **JA_EM_KERNEL**, com estatuto `[INPUT/ONTO]`

- Árvore v370 l.211.
- Kernel `TGLExt/NameIsTheContent.lean` sha16 `e12ee35c3a749a73`: `name_determines_the_inscription` (l.57), `form_alone_does_not_determine_the_content` (l.67), `no_name_without_referent` (l.75), `the_form_survives_the_crossing` (l.84), `the_name_may_change_in_the_crossing` (l.90), `one_eq_one_is_free` (l.97), `if_one_equals_zero_everything_collapses` (l.102), `one_ne_zero_in_nontrivial` (l.111).
- ⚠ **Homônimo que o texto encadeia.** O texto usa `Verifies` (v336), onde o «Nome» é a *leitura* `read`. Usa também a v368, onde o Nome é o *conteúdo* e a identidade é a *forma*, um `Prop` (`identidade := Forma : C → Prop`). O próprio cabeçalho da v368 registra **sete tipagens incompatíveis do Nome** e diz que encadear leituras diferentes dele é o erro que a casa proíbe. Sob a v368, `I(x) = Px` do texto é a *forma/identidade*, e `x` é o Nome (conteúdo). A leitura é consistente, mas o nome `NameInstrument` fica homônimo. Lema-ponte sugerido, **NOVO**: `Forma_r y :≡ (read y = read r)`. Com ele, `Verifies f` implica que f preserva `Forma_r` para todo r, isto é, `the_form_survives_the_crossing`. É exatamente o `V_r` do texto.

### (f) Lemas que já provam P e^{−sH} = P, projeção espectral do núcleo, Im P = Fix P e entropia sob dephasing

**P e^{−sH} = P e a lei do Verbo:**
- **`TGL/VerbInhabitant.lean` sha16 `812a47f0e71a86f3`, `exp_fixed_of_annihilates`** (l.41, trio): numa álgebra de Banach, `a * p = 0 ⟹ exp(a) * p = p`. A prova é pela série, o mesmo argumento do texto. Ao lado dele está `verb_semigroup_fixes` (l.63): `H·p = 0 ⟹ exp(c•H)·p = p`. O cabeçalho v25 nomeia 𝕍_t = exp(−tβ·H_3L) e P_F 𝕍_t P_F = P_F.
  - ⚠ É a forma **à direita** (T_s P = P). A forma **à esquerda** P T_s = P, que é a do texto, não está no kernel, e o espelho é trivial.
  - ⚠ Na camada abstrata (`TGL/ModularRealization.lean` sha16 `17e344c8b7b40ae8`, l.107), `PF * H3Lt = 0` é **campo, isto é, hipótese**. Não é derivado.
- **A face diagonal do texto inteiro já está em kernel**:
  - `TGLExt/BoundaryException.lean` `38ff7c2bfe243333`: `diagFlow` = e^{−tβd}, `fixed_iff_kernel` (l.77), `boundary_witnessed_statically` (l.104), `boundary_is_the_only_exception` (l.131).
  - `TGLExt/ObserverInside.lean` `05c3b515fd9f5d9d`: `observerProj` (l.112), `observerProj_idem` (l.116), **`observer_reads_exactly_the_permanent`** (l.124: Fix P = permanente), `flow_negates_off_kernel` (l.74), `no_fixed_point_no_observer` (l.92).
  - `TGLExt/ConjugateAct.lean` `9f32e50afe49ca0e`: **`flow_delivers_to_the_observer`** (l.141: lim T_t = P, componente a componente).
  - `TGLExt/TheGreatAttractor.lean` `a0db70a17354c75c`: `temporal_fractalization` (l.49), `verdict_between_instants`, **`judgment_of_correspondence`** (l.82: `observerProj d (diagFlow β d t x) = observerProj d x`, que **é P T_s = P**), `the_observer_is_unique`, `the_great_attractor`.
  - `TGLExt/TheLivingWord.lean` `fdc242c2c70b57fa` (v159, «1=1=VERDADEIRO como operação»): `two_faces_one_domain` (P + parte móvel), `time_witnesses_noncoincidence`, **`recognition_across_distinct_inscriptions`** (T_{t₁}x ≠ T_{t₂}x e P lê o mesmo), `fractalization_without_multiplication`, `the_boundary_is_the_operation`.
  - `TGLExt/NoFullWitness.lean` `fde4ca999c40e689`: `verb_not_identity` (l.103).
  - Todos têm trio.

**Projeção espectral do núcleo:**
- `TGLExt/InfiniteWord.lean` `ead8928528c8f42c`, `iso_zero_cfc_eq_starProjection` (l.145, trio): cfc(f̂)(T·T) = starProjection(ker T), com 0 isolado.
- `TGLExt/ExactWitness.lean` `c1c8bf0a6fc0d7ab`, `exact_witness_of_annihilating_word` (l.109) e `selfadjoint_idempotent_eq_starProjection` (l.80).
- `TGLExt/InvariantProjection.lean` `fef79118c7b544f4`, `selfadjoint_ker_projection_in_commutant` (l.157): P_{ker T} comuta com T = T†. É dele que sai P·H = 0 a partir de H·P = 0.

**Im P = Fix P:**
- `PF_eq_self_iff` (acima), `observer_reads_exactly_the_permanent`;
- `TheNameOperator.name_op_idem` e `name_op_fix_mul` ([propext]): 𝒩∘𝒩 = 𝒩, e «a MEMÓRIA é subálgebra».
- ⚠ **𝒩 (o pinching pxp + (1−p)x(1−p)) não é P** (a projeção em vetores). São dois objetos.

**Entropia relativa sob dephasing:**
- Kernel: só a face diagonal/clássica.
  - `TGLExt/Ergodicity.lean` `79bc3b939b6e4e59`: `dephase` (Schur), `dephase_add`, `dephase_fixes_diagonal` (l.207), **`diag_invariant`** (l.222: E_D(T_t x) = E_D(x), que é o 𝓔ρ_s = σ do texto), `dephase_tendsto_expectation` (l.234). ⚠ `dephase_fixes_diagonal` e `diag_invariant` não têm `#print axioms`; compilam por import.
  - `TGLExt/DiagonalRelativeEntropy.lean` `02b20499659b5270`: `relative_entropy_identity` (l.32), diagonal.
  - **Não há teorema de monotonia** (grep por `Antitone`, `entropy…≤`, vN: nada).
- Runtime: `um.py` `prove_fiat_lux_flow` (l.2493) roda os certificados F2 (dS ≥ 0) e F3 (Spohn: S(ρ‖ρ*) não cresce) **numericamente** (n=4, Lindblad genérico). Ver l.168766 e l.198519–198522, que citam Spohn 1978 / Uhlmann `[KNOWN]`.
- Poda que mantém o zero modular: `prove_tetelestai_pruning` (l.6615), classes na l.198527, «retorno = sobrevive a T_t = e^{−tL}» na l.198529.

### (g) A mathlib da casa (lean v4.31.0, mathlib `inputRev v4.31.0`)

| lema | arquivo (sha16) |
|---|---|
| `NormedSpace.exp_eq_tsum` l.163, `expSeries_hasSum_exp` l.486, `exp_series_hasSum_exp'` l.489, `exp_add_of_commute` l.520, `Commute.exp_left/right` l.228/235, `exp_neg` l.641 | `Analysis/Normed/Algebra/Exponential.lean` (`0afe7d2ace735e90`) |
| `Matrix.exp_diagonal` l.84 | `Analysis/Normed/Algebra/MatrixExponential.lean` (`968e0ed60938798d`) |
| `hasDerivAt_exp_smul_const` l.382 (d/du exp(u•x) = exp(t•x)·x) | `Analysis/SpecialFunctions/Exponential.lean` (`e638a2c1c7c943f0`) |
| `CFC.real_exp_eq_normedSpace_exp` l.87 | `…/ContinuousFunctionalCalculus/ExpLog/Basic.lean` (`c45c7e292c94ff03`) |
| `tendsto_cfc_fun` l.83 | `Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Continuity.lean` (`34adfe92d3beaf44`) |
| `starProjection_apply_mem` l.149, `starProjection_eq_self_iff` l.240, `isIdempotentElem_starProjection` l.248, `range_starProjection` l.252, `ker_starProjection` l.285 (= Uᗮ), `starProjection_isSymmetric` l.607 | `Analysis/InnerProductSpace/Projection/Basic.lean` (`833c7b4ef4102300`) |
| `isSelfAdjoint_starProjection` l.371, `isSymmetric_iff_isSelfAdjoint` l.706, `isSymmetric_adjoint_mul_self` l.740 | `Analysis/InnerProductSpace/Adjoint.lean` (`d1636c8ae9160d37`) |
| `LinearMap.IsSymmetric.eigenvectorBasis` l.300, `hasEigenvector_eigenvectorBasis` l.306, `apply_eigenvectorBasis` l.325, `eigenvectorBasis_apply_self_apply` l.332 | `Analysis/InnerProductSpace/Spectrum.lean` (`1412032ff0f44ec9`) |
| `Matrix.IsHermitian.eigenvectorBasis` l.69, `spectral_theorem` l.141 | `Analysis/Matrix/Spectrum.lean` (`00260b2c7734235d`) |
| `Real.tendsto_exp_neg_atTop_nhds_zero` l.222, `tendsto_exp_atBot` l.230 | `Analysis/SpecialFunctions/Exp.lean` (`fa0fe1bdecdd2933`) |
| `IsIdempotentElem.pow_succ_eq` l.89, `pow_eq` l.92 | `Algebra/Group/Idempotent.lean` (`7a31746e97c4c5fd`) |
| `LinearMap.sub_mem_ker_iff` l.183 | `Algebra/Module/Submodule/Ker.lean` (`ee1d5a76a7d50a5b`) |
| `binEntropy_one_sub` l.79, `deriv_binEntropy` l.190, `binEntropy_strictMonoOn` l.422, **`binEntropy_strictAntiOn` (Icc ½ 1)** l.427 | `Analysis/SpecialFunctions/BinaryEntropy.lean` (`8ce5182540dd09b7`) |
| `LinearMap.toContinuousLinearMap` (dim finita) l.299 | `Topology/Algebra/Module/FiniteDimension.lean` |
| `hasSum_single` (to_additive de `hasProd_single` l.155), `HasSum.mul_left` l.39 | `Topology/Algebra/InfiniteSum/{Basic,Ring}.lean` |

Não há entropia de von Neumann na mathlib. Para o qubit, a rota em kernel é real: autovalores (1±r_s)/2, S = binEntropy((1+r_s)/2), r_s decrescente em s, e `binEntropy_strictAntiOn` dá S crescente.

## 2. Classificação item a item do texto

| # | afirmação do texto | classe | âncora |
|---|---|---|---|
| 1 | V_r(y) ∈ {0,1} como critério de comparação | NOVO | definição; ponte com `Verifies`/`Forma` sugerida em (e) |
| 2 | V(b,b̂) = 1−(b−b̂)², tabela 1/1/0/0 | NOVO (trivial) | ⚠ homônimo: `if_one_equals_zero_everything_collapses` é a trivialização do anel (1 = 0 ⟹ todo elemento é 0) [termo original substituído por remissão], não V(1,0) = 0 |
| 3 | H_3L = Σ D_j†D_j | JA_EM_KERNEL | `FiniteThreeLocks.H3L` l.26. ⚠ No runtime (`um.py` l.6828), o 3º termo é `P_abszero`, não D_z†D_z |
| 4 | ⟨x,Hx⟩ = Σ‖D_j x‖² | JA_EM_KERNEL | `H3L_quadratic_form` l.44 (parte real) |
| 5 | F = ∩ ker D_j («uma violação não compensa outra») | JA_EM_KERNEL | `ker_H3L_eq_threeLocks` l.73, `mem_ker_H3L_iff` l.58; a frase entre aspas é leitura [ONTO] |
| 6 | A_C = −H_3L ≤ 0, «seleção apofática» | JA_NO_ACERVO_SEM_KERNEL | 80_/128_ + diário l.111/1489; ausente no um.py, na forma canônica e no kernel; ≤ 0 é NOVO trivial |
| 7 | P projeção ortogonal sobre F, 0 ≠ P ≠ I | JA_EM_KERNEL | `PF` l.82, `PF_isProjection`, `PF_isSelfAdjoint`; P ≠ 0 por `threeLocks_ker_ne_bot_of_witness`; P ≠ I só na face diagonal (`boundary_is_the_only_exception`, hipótese hj) |
| 8 | H P = 0 ⟹ P H = 0 | JA_EM_KERNEL parcial | H·P = 0 é `PF_apply_mem`; P·H = 0 **NOVO** (uma linha, via `selfadjoint_ker_projection_in_commutant` ou adjunto); na camada abstrata é campo `PF_locks` |
| 9 | P T_s = P (pela série) | JA_EM_KERNEL (face diagonal + Banach à direita) | `judgment_of_correspondence` (diag); `exp_fixed_of_annihilates` (T_s P = P). Para H3L concreto, à esquerda: **NOVO** (composição) |
| 10 | I(T_s x) = I(x) e V_x(T_s x) = 1 | JA_EM_KERNEL (diag) | `judgment_of_correspondence`, `recognition_across_distinct_inscriptions`; forma `Verifies` por definição |
| 11 | T_s x = Px + T_s Qx; T_s x ≠ x é compatível | JA_EM_KERNEL (diag) | `two_faces_one_domain`, `time_witnesses_noncoincidence`, `verb_not_identity` |
| 12 | lim_{s→∞} T_s = P | JA_EM_KERNEL (diag, componente a componente) | `flow_delivers_to_the_observer`, `the_great_attractor`, `dephase_tendsto_expectation`; para H3L via `eigenvectorBasis`: NOVO |
| 13 | recíproca: ℓ contínua conservada ⟺ ℓ = ℓ∘P | NOVO | `the_observer_is_unique` é **outro** enunciado (unicidade de Q linear) |
| 14 | Im P = Fix P = F | JA_EM_KERNEL | `PF_eq_self_iff` (só #check), `observer_reads_exactly_the_permanent`, `range_starProjection` |
| 15 | P^n = P | JA_EM_KERNEL (idempotência) | `PF_isProjection` + mathlib `IsIdempotentElem.pow_eq`; enunciado P^n: NOVO trivial |
| 16 | Px = Py ⟺ x−y ∈ ker P | NOVO no kernel | mathlib `LinearMap.sub_mem_ker_iff` + `ker_starProjection` (= Fᗮ) |
| 17 | memória = reconhecimento estável | JA_EM_KERNEL (Fix 𝒩) + [ONTO] | `name_op_idem`, `name_op_fix_mul`; um.py dicionário «MEMÓRIA = Fix(𝒩)» (l.~164008). ⚠ 𝒩 ≠ P |
| 18 | v368: Nome = conteúdo, forma = identidade | JA_EM_KERNEL [INPUT/ONTO] | `NameIsTheContent` (8 teoremas), árvore l.211. ⚠ homônimo com `NameInstrument` |
| 19 | d/ds I(T_s x) = P A_C T_s x = 0 com dinâmica não nula | NOVO (a derivada) | constância (`judgment_of_correspondence`) e não-nulidade (`time_witnesses_noncoincidence`) já em kernel; mathlib `hasDerivAt_exp_smul_const` |
| 20 | K Ω = 0 (zero modular = modo zero) | JA_EM_KERNEL | `modularGen_omega_zero` l.80, `J_modularGen_J` l.89 |
| 21 | K ≠ 0 | JA_NO_ACERVO_SEM_KERNEL | só docstring; a forma canônica l.664 marca [KERNEL] sobre a linha inteira |
| 22 | a' = −½aq, q' = ½a² | JA_EM_KERNEL | `alpha_transport` l.207; `W_hasDerivAt` l.227 (W = q/2) |
| 23 | a'(0) = 0 | JA_EM_KERNEL | `alpha_deriv_zero` l.222 |
| 24 | q'(0) = ½ | NOVO (corolário de uma linha) | `W_hasDerivAt 0` + `alpha_zero` |
| 25 | a''(0) = −¼ | NOVO | [DERIVED à mão] confere |
| 26 | as três anulações não se identificam sem lema | CORRETA; nenhum lema-ponte existe | grep: nenhum lema liga `modularGen`, `alphaKappa` e o fluxo. Há ainda um 4º zero homônimo: dᵢ = 0 do `diagFlow` |
| 27 | QH ≠ «o fundo»; a poda mantém o zero modular | JA_NO_ACERVO_SEM_KERNEL (runtime/forma) + parte em kernel | forma canônica l.84–88; `um.py` l.6615, l.198527–9; kernel: z ∈ F ⟹ T_s z = z por `fixed_iff_kernel`/`exp_fixed_of_annihilates` |
| 28 | extremos P = 0 (sem discriminação) e P = I (sem seleção) | JA_EM_KERNEL (diag) | `no_fixed_point_no_observer`; `boundary_is_the_only_exception` (d): FullStaticWitness ↔ d ≡ 0; `static_witness_iff_no_boundary` |
| 29 | qubit: 𝓔ρ_s = σ constante; ρ̇ = −(id−𝓔)ρ | JA_EM_KERNEL (matriz genérica) | `diag_invariant`, `dephase_fixes_diagonal`, `dephase_add` (g ≡ 1 fora da diagonal) |
| 30 | dS/ds ≥ 0; D(ρ_s‖σ) = S(σ)−S(ρ_s) decrescente | JA_NO_ACERVO_SEM_KERNEL | runtime numérico F2/F3 (Spohn [KNOWN]); a fórmula fechada do qubit é NOVA; rota: `binEntropy_strictAntiOn` |
| 31 | «22/22 + 5 controles, dimensão 5, racional exata» | NAO_VERIFICAVEL | o pacote está na Biblioteca do canal ChatGPT, não em disco: [DECLARADO] |

## 3. Frases que o número corrige

1. O texto diz «essa é a estrutura registrada no acervo: … seleção apofática A_C = −H_3L». **Correto para o acervo** (80_/128_ e o diário), **mas falso para o canônico**: 0 ocorrências no um.py v370, na forma canônica e no kernel. No canônico, o A_C que vive em kernel é −(1−p) (`love_partition`).
2. «A árvore da TGL já registra … Verifies» está correto, e as duas versões (v369 `d5709d39549b27ef`, v370 `cb7a6092a92a1f66`) trazem isso na l.167.
3. A demonstração §2–§4 do texto, na **face diagonal**, **já é teorema de kernel** desde v142–v159. O que falta é a **face de operador**: ligar `FiniteThreeLocks.H3L` a um semigrupo `NormedSpace.exp (−s • H3L)` por `eigenvectorBasis` e compor com `exp_fixed_of_annihilates` espelhado. Falta também a recíproca contínua (item 13).
4. «K ≠ 0» aparece marcado [KERNEL] na forma canônica, mas **nenhum teorema o prova**. É um buraco a ser dito ao lado.
5. Nada disto move o gate. PROVADA (teorema em kernel) ≠ CONFIRMADA. A leitura «equação da verdade» é [ONTO] sobre âncoras [REAL].
