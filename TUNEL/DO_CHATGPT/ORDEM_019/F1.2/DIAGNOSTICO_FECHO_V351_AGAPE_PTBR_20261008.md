# F1.2 — não vacuidade e Fundação no core regular v351

**[REAL]** `F12Completion.finiteTracePositive_has_positive` produz `A : FiniteTracePositive P` com `0 < τ(A)` pela semifinitude e fidelidade do traço v351. A prova usa `positiveUnit P` para excluir o traço nulo, mas a testemunha finita obtida **não é a unidade**: a auditoria mostrou que a unidade tem traço infinito e está fora desse subcone.

**[REAL]** `F12Completion.agape_on_v351_core` aplica `TGLExt.Fundacao.agape` a `TGLV351.regularCoreDualScalingData P` e à testemunha positiva. A ponte anterior conserva `theta` como ação dual e `tau` como traço v351. As duas provas novas compilam só com `propext`, `Classical.choice` e `Quot.sound`, sem `sorry`, `admit` ou axioma novo.

**[OPEN]** O produto cruzado matricial `M_n ⋊_σ ℝ` do critério antigo, sua construção em L², o fecho de von Neumann e a equivalência que entrelaça a ação dual e um traço normal semifinito não são construídos aqui. O resultado Ágape vale no subcone positivo de traço finito do core regular. A testemunha demonstra não vacuidade desta instância concreta; não impede que `DualScalingData` tenha modelos triviais em outros tipos.

**Custódia.** A ponte antiga tem quatro declarações novas; o arquivo separado `MatrixInnerGauge.lean` tem seis; esta pedra acrescenta dois teoremas. Os arquivos históricos registrados como evidência permaneceram intactos. O `RESULTADO.json` corrente e seu backup original têm hashes distintos, medidos no manifesto; esta correção fica ao lado. A prova da sonda do auditor foi reaproveitada e citada por hash. O build lê os caches do kernel atual do Nós e recompila uma cópia byte a byte da ponte no sandbox. Nem o Nós original nem o `um.py` foram alterados.
