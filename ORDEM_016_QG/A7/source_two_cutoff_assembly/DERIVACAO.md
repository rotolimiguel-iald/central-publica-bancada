[DERIVED — fonte plana singular com dois cutoffs; não é a Ward completa]

# Extensão e localização nos dois extremos

Fixe a prescrição já usada R=FP_a[(1-a)mu^(2a)z^a], z=(X-Y)²,
em quatro dimensões euclidianas auxiliares. CE=-4pi² é a constante
escalar do resíduo. Para evitar confusão, escreva o defeito de operador
como mathcalC_D(f)=R(Df)-D R(f). R comuta com multiplicação suave.

## O tensor antes da redução do ghost externo

A fonte é A_ab,r c^r+B^j_ab,r partialY_j c^r. Sua redução fora da
diagonal é C=A-divY B, já calculada anteriormente. O tensor B foi
extraído diretamente dos mesmos propagadores e vértices, sem inferi-lo
apenas de sua divergência. Seus coeficientes na base seguinte são

    (-2,-4,-4,16,-8,20,0):

    delta_jr delta_ab/z3;
    (delta_ja delta_br+delta_jb delta_ar)/z3;
    delta_ab Xj Xr/z4;
    delta_jr Xa Xb/z4;
    (delta_ja Xb Xr+delta_jb Xa Xr)/z4;
    (delta_ar Xj Xb+delta_br Xj Xa)/z4;
    Xj Xa Xb Xr/z5.

No plano partialY=-partialX, e a contração explícita recupera exatamente

    C_ab,r=[-12delta_ab Xr-30(delta_ar Xb+delta_br Xa)]/z4
            +96Xa Xb Xr/z5.

Todos os componentes da reconstrução foram conferidos como identidades
racionais, e amostras axiais e não axiais foram confrontadas com os
jatos do motor bilocal original. A igualdade C não determina B sozinho;
foi usada como controle, não como definição de B.

## O contato da derivação em Y

A diferença mathcalC_divY(B)=R(divY B)-divY R(B) tem símbolo

    D_ab,r/CE=-(1/16)delta_ab q_r q²
              +(1/6)(delta_ar q_b+delta_br q_a)q².

q denota derivadas da delta na variável X-Y. Não é momento de Fourier
com fator i suprimido. A expressão foi extraída de duas maneiras:
pela tabela de contatos de primeira derivada aplicada a B, com a regra
de multiplicação X_i delta^nu, e pelo resíduo do termo do regulador

    2a Xj B^j/z
      =a[-12delta_ab Xr+32(delta_ar Xb+delta_br Xa)]/z4.

Esta última fórmula coincide com a extração antiga do estágio Y,
preservada em bilocal_Y_regulator/results.json. Não se mudou a extensão
para obter concordância. O log não está presente neste recorte K0.

## Dois cutoffs independentes

Sejam chiX(X),chiY(Y) suaves de suporte apropriado. Antes de aplicar E_X,
a integração por partes no ghost produz

    H=chiY C-(partialY_j chiY)B^j.

Não é chiY C sozinho. Compare os dois objetos precisamente tipados:

    P=E_X{chiX[chiY R(A)-divY(chiY R(B))]},
    Q=R{E_X[chiX H]}.

P primeiro estende o acoplamento e depois deriva a fonte localizada;
Q estende a expressão já diferenciada fora da diagonal. Pela definição
de D, pela regra do produto e por R(chi f)=chi R(f),

    chiY R(A)-divY(chiY R(B))=R(H)+chiY D.

Consequentemente, a identidade completa deste objeto é

    P-Q=-mathcalC_E(chiX H)+E_X[chiX chiY D].

O sinal negativo da primeira parcela é fixado pela definição de
mathcalC_E. A segunda inclui a diferenciação do contato de Y; descartá-la
ou interpretar a adjunção como uma fonte adicional de contato dá outro
objeto. Aqui E é o Einstein linearizado plano físico, não o operador
mínimo obtido por fixação de gauge.

A primeira parcela admite a decomposição de Leibniz já demonstrada:
mathcalC_E(chiX H)=chiX mathcalC_E(H)+termos com partial chiX e
mathcalC_partial(H). Não há termo novo independente com partial²chiX
nesse comutador, mas E_X[chiX chiY D] possui tais derivadas, e os
produtos chiX delta^nu continuam contendo todos os jatos até |nu|.

## Verificação preservando os produtos distribucionais

Foi usado chiX=exp(lambda X0) como gerador de jatos locais, realizável
até a ordem necessária por função compacta igual a ele perto da origem.
No símbolo de delta sua multiplicação é q0->q0-lambda. Essa regra
implementa os jatos do cutoff; substituir apenas por chiX(0)=1 não serve.
O cálculo compara o regulador bilocal diferenciado diretamente com
a soma de contatos acima. Não impõe que a soma seja zero.

Para r=0, componente ab=11, q=(2,1,0,0), lambda=1, os valores de
(P-Q)/CE são:

    gradY chiY=0:  -29/32;
    gradY chiY=e0: -17/120;
    gradY chiY=e1: -79/160,

com chiY(0)=1. Omitir a derivada em Y perde, respectivamente, 367/480
ou 33/80 nesses dois controles. A escolha q=e0,lambda=1 registrada no
runner principal dava zero para esses componentes; ela é um controle
degenerado do deslocamento q0-lambda e não foi usada como prova de
cancelamento. O controle adicional não degenerado fica no recibo.

## Alcance e evidência

Extração B e contatos do novo termo de Y:370 controles, CPU3.734375s,
rc0 (v2). A primeira tentativa falhou depois da extração de B por falta
de product no namespace que importava funções puras por AST; log e
checkpoint preservados. Nenhum motor científico foi alterado.

Montagem P-Q e contato D:240 controles, CPU11.875s, rc0. O argumento
geral é a identidade distribucional escrita; as amostras verificam
implementação e sinais, não substituem esse argumento.

Isso resolve a localização da fonte singular plana no comparador Q
explicitamente escolhido. Ainda faltam a montagem dos laços métricos
e ghost com cutoffs e fronteira EH, a primeira curvatura correspondente,
as outras aridades e a extensão causal completa. Não trocar esse
comparador pela Q2 integral. Kernel, gate e originais preservados.
