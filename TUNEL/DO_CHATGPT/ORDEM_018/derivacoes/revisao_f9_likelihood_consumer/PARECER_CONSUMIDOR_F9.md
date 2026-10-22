# Revisão independente do consumidor puro F9

**[REAL — inspeção estática] Não identifiquei bloqueador material no escopo de chamador confiável declarado pela API.** O pacote pode seguir à decisão concreta de integração de engenharia da coordenação. Este parecer não autoriza execução, não libera observados e não certifica um resultado numérico.

Unidade revisada: `a9874f79-9d71-48f5-824c-d51d6d819534`. Rota consultada/registro prévio: `hubble.fase9_razao_discriminante`, seq. 559. Foram conferidos os 14 artefatos do manifesto, 23 declarações de pins de fontes (com repetições) e 34 caminhos únicos; 57 verificações locais de bytes/AST/metadados passaram. O manifesto inicial e final permaneceu idêntico, e sua cópia de bytes está nesta pasta. Os hashes completos estão no recibo e no manifesto da revisão.

## 1. Transporte efetivo de unidades, identidade e offsets

**[DERIVED — leitura de implementação]** `prepare_joint` implementa, nas linhas 280–315 de `likelihood_consumer.py`, a conversão:
\[
y'=Ty,\qquad C'=TCT^\top,\qquad o'=To,
\]
com T diagonal, fixado pela estrutura. A multiplicação de C é feita em suas duas dimensões; conserva também as covariâncias cruzadas fornecidas, sem construir silenciosamente uma matriz por blocos. X é montado dos coeficientes já transformados pelo produtor, e as médias recebidas também já estão nas unidades finais. Eles não recebem T de novo.

**[REAL — metadados]** Reconstruí exclusivamente a ordem de IDs, os nomes/unidades da base nuisance e o vetor de escalas a partir do layout estrutural e do desenho pinados. Coincidem com `IDENTIDADE_ESTRUTURAL_METADATA.json` e com os três hashes constantes do consumidor: 16 linhas de fundo + 267 locais, todas as 283 identidades únicas; 63 colunas eta distintas; sete fatores 5 (SN_HF, SBF_HF e cinco megamasers). Nenhum valor observado, matriz numérica, posto ou resposta do solver foi calculado.

O produtor, nas linhas 134–152 e 245–282 de `five_model_assembly.py`, multiplica por cinco os coeficientes X/a_h/c_C das mesmas famílias. O consumidor confere a projeção estrutural inteira contra a admissão externa e exige igualdade dessa estrutura em cada pacote. A conferência independente da origem dos coeficientes X/a_h/c_C pertence à admissão do chamador; os três hashes internos de identidade não devem ser apresentados como uma recompilação independente de todos esses coeficientes.

A convenção explícita é `NATIVE_EQUATION_Y_OFFSETS_ALREADY_INCLUDED`: y já contém, conforme a equação admitida, offsets como α+5 e m110−M110_table. O consumidor não aplica outro offset. Portanto a linha logarítmica com α+5 produz 5(α+5), não 5α+5. A API exige uma referência da compressão/offsets; não infere a redução de um catálogo nem decide que covariâncias ausentes sejam nulas.

## 2. Suporte afim comum e integral nuisance

**[DERIVED]** Para b=y'−μ, r=rank(C') e p=63, sob as hipóteses verificadas pelo backend, o fator retido é
\[
\int_{\mathbb R^{63}}L(b-X\eta)\,d\eta
=(2\pi)^{-(r-63)/2}
[\operatorname{pdet}(C')\,\det(X^\top C'^+X)]^{-1/2}
\exp[-\tfrac12\|\,(I-QQ^\top)Wb\,\|^2],
\]
onde W branqueia o suporte positivo de C' e Q vem da SVD de WX. Esta é a fórmula de `FlatNuisanceGaussian`: o código novo reutiliza a classe injetada e não duplica diagonalização, SVD, inversão ou solver.

A construção do backend conserva as condições: PSD/simetria dentro das tolerâncias fornecidas; X dentro do suporte; 63 colunas linearmente independentes após branqueamento; posto igual ao admitido. Antes de avaliar qualquer integral dos cinco modelos, o consumidor verifica μ_i−o' no suporte da mesma C'. Uma média com suporte afim diferente provoca `AFFINE_SUPPORT_CHANGED`. O ponto o é fixado e pinado externamente; não é escolhido no consumidor a partir de um ajuste ao y.

Nenhum desses postos/condicionamentos foi medido nesta revisão. O uso de limiares de ponto flutuante é explícito e corresponde ao comportamento de engenharia dos módulos existentes; não é um certificado de suporte exato. Não há jitter, troca de posto, reparo de matriz ou fallback acrescentado pelo consumidor.

O prefator de normalização é preservado e informado na saída. Omitir log κ é coerente somente porque a base eta, sua unidade, a dimensão e a medida comum κ dη são as mesmas. A saída é uma integral pontual sobre dη, não log Z: os priors dos parâmetros físicos são apenas transportados como metadados, sem multiplicação ou integração. `common_measure_id` identifica o acordo externo, não demonstra por si só sua validade.

A densidade está referida à medida euclidiana no suporte **transformado** fixo. Para comparar os cinco modelos nesse mesmo contexto, não falta um fator adicional det(T). Uma conversão para a densidade nas coordenadas nativas teria de usar o Jacobiano restrito ao suporte; a API não aplica incorretamente o determinante ambiente a uma covariância singular.

## 3. Coleção completa, falhas e densidade zero

Nas linhas 336–414, o consumidor exige exatamente os cinco modelos H1–H5 do produtor, o pacote de engenharia sem veredito, a estrutura comum e os pins de identidade/admissão. Prepara e verifica todas as médias antes da avaliação. Uma exceção de preparação, suporte ou integração aborta a chamada inteira; não retorna uma coleção parcial nem remove um rival.

Para um resíduo fora do suporte comum, o backend qualificado devolve −inf, que é preservado com o rótulo `ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT`. Dentro do suporte, o valor deve ser finito; −inf/não finito é erro. Não há conversão de exceções de engenharia em likelihood zero. Uma densidade zero assim rotulada não é um veredito físico; em particular, uma coleção com todos os modelos fora do suporte não permite transformar 0/0 em uma razão de evidências. A API não tenta fazê-lo.

A saída exige codificação externa explícita de −inf para JSON estrito. Isso já está documentado; o consumidor retorna um objeto Python e não promete ser seu próprio serializador, supervisor ou mecanismo de contenção.

## 4. MM, proveniência e fronteira de responsabilidade

O estatuto `CONDITIONAL_UNRATIFIED` dos megamasers permanece tanto na admissão quanto na saída. A fórmula gaussiana é aplicável ao experimento de trabalho com C fixo que vier a ser admitido; este código não transforma propagação baseada nos valores medidos em uma verdadeira lei condicional exata. Não ratifica C, a propagação MM, correlações ausentes ou coleta adicional.

O pacote mantém `UNBOUNDED_THEORY_ERROR`, `certified=False` e certificado numérico nulo. Isso é uma limitação explícita do resultado de engenharia, não um bloqueador artificial para preparar estimativas honestas. Não se calculam ajuste, evidência, p, sigma ou veredito.

O consumidor não abre arquivos para autenticar módulos. Ele recebe NumPy e `FlatNuisanceGaussian`, confere nome/módulo e um recibo pinado, e delega ao chamador confiável a conferência dos objetos realmente carregados. O contrato reconhece que nome e hash declarados não autenticam um objeto arbitrário. Do mesmo modo, referências chamadas “operator_release” e “V1” não constituem autorização por sua mera presença. Não identifiquei divergência entre esta fronteira de confiança documentada e a implementação; não exijo que o adaptador puro se torne um segundo executor ou sistema de autorização.

## 5. Alternativas e conclusão delimitada

As alternativas já documentadas foram confrontadas: reutilizar o backend qualificado com admissão externa explícita, como implementado; ou criar um solver paralelo, que duplicaria a matemática sem necessidade para esta unidade. Quanto à medida dos dados, manter o suporte transformado comum é coerente; trabalhar na medida nativa exigiria o Jacobiano restrito correspondente, uma escolha distinta que não cabe introduzir silenciosamente aqui.

**[REAL — atividade desta revisão]** Houve somente leitura de documentos/código, AST, hashes e projeção de IDs/unidades/escalas. Zero importações de candidato, NumPy ou backend; zero chamadas de solver, controles, dados observados, WSL ou modelo remoto; nenhuma autorização ou CLAIM criada. Dois erros dos auxiliares de leitura/AST do revisor foram corrigidos antes da gravação do recibo e estão discriminados nele; não foram execuções da unidade científica.

A falha terminal anterior de `ffd6ccba-cd70-4747-aceb-a10003dfb7f4` não foi repetida, contornada ou editada. O presente parecer trata somente deste consumidor independente. Não substitui a futura evidência de execução e não propõe campanha extra: prepara a decisão de ROOT sobre a integração concreta já em andamento.
