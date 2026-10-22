# Adendo P3-01 — correção do recibo de exceções, V2

[REAL — revisão estática independente] O revisor identificou que a fonte P0–P2 incrementa seu contador histórico EDOM apenas quando a função de waveform devolve None. Com catch_waveform_errors=False, o Bilby instalado relança a exceção; o ramo de None não é alcançado. Portanto, o recibo P3 inicial poderia registrar FAILED e EDOM=0 apesar de uma mensagem explícita Input domain error. O achado se refere ao novo recibo P3. Nenhuma execução P3 ocorreu.

[REAL — correção local, fontes P0–P2 preservadas] O campo ambíguo EDOM foi removido do resultado P3. failure_receipt agora distingue:

- source_returned_none_count e source_returned_none_counter_raw: contagem de retornos None e o contador histórico da fonte, sem chamá-los de total EDOM;
- recognized_domain_exception_count: errno EDOM ou texto explícito Input domain error após uma tentativa nativa contada;
- indeterminate_exception_after_native_attempt_count: outras exceções após tentativa, sem inferir origem exata dentro de C;
- guardas temporais, exaustão de budget, exceções pré-nativa e exceções de aplicação;
- domain_error_total=null: não é inferido um total de domínio a partir de None ou exceção genérica.

Cada evento preserva tipo, texto, errno, parâmetros e contadores antes/depois. A mesma instância de exceção propagada ao handler externo é registrada uma vez. Um retorno None é convertido em aborto explícito antes de o Bilby poder tratá-lo como likelihood negativa infinita. Nenhuma falha recebe retorno -inf ou nova tentativa.

A função efetivamente vinculada a wf.frequency_domain_source_model é envolvida após generator(cfg). O wrapper usa functools.wraps e encaminha os mesmos args/kwargs; não troca apenas um atributo de pseob_source que o adaptador já tenha capturado por import. As três deformações fixas continuam zero e o source qualificado continua criando nova dict LAL por chamada. O status de budget usa a classificação já registrada com seu estágio; uma mensagem genérica de prazo após tentativa nativa não é reinterpretada como guarda pré-nativa.

[REAL — validação exclusivamente pura] CONTROLES_EXCECOES_P3_V2_FINAL.json registra100 verificações sem NumPy/Bilby/LAL/Dynesty: stubs de sucesso, None, domínio por texto, domínio por errno, erro genérico, erro pré-nativa, janela temporal, budget, prazo da fonte e timeout indeterminado. Conferidos propagação da mesma exceção, evidência, deduplicação, assinatura e encaminhamento. CONTROLES_PREPARACAO_V2_FINAL.json registra40 controles de sintaxe, pins, prior e ausência de diretório/recibo de execução. Esses controles não são PE nem qualificação nativa do sampler.

[REAL — preservação] Alterações ficaram no driver P3, helper puro, contrato, comando e documentação derivados. Fontes/arrays/PSD P0–P2, lista V1, quatro holds, D, Atlas, fila e originais permanecem fora da mutação. Backups imediatos de bytes preservam cada draft; DELTA_P3_01_DRIVER.patch compara com o driver examinado pelo revisor. O contrato atual identifica V2 e o pin V1 superado. O manifesto antigo permanece histórico; os caminhos correntes mudados passam a ser descritos pelo MANIFESTO_P3_PREPARADO_V2.json.

[OPEN] Revisão independente do delta e autorização da coordenação para execução continuam pendentes. O exemplo de recibo permanece authorized=false, o comando exato não foi executado e não há AUTORIZACAO_COORDENACAO.json nem EXECUTION_001. Esta correção não altera prior, seeds, alvos, grade, PSD, limites de custo ou critérios de convergência.
