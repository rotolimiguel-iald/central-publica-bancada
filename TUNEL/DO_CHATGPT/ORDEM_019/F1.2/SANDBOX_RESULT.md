# F1.2 — prova algébrica no sandbox

07/10/2026 · [REAL] `sandbox/MatrixInnerGauge.lean` foi compilado com o kernel **copiado** da bancada A1b. A reprodução medida está em `sandbox/COMPILE_RESULT.json`: rc=0, zero `sorry`/`admit`/`axiom` no fonte e, para os dois teoremas, apenas `propext`, `Classical.choice`, `Quot.sound` no `#print axioms`.

- `gauge_matrixRep_ungauge`: a representação matricial interna `π_σ(a)` vira multiplicação constante por `a` sob a conjugação pontual pelo mesmo `modPow ρ r` do kernel.
- `gauge_shift_ungauge`: a translação regular vira `modPow ρ t` multiplicado pela mesma translação.

O cálculo reaproveita `TGLExt.ModularFlow.modPow_add` e `modPow_mul_neg`. O tipo de teste é o núcleo **algébrico** de funções matriciais sobre ℝ. [OPEN] Ainda não há aqui espaço L² completado, fechamento de von Neumann, equivalência `M_n⋊_σℝ ≅ M_n⊗L(ℝ)`, traço normal semifinito transportado ou a instanciação exata do `RegularCoreTraceData`. Portanto F1.2 continua `EM_CURSO`; estes dois termos pagam somente a conjugação dos geradores e não deslocam o gate.
