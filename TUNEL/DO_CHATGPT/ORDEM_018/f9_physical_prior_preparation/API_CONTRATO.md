# API candidata — médias dos priors extras em theta fixo

Pedido df482198-56c4-4169-ae5e-3908f5d12f2c. Preparação ENGINEERING_ONLY.
Nenhum módulo candidato/NumPy/SciPy/backend foi importado; nenhum exemplo, controle ou
chamada científica foi executado. Este texto não autoriza uso de dados ou execução.

## Entrada e reuso

integrate_at_fixed_theta(joint, assembly_json, *, assembly_sha256, background_json,
                        consumer_module, precision_json, precision_sha256, services)

joint é uma instância válida e inalterada de PreparedJoint do consumidor a987 pinado.
consumer_module é o módulo correspondente, carregado/verificado pelo chamador confiável.
A integração usa expressamente os campos privados _np, _engine, _y, _origin, _structure e
_admission_sha256 dessa versão; é um adaptador ACOPLADO AO PIN, não promessa de API privada
estável. Não editar o módulo antigo para acomodar esta preparação; uma mudança de fonte
exige revisar esse acoplamento. O reuso dos validadores privados _json/_keys/_reference/
_digest/_fraction evita uma segunda implementação do contrato de custódia.

assembly_json são os bytes do pacote das cinco médias, com SHA esperado independente.
A função chama joint.evaluate_five para reutilizar todas as verificações de família,
283/63, estrutura, unidades, suporte afim e normalização. Um erro dessa chamada aborta
toda integração; não se selecionam apenas modelos válidos.

background_json são os bytes do MESMO resultado de fundo previamente calculado, cujo SHA
deve coincidir com identity.background_packet_sha256 da montagem. A identidade completa
coincide com background_identity. theta confere tanto na identidade quanto no resultado e
nos cinco modelos. Não se chama assemble_five/CAMB/qualquer solver para mudar um extra.

Os priors/extras e suas coordenadas têm de ser os originais exatos do montador.
A função reconstrói somente os três eixos afins nas unidades de saída já transformadas.
H3 usa I_law e a_h; H4 c_C e delta(s); H5 as 13 médias BAO multiplicadas por rd_ref,
zero fora delas. Não recebe y/C brutos, não os abre e não reconstrói block-diagonal.
O contexto joint já é o único portador explícito dos valores futuros admitidos pelo chamador.

precision_json/precision_sha256 fixam a identidade das dependências, o hash da admissão
do contexto, o pacote de médias, serviços numéricos, referências externas e metas/tetos.
Não são certificados ou autorização. SOURCE_PINS foi gerado de bytes reais das cinco fontes
de implementação/resolução; nomes/hash declarados não autenticam objetos Python arbitrários.
O chamador deve verificar o código e runtime efetivamente carregados, o conteúdo dos
referenciais e a admissão científica, fora deste adaptador puro.

## Admissão de precisão

JSON estrito com schema F9_PHYSICAL_PRIOR_PRECISION_V1 e campos exatos:

- source_pins: SOURCE_PINS do módulo, sem alteração;
- consumer_admission_sha256: igual a joint._admission_sha256;
- assembly_sha256: igual ao argumento esperado do pacote;
- services: duas referências id+sha256, log_exp_quad_interval e positive_quad_1d;
- max_quadrature_evaluations e max_window_evaluations: inteiros 1..1.000.000, bool recusado;
- absolute_log_error_target, absolute_scaled_error_target, relative_scaled_error_target:
  números finitos positivos explicitamente escolhidos;
- caller_verification_reference: id+sha256 da conferência externa dos serviços carregados.

Não há defaults de tolerância, orçamento científico, escolha de pacote de precisão ou
instalação. O teto1.000.000 é apenas limite de schema; o orçamento FUTURO deve escolher um
valor concreto compatível com sua autorização. Esta entrega não o escolhe, não lança campanha
nem promete tempo operacional. Runtime/tempo/memória pertencem ao futuro contrato de execução.

## Serviços injetados

services é um dict exato de duas funções locais puras já verificadas externamente.

log_exp_quad_interval(A,h,L,U, *, absolute_log_error_target, max_evaluations)

Retorna log W, W=integral_L^U exp(h*z-A*z²/2)dz, usando o ALVO COMPLETO combinado.
A>0; L<U finitos, L<=0<=U; ancoragem no máximo restrito. Deve ser estável em caudas,
janelas curtas, A pequeno e endpoints normalizados que coalesceriam em float.
A forma completada e as alternativas de estabilidade estão em DERIVACAO.md.
Não basta usar Phi(U)-Phi(L) comum ou exp(h²/(2A)) isoladamente.
Se não consegue uma estimativa finita honesta, deve propagar falha, nunca -inf por underflow.

positive_quad_1d(f,0.0,1.0, *, absolute_error_target, relative_error_target, max_evaluations)

Integra a função positiva ESCALADA de H5. O callback contém a transformação q=1/rd,
todo Jacobiano normalizado, C completa e likelihood do backend. A função deve permanecer
dentro do intervalo e orçamento, não mudar o alvo, não acessar dados ou chamar solver/rede.
Sua contagem deve coincidir com o número real de chamadas ao callback contado no adaptador.
Pode usar um algoritmo de quadratura existente qualificado; a escolha não foi executada,
instalada ou presumida nesta preparação. Não há segunda quadratura oculta/nova campanha.

Um callback com erro fica marcado mesmo se a função de quadratura tentar capturar a exceção:
após retornar, o adaptador recusa seu resultado por QUADRATURE_CALLBACK_FAILED.
Nenhum retorno parcial é aceito por exceção e nenhum fallback/retry é disparado automaticamente.

## Recibo dos serviços e alcance da precisão

Os dois serviços retornam um dict com campos EXATOS:

service_id, status, log_value (janela) OU value (quadratura),
error_estimate, error_kind, converged, evaluations, method.

service_id casa com a referência admitida. status é ENGINEERING_ESTIMATE.
Valores devem ser Python int/float finitos (bool e escalares de outro tipo não são aceitos).
evaluations é int>=0; method uma string não vazia; converged é bool.
error_kind é ESTIMATED_NOT_CERTIFIED com error_estimate finito>=0, ou UNASSESSED com None.
Para janela, error_estimate é erro absoluto ESTIMADO do log da janela.
Para quadratura, é erro absoluto ESTIMADO da área escalada; a meta relativa também é passada.
Sem erro avaliado ou convergência, uma estimativa finita continua explicitamente limitada;
a API NÃO a promove a certificado nem afirma que a meta foi alcançada.

A implementação não verifica analiticamente o estimador interno dos serviços: isso pertence
à qualificação externa indicada pelos pins. As metas são solicitações, não garantias por
passagem de argumentos. Mesmo um erro local estimado pequeno não inclui arredondamentos
do backend/A/B/origens, reconstrução float do eixo BAO, nem erro uniforme teórico do fundo.
O campo precision_scope deixa essa separação explícita. ENGINEERING_ONLY com erro não
limitado é permitido; não se cria um bloqueio artificial de ciência por falta de certificado.

## Casos degenerados, caudas e falhas

Cada direção passa por residualize do backend e por verificações do suporte afim nos dois
extremos. A=0 só é plano quando o vetor projetado é inteiramente zero no cálculo; caso
contrário falha por underflow. Não se exige identificabilidade do extra para integrar um
prior próprio. Não se altera o requisito de posto dos 63 nuisance nem se adiciona jitter.

Sob o suporte comum admitido, um resíduo fora desse suporte tem densidade zero em toda a
família afim e pode devolver log integral=-inf com estatuto próprio. Isto continua condicionado
à geometria admitida; as conferências float do suporte não são certificado de nulidade exata.
Uma região perdida por falha, quadratura ou underflow nunca é esse caso. Precisão geométrica
perto da tolerância deve ser considerada pelo chamador, como já exigido pelo backend.

O retorno do serviço de janela deve ser finito para seu integral matematicamente positivo.
H5 exige área escalada>0: zero de quadratura gera QUADRATURE_ZERO_OR_UNDERFLOW.
Nós que underflowam são contados e rotulados; não são massa exatamente nula nem cota de erro.
A coleção completa só retorna ao final. Uma falha científica/engenharia aborta a função;
nenhum modelo, pedaço do prior ou cenário é removido ou renormalizado.

Não existe implementação automática da alternativa de quadratura direta beta/s/rd depois
de falha da analítica. Essa opção foi comparada documentalmente; uma escolha futura deve
ser explícita e respeitar a unidade/orçamento, sem transformar retry em comportamento oculto.

## Saída

F9_CONDITIONAL_PHYSICAL_PRIOR_RESULT_V1, ENGINEERING_ONLY:

- models: os cinco log_conditional_integral no theta fornecido, método e diagnósticos;
- H1/H2: valores pontuais sem extra, preservados do consumidor;
- H3/H4: janela analítica ancorada com densidades/Jacobianos completos;
- H5: quadratura positiva em q com q^-2, contagem e underflow de nós;
- geometry nos três rivais: A/B, referência e diagnósticos de suporte dos endpoints,
  sem tratar degenerescência float como certificado exato;
- base_theta_prior: density_exact="50/3", applied=False, integrated=False;
- prefator Gaussian/κ/medida de dados preservados; MM CONDITIONAL_UNRATIFIED;
- proveniência do consumidor, assembly, fundo e precisão; UNBOUNDED_THEORY_ERROR;
- absolute_evidence, theta_integrated_evidence, lnB, p, sigma e verdict em None.

São integrais CONDICIONAIS apenas. O theta base ainda requer integração posterior;
não denominar os retornos logZ ou Bayes factors. Nenhuma otimização ou mínimo global foi
feito. A fórmula de mínimo condicional está documentada para reutilização sem rotina nova:
em H4 B-lambda NÃO pertence ao mínimo da likelihood, somente ao integrando do prior.

Os resultados são objetos Python. Um -inf legítimo exige representação rotulada ao gravar
JSON estrito externamente; não usar NaN/Infinity literal nem disfarçar erro com null/zero.
Não há gravação nem abertura de caminho na implementação.

## Verificações futuras mínimas, sem campanha proposta

1. Revisão independente da derivação e correspondência do código aos três Jacobianos.
2. Conferência do carregamento das dependências e dos dois serviços de precisão injetados.
3. Na integração concreta já autorizada que vier a consumir o módulo, distinguir erro local
   do serviço de erro da geometria/fundo e preservar callback failures, suporte e a família.
4. Observar limitações nas caudas/janelas curtas, A=0/underflow e média BAO reconstruída,
   sem chamar conferência estática de teste numérico.

Não há novos casos/launcher, AUTH, CLAIM, runtime, comandos científicos ou solicitação de
campanha nesta entrega. Nenhum pacote consumido, modelo, prior, V1 ou memória foi alterado.
