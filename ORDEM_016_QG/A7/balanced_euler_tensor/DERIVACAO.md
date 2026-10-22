[DERIVED+CAS — contato composto Euler/ghost na prescrição balanceada; Q2 completa OPEN]

Reutilizada literalmente a função ordered_descendant do motor anterior, com
os mesmos vértices, duas contrações Grassmann e fatores de adjunção. Somente
o contato escalar mudou para soma_i DeltaR_(u+ii,v), declarado antes da conta.
O termo livre soma_i f_(u+ii) vale zero fora da diagonal; sua extensão composta
balanceada não é fixada por essa igualdade pontual. Ela não foi escolhida para
cancelar o resíduo Ward. Não se escolheu tau nem novo peso global.

Foram calculados os16 componentes em cada ordem de cutoffs lambda=(1, -1, 0, 0),eta=(1, 0, 0, 0),
com 852/532 contrações. Não nulos B,Brev,defeito,defeito-rev: [16, 16, 16, 16].
Rangos das colunas dos dois antigos kernels e dos dois novos: {'old': 2, 'augmented': 4}.
O teste compara os contatos, não procura coeficientes para ajustar o resultado.
A antissimetria graduada verificada é entre os DOIS CAMPOS GHOST ímpares;
ela não é antissimetrização das duas entradas pares F,G da identidade A2.
33 controles, CPU12.921875s, rc0.

Os demais diagramas ainda precisam ser convertidos à mesma prescrição.
Não somamos esses valores aos coeficientes R_raw como se fossem da mesma família.
Não prova anulação de A2 nem constrói a extensão curva causal completa.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
