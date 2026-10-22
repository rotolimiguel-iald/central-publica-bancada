# Derivação e alternativas da integração externa F1(c)

[DERIVED — sem avaliação numérica] Seja J_i(θ)=∫L_i(y|θ,extra,η)π_i(extra)dextra dη o log-callback df482, já com as63 nuisances e somente os priors extras próprios integrados. H1/H2 não têm esse extra. O produto final desta camada é
\[
\widetilde Z_i=\int_{\Theta}J_i(\theta)\,\frac{50}{3}\,dH_0\,d\omega_b\,d\omega_c.
\]
A constante κ da medida nuisance comum está omitida em J e continua omitida aqui. A medida comum de dados e o prefator Gaussian são conservados. Uma comparação relativa na mesma admissão usa lnB_ij=lnZ̃_i−lnZ̃_j; não fornece evidência absoluta em η nem p/sigma.

Com u∈[0,1]^3 e θ_k=l_k+(r_k−l_k)u_k, o Jacobiano é40×(3/200)×(1/10)=3/50. Logo (50/3)dθ=du exatamente no modelo do prior. A integração exterior é uma média uniforme no cubo inteiro, sem fatores extras de densidade ou corte de caixa.

A alternativa A é cubatura adaptativa conjunta logescalada. Ela pode concentrar trabalho em estruturas localizadas; depende de um serviço adaptativo qualificado e seu estimador local também pode não enxergar picos fora dos nós. A alternativa B escolhida é produto de Simpson composto positivo em grades diádicas aninhadas, com dependências apenas da stdlib. Ela privilegia transparência de cobertura do domínio e reaproveitamento exato de identidade dos nós, pagando crescimento cúbico. Nenhuma dessas alternativas certifica sozinha ausência de pico estreito não amostrado.

Para n=2^L, os pesos1D são (1,4,2,...,4,1)/(3n); sua soma é1. O produto3D também soma1 e conserva a positividade do integrando. Em logs,
\[
\log\widehat Z_{i,L}=m+\log\sum_{abc}\exp(\log J_i(\theta_{abc})+\log w_{abc}-m),
\]
onde m é o máximo dos termos ponderados finitos. Isso evita exponenciar diretamente grandes logs absolutos. Uma densidade zero legítima contribui zero; um erro de callback interrompe a integral inteira.

Todos os níveis previamente indicados são computados, sem teste de parada adaptativo. A diferença entre os dois últimos logs é um diagnóstico de refinamento, não um estimador certificado. Não se aplica automaticamente o fator1/15 de Richardson: a quarta ordem assintótica exige suavidade/regime que não foram demonstrados para este integrando completo. A concentração de contribuição e a massa dos nós de fronteira ajudam a reconhecer sub-resolução, sem provar seu contrário.

Cada novo nó fornece os CINCO resultados conjuntamente. A cache só armazena retornos completos validados; repetição de uma identidade canônica em nível posterior reutiliza esses valores, com os pesos próprios do nível. O número total de callbacks é o número de nós da grade final, não a soma dos números de nós por nível. O controlador conserva a exclusão de repetição de resultados incertos além da memória de um processo.

A integral interior de df482, seus erros e o fundo entram como entradas explícitas. Esta camada não abre observações nem cria outra álgebra gaussiana, modelo cosmológico, normalização nuisance ou prior. O serviço da gerente f820 continua independente. Uma avaliação CAMB e montagem c435 já consumida não é repetida por este preparo.

[REAL — esta entrega] Somente código/documentos/AST/metadados; nenhuma regra, soma, nó, callback, solver, controle ou observação avaliada. A revisão independente e a futura admissão do plano continuam separadas desta preparação.
