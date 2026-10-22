# R87 — corrente de Palatini pela variação simétrica

[REAL — sandbox] Tentativa 2: EXIT 0, 56.555342 s, cinco teoremas, somente propext/Classical.choice/Quot.sound, zero marcadores de prova incompleta e zero avisos. A tentativa 1 falhou apenas na normalização dos representantes Fin; permanece arquivada. Nenhuma execução adicional após o verde.

Escreva q=g⁻¹, D_k=∇_k h, com h covariante simétrico e Γ a conexão Levi-Civita real do kernel. `lower_covariant_variation` prova lowerChristoffel(D)_i=lowerChristoffel(dh)_i−hΓ_i usando simetria e torção nula. `actual_connection_variation_covariant` liga isso ao δΓ de g+t h, sem hipótese da igualdade-alvo.

A contração provada é Wᵃ=Σ_b(q D_b q)ᵃᵇ−Σ_k qᵃᵏ tr(q D_k), no mesmo `palatiniCurrent` já consumido pela derivada real de Ricci em R85 e pela divergência com volume em R86. Não se define uma nova corrente para tornar a igualdade tautológica. A simetria de D é derivada da simetria de h e dh.

[OPEN — limite preciso] A pedra prova as contrações covariantes ponto a ponto. A identificação delas com derivadas ordinárias/covariantes do campo levantado H=q h q e da função tr(qh), o fechamento da corrente Hess(f), a montagem variacional completa e a estacionariedade em P ainda não são teoremas desta pedra. Não conclui H3 nem equação física de fonte completa.

Fontes e linhas: SOURCE_PINS_R87.json; declaração final em SymmetricBoundaryR87_2.lean:72. Fontes canônicas, memória, produção e gate preservados.
