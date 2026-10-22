# E6 — preparação independente do sidecar

[INPUT — escopo autorizado] Preparar contrato, fontes e código em `bis/e6_prepare`, sem executar E6. Nenhum posterior, strain, waveform, PE, MC ou cálculo científico novo. E7 e E4 permanecem intocados. A ordem continua aberta; E7 real vem somente depois de E6 e da autorização pertinente.

[REAL — artefatos de preparação] `generate_reach_table.py` usa somente biblioteca padrão. `prepare_static.py` produz os contratos/pins a partir de metadados locais e examina a AST sem importar nem executar o gerador. O recibo estático registra exatamente esse alcance. Não há resultado E6 nesta entrega. Sintaxe e inspeção estática não certificam funcionamento, correção científica ou compatibilidade com recibos futuros.

## Forma do quadro

O produto previsto contém 180 células de contrato: três canais × dez leituras E2, na ordem registrada × seis grupos de dados. Cada célula contém cenários separados, sem soma entre eles:

- `TAU220_POPULATION`: planejamento populacional em δτ220, mantendo população, convenção e diagnóstico com intercepto livre separado do offset fixo em zero.
- `TAU440_FIXED_SOURCE_FISHER`: todos os cenários do produtor E4, incluindo ambas as variantes 440, dois perfis e duas convenções de SNR. A fonte de referência fixa não é a mediana de GW250114. SNR do modo isolado não é SNR IMR/rede.
- `DF220_POPULATION_WIDTH_IV`: informação local de variância em δf220 e cenários Brownianos registrados. Não é informação de média em δτ; não se somam equivalentes entre canais.

Grupos: O4 hoje, O4 cego, O4c/GWTC6, O5 banda, ET e CE. O4 hoje significa acervo disponível hoje, incluindo populações históricas de outros runs devidamente identificadas. Não é seleção de uma população O4 pura.

Cada cenário expõe `z_expected_conditional`, `N90_information_target`, `N90_count_scenario`, `GW250114_equivalents`, `delta`, `sigma`, `correction_over_sigma`, taxa/IC, `z_physical`, `lnB`, gate numérico e veredito. Cada métrica tem valor, unidade, estatuto, motivo e caminho/SHA256/JSON Pointer da fonte. `None`/`null` permanece `OPEN`. Zero só é transportado quando existe na fonte, por exemplo na variante sem deformação do 440; não preenche ausência.

Os estatutos das dez leituras vêm de `C1_LEITURAS_v4.json:/rows/*/clock_status`, com a classificação resumida INPUT ou CONJECTURE e o texto completo preservado no contrato. Nenhuma leitura é escolhida. O controle `GR_FALSE_FALSIFIER` é referenciado no mapa como controle, não incluído como uma décima primeira leitura. A RG permanece limite clássico/controle; NOT_FALSIFIED não significa CONFIRMED.

## Limites de interpretação

Os alvos E0 de offset zero são planejamento NÃO CEGO e `PROIBIDA_COMO_TESTE`; não recebem significância física. O diagnóstico de intercepto livre é outro cenário. A convenção principal copiada para correção/sigma é std_ddof1; sigma_q90 e exact_QNM_all_control permanecem fontes de sensibilidade pinadas, sem seleção pós-hoc de uma delas.

Os N90 Fisher são contagens condicionais de fontes idênticas. Não são convertidos em informação nem equivalentes 220 por fórmula nova. Os N90 de rota IV são limites inferiores condicionais comuns, repetidos como referência nas dez leituras: não representam dez previsões de jitter. O vínculo leitura → jitter recuperado continua OPEN. Covariância sintética E1 não vira covariância física calibrada.

O5 conserva bandas, exposições e controle BNS identificado como controle, nunca previsão BBH. IC de taxa é Poisson condicional ao universo publicado e à exposição INPUT; não é IC total de z/poder e não presume tempo vivo ou eficiência de seleção medidos. Os cenários 3G de âncora SNR do E0 aparecem sob ET/CE explicitamente como referência genérica compartilhada, sem conversão em previsão específica de instrumento. As linhas Fisher ET/CE mantêm suas PSDs distintas.

Pisos históricos 220 e E1 aparecem em contextos separados, com números copiados e sigma calibrado null quando ausente. Não se transplantam ao 440 ou ao δf. O gate do cenário começa OPEN. Sem dado de teste: AWAITING_DATA. Com teste e gate vermelho/aberto: somente INCONCLUSIVE_SYSTEMATICS; sem z físico/lnB. Gates verdes e resultados fortes são apenas transcrições de decisões revisadas, jamais inferência do gerador a partir de z condicional ≥5. Não existe cálculo de β neste sidecar: valores já publicados são transportados, sem novo modelo ou aproximação.

## Interface futura, ainda não ativada

`CONTRACT.json` e `STAGE_RECEIPT_SCHEMA.json` descrevem uma interface proposta de adaptação. Não afirmam que produtores E3 já emitem esse formato. O principal e o revisor devem fechar os mapeamentos de campos reais e emitir recibos/revisões verdadeiros. Este pacote não fabrica recibos faltantes nem aprova seu próprio mapeamento.

Para cada estágio E3.2, E3.3 e TESTE (identificador `TEST`), a autorização futura deverá pinar um recibo `E6_REVIEWED_STAGE_V1`, seu artefato JSON e sua revisão independente. A revisão aceita explicitamente o outcome e a lista exata de bindings. `BLOCKED`, `UNAVAILABLE` e `PARTIAL` são admitidos como resultados revisados, preservando paredes e lacunas; não autorizam leitura física. Arquivos legados em outros formatos precisam de adaptação explícita revisada, fora desta preparação.

Cada binding identifica rota, leitura, grupo, cenário, escopo e métricas por JSON Pointer/unidade. O gate exige campos explícitos, incluindo nulls. Um resultado físico/forte em TEST exige todos os estágios COMPLETED, recibo E3.3 referenciado por SHA, cenário de calibração na mesma célula, gate verde compatível e flags pagas. Também exige descegamento autorizado, verificações de população, regra de decisão e multiplicidade pagas. EXCLUDED_IN_READING exige regra de exclusão relativa paga. A normalização/seleção abertas mantêm lnB null.

A autorização futura, de estatuto `AUTHORIZED_E6_ASSEMBLY_AFTER_REVIEWED_E3_AND_TEST`, identifica E2 e testemunha, contém timestamp com timezone, pins dos quatro arquivos de pacote indicados no contrato, três recibos e run_id inédito. O gerador confere E2_ACTIVATION_COMPLETE, hashes e cronologia E2 ≤ recibos ≤ revisões ≤ autorização ≤ agora; revalida fontes antes da publicação. Não importa o guard mutável do produtor principal, E4/E7, NumPy, SciPy ou h5py.

Somente após revisão e ativação pelo principal, a interface prevista é:

```text
/opt/lal_env/bin/python -B -O generate_reach_table.py --execute --authorization <autorizacao-real.json> --authorization-sha256 <sha-lido-do-arquivo>
```

Esse comando NÃO foi executado. A saída futura ficará exclusivamente em `e6_prepare/runs/<run_id>/QUADRO_DE_ALCANCE_V1.{json,md}` e `RESULT_RECEIPT.json`. Cada arquivo é limitado a 25 MiB, gravado por temporário verificado e publicação exclusiva; run existente é recusado. Se houver falha após criar o diretório de run, os arquivos já publicados permanecem e o run_id não é reutilizado. Não há atomicidade de transação entre os três arquivos; consumidor só deve aceitar um run com recibo final válido.

## Próximos passos do principal

1. Revisar este código/contrato e seus pins antes da ativação. Não há teste de execução neste pacote.
2. Concluir/revisar E3.2, E3.3 e TESTE; registrar resultados ou paredes sem inventar dados.
3. Preparar os bindings e revisões correspondentes, sem alterar a seleção de leituras do E2. Se houver mudança de contrato/código, produzir nova versão/pins antes de autorizar.
4. Ativar explicitamente a montagem E6; conferir quadro, números e recibo. Esta preparação não libera extração E7 nem conclui a ordem.
