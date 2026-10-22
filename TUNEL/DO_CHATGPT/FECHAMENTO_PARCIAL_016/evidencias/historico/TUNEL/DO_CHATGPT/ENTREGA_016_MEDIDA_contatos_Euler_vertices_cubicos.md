[DERIVED+CAS — dois contatos Euler dos vértices cúbicos; Q2 OPEN]

Calculados os contatos de duas linhas entre (qFaf)_Euler e Vghost,
com saída h,c. Eles diferem do descendente E_h[G,chi]w anteriormente
medido, cuja saída tem dois ghosts. Não são uma repetição desse diagrama.

 (qFaf)_Euler=E_A(Lie_c h)_A-(Qbarc)_i c^j d_j c^i.

No primeiro termo, E_A--h_B=box f delta_AB usa o inverso completo h,b.
A segunda contração é c--barc. No segundo termo há duas linhas ghosts;
o menos do vértice cancela o menos de barc--c, e os dois emparelhamentos
restantes têm sinais+ e-. Esses sinais foram conferidos por enumeração
independente da ordem dos cinco fatores ímpares, antes da soma tensorial.

Usamos a R_bal já declarada, mantendo todas as derivadas em cada linha,
os dois cutoffs e a adjunção que põe h à esquerda de c no resultado.
Foram computadas40componentes em cada ordem; dados: [{'order': 0, 'lambda_x': (1, -1, 0, 0), 'eta_y': (1, 0, 0, 0), 'contractions': [1020, 680], 'nonzero_metric': 40, 'nonzero_ghost': 40, 'nonzero_total': 40}, {'order': 1, 'lambda_x': (1, 0, 0, 0), 'eta_y': (1, -1, 0, 0), 'contractions': [1224, 816], 'nonzero_metric': 40, 'nonzero_ghost': 40, 'nonzero_total': 40}].

São valores de grafos crus divididos por CE, sem selecionar um peso para
zerar o subtotal. A tradução para os prefatores de Tc2/A2 ainda deve
acompanhar a fonte composta inteira. Não somamos silenciosamente esses
valores à matriz anterior. 84controles (incluem80verificações de
aritmética exata; não80identidades de Ward), CPU27.421875s,rc0.
Termos curvos e família completa continuam OPEN; nenhum gate alterado.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
