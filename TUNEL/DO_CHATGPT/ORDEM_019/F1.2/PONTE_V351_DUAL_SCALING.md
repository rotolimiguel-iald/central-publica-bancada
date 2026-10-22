# F1.2 — ponte compilada entre DualScalingData e o core regular v351

[REAL — sandbox, 07/10/2026] `V351DualScalingBridge.lean` compila sobre a cópia do kernel v351. `regularCoreDualScalingData` instancia `TGLExt.DualScalingData` com o traço `scalarInverseLimitTraceData` e a ação `positiveDual` do core regular. `finiteTracePositive_not_fixed` aplica o consumidor `DualScalingData.finite_trace_not_fixed` de `CornerFamily.lean` a esse objeto concreto. Ambos reportam somente `propext`, `Classical.choice`, `Quot.sound` e não há `sorry`/`admit`/`axiom` novo.

[DERIVED — tipagem] O traço v351 é `ℝ≥0∞`; o contrato antigo pede `ℝ`. Por isso o domínio é o subcone positivo de traço finito. A ação dual preserva esse subcone pela lei compilada `scalarInverseLimitWeight_dual`, e `ENNReal.toReal_ofReal_mul` entrega a lei real `τ(θ_s A)=exp(-s)τ(A)`. O teorema de não fixação é condicional a `A ≠ 0`, sem afirmar que um canto físico específico já foi construído.

[OPEN — escopo] A pedra não constrói um novo produto cruzado matricial `M_n ⋊ ℝ`, não identifica `SiteProfile` com `Matrix n n ℂ` e não altera o kernel canônico. `Fundacao.lean` consome a estrutura genérica em outro pacote; a instância agora existe para aplicação, mas esse arquivo não foi recompilado contra a ponte. O plano matricial anterior permanece registro histórico aberto. Esta entrega segue o alvo rebaseado do ADENDO 003.

[REAL — evidência] Compilação, hashes lidos e escopo: `sandbox/V351_BRIDGE_COMPILE_RESULT.json`; saída bruta: `sandbox/V351_BRIDGE_COMPILE.log`.
