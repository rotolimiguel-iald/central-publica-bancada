# R78 — resposta complexa OH–luz, candidato de ensaio

[INPUT] Pré-registro sintético anterior à execução: corte total N≤3 (dimensão16), três ramos e dois preparos P1 fixados. O OH fornece a face na interpretação do autor; não se impõe OH no fundamental nem G_OH como polarização.

[DERIVED] Reutiliza por AST as funções model/liou R66 (linhas63–89), com as cinco dissipações, bomba e J=A+B indiviso. Beta vem de CODATA*sqrt(e) em runtime; todas as taxas são INPUT, incluindo Gamma. Não importa nem executa o script original.

Para h_epsilon=h+epsilon X, V=-i[X,.], a matriz em blocos [[G,0],[V,G]] propaga rho e sua primeira variação Duhamel. Duas direções X_in/P_in, multiplicadas por ganho1,3 sqrt(kappa_in), representam sondas Hamiltonianas; seu vínculo ao laser/RF real continua OPEN. Dois epsilon fixos verificam a diferença central, sem calibrar parâmetros.

O receptor usa Lout e duas referências LO para a média complexa z=(QX+iQP)/sqrt2. Não há feedthrough coerente nesta porta distinta da entrada. A fase LO incorreta gira z por exp(-i0,6); detectabilidade da mudança da resposta é informada, não exigida quando nula.

O preparo sem semente retira apenas a amplitude inicial de |010>; sinal coerente nulo é admissível e visível. O semeado testa modulação condicionada. O controle gJC=lambda=0 bloqueia os dois acoplamentos neste modelo, mantendo bomba/demais perdas: não identifica sozinho qual mecanismo físico atuaria.

Também registra primeiras variações de n_out e ai†ao, explicitamente intracavidade, sem chamá-las correlação temporal do detector. O defeito hP-i hX é diagnóstico de resposta complexa escalar; não se força sua anulação nem a lei tanh/gS_beta.

O contato de ruído para integral boxcar de duraçãoT é gain² T/2, não variância total nem SNR. Não há ramo estacionário/resolvente, dado, calibração material ou erro para Fock infinito: a nova sonda Hamiltoniana não herda silenciosamente a cota R75 da bomba. Aprovação dos checks é validade numérica finita, não fechamento R4/R5.
