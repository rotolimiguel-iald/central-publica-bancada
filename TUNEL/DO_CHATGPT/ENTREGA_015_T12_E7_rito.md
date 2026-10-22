[REAL — T12 entregue; NÃO-CEGO; MEDIDA — ativação de jobs sob subemenda]

# T12 — E7 na variante rito

Abertura015SHA256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

PAGO: variante em `ORDEM_013_RINGDOWN/bis/e7_prepare_v1_1/producer/`, quatro ASTs idênticos;53 testes históricos passaram e72 testes da variante passaram. Um teste do importador externo foi aposentado porque esse importador foi removido, com novos controles de guarda em seu lugar. Fonte antiga intocada.

PAGO: subemenda V1.1.1 testemunhada, SHA256 75b1884d18240ddbc94616bfe4f80c0409e9baee9461c37a49c4583f08d806f9. Histórico E7 continua V1; plano, autorização, posterior e recibo anteriores são conferidos sem reetiquetar a extração. A variante só lê o produto histórico explicitamente pinado.

PAGO: replay rc0 em 19.400s de parede; 33 eventos de calibração, test_count=0. Estados dos pins de fontes/tar: FILE_HASH_VERIFIED_HERE. 330 linhas220 concordam com T05, maior diferença absoluta 6.93889e-17;440 transportado do T05, não reextraído. N_alvo operacional=null, alvos E0 e seus tetos ao lado, gate red com causas. lnB e z físico=null, AWAITING_DATA. Condição de leitura, não ganho de sigma.

MEDIDA: `checked_registration()` da guarda V1.1 devolveu `ValueError: V1.1 activation does not match latest registration/witness`. O recibo fixo descreve V1.1 base. Recibo sucessor publicado ao lado, sem substituir o original. Esta entrega não declara ativação da campanha; mecanismo versionado por elo precisa ser resolvido antes do primeiro job. A guarda V1 antiga chegou ao TimeoutError esperado, preservando sua árvore.

Falhas preservadas: caminho do preparador inicialmente errado (nenhuma saída), WSL sem acesso no sandbox (nenhum trabalho científico iniciado), teste positivo detectou alias GW250114 versus GW250114_082203 e estado OPEN_NO_UNIQUE_EXPONENTIAL; corrigidos antes da testemunha. Revisão local independente apontou quatro inconsistências de metadados/escopo; corrigidas e testadas. Nunca se alterou fórmula para fazer teste passar.

Artefatos: `RITE_REPLAY_RESULT.json` SHA256 9834bf3c799dedf29efda5d9554051dbc69cd2f3888561f404e64c8a1cafdc94; `RITE_REPLAY_RECEIPT.json` 5cefac33b2fe8f0ce65688fff09497382d0959c853d6bfac7ee44279c4ca2b27; `RESULT.json` 462c66dbc21efed2a7f9dadea5c990c32fea743fa1bf678d3f2f6762b44a523f; `LAUNCH_GUARDS.json` 530b00de37875bbc1de67fb77ccafa366b9ec74205c468ed2d356f5137b357e7. Manifesto completo: `DELIVERY.json` nesta pasta.

Reprodução de controles: `/opt/lal_env/bin/python -B .../e7_prepare_v1_1/run_tests.py --legacy` e sem `--legacy`. Fixtures em pasta própria, nunca dados físicos. Replay: comando integral em RITE_REPLAY_RECEIPT; usar destino novo porque o produtor recusa sobrescrita. A cadeia pode ganhar elo posterior e recusar o replay antigo como stale, corretamente.

Axiomas: N/A — sem Lean. Horas de máquina pesada:0. Custos externos novos:0; custo da revisão da coordenação não medido, não tratado como zero. Próximo: orçamento015 e resolução da ativação antes de R7.
