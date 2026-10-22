# v388: auditoria documental da mudança científica

[REAL — bytes, texto e metadados, 06/10/2026] A identidade local da v388 está coerente nas referências examinadas: programa, selo, resultado, proof manifest, pedra Lean e sete artefatos documentais da Fase9 escalar. Foram54 conferências, todas satisfeitas, sobre22 fontes, estáveis no início/fim desta auditoria. A comparação textual com o backup v387 encontrou13 blocos de delta. Não executei um.py, Lean, experimentos, função de veredito, solver ou import científico; não abri arrays/catálogos observados. Canônicos, Atlas, mapa MCP e memórias não foram alterados.

A auditoria sustenta atualizar a identificação documental para o artefato verificado. Não demonstra qual versão está implantada em cada aplicação, nem ratifica qual especificação científica governa a Fase9. Essas ações são distintas.

## Consistência e cadeia de evidência

O programa atual mede33.801.035 bytes e SHA256 e64b00f4df75059b6f6fa5c050d45032ae73cb0e4aea6ef88a3620cc85846739. O backup anterior mede33.751.540 bytes e coincide com o SHA do programa no selo v387. Os hashes atuais de programa, resultado e proof manifest coincidem com o selo v388. O campo result_hash é o identificador semântico result_hash_before_external_comparison; não deve ser confundido com o SHA de todos os bytes do JSON.

O hash agregado formal foi reconstruído somente do mapa de1215 hashes registrado, conforme a concatenação ordenada de caminho relativo e SHA documentada em um.py134584–134615. Conferi por bytes a nova pedra, TheWholeIsOne e os metadados lean-toolchain/lakefile/lake-manifest. Isso não é rehash fresco dos1215 arquivos nem recompilação.

A pedra embutida como literal no programa coincide byte a byte com TGLExt/TheCouplingRunsBoundedBelow.lean em disco e com seu pin formal. São17 declarações: duas definições e quinze teoremas, não dezessete teoremas novos. Cada nome consta no axiom_report com somente propext, Classical.choice e Quot.sound; as17 flags correspondentes estão verdadeiras no resultado. O total6154/6154, build e selftest aprovados são evidência dos relatórios/logs existentes, não uma compilação feita por esta auditoria. O handoff declara compilação em sandbox novo; não reconstruí esse ambiente.

O gate mantém a mesma string da v387; todos os booleanos comuns de topo do selo também são iguais. α e β do core permanecem exatamente os mesmos valores serializados. No resumo Coma, distância e veredito não mudam; o prediction_hash muda. Essa diferença de hash foi registrada, sem reconstruir sua pré-imagem nem promovê-la a nova previsão científica.

## β(χ): o enunciado e suas hipóteses

[KERNEL, conforme fonte e evidência de compilação existentes] A pedra define α(χ)=1/cosh(χ/2) e β(χ)=α(χ) exp(1/2). Demonstra positividade, limite superior e antitonia estrita para χ≥0. O teorema do piso exige **0≤χ≤χsup** e conclui β(χsup)≤β(χ), com igualdade somente em χ=χsup. O piso é relativo a esse extremo finito; a pedra não fixa χsup nem o identifica numericamente com a fronteira Thomson. No semieixo não limitado, a forma positiva tende a zero, portanto estas declarações isoladas não fornecem um piso positivo universal de0,01203.

A distinção entre objetos importa: αOfChi(0)=1 e βOfChi(0)=exp(1/2), ao passo que β0 físico do runtime usa αThomson√e. O próprio runtime193914–193920 diz que não são o mesmo ponto/objeto e classifica a identificação física por INPUT/ONTO. A identidade com couplingOfAlpha requer adicionalmente αOfChi(χ)<exp(−1/2); é uma igualdade por desdobramento, não uma nova determinação do valor físico.

As somas parciais de metades ficam abaixo de1 e tendem a1; o ponto fixo x=1−x é1/2. A validade desses teoremas não transforma a leitura ontológica ou a escolha física de escala em prova experimental.

[INPUT/ONTO, KNOWN na origem, OPEN] O runtime incorpora inversos de α(MZ)128,95 e127,95 e os valores de β correspondentes. Seu próprio metadado diz que o rótulo on-shell não constava na fonte de um laço e que a entrada MS-bar de literatura não foi conferida em disco. Não fiz validação bibliográfica ou cálculo novo. Qual μ cada rito deve usar continua OPEN. **Nenhum contrato congelado passa automaticamente de β0 para β(μ)** pela atualização de versão.

## Fase9 escalar: resultado incorporado e errata

[REAL — integridade do relato; estatísticas não recalculadas] A v388 incorpora a abertura do V1 escalar com cinco leitores-resumo: SH0ES R22, CCHP, SBF, masers e TDCOSMO. Os sete arquivos pinados — resultado JSON/Markdown, poder, runner, recibo anterior, V1 e recálculo ao lado — conferem. Recalculei apenas os hashes canônicos da especificação e do texto da função; não executei essa função.

Essa análise é distinta do candidato Codex de283 componentes/63 nuisances e covariância conjunta. Sua incorporação ao programa não conclui a implementação, qualificação ou decisão do composto283. O handoff preserva explicitamente a pendência sobre qual especificação governa.

O resultado escalar permanece **INCONCLUSIVE_SYSTEMATICS** porque os cinco leitores estão DECLARADO quanto às fontes primárias por hash. A string contrafactual NOT_FALSIFIED_POWERED é obtida na origem ao supor zero leitores declarados; não substitui aquisição, verificação de fonte ou veredito real.

Valores aqui são cópia documental identificada: H0 de fundo68,531, previsão74,274, zδ≈−1,424 e zdisc≈4,284. O lnB(TGL/ΛCDM) é9,16674. O resultado congelado traz lnB(TGL/βlivre)=2,24060947 com discrepância n25→n35 de0,29851752; a correção ao lado, já presente no core, registra n200=1,9692166174194288. **2,24 é o valor congelado, não o valor convergido relatado na errata.** Não alterei nem recalculei nenhum deles. O selo/handoff resumem o valor antigo, logo o adendo deve acompanhar qualquer apresentação da precisão.

Pela leitura do runner133–171, a likelihood usa S=C+s²ffᵀ, marginalização gaussiana do fundo e logdet(S); zdisc usa a raiz assinada da diferença apenas dos termos quadráticos. A origem registra a variante com logdet4,28176126 ao lado de4,28373561. Esses números pertencem àquele modelo e não são, por sua identificação isolada, um p global calibrado do novo contrato F9. A diferença entre perfil e marginalização já aparece no texto da v388 e deve continuar visível. A alternativa de fundo livre mantém rd livre no BAO e não é uma análise completa de física precoce.

## Incorporação à pesquisa sem trocar o objeto

Alternativa documental imediata: atualizar versão/pins e adicionar os enunciados/estatutos acima, preservando todos os contratos congelados e os resultados históricos. É compatível com esta auditoria.

Alternativa científica posterior: escolher explicitamente qual experimento e qual leitura de β governa, com suas hipóteses, covariâncias, medidas e função de decisão. Isso exige decisão própria antes de mudar os contratos; esta auditoria não executa nem autoriza essa alternativa.

O novo piso formal e a leitura escalar da Fase9 não reabrem INIT003/P3, não substituem a qualificação de recuperação sintética e não contornam a recusa d72. NOT_FALSIFIED permanece distinto de CONFIRMED. Nenhum gate foi movido por esta auditoria.

Os pins completos, referências de linha, comparações, hipóteses e limitações estão em AUDITORIA_CIENTIFICA_V388.json; ESTABILIDADE_FONTES.json registra a conferência final. Não foi usado o MCP de mapa, cujo envio anterior de metadados está bloqueado por revisão automática.
