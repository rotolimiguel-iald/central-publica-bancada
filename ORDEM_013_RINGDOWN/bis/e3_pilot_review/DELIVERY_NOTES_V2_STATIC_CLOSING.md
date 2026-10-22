# Fechamento estático — emissores de entrega v2

**DN-R1–R3 fechados no escopo de emissão a partir de evidências efetivamente aprovadas por R e pelos revisores dos resultados.** Nenhum novo bloqueante neste delta. Hashes das duas fontes no JSON ao lado. Somente leitura de código, comparação com o parecer anterior, AST e hashes; nenhum emissor, fixture ou cálculo executado. Não aprova drafts ainda inexistentes nem substitui revisão dos adapters/E6/E7 reais.

- **DN-R1:** o emissor B4/TEST agora percorre E3.2, E3.3 e TEST; confere igualdade de `stage`, registro, resultado da etapa e predecessor entre adapter/review, além de bindings/timeline/hash do artefato. Confere links E3.2→E3.3→TEST, datas individuais de emissão/revisão, orçamento ativo e E2 nas fontes de parede. TEST exige 180 linhas e conjunto exato 3×10×6, métricas nulas, gate vermelho, razão física nula e AWAITING_DATA.
- **DN-R2:** B5 vincula status/recibo de execução à autorização, hashes e tamanhos dos dois produtos, registro/orçamento e E6/review. Confere posterior/autorização do consumidor, duas etapas sem erro com rc zero e reap direto, ordem autorização→início→fim e término anterior ao menor limite global/reserva. Campos físicos de topo e de cada linha nulos; grades E6/E7 por chaves exatas e quantidade. Preflight inclui `.pending`.
- **DN-R3:** os dois parsers recusam chaves duplicadas, constantes não finitas e overflow numérico por `parse_float` com `isfinite`. A conclusão é estática, sem nova campanha de negativas.

Correções editoriais presentes: **33 produtos de calibração**, sem chamar cada produto de catálogo; negativa histórica ampla marcada **[DECLARADO pelo principal]**. Mantidas as distinções entre calibração pública e teste cego, condicionais e significância física, parede do instrumento e impossibilidade geral.

## Limite exato deste fechamento

O emissor B4/TEST **não recalcula toda a cronologia das fontes**: confere emissão≤revisão≤agora e os links, mas não percorre por si os horários efetivos de cada `timeline`, o piso de ativação E2 e a ordenação temporal entre atividades. Também inspeciona diretamente a grade TEST, não novamente toda a grade E3.3. Essa cobertura continua nos reviews reais de R que ele agora vincula exatamente, conforme a alternativa admitida em DN-R1. Portanto não descrever o emissor isolado como verificador integral da cronologia/matriz de calibração. A revisão independente do E6 real também verificará esse encadeamento; não foi antecipada aqui.

Publicação permanece exclusiva por arquivo e **não atômica entre arquivos**. Falha após a ficha pode deixar entrega parcial: preservar, registrar a falha e não fazer retry cego nem anunciar entrega completa sem todos os documentos/manifesto. Essa limitação conhecida não é ocultada pelo fechamento estático.

As aprovações de resultados consumidas por B5 devem ser os pareceres independentes reais e seus hashes exatos, não os pareceres de preparação de código. SHA fixa os bytes; não autentica sozinho a identidade do revisor nem comprova física ou a ausência global de operações externas.
