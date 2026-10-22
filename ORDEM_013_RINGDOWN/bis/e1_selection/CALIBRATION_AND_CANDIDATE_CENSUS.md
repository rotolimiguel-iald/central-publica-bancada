# Censo independente — calibração e candidatos antes de E2

[REAL — conjuntos/índices/metadados conferidos; INPUT — elegibilidade; OPEN — ausência universal e cegamento]

**Conferido: 33 HDF no pSEOB do record21454847; 18 produtos GWTC3; 12 eventos sobrepostos; união de39 eventos únicos, em51 produtos.** O número39 não pertence ao tar pSEOB do GWTC5. Nomes do índice, recibo de extração e esquema coincidem nos33; hashes declarados e tamanhos se encadeiam. O censo não reabriu valores HDF5 nem rehasheou os grandes binários.

Calibração exposta inclui todos33+18, inclusive controles excluídos de combinações31/10. Esses eventos não se tornam cegos por terem sido excluídos de um resultado. A preferência pelo produto GWTC5 em duplicatas é organização do censo; não foi calculada likelihood de união nem multiplicados posteriores sobrepostos.

| corrida | SNR≥12 | com220 no corpus | ausentes no corpus | elegíveis INPUT | elegíveis com220 | candidatos elegíveis ausentes | aguardando GR |
|---|---:|---:|---:|---:|---:|---:|---:|
|O4a|28|7|21|17|7|10|6|
|O4b|45|14|31|27|14|13|1|
|O4c_discovery_only|1|0|1|0|0|0|1|
|O4_public_total|74|21|53|44|21|23|8|

## Os13 candidatos O4b no corpus auditado

| evento | SNR GWOSC | mediana Mf_det/M☉ | mediana chi_f |
|---|---:|---:|---:|
|GW240513_183302|14.5|54.8|0.74|
|GW240515_005301|12.8|85.4|0.84|
|GW240615_160735|13.1|75.2|0.78|
|GW240920_073424|14|46.6|0.64|
|GW240923_204006|13.6|126|0.7|
|GW240930_035959|16.1|42.3|0.58|
|GW241102_144729|12.7|114|0.65|
|GW241111_111552|16.3|55.6|0.72|
|GW241130_034908|13.8|70.1|0.71|
|GW241210_060606|13.4|69.3|0.7|
|GW250104_015122|12.1|133|0.73|
|GW250109_010541|13.1|97.4|0.66|
|GW250118_170523|13.9|86.8|0.73|

**O4b:45−14=31 ausentes antes do corteGR; 27−14=13 candidatos elegíveis depois dele.** O evento O4b sem metadadosGR, GW241230_233618, permanece aguardando. Não se conta como aprovado ou reprovado. Os17 valores conhecidos que não passam foram mantidos no JSON.

O adendo O4a acrescenta17 elegíveis, dos quais7 possuem posterior no corpus e10 são candidatos por ausência nesse corpus: GW230601_224134, GW230811_032116, GW230919_215712, GW230922_020344, GW230922_040658, GW230924_124453, GW230927_043729, GW231108_125142, GW231123_135430, GW231206_233134. Há6 O4a ainda aguardandoGR. GW250207_115645 segue aguardandoGR, sem certificação de elegibilidade por substituição de chi_eff.

Nenhum dos candidatos elegíveis desta interseção alcança a prioridade SNR≥30. Esse fato não muda o corte mínimo≥12. A lista completa39 de calibração, os12 duplicados, os6 exclusivos antigos e todas as74 linhas O4 com SNR≥12 estão no JSON.

## Limite de ausência e uso antes de E2

**Ausente dos dois corpora pSEOB pinados não equivale a nunca publicado em qualquer lugar.** Não fiz busca universal de todas as releases/estudos, não certifico cegamento e não abri posteriores de candidatos. Estatutos `universal_never_published=null`, `blindness_certified=false` e `E2_registered=false` permanecem explícitos. O registro E2 deve fixar o universo de consulta/corte temporal e como tratar eventual posterior externo/exposição anterior; este censo não o substitui.

Bases: snapshot GWOSC do E0, critérios INPUT adotados, TGR5 tabelas2–3 e adendo TGR4III tabela1. A SNR da tabela histórica não substituiu a SNR GWOSC. Fontes/arrays originais preservados. Código `check_calibration_candidate_census.py`, JSON homônimo de resultados e `CENSUS_RECEIPT.json` registram hashes e escopo de conferência.
