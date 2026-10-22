# Ligação I05→I06 — API e acoplamento futuro

[INPUT] Preparação local somente. Não constitui revisão independente, autorização, CLAIM ou execução. Módulos e fontes selados permanecem intactos.

## API concreta

`Bridge(modules=..., object_verifier=..., object_verifier_sha256=..., semantic_verifier=None, semantic_verifier_sha256=None, semantic_scope=EXTERNAL_SCIENTIFIC_CONDITIONAL, deadline=..., clock=...)`.

Os quatro objetos são os módulos profile, theta, tail e reducer referenciados em SOURCES.json. O validador de objetos deve conferir os objetos realmente carregados e seus imports/closure sob um loader confiável; comparar apenas atributos ou SOURCE_PINS não satisfaz esse dever. Seu recibo tem tipo Receipt, papel LOADED_OBJECTS e hash do payload/pins. A ponte verifica identidade do recibo, não prova que um verificador arbitrário é honesto. O ambiente de testes injeta doubles explicitamente sintéticos.

`estimate_family(records, contexts=..., level=..., max_records=...)` consome um iterador ordenado: cenário, chave canônica do nó, bytes profile_json, SHA esperado do perfil, SHA esperado da assembly e SHA esperado do background. Os hashes esperados devem vir dos recibos do DurableStore já autenticados pelo carregador, não da própria carga solta. Não chama perfil/CAMB/solver/callback; aproveita o resultado já produzido por `profile_at_fixed_theta` dentro de I02. Usa somente `theta._node_key` e `theta._theta` pinados para conferir o plano e coordenadas.

Preserva os 600 rótulos exatos, ordem e cinco modelos, sem deduplicação; conserva domínio original fechado em θ e extras. Para nível l, exige 600×(2^l+1)^3 perfis; l=1 corresponde a16.200 registros, l=2 a75.000. São contagens derivadas do plano, não orçamento autorizado ou tempo/memória medidos. Nenhum nível é selecionado automaticamente. Mínimos sobre esses pontos são candidatos/estimativas; não há alegação de cobertura contínua, convergência global ou U certificado. Um perfil fora do suporte pode ficar sem testemunha finita; falhas desconhecidas não viram zeros ou infinito.

`reduce_certificates(contexts=..., certificates=..., materials_by_scenario=..., opening=None, opening_materials=None)` é o chamador produtivo da cauda por teste/cenário e do redutor uma única vez. Não recebe estimativas como certificados. Sem opening, exige ausência de certificados e mantém a saída fechada. Uma admissão futura exige bytes de prova e verificador semântico externo que confira decisão real, ratificação, suporte e a identidade dos contextos. Não basta passar os quatro booleanos.

## Formatos mínimos

Contexts: dicionário na ordem exata de SCENARIOS, cada valor com data_sha256, covariance_sha256, X_response_sha256, support_sha256, engine_config_sha256 e consumer_admission_sha256.

Cada cenário: `models` com as cinco identidades completas (valores null ou certificado), e `hypotheses` com os cinco testes (null ou hipóteses). Certificado de mínimo: binding, lower/upper racionais exatos opcionais, error_status e proof. Binding inclui modelo, cenário, contratos numérico/modelo/domínio/família e todos os campos de Contexts. A prova material precisa existir por SHA em materials_by_scenario. O verificador semântico valida o alcance no domínio completo, testemunha factível, proveniência e erros; a ponte apenas verifica vínculos e aritmética de composição.

Hipóteses: binding específico do teste com nulo e competidor completos, degree, support, domination, degree_proof e inclusion. LAW exige prova material de H1⊂H3; outros testes exigem inclusion=null. Graus até148 são um teto do consumidor existente, não graduação presumida. A adequação do grau (148/17/18 quando aplicável) e a lei amostral pertencem à prova externa.

Receipt: role, payload_sha256, evidence_sha256 (tupla ordenada), verifier_sha256 e scope. Para ciência, exige EXTERNAL_SCIENTIFIC_CONDITIONAL. O modo SYNTHETIC_CONTROL_ONLY é separado na construção: retorna somente synthetic_decision e jamais scientific_decision. Um booleano ou assinatura de forma não é prova científica. Falta de material/verificador/erro limitado retorna indisponibilidade; colisão de identidade, prova adulterada ou recibo inválido falha visivelmente.

Papéis do verificador externo: OPENING_AND_ADMISSIONS; MINIMUM_BOUNDS; STATISTICAL_HYPOTHESES. O limiar é conferido internamente por threshold_audit.py, implementação separada com Fractions, Taylor/Machin/isqrt e comparações racionais. Confronta todos os booleanos, estados, completudes, direções e decisões combinadas do redutor; números p/log/exp da proposta float não são certificados. Divergência ou cruzamento do intervalo de alpha mantém os bounds/calibração e deixa a decisão indisponível. A saída científica separada contém apenas racionais exatos, booleanos e estados condicionais.

## Ponto de acoplamento futuro

O controller d72 cria NodeContext com profile_enabled e I02 persiste profile_json separado do envelope theta (node_adapter.py, bloco após cálculo condicional). Um sucessor explicitamente revisto do integrador/supervisor poderá fornecer o iterador ordenado a partir desses mesmos registros autenticados, após encerramento/recibos válidos. Esta entrega não altera d72 nem o relança. Não repete perfil/solver para recuperar um artefato ausente.

Para cálculos certificados, a mesma execução futura precisa de produtor/verificador científico real de L/U e hipóteses. Os módulos atuais não o fornecem: a ponte permite conectá-lo sem substituir por flags. Sem prova de erro uniforme, valores computacionais continuam estimativas. O ramo analítico de não negatividade admite somente L=0 e U=null, ainda condicionado às hipóteses verificadas, nunca inventa testemunha superior.

Nenhuma ligação usa a ordem histórica invertida da tabela F4. O mapa explícito está em frozen_contract.TEST_MODELS, derivado do contrato V2 e conferido com a fórmula dos cinco modelos.
