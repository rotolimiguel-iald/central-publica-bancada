# Serviços de precisão F9: derivação do candidato

Pedido f820203f-b83c-420a-87ec-7816f3179139. [DERIVED — fórmulas sob as hipóteses explicitadas] [REAL — código preparado e fontes conferidas, sem execução numérica]. Este pacote resolve duas dependências de implementação do df482; não acrescenta prior, modelo físico, solver gaussiano ou autorização. Não calcula dados, controles, evidência ou sigma.

## 1. Escolha do algoritmo

Foram comparadas as duas alternativas do pedido. A forma log-CDF/erfc é uma identidade útil, mas exige uma realização qualificada para diferenças estreitas, caudas extremas e cancelamento entre prefator e cauda. Subtrair CDFs comuns ou chamar erfc e depois log não resolve todos esses casos. Não foi importado nem qualificado um serviço especial externo nesta preparação.

A escolha concreta é quadratura positiva adaptativa, com uma transformação analítica que localiza o máximo quando a quadrática é conhecida. O mesmo núcleo de Simpson atende a janela e o callback H5; a geometria do backend gaussiano existente continua no chamador. Dependências do candidato: math, heapq e fractions, da biblioteca padrão. A integração genérica não tem acesso a curvatura/pico do callback: sua limitação a picos não amostrados é explícita, não suprida por adivinhação.

## 2. Recentralização exata dos números recebidos

O alvo é W=integral[L,U] exp(hz−Az²/2) dz, A>0, L<U e L≤0≤U. As entradas int/float são convertidas a floats finitos, como exige o contrato de engenharia. Em seguida Fraction representa exatamente ESSES floats; não reconstrói a precisão perdida no backend que os produziu.

Defina p=clip(h/A,[L,U]), M=hp−Ap²/2 e c=h−Ap. Essas operações são racionais. Não formamos h²/(2A) em float, nem dois endpoints de CDF normalizados quase iguais. Em cada lado não vazio de p, com distância r≥0, a função tem a forma:

exp(M) exp(−b r−A r²/2).

No lado esquerdo b=c e d=p−L; no direito b=−c e d=U−p. O máximo restrito garante b≥0 em cada lado existente: se p é interior, c=0; se p é uma fronteira, só existe o lado de derivada não positiva. A aritmética racional conserva esse fato mesmo quando o h recebido possui pequeno resíduo por arredondamento da ancoragem anterior. O serviço não exige h exatamente zero para uma entrada aproximadamente centrada.

Como zero pertence ao intervalo, M≥0. Isso não significa que exp(M) será calculado. Só M e o log da integral escalada são combinados. Se o log final ou o próprio M não tiver representação finita suportada, há falha de faixa numérica, nunca −inf fabricado para uma integral positiva.

## 3. Escala que resolve o máximo e a janela curta

Escolha s_A diádico com 1/4 < A s_A² ≤ 1. A aproximação inicial usa comprimentos de bits do racional A; comparações racionais ajustam o valor. Para cada lado:

s=min(d,s_A,1/b), omitindo 1/b quando b=0;
B=b s, C=A s²/2, T=d/s.

Temos 0≤B≤1, 0<C≤1/2 e T≥1. Se T>1, a escala foi limitada pela curvatura ou pela inclinação: B=1 ou C>1/8. Assim, uma região de variação de ordem um está sempre ancorada em t=0. Se a janela for menor que ambas as escalas, s=d e T=1: a largura pequena permanece no fator s em log, sem desaparecer na subtração de endpoints normalizados.

A contribuição do lado é s K, K=integral[0,T] exp(−Bt−Ct²)dt. O sinal positivo evita cancelamento entre contribuições. Não há limiar que substitua A pequeno por zero. A=0 está fora desta API; o df482 já trata seu ramo plano pela normalização do prior.

## 4. Cauda finita contabilizada

Para psi(t)=Bt+Ct², convexidade dá psi(t)≥psi(R)+psi'(R)(t−R) para t≥R. Portanto, em aritmética real:

0≤integral[R,T] exp(−psi(t))dt ≤ exp(−psi(R))/(B+2CR), se R<T.

Quando R=T, não há cauda omitida. Além disso, K≥integral[0,1] exp(−Bt−Ct²)dt≥exp(−3/2). Essa desigualdade permite escolher o corte sem avaliar previamente uma massa arbitrariamente pequena.

O código dobra R a partir de1, sempre limitado pelo endpoint racional T, até que o log da envoltória seja menor que log(min(meta_log,1/4)/32)−3/2. Há no máximo16 passos de localização. O restante não é silenciosamente apagado: sua envoltória entra na estimativa relativa. O método reporta corte e log da envoltória em seu texto de diagnóstico. O limite16 e o teto de nós são recursos distintos; a localização usa álgebra/logaritmos, sem chamar o integrando ou um backend.

Essa desigualdade é algébrica. Sua avaliação float nesta implementação NÃO constitui limite com arredondamento externo certificado. O resultado continua ESTIMATED_NOT_CERTIFIED. Se a exponencial da contribuição relativa da cauda underflowar, o código conserva uma margem positiva mínima representável em vez de chamar a massa de exatamente zero.

O intervalo restante é transportado para u∈[0,1], t=Ru. A área numérica J=integral[0,1] exp(−BRu−CR²u²)du produz log(s)+log(R)+log(J). Essa representação evita materializar s quando sua conversão direta underflowaria. O log de um racional positivo usa uma mantissa de ordem um e expoente binário inteiro.

## 5. Regra adaptativa positiva compartilhada

Cada painel [a,b] mantém cinco nós distintos: extremos, ponto médio e os dois meios de cada metade. S é Simpson com três nós; S2 é a soma das duas metades. Os pesos de S2 são positivos, proporcionais a (1,4,2,4,1). Para evitar overflow desnecessário em valores altos, a média ponderada é calculada após divisão pelo maior valor do painel, e o fator é recolocado depois da largura.

Se o erro de Simpson estiver no regime assintótico c h⁴, refinamento por2 reduz esse erro por16; a diferença S2−S estima quinze vezes o erro de S2. Por isso o estimador local é |S2−S|/15. A implementação usa S2 positivo, sem correção de Richardson que possa produzir massa negativa. Acrescenta margens heurísticas de arredondamento baseadas em epsilon/ulp; essas margens não são enclosures rigorosos de funções elementares, de callbacks ou do backend.

Os painéis são mantidos numa fila por maior erro estimado. Uma subdivisão custa quatro chamadas novas; valores em nós compartilhados são reutilizados. O serviço H5 inicia com quatro painéis (17 nós), cobrindo [0,1]. Cada lado monotônico da janela inicia com um painel (5 nós); a localização analítica já ancorou seu máximo no primeiro extremo.

Antes de começar uma subdivisão, verifica-se se há quatro avaliações disponíveis e se os novos nós são distintos em float. Se não, preserva-se a partição atual inteira. Nenhum painel é descartado ou renormalizado. A soma final é refeita com fsum sobre todos os painéis; não se aceita somente uma soma incremental. O teste local usa erro≤max(meta_absoluta,meta_relativa×área), implementado por comparações que evitam overflow da multiplicação.

O encerramento por orçamento ou resolução float devolve estimativa finita com converged=False. O serviço não repete a unidade nem troca automaticamente de algoritmo. Orçamento menor que a malha inicial necessária é erro explícito antes de chamar o callback:17 para H5,5 por lado não vazio para a janela.

## 6. Erro do log e soma dos lados

Se uma margem relativa r<1 limitasse efetivamente o erro de uma área positiva, −log(1−r) limitaria a diferença de seus logs. O código usa essa relação para transportar o estimador local e a contribuição de cauda, somando a margem heurística de arredondamento da escala/coordenadas. Se não obtiver estimativa finita útil desse transporte, marca o erro UNASSESSED e converged=False ou propaga falha de faixa; não declara convergência sem diagnóstico.

A soma dos lados é feita por log-sum-exp e recebe o maior erro logarítmico estimado dos lados mais margens de combinação e do pico. A combinação é positiva. Um lado muito menor pode ficar abaixo da resolução relativa de float, limitação que as margens de engenharia não transformam em prova de exatidão. O módulo retorna o alvo combinado, sem exp(M) nem produto gigantesco por massa minúscula.

Os orçamentos da janela são repartidos de forma determinística entre os lados restantes; a sobra não usada no primeiro fica disponível ao segundo. Não há segunda tentativa para redistribuir retrospectivamente orçamento de um lado que não convergiu. A contagem total soma exatamente os nós avaliados nos lados e não ultrapassa o teto.

## 7. Limitação inevitável do callback genérico

O serviço positive_quad_1d recebe somente uma função opaca e duas metas. Nenhum algoritmo com amostras finitas pode excluir um pico arbitrariamente estreito entre os nós sem informação adicional. A coincidência de duas regras e um erro estimado pequeno não demonstram a ausência desse pico. Isso vale também para uma função suave cuja escala de variação não foi limitada.

O callback H5 é positivo e escalado pelo df482; sua forma especial não é acessível por esta API. O método registra missed_peaks_unbounded. converged=True significa somente satisfação do critério do estimador amostrado. Todos os nós zero provocam falha NO_POSITIVE_SAMPLED_MASS, pois não distinguem underflow de pico não encontrado. Valores negativos, NaN, infinito, bool ou tipos numéricos não admitidos falham. Uma área zero/underflow não vira integral física nula.

Exceções do callback propagam sem catch/retry ou substituição por zero. A contagem é incrementada antes da chamada real e nós em cache não chamam o callback novamente. Isso casa com o contador do df482 e preserva seu latch externo. O chamador precisa fornecer callback determinístico e sem efeitos colaterais; o módulo não é sandbox para um objeto arbitrário.

## 8. Escopo preservado

Os oito campos do recibo são exatamente os aceitos pelo df482. Ambos os serviços são ENGINEERING_ESTIMATE; nenhum retorna certificado, Bayes factor ou sigma. O erro local estimado não cobre C/suporte, coeficientes A/h, reconstrução de médias, aritmética do backend ou erro físico do fundo. MM continua condicional e theta não é integrado por estes serviços.

Não houve importação de precision_services.py, execução de fórmulas de exemplo, comparação de algoritmos em números, controle sintético, solver, leitura de observados, rede, provedor, instalação ou criação de AUTH/CLAIM. AST e hashes são verificação estática; qualificação numérica permanece uma etapa futura própria, dependente de revisão e decisão específicas.
