# P3 INIT_QUALIFIED_003 — pacote preparado, sem execução

[INPUT — coordenação] Preparação separada autorizada após o controle integral de inicialização concluído e registrado no mapa 465. Esta entrega não emite autorização, não cria CLAIM, não executa o supervisor/driver, não repete o controle de inicialização e não abre dados D. Falhas V2 e CODEC002 continuam terminais e intactas.

[REAL — preparação] 117 verificações registradas de preparação/invariância e 21 verificações estáticas de integração/assinatura passaram. A leitura atual do WSL verificou 1.165 pins: 1.162 arquivos do runtime anterior, interpretador, codec cp437 e ASD adicional exata. Essa verificação de hashes não importou módulos científicos. A ciência preparada tem 26 entradas pinadas; o driver não foi importado ou executado nesta preparação.

## O delta restrito

O novo driver usa build_B e verify_analytic_state do helper init_detectors.py exatamente qualificado no controle anterior. A factory Bilby H1/L1 lê a curva instalada aLIGO_O4_high_asd.txt; só esse arquivo exato é acrescentado à allowlist de runtime. Seu tamanho e hash são conferidos e a origem efetiva é comparada. Não há wildcard ou permissão para diretório. Um snapshot local da mesma curva preserva a referência documental local_path; não é a PSD usada pela likelihood.

A PSD default é substituída pelo array analítico do NPZ qualificado antes de construir a likelihood. O helper confere PSD crua/efetiva, grade, geometria, banda, duração, época, janela e notches. O driver verifica também o strain sintético armazenado e repete a verificação da PSD depois do construtor GWT. Defaults e estados antes/depois entram no recibo; um bloqueio de leitura engolido durante inicialização provoca falha explícita. O diff integral está em DELTA_DRIVER_VS_CODEC002.patch, e o diff do contrato está ao lado.

O helper contém também a alternativa A preservada byte a byte, mas o driver chama exclusivamente build_B e o contrato fixa B. Nenhum guard de contagem zero, monkeypatch de waveform/likelihood ou bloqueio do sampler foi trazido do controle. Essas interdições pertenciam ao controle consumido, não ao programa científico preparado.

## Ciência e limites preservados

Supervisor launch_p3.py, prior_transform.py, failure_audit.py, source/adapter/contrato temporal, configuração sintética, manifesto do runtime e preload cp437 são cópias exatas de CODEC002. Os dois alvos GR_GAUSS/RB_GAUSS, NPZ, hashes dos seis arrays por job, ruído pareado, sementes, normalização SNR20, priors e grade permanecem iguais. Hipótese única em ambos: IMR pSEOBNRv4HM_PA alinhado, DTau220 livre; DOmega220, DTau440 e DOmega440 fixos em zero. Os rótulos dos datasets não são dois modelos rivais; não cabe BF comparando seus logZ.

Novas identidades propostas: P3_GR_INIT_QUALIFIED_003 e P3_RB_INIT_QUALIFIED_003; diretório futuro EXECUTION_INIT_QUALIFIED_003, ainda inexistente. A identidade nova não é autorização de repetir ciência: ROOT decide especificamente após revisão independente.

| Limite por job | Valor preservado |
|---|---:|
| Likelihoods incluindo inicialização | 10.000 |
| nlive / walks | 256 / 25 |
| Parede interna / supervisor | 3.600 / 3.610 s |
| CPU soft / hard | 3.300 / 3.305 s |
| Memória endereçável | 8 GiB |
| Workers / threads / jobs simultâneos | 1 / 1 / 1 |
| Jobs planejados, sem retry/resume | 2 |

Teto de duas unidades: 20.000 likelihoods, 7.220 s de espera supervisionada e 6.610 s de CPU hard dos filhos. Estes são os mesmos envelopes anteriores, não uma previsão de custo medido. EDOM, erro nativo, leitura não permitida ou incerteza interrompem a campanha conforme o contrato preservado; somente esgotamento gracioso previsto pode avançar ao segundo job. Convergência mantém dlogz<0,1, ESS≥100 e demais condições anteriores; dois jobs não medem cobertura.

## Assinatura e cadeia integral

[REAL — inspeção estática] O snapshot de waveform_generator.py coincide por hash com o manifesto do runtime. Seu construtor vincula synthetic_only220 e obtém source_parameter_keys da assinatura original antes de o driver atribuir o wrapper FailureAudit à callable efetiva. A atribuição posterior não usa descriptor nem refaz a inferência. O wrapper conserva args/kwargs e os três zeros; nenhum shim de compatibilidade foi acrescentado. As cópias exatas do adapter e do wrapper permanecem as qualificadas anteriormente.

O controle anterior verificou H1/L1, ambos os rótulos e a PSD antes/depois GWT, com zero avaliações; seus pins são entradas de proveniência. Esse resultado não ensaiou inicialização de Dynesty, leitura preguiçosa durante sampling, domínio de todas as waveforms no prior ou recuperação/convergência. Essas fronteiras continuam OPEN. O hook Python continua posterior a imports/pins fixos e não equivale a confinamento nativo/OS. O roll-off do objeto de strain permanece o default 0,2 s; o contrato temporal da fonte mantém 0,4 s — papéis distintos já preservados na qualificação.

## Comando proposto e decisão pendente

COMANDO_EXATO_NAO_EXECUTADO.json fixa argv e SHA do contrato. Requer AUTORIZACAO_COORDENACAO.json correspondente, ausente. Não foi criado recibo de autorização nem CLAIM, e a campanha permanece sem execução. O supervisor é idêntico ao anterior. A revisão independente e a decisão específica da coordenação devem anteceder qualquer lançamento; não há fallback ou nova tentativa implícita.
