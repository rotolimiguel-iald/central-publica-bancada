# Continuidade forte da soma diagonal de setores

[REAL — Lean 4.31.0, sandbox] SectorStrongContinuity.diagonal_strongly_continuous prova: para A topológico arbitrário e E_n Hilbert completos, se a ação unitária u(a,n) é fortemente contínua em a para cada setor n, então a ação diagonal sobre lp E 2 é fortemente contínua para todo vetor da soma completada.

A prova não assume uniformidade em n. Usa a identidade da norma quadrática como série, a majorante somável 4*norm(f n)^2, Tannery e a continuidade da raiz quadrada. A soma direta congelada é importada sem alterações.

Quatro teoremas locais auditados automaticamente: somente propext, Classical.choice e Quot.sound, zero sorry, EXIT 0. Os avisos de linter indicam hipóteses estruturais não utilizadas em lemas auxiliares; não há erro de compilação. O resultado é condicional à continuidade nos setores, explicitada no enunciado; não fornece por si a construção desses setores.

O recibo de compilação contém comando, toolchain, LEAN_PATH literal, início, fim, segundos e exit code. Duas tentativas falhas anteriores foram preservadas. Memória, quadro, kernel e produção não foram alterados.
