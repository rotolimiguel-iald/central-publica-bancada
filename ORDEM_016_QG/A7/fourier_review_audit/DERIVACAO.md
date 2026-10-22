[DERIVED — auditoria exata parcial do parecer Fourier; convenções separadas]

O parecer Kimi6c210ea9 foi lido integralmente. Fixando Fourier exp(-ip.x),
harmônicos sólidos usuais e z=x², Schwinger fornece

    F[H_l(x)z^-lambda]
      =(-i)^l pi² 2^(4-2lambda+l)
        Gamma(2+l-lambda)/Gamma(lambda) (p²)^(lambda-l-2) H_l(p).

Com N=(m+l+4)/2, k=(m-l)/2, lambda=N-a, a família regularizada
contém exp(a log(4mu²/p²)) (p²)^k. Não contém, adicionalmente,
(p²)^(-a). A linha intermediária do parecer conta essa potência duas
vezes; sua fórmula final já elimina a duplicação.

Na parte finita FP[(1-a)...], as formas gerais do motor foram conferidas
nos36 casos m=0..4,l=0..6 de paridade compatível, log0/1. Separando
C_E i^m, a fórmula Schwinger é (-1)^l vezes a do motor. Isso confirma
a discrepância ímpar SOB ESSAS CONVENÇÕES. Ainda não é diagnóstico de
sinal errado da amplitude montada: é necessário rastrear as fases dos
geradores externos e a orientação dos endpoints. Nenhum motor foi editado.

O coeficiente cúbico de log[Gamma(1+a)/Gamma(1-a)] é -2zeta(3)/3,
e não positivo. Não afeta as partes finitas estudadas (log0/1).

A objeção à mudança m->m-j para multiplicadores angulares não procede.
Se o kernel tem homogeneidade -m-4, multiplicá-lo por um polinômio
homogêneo de grau j dá -(m-j)-4. Toda componente harmônica recomposta
tem esse mesmo grau total. Seu índice l muda, mas não esse m-j.
Controle não radial, H_l=(x0+i*x1)^l:

    x0 H_l = Hplus_(l+1) + z*l/[2(l+1)] H_(l-1),
    Hplus = x0 H_l - z*l/[2(l+1)] H_(l-1).

Hplus é harmônico em quatro dimensões. Nos oito pares testados,
m=1..4,l=m+2 ou m+4, a transformação das DUAS componentes com m-1
reproduz i*d/dp0 da transformada original. Nenhuma média angular
foi usada para apagar componentes.

Três valores literais da tabela do parecer diferem da própria fórmula
geral: c0(0,4,0)=-1/24; c0(0,6,0)=1/48; c0(1,1,1)=-7/64.
O JSON preserva as afirmações originais e os valores medidos.

Um polinômio em p, transformado de contato em x, é visível em p²>0.
Não deve ser confundido com distribuição suportada somente em p=0.
Além disso, k<0 sozinho não determina a integrabilidade no zero:
H_l(p) participa do grau total. Esta auditoria não fixa uma extensão
lorentziana nem uma prescrição nova no momento zero.

57 controles exatos, CPU8.8125s, rc0. Não são observações físicas
independentes nem prova Lean. Próximo: rastrear a fase ímpar na montagem
externa e confrontar a soma distribucional completa. Q2 continua OPEN.
