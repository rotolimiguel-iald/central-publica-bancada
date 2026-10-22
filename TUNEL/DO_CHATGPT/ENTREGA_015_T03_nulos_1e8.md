[REAL — calibração SINTÉTICA; não é detecção nem calibração física de sistemáticas]

# T03 — caudas e covariâncias registradas

Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a
Abertura015SHA256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
Registro SHA256: a02c4224b0c832a85e8eaef736197754235aa573290760bb2307ad6ac4c713b4

Estado: T03_MEDIDA_INCOMPLETE_WITH_COST; 0/30 células concluídas. Cada célula concluída consumiu exatamente10^8 draws e preserva a semente já registrada. Nenhuma repetição de célula V1 ou de tentativa incerta. As6células IV usam LRT>25; as24t5 usam matched_z>5 e as3covariâncias registradas. ICs por célula, sem correção de multiplicidade; não dão alegação global.

|Célula|k|p empírico|UL95 unilateral Clopper–Pearson|
|---|---:|---:|---:|


Somente nas células IV, a comparação UL95≤2,87e-7 avalia a suficiência SINTÉTICA do limiar25. Não determina p físico, sigma_sys ou sigma_jit,rec. t5 é escala comum com nuisance gaussiana; não reinterpretar como ruído independente nem converter estes controles em detecção.

Falha/limite: {"type": "TimeoutError", "message": "T03 allocated machine hour exhausted"}. Não iniciadas: 24. Se parcial, os resultados concluídos permanecem e os demais não são inventados nem repetidos.

Custo: união de intervalos próprios=0.997271071h; CPU filhos=21476.335183s; parede supervisor=3590.217728s. Alocação1h. Máximo6filhos; nenhuma PE concorrente. Chamadas remotas0; custos de coordenação desconhecidos permanecem desconhecidos.

Manifestos: RESULT.json sha256 142d8fbcbcde607c7350506757ca2558e8af6918dcf59e57c9f376d9e36d473e; SUMMARY.json sha256 6af63532b95083acddb659eb76c08ab256fa5a1c30d014b94a3b5e76e0d9b8ed. Arquivos em ORDEM_013_RINGDOWN/bis/015/nulls_campaign_001 e recibos por célula em bis/. Tentativas e logs preservados.

→ CONTINUE: T04, qualificação400 e piloto só220. Nenhum gate ou original alterado; dados cegos não abertos.
