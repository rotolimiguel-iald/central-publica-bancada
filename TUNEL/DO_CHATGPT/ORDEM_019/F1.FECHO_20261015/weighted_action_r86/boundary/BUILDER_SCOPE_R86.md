# R86 — Corrente curva com volume e peso escalar

[REAL — Lean sandbox] WeightedPalatiniR86_3.lean compilou em Lean4.31.0, exit0: 10 teoremas, somente propext/Classical.choice/Quot.sound, zero sorry e zero avisos. Duas tentativas anteriores preservadas, sem quarta execução.
O diferencial de v(G)=sqrt|det G| foi obtido da diferenciabilidade do determinante multilinear e da variação afim já existente; sua composição com g(x) produz a parcial espacial real. Compatibilidade métrica prova ∂ₐv=v tr(Γₐ), e torção nula prova ∂ₐ(vVᵃ)=v∇ₐVᵃ.
Reaproveitando W da R85, a nova conclusão curva é v f gᵇʲδRicᵦⱼ=∂ₐ(v f Wᵃ)−v(∂ₐf)Wᵃ. O último teorema é HasDerivAt da família real g+t h, com métrica inversa, v e f fixos na contração temporal; a variação espacial de f entra explicitamente na divergência.
Não é a derivada inteira de v f R: δv, δf e δg⁻¹·Ric permanecem as parcelas existentes de R83; esta pedra fecha o transporte da parcela δRic para a divergência coordenada.
Nenhuma identidade de volume ou corrente desejada foi tomada como hipótese. Hipóteses locais: g/h suaves, g simétrica invertível, f diferenciável e a regularidade explícita de C=δΓ já usada na R85. Originais, kernel e produção somente leitura.
[OPEN — passo seguinte] Identificar W=div(H)−grad(tr h), integrar/reorganizar df·W em Hess(f)−g□f e conectar a corrente B completa à identidade integrada. Estacionariedade em P e sua suficiência para a equação métrica não são concluídas aqui.
Reuso: ScalarMatterDensityVariation:43–83 (determinante e volume), MetricFieldConnection/MetricCurvatureSymmetries (compatibilidade e torção), PalatiniBoundaryR85_3 (cópia byte a byte de fonte/olean). Pinos anteriores à execução em PREBUILD_PINS_1/2/3; comando, toolchain, LEAN_PATH literal, início/fim e duração em BUILD_3.json.
As falhas1/2 foram de configuração da norma matricial e ordem de reescrita do traço, respectivamente; o histórico registra sorryAx gerado pelo Lean nas tentativas com erro, que não são entregas validadas. A tentativa3 não contém esse axioma.
Nenhum dado observado, provedor, memória, mapa/quadro ou gate foi alterado pelo construtor.
