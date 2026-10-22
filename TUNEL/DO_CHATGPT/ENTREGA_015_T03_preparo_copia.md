[REAL — preparação parcial T03; emenda ainda NÃO registrada]

Abertura015SHA256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

A árvore irmã bis/e2_code_v1_1 contém cópias byte a byte dos 14 arquivos Python da V1. Nenhum deles foi emendado ainda. Antes e depois, checked_registration() da V1 rodou em /opt/lal_env e alcançou TimeoutError('Part B hard deadline reached'), depois de conferir testemunha, ativação, árvores e runtime. Registro V1 e árvores extras preservados. Recibo COPY_RECEIPT.json, sha256 26e76734759c5770fcc92017fdb4e8ef98444ac3e82c102d71cfe886414b31bd; CPU 2.950409s, parede 10.426363s.

Nenhum R7 criado; nenhuma PE, dado cego ou leitura de semente. Falta: guarda V1.1 e cadeia estatística/alocação; separação geração/banda e registro EDOM; nulls_v1_1 e recusa ids V1; blinding por leitura; qualificação source-only R5 do runner emendado; provas negativas; registro/testemunha. A ordem R1 usa só-220 com 440 fixo RG. Caixa(b) não autorizada. A tarefa DeepSeek de cadeia/estatística permanece preparada, NÃO enviada, pendente de autorização específica após a revisão automática.

Inspeção somente de leitura do Bilby pinado: _base_lal_cbc_fd_waveform usa delta_frequency extraído da grade, maximum_frequency no LAL e trunca/preenche para len(frequency_array), aplicando depois máscara e fase temporal. A próxima implementação deve conferir a grade de geração e a restrição aos bins da grade de dados; não presumir que trocar apenas um campo configure independentemente a amostragem interna. Esta leitura não é teste de geração ou validação R5.
