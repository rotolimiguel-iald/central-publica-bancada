# R85 — Primeiro elo curvo da corrente gravitacional

[REAL — Lean sandbox] PalatiniBoundaryR85_3.lean compilou em Lean4.31.0, exit0: 8 declarações (2 definições e 6 teoremas), somente propext/Classical.choice/Quot.sound, nenhum placeholder. Duas tentativas anteriores falharam por elaboração e estão preservadas; nenhuma quarta tentativa.
A direção C tem derivada de tensor (1,2), incluindo o índice covariante que identifica a direção da conexão. Sob ausência de torção, a variação de Ricci existente é exatamente ∇ₐCⱼᵃᵦ−∇ⱼCₐᵃᵦ.
A corrente construída é Wᵃ=qᵇʲCⱼᵃᵦ−qᵇᵃCⱼʲᵦ. A prova deriva suas parciais por produtos/somas e demonstra qᵇʲδRicᵦⱼ=∇ₐWᵃ quando q é paralelo.
No teorema final q=g⁻¹ e Γ é Levi-Civita. A compatibilidade de q é obtida do lema existente inverse_metric_derivative, a ausência de torção da construção existente, e δRic é a derivada real da família g+t h: não é uma hipótese do resultado desejado.
Importante: g⁻¹ fica FIXO na contração do teorema final. Trata g⁻¹·δRic, não a derivada completa de R, que possui também δg⁻¹·Ric e já aparece separadamente em MetricEinsteinVariation/R83.
Hipóteses locais: U aberto, g/h suaves, g simétrica e invertível; diferenciabilidade componente a componente de C=metricConnectionVariation g h explicitada. A regularidade de C não é uma equação de campo e não foi eliminada nesta pedra.
[OPEN — continuação concreta] Identificar W com ∇ᵦHᵃᵇ−∇ᵃtr(h); transportar ∇ₐWᵃ para ∂ₐ(vWᵃ); integrar a parcela ∂f·W para obter Hess(f)−g□f e a corrente completa B. Não se afirma que essas três conversões estejam provadas por este arquivo.
Reuso: CurvatureNonlinearVariation:256–263; MetricRicciVariation:208–224; GeometricEinsteinReconstruction:25–56; LeviCivitaLieVariation:49–72. Âncoras exatas e hashes em SOURCE_ANCHORS_R85.json.
Escopo: nenhuma estacionariedade em P, equação de Euler–Lagrange, H3, condição de contorno ou solução física foi assumida/concluída. Fontes canônicas somente leitura; nenhuma memória/produção/gate modificada.
