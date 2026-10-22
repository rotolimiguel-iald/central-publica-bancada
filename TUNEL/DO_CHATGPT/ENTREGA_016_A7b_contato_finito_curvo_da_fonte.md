[DERIVED — extensão explícita de componente singular; REAL — CAS; OPEN — soma Ward completa]
# A7.b — contato finito curvo da bolha antifield–ghost
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T05:49:15.434491+00:00.

**Objeto efetivamente calculado:** os kernels A(T,v;x) e B(T,dv;x)
de curved_source_jet_engine na primeira ordemK, com os dois vértices
e bitensores já usados no log. Acrescentou-se ANTES da extensão o
transporte da densidade externa

    delta T=-z T/6-(xx^t T+T xx^t)/6.

Permanecem retirados os fatores globais dos propagadores,4kappa e
fases de Fourier. É a parcela singular geométrica, em cálculo
auxiliar euclidiano; não se afirma que os jatos suavesW sejam zero.

## A mesma prescrição, agora aplicada aos kernels
Conserva-se R=FP[(1-a)mu^(2a)z^a .], fixada antes destas contas.
Para escrever explicitamente R dos numeradores anisotrópicos,
decompusemos P(x)=sum z^j H_l(x), Delta_x H_l=0, e usamos

    H_l(partial)z^(a-b)
      =2^l product_(j=0)^(l-1)(a-b-j) H_l(x)z^(a-b-l).

Derivadas em a incluem os termoslog. Inverter essa identidade
determina uma representação por derivadas de R(z^-b L^r). Quando
o coeficiente tem zero simples, usa-se uma potência adicional deL;
o coeficiente do termo anulado pela derivada é fixado emzero apenas
na REPRESENTAÇÃO. Nenhuma constante de R é ajustada.

O contato de normalização é computado pelos mapas Laurent já pagos:

    R[H_l(partial)f]-H_l(partial)R[f]=C N_l[H_l,f]delta.

Logo a saída consiste na representação diferencial completa MAIS
seu contato local. Esta representação é uma referência de cálculo;
não foi chamada de prescrição BRST-invariante.

## Resultado e verificação independente
Para A, o contato local na primeiraK é

    Delta A/C=K[-13(q.T.v)/48-19 trT(q.v)/96],

com q representando derivadas do delta. Para B, o contato RELATIVO
à sua representação harmônica diferencial exibida é zero. Isso
NÃO diz que B seja zero ou que não contenha logaritmos: o controle
T00=1,v=e0 dá numeradorlog

    6x0²-2x1²-2x2²-2x3²,

não nulo. A média esférica desse log é zero; descartá-lo destruiria
o kernel fora da diagonal.

Foram calculados40 casos (dez fibrasT vezes quatro ghosts, p=e0)
e um caso denso não axial. A auditoria reconstruiu os80 kernels
A/B das40 amostras por derivadas radiais literais. Outra rota,
sem a inversão diferencial, usa a projeção esférica l=1:

    Delta A/C=(K/8)sum_i <A_geom(n)n_i>_S3 q_i.

Ela reproduz os mesmos coeficientes. Não incluir deltaT muda o
contato: em T00=1,v=e0 o erro é47q0/96. Assim, só o log previamente
medido não determina todos estes termos de extensão.

Movendo a derivada do delta para o ghost no funcional, a diferença
local tem a expressão covariante de primeira ordem

    Delta R(v)/C=-K[13G(v)+19g divv]/96,
    E Delta R(v)/C
       =19K[Hess(divv)-g Box(divv)-3Kg divv]/48.

A segunda identidade foi verificada com o operador físico E e
jatos reais covariantes, em duas amostras polinomiais atéK². Seu
termoK² é a imagem desse contatoK; NÃO inclui uma fonteK² ainda
não calculada. A parcelaG anula por E G=0; usou-se
E(gf)=-2Hess f+2gBox f+6Kgf, sem substituição por operador
gauge-fixado.

**Alcance:** 466 controles exatos, CPU55.25s, duas execuçõesrc0.
Ainda faltam os contatos finitos das outras bolhas e a soma com
a referência diferencial não local, suas ordenações covariantes e
os jatosW. O contato acima é a diferença entre duas escritas do
MESMO kernel estendido; não é sozinho Q2, nem justificativa para
zerar a quebra por escolha de contratermo. Os dados completos e
hashes estão no manifesto. Gate, kernel e originais intactos.

Falha técnica preservada: v1 substituiu z=x² antes de expandir e
cancelar os denominadores, produzindo PolynomialError; v2 muda
apenas essa ordem algébrica. Fonte, pré-registro e logv1 permanecem.
