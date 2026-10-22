[REAL — auditoria exata; DECLARADO — parecer externo; OPEN — Q2]
# A7.b — revisão local do parecer Kimi sobre curvatura
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T03:36:18.944282+00:00.
Parecer recebido: job679d8876-d8b9-44db-ae96-3f8f8f67fb54;
fonte recebida preservada em received_reviews/ com hash no manifesto.

**Aproveitado:** traços de curvatura(-144,-24)K² e peso de calor livre
-571K²/15 coincidem com o cálculo já entregue. A distinção entre conexão
de fibra e dez campos escalares é correta. Não foi refeito esse laço.

**Correções demonstradas:**
1. D=-(nabla²+E) tem símbolo q²-E. Os denominadores são q²+2K
   (sem traço), q²-6K (traço), q²-3K (ghost), não os sinais da seção7.
2. Em coordenadas normais, partial_i g^ij=-Kx^j e
   g^ij partial_i log sqrt(g)=-Kx^j nessa ordem. Somam -2Kx^j;
   não se cancelam. O controleC5 proposto no parecer falha.
3. Duas inserções lineares de Omega têm ordemK². Derivar em momento
   não transforma esse produto em ordemK, mantida a expansão local UV.
4. A simetria maximal não reduz a Hessiana hh a um único Kp²:
   os4 invariantes bilineares usados pela bancada têm posto4.

**Correção de objeto:** o calor livre no fundo on-shell não é a família
de operadores com h externo, nem sua Hessiana. O valor de uma função num
ponto não determina sua segunda derivada. O resultado ghost já entregue
contém, no canal conforme, integral[7(boxf)²/8-19K(df)²/2], condicionado
à sua redução de calor. Portanto não cabe promover o paralelismo do fundo
à ausência desses termos. Momento externo e momento interno do laço
também precisam de nomes separados. O próprio parecer mantém Kq² OPEN.

A fatoração de determinantes finitos e sua fase não é estabelecida apenas
pela comutação com B; regulação e escopo devem acompanhar a afirmação.
A anulação de uma inserção Omega em linha livre isotrópica não prova
anulação numa bolha com vértices tensoriais arbitrários.

18 controles exatos, rc0, CPU0.125s.
Nenhuma repetição de chamada, novo laço ou alteração de originais/gate.
Os resultados úteis do modelo são preservados; a proposta de símbolo da
seção7 não será usada sem essas correções. Q2 continua aberta.
