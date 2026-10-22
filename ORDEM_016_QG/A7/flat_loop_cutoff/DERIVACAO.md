[DERIVED — localização plana de bolhas; completar vértices EH e extensão]

## Dados não reduzidos e localização

Para cada jato externo mu (0 para h, i para partial_Xi h), sejam F0^mu_ab
e F1^mu,j_ab as contrações com o vértice Y sem e com derivada externa.
Os fatores dos motores são conservados: métrica /16; ghost com transposta
do vértice Y; multiplicidade m_ab=1 diagonal e2 fora da diagonal.

W^mu(chiY)=sum_a 2/m_ab [-chiY partial_Ya F0^mu_ab
 -(partial_Ya chiY)F0^mu_ab
 +sum_j {chiY partial_Ya partial_Yj F1^mu,j_ab
 +(partial_Ya chiY)partial_Yj F1^mu,j_ab
 +(partial_Yj chiY)partial_Ya F1^mu,j_ab
 +(partial_Ya partial_Yj chiY)F1^mu,j_ab}].

O coeficiente final de h após adjunção X é
L=chiX W^0 - sum_i partial_Xi(chiX W^i).
No plano, os kernels não reduzidos dependem de X-Y:
partial_Xi F=-partial_Yi F. Isso vale para F, NÃO autoriza derivar
chiY em X. No motor extra_word aplica-se apenas ao kernel.
Daí L=chiX W^0 - (dchiX)_i W^i +chiX W^i[partial_Yi F].
A fórmula resulta da regra do produto e adjunção em testes compactos.
São necessários F0,F1 e seus jatos: os W^mu com chiY=1 não os determinam.

## Comparação com os dados já existentes

Novo motor calcula os propagadores planos e suas derivadas diretamente:
G_ghost=delta/z e G_metric=(delta_ac delta_bd+delta_ad delta_bc
-delta_ab delta_cd)/(2z). Mantém os vértices existentes.
Em X-Y=(1,2,-1,1), os80 valores para h11,h01, cinco jatos X,
quatro componentes de c e dois tipos de laço coincidem EXATAMENTE com
as bases C0/C1 da extração bilocal anterior. O ponto não é axial.
64 valores de localização têm aritmética racional exata;8 cancelamentos
no cutoff constante e2 controles de não cancelamento completam154.

Para h11,c0, a combinação ghost-metric/2 é:
chiX=chiY=1, gradientes nulos: 0;
dchiY=(1,0,0,0): 2344/117649;
dchiY=(1,0,0,0),dchiX=(1,-1,0,0): 9112/117649;
dchiY=0 e HessY=[[1,2,0,0],[2,-1,0,0],[0,0,0,0],[0,0,0,0]]:
360/16807. Em todos os casos os valores chiX=chiY=1 são locais;
esses jatos admitem realizações por funções suaves compactas.

Não se usa o cancelamento com cutoff constante como prova para cutoff
variável. Os termos adicionais são resultados, não erro numérico.

## Identidade de comparação da extensão (derivação, ainda sem soma numérica)

Defina C_D(f)=R(Df)-D R(f), R comutando com multiplicação suave.
Se W_R^mu usa os F estendidos antes das derivadas e W^mu é a expressão
fora da diagonal, então Delta^mu=W_R^mu-R(W^mu) é
sum_a 2/m_ab [chiY C_partialYa(F0^mu_ab)
 -sum_j {chiY C_partialYa partialYj(F1^mu,j_ab)
 +(partial_Ya chiY)C_partialYj(F1^mu,j_ab)
 +(partial_Yj chiY)C_partialYa(F1^mu,j_ab)}].
O termo HessY multiplica R(F1), portanto não cria um comutador adicional.
Para P=chiX W_R^0-partial_Xi(chiX W_R^i), e
Q=R[chiX W^0-partial_Xi(chiX W^i)], segue exatamente
P-Q=chiX Delta^0-partial_Xi(chiX Delta^i)
     +sum_i C_partialXi(chiX W^i).
Prova: substituir W_R=R(W)+Delta; a comutação de R com multiplicação
elimina os termos sem derivada, e os demais são a definição de C_partial.
Não se acrescenta contato à adjunção de distribuições já estendidas.
Multiplicar uma derivada de delta por chiX exige seus jatos completos.

## Limites e próximo passo

O vértice métrico usado aqui é GammaGamma. A corrente de divergência
EH foi derivada separadamente e NÃO foi somada a estas bolhas.
Também faltam os contatos da extensão das expressões localizadas,
curvatura, aridades superiores e a identificação causal. Não é Q2 completo
nem demonstração de cancelamento da anomalia. O próximo cálculo é
incorporar a corrente EH ao vértice localizado, conservando estes dados
não reduzidos, e só então montar a comparação de extensão acima.
Nenhum original, kernel ou gate foi alterado.
