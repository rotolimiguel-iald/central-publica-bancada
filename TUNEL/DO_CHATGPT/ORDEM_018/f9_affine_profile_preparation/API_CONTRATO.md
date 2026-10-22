# API dos perfis condicionais F9 — I05

Pedido 4eea0cfb-0a3e-4b38-abcd-37bddbf5bbe3. [REAL — preparado, não executado]. Este adaptador acrescenta a operação de perfil, reutilizando as duas dependências existentes a987/df482; não cria outra camada de solver.

## Entrada

`profile_at_fixed_theta(joint, assembly_json, *, assembly_sha256, background_json, consumer_module, physical_prior_module, caller_verification_reference)`

- joint: o PreparedJoint já admitido, com C/X/y/origem fixos. A API não o constrói nem abre dados.
- assembly_json: bytes da montagem H1–H5, com hash esperado assembly_sha256.
- background_json: bytes do MESMO fundo, cujo hash/identidade/θ constam da montagem. Não recalculado.
- consumer_module: módulo a987 verificado e carregado pelo chamador.
- physical_prior_module: módulo df482 verificado e carregado pelo chamador; fornece _Curve, peak, mean, log_likelihood e limites.
- caller_verification_reference: objeto {id,sha256} de uma verificação externa dos objetos/dependências carregados. Estrutura/pins são conferidos; a referência não autentica sozinha objetos Python arbitrários nem autoriza observados.

A fonte exata de ambas as dependências e do backend está em SOURCE_PINS, preenchido por script a partir dos bytes efetivamente lidos. A API acopla-se aos campos privados pinados de PreparedJoint e _Curve; não presume que qualquer versão futura terá os mesmos internals. Não lê caminhos nem tenta importar dependências por nome.

O consumidor existente confere família completa, estrutura, identidade, médias/suporte e normalização. O adaptador confere θ comum dentro da caixa original, fundo/identidade, coordenadas, priors exatos como metadados e referências dentro dos domínios dos extras. O uso de qualquer prior como penalização ou peso de perfil é proibido pelo alvo e não implementado.

## Saída

Objeto Python `F9_CONDITIONAL_AFFINE_PROFILE_RESULT_V1`, ENGINEERING_ONLY, com os cinco modelos completos. H1/H2 retornam seu valor pontual, q_feasible_estimate e parâmetros originais; H3/H4/H5 retornam perfil condicional factível, geometria A/B e intervalo, parâmetros físicos, candidato/coordenada efetivamente avaliada e deslocamento de ida e volta.

q_feasible_estimate é a norma quadrática projetada no ponto, não um certificado global. log_profile_deta mantém todos os fatores do backend na mesma medida e omite somente logκ comum, como a origem. Os ramos são:

- CONDITIONAL_FEASIBLE_PROFILE_ESTIMATE: vértice restrito calculado, ponto físico factível avaliado; não é mínimo certificado.
- FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY: direção projetada calculada zero; referência usada e intervalo inteiro rotulado. Não afirma degenerescência científica exata.
- ZERO_DENSITY_ON_COMMON_AFFINE_SUPPORT_COMPLEMENT nos extras, ou o status pontual equivalente de H1/H2: log −inf legítimo, q e parâmetros factíveis indisponíveis. Não inferir rejeição ou fabricar mínimo infinito a partir desse diagnóstico.

Cada modelo tem campos separados:

`certificates.conditional_minimum = {status:UNAVAILABLE, lower:None, upper:None, certificate:None, verified:False}`

`certificates.global_theta_minimum = {status:NOT_SEARCHED, estimate:None, lower:None, upper:None, certificate:None, verified:False}`

Essa API não aceita certificados e não implementa verificador. Um consumidor futuro pode relacionar certificados externos verificados ao mesmo cenário/θ/pins/alvo, em estrutura própria, sem substituir essas estimativas por limites só por mudança de rótulo. A interface documental de certificados é uma dependência consultada, não uma autorização implementada.

measure, output_measure, common_measure_id, normalization e certification são preservados do consumidor. MM_status continua CONDITIONAL_UNRATIFIED. global_minima, relative_evidence, lnB, p, sigma e verdict continuam None. global_theta_search_performed e physical_extra_priors_applied são False.

## Falhas, recursos e limites

Falhas de admissão, JSON/hash, suporte, domínio, tipo, overflow/underflow relevante ou backend propagam como exceções. A coleção só retorna ao concluir os cinco modelos. Não há fallback, retry, ajuste de tolerância, omissão de rival/linha/cenário ou captura que devolva −inf por falha.

A API tem trabalho finito por chamada e nenhuma busca iterativa: evaluate_five é chamado uma vez; criam-se três _Curve; cada extra não plano e em suporte chama log_likelihood uma vez. H1/H2 e ramos planos reutilizam seus logs pontuais. A avaliação de q usa residualize do mesmo backend. Não há chamada CAMB nem nova fatoração de C/X. Custo real e precisão não foram medidos aqui; uma futura execução precisa preservar os limites do executor.

Na devolução ao parâmetro físico, o adaptador avalia a curva na coordenada obtida por recomposição do parâmetro retornado. Endpoints físicos permanecem os originais, não uma caixa ajustada. A reconstrução BAO, coeficientes e inversas são float e não possuem enclosure de arredondamento. q_feasible_estimate não é U certificado; ausência de erro uniforme não impede uma estimativa de engenharia explicitamente rotulada.

−inf é representação Python do zero legítimo de densidade; não é número JSON estrito. O gravador externo deve serializá-lo com rótulo preservado, nunca trocar por zero finito ou permitir NaN como se fosse JSON interoperável. Este módulo não grava resultados.

## Verificação desta entrega

prepare_static.py confere o pedido/fontes, preenche pins por bytes, analisa AST sem importar candidatos e verifica a assinatura, import único math, chamada a _Curve/peak sem prior e ausência de solver/otimizador/importação dinâmica. O manifesto congela código, derivação, contrato e recibo estático. Nada disso mede precisão numérica, autentica a natureza do modelo ou move gate. Revisão independente continua necessária antes de eventual consumo.
