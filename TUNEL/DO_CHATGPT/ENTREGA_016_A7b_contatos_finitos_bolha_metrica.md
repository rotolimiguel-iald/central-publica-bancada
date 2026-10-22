[DERIVED — diferença local de um par métrico; REAL — CAS; OPEN — soma completa]
# A7.b — contato finito do kernel métrico com jatos covariantes
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T06:11:47.583935+00:00.

Mantivemos os vértices W2/W1 e de potencial, Green bitensorial G0/G1/GL,
a medida geométrica e os jatos ordenados usados na Hessiana logarítmica.
Agora substituímos o peso de Taylor pelos projetores harmônicos do contato
finito já verificados, sem mudar R=FP[(1-a)mu^(2a)z^a .]. A integração
usa os128 nós racionais existentes da cubatura de S3 até grau8.

Para dois vértices com n_x,n_y derivadas internas, ordem geométrica r,
o contato usa m=n_x+n_y-2r. Jatos de ordem covariante o, e potências
explícitas e_x,e_y do potencial, satisfazem o+r+e_x+e_y=ordemK.
Os monômios q^I já trazem seus coeficientes: não se reaplica o divisor I!.
O sinal (-1)^m vem da ação da derivada do delta no teste. Permanecem o
sinal da integração por partes da perna ancorada e o sinal relativo dos
vértices de potencial, calibrados na construção logarítmica anterior.

Harmônicos escalares l0 dão contato zero RELATIVO a R(U_b L^r). Por isso
o kernel geométrico r2, com m0, não gera esta diferença; a parcela K²
ainda recebe contribuições dos jatos covariantes dos kernels r0 e r1 e
dos vértices de potencial. Isso não descarta a amplitude não local r2.

## Resultados
Na base K[p²trAB,p²trA trB,pAp trB,pBp trA,pABp], os coeficientes são:

    ['215/432', '-1099/1728', '107/864', '107/864', '437/288']

Na base K²[trAB,trA trB], são:

    ['4463/216', '-4463/864']

Normalização: contato/C do PAR MÉTRICO CRU, com o fator1/16 herdado do
motor posicional. Ainda NÃO aplicado o peso de Wick -1/2, nem acrescentado
o tadpole finito, o ghost, W suave ou as fases causais Lorentzianas.
Diferença entre os coeficientes pAp trB e pBp trA:

    0

Esse diagnóstico é preservado. Uma diferença de referências não deve ser
tratada como contratermo admissível ou operador físico sem conferir suas
simetrias e a amplitude de referência que a acompanha.

## Verificação e limite
PrimeiraK: cinco pares escolhidos por posto algébrico, mais um novo par
de fibras e um novo momento não axial. Dos quatro pares chamados holdouts
no pré-registro, três já estavam no ajuste: são RECHECAGENS, não evidência
independente. SegundaK: dois coeficientes obtidos de dois pares e conferidos
em dois pares adicionais. O relatório conserva valores de cada parcela
geométrica e logarítmica, sem impor que logs desapareçam por hipótese.
São 7 comparações de reconstrução, rc0, CPU443.84375s.

Não é a quebra Ward total: falta a combinação com o par ghost finito,
tadpoles, contatos da fonte na mesma referência e W admissível. A passagem
entre esta representação harmônica e a representação principal anterior
foi enviada em tarefa distinta ao Kimi. Nenhum gate ou original alterado.
