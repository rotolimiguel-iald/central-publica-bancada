[DERIVED+CAS — setor escalar até K²; correspondência local medida, Q2 integral OPEN]

AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

No mesmo auxiliar euclidiano4D espaço-forma, calculamos o contato real
Euler_phi(X)c.grad(phi)(X) com o vértice cúbico h(phi,phi)(Y), três sabores,
na extensão parcial rotulada R_bal mais a regra de linha suave já fixada.
O parametrix singular local, sem acrescentar estado suave, é
H(r)=1/r²+K(1/4−log(r²)/2)+19K²r²/480.
A distância bilocal r²=w+K d1+K²d2 vem da lei dos cossenos do espaço-forma:
d1=−(xx yy−xy²)/3;d2=−(xx+yy−4xy)(xx yy−xy²)/45.
A verificação radial dá Lap H=29K²/20, compatível com o coeficiente de
calor anterior. É um parametrix, não um estado/bissolução global. A derivada
em Y desse termo constante desaparece nesta ordem; mantivemos isso separado
da extensão na diagonal. A primeira tentativa de controle exigia expand=0
numa expressão racional; cancel confirma a mesma identidade, sem trocar H.

O contato K² CE em derivadas coordenadas de delta é
 509/1920 δab Qr −187/1920(δar Qb+δbr Qa).
A leitura no fantasma contravariante transportado inclui P1=(xx I−xxᵀ)/6
e P2=7xx(xx I−xxᵀ)/360. Ela dá
 1289/5760 δab Qr −17/1152(δar Qb+δbr Qa).
Os jatos de transporte foram conferidos por preservação métrica e pela
ação das distribuições em funções-teste. Não se confundem esses dois pares.

Com os contatos de graus5,3,1, obteve-se N=N4+K N2+K² N0, usando o motor
covariante de jatos existente. N G(c) coincide com o polinômio medido nas
quatro polarizações, com momento simbólico e parâmetros b,c,t ainda livres.
N4,N2,N0 completos estão no results.json; nenhum parâmetro foi escolhido.
O fator da distribuição integrada em exp(ipx) é−i CE; ele foi mantido
explícito para não trocar o sinal entre graus5,3,1.

Isso paga a correspondência local deste setor na leitura declarada.
Ainda NÃO paga a naturalidade da família temporal integral, o setor
métrico/ghost completo, os cutoffs, as inserções compostas nem a classe
de Q2 inteira. O emprego como contratermo BRST exige conferir o adjunto
formal e transportar a identidade local ao funcional com esse mesmo sinal.
Crítica Kimi preparada para essa ligação; MiMo para a construção geométrica
de H até K². Resultados de modelos serão auditados separadamente.

Comandos,rc0 e CPU: scalar_parallel_readout.py,5.875s;
scalar_measured_primitive.py,4.765625s;
scalar_second_curvature_check_v2.py,49.484375s;
scalar_second_parallel_primitive.py,46.828125s.
Controles respectivos217,128,312,296. São controles CAS exatos, não
compilações Lean. C6ACTIVE; prazo original inalterado. Originais/gate intactos.
