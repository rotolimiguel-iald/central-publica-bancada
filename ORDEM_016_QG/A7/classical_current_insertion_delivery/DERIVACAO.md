[DERIVED — inserção métrica da corrente e fluxo localizado de gauge; Q2 OPEN]

## Corrente métrica como vértice

J_BV(h,h,c) previamente construído é homogêneo de grau2 nos12 marcadores
de derivada (p,q,k): V2 tem grau2, Lie grau1 e a corrente de Green grau1.
Portanto a polarização quadrática recupera exatamente seus78 monômios,
sem truncar uma série nem ajustar uma aproximação. Obtida a realização
para c0 e todos55 pares simétricos de fibras, com a troca para100 pares.
990 comparações conferem dois pontos não axiais, corrente, divergência e
troca das pernas. Há276 monômios de segunda derivada interna e159 de
segunda derivada no ghost externo. Um vértice apenas de primeiras
derivadas por perna perderia essas contribuições.

## Primeira inserção realmente contraída

O vértice -partial_mu chiY J_BV^mu foi contraído com o vértice EH cúbico
completo localizado em X. Conservaram-se os jatos internos de ordem2 e
os jatos externos do ghost; adjunção em Y usa produtos de(d_i-eta_i),
e em X -(d_i+lambda_i) para a perna derivada. A extensão usa o mesmo
R=FP[(1-a)mu^(2a)z^a], C_D=RD-DR e q->q-lambda na diagonal.
350 verificações comparam o kernel simbólico com contrações racionais
no ponto(1,2,-1,1), incluindo suas derivadas. Essa comparação audita a
implementação; não afirma independência dos vértices de entrada.

Normalização explícita: /16 por par métrico, SEM fator de simetria do
diagrama. Para h11,c0 e q=(2,1,0,0), normalizado por CE=-4pi²:
* lambda=0,eta=e0: fora diagonal -12104/117649; contato -63841/3840.
* lambda=e0-e1,eta=e0: fora diagonal -175792/117649; contato131279/3840.
Não somar esses números à Ward com fator ajustado pelo resultado. A
montagem deve derivar os pesos e incluir as outras correntes abaixo.

Falha v1 preservada: 0/16 do Python introduziu float nos termos nulos.
No primeiro comparador que falhou,716/16807 virou0.04260129707859826,
diferença-6.24500451351651e-17. v2 usa Rational/Fraction explicitamente,
sem tolerância ou alteração de física. Logs/diagnóstico/predecessores
permanecem no manifesto. Não se chama a v1 de aritmética exata.

## Correção de convenção ao lado e correntes que faltam

BV069 §3,eq7, fixa s0barc=-b, não +b. O parágrafo ghost em
localized_brst_flux/DERIVACAO.md usou +b; fica CORRIGIDO AO LADO.
Nenhum código do cálculo métrico utilizou esse sinal, mas a montagem
ghost deve seguir a fonte. Para Igh=integral chi barc divZ:
sIgh=integral chi[-b divZ-barc div(sZ)]
    =integral(chi db+dchi b)Z+(chi dbarc+dchi barc)sZ.
Não misturar essa convenção com antighost hermitiano/fator i alternativo.

Ponha Z=L_c h, w=c.partial c. A identidade graduada é s0Z=-G w.
Para as transformações localizadas s1chi h=chi Z, s1chi c=chi w,
mantendo S0 sem cutoff e Vghostchi=integral chi barc C Z:
s0Vghostchi+s1chi S0gf
 = integral b[C,chi]Z-barc[Q,chi]w, Q=CG.
No plano, C é divergência com reversão de traço, Q=box em notação de
derivada real (seu símbolo Fourier tem o i² separado):
[C,chi]Z_nu=(d_mu chi)(Z_mu,nu-delta_mu,nu trZ/2),
[Q,chi]w=(box chi)w+2(d_mu chi)d_mu w.
Integrando por partes o termo box chi, a corrente é
J_gf^mu=b_nu Zbar_mu,nu+(d_mu barc_nu)w^nu-barc_nu d_mu w^nu,
com contribuição +integral dchi.J_gf. A fonte métrica tem contribuição
-integral dchi.J_BV na convenção da seção anterior. Isso ainda não é o
colchete completo nos setores com antifields externos.

27 verificações CAS incluem a identidade s0Z=-Gw com momentos e
polarizações SIMBÓLICOS arbitrários de duas ondas Grassmann ímpares,
os comutadores em campos/cutoff polinomiais e a divergência exata entre
as duas formas de J_gf. Controles não nulos:[C,chi]Z=(568,207,-121,988)
e -barc[Q,chi]w=-488 num ponto declarado. O sinal+ b incorreto já deixa
variação40 na ação livre de um controle; o sinal-b a cancela.

Consequência: b não propaga como um laço independente, mas o termo b h c
da corrente pode contrair pela entrada mista b-h. Também há a corrente
barc c c no diagrama ghost. Faltam essas inserções quânticas e seus pesos,
curvatura, partes suaves/tadpoles, aridades superiores e causalidade.
A soma de fonte+pares anterior nunca foi declarada Q2 e não recebe esse
estatuto agora. Nada mudou em um.py, kernel, horizonte, Atlas ou gate.
