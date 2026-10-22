[DERIVED — auditoria parcial de parecer; nenhuma alteração dos motores]

# Frame, conexão e normalização

O parecer c76366aa derivou corretamente, em RNC euclidianas 4D,

    f_a^b(Y)=(Y² delta_ab-Y_a Y_b)/6,
    frame2(i,j,a,b)=(2 delta_ij delta_ab-delta_ai delta_bj-delta_aj delta_bi)/6.

As primeiras derivadas de f anulam em Y=0. Isso simplifica a regra do
produto dos componentes convertidos para frame. Não elimina a conexão
de Levi-Civita dos jatos covariantes. São duas operações distintas.

## Um controle que separa as operações

Tome V com componentes constantes no frame radial, V^a=delta^a_b.
Em coordenadas, V^mu=e_b^mu=delta_b^mu+K f_b^mu. A primeira derivada
covariante anula na origem. Na segunda, ao coeficiente de K:

    (nabla_i nabla_j V)^a(0)
      = frame2(i,j,a,b) + partial_i Gamma1^a_jb(0)
      = (delta_ai delta_jb-delta_aj delta_ib)/2,

com a convenção do motor

    Gamma1^a_jb=-(delta_ab Y_j+delta_aj Y_b-2 delta_jb Y_a)/3.

Para i=0,j=1,a=0,b=1, as parcelas são -1/6 e +2/3. Sua soma
é +1/2; trocando i,j, a soma é -1/2. O comutador vale 1.
As derivadas parciais do frame, simétricas em i,j, não produzem sozinhas
esse comutador de curvatura. Portanto, a conclusão de completude baseada
apenas em frame2 é incorreta, mesmo com Gamma(0)=0.

O código recebido não tem a omissão sugerida pelo parecer:
bilocal_covariant_jet_engine inclui conexão nos jatos internos, e os
dois motores do par incluem explicitamente

    +(8/3) v1/m - (2/3) v2

na etapa de Ward em Y. Não retirar esses termos nem adicionar novamente
o operador coordenado inteiro. Uma comparação entre métodos exige
contabilizar todas as parcelas, não a regra genérica de que frame e
conexão seriam alternativas. A auditoria antiga da divergência em X
permanece em bilocal_frame_divergence_audit; não foi repetida aqui.

## Duas correções de leitura da fonte

tensor(a,b) usa OR booleano, não soma de deltas: na diagonal o valor é 1,
fora dela são duas entradas 1. Assim ||tensor(a,b)||²=1 ou 2, exatamente
multiplicity(a,b). O parecer descreveu valor diagonal 2 e norma² 4.
A implementação não deve ser alterada para acomodar essa descrição.

frob(empty,empty) devolve int(0), exato. A preocupação do parecer com
float(0.0) não se aplica a essa soma; não há motivo para uma mudança
cosmética para Fraction que pretenda corrigir perda de exatidão ausente.

## Evidência e alcance

1116 igualdades/controles exatos, CPU 0.046875 s, rc 0. As 256 escolhas
de i,j,a,b conferem frame2, a conexão e o comutador; 36 componentes
da derivada da conexão são não nulas. Também conferidas as primeiras
derivadas, multiplicidades, soma vazia e presença dos termos na fonte.

A derivação de frame2 e os sinais de conversão são aproveitáveis.
O parecer é parcial e não certifica a Ward completa, a extensão causal
ou Q2. Nenhum original, kernel ou gate foi alterado. O recibo conserva
dois custos divergentes, ainda sujeitos a reconciliação administrativa;
não se escolheu silenciosamente um deles como custo definitivo.
