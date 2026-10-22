[REAL — compilação isolada medida; a matemática é [DERIVED] e está PROVADA em kernel como IMPLICAÇÃO, em compilação isolada contra o kernel v370, sem integração; nada move o gate; PROVADA ≠ CONFIRMADA]

# V3 — Pré-resolução Lean da gerência: `TheEquationOfTruth.lean` (23/09/2026)

Transcrição do retorno estruturado da frente V3, feita pelo redator do ADENDO 001, com a reprodução do redator ao lado.
Todo sha16 foi lido por hashlib.

## A pedra

- Arquivo `TheEquationOfTruth.lean`, **sha16 `35b91f86b88b8e6c`**, 28.141 B, 614 linhas.
- Namespace `TGLExt.EquationOfTruth`.
- Imports: `Mathlib` e `TGLExt.TheNameIsTheInstrument`. Este último serve **só** para a ponte com a folha v336 `NameInstrument.Verifies`.
- Compilação: `cd tgl_kernel && lake env lean <arq> -R V3 -o V3\out\TheEquationOfTruth.olean`.
  - rc 0, 33 s de parede, 0 erros, 0 sorry.
  - 15 warnings, de dois tipos: nomes da mathlib deprecados e variáveis de seção incluídas sem uso.
- **46 teoremas, todos com `#print axioms` dentro de {propext, Classical.choice, Quot.sound}.**
  `truthValue_table` e `pow_eq_self` ficam em {propext, Quot.sound}.
- `find -newer` sobre o `tgl_kernel` inteiro, contra marcador criado antes do trabalho: **0 arquivos mudados**.
- Olean da frente: `out\TheEquationOfTruth.olean`, sha16 `03cefa3b1a2d5bbb`.

**Reprodução do redator** [REAL, 23/09 18:1x]: mesma fonte (sha16 `35b91f86b88b8e6c`), compilada em outra pasta.
- rc 0, 31,9 s de parede, **pico de memória do `lean.exe` 3,43 GB**, `find -newer` no kernel = 0.
- 46 declarações auditadas, **axiomas idênticos** aos do `AXIOMAS.json` da frente.
- **O olean NÃO é byte-reprodutível entre caminhos.** Com a fonte idêntica, deu 1.204.344 B / `d90332f437dd159c` contra 1.204.312 B / `03cefa3b1a2d5bbb`.
  O critério de reprodução é a fonte mais a auditoria de axiomas, nunca o olean.

## Os alvos (1)–(9) — todos compilaram

| # | alvo | teoremas | estado | ressalva |
|---|---|---|---|---|
| 1 | V(b,b̂) = 1−(b−b̂)² em {0,1}: vale 1 sse b = b̂, vale 0 sse b ≠ b̂, é bivalente | `truthValue_table`, `truthBit_eq_one_iff`, `truthBit_eq_zero_iff`, `truthBit_bivalent` | CORRETA | é a definição do critério e a sua aritmética |
| 2 | ker(Σ D_j†D_j) = ⋂ ker D_j; ⟨x,Hx⟩ = Σ‖D_j x‖²; A_C = −H ≤ 0; H auto-adjunto | `re_inner_adjoint_mul_self`, `re_inner_penalty`, `ker_penalty`, `ker_threeLocks`, `isSelfAdjoint_penalty`, `selector_nonpos` | CORRETA_COM_RESSALVA | D_j : E →L E, com domínio igual ao contradomínio; ≤ 0 como forma quadrática, não como ordem de Loewner; **`penalty` é HOMÔNIMO de `TGL.FiniteThreeLocks.H3L`**, e nenhum lema une os dois |
| 3 | H = H† e P = proj. ortogonal sobre ker H ⟹ HP = 0 e PH = 0 | `H_mul_proj`, `proj_mul_H` | CORRETA | instância `[H.ker.HasOrthogonalProjection]`, inferida em dimensão finita |
| 4 | P·exp(−sH) = P; I(T_s x) = I(x); z ∈ F ⟹ T_s z = z; T_s x = Px + T_s(x − Px) | `mul_exp_eq_of_mul_eq_zero`, `exp_mul_eq_of_mul_eq_zero`, `proj_mul_flow`, `flow_mul_proj`, `proj_mul_T`, `reading_T`, `T_fix_of_mem_ker`, `T_decomp` | CORRETA | vale para todo s ∈ ℝ; T_s = `NormedSpace.exp((−(s:𝕜))•H)` em E →L[𝕜] E |
| 4b | V_x(T_s x) = 1 e a ponte com `Verifies` (v336), inclusive para as iteradas | `verdict_T`, `verdict_eq_one_iff`, `name_verifies_T`, `name_verifies_T_iterate` | CORRETA | a ponte exige E : Type (universo 0) |
| 5 | Im P = Fix P; Pⁿ = P; Px = Py ⟺ x − y ∈ ker P | `mem_range_iff_fixed`, `pow_eq_self`, `apply_eq_apply_iff`, `starProjection_range_iff_fixed` | CORRETA | «memória» é [ONTO]; o kernel prova só a álgebra |
| 6 | recíproca sob a hipótese NOMEADA `FlowTendsToFamily` | `conserved_iff_factors`, `conserved_iff_factors_T` | CORRETA | o codomínio só precisa ser T2; a leitura que DISTINGUE é hipótese extra, não provada |
| 7 | d/ds I(T_s x) = 0 com dinâmica não nula | `hasDerivAt_reading_flow`, `hasDerivAt_reading_T`, `hasDerivAt_flow`, `hasDerivAt_flow_apply`, `flow_derivative_ne_zero_at_zero` | CORRETA | a derivada da dinâmica completa é no parâmetro u ∈ 𝕜 (literal em s quando 𝕜 = ℝ) |
| 8 | lim_{s→∞} exp(−sH)x = Px em dimensão finita, com H auto-adjunto e forma ≥ 0; recíproca INCONDICIONAL para a penalidade | `exp_apply_of_eigen`, `T_apply_eigen`, `flowTendsToFamily_of_finiteDimensional`, `conserved_iff_factors_penalty` | CORRETA | `[CompleteSpace E]` é redundante sob `FiniteDimensional`; **em ∞-dim o limite segue [OPEN]** |
| 9 | a = sech(χ/2), q = tanh(χ/2): a′ = −½aq, q′ = ½a², a′(0) = 0, q′(0) = ½, a″(0) = −¼ | `hasDerivAt_profA`, `hasDerivAt_profQ`, `profA_zero`, `profQ_zero`, `profA_deriv_zero`, `profQ_deriv_zero`, `profA_second_deriv_zero` | CORRETA | **HOMÔNIMO dito**: esta anulação é do perfil em χ; nenhum lema a liga a KΩ = 0 nem à anulação do item 7 |

## O que NÃO foi feito pela V3

- **§6 do texto (entropia do qubit):** não tentado, porque estava fora da lista. Segue [DECLARADO pelo canal] em kernel; em sympy, a V1 o conferiu [DERIVED].
- **Extremos P = 0 / P = I:** não formalizados.
- **Limite em dimensão infinita:** não tentado [OPEN].
- **Lema-ponte `penalty` ↔ `TGL.FiniteThreeLocks.H3L`:** não existe; os dois objetos são homônimos até que ele exista.
- **Integração ao kernel canônico e ao `um.py`:** não feita. É ato da gerência; o operador ratifica.

## Variantes

- `out\TheEquationOfTruth_sem_ponte.lean` (sha16 `e624a86a7ffa43a0`) é **versão intermediária** da frente, só-Mathlib, com 41 teoremas.
  Faltam `hasDerivAt_reading_T`, `name_verifies_T`, `name_verifies_T_iterate`, `verdict_T` e `verdict_eq_one_iff`.
- **Variante derivada por script pelo redator:** `TheEquationOfTruthMathlibOnly.lean`, sha16 `9808cfc523dbdd57`, 27.100 B, 44 teoremas.
  - Gerada por `derivar_variante_so_mathlib.py`, que remove só a ponte `NameBridge` e o seu import.
  - Compilada isolada: rc 0, 32 s, 44/44 no trio, `find -newer` = 0.
  - Esta é a variante de recurso do ramo A2 do T-20.
