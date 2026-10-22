[DERIVED — parcelas tensoriais do laço; REAL — CAS exato; OPEN — soma curva]
# A7.b — inserções do endomorfismo e transporte tensorial
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T03:51:48.822718+00:00.

**Nova parcela da bolha.** Conservados os vértices métricos, a inversa de
Gram, I_tr e a contração transposta de Wick. Expandiu-se somente a parte
de endomorfismo dos propagadores; não se trocou o feixe por dez escalares.
Para D=q²-E, E=K(-2P_TL+6P_tr),

    D^-1=I/q²+E/q4+E²/q6+… .

Na mesma base bilinear [p²trAB,p²trA trB,pAp trB+pBp trA,pABp],
a bolha com dois vértices principais e UMA inserção de E dá

    K[-14/3, 3, -1, 8/3].

Na base [trAB,trA trB], a mesma bolha com DUAS inserções (na mesma
linha ou uma em cada linha) dá K²[34/3,41/3]. Um vértice de potencial
e um principal, com UMA inserção de E e todas as posições somadas,
dão K²[96,-24]. São coeficientes brutos/A0; o fator -1/2 da Hessiana
efetiva ainda não foi aplicado a estas tabelas.

São parcelas diferentes das bolhas de potencial já entregues. Os179
checks verificam os55 pares bilineares em cada parcela e a expansão
dos vértices fora dos nós. Um controle independente usa os denominadores
exatos q²+2K e q²-6K com os projetores tensoriais e o extrator radial,
sem inserções explícitas: os coeficientes deK eK² coincidem. Apagar cada
nova parcela produz um resíduo não nulo. rc0, CPU8.546875s.

**Dados geométricos para a parcela restante.** Em quadro ortonormal por
transporte radial, retire o fator4kappa/(4pi²) de GH; z=x²,L=log(mu²z),
S=I_tr Gram^-1, V=g g^t/2 e A_i=x^j Omega_ji/2 (Omega com K retirado).
Os jatos de ordemK, nas duas pontas X eY=0, são

    H1=S/4+V L,
    (nabla_Xi H)1=A_i S/z+2x_i V/z,
    (nabla_Yj H)1=A_j S/z-2x_j V/z,
    (nabla_Xi nabla_Yj H)1=
      (z delta_ij-x_i x_j)S/(3z²)+Omega_ij S/(2z)
      -2x_i A_j S/z²+2x_j A_i S/z²
      +V(-2delta_ij/z+4x_i x_j/z²).

Essas são matrizes de10 componentes; A eOmega agem na fibra inteira.
Os2500 componentes foram comparados com o parametrix em coordenadas
normais, convertendo as duas pernas tensoriais e o índice de derivada
com o coframe e incluindo Christoffel. Não se apagou a derivada transversal
do transporte. rc0, CPU2.90625s. A v1 da verificação esqueceu
impor z=sum x_i² e falhou; preservada. A v2 corrige apenas essa relação.

**Integração angular preparada:** cubatura racional em128 direções com
pesos assinados, conferida para TODOS os495 monômios de grau até8 em S³.
São pesos de quadratura, não probabilidades. Não integra funções arbitrárias;
a cota de grau do integrando deve ser verificada antes do uso no laço.
rc0, CPU0.046875s; nenhum laço foi inferido dessa preparação.

**Alcance:** o transporte e seus jatos estão conferidos, mas ainda precisam
ser contraídos com os dois vértices e o volume. Eles não podem ser somados
como se fossem os coeficientes de E acima: as decomposições sobrepõem-se.
A soma da bolha métrica curva, sua conversão covariante e sua combinação
com ghost/fonte BV continuam abertas. Q2 finita causal não foi calculada.
Nenhum original, kernel ou gate alterado.
