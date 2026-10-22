[DERIVED — fonte plana com fronteira ghost; montagem parcial de contatos]

O vértice Y é o mesmo que agora entra no par ghost:
integral chiY barc divZ=-integral(chiY dbarc+dchiY barc)Z.
Assim não basta multiplicar por chiY os coeficientes antigos A e B.
Aeta e Beta incorporam a substituição, na linha ghost interna,
partial_Ymu f -> (-d_mu+eta_mu)f, com d=partial_(X-Y).
As derivadas no outro extremo da linha são mantidas. Os sinais e a
contração dirigida são os do vértice já existente. O código explicita
os três termos de Lie_c h, o propagador métrico e seu traço revertido.

Depois da adjunção do ghost externo, a fonte é
Heta=Aeta+sum_j(d_j-eta_j)Beta^j.
Por isso existem termos quadráticos em eta, embora o vértice só tenha
uma derivada de cutoff. Eles vêm da adjunção sobre o coeficiente.
O operador em X continua o Einstein linear não fixado por gauge.

P=E_X{chiX[chiY R(Aeta)-divY(chiY R(Beta))]},
Q=R E_X{chiX chiY Heta}, C_D=R D-D R:
P-Q=-C_E(chiX chiY Heta)+E_X[chiX chiY C_divY(Beta)].
Não há termo de contato autônomo na adjunção das distribuições; ele está
na diferença entre aplicar derivadas antes e depois da extensão R.

Duas rotas calculam esse contato. A primeira usa a tabela C_D, Leibniz
completo e q->q-lambda para multiplicar chiX sobre derivadas de delta.
A segunda extrai o resíduo da expressão regulada
E_(d+lambda+2a*x/z)(Heta+a*2sum x_j Beta^j/z)-E_(d+lambda)Heta.
Só o coeficiente linear em a contribui para esses kernels racionais com
polos simples. Essa simplificação não é exportada a kernels logarítmicos.

488 verificações exatas:320 comparações com B antigo e C reduzido,
80 contrações de fronteira contra jatos de bitensores independentes,
40 recuperações do contato constante e48 comparações entre os dois
cálculos da extensão. Geradas120 componentes fonte (10x4x3 cutoffs).
Os dois métodos de extensão foram comparados para r=0; não declarar
que todas120 receberam a mesma comparação independente.

Falha preservada: v1 comparou polinômios tratando z independente de x.
Por exemplo,34x0²/z4-2(x1²+x2²+x3²)/z4-8/z3 versus36x0²/z4-10/z3
diferem por2(z-sum x²)/z4. No domínio z=sum x² são iguais. v2 usa
redução nesse ideal SOMENTE na comparação de kernels fora da diagonal;
o motor e o esquema de extensão não foram alterados. Logs/predecessor
estão preservados. Não se substituiu um desacordo numérico por tolerância.

Somados os contatos aos pares completos já calculados, na mesma
normalização CE=-4pi², obtém-se a tabela do JSON de montagem. Esta soma
é fonte+pares, ainda não a quebra Q2: as inserções da corrente BRST
clássica precisam ser calculadas na mesma prescrição. São igualmente
pendentes curvatura, partes suaves/tadpoles, aridades e causalidade.
Nenhum contato isolado não nulo demonstra obstrução cohomológica.
