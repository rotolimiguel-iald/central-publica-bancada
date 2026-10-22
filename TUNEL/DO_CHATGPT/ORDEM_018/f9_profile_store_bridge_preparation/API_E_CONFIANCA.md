# API concreta de recuperação I02 → estimativas V2

[INPUT] Preparação somente. Não autoriza executar d72, ler observado, importar módulos científicos, consumir unidade, produzir decisão científica ou executar esta suíte. Os originais permanecem intactos. O registro/mapa/memórias pertence à ROOT.

## Entrada pública

`Recovery(intake_raw, intake_sha256, registry, reader_bindings, stores, protected_roots, metadata, external_evidence, bridge_module, registry_module, deadline, clock)` — todos os argumentos são nomeados. `estimate()` é a única publicação final. Não há CLI executável: `__main__` recusa.

O intake é um contrato proposto de leitura, não AUTH/ROOT_DECISION nem recibo já produzido. Seu hash esperado vem da admissão externa confiável. O chamador não deve escolher esse hash a partir da mesma carga que deseja admitir. A implementação confere bytes e vínculos; não autentica a identidade humana que admitiu o intake. A origem e a verificação independente da admissão são fronteira explícita de confiança.

`registry` é LoadedRegistry já existente do **processo leitor**. `registry_module` é o módulo original confiável que construiu esse objeto; a classe não é recarregada. `reader_bindings` vincula papel → caminho efetivamente carregado, bytes e SHA. Todos os papéis exigidos estão no código, incluindo store_contract. RegistryVerifier chama o método de classe retido `LoadedRegistry.check(deep=True)`, sem usar override de instância, confronta os objetos da ponte e emite Receipt(LOADED_OBJECTS,…,LOADED_OBJECTS_ONLY) somente após a conferência. Não se afirma que os objetos do produtor encerrado ainda estão vivos. O registro histórico deles permanece no stdout/recibo de produção.

O loader existente executa bytes pinados e retém identidades de funções/classes/code; o check profundo confere fontes e mapas nativos amostrados. Não prova integridade universal de globals, defaults, closures, conteúdo nativo, syscalls ou processo hostil de mesmo UID. O próprio bootstrap confiável, o registry_module e sua política devem ser os objetos efetivos já admitidos; comparar caminho/hash sozinho não demonstra isso. O carregamento que os estabeleceu é responsabilidade externa, sem um falso verificador autodeclarado.

`stores` contém somente DurableStore existentes de nodes/runs. `protected_roots` contém ProtectedDirectory existentes de unit/nodes/runs, com paths e (device,inode,uid,mode) admitidos. StoreView expõe lookup somente e chama o método de classe pinado. DurableStore.lookup lê claim/result, valida nonce/identidade/base64/hashes e recusa failure/pending; ao fim faz fsync do diretório. Isso não publica arquivo, mas significa que a API não é isenta de toda operação de filesystem. Não há emulação POSIX no Windows. A política externa pode registrar uma negação; não se promete ausência de efeitos do mecanismo de auditoria sob falha. O chamador mantém responsabilidade pelos handles e os fecha.

## Autenticação dos resultados

O intake exige pins externos independentes para admission.json, terminal_candidate.json, completion_seal.json, child_stdout.json, stdout final do parent e observação externa do término do parent. Os quatro primeiros são relidos no diretório protegido e comparados byte a byte. Ausência de failure.json é conferida fisicamente antes/depois, inclusive antes de publicar. Saída zero/reap da criança não substitui saída zero/reap do parent.

O pacote produtor não define schema persistido para o término do próprio parent. `parent_exit_pointers` mapeia cinco valores em um recibo JSON externo REAL: execution_unit_id, completion_seal_sha256, parent_stdout_sha256, exit_code inteiro zero, reaped booleano true. O arquivo/pin precisa já ter sido verificado externamente; essa API não o cria. Se o sistema de captura não registrar esses vínculos, a integração está OPEN e a leitura recusa. O mapeamento não transforma a forma do recibo em prova de execução. Não existe lançamento/resultado d72 por esta preparação.

O run commit é recuperado pelo key derivado da unidade e identidade request/decision vindas do child_stdout admitido. Os pins admitidos do claim/result global também devem coincidir. Controller result precisa coincidir com o stdout autenticado; arquivos são exatamente os quatro globais e 600 couplings. Supervisor terminal é passado ao validador existente e vinculado a nonce/processo/runtime.

## Documentos retidos e seis campos de contexto

`metadata` é mapa nome de artifact do request → bytes originais. A API lê apenas os metadados necessários, não os arrays y/C/origin. theta_plan, consumer_admission, coupling_template, structure e referência de suporte precisam ter sido retidos e coincidir com request.artifact_pins. Ausência é ORIGINAL_METADATA_NOT_RETAINED; não há busca, fallback, reconstrução ou prepare_joint.

| Campo da ponte | Fonte autenticada | Alcance |
|---|---|---|
| data_sha256 | consumer_admission.input_sha256.y_native_f64le | Identidade de y nativo; a ordem é vinculada pela mesma admissão e row_ids do request. |
| covariance_sha256 | input_sha256.C_native_f64le | C nativa, não confundir com covariance_out transformada. |
| X_response_sha256 | structure_sha256 + bytes structure + consumer._structure | Estrutura inteira contém X, respostas, unidades, T, linhas e medida. |
| support_sha256 | references.fixed_affine_support.sha256 + bytes da referência pinada no request | Identidade documental de engenharia; não certificado geométrico. Origin/rank/tolerâncias continuam vinculados pela admissão. |
| engine_config_sha256 | theta_plan.engine_configuration_sha256 | Confrontado com global_artifacts do request. |
| consumer_admission_sha256 | SHA dos bytes originais da admissão | Não recalculado a partir de projeção semântica. |

ReadContext é uma fachada SOMENTE de metadados, sem arrays e sem PreparedJoint. Reutiliza métodos NodeContext de descriptor/identity/background/validate/decode/validate_profile via chamada vinculada; o campo joint é explicitamente um pequeno proxy da admissão. Não se chama o construtor NodeContext, compute ou consumidor numérico. ThetaIntegrator é instanciado somente para validar plano, criar descriptor e aceitar envelope; callback é forbidden e run nunca é chamado. `_precision` e `_structure` são validações de metadados.

## Ordem, nível e publicação

O nível deve ser explicitamente admitido e igual ao last_level de cada plano original. Não se inventa nova malha. A ordem é os 600 SCENARIOS da ponte V2, depois product(range(2**level+1),repeat=3), com a chave dyádica canônica existente. Os cinco modelos/domínio integral permanecem na ponte. Nível2 implica 75.000 registros, não 75.000 novos cálculos.

O iterador privado `_records` confere claims/resultados e backgrounds, metadados do assembly/precision/envelope/profile e os vínculos de origem. Conserva os hashes dos result.json e, ao esgotar, compara a cadeia em ordem lexical de node_*.claim.json ao integrated_reference do terminal original. Perfis não têm pin esperado autodeclarado como autoridade final: o pin de cada arquivo é incluído nesse resultado e a cadeia foi ancorada externamente. Tuplas intermediárias não são entrega autenticada independente; somente estimate consome até o next final da ponte V2 e publica após essa checagem. Falha no fim não devolve estimativas parciais.

Saída F9_PROFILE_READBACK_RESULT_V1 é SYNTHETIC_ENGINEERING_ONLY. estimate_family gera estimativas na malha finita, não mínimos contínuos, L/U/SF ou p/veredito. Não existe campo scientific_decision nem chamada reduce_certificates. callbacks_executed=0 dentro da ponte significa zero callbacks científicos; os verificadores de objetos/recibos realmente são chamados. Verificação só tem prazo cooperativo e não substitui o supervisor externo já existente.
