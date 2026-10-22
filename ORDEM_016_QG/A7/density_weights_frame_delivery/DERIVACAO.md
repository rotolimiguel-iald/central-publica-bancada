[DERIVED — conversão e combinatória verificadas; montagem completa/Q2 OPEN]

## Correção de sinal ao lado da entrega anterior

A inversa bosônica anterior permanece:GD=-4kappa S GQ e Ghb=G GQ.
O passo incorreto era tomar V3stored/(16kappa) como vértice em derivadas REAIS.
O arquivo metric_principal_vertices.py armazena o polinômio FOURIER.
Na ação S=-integral chi sqrt(g)R/(2kappa), cada monômio localizado tem DUAS
derivadas, inclusive a fronteira dchi.B. Substituir partial por ip dá i²=-1.
Logo V3real=-V3stored/(16kappa), V2real=-V2stored/(8kappa).

Uma expansão independente de g^-1,sqrt(g),Gamma por coeficientes nilpotentes
reconstruiu C_GammaGamma com Gamma REAL e a corrente B. Em5 configurações,
V3stored=-16 V3real(kappa=1), incluindo dchi não nulo;16 verificações.
Exemplo: densidade cúbica real=-1; vértice armazenado=16.
Portanto o diagrama com UM EH e Jb direto recebe+1/4, não-1/4.
Dois vértices EH-derivados têm os dois sinais e preservam o produto.
mixed_b_h_current_engine_v3.py corrige somente esse fator;575checks novamente.
O controle Y passa a128/16807 e contato-259/192; XY a-1222/16807 e-35/32.
A entrega anterior e v2 ficam preservadas com errata explícita, não apagadas.

## Pesos de Wick derivados sem olhar o resíduo

Na expansão euclidiana formal exp(-V/hbar), o coeficiente cruzado conectado
da ação efetiva é-<VX VY>. Para VX=x.A.x/2 e VY=y.B.y/2, Gamma_G²/2 dá
<VX VY>=tr(A G B G^T)/2. O par métrico tem peso-1/2.
Para barX cX barY cY, a contração cruzada é negativa; o par ghost tem+1.
Para a média da corrente, a primeira ordem é-<C V>:
* corrente simétrica C=J_AB h_A h_B c/2: peso-1/2 na contração matricial;
* corrente b h c: peso-1 em UM emparelhamento ordenado (os dois cancelam1/2);
* corrente ghost: peso-1 no resultado que JÁ inclui os dois emparelhamentos.
O cálculo por derivadas bosônicas simbólicas e álgebra exterior conferiu11
identidades. Não são fatores ajustados para cancelar um número da bancada.
É necessário ainda ligar todos os representantes de densidade à MESMA Ward.

## Controle da montagem parcial e termo que falta

Antes da execução foi registrada a soma candidata
pair+source+current_metric/2+current_bh+current_ghost,
com corrente situada emY, h externo emX e c externo emY.
Com h11,c0,x=(1,2,-1,1) e jatos EXPONENCIAIS completos:
* lambda=eta=0:resíduo0;
* lambda=0,eta=e0:resíduo0;
* lambda=e0-e1,eta=e0:resíduo-14928/117649.
No segundo caso,pair=3281/117649,source=-796/117649,metric=-12104/117649,
bh=128/16807,ghost=2671/117649. A soma com os pesos pré-fixados é0.
O valor antigo3960/117649 tinha apenas gradienteY, demais jatos nulos;
não é o mesmo teste que chiY com jatos exponenciais de todas as ordens.

O teste NÃO cobre todos os tensores/pontos/estados e não prova Q2=0.
Ainda faltam correntes situadas emX com h externo e ghost interno, contra
o vértice ghost emY, além dos setores já abertos. Essas inserções podem
contribuir quando dchiX!=0; a identificação não prova que absorvam todo o
resíduo. Um resíduo fora da diagonal diagnostica montagem incompleta ou
incompatível, não uma anomalia LOCAL da extensão. Nenhum peso foi reajustado.

## Parecer Kimi normal-frame

Recebido e lido inteiro, consumo registrado uma vez:378738tokens totais;
assinatura sem custo monetário alocado. Detector não axial conferido:
estruturas(14,-14,2) e(0,-7,-2); contatos/C_E=113/8 e83/288; ordem5=14.
A diferença de esquemas(-35/144,-1/12,7/72) foi conferida.
Correção: diferença não nula NÃO prova não naturalidade de um esquema.
Dois operadores naturais podem diferir por contratermo natural local não zero,
como K g_ab box(div c). A naturalidade da prescrição coordenada continua
OPEN até conferir sua transformação; não foi refutada por aquela diferença.
Taylor radial para testes suaves vale como identidade de jatos finitos com
resto, não série necessariamente convergente. Convenção de fase já tinha
ponte medida; falta de contexto do parecer não reabre esse item.
29 controles na auditoria v2;v1 preservada por testar apenas soma das entradas
da matriz de rotação, substituída por conferência componente a componente.

Total631 verificações (inclui575 repetidas pela mudança de sinal) +3
diagnósticos da soma;CPU24.109375s. Primeiro comando da densidade usou Python
semSymPy e falhou antes do cálculo; log preservado, runtimeA4 concluiu rc0.
Custo externo conhecido parcial recontado:US$1.4569561218, estimativa/não fatura.
Nada alterado emum.py,kernel,gate ou fontes canônicas. A7b segue até20:32UTC.
Abertura sha256:216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
