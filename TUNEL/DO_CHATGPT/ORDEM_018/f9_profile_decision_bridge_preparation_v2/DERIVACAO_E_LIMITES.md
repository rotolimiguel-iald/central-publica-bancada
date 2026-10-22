# Derivação e limites — preparação somente

[DERIVED condicional] g_i é o ínfimo de q_i em todo o domínio físico original. Os perfis eliminam o extra afim condicionado a θ; varrer um conjunto finito produz somente uma estimativa/testemunha numérica. Arredondamento, backend e teoria não ganham certificação pela convergência da malha.

Com limites admitidos L_i≤g_i≤U_i, a composição exata é:
G1_lower=max(0,L1);
Q1_lower=max(0,L1−U3), somente após prova de H1⊂H3;
T21_lower=L2−U1; T41_lower=L4−U1; T51_lower=L5−U1.
U ausente mantém o contraste indisponível. Subtração usa Fraction; não há ajuste aos dados ou penalidade de prior na minimização.

Cada lower é ligado ao cenário/modelo/domínio/dados/C/X/resposta/suporte/configuração e ao conteúdo dos certificados. A cauda existente retorna uma cota racional conservadora condicionada às hipóteses externas. d=0 com estatística positiva continua INVALID, nunca rejeição. Ausência de calibração não é preenchida por p=1; o p=1 matemático válido após hipóteses admitidas permanece permitido pelo contrato original.

Bonferroni5 é aplicado somente pelo redutor. A ponte não chama aggregate_bounds nem multiplica por600. Os600cenários representam uma família finita de sensibilidade com máximo robusto, não600testes independentes. Nenhum Bayes vira sigma; ratios/lnB/poder não são inferidos de mínimos.

## Transporte racional→log

Normalizar p=m·2^(−k), 1/2<m≤1, por comparações inteiras. Para z=(m−1)/(m+1) em[−1/3,0], a soma truncada S=2Σj<64 z^(2j+1)/(2j+1) é superior a ln(m), pois os termos omitidos são negativos. L=2Σj<64 1/[(2j+1)3^(2j+1)] é inferior a ln2. Portanto ln(p)≤S−kL. A diferença é menor que (k+1)·9/(4·129·3^129). Não há inflação de p por fator2.

A soma exata pode ter dezenas de milhares de bits; antes de serializar, toma-se ceil((S−kL)·10^80)/10^80, somando no máximo10^-80 ao erro. A comparação do float com Fraction(as_integer_ratio) permite nextafter para cima se necessário; a direção é conferida exatamente. Não se altera sys.set_int_max_str_digits.

Isso certifica o transporte do bound racional recebido, condicional ao bound original, e NÃO certifica automaticamente a implementação float de alpha5=0,5erfc(5/√2), log5 e somas do redutor. O módulo separado threshold_audit.py decide com os p_upper racionais ORIGINAIS, preservando poder junto ao limiar; o dyádico é somente diagnóstico. A implementação exata confronta todos os campos decisórios da proposta do redutor e não publica a proposta inteira como científica. Logs e probabilidades float permanecem diagnósticos.

## Fronteiras honestas

[OPEN] Autenticidade/qualificação dos objetos carregados exige loader/verificador confiável; origem em arquivo pinado não se prova por atributos mutáveis.
[OPEN] A semântica de certificados numéricos e hipóteses físicas exige implementação externa efetiva; a cauda apenas confere recibos vinculados e faz a aritmética racional. O double dos testes não serve para ciência.
[OPEN] Uma busca/otimização contínua não foi implementada nem necessária ao pós-processamento finito; o domínio integral permanece como alvo.
[DERIVED/OPEN] A conferência independente racional do limiar está implementada separadamente, conforme revisão matemática comunicada por ROOT/preregistros. A execução da implementação e sua revisão de código ainda estão pendentes; nenhuma aprovação científica nasce de presença de código.
[OPEN] O adaptador não integra evidências relativas; preserva esse campo separado. Não substitui integrador de priors existente.
[INPUT] Recursos: deadline cooperativo explícito,6002 chamadas semânticas no máximo, material até32 blobs/8MiB por cenário, perfil até256KiB, uma passagem por cada nó. Limites OS, memória agregada, persistência de claim/no-retry e kill/reap ficam no supervisor futuro existente. Estes caps são guardas de esquema/execução propostas, não custos medidos ou autorização de consumo.

## Intervalo racional estreito de alpha5

[DERIVED — argumento conferido independentemente por preregistros e aprovado por ROOT na coordenação de06/10/2026; esta preparação não reexecutou a conferência.]

S_N=Σn=0..N (−1)^n·5^(2n+1)/(2^n n!(2n+1)).
O resto de Taylor de exp(−x²/2) tem o sinal alternado em todo[0,5]; portanto S127<I<S128, com I a integral de0a5. Não é preciso supor termos decrescentes desde n=0.

A_N(z)=Σn=0..N(−1)^n z^(2n+1)/(2n+1).
Machin dá piL=16A65(1/5)−4A64(1/239), piU=16A64(1/5)−4A65(1/239). A subtração troca os limites do segundo termo.

Para racional a/b>0, Q=10^70, k=isqrt((aQ²)//b); verificar k²b≤aQ²<(k+1)²b produz [k/Q,(k+1)/Q]. Obter sL=rootlower(2piL), sU=rootupper(2piU), cL=1/sU,cU=1/sL.
alphaL=1/2−S128cU; alphaU=1/2−S127cL.

O revisor informou largura<10^-69 e bracket5·2^-25<alphaL<alphaU<5·2^-24; o módulo confere essas desigualdades racionais durante sua futura chamada. Não há hash/endpoints copiados de memória nem valor transcendental float promovido a prova. A fonte documental do parecer independente será a revisão irmã, quando selada.

Para cada cenário e depois para o máximo robusto completo, pF=min(1,5p_upper). Se pF≤alphaL, rejeita; se pF>alphaU, não rejeita por este majorante. Intervalo cruzado é UNAVAILABLE para decisão, sem apagar a validade da cota/calibração. Não-rejeição por majorante não prova p verdadeiro grande. A comparação por inteiros não pressupõe precisão de libm; qualquer divergência de booleanos/estados do redutor fecha a decisão.
