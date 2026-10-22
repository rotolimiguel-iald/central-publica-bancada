# API — integração externa do prior theta inteiro

Unidade de **preparação** ad02511d-1536-4a1b-a6c4-fb3e5eb26550. [REAL] Código escrito e examinado por AST/metadados; não importado ou executado. Nenhuma AUTH, CLAIM, unidade de execução, observação ou campanha foi criada.

## Entrada

`ThetaIntegrator(plan_json, *, plan_sha256, evaluate_node)`, seguida de **uma** chamada `run()`. `diagnostics()` apenas expõe estado, contagens, nó ativo e eventual falha. A instância é terminal depois de sucesso ou erro. Ela não faz I/O.

O plano JSON pinado tem campos exatos:

- `schema="F9_THETA_INTEGRATION_PLAN_V1"`, `preparation_request_id`, `execution_unit_id`;
- `source_pins` igual à constante do módulo;
- `consumer_admission_sha256`, `assembly_admission_sha256`, `engine_configuration_sha256`, `common_measure_id`;
- `callback_reference` e `controller_reference`, cada uma `{id,sha256}`;
- `first_level`, `last_level`, `max_callback_calls`;
- `absolute_log_refinement_target`.

O futuro execution_unit_id deve ser diferente da identidade desta preparação e ter decisão própria verificada pelo controlador. O schema exige pelo menos dois níveis consecutivos, 1≤first_level<last_level≤6. Exige teto inteiro explícito de callbacks entre1 e300000, suficiente para **todos** os (2^last_level+1)^3 nós da grade mais fina antes da primeira chamada. Esses tetos são limites de schema, não orçamento concedido nem sugestão de campanha. Não há valores de nível/teto/metas escolhidos nesta entrega.

A meta de diferença absoluta entre logs é positiva, finita e explícita. Ela não determina uma parada precoce. O módulo executará todos os níveis do plano, se uma execução vier a ser autorizada; o atendimento da meta é apenas um indicador ao final, não certificado de erro da integral.

O plano é a admissão externa do contexto. Ele não contém y, C, centros ou dados observados. O hash da admissão do consumidor deve permanecer o mesmo em todos os nós. O chamador verifica os objetos efetivamente carregados, os referenciais, a liberação dos dados quando cabível e a autorização concreta. Pins/nomes declarados não substituem essa verificação.

## Callback conjunto e reaproveitamento do fundo

`evaluate_node(descriptor)` recebe um descritor com:

- execution_unit_id, consumer_admission_sha256, callback_reference, assembly_admission_sha256, engine_configuration_sha256;
- dyadic_numerators (três inteiros), dyadic_denominator (potência de2 reduzida);
- node_id: SHA256 do objeto canônico formado pelos sete campos acima, antes de acrescentar theta;
- theta na ordem [H0,ombh2,omch2], theta_names e five_models.

O descritor usa a fração diádica canônica comum às três coordenadas. O mesmo nó em níveis distintos tem a mesma chave e é avaliado uma única vez. Nos extremos, theta usa diretamente o limite original; no interior aplica a transformação afim da caixa. A ordem é lexicográfica de itertools.product.

O callback deve:

1. Consultar/reservar duravelmente a identidade da unidade+nó **antes** de chamar qualquer execução externa/local científica. Recusar nó falho, pendente ou de resultado incerto; uma nova instância/processo não autoriza repetição. Persistir a identidade e os recibos reais fora deste módulo puro.
2. Obter um único fundo compartilhado para aquele theta, por nova execução própria ou cache durável verificado e construir os cinco modelos com as fontes/admissões já previstas. Consumir df482 (`integrate_at_fixed_theta`) e seus serviços numéricos próprios. Não recalcular CAMB para β/s/r_d, nem por rival.
3. Preservar o objeto completo retornado por df482 e fornecer seu recibo. Não remover modelo, cenário ou região do prior por falha; não repetir automaticamente uma chamada incerta.

O retorno tem exatamente `{"conditional_result": result, "receipt": receipt}`. O result é o objeto nativo completo da API df482, sem alterar seu schema. A preparação f820 dos serviços de precisão é da gerente e não é duplicada aqui.

O receipt possui exatamente node_id, execution_unit_id, callback_reference, conditional_result_reference, background_execution_reference, background_attempts, background_successes, background_origin, background_calls_this_callback, assembly_admission_sha256 e engine_configuration_sha256. As duas referências são {id,sha256}. As contagens do recibo ORIGINAL de fundo devem ser1/1. background_origin distingue NEW_EXECUTION (uma chamada nova) de VERIFIED_DURABLE_CACHE (zero chamadas novas), com igualdade obrigatória em background_calls_this_callback. O cache deve conferir theta, configuração, runtime, física, redshifts/precisão e custódia da execução original, sem mudar sua identidade. Essa é uma obrigação do callback e uma conferência de recibo; o integrador **não instrumenta o solver** nem afirma medir essas chamadas independentemente. As contagens de entrada/retorno ao próprio callback são observadas de fato.

`conditional_result_reference.sha256` é definido por `canonical_conditional_sha256(result)`: JSON UTF8, sort_keys/ensure_ascii, separadores compactos, sem newline; −inf só no campo models/<modelo>/log_conditional_integral é substituído pelo objeto {"$float":"-inf"}. Nenhum outro número não finito é aceito. O objeto original df482 não é modificado. O limite de4MiB se aplica ao transporte canônico gerado, não é uma promessa de limite físico de memória durante a construção de objetos Python.

O integrador valida theta, a família exata de cinco modelos, priors extras já integrados e prior base ainda não aplicado, a linhagem df482, a admissão comum, a normalização e estatutos. Um pacote de fundo com o mesmo hash não pode reaparecer sob outro theta. O reaproveitamento entre níveis ocorre apenas pelo cache interno de um retorno completo já validado, sem chamar o callback.

## Regra, normalização e custo

Para L, n=2^L intervalos por eixo; i=0..n. O peso1D é a_i/(3n), a_i=1 nos extremos,4 nos índices ímpares,2 nos pares interiores. O peso3D é o produto, sempre positivo. As regras usam a caixa inteira; não há corte em ±sigma, região escolhida por melhor ajuste ou renormalização após falha.

A caixa original [50,90]×[0,015;0,030]×[0,08;0,18] tem Jacobiano3/50, exatamente cancelado pela densidade50/3 do prior uniforme nas coordenadas originais. Portanto a integral do callback sobre o cubo unitário já inclui o prior base normalizado: não multiplicar por50/3 novamente.

Os cinco somatórios usam os mesmos nós e pesos e log-sum-exp. O custo científico é N=(2^last_level+1)^3 callbacks únicos completos; nós mais grossos estão contidos na grade final. O custo do callback (incluindo a integração dos extras) não foi medido aqui. O cache é O(5N) valores, além de chaves/overhead Python. A redução usa memória temporária O(N) por modelo. Tempo, RAM e recolhimento devem ser limitados pelo futuro controlador; este módulo puro não promete prazo/limite de SO.

## Falhas, zeros e ausência de convergência

A chave é marcada como tentada antes da entrada no callback. Exceção, interrupção ou falha de validação encerra a instância em FAILED_TERMINAL, conserva contagens/nó ativo e não retorna uma família parcial. A função não tenta novamente. A garantia entre processos depende do controlador/callback durável; a memória da instância não é um ledger persistente.

−inf só é aceito com o estatuto de densidade zero no complemento do suporte comum vindo de df482/a987. Falha de engenharia, overflow ou underflow não é convertido em zero.

Se um nível tiver apenas zeros amostrados para um modelo, registra NO_POSITIVE_SAMPLED_MASS e continua os níveis já fixados da caixa inteira. Se isso persistir na grade final para algum dos cinco modelos, a chamada falha sem evidência parcial: valores nulos nos nós não provam integral global nula. Isso também evita transformar 0/0 numa razão. Não há nova cota científica exigida pelo algoritmo; o objeto não medido permanece dito.

A saída retém todos os níveis, gaps finais de log, fração do maior nó ponderado, fração da soma nos nós de fronteira, maior valor amostrado e hashes de localização. Esses diagnósticos tornam visível concentração/resolução pobre. Termos perdidos por underflow do somatório e nós underflow dos serviços internos são contados; não são uma cota de massa perdida.

A regra por produtos pode perder um pico estreito entre nós, mesmo quando dois níveis parecem concordar. Não há limite para essa massa não resolvida nesta preparação. Portanto indicator_satisfied não significa convergência global, e global_convergence/unresolved_peak_mass_bound permanecem nulos. Metas/erros do callback e do fundo continuam separados dos gaps exteriores.

## Saída e alcance

O retorno F9_THETA_RELATIVE_INTEGRATION_RESULT_V1 é ENGINEERING_ONLY e contém:

- log_relative_evidence_without_common_log_kappa para os cinco modelos;
- lnB_against_H2_same_context, como diferença dos cinco somatórios na MESMA medida;
- prior original/Jacobiano, todos os níveis, diagnósticos de resolução e contagens reais de callback;
- normalização comum, cadeia de hashes dos descritores/resultados/recibos completos e referências;
- MM CONDITIONAL_UNRATIFIED e UNBOUNDED_THEORY_ERROR.

A integração é relativa à mesma medida κdη. Os prefatores do consumidor já presentes no callback são conservados. A constante comum κ é omitida; absolute_evidence fica nula. p, sigma e verdict também ficam nulos: razão de evidências não é estatística frequentista nem confirmação física.

Uma saída finita com indicador de resolução insuficiente continua identificada como estimativa limitada, sem proclamar tolerância alcançada ou disparar aumento de níveis. Toda alteração futura de método/plano é uma decisão explícita, não retry automático. Preservados c435 consumida, ffd6 terminal e a unidade f820 separada.

## Acoplamento concreto à configuração global — esclarecimento ROOT

O consumidor a987 fixa prediction_admission_sha256; esse campo identifica a admissão estrutural do montador (assembly_admission_sha256 nesta camada). A admissão do montador fixa engine_configuration_sha256 e runtime_sha256, que o pacote de fundo deve reproduzir. Portanto não basta reutilizar literalmente a admissão/configuração pontual consumida por c435 em uma integral com múltiplos theta.

ANTES de qualquer callback, o futuro controlador deverá materializar e pinçar a configuração GLOBAL de toda a grade finita escolhida, incluindo pontos theta e IDs determinísticos, e uma admissão de montagem comum. O consumidor terá admissão comum vinculada a ela. A API atual prediction_worker seleciona point_id em config['points']; essa rota admite uma lista global finita sem mudar o motor. Isso não autoriza usar o launcher antigo dos cinco controles: esse launcher tem orçamento/identidade próprios já consumidos.

O plano exterior exige os hashes de admissão da montagem e da configuração global; cada descritor e recibo repete os mesmos hashes. Esta camada confere sua igualdade, mas não abre/gera a configuração: o controlador verifica o conteúdo, a cobertura completa e a cadeia consumer→assembly→configuration. Nenhuma configuração, lista de pontos ou campanha foi gerada nesta preparação.

Um fundo durável já validado pode servir ao mesmo theta em cenários distintos que compartilhem exatamente a configuração/física/runtime relevantes. A admissão de consumidor, C e cenário continua própria e fixa para cada integral; não se reusa uma likelihood entre cenários só porque o fundo coincide. O recibo distingue reutilização validada de chamada nova, e jamais interpreta os cinco modelos como cinco CAMB.
