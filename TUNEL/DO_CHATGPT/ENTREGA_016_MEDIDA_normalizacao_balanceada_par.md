[DERIVED+CAS — normalização diferencial explícita do par escalar; Q2 completa OPEN]

Correção do teste: v1 terminou rc1 porque coeff(q0,2) foi aplicado antes
da expansão algébrica, perdendo o termo tau. A v2 expande antes de extrair;
não altera a prescrição nem seus coeficientes. Original e pré-registro preservados.

Declaramos ANTES da conta uma continuação por derivadas balanceadas:
Dtot=D1+D2, Dbal=(D1-D2)/2. Os primários Dbal^v(fg) recebem a extensão
radial R anterior; as derivadas Dtot são aplicadas DEPOIS de estender.
Para derivadas individuais, expandimos D1=Dtot/2+Dbal e D2=Dtot/2-Dbal.
Cada termo Dtot^u R(Dbal^v(fg)) difere de R(Dtot^u Dbal^v(fg)) pelo
contato -CE C_u já calculável no motor existente. Nenhum resíduo Ward foi
usado para ajustar coeficientes. A tabela tem 495 pares até ordem4.

Esta é R_bal, uma continuação explícita. O par SEM derivadas é o mesmo,
mas produtos de linhas derivadas recebem correções locais. Portanto os
números anteriores de R_raw não podem ser somados aos novos sem conversão.
Isso não altera os artefatos anteriores nem seleciona uma leitura física.

Para f=g=1/z, no auxiliar euclidiano, obtivemos
 R_bal((Delta f)g)/CE=3q²/32,
 R_bal(f(Delta g))/CE=3q²/32,
 R_bal(grad f.grad g)=4R(z^-3)+CE*3q²/32.
O total pela regra de Leibniz é8R(z^-3)+CE*3q²/8, como exige Delta R(z^-2).
Derivação curta: Dbal(fg)=0 e Dbal²(fg)=-2z^-3; logo
R_bal((Delta f)g)=Delta R(z^-2)/4-2R(z^-3)=CE*3q²/32.

A família de alocação anterior tinha Euler1=tau q²/8 e Euler2=(1-tau)q²/8.
Igualar o primeiro requer tau=3/4; igualar o segundo requer tau=1/4.
Não existe tau único que reproduza esta normalização simétrica. Assim,
o teste anterior de não pertencimento ao span de dois kernels Euler não
excluía todas as normalizações diferenciais: R_bal está fora daquela família.
Não se está apagando o teste anterior; seu domínio fica identificado.

A identidade verificada para todas as entradas da tabela com ordem até3 é
 DeltaR_(u+i,v)+DeltaR_(u,v+i)-q_i DeltaR_(u,v)
 =-C_i((D^u f)(D^v g)). Ela expressa derivar a inserção total antes/depois
da extensão. Testamos também troca das linhas e controles de Laplaciano.
1162 controles exatos, CPU 3.546875s, rc0.

Próximo: transportar as contrações tensoriais para R_bal e conferir as
condições restantes de uma única família T2, inclusive curvatura, graus
Grassmann e inserções lineares. Só a normalização diferencial escalar foi
construída aqui; não é Q2 nem uma prova completa de causalidade/realidade.
Não adotamos tau, não movemos gate e não alteramos fonte canônica.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
