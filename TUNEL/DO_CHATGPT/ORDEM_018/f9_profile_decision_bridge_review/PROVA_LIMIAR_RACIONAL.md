# Derivação independente da ligação racional ao limiar

[DERIVED] Revisão matemática da construção finita, sem avaliação dos candidatos ou repetição da conferência aritmética anterior. Esta nota não certifica L/U de um modelo físico nem hipóteses amostrais. O código foi inspecionado; sua execução permanece separada.

## Intervalo para alpha5

Defina I = integral de 0 a 5 de exp(-t²/2) dt e alpha5 = 1/2 - I/sqrt(2*pi). Para u >= 0, o resto de Taylor de exp(-u) após ordem N tem sinal (-1)^(N+1), porque a derivada correspondente é esse sinal vezes um número estritamente positivo. Integrando em t, S127 < I < S128, onde

S_N = soma n=0..N de (-1)^n 5^(2n+1)/(2^n n! (2n+1)).

A validade não exige que os primeiros termos da série sejam decrescentes. As séries arctan em 1/5 e 1/239 têm termos decrescentes e resto alternado. Pela identidade de Machin, pi = 16 atan(1/5) - 4 atan(1/239); portanto

piL = 16 A65(1/5) - 4 A64(1/239);
piU = 16 A64(1/5) - 4 A65(1/239).

O sinal de subtração troca os extremos do segundo termo. Para x=a/b>0 e Q=10^70, k=isqrt(floor(a Q²/b)) satisfaz k² b <= a Q² < (k+1)² b. Logo k/Q <= sqrt(x) < (k+1)/Q, inclusive quando x é quadrado exato. Aplicando aos extremos 2*piL e 2*piU, obtemos sL <= sqrt(2*pi) <= sU. Como I e os denominadores são positivos:

alphaL = 1/2 - S128/sL < alpha5 < 1/2 - S127/sU = alphaU.

threshold_audit.py verifica a identidade inteira das raízes, ordem/positividade, largura < 10^-69 e o bracket 5*2^-25 < alphaL < alphaU < 5*2^-24. Essas verificações estão no candidato; não foram executadas nesta revisão. A conferência aritmética pontual anterior autorizada foi comunicada à coordenação e não foi repetida.

## Transporte do majorante racional para log

Para 0<p<=1, a normalização inteira escolhe k>=0 e m=p*2^k com 1/2<m<=1. Ponha z=(m-1)/(m+1), logo -1/3<z<=0. A identidade ln(m)=2*atanh(z) dá uma série com todos os termos omitidos negativos quando z<0. Assim S=2 soma j=0..63 z^(2j+1)/(2j+1) >= ln(m). Já L=2 soma j=0..63 1/[(2j+1)3^(2j+1)] < ln(2). Portanto U=S-kL >= ln(p).

O resto absoluto da série para |z|<=1/3 é limitado por
R = 2*(1/3)^129 / [129*(1-1/9)] = 9/(4*129*3^129).
A diferença U-ln(p) é no máximo (k+1)R. A compressão ceil(10^80 U)/10^80 acrescenta menos que 10^-80 e mantém a direção superior; comparar o float produzido com Fraction(*float.as_integer_ratio()) e aplicar nextafter para cima, se preciso, preserva a mesma direção. Não há conversão libm de log promovida a prova. p=1 pode retornar exatamente log0, com erro0.

## Decisão exata e multiplicidade

Os 600 cenários formam a família finita de sensibilidade declarada; sua união usa o máximo dos majorantes, sem supor independência e sem substituir cenários ausentes por 1. Para cada teste j, p_FWER_upper = min(1,5*max_s p_upper[j,s]); no cenário, usa-se min(1,5*p_upper[j,s]) apenas para confrontar a proposta diagnóstica.

Se esse racional <= alphaL, a desigualdade com alpha5 é demonstrada. Se > alphaU, o majorante não satisfaz o limiar; isso não prova que o p verdadeiro seja grande. Se cruzar [alphaL,alphaU], a decisão fica indisponível. O código reconstitui os booleanos e os estados exatos e exige concordância da proposta float. Não certifica os valores float erfc/log/exp dessa proposta. A inflação dyádica de até 2 vezes não é usada: compara o p racional original.

## Vínculo com mínimos

Sob as hipóteses verificadas de mesma C, mesmo suporte afim e mesmo X entre os modelos de um cenário, os fatores de normalização da likelihood amostral são comuns. Então os contrastes de máximos de log-likelihood podem ser compostos pelas diferenças dos mínimos de q, sem utilizar a integral plana sobre eta como likelihood amostral:

G1 >= max(0,L1);
Q1 >= max(0,L1-U3), com inclusão H1 contida em H3 verificada;
T21 >= L2-U1; T41 >= L4-U1; T51 >= L5-U1.

O prior físico limita o domínio, mas suas densidades/Jacobianos não entram nessa minimização. A medida comum kappa d eta continua pertinente aos usos relativos de evidência em outra interface; a ponte não calcula evidência nem lnB. Certificados externos precisam demonstrar os mínimos sobre todo o domínio e os erros pertinentes. Testemunhas em uma malha finita continuam ENGINEERING_ONLY e não são L/U certificados.

## Fronteira de confiança

Pins e recibos vinculam identidades; não tornam um verificador arbitrário honesto. A qualificação dos objetos carregados, da admissão, dos mínimos, do suporte, da dominação nula, do grau e da inclusão depende de verificador externo confiável ainda não fornecido. Os doubles de composição têm escopo SYNTHETIC_CONTROL_ONLY e não podem emitir scientific_decision. Nenhuma prova de física, ratificação, abertura ou autorização de execução é concedida por esta nota.
