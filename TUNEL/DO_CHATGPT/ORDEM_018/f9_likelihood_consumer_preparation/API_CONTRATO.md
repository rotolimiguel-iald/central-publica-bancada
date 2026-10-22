# API do consumidor F9 — preparação, sem execução

Pedido persistente: a9874f79-9d71-48f5-824c-d51d6d819534, ORDEM018 F1(c).
[REAL — engenharia documental] Código e verificações AST/bytes nesta pasta.
[OPEN] Revisão independente, integração numérica futura, admissão de dados, validade científica
da covariância/modelo e qualquer decisão do operador. Zero importações do candidato/numpy/backend,
zero leituras de centros, zero controles e zero campanhas nesta entrega.

## Alternativas e reaproveitamento

A alternativa A, escolhida antes da implementação, é um adaptador puro com a classe
FlatNuisanceGaussian e numpy injetadas pelo chamador. B seria escrever/copiar outro solucionador
gaussiano; rejeitada porque a implementação com suporte/normalização já existe e tem recibos.
C seria carregar catálogos automaticamente; excederia a unidade. O registro anterior está em
ALTERNATIVAS_ANTES_IMPLEMENTACAO.json.

linear_gaussian.py e singular_gaussian_v2.py são dependências externas preservadas, com pins
em PIN_FONTES.json e SOURCE_PINS. Nenhuma fórmula de inversa, autodecomposição, SVD, projeção,
Schur, densidade gaussiana ou normalização foi reimplementada. O contexto invoca a classe
qualificada uma vez para C e X fixos e usa support.evaluate e log_integral. Os recibos históricos
de 16 e 37 controles são evidência limitada desses módulos; não são testes deste adaptador,
da dimensão 283, de dados observados ou de uma instalação futura. Não há consumidor equivalente
283/63 nas fontes locais pesquisadas; a montagem revisada gera médias e desenho, sem consumir y/C.

## Fronteira da interface e admissão

A API é para um chamador confiável no mesmo processo. Não é sandbox, verificador de assinatura,
autoridade científica ou mecanismo de autorização. Nomes Python e hashes em recibos não
autenticam sozinhos objetos arbitrários. Antes de chamar, o coordenador deve verificar fora da
API os bytes realmente carregados de numpy/backend, a relação do recibo com esses objetos,
a procedência do pacote de médias, a admissão da estrutura e o conteúdo dos referenciais.
A API não lê esses referenciais por caminho nem fabrica certificados a partir de flags.

A admissão fixa explicitamente a identidade do cenário, hashes dos quatro insumos, estrutura,
rank esperado, tolerâncias nas unidades pertinentes, medida comum e referência à admissão do
montador. Ela é fornecida em bytes com hash esperado independente. A API confere a coerência
dessas ligações em memória. Isso não prova que a covariância representa a natureza, que uma
leitura observada foi autorizada ou que a normalização da compressão é válida.

O pacote não oferece admissão preenchida com dados simulados como se fossem reais. O contrato
CONTRATO_API.json descreve os campos, sem ser uma autorização. Um uso futuro com observações
exige data_kind=OPERATOR_RELEASED_OBSERVATIONS e referências operator_release e V1, além da
liberação externa efetiva. Strings com esses nomes não concedem liberação. MM continua
CONDITIONAL_UNRATIFIED em toda saída; nenhuma observação é aberta nesta preparação.

## Funções

extract_structure(assembly_json: bytes, *, assembly_sha256: str) -> bytes

Extrai apenas row_ids, row_units, native_to_output_row_scale, nuisance e response_columns,
conferindo o schema e a estrutura básica. A ordem dos 283 IDs, as 63 colunas e as sete posições de escala cinco também são ligadas por hashes canônicos derivados exclusivamente dos metadados do layout/desenho pinados (IDENTIDADE_ESTRUTURAL_METADATA.json). Retorna JSON canônico: UTF-8, ensure_ascii=True,
sort_keys=True, separators=(',', ':'), allow_nan=False, sem newline. A projeção estrutural
não admite a si mesma: o coordenador deve conferir a correspondência ao desenho/layout
pinados e congelar seu hash em admission.structure_sha256 antes do uso. O helper não chama
backend/numpy e não calcula médias. Não foi chamado nesta unidade.

prepare_joint(y, C, row_ids, *, affine_origin_native, structure_json,
              admission_json, admission_sha256, backend_receipt_json,
              numpy_module, flat_gaussian_class) -> PreparedJoint

As quatro entradas de valores são explícitas. y e affine_origin_native têm shape (283,),
C tem (283,283). Cada matriz/vetor aceita somente bytes brutos float64 little-endian, C-order,
de tamanho exato, ou ndarray exato float64 de shape correto (subclasses/array-like são recusados).
Cópias locais são canonizadas como <f8/C-order e tornadas somente leitura. Não há abertura de
NPZ/HDF5/pickle, strings de caminhos, arquivos ou rede. Todos os valores devem ser finitos.
row_ids aceita lista/tupla de 283 strings únicas ou seus bytes JSON. Sua hash é do JSON canônico
da lista; hashes das matrizes são dos bytes <f8/C-order, sem header. A admissão inclui os hashes
nativos; o resultado carrega também a hash de C transformada.

structure_json contém a projeção exata do montador, admitida e pinada. X_sparse_rows já está
nas unidades de saída; a API o densifica, preservando a ordem das 63 colunas e exigindo strings
racionais canônicas de até 64 caracteres. Estrutura e respostas não são reconstruídas a partir
de arquivos científicos. O hash da admissão protege a projeção; o chamador deve verificá-la
independentemente contra as fontes listadas.

numpy_module é o módulo previamente carregado e verificado pelo chamador.
flat_gaussian_class é exatamente a classe qualificada, não um novo algoritmo.
backend_receipt_json tem schema F9_QUALIFIED_BACKEND_CALLER_RECEIPT_V1, pins dos dois módulos,
runtime_reference, class_module/class_name e caller_verification_reference.
Seu hash esperado está na admissão. A conferência de metadados Python não substitui a
verificação externa dos objetos carregados.

O construtor chama FlatNuisanceGaussian(C_out,X_out,**tolerances) sem selecionar defaults;
confere n=283, p=63 e rank observado pelo backend igual ao rank admitido. O backend preserva
seus próprios requisitos: C sem indefinição além do limiar explícito, X no suporte, posto
completo de X branqueado, normalização finita. Não há jitter, pseudoposto alternativo, remoção
de linhas/colunas, adaptação de tolerância ou fallback. O pequeno teste de simetria e a
simetrização do backend já pertencem ao seu contrato existente; não foram alterados aqui.

PreparedJoint.evaluate_five(assembly_json: bytes, *, assembly_sha256: str) -> dict

O hash esperado vem do chamador, que deve verificar a proveniência do pacote de assemble_five.
Exige exatamente os cinco modelos H1_TGL, H2_LCDM, H3_beta_free, H4_Cepheid, H5_rd_free;
verifica identidade/admissão upstream, os pins e a igualdade canônica de toda a estrutura fixa.
Não recalcula os modelos, β, rdrag, priors ou qualquer resultado do motor cosmológico. Cada
mean_without_nuisance tem 283 números finitos já na unidade final. Metadados de parâmetros/prior
são preservados e rotulados como não aplicados; não se somam log-priors nem se integra o espaço
de parâmetros físicos. Hash/proveniência e revisão externa do montador são a fronteira dessa
delegação, e não uma segunda validação de suas fórmulas.

Primeiro são validados os cinco deslocamentos mu−origin_out, usando support.evaluate, para
garantir a classe afim fixa admitida sob a tolerância explícita. Depois calcula-se b=y_out−mu,
preservando os mesmos C/X/rank/medida em todos os modelos e reutilizando log_integral(b).
Qualquer erro aborta a chamada inteira, sem devolver coleção parcial nem retirar um modelo.

## Unidades, offsets e covariância inteira

T é diagonal: 16 linhas CMB/BAO dimensionless, 267 locais na unidade alvo mag. Exatamente
sete linhas locais log10 são multiplicadas por cinco; as demais têm escala um. A operação
efetiva é y_out=T y_native, C_out=T C_native T^t, origin_out=T origin_native. Entradas da
covariância têm produto das unidades nativas correspondentes; blocos cruzados são transformados
também. Não se monta block_diag nem se presume independência a partir da ausência de uma fonte.
Toda hipótese de blocos cruzados precisa constar do referencial covariance_and_cross_blocks.

X, a_h, c_C e mean_without_nuisance vêm JÁ transformados pelo montador. Multiplicá-los
novamente por cinco seria erro. O consumidor usa X e mean diretamente; a_h/c_C são preservados
na identidade estrutural para impedir mudança oculta, sem remontar a média.

y_native é a equação canônica já reduzida, não o campo bruto de catálogo. Preserva, por exemplo:
host/distância e restrição de grupo; magnitude SN calibradora; SBF m110−M110_table;
interceptos SN/SBF α+5; e a variável log10 MM conforme contrato candidato. O consumidor
não soma +5 outra vez, não restaura M110_table, não redefine a transformação MM nem usa o sinal
para escolher redução. Assim, uma linha α+5 vira 5(α+5), e não 5α+5. q0/j0 e demais convenções
fixas da redução não são recalculadas por modelo. A referência compression_and_offsets deve
cobrir resíduos/normalização da compressão e evitar repetir ancoragens já presentes em C.

Há 283 linhas (16+267), não a seleção 262 de outra preparação. As 63 coordenadas η em mag
(59 distâncias de hosts, duas de grupos, M_B e M110_offset) mantêm a mesma ordem e medida.
A API não elimina as cinco linhas MM nem ratifica seu tratamento estatístico.

## Suporte afim e falhas

O chamador fornece uma origem afim nativa, fixada por identidade/admissão antes das comparações.
Ela não é estimada de y por esta API, nem alterada por modelo/θ para fazer um resíduo caber.
A diferença de cada média para a origem deve pertencer ao suporte linear comum de C.
Design fora do suporte, posto inadequado ou média em outra classe afim são falhas de contrato;
nenhuma delas recebe likelihood zero ou implica rejeição física.

Um b legitimamente fora do suporte afim comum é diferente: support.evaluate fornece o
diagnóstico e log_integral retorna −inf exatamente como definido no backend. Nesse caso,
a saída do modelo mantém ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT, null_residual_norm,
support_tolerance, rank/nullity e log_integral_deta=-inf. Isso é densidade matemática zero
na medida fixada, não certificado de rejeição; não usar tolerância para regularizar o resultado.
A existência de zero requer cuidado posterior com razões 0/0 ou integrais globalmente nulas;
nenhuma comparação/evidência é feita aqui.

Erro de JSON/pin/schema/shape, NaN/Inf na entrada, overflow da transformação, covariância,
posto, suporte de desenho, normalização ou exceção do backend gera ConsumerError (com causa
encadeada) ou falha de processo visível. Nunca retorna -inf por except, nunca engole o erro,
nunca tenta outro solver. A saída é apenas construída após todos os cinco modelos passarem
as verificações de família e suporte. Failure codes estão no contrato máquina.

## Normalização e medida

A classe reutilizada fornece, ponto a ponto nos parâmetros físicos, o logaritmo de
(2π)^(-(r−63)/2) [pdet(C_out) det(X_out^t C_out^+ X_out)]^(-1/2)
exp(−b^t P b/2), com P definido pelo solucionador existente. Todos esses fatores ficam
na saída do backend, sem declarar prefatores cancelados. Não é um segundo cálculo dessa
expressão no adaptador. O multiplicador comum κ de κ dη é omitido e identificado como tal.
Não é evidência Bayesiana absoluta; integrar priors próprios dos parâmetros físicos ou
comparar evidências exige procedimento separado e suas condições.

A densidade é relativa à medida euclidiana NO SUPORTE TRANSFORMADO e à mesma medida dη.
A transformação singular usa pdet(C_out); não se aplica det(T) ambiente como correção
universal. Converter a densidade ao sistema nativo exige Jacobiano restrito ao suporte,
fora desta API. Apenas com T, classe afim, C/X/posto e medidas comuns fixos podem fatores
comuns cancelar em comparações apropriadas. Mudança do cenário, C, desenho, rank ou medida
exige nova admissão/contexto e revisão de comparabilidade; não é permitida silenciosamente
dentro desta instância.

A implementação é float64 de engenharia e mantém UNBOUNDED_THEORY_ERROR do montador.
Não produz envelope intervalar, cota uniforme, certificado numérico/físico, g/S, p, sigma,
lnB, ajuste, veredito nem cobertura MM. Mesmo uma avaliação futura bem-sucedida não faria
essas conversões automaticamente.

## Saída e serialização

Resultado F9_POINTWISE_FLAT_CONSUMER_RESULT_V1, ENGINEERING_ONLY: cinco log_integral_deta
ponto a ponto, diagnósticos de suporte, parâmetros e prior_metadata_not_applied;
normalization preserva rank, eta_dimension=63 e log_prefactor, common_log_kappa_omitted=True.
provenance vincula admissão, assembly, fontes e covariância transformada. Campos absolute_evidence,
lnB, p, sigma, fit e verdict permanecem None.

O resultado é um objeto Python; o -inf legítimo é float negativo infinito. JSON estrito não
o representa. Um gravador externo deve convertê-lo explicitamente para uma representação
rotulada (por exemplo string "-inf" acompanhada do status), preservando o diagnóstico.
Não usar allow_nan para fingir JSON interoperável e não trocar -inf por zero finito ou null
sem estatuto. A API não grava/serializa saídas e não determina caminhos.

## Limites honestos e próximos passos

A verificação desta entrega é leitura/AST/hash/metadados. Não houve import, chamada a
extract_structure, prepare_joint ou evaluate_five, densificação, transformação numérica,
autodecomposição, SVD, likelihood, solver/WSL/rede, centro observado ou controle sintético.
Os hooks de admissão externa não demonstram que existe hoje uma admissão de observações.
Não há autorização, CLAIM, launcher ou campanha nesta pasta.

Revisão independente do código/contrato e decisão ROOT permanecem antes de qualquer consumo.
O chamador futuro deve preservar as restrições do operador/V1, MM condicional e a distinção
entre preparação, execução e certificação. Não alterar os pacotes congelados nem repetir
unidades terminais como consequência desta implementação.
