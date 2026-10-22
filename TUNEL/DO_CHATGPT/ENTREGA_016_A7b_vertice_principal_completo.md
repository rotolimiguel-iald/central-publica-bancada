[DERIVED — decomposição do vértice principal h*hc; REAL — álgebra racional/CAS; OPEN — Q2 causal finita]
# A7.b — a derivada do ghost completa o vértice principal

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T00:20:50.589462+00:00.

Calculamos400 componentes de R1(H,p;r,v)=G-M/4 como polinômios exatos
em p=a e0,r=b e0+c e1:10H×10T×4v. O fator comum retirado é4iκA0,
A0=1/(8π²). O motor reutiliza o vértice cúbico EH, homogêneo de grau2,
e a extração do log UV previamente auditada. Cinco comparações cúbicas e
quinze comparações com o motor Sympy direto passaram;400 limites de ghost
constante coincidiram com a rodada anterior e todos os termos têm grau3.

A candidata anterior deixou116 componentes com resíduo. Apenas acrescentar
uma mudança quadrática simétrica de métrica A2, em57 contrações O(4), deu
posto33 contra34 no sistema aumentado. Permitir também as21 componentes
DeltaZ, mantendo bracket e os seis coeficientes constantes, deu48 contra49.
Esses negativos são preservados; não são provas de obstrução BV geral.

O termo que faltava nesse ansatz é permitido pela álgebra graduada:

    D1(E;r,v)=1/2 [ sym(r,Ev)-sym(v,Er) ],
    sym(x,y)=(xy^T+yx^T)/2.

Ele é antissimétrico na contração das fibras:
<T,D1(E)>=-<E,D1(T)>, e some para r=0. O segundo termo testado,
D2=[sym(v,r)trE-I(v·Er)]/2, tem a mesma propriedade. As800 identidades
de antissimetria foram verificadas em base. Para uma matriz de fibras
antissimétrica C e um jato ímpar d de ghost,

    delta[ (1/2) u_A C_AB d u_B ] = u_A C_AB d E_B,
    delta u=E, delta d=delta E=0.

Isso segue diretamente da regra graduada; um teste exterior de três fibras
conferiu identidade, nilpotência e graus. Usar derivada não graduada falha.
Logo D1 pode vir de um gerador local quadrático em antifields com derivada
do ghost; não é um tensor livre acrescentado sem primitiva.

O sistema completo,656 equações escalares em80 coeficientes, tem posto49
igual ao aumentado. Uma solução (parâmetros livres zero) tem DeltaZ=0,
coeficiente de D1=-1/3 e de D2=0. A2, com seus57 coeficientes, está listado
integralmente em bv_gradient_fit/results.json; cada base é simetrizada sob
(H,p)<->(J,r), como define quadratic_metric_engine.py. O resultado exato é

    R1 = Lie_(F_r v) H - K_(p+r) Z_new(H,p;r,v)
         -2 A2(H,p;K_r v,r)
         + [(p+r/2)·v] B(E_pH) - (1/3)D1(E_pH;r,v),
    F_rv=-3r²v/8+r(r·v)/4, B(E)=-E/6-I trE/12.

Z_new é o representante já fixado que conserva o bracket. O sistema
conferiu400 componentes R1,64 do bracket e6 condições constantes:470
identidades polinomiais, sem modificar nenhum coeficiente dos laços.
Por covariância O(4), dois momentos Euclidianos arbitrários podem ser postos
nesse plano; degenerações seguem por continuidade polinomial. Isso fornece
uma identidade tensorial principal, não uma escolha de prescrição causal.

Após congelar os coeficientes, três novos casos com momentos fora do plano
foram computados DIRETAMENTE pelo motor Sympy de laços:25/6,43/6,-245/3,
todos iguais à fórmula. As contribuições D1 nesses casos foram3,3,-6;
retirá-las ou inverter seu sinal falha (seis controles). Há ainda um controle
graduado negativo, totalizando sete. Essas verificações não são independentes
de todas as convenções de vértices; o motor-base já tinha auditoria própria.

Com u=4κ(h*+C*barc), a parcela nova de gerador é -A0/6 integral u D1(∂c)u;
seu diferencial livre produz a parcela calculada, além dos termos de antighost
do deslocamento, que não podem ser descartados. Restam a involução/realidade,
os demais componentes de s1F, os contatos de cutoff, curvatura e partes
finitas da anomalia. A identidade acima não prova QME completa, não atualiza
kernel nem gate. Não houve Lean nesta rodada. Cinco execuções rc0;
CPU total44.625s, parede45.022425599978305s; zero novas chamadas externas nesta medição.
