# Contrato dos dois serviços locais de precisão

[REAL — candidato preparado, não executado] Pedido f820203f-b83c-420a-87ec-7816f3179139. O consumidor é physical_prior.py do pacote df482, conferido pelo manifesto desta entrega. Nenhuma fonte anterior foi alterada.

## APIs preservadas

`log_exp_quad_interval(A,h,L,U, *, absolute_log_error_target,max_evaluations)`

Alvo: log integral[L,U] exp(hz−Az²/2)dz. Domínio: floats finitos após conversão de int/float Python, A>0, L<U e L≤0≤U. Bool e escalares de bibliotecas externas são recusados. A operação racional recentra o máximo dos números recebidos, sem exigir que o h residual da ancoragem anterior seja exatamente zero. Um resultado não representável é falha de faixa, nunca −inf por underflow.

Identidade do serviço: `f9.log_exp_quad_interval.scaled_simpson.v1`, exportada como LOG_SERVICE_ID. O orçamento exige pelo menos5 nós por lado não vazio (um ou dois), e no máximo1.000.000 pelo schema herdado. A contagem se refere a avaliações do integrando escalado; álgebra racional e localização finita da cauda não são chamadas ao solver/likelihood nem nós. O erro_estimate é erro absoluto ESTIMADO no log do alvo completo.

`positive_quad_1d(f, lower, upper, *, absolute_error_target,relative_error_target,max_evaluations)`

Exige lower=0 e upper=1 exatamente após a conversão admitida. Integra o callback positivo escalado H5, sem conhecer nem modificar sua transformação q=1/rd, seus Jacobianos, priors, covariâncias ou backend. Identidade: `f9.positive_quad_1d.adaptive_simpson.v1`, exportada como QUAD_SERVICE_ID. Exige pelo menos17 nós para a malha inicial de quatro painéis; orçamentos menores falham antes do callback. O teto é inteiro1..1.000.000, bool recusado.

O callback pode devolver zero em nós sob underflow, mas deve sempre devolver int/float Python finito não negativo. Todos os nós iniciais zero causam falha explícita. Exceções próprias do callback propagam sem alteração ou nova chamada. A contagem do retorno é exatamente o número de chamadas reais; cache não aumenta contagem. A área deve permanecer finita e positiva.

Metas são explícitas, positivas e finitas; não há default de tolerância ou campanha. Para a quadratura, o critério é a convenção max(absoluta,relativa×área), não a exigência simultânea de ambas. Para a janela, o erro logarítmico total estimado precisa satisfazer a meta, além da convergência estimada de cada lado.

## Recibo exato

Ambos retornam um dict com somente:

- service_id;
- status=`ENGINEERING_ESTIMATE`;
- log_value para a janela, ou value para a quadratura;
- error_estimate;
- error_kind;
- converged;
- evaluations;
- method.

error_kind é ESTIMATED_NOT_CERTIFIED com estimativa finita não negativa, ou UNASSESSED com None na janela quando o erro de log não puder ser avaliado de forma útil. Um valor sem convergência continua uma estimativa limitada; o código não o promove a certificado. method identifica escala/regra, término, painéis e, na janela, cortes/envoltórias de cauda. A chave method não contém nova autorização nem um protocolo estatístico.

`PrecisionServiceError` identifica code/detail e evaluations quando a contagem está disponível. Em falhas de validação/algebra sem contexto de contador, evaluations pode ser None: não se inventa contagem zero. Callback errors mantêm seu tipo original; o contador externo do df482 continua responsável pelo registro em uma execução abortada. Não há recibo parcial apresentado como retorno bem-sucedido após exceção.

## Injeção futura, sem execução nesta entrega

O chamador confiável verificará o SHA do módulo realmente carregado e declarará seus dois IDs nas referências services da admissão F9_PHYSICAL_PRIOR_PRECISION_V1. O mesmo arquivo fornece ambas as funções; o código não autentica a si mesmo ou objetos arbitrários. Um mapa com essas duas funções pode ser construído pelo chamador após sua admissão; nenhum exemplo executável ou launcher é criado aqui.

O recebimento de tolerâncias não significa que foram alcançadas. A saída mantém ENGINEERING_ONLY e o contrato original de priors/modelos. O serviço não altera physical_prior.py, não chama evaluate_five/assemble_five, não abre dados ou arquivos e não implementa outro backend gaussiano.

## Recursos e limitações

Simpson adaptativo conserva uma partição completa e valores de nós em cache. Cada refinamento acrescenta quatro avaliações. Tempo algorítmico da fila é O(N log N), memória O(N), além do custo real do callback; não são tetos de segundos/RAM medidos. O limite operacional pertence ao futuro executor. Nenhuma garantia de latência é deduzida desta análise estática.

math/heapq/fractions são dependências stdlib. Os metadados registram o runtime disponível e referências ao inventário já existente; isso não equivale a importar o candidato em Windows ou Linux nem a observar seus imports transitivos. O chamador futuro precisa verificar o runtime efetivo. Não foi instalado pacote ou alterada permissão.

A diferença entre regras é estimador, não resto certificado. Picos não amostrados do callback genérico permanecem possíveis; janelas conhecidas recebem localização geométrica explícita. Arredondamentos extremos, falhas do callback, orçamento insuficiente e resolução da malha têm saídas visíveis. Não há fallback automático para SciPy, log-CDF, outra quadratura ou novo solver.

A revisão estática posterior deve conferir: assinaturas/chaves/IDs contra o df482; recentralização e sinal dos lados; escala/cauda/log; positividade e cobertura; contagem/cache/limites; propagação de exceções; distinção erro estimado/certificado. Nenhum teste numérico ou campanha foi autorizado por este texto.
