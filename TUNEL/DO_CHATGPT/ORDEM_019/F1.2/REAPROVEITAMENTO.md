# F1.2 — escala dual: reaproveitamento e ligação pendente

07/10/2026 · [REAL] Consulta prévia `C:\Python314\python.exe C:\IALD\NOS_VIVO\consultar.py --unidade F1.2`. Foram lidas as três entregas `ENTREGA_011_A1_*` no túnel, a correção posterior `TETELESTAI_V351_FECHO_MATEMATICO\LACUNAS_A1.md` e as fontes canônicas indicadas em `RESULTADO.json`.

## O que já existe

1. [REAL/KERNEL] `V351RegularGeneratorDualScaling.regularPositiveGenerator_dual_scaling`: o mesmo gerador regular no espaço L² obedece à conjugação dual, com domínio controlado. A ORDEM 011 A1 registrou compilação autoral e revisão independente, rc=0, sem `sorry`, com o trio `propext`, `Classical.choice`, `Quot.sound`.
2. [REAL/KERNEL] `V351InverseLimitScaling.scalarInverseLimitWeight_dual` demonstra `τ(θ_s X)=ENNReal.ofReal (exp(-s))·τ(X)` para o mesmo `PositiveCoreInput` e a mesma ação `positiveDual`, inclusive quando o peso vale infinito. A demonstração usa o peso dual invariante no sanduíche e a cofinalidade dos reguladores. **Peso dual invariante e traço canônico escalante são objetos distintos.**
3. [REAL/KERNEL] A nota A1(b) de 14/09 dizia que a tracialidade e a semifinitude ainda estavam abertas **naquela etapa**. A construção posterior `V351RegularCoreTraceConstruction.scalarInverseLimitTraceData` preenche os campos `zero`, aditividade, homogeneidade, monotonia, fidelidade, normalidade, semifinitude, tracialidade e escala dual do `RegularCoreTraceData` **para o núcleo regular parametrizado por `SiteProfile`**. `V351QuadraticTrace` e os fornecedores importados pagam a tracialidade. Esta evolução corrige a leitura histórica sem sobrescrever o recibo antigo.

## Árvore da ORDEM 019

| Rota | Resultado nesta inspeção | Evidência / próximo elo |
|---|---|---|
| A — núcleo contínuo geral | [KNOWN/VINCULADO] Teorema de Takesaki para a álgebra da luz consta como campo de `FockCertificate`; não há habitante físico do certificado | A construção regular v351 é concreta, mas não instancia por si a cunha da luz. |
| B — multiplicação em L²(ℝ), Fourier | [REAL/KERNEL] Já entregue na ORDEM 011 A1 e fechado no contrato regular v351 | Reaproveitar os termos acima. Não repetir a pedra. |
| C — estágios `2^{-n}ℤ` | [REAL/KERNEL] `GlobalLiftLadder` prova aproximação diádica; o próprio módulo mostra que a escala não cria traço não nulo em estágio fixo | Não identificar limite de grupos com construção automática do núcleo contínuo. |
| D — parede | [OPEN] A ligação exata do produto cruzado `M_n⋊_σℝ` com o tipo `RegularCoreTraceData P` ainda não foi localizada como teorema Lean | Especificar morfismo da representação regular matricial contínua para o núcleo v351 e transportar ação, peso e traço; compilar em sandbox antes de qualquer alegação de fechamento desta face. |

[REAL] `FiniteCrossedProduct.lean` trabalha com **grupo finito** e `Matrix n n ℂ`: sua ação dual de personagens é compacta, e o próprio arquivo declara que não há escala real de traço ali. Portanto, a prova de F1.2 é a escala no modelo regular contínuo já existente; a identificação explícita do modelo matricial é um elo separado. Nenhuma execução Lean nova foi necessária para constatar isso, nem foi executada nesta inspeção. A auditoria de compilação aqui é a da entrega 011 e dos fornecedores posteriores, não uma nova reprodução independente da v391.

[OPEN] Critério para uma nova pedra: apresentar a assinatura do morfismo `M_n⋊_σℝ → regularCoreAlgebra P`, mostrar que preserva `dualAction` e o peso limite, e então aplicar `scalarInverseLimitTraceData`. Se a forma do morfismo exigir hipóteses adicionais (por exemplo, matriz de densidade fiel e regularidade do fluxo interno), registrá-las no tipo. A tarefa não autoriza substituir o núcleo contínuo por uma identidade do grupo finito.
