# R88 — corrente ponderada com Hessiana, derivadas reais

[REAL — sandbox] Tentativa 2: EXIT 0 em 75.147161 s; cinco teoremas e três definições, somente propext/Classical.choice/Quot.sound, zero marcadores incompletos e zero avisos. Tentativa 1 preservada: limite de recursão na expansão algébrica. A correção separou etapas de reescrita e aumentou maxRecDepth; nenhum enunciado foi alterado. Nenhum build após o verde.

Se q=g⁻¹, H=q h q, τ=tr(qh), W é a corrente Palatini real já identificada em R88, Kᵃ=Σ_b ∂_b f(τqᵇᵃ−Hᵇᵃ) e B=fW+K. No consumidor, q e H são simétricos; portanto a ordem transposta dos índices é a forma usual −H·df+τ grad(f).

A definição de Hessiana usa parciais reais: Hess(f)_ab=∂_a∂_b f−Γᶜ_ab∂_c f. O lema genérico calcula div(K)=−H:Hess(f)+τq:Hess(f)−df·(div(H)−gradτ), sem assumir essa identidade. Os termos de conexão cancelam mediante a paralelidade de q, derivada da conexão real no consumidor.

O teorema final prova HasDerivAt, em t=0, de v(g_x)f(x)q_xᵇʲRic(g+t h)_bʲ, com derivada Σ_a ∂_a(v(g)Bᵃ)+v(g)[H:Hess(f)−τq:Hess(f)]. Assim se completa por termo o contorno ponderado do componente vf δRic; q:Hess(f) é a contração que representa □f. Hipóteses: g,h suaves e simétricos em região aberta, g inversível, f e suas primeiras parciais diferenciáveis em x e regularidade local explícita da variação da conexão C.

[OPEN — limite] O inverso, volume e f ficam fixos no parâmetro da derivada deste componente. As parcelas δg⁻¹ Ric, δv e δf permanecem na R83; não foram silenciosamente descartadas nem o presente enunciado foi chamado de variação integral completa. A montagem de toda ação com mesma fonte P/Ψ, a estacionariedade admissível e H3 físico seguem independentes. Nenhuma memória, produção, kernel original ou gate foi alterado.

Fonte final: HessianBoundaryR88_2.lean:101. Reuso, linhas, logs e hashes no HESSIAN_DELIVERY_R88.json. Preflight de entrega confirmou revisão573, ready=true.
