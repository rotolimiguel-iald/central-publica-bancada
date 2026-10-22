# Kerr V2 — revisão independente do resultado concluído

[REAL — verificações documentais e recálculo leve sobre amostras já produzidas] **KERR_V2_NONBLIND_CALIBRATION_REVIEWED_WITH_LIMITATIONS; blocking_findings=[]**. Recibo completo: `KERR_V2_POST_RESULT_REVIEW.json`, SHA256 `0e92967fd6f228ad2e6bc003b0ed8a67a994a6fdc6d660013e99c66a686248c7`. Código: `review_kerr_v2_result.py`. Foram 9.565 verificações, incluindo pins rechecados ao final; execução da revisão em 4,278 s, sem PE, ondas, leitura de strain ou análise das amostras parciais V1.

## Convergência, integridade e custo

Terminal bruto HDF5 e recibo concordam: estado registrado antes de add_live, delta_logz=0,09995244827021912 < 0,1; ncall=1.356.580 < 3.000.000; ncall_reported igual. ESS recalculado dos pesos nested=3.093,8512933753923, superior ao mínimo100; N posterior=2.128, superior ao mínimo1000. ESS dos pesos nested e N das amostras reamostradas são grandezas diferentes; ESS maior que N não constitui erro. Evidência/erro finitos conferidos como controles, sem interpretação de lnB entre hipóteses.

Pins dos cinco fontes, demais fontes/dependências, distribuições e arquivos do manifesto de runtime conferem. As oito colunas do NPZ são finitas, pareadas, estão no suporte dos priors e coincidem exatamente com as colunas do HDF5; priors do HDF5 conferem com CONFIG. Hash NPZ coincide com COMPARISON. Cabeçalho da referência permite Mf/af; referência tem 52.744 linhas, tratadas como equal-weight conforme o contrato, com proveniência de merging ainda OPEN.

Condições de covariância reportadas: H1=1.673.599,0233 e L1=13.059,4615, ambas abaixo de 10^12. Verificados pins PSD e onsource nos recibos, 819 amostras por detector e resíduos de grade nativa menores que 1/4096 s. Não houve reconstrução de covariância ou nova conferência dos bytes de strain. O Welch V1 recusado permanece resultado negativo, sem reaproveitar suas amostras.

Launch wall=641,114773358 s; controlador=641,003189313 s; CPU filhos=637,422408 s. Runner após comparação: wall=638,337946532 s, CPU=636,289446466 s. São escopos sobrepostos, não parcelas somáveis. V1+V2: wall dos controladores=1.035,302018652 s e CPU filhos=1.026,449371 s. Finalização em 22/09/2026 22:29:19,501563 UTC, antes do stop público e do deadline original 23/09/2026 00:00:09,447676 UTC. Uma variante public_psd, rc0, cutoff=false e group_absent=true; cleanup confirmado pelo recibo, sem nova varredura de processos.

Sampler ncall=1.356.580; likelihood_calls=1.357.974; após construção do sampler=101. Não igualar esses contadores. O contador Kerr está depois da guarda de prazo, conforme ressalva anterior.

## Comparação recalculada independentemente

Quantis 5/50/95 por ordenação e interpolação linear, variância/covariância por somas explícitas e KS por ECDF; concordam com COMPARISON nas tolerâncias registradas no código.

| Parâmetro | Próprio: mediana [5%,95%] | Publicado: mediana [5%,95%] | Diferença de medianas | KS descritivo |
|---|---|---|---|---|
| Mf detector, M☉ | 74,574910 [69,268090;79,882842] | 73,505287 [66,735452;79,902241] | +1,069623 | 0,145400 |
| af | 0,762459 [0,672229;0,830906] | 0,751952 [0,626469;0,834719] | +0,010507 | 0,116048 |

Os intervalos centrais de 90% se sobrepõem. Desvios ddof1 próprios/publicados: Mf=3,268379/4,005265; af=0,049891/0,065150. Razões de diferença por largura em quadratura=0,206908 e 0,128041 são descrições, **não z físicos**. Mesmo evento/dado, sem evidência independente, sem Bayes factor por proximidade de posteriores.

Nenhuma amostra de Mf/af ocupa o 1% extremo de seus priors. Algumas dimensões nuisance seguem amplas: A2220_2 tem 3,242% de amostras no 1% inferior; cosiota, 1,551% no 1% superior. Isso não é evidência de truncamento resolvido ou de modos todos explorados. Bordas de fases são periódicas. Um seed e 512 live points não certificam exaustão multimodal.

## Ressalvas obrigatórias, sem bloqueio neste escopo

- O HDF5 não incorpora manifest/mode em meta_data, apesar dos argumentos do runner. A vinculação foi conferida pela cadeia externa de recibos e pela igualdade exata HDF5–NPZ. Não anunciar pin interno inexistente.
- `CONTROL_PSD_NOT_IDENTICAL_RELEASE` é rótulo operacional: identidade do PSD com a análise pyRing publicada continua UNKNOWN; não é demonstração de inequivalência física. GWOSC versus C00_AR e versão exata da release também permanecem não demonstrados.
- Cronologia pre-live foi corroborada no terminal armazenado e hook pinado; não houve replay independente do sampler. Critérios registrados foram satisfeitos, sem garantia adicional de todos os modos ou de calibração de cobertura.
- O resultado paga a revisão desta calibração não-cega no PSD selecionado. **equivalent_reproduction_paid=false**; não fecha robustez entre PSDs, não mede deformação dtau livre e não confirma física/TGL.

Fontes, E2, autorização, V1, recibos anteriores e revisão do delta permaneceram intactos. Este parecer não lança piloto nem condiciona a ordem completa à obtenção de custo convergido.
