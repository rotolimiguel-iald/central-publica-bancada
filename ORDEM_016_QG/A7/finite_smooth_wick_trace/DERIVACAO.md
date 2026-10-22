[DERIVED — transporte de Wick da ação métrica e contribuição com cutoff]

## Transportar a representação inteira

Para um núcleo suave bosônico W, defina D_W=(1/2)<W,delta²/dh²> e
alpha_W=exp(hbar D_W). Na convenção de transporte já conferida nesta bancada,

    T_n^W = alpha_W T_n (alpha_W^(-1) tensor ... tensor alpha_W^(-1)).

Em particular, SE T_1=id na representação de partida, então T_1^W=id.
O transporte não acrescenta por si um tadpole independente a T_1. Entretanto,
a MESMA interação abstrata é representada por S^W=alpha_W S, logo

    S^W = S + hbar D_W S + O(hbar²).

Manter a expressão S em ambas as representações e ao mesmo tempo acrescentar
a contração D_W S é outra operação. Para evitar dupla contagem, é necessário
indicar qual expressão representa a interação e qual mapa T se está usando.
Este enunciado transporta qualquer normalização existente: não escolhe uma
nova normalização causal, nem resolve as extensões multidiagonais pendentes.

## O operador de simetria também atravessa

No setor métrico, com W independente do campo h, tome
s h=G c+L_c h. Em coordenadas de campo, R^i=G^i+L^i_j h^j e
s=R^i partial_i, acrescentando a ação apropriada nos ghosts quando aplicável.
Como R é afim em h,

    [D_W,s]F = W^{ab} L^i_a partial_b partial_i F
             = D_(L W + W L^T) F.

O termo (1/2)W^{ab}(partial_a partial_b R^i)partial_i F é zero.
No domínio funcional, L atua nas duas entradas do núcleo: L_c^X W+L_c^Y W.
Derivadas e adjuntos são interpretados com os suportes do funcional; isso
inclui as derivadas de W, não apenas a ação matricial pontual. Aqui sW=0,
isto é, W é a referência fixa da representação inicial. Dar a W uma
transformação adicional altera esta contabilidade e deve ser dito.

Como os coeficientes de L W+W L^T não dependem de h, o próximo comutador
com D_W se anula. Assim, no recorte métrico afim,

    s^W = alpha_W s alpha_W^(-1)
        = s + hbar D_(L_c^X W+L_c^Y W).

O novo termo é de segunda ordem funcional: não é uma simples transformação
clássica de campo sob o produto ordinário. O produto também foi transportado.
Se sS=0, então s^W S^W=alpha_W(sS)=0. Na ordem hbar, isso dá

    s(D_W S) + [D_W,s]S = 0.

Esta é uma identidade de conjugação, não um cálculo da anomalia quântica.
No grau hc ela reproduz a Ward encontrada no tadpole: o quártico contraído,
o cúbico contraído avaliado em Lie_c h e o transporte das duas pernas de W.
Não se pode apagar os dois últimos e exigir que o primeiro se anule sozinho.
Se sS tem um termo de fronteira de cutoff, a mesma conjugação transporta
esse termo; não se escreve zero no seu lugar.

## Contração independente da ação existente

Na família h=u delta em4D, o resultado métrico já derivado é

    V_chi = 3chi/(4kappa) * u/(1+u) * (du)^2.

Não se substitui a gravidade por um campo escalar: é a restrição da mesma
ação à direção de traço. Seus termos cúbico e quártico são
V3=3u(du)^2/(4kappa), V4=-3u²(du)^2/(4kappa).
Para o jato suave do coeficiente u, escreva

    W00=a, W0i=b_i, Wij=c_ij, c=tr(c_ij).

A derivação funcional direta dá

    D_W V3 = 3/(4kappa) [2b.du+c u];
    D_W V4 = -3/(4kappa) [a(du)^2+4u b.du+c u²].

Essas contrações retêm os três grupos de derivadas internas da entrega
anterior. Com o prefator de propagador 4kappa/(4pi²), multiplicam-se por
hbar*4kappa/(4pi²). O fator1/2 da contração já está em D_W.

A Hessiana de D_W V4 nas direções f,g é

    -3/(4kappa) [2a df.dg +4b.(f dg+g df)+2c f g].

Para W=[exp(irX)exp(isY)+exp(isX)exp(irY)]/2, tem-se
a=1, b=i(r+s)/2, c=-r.s no ponto de ancoragem. A Hessiana em ondas planas,
após multiplicação por4kappa, é 6sum_(i<j) p_i.p_j. O vértice tensorial
independente V4raw/16 dá a mesma expressão; três controles resultaram
-84,6,-6. Os sinais Fourier são mantidos uniformemente.

## O cutoff que a conta deve conservar

Retire apenas o prefator comum e escreva a densidade

    F=chi[a(du)^2+4u b.du+c u²].

Sua derivada de Euler exata é

    delta F/delta u = -2div(chi a du)-4u div(chi b)+2chi c u.

O defeito de substituir essa expressão por chi vezes o operador com
cutoff constante é

    -2 dchi.(a du+2bu).

No controle chi=1+x0, a=1+x0, u=x0², b=(1/2,0,0,0), o defeito é
-6x0²-4x0. A simetria de um W suave implica b=da/2 na diagonal; ela NÃO
fixa c, que contém o jato misto. Sob essa relação,

    delta F/delta u = -2div(chi a du)-2u div(chi da)+2chi c u.

O CAS verifica a expressão em quatro coordenadas e coeficientes suaves
simbólicos, além da contração funcional e da comparação tensorial.
São14 verificações, CPU0.265625s, rc0. Os testes de conjugação bosônica e
da Ward quártica anteriores foram reutilizados, sem rerodar nem somar
suas contagens como novas. Esta rodada não testa a graduação ghost completa.

## Alcance e dado ainda necessário

A conta resolve a contabilidade do transporte neste setor: tadpole,
cúbico contraído e simetria transportada pertencem à mesma transformação.
A referência fixa não permite descartá-los seletivamente. O confronto
com uma Q2 calculada exige explicitar essa representação nos produtos
temporais, manter os termos de fronteira e completar as outras contribuições.
O resultado não escolhe estado físico, T1 novo, contratermo ou horizonte,
e não transfere esta verificação de traço para todas as polarizações com
cutoff variável. A prescrição completa/QME, o kernel e o gate não mudaram.
