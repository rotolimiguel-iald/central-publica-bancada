# API candidata da covariância conjunta F9

[REAL — preparação estática] Unidade I03, request `f200dee1-0ecf-4a51-9b38-4c32d7eb0696`. O módulo `joint_covariance.py` foi escrito e analisado como texto/AST. Não foi importado, instanciado ou executado. Não há C conjunta calculada nesta entrega.

[INPUT CONDICIONAL] O01/MM e O02/família/correlações continuam não ratificados. O módulo implementa a proposta de experimento gaussiano de trabalho, não demonstra que erros publicados são a covariância verdadeira. Não concede abertura de dados, execução ou V1.

## Entradas e saída

`JointCovarianceBuilder(metadata_json, numpy_module=..., block_correlation=..., runtime_receipt_json=..., runtime_receipt_sha256=...)` recebe bytes explícitos da metadata pinada e objetos já carregados por controlador autorizado. O construtor só verifica metadata. Não importa NumPy, módulos de bancada, catálogos, arquivos, solver ou classes gaussianas. Os únicos imports declarados no módulo são hashlib/json/math/Fraction.

A callable injetada é `block_correlation(keys, groups, scenario)`, de `covariance_support/qualify_stellar_family.py`, já usada na qualificação histórica. O controlador deve conferir o arquivo e a identidade da callable carregada, inclusive seu global `np` apontar ao NumPy indicado; deve evitar `main()`. Nome, módulo e recibo não autenticam um objeto Python hostil. O módulo é uma API de composição entre componentes confiáveis, não sandbox.

O recibo de ligação contém exatamente:
- schema = F9_COVARIANCE_PRIMITIVE_BINDING_V1;
- primitive_source_sha256, primitive_name = block_correlation, primitive_module;
- runtime_reference e loaded_callable_and_numpy_global_reference.

Uma referência tem exatamente `artifact_sha256` (64 hex minúsculos), `clause` (localizador textual) e `status` entre INPUT_CONDITIONAL, SYNTHETIC_FIXTURE ou REVIEWED_IMPLEMENTATION. É proveniência declarada pelo chamador; a existência e o conteúdo científico do artefato não são verificados por leitura implícita.

`family_metadata()` devolve cópia defensiva dos 600 rótulos pinados. A ordem é cenário de sinais da fonte → tupla da grade da fonte → receita SBF da fonte. Cada rótulo contém ambos os nomes SBF: o nome do preflight e o correspondente do resolutor. Não são 600 amostras independentes nem um prior sobre cenários.

`build_case(label, common_blocks=..., cross_blocks=..., stellar=..., sbf=..., mm=..., bindings=...)` devolve:
- C_native: array f64 little-endian 283×283, cópia própria marcada sem escrita;
- row_ids: os 283 IDs exatamente na ordem pinada;
- record: hash dos bytes de C, proveniência dos componentes, identidade das respostas, vínculos de suporte/normalização e estatuto ENGINEERING_ONLY_UNQUALIFIED_COVARIANCE.

O chamador pode tecnicamente desfazer a flag de escrita: deve conservar os pins. A proteção de array é disciplina de composição, não isolamento contra código hostil.

## Coordenadas e blocos

Nove blocos, nesta ordem: PLANCK (3), DESI (13), STELLAR (178), GROUP (13), SN_CAL (55), SBF_CAL (14), SN_HF (1), SBF_HF (1), MM (5). Total 283. O domínio mantém 63 nuisances e cinco MM.

C_native usa coordenadas nativas: 16 linhas de fundo dimensionless, primeiras 260 locais mag e últimas sete locais dex. Cada entrada cruzada tem produto das unidades de suas linhas. O campo coordinates de qualquer bloco deve ser NATIVE_F9_283. O transporte pelo fator5 pertence exclusivamente ao consumidor a987: `y'=Ty; C'=TCTᵀ; o'=To`. X e médias da montagem das cinco hipóteses já estão nas coordenadas finais. Não aplicar T duas vezes, nem deslocamentos fixos novamente.

common_blocks exige exatamente PLANCK, DESI, GROUP, SN_CAL, SBF_CAL, SN_HF. Cada bloco é uma matriz inteira explícita, não reconstruída a partir de um centro, de um σ agregado de H0 ou de uma independência presumida. SN_HF tem variância dex².

Cada registro de matriz tem exatamente values, row_ids, column_ids, coordinates, values_f64le_sha256, reference, zero_policy. Shape e bytes convertidos a f64 são verificados. values_f64le_sha256 é hash do array C-contiguous little-endian após conversão, não hash do arquivo textual de origem; esse arquivo fica na referência. Diagonais dos blocos diagonais devem ser positivas. Simetria e PSD numéricas completas ficam para o guard existente; o builder não introduz tolerância própria, clipping, jitter ou média da matriz.

cross_blocks contém **todos os 36 pares superiores** A|B em ordem BLOCKS, com IDs dos dois eixos. Nenhum par pode faltar. Para uma matriz inteiramente zero, zero_policy deve ser EXPLICIT_INPUT_ZERO; caso contrário EXPLICIT_MATRIX. Os números zero têm de ser fornecidos: não basta deixar um campo ausente. Sua referência deve explicitar a hipótese/receita. A parte inferior é preenchida como transposta do mesmo bloco, não como outra hipótese. PSD de blocos separados não prova PSD conjunta com cross-blocos.

## Estelar: reutilização e orçamento de erro

stellar tem exatamente sigma_by_primitive, sigma_f64le_sha256, reference, D0_policy, D0_reference.

sigma_by_primitive possui mapas completos anchor, MAS e HMS com chaves exatas da metadata; os σ são finitos e positivos, em mag, explicitamente fornecidos. Seus três hashes correspondem à ordem das chaves pinadas e aos vetores f64 little-endian. A referência deve vincular os valores ao orçamento admitido; o módulo não baixa nem abre ERROR_COMPONENTS.

D0_policy deve ser EXPLICIT_ZERO_BASELINE_RECIPE, com referência própria. É a escolha explícita da construção qualificada, não a conclusão de que um erro desconhecido é zero. Orçamento D0 extra ou termos cruzados latentes MAS–HMS requerem receita distinta, fora desta candidata; não são adicionados por conveniência.

Incidências A/B/H reutilizam o grafo MAS/HMS/âncoras de ESPECIFICACAO_LINEAR. Zeros e uns de incidência expressam a topologia, não independência inferida de observações. A parte variável reutiliza quatro chamadas à primitiva pinada block_correlation. A aritmética adicional implementa a montagem documentada:
`Cstar=(A*a)(A*a)ᵀ+(B*m)Rm(B*m)ᵀ+(H*h)Rh(H*h)ᵀ`.
Nenhum segundo solver é implementado.

Os 14 keys MAS da fonte incluem entradas sem incidência ativa; os 104 HMS e quatro âncoras conservam sua ordem fonte. Isso não conflita com a contagem de 11 MAS ativos no desenho. A metadata mantém os rótulos de todos os casos, inclusive coincidências no ponto de frações zero.

## SBF e MM

sbf tem recipe_id, variance_dex2, variance_reference, compression_reference. recipe_id deve coincidir com o rótulo:
- SBF_UPSTREAM_M_ONLY → UPSTREAM_M_ONLY;
- SBF_INDEPENDENT_M_ADDITION_CONDITIONAL → INDEPENDENT_M_ADDITION_CONDITIONAL.

A variância do intercepto é entrada explícita positiva. O módulo não recalcula as médias ou o GLS, não importa o qualifier de fluxo e não reexecuta controles consumidos. A referência pode apontar o recibo FLOW existente e sua receita. Se a receita mudar os pesos, pode mudar **o intercepto observado comprimido e suas cross-covariâncias**; o controlador deve vincular y, offsets e compressão correspondentes ao mesmo rótulo. Usar a nova variância com o intercepto da outra receita sem justificativa é uma lacuna, não resolvida pelo builder. A API conserva compression_reference tanto no caso quanto na receita.

mm implementa apenas a alternativa A_UPSTREAM_FIXED_ERROR_WORKING_GAUSSIAN proposta no contrato MM. Campos: recipe=H0DN_MM_DZ_UPSTREAM_SYMMETRIC, rows (cinco em ordem), dependence_policy=EXPLICIT_DIAGONAL_WORKING_INPUT, dependence_reference e reference_endogeneity_reference. Cada row exige row_id, variance_dex2 positiva, distance_reference_mpc, velocity_reference_km_s, U_reference_km_s positivos, fixed_reference e variance_recipe_reference.

O builder não deriva D_ref de H0(theta), não substitui a propagação upstream pelo Jacobiano cosmográfico completo, não abre referências e não calcula a variância a partir de centros. Recebe a variância já admitida e o vínculo de sua receita. Os três valores de referência positivos documentam a escala, mas o teste de positividade não prova U(v), o prior do estimador ou a lei condicional: isso é responsabilidade científica externa explicitada no contrato. Não são fornecidos valores para eles nesta entrega.

Sob A, a diagonal5×5 é formada com as cinco variâncias fornecidas; off-diagonais MM são zeros **declarados** pela dependence_policy. Os oito cross-blocos MM–resto ainda precisam existir como matrizes explicitamente zero, com referência; o código recusa valores não zero neste recorte. Dependência MM diferente ou lei primitiva B deve produzir OPEN_MODEL_COMPONENT, não uma extensão silenciosa da alternativa A.

Falta de MM, de qualquer bloco, referência ou receita não permite excluir linha, reduzir dimensão ou usar variância zero. Top-level None em build_case gera CovarianceError(OPEN_MODEL_COMPONENT); omissão/schema inválido gera falha visível. `open_record(label, missing_components=[...], bindings=...)` permite representar explicitamente o caso inteiro indisponível, com C=null, sem numerar uma pseudomedição.

## Vínculos e família inteira

bindings tem exatamente:
- family_common_input_sha256: manifesto comum previamente fixado pelo chamador;
- five_model_response_sha256: identidade do desenho/receita das cinco respostas, **não hash de uma média em um theta escolhido**;
- consumer_structure_sha256: bytes estruturais completos aceitos pelo consumidor;
- fixed_affine_support_reference, normalization_recipe_reference;
- common_measure_id: mesma coordenada e constante κ dη em R63;
- model_and_O01_O02_reference: cláusulas condicionais, não licença de abertura;
- compression_reference: identificação do processamento/offsets.

Os IDs/eta/T da metadata são os mesmos da montagem revisada. O builder não modifica X, respostas, origem afim, médias ou offsets. As referências de suporte e normalização ainda não são recibos numéricos: actual_rank, support_receipt e normalization_receipt ficam null.

`summarize_family(records)` exige exatamente 600 registros na ordem pinada e verifica seus hashes, identidade, SBF correto e invariâncias. Ela vincula a lista completa ao hash do mapa; um subconjunto ou duplicação não completa a família. Também recalcula o hash dos componentes e das invariâncias, em vez de confiar no campo declarado. Blocos comuns, σ estelares, MM e cross-blocos sem SBF_HF devem ser os mesmos. Para cada uma das duas receitas SBF, variância/compressão/cross-blocos de SBF_HF devem ser os mesmos nos 300 rótulos estelares. Isso fixa a família parametrizada agora; correlações cruzadas com dependência adicional nos quatro parâmetros requerem outra receita explícita, não aceita por esta API.

Sem casos abertos, a saída é ALL_600_ASSEMBLED_UNQUALIFIED_ENGINEERING_ONLY. Havendo qualquer aberto, COMPLETE_LABEL_MAP_WITH_OPEN_COMPONENTS. Nenhum dos estados significa matriz verdadeira conhecida, suporte qualificado ou V1 ratificado. Os registros completos são fontes confiáveis produzidas pelo builder e preservadas por hash; summarize_family audita vínculos/identidade, não recalcula C a partir de todos os números nem autentica afirmações físicas.

## Continuidade com a implementação revisada

O controlador futuro deve conferir os pins e admitir componentes/receitas; ligar os bytes nativos de C ao input_sha256.C_native_f64le do consumidor; carregar o desenho comum; e qualificar C'/X com SupportGaussian/FlatNuisanceGaussian, tolerâncias explícitas e referências de suporte afim/origem. O backend já distingue erro de engenharia/modelo de residual legitimamente fora do suporte, que pode ter densidade zero. Esta candidata não converte falhas em log−inf.

Posto real, orientação do suporte, informação das respostas e prefator dependem da C conjunta inteira. A fórmula relativa mantém pdet(C') e det(X'ᵀ C'⁺ X') e a mesma medida κdη. O número estrutural148 é limite condicional, não posto/ν medido desta saída. Não cancelar normalizações entre cenários diferentes por terem os mesmos IDs. Não calcular p, g, S, lnB, sigma ou ajuste neste builder.

A futura qualificação deve cobrir somente a ligação nova: montagem, cross-blocos explícitos, transporte único e identidade dos 600 rótulos. Os antigos controles consumidos não foram repetidos e seus escopos não são estendidos por esta documentação. A preparação não agenda campanha, não contém launcher, AUTH ou CLAIM.
