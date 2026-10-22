# Revisão independente — serviços de precisão F9

**[REAL — revisão estática] Nenhum bloqueador material identificado no pacote f820203f-b83c-420a-87ec-7816f3179139 para o escopo de engenharia declarado.** As duas implementações podem seguir à decisão concreta de integração de ROOT. Este parecer não executa, qualifica numericamente ou autoriza consumo dos serviços.

O contrato df482 e o parecer573 foram lidos antes do exame. A consulta prévia da rota foi seguida pela anotação582. O manifesto da origem foi conferido por bytes no início e no fechamento; seus oito membros e o backup imediato concordam com os pins. O recibo registra cada fonte e verificação, sem transferir uma medição do autor para a autoria desta revisão.

## Janela exponencial quadrática

[DERIVED — álgebra sobre as entradas recebidas] Em precision_services.py:224–289, após conversão admitida para float finito, Fraction representa exatamente esses floats. Não recupera precisão de A/h perdida anteriormente. Para p=clip(h/A,[L,U]), M=hp−Ap²/2 e c=h−Ap, a exponencial é exp(M) exp(−b r−A r²/2) em cada lado existente. Os sinais usados são corretos: b=c à esquerda e b=−c à direita. Em máximo interior c=0; num máximo de fronteira só existe o lado cujo b é não negativo.

A escala diádica s_A satisfaz 1/4 < A s_A² ≤ 1. A escolha s=min(d,s_A,1/b), omitindo 1/b quando b=0, produz B=bs∈[0,1], C=As²/2∈(0,1/2] e T=d/s≥1. Se T>1, pelo menos a inclinação ou a curvatura determina uma escala resolvida no extremo t=0. Se a distância d limita a escala, T=1 e a janela estreita é mantida em log(s), sem subtrair endpoints de uma CDF.

Para R<T, convexidade de ψ(t)=Bt+Ct² implica a envoltória de cauda exp(−ψ(R))/(B+2CR). O limite inferior integral[0,1]exp(−ψ)dt≥exp(−3/2) justifica a localização prévia. O código considera R=T como ausência de cauda omitida e inclui a contribuição estimada do restante nos outros casos; não integra a janela truncada como se fosse o alvo completo. A localização tem 16 passos máximos, separados do orçamento de avaliações.

O integrando numericamente avaliado é exp(−BRu−CR²u²). A contribuição combina log(s)+log(R)+log(área), depois soma os lados por log-sum-exp e acrescenta M. Nenhum exp(M) ou produto de prefator gigantesco por diferença de CDFs é formado. O h residual não precisa ser exatamente zero; o recenter racional acomoda a ancoragem float de df482.

A pequeno positivo não é trocado por zero. A=0 fica fora deste serviço e permanece no ramo plano de df482. Escalas racionais muito pequenas não são primeiro convertidas diretamente em float: seus logs usam expoente binário e mantissa normalizada. Alturas/logs fora da faixa admitida produzem erro; uma integral positiva não recebe −inf por underflow. As conversões finais de coeficientes, log/exp e somas continuam float; a derivação não as apresenta como aritmética intervalar certificada.

## Quadratura e avaliação do callback

[REAL — estrutura lida] _Samples.at:60–75 verifica o domínio, consulta cache, verifica teto e incrementa count antes da única chamada ao callback. A chamada não está dentro de try/except; suas exceções propagam sem retry ou substituição por zero. O cache só recebe retorno validado. Bool, tipos externos, valores negativos e não finitos são recusados. O chamador precisa fornecer a função determinística e sem efeitos colaterais já prevista; este módulo não é uma sandbox para callback arbitrário.

positive_quad_1d:157–170 exige exatamente [0,1] após a conversão documentada, metas positivas finitas e orçamento inteiro. A malha inicial tem quatro painéis, logo 17 avaliações distintas. Cada subdivisão diádica acrescenta quatro nós; a disponibilidade é conferida antes e o teto também é imposto em cada chamada. As subdivisões preservam toda a partição. A contagem de sucesso é compatível com a comparação exata feita pelo df482:240–241 com seu contador externo.

A regra fina usa pesos positivos (1,4,2,4,1); a correção de Richardson não altera a área. |S2−S|/15 é usado como estimador, acrescido de margens heurísticas de arredondamento. A soma final é refeita por fsum; a aceitação também reconfirma o critério após recompor as somas. Orçamento ou resolução float encerram com converged=False e a partição atual, sem descartar massa ou renormalizar.

O critério H5 é erro≤max(meta_absoluta,meta_relativa×área), exatamente o que a documentação declara. Não exige ambas as desigualdades simultaneamente. Todos os nós inicialmente zero falham, e área final zero/underflow também falha. Um pico não visto entre nós permanece possível mesmo havendo valores positivos e acordo entre regras; missed_peaks_unbounded e ESTIMATED_NOT_CERTIFIED registram esse limite explicitamente. Não identifiquei falsa alegação de exclusão global de picos.

Na janela, os orçamentos são repartidos entre um ou dois lados; sobras passam ao próximo, sem reexecutar o primeiro. evaluations soma os integrandos internos efetivamente avaliados, não operações racionais/logaritmos ou chamadas cosmológicas. Nos erros sem um contador disponível, evaluations=None já é permitido; não deve ser reinterpretado como zero chamadas. O contador externo de H5 conserva a evidência de chamada abortada.

## Erro local, API e alternativas

O transporte do erro relativo r<1 para o log por −log(1−r), seguido do máximo dos erros dos lados numa soma positiva, é coerente se as margens fossem bounds. Aqui são expressamente estimadores: a cauda é uma desigualdade em aritmética real, mas sua realização float não recebe arredondamento externo. A meta log só é marcada converged quando todos os lados satisfazem seu critério e a estimativa final está abaixo da meta. UNASSESSED/None ou falha de faixa não é convertido em convergência.

As assinaturas, IDs e os oito campos de cada retorno coincidem com _service_result e a admissão de df482. Tipos, finitude, status, error_kind, method e evaluations são compatíveis. Erro local do serviço não cobre A/h, o backend, reconstrução, suporte/C ou erro físico. H1–H5, priors, 283/63, κdη comum, theta fixo e MM condicional não são alterados. Não há segunda álgebra gaussiana nem solver.

Foram comparadas duas alternativas reais já previstas: (1) primitiva log-CDF/erfc estável com tratamento próprio de diferenças estreitas e caudas; (2) quadratura positiva com localização analítica da quadrática, escolhida. A segunda evita depender agora de funções especiais externas qualificadas e mantém a interface. A primeira pode reduzir avaliações da janela, mas subtração ordinária de CDFs não a realiza de forma estável. Não há evidência de desempenho relativo obtida nesta revisão, nem fallback autorizado entre as alternativas.

Para o callback H5, uma API com escala/forma conhecida poderia orientar a amostragem de modo adicional; a API atual é opaca. A limitação já declarada não constitui defeito de conformidade nem razão para exigir certificado uniforme antes de produzir estimativas honestas ENGINEERING_ONLY. Metas mais estritas podem resultar em não convergência por arredondamento/orçamento; isso é resultado visível previsto, não autorização para ampliar recursos.

[OBSERVAÇÃO documental não bloqueante] O contrato descreve O(N log N) para a fila adaptativa. Cada recomposição _totals tem custo linear no número de folhas e pode ser invocada além do término, na reconfirmação do critério. Tratar aquela descrição como custo da organização/refinamento, não teto assintótico geral demonstrado de todos os caminhos. Isso não altera a correção das contagens de callback, e o pacote já não promete teto de tempo/RAM medido.

## Alcance final

Os pins Windows foram relidos localmente. Os pins Linux foram confrontados com o inventário arquivado; nenhum arquivo Linux foi novamente medido e nenhum WSL foi iniciado. A ressalva de fechamento transitivo não observado e a verificação futura do runtime carregado permanecem explícitas. Hashes declarados não autenticam, sozinhos, objetos Python arbitrários injetados.

[REAL — atividade do revisor] Leitura, hashes, AST e confronto algébrico/documental somente. Zero importações dos candidatos ou NumPy/SciPy, zero controles numéricos, integrais avaliadas, solver, observados, WSL, rede ou modelo remoto. Não foi criada AUTH/CLAIM; pacotes selados, memórias compartilhadas e ledger ficaram intactos. O aceite é estático e delimitado: não declara precisão atingida, não consome unidade e não substitui a decisão de ROOT.
