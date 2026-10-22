# Extensão de Gram numa família total — R6

[REAL — compilado, revisão independente pendente] `GramTotalExtensionR4.lean`, namespace `F1Fecho.GramExtension`, para escalares RCLike (inclui ℝ/ℂ). Build Lean 4.31.0: EXIT 0, 19,190995 s; 12 declarações impressas somente em propext, Classical.choice e Quot.sound; zero sorry.

## Contrato e construção

Entradas: famílias f:ι→E e g:ι→F, igualdade de Gram `inner(g i,g j)=inner(f i,f j)` para todos i,j e `Total f`, definida como fechamento topológico do span de range f igual a ⊤. F é completo. A igualdade de Gram é transportada por somas finitas a todas as combinações lineares, obtendo igualdade de normas. Os mapas `Finsupp.linearCombination` são passados a `LinearMap.extendOfNorm`, já existente; isso constrói o mapa contínuo no Hilbert, sem supor independência linear dos geradores nem existência prévia da extensão. A preservação da norma passa à totalidade por densidade.

Saídas: `isometry f g hg hf : E →ₗᵢ[𝕜] F`; `isometry_apply` em cada gerador. Se E também é completo e `Total g`, `equivalence f g hg hf ht : E ≃ₗᵢ[𝕜] F`, reutilizando `LinearEquiv.extendOfIsometry` sobre a identidade no espaço de coeficientes. `equivalence_apply` preserva os geradores. `extensionMap_unique` prova unicidade entre mapas lineares contínuos coincidentes na família total.

`span_weighted_reindex` e `total_weighted_reindex` mostram que pesos c(i)≠0 e reindexação σ sobrejetiva conservam exatamente o span e sua totalidade. Para Weyl, σ(g)=g+f e c(g)=a(f,g) exponencial: a totalidade da imagem pode ser deduzida, sem postulá-la de novo. O pai fornecerá a igualdade de Gram escalar e a construção concreta dos vetores exponenciais.

## Alcance

Esta unidade constrói a extensão genérica. Não afirma ainda que a família concreta de exponenciais cumpre o contrato: seus lemas `exponential_inner`/`exponential_total` e o cociclo serão consumidos em unidade composicional pelo construtor designado. Não contém hipótese de isometria, inversa, extensão ou existência de operador Weyl. Não altera memória, produção, originais, kernel canônico, dados ou gate. O autor desta pedra não é seu auditor.

As três tentativas recusadas foram preservadas: R1 exigiu explicitar o corpo escalar; R2 exigiu expor definições/coerções; R3 ficou somente na coerção de pertinência ao span. Nenhuma foi promovida por exibir impressões de axiomas com `sorryAx` de recuperação do elaborador. Só R4, EXIT 0, é fonte aceita para revisão. Os avisos de linter remanescentes não são erros nem lacunas lógicas.

Reaproveitamento com arquivo/linha e hashes: `REUSE_R1.json`. Comando, LEAN_PATH literal, toolchain, início/fim, duração, stdout/stderr e hashes: recibo de build pinado em `DELIVERY_R1.json`.
