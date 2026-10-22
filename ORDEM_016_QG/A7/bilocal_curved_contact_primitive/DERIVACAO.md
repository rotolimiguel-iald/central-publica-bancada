[DERIVED — identidade diferencial covariante formal até O(K); identificação com o contato distribucional ainda em auditoria]

# Primitiva quadrática e a hipótese que resta conferir

Considere um espaço-forma auxiliar euclidiano de dimensão quatro, Ric=3Kg,
o operador de gauge (Gc)_ab=∇_a c_b+∇_b c_a e suporte compacto. Não se
identifica K com o gerador modular nem se escolhe um horizonte físico aqui.

O contato medido anteriormente tem três coeficientes na ordem cinco e
três na ordem K vezes três. Definimos A_cov substituindo cada monômio
pelas derivadas covariantes TOTALMENTE simetrizadas do covetor c.
Essa é uma definição de completação, ainda não uma prova de que coincide
com a transposição distribucional do contato original nos dois extremos.

Defina a Hessiana N por cinco estruturas de quarta ordem e quatro de
segunda ordem multiplicadas por K. Sua implementação integral é
loop_gauge em oneform_second_curvature_engine_v2.py. O sinal negativo
da parte K∇² corresponde ao símbolo positivo Kp². A normalização dos
termos mistos inclui o fator 1/2 explícito nesse arquivo. Os coeficientes
exatos, sem arredondamento, estão em results.json. b,c,t são livres.

O cálculo obtém, para cada uma das duas completações de regulador,

    N_bct G c = A_cov c + O(K²).

Três amostras numéricas somente identificam a solução do sistema linear
na base predefinida. A aceitação usa depois quatro polarizações
independentes e momentos p0,p1,p2,p3 simbólicos, em todos os 16 componentes,
nas duas ordens e nas duas completações: 256 igualdades polinomiais.
As conexões atuam também em cada índice de derivada; não se substitui
simplesmente ∇ por ip antes de compor N com G.

## O que essa verificação pode sustentar

Ao longo de uma geodésica radial, trivialize o fibrado por transporte
paralelo. A n-ésima derivada do componente nessa trivialização, na origem,
é a contração radial de ∇_(i1...in)c. A identidade polinomial em todas as
direções, polarizada, determina os jatos simétricos. Os jatos ordenados
são recuperados com os comutadores de curvatura, que o motor conserva.
Essa observação explica o uso de ondas em frame paralelo para verificar
o operador A_cov definido acima. Não demonstra automaticamente a regra
de integração por partes de uma distribuição bilocal calculada em outra
convenção de densidade ou de extremo.

Os tensores coeficientes de N são reais e paralelos. A transposição das
fibras preserva cada estrutura ou troca os dois termos de um par que
tem o mesmo coeficiente. Para palavras de comprimento par completamente
simetrizadas, a reversão da palavra produz a mesma média. Com a medida
geométrica e suporte compacto isso dá N*=N formalmente. O exame independente
foi encomendado ao DeepSeek; seu parecer não substituirá essa verificação.

Portanto, para a anomalia FORMAL A_cov integrada na convenção correspondente,

    B_bct = -C_E/2 ∫ h.N_bct h,       C_E=-4π²,
    s0 B_bct = -C_E ∫ h.A_cov c + O(K²).

Nenhum valor de b,c,t foi escolhido; nenhuma subtração foi incorporada
ao produto temporal ou ao programa canônico.

## Ponte distribucional a auditar

No contato anterior, q significa derivada de delta em X e os coeficientes
foram calculados com volume e conversão de frame. Passar dessa distribuição
para um operador em c(Y) exige indicar sobre qual teste a derivada age,
transpor índices e integrar por partes. As ordens ímpares tornam obrigatório
conferir o sinal. Mudar a âncora pode acrescentar termos que não são vistos
por uma comparação pontual. O regulador coordenado w não ganha naturalidade
por ser reescrito numa base covariante em uma única origem.

Essa ponte é o objeto específico da nova unidade Kimi; o resultado local
acima permanece uma identidade da completação formal enquanto ela é
auditada. Não se anuncia ainda remoção do contato realmente medido.

## Localização e próxima aridade

Se N*=N e χ é um corte escalar fixo, a variação de
Bχ=-C_E/2∫χ h.Nh contém Nχ além de χN. Assim a forma esperada envolve
χN+[N,χ]/2; descartar o comutador apaga termos de borda do corte.
A expansão ordenada de quarta ordem foi solicitada separadamente ao DeepSeek.

Com A1=-s0B e s0A2+s1A1=0, a combinação fechada é A2+s1B, pois
s0s1=-s1s0. Isso não fornece A2 nem uma primitiva cúbica por si só.
Continuam ausentes desta entrega W geral, demais diagramas locais,
K², aridades superiores e valores de contorno lorentzianos. Q2 completa OPEN.
