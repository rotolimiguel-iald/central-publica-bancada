[DERIVED — tadpole finito da referência constante; contração de gauge nula]

## Contração nova e unidades

Usa-se o vértice quártico Einstein–Hilbert já derivado, com saída
V4raw=32kappa V4, g=delta+h, Fourier exp(+ip.x). Para o jato suave
constante, as duas pernas internas não têm derivadas:

    T_W(A,B;p)=1/16 sum_ab W_ab V4raw(A,p;B,-p;Ea,0;Eb,0).

Os coeficientes W_ab são covariâncias dos dez componentes independentes;
o fator1/2 das componentes fora da diagonal está contido no W_I. Não
se acrescenta outra divisão por4!: V4raw já é o vértice polarizado.
Para GH=(4kappa)/(4pi²)(S0/z+W), a Hessiana física deste tadpole é
hbar*T_W/(4pi²), pois (1/2)*(4kappa)/(32kappa)=1/16.

Na base [p²trAB,p²trA trB,(pAp)trB+(pBp)trA,pABp]:

    W_I: (5/2,-5/2,5/2,-5);
    W_T: (1,-1,1,-2).

Comparação com as unidades antigas CE/(4pi²)^2, CE=-4pi²:
o quociente dos prefatores é -1 e a troca do símbolo Fourier p pelo
símbolo diferencial real q acrescenta outro -1 na ordem2. Assim os
coeficientes acima entram com sinal positivo nessas unidades. Ainda
assim sua contração com Gc é zero: as duas Hessianas são múltiplos do
operador Einstein livre. Os resíduos anteriores da bolha+fonte ficam
inalterados, respectivamente (-1/8,15/8,1/2) e (5/4,1/4,-1).

Foram490 verificações exatas, incluindo os55 pares de fibras externas,
momentos fora do eixo e confronto com o vértice completo de quatro
pernas. CPU1.078125s, rc0. Não foi escolhido se T1 inclui ou subtrai
essa contração: ela é entregue explicitamente para a contabilidade
da ordenação/transporte, sem mudar a prescrição.

## A nulidade não exige isotropia

Para toda métrica constante não degenerada M próxima de delta, o
fundo é plano e on-shell no recorte K=Lambda=0. A Hessiana de EH
obedece H_M Gv=0, onde (Gv)_ab=p_a v_b+p_b v_a. A imagem de gauge
pode ser escrita nessa mesma forma para todo M: escolher o parâmetro
vetorial epsilon=M^-1 v dá Lie_epsilon M=Gv, com v mantido fixo.

Derivando duas vezes em M, nas direções constantes Ea,Eb, obtém-se

    V4(A,p;Gv,-p;Ea,0;Eb,0)=0.

Consequentemente T_W G=0 para qualquer fibra constante W, inclusive
anisotrópica. Isso decorre da degenerescência de gauge da Hessiana em
toda a família plana constante, e não de extrapolar três momentos.
É uma identidade do vértice EH, módulo divergências e com cutoff
constante. Não vale automaticamente com jatos variáveis ou curvatura.

O controle geral contrai a identidade quártico/cúbico anterior com
todas as55 fibras simétricas de W. A soma dos transportes das duas
pernas internas é igualmente nula.331verificações, CPU0.21875s, rc0.

A primeira execução esperava um controle anisotrópico não nulo e
falhou ao encontrá-los todos nulos. A hipótese foi corrigida, não os
vértices: o scriptv1 e seu plano permanecem. A versãov2 exige ambas
as nulidades e a identidade entre a expressão cúbica e quártica.

## O que resta

Este resultado retira o tadpole derivativo de jato zero constante
como candidato a cancelar o resíduo hc plano. Não apaga o tadpole da
Hessiana, que é não nulo; sua contração de gauge é que se anula.
Continuam separados os jatos de W com derivadas, curvatura, contatos
do cutoff, outras aridades e normalização lorentziana. Não houve
seleção de estado nem cálculo da Q2 integral. Kernel e gate intactos.
