# R84 — Conferência diferencial independente da geometria candidata

[REAL — execução simbólica] SymPy 1.14.0, uma execução, exit 0, 15 controles passaram; 3,362 s de cálculo, 4,395 s do processo. Resultados exatos, sem tolerância numérica.
[DERIVED] Das seis probabilidades da nota p_variations, o script calcula Fisher, relógio e g. A conexão e Ricci são calculados por derivadas coordenadas de g; a fórmula de produto entra somente como comparação posterior.
Calculados também □φ_j=3φ_j/a² para os cinco potenciais, T a partir dos mesmos gradientes e ∇ᵃT_ab=0 diretamente. O fator constante c_G=k_G/(π cosh²k_G)>0 é mantido simbólico; nenhuma calibração ou ajuste.
No ponto (π/2,π/4,π/4,π/4), duas direções nulas dão Ric(ℓ,ℓ)=1 e 7/4, enquanto T(ℓ,ℓ)/c_G=1/2 em ambas: exigiriam Cc_G=2 e Cc_G=7/2 simultaneamente. Λg não altera essas contrações nulas.
O domínio aberto 0<τ<π, 0<θ,χ,ψ<π/2 garante positividade das probabilidades e dos potenciais condicionais; Fisher diagonal positivo implica rank(dP)=4, e dp0≠0. Esse argumento de domínio está declarado, separado dos controles de igualdade simbólica.
A fonte selecionada é a sigma de SelectedProbabilitySigma:132–150, com finiteCovectorStressField e CoherentScalarStress:26–30. A convenção de Ricci foi conferida em CurvatureJetAlgebra:27–29 e MetricCurvatureSymmetries:31–32.
Escopo: verifica a geometria do contraexemplo candidato ao passo “mesmos P + conservação ⇒ H3”. Não demonstra estacionariedade dessa configuração, não verifica toda a dinâmica não minimal da TGL e não afirma solução física. Não é prova Lean; não fecha o objetivo R16.
Custódia: PLAN_GEOMETRY_R84.json e PREEXEC_PINS_R84.json precedem START; código, saídas, tempos e fontes integram DELIVERY_GEOMETRY_R84.json. Nenhum original, memória, produção ou gate alterado.
