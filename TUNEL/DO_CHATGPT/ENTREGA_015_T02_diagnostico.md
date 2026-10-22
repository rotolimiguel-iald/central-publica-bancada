[REAL — comportamento nativo; DERIVED — mecanismo pela fonte C; nenhum novo teste físico]

Abertura015SHA256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a
Predecessores intactos: [{"path": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e3_pilot_failure_diagnostic\\DIAGNOSIS.json", "sha256": "3d02f43355301dab5a110c44fae48f569fe6f13aa84828703cf75da4b6f170d6"}, {"path": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e3_pilot_failure_diagnostic\\DIAGNOSIS.md", "sha256": "92a51a6212f6a4024c6ad7fab9ba338ce48c82139904e784558c2efa6250ed47"}]

Replay exato: primeiros8sorteios coincidem;15concluem e o16aborta com rc-6 no mesmo processo. Em subprocessos separados abortam16/20/22/24(rc−6 nesta rodada);2/8 retornam domínio. O diagnóstico anterior de sorteio desconhecido fica corrigido nesse escopo. Identidade com o heap do piloto original continua DERIVED.

Grade fina:{'REF': {'last_finite': 1.0, 'first_crash': 1.1}, 'DRAW8': {'last_finite': 1.0, 'first_crash': 1.1}, 'HIGHMASS': {'last_finite': 1.0, 'first_crash': 1.1}, 'LOWMASS': {'last_finite': 1.0, 'first_crash': 1.1}, 'HIGHSPIN': {'last_finite': 1.0, 'first_crash': 1.1}, 'NEGSPIN': {'last_finite': 1.1, 'first_crash': 1.2}}. Na grade de122pontos das seis fontes(56+66), o critério não é o sinal de dtau220. A escala do limiar é max(1,1+dtau220); previsto pela fonte2·Imω440/Imω220=2.11365002; medido2,0 com intervalo de grade[1.75, 2.25]. retLen/indAmax/Nrdwave não instrumentados, não medidos.

Scan registrado120:{'FINITE': 80, 'DOMAIN_RETURNED_NONE': 3, 'CRASH': 37, 'OTHER': 0}; sinais entre abortos:{'-6': 37}. Comparações com a gerência:{"grid": {"own_rows": 56, "management_rows": 56, "same_outcomes_ignoring_heap_signal": true, "own_crashes": 20, "management_crashes": 20}, "fine": {"own_rows": 66, "management_rows": 66, "same_outcomes_ignoring_heap_signal": true, "own_crashes": 47, "management_crashes": 47}, "registered_scan": {"own": {"FINITE": 80, "DOMAIN_RETURNED_NONE": 3, "CRASH": 37, "OTHER": 0}, "management": {"FINITE": 80, "DOMAIN_RETURNED_NONE": 3, "CRASH": 37, "OTHER": 0}, "same": true}}. C04(400sorteios,22SIGSEGV/98SIGABRT) permanece DECLARADO pela gerência, fonte hash7e1576575ec41f90cb5360edf306c98f4cc6c9907387d57f3a96afd9963dcaca; não é contagem nova da bancada. A reprodução exata do sinal pode variar com o heap.

EDOM: previsão f550>1024 conferiu em150/150chamadas isoladas. Quatro sementes,8000sorteios:4,35%; SE binomial combinado0,228p.p., contra0,456p.p. por2000sorteios. O4:22/36excedem1024 no550,18/36excedem2048,4/36têm o220fora da banda1024. Os8semMf continuam sem diagnóstico. Nos cantos do posterior conhecido, o limite1024não demonstrou viés; não houve PE nova.

CPU medida=399.661s; parede sequencial=462.910s; nenhum comando ultrapassou900sCPU. O tempo anunciado anteriormente de10–13min para DG02 foi substituído pela medição destes recibos. Runtime conferido antes:4621arquivos; nenhuma instalação ou modificação em/opt. Nenhum jobV1 relançado; nenhuma semente cega lida; nenhum gate alterado.

Próximo ramo obrigatório:T13(higiene), depoisT03(guarda/emenda).
