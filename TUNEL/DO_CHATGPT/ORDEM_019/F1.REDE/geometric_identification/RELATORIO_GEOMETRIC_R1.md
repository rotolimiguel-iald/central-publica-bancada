# F1.REDE — identificação geométrica da conjugação

[REAL — Lean 4.31.0, sandbox] Duas fontes novas e a sonda de axiomas compilam com EXIT 0. Todas as 22 declarações locais usam só propext, Classical.choice e Quot.sound; zero sorry. Os recibos incluem início, fim, segundos, comando, toolchain, LEAN_PATH literal e hashes.

FourierConjugation prova, para antiunitária involutiva num Hilbert complexo, F(Cf)(xi)=C(Ff(-xi)). A identidade é demonstrada primeiro no integral de Bochner e nas funções de Schwartz, depois estendida a todo L² por densidade e continuidade. A relação com Fourier não é hipótese.

GeometricIdentification constrói productJ independentemente do Jcandidate anterior: reflexão do vetor transversal q, conjugação das componentes e troca de helicidades, mantendo a rapidez r. A medida produto é preservada. A currificação de Fubini entrelaça essa ação com a antiunitária da fibra.

Resultados exatos: Jcandidate_rapidity e Jcandidate_eq_geometricJ identificam operadores L²; Jcandidate_rapidity_coordinates prova, quase em toda parte na medida produto, (toRapidity(Jcandidate f))(q,r,i)=star((toRapidity f)(-q,r,helicitySwap i)). O H1 e a carta canônica não foram alterados.

[OPEN] A covariância completa de Poincare, a identificação da localização dos subespaços em todas as cunhas e a rede 4D são obrigações posteriores. Esta entrega paga a fórmula geométrica da antiunitária na carta de rapidez. Não integra produção, não altera o kernel, memória, quadro ou gate; a raiz coordena os registros e a revisão independente.
