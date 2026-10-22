[DERIVED — recorrência de Killing conferida; resto do parecer refutado]

Resposta Kimi9c1 foi lida integralmente,238 linhas. A máquina não tomou
VERIFICADO escrito pelo modelo como verificação local. O parecer explicita
que não executou código; aqui1136 verificações exatas terminaram rc0.

Aceito neste escopo: k_i^a=delta_i^a-K(xx delta_i^a-x^a x_i)/3
satisfaz Lie_k g=0 até primeira ordemK, para
g_ab=delta_ab-K(xx delta_ab-x_a x_b)/3.
A conexão derivada dessa métrica confere com o motor existente.
O operador D_i=k_i.partialX+rho_X, com rho_X atuando nos índices X,
fornece partial_Yi G|0=-D_i G|0. A segunda derivada parcial é
partial_Yj partial_Yi G|0=D_i D_j G|0-sum_{slotsY} Q_jB,i^c G_(B->c),
Q_jB,i^c=partial_Yj partial_YB k_i^c(0).
Para índices covariantesY, -Q_jB,i^c=partial_Yi Gamma^c_jB(0).
Essas correções não podem ser descartadas ao repetir a derivada.

Conferidos:64 componentes de primeira derivada ghost;256 de segunda;
400 primeiras derivadas métricas (10x10x4); mais identidades de Killing,
conexão, distância e termo Q. Não se verificaram aqui todas as segundas
derivadas métricas, nem se alegou precisão em K² ou um estado completo.

Refutado: a §5.3 do parecer afirma falta de2K deltaij deltaAB/(3w)
no kernel. A recorrência e o kernel concordam exatamente em todas256
segundas derivadas ghost. A origem do erro é localizável:
distance1=-(xx yy-(X.Y)^2)/3,
partial_Yi partial_Yj distance1|0=-2(xx deltaij-XiXj)/3.
O parecer reteve2XiXj/3 e omitiu-2xx deltaij/3. Como o propagador tem
-distance1 deltaAB/w², o termo omitido fornece justamente
+2xx deltaij deltaAB/(3w²). Ele já existe no kernel; nada deve ser somado.

Controle X=(1,2,-1,1),w=7,i=j=0,A=B=1:
derivada e recorrência dão-473/2058; o extra alegado seria2/21.
No controle i=0,j=1,A=1,B=2, ambos37/1029.
O resto reivindicado é não nulo em16 componentes de índices; falha nas16.
Isso não é suporte na diagonal X=Y:1/w, mesmo se estivesse presente,
seria singular fora dela, não automaticamente um contato de delta.

Errata menor: a primeira fórmula de Gamma na §1.1 está com sinal
oposto ao motor (36 componentes não nulas). Fórmulas posteriores do
parecer usam o sinal correto. Não foi necessária alteração do motor.
Também os exemplos individuais de primeira derivada no parecer omitem
derivadas logarítmicas que cancelam na diferença; nossa conferência usa
a função completa, inclusive log, e não essa abreviação como igualdade.

Resultado útil: a recorrência é um verificador independente dos jatos,
mantido sem dY=-dX ingênuo. Não é autorização para reparar o propagador
com o termo espúrio, nem conclusão sobre Q2, W suave ou estado físico.
O kernel e a prescrição de extensão permanecem inalterados.
