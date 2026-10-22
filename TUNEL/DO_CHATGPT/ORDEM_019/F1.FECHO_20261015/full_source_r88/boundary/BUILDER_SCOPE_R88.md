# R88 — corrente em derivadas dos campos reais

[REAL — sandbox] Primeira tentativa: EXIT 0, 57.067149 s, cinco teoremas e uma definição, somente propext/Classical.choice/Quot.sound, zero marcadores incompletos e zero avisos. Sem recompilação após o verde.

Para q=g⁻¹, H=q h q e t=tr(qh), a pedra prova ∇_k H=q(∇_k h)q e ∂_k t=tr(q∇_k h). A derivada contravariante contém as parciais efetivas tensorFieldJet H mais Γ_k H+H Γ_kᵀ; não é definida pela expressão desejada. A regra de produto é aplicada aos campos reais. O cancelamento na derivada do traço usa ciclicidade.

A paralelidade da inversa, inicialmente premissa dos lemas genéricos, é derivada no consumidor final por inverse_metric_derivative e compatibilidade da conexão Levi-Civita do próprio g. Portanto, para g/h suaves e simétricos numa região aberta, g inversível, o mesmo palatiniCurrent de R85/R86/R87 satisfaz Wᵃ=Σ_b∇_b Hᵃᵇ−Σ_k qᵃᵏ∂_k t. A igualdade-alvo não é hipótese; não há restrição a fundo plano.

[OPEN] Esta camada não prova a corrente ponderada com Hess(f), a ação integral completa do mesmo P/Ψ, sua estacionariedade nem a fonte física completa/H3. Reutiliza as compilações anteriores por imports; não as reexecuta. Memória, kernel canônico, produção, dado e gate preservados.

Evidências: BUILD_1.json/log, AXIOMS_VERIFIED_R88.json e SOURCE_PINS_R88.json. Declaração final: RaisedBoundaryR88_1.lean:83.
