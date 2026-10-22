# Guarda de suporte singular — protótipo sintético para F1

[REAL computacional / DERIVED condicional] 18 controles sintéticos passaram sob PROTOCOL_V1.json congelado antes da execução. Nenhuma matriz da rede H0DN foi montada, nenhum catálogo foi aberto por estes scripts e nenhum ajuste ou veredito científico foi realizado.

A revisão documental seq399 mostrou que C pode ser semidefinida. O protótipo calcula autovalores/autovetores, explicita posto e núcleo, verifica ||N^T r|| antes de aceitar a densidade e usa apenas o subespaço positivo para chi2 e pseudo-determinante. Não acrescenta jitter nem inventa variância nos vínculos determinísticos.

O contraexemplo independente é C=[[1,1],[1,1]]: resíduos (1,1) e (2,0) têm o mesmo custo da pseudoinversa; somente o primeiro pertence ao suporte. A guarda rejeita o segundo. Foram também conferidas razões de likelihood contra a medição elementar, transformação redundante não ortogonal, invariância por rotação, covariância indefinida/assimétrica/não finita e o caso determinístico de variância zero. Uma convolução escalar com prior gaussiano próprio testa a normalização; isso não implementa as evidências das cinco hipóteses sob priors uniformes.

Os cortes 1e-12 relativo nos autovalores e 1e-10 no residual do núcleo são INPUTs do contrato de exemplos adimensionais. Não são tolerâncias qualificadas para H0DN. Antes do uso em dados reais, padronização/unidades, espectro, limiar de posto e suporte precisam de contrato próprio e validação. Um autovalor pequeno descartado é uma escolha numérica registrada, não prova de vínculo físico exato.

As densidades são relativas à medida euclidiana no suporte. Duplicar/reescalar dados pode mudar a normalização absoluta; as razões conferidas aqui usam o mesmo espaço de observações e os mesmos vínculos. Densidades em suportes de dimensões diferentes não podem ser divididas e apresentadas como Bayes factor sem medida comum. O helper com prior gaussiano pode ampliar o suporte e deixa esse limite explícito.

Alternativas do protocolo: eliminar redundâncias em medidas elementares; ou manter as equações redundantes com suporte explícito. Os dois caminhos concordam nos controles de razões. O programa não contém carregador de dados reais, otimizador ou conexão a provedor. É preparação de instrumento, ainda sem revisão independente externa da implementação e sem incorporação ao V1 ratificado.

Arquivos: singular_gaussian.py, verify_support.py, PROTOCOL_V1.json, PROTOCOL_FREEZE.json e RESULT.json. O resultado inclui ambiente, custo medido e hashes dos scripts. A análise H0DN original e seus arquivos permaneceram intocados.
