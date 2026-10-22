# R75 — consumidor bosônico preparado

Reutilização por AST dos corpos exatos `liou`, `model`, `include` de R66 (linhas/pinos no plano), sem executar seu main; fatores √n, cinco canais e bomba preservados. Reuso das duas atribuições do decoder C/B R62 e da hierarquia de momentos R64/R74. Cortes totais N≤2,3,4, dimensões 9,16,25; estado comum N≤1; T=.75. Quatro configurações de homódino separadas, resolvidas em um vetor batched por corte. Um quarto solve no corte3 transporta o quadro R74; há conferência pontual independente contra H' e os cinco L' explícitos.

A estimativa nova é a série Dyson ponderada da nota BOSONIC_FILTERED_MOMENTS_R75.md. O consumidor usa majorantes geométricos positivos, guardando denominadores, e entrega bounds para cada corte contra o limite analítico, além de comparar todas as duplas finitas. Ganhos são retirados no decoder e no respectivo bound. O maior corte não é referência infinita exata. Covariâncias e C/B centrados recebem propagação de erro própria.

Negativos algébricos fixados: coeficiente de abaixamento n=2, não comutação entre comprimir e elevar uma quadratura ao quadrado, e termo shot omitido. Os dois últimos controles são identidades locais/analíticas; não fingem uma execução extra de receptor errado. Não se extrapola controle de norma-traço para observável ilimitado sem o bound ponderado.

Plano e scripts preparados, nenhuma execução. Revisão distinta antes de FREEZE, START e rodada única. Não se constrói medida global de saída/HP ilimitado nem calibração física por esta camada.

