[DERIVED — composição localizada do tadpole EH; referência suave formal]

# Os jatos W20 e W02 da divergência EH

Escopo: 4D euclidiano auxiliar, K=Lambda=0, g=delta+h, Fourier exp(+ipx).
W=(U(X) tensor V(Y)+V(X) tensor U(Y))/2 é uma referência suave formal,
sem afirmação de positividade ou de estado físico. A conta é de um
vértice quártico; não é a extensão do produto singular de dois vértices.

Mantêm-se V4raw=32kappa*S4 e a Hessiana contraída T=V4raw/16.
A contribuição física é hbar*T/(4pi²) na normalização já registrada
do propagador. Não acrescentar outro 4! nem outra simetrização de W.

## Fórmula por posições de derivadas

O corrente B^mu=sqrt(g)(g^ab Gamma^mu_ab-g^mu,a Gamma^b_ab) contém
uma derivada. Seu coeficiente polarizado de quarta ordem, com o fator i
retirado, é linear nos quatro momentos:

    b4(A_p,B_q,U_r,V_s)=b_A(p)+b_B(q)+b_U(r)+b_V(s).

Cada parcela é obtida pondo os outros três momentos em zero no motor
existente. Ponha P=p+q e b_E=b_A+b_B. A ação usa

    sqrt(g)R=C_GammaGamma+partial_mu B^mu,
    S_chi=-integral chi sqrt(g)R/(2kappa).

Logo a parcela de fronteira na Hessiana normalizada é exatamente

    T_boundary=(P+r+s).(b_E+b_U+b_V).

Sob r->a r e s->b s, os seis coeficientes são

    a0 b0 : P.b_E,
    a1 b0 : P.b_U+r.b_E,
    a0 b1 : P.b_V+s.b_E,
    a2 b0 : r.b_U,
    a1 b1 : r.b_V+s.b_U,
    a0 b2 : s.b_V.

Essa fórmula decorre da linearidade de B em uma derivada e da divergência
externa; não depende de ajuste a uma tabela numérica. Os termos a² e b²
representam derivadas de segunda ordem na mesma perna interna, isto é,
W20 e W02 antes de integrar a divergência por partes. A conversão de
momentos para derivadas reais deve preservar os dois fatores i.

Isso complementa, sem contradizer, a partição anterior T0/T1/T2 de
GammaGamma: naquela densidade cada uma das duas derivadas incide em
pernas diferentes. A densidade EH completa inclui também a divergência.
Não transportar a ausência de W20/W02 de uma densidade à outra.

## A mesma ação com o cutoff explícito

Para suporte apropriado,

    S_boundary=+integral (partial_mu chi) B^mu/(2kappa).

O momento de chi é ell=-(P+r+s). Os dois fatores i dão
-ell.b4=(P+r+s).b4, exatamente a mesma contribuição normalizada.
Nesta representação resta uma derivada nas pernas do corrente e uma
derivada no cutoff. Os jatos W20/W02 da densidade anterior foram
reorganizados por integração por partes; não foram declarados zero.

Se Q=P+r+s=0, a contribuição da divergência é zero, como deve ocorrer
na ação com cutoff constante e condições de contorno adequadas. Isso
não permite pôr Q=0 antes de extrair uma identidade localizada.

## Controle explícito e rastreabilidade

Para A=e00, B=e11, U=V=e00 e
p=(1,2,-1,1), q=(2,-1,0,3), r=(0,1,1,0), s=(-1,0,2,1),
os seis coeficientes na ordem acima são

    45/8, 15/8, -21/4, 0, -3/2, -15/8.

Sua soma é -9/8. Omitir a corrente perde esse termo; o coeficiente
W02 é não nulo (-15/8). Foram testadas 55 fibras internas simétricas
em dois pares externos: 48 têm algum termo de segunda derivada numa
mesma perna. A interpolação independente das potências confirma a
partição, incluindo limites Q=0 e a forma com derivada de chi.

Versão exata v2: 1321 controles, CPU 5.484375 s, rc0. A primeira
execução passou, mas uma divisão de inteiros gerou floats. Seus arquivos
e log foram preservados; v2 força Fraction e recusa floats em cada
igualdade. A evidência de aritmética racional é exclusivamente v2.

O que fica pago neste recorte é a composição dos jatos suaves com a
corrente de fronteira do vértice. A igualdade com a quebra completa dos
produtos temporais, a extensão causal e a contribuição não linear A2
não decorrem disso. Q2 integral permanece OPEN. Kernel e gate intactos.
