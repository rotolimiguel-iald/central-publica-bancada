# Revisão independente do reparo de inicialização P3

Identidade: chatgpt-codex/ordem-018/derivacoes. Mapa consultado: registro 441, rota ringdown.ramo_b_preregistro_v386; falha V2 preservada no registro 434.

[REAL — inspeção estática e integridade] As 81 verificações do recibo passaram. Não identifiquei defeito bloqueante no delta do codec. O aceite técnico sustenta preparar um pacote local corrigido do mesmo escopo. Este parecer não autoriza uma nova execução científica.

O candidato é idêntico, byte a byte, ao driver V2 depois da remoção das duas linhas de importação/chamada de preload_npz_codec. A igualdade também foi conferida por AST. As linhas entram antes do audit hook e da leitura do NPZ. Permanecem iguais a allowlist, os controles de autorização/CLAIM, orçamento, contadores, modelo, parâmetros/priores, ruído/sementes, grade, sampler e convergência. Foram conferidos os 17 insumos do contrato original; não houve alteração em arquivos do autor.

[REAL — código lido] O helper exige o caminho exato /usr/lib/python3.12/encodings/cp437.py, confere tamanho e hash dos bytes, origem resolvida do módulo, identidade do codec e roundtrip dos 256 bytes. O carregamento ocorre antes do hook, sem acrescentar uma permissão de leitura à allowlist. Os bytes atuais do codec e dos parsers conferem com seus pins. A futura montagem executável precisa incluir helper e CODEC_CP437_PIN.json entre seus insumos congelados; o candidato deliberadamente ainda não é esse pacote.

[REAL — controle arquivado; não repetido] O controle isolado V2 registra 48 verificações aprovadas, 14 arrays e apenas o NPZ lido após o hook. O primeiro controle, recusado por importação de zipfile, permanece preservado. Nesta revisão foram lidos código, contratos, recibos e hashes; o controle não foi repetido e o NPZ não foi interpretado. Os bytes do arquivo sintético foram lidos somente para integridade.

[DERIVED — comparação dos caminhos] O harness V2 carrega explicitamente zipfile e ast antes do hook, pois não importa as bibliotecas científicas do driver. Essa diferença não encobre uma dependência ausente na fronteira do codec examinada:

- ast: o driver importa Bilby antes do hook. Foi verificada nas fontes atuais a cadeia Bilby → core → utils → introspection → inspect → ast; inspect.py importa ast na linha 145. Os quatro arquivos Bilby dessa cadeia conferem com os pins do runtime original. Não importei esses módulos científicos para fazer a revisão.
- zipfile: o recibo da falha original chega à tentativa de leitura de cp437 depois de abrir o NPZ, sem leitura/bloqueio de zipfile ou ast após o hook. A allowlist original não concede leitura aos parsers da biblioteca padrão. A fonte atual de zipfile contém o uso de cp437 nas linhas 1470 e 1656. Isso sustenta que o parser já estava carregado no caminho real registrado; não equivale a uma nova atestação de execução.

[OPEN — alcance] O controle isolado não cobre a continuação por np.fft, configuração dos detectores, montagem da waveform/likelihood, sampler, convergência ou cobertura. Esses pontos continuam não testados por esta revisão. O audit hook de Python também não constitui confinamento de syscalls nativas ou do sistema operacional.

[REAL — ausência de nova unidade] No recorte examinado, o diretório candidato não contém CONTRATO_P3 executável, autorização, launcher, CLAIM ou diretório de execução novos. A preparação original conserva somente EXECUTION_001 e um CLAIM. P3_GR_001 permanece FAILED, com zero chamadas de likelihood e do wrapper nativo; não foi reaberto. Nesta revisão houve zero importações científicas, PE, waveform ou likelihood.

[DERIVED — decisão técnica] É adequado preparar, localmente e sem executar ciência, um pacote corrigido com o mesmo objeto científico, limites e allowlist, preservando a preparação V2, seus identificadores, CLAIM e falha. Não identifiquei motivo científico concreto para exigir uma decisão externa adicional apenas para essa preparação local já abrangida pela missão. Qualquer execução posterior depende de contrato novo e decisão específica da coordenação; este parecer não concede essa autorização e não decide como identificar eventual nova unidade.

A proibição de repetir executores remotos falhos ou envios incertos permanece integral. O reparo local sintético não chama modelo remoto, não abre D, não modifica V1/P0–P2 nem resolve suspensões/decisões pendentes. Nenhum gate ou veredito físico é alterado.

Evidência auditável: REVISAO_P3_CODEC_RECIBO.json (81 verificações, fontes, hashes e limites), FONTES_WSL_LEITURA.json (oito fontes WSL lidas sem importação científica), REVISAO_P3_CODEC_MANIFESTO.json (hashes desta revisão).
