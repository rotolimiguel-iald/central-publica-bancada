[DERIVED+CAS — ligação dual ghost e Euler métrico completo em primeira curvatura; Q2 OPEN]

AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

1. Ghost: H^a_b foi dualizado para gX_ac H^c_d gY^db usando o motor
rotulado existente. A compatibilidade métrica foi confrontada com uma
recursão independente, com conexões covetorX/vetorY: 57 palavras,
2112 verificações, CPU0.890625s, rc0. Não há sinal
de Wick atribuído nesta ligação. Nos contatos sem jatos extras com
espectador ghost,16 dos256 valores mudam: nas componentes diagonais,
7/16 passa a1/4 (diferença−3/16), em unidades CE*K. O plano é preservado.

2. Métrica: implementado PH_hh=I_tr Lh P−Cstar S com
S=−2CP−HQ Kstar; P=Hh I_tr, HD=−4κP, ell=1/(2κ).
Cstar v=−sym∇v+g div(v)/2. Métricas, derivadas e densidade são
aplicadas antes da extensão. O código reaproveita os perfis e palavras
radiais; não introduz outro parâmetro nem troca a prescrição.
540 verificações, CPU10.4375s, rc0.

O bloco misto é zero fora da diagonal atéK, mas suas palavras rotuladas
não somam zero antes da extensão:22 dos100 contatos ganham contribuição.
Para o espectador métrico(01,01), a tabela inteira verifica:
 contato_misto/(CE*K)=(18 Id_sym−g⊗g)/128;
 contato_completo/(CE*K)=(10 Id_sym+31 g⊗g)/128.
200 comparações adicionais conferem estas fórmulas nas100 componentes.
Não extrapolamos essa tabela a espectador arbitrário nem a jatos maiores.

Falha preservada: o primeiro verificador deixou w independente de|x−y|²
na comparação fora da diagonal. Seu rc1 e log permanecem. A v2 impõe
essa relação só na realização ordinária; o motor rotulado não mudou.

Alcance: ligações necessárias à montagem, não a soma final de vértices.
Pesos temporais, montagem completa e Q2 integral continuam OPEN.
Crítica externa específica preparada; resultado ainda não recebido.
Nenhum original, kernel, gate, Atlas ou diário canônico foi alterado.
