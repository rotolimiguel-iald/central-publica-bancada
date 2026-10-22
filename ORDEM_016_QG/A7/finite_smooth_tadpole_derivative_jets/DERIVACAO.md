[DERIVED — contribuição finita com jatos derivados; identidade de Ward do vértice]

## Objeto e decomposição completa deste vértice

Mantidos o vértice EH GammaGamma existente, K=Lambda=0, Fourier exp(+ip.x),
g=delta+h e cutoff constante, módulo divergências. A referência W é suave
formal; não se afirma que seja positiva, bissolução ou estado físico.
O recorte é um tadpole métrico de UM vértice quártico, não a bolha de dois
vértices nem a soma Q2. Nenhuma normalização T1 foi escolhida aqui.

Defina C(U,V;D A,D B) como a soma das duas ordens de
second_coefficient_4(U,V,gamma2(A),gamma2(B)). D denota a derivada na perna
indicada; em Fourier, gamma2 retira i/2. Para quatro pernas A,B,U,V,
a soma V4raw/16 tem exatamente os três grupos:

    T0 = C(U,V;D A,D B)/16;
    T1 = [C(A,U;D B,D V)+C(A,V;D B,D U)
         +C(B,U;D A,D V)+C(B,V;D A,D U)]/16;
    T2 = C(A,B;D U,D V)/16.

São respectivamente zero, uma e duas derivadas nas pernas internas U,V.
Esta é uma partição das seis escolhas de pernas não diferenciadas do
vértice; cada escolha conserva as duas ordens dos gammas. Logo T=T0+T1+T2
é uma identidade do algoritmo, não uma aproximação ou ajuste de coeficiente.
As duas pernas internas são contraídas com

    W(X,Y)=[U(X) tensor V(Y)+V(X) tensor U(Y)]/2.

Por simetria do vértice a média dá o mesmo valor da contração U,V. Por
linearidade/polarização isso descreve os jatos simétricos gerais:
T0 usa W00; T1 usa W10 e W01; T2 usa W11. Antes de integrações por partes,
não há segunda derivada numa mesma perna. Isso não impede que W20/W02
apareçam ao derivar os coeficientes do operador resultante. Não se devem
tratar jatos de coincidência como constantes durante essa operação.

As unidades continuam as anteriores: Hessiana física = hbar*T/(4pi²)
para GH=4kappa(S0/z+W)/(4pi²). Não se divide por4! novamente. A troca para
derivadas reais retira o produto i² do vértice; deve ser feita conjuntamente
com as unidades CE/(4pi²)^2, CE=-4pi², e não só nos termos selecionados.

## Identidade derivada de Noether

Com parâmetro vetorial c fixo, a variação é delta_c h=Gc+Lie_c h,
onde Gc=Lie_c delta. Escreva S_n como a n-ésima derivada da ação em delta,
sem fator n! no próprio vértice. O coeficiente multilinear de grau três
em delta_c S=0 dá

    S4(A,Gc,U,V)+S3(Lie_c A,U,V)
      +S3(A,Lie_c U,V)+S3(A,U,Lie_c V)=0.

Isso segue diferenciando a identidade da ação; não é extrapolação dos
controles numéricos. Os termos com S3 vêm da parte linear Lie_c h da
transformação. Não é permitido omitir Lie_c A ao contratar U,V.
Na normalização dos motores, V4raw=32kappa*S4 e V3raw=16kappa*S3:

    T_W(A,Gc) = -[V3raw(Lie_c A,U,V)
                  +V3raw(A,Lie_c U,V)
                  +V3raw(A,U,Lie_c V)]/8.

Os dois últimos termos são o transporte de W nas suas duas entradas;
o primeiro é a contribuição cúbica contraída aplicada a Lie_c A. A soma
exprime a covariância do objeto completo neste recorte. Se W é mantido
fixo sob s0, esses transportes não desaparecem por uma regra verbal: a
contração T_W G pode ser não nula. A fórmula não identifica por decreto
as convenções W fixo e W transportado.

O controle usa p+k+r+s=0. Cada termo da Ward tem o mesmo fator i adicional
do gauge/Lie, retirado uniformemente. Para r=s=0 recupera-se T_W G=0.
Para referência variável isso deixa de valer em geral.

## Evidência exata e controle que pode falhar

Exemplo: A=e00, U=e00, V=e01+e10;
p=(1,2,-1,1), r=(0,1,0,0), s=(1,0,-1,0),
k=(-2,-3,2,-1), v=(2,-1,1,3).

    (T0,T1,T2)=(6,-21/2,-27/2), portanto T_W(A,Gc)=-18.
    (cúbico externo,cúbico interno1,cúbico interno2)=(5,10,3).
    -18+5+10+3=0.

Se as derivadas internas forem omitidas, sobra 6+5+10+3=24, não zero.
Portanto a identidade distingue o vértice completo da versão incompleta.
O runner passou716 verificações exatas:55pares de fibras x3controles,
identidade cúbica/quártica, simetrias e recuperação do limite constante.
A omissão produz resíduo não nulo em159controles. CPU1.046875s; rc0.
O programa não prova o caso universal por amostragem: a identidade acima
decorre de Noether e a decomposição decorre da polarização do vértice.

## Alcance na soma pendente

Este resultado fornece os termos internos derivados que faltavam ao
tadpole finito. Não prova que o tadpole cancele os contatos singulares
ou mistos da bolha, nem calcula as outras aridades da quebra. Para
contabilizá-lo em Q2 é necessário preservar a normalização T1 e seu
transporte de Wick, juntamente com os termos cúbicos e de fonte.
Cutoff variável exige correntes de fronteira que não foram calculadas
nesta unidade. Curvatura, normalização lorentziana e Q2 integral seguem
com os respectivos limites já registrados. Kernel e gate intactos.
