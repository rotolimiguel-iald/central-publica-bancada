# Revisão independente — prontidão documental E3 cego, V1

**ACCEPTED_DOCUMENTARY_ARITHMETIC_ONLY_WITH_REUSE_ADVISORY. Não é admissão, alocação, autorização de download ou PE.** Artefatos atuais consistentes com as fontes pinadas; há uma correção de comparação de datas a fazer numa nova versão do construtor antes de reutilizá-lo. Originais e pareceres anteriores preservados.

## Resultado e alcance

[REAL — metadados locais e aritmética finita] Conferidos **438/438 checks documentais**, **392/392 comparações escalares** e **9/9 fixtures da sequência de hashes**. Nenhum produtor importado/executado; não houve rede, download, strain, posterior, waveform, bootstrap, refit, RNG, seed real ou PE. As fixtures usam cópia byte a byte do guard em raiz fictícia própria. Não foi chamada a ativação real E2 nem o launcher.

Manifesto, adendo de duas fases e todos os pins de fonte foram conferidos e relidos ao fechar. O guard conferido coincide com `own_code_tree_sha256` do E2. A validação dos metadados não demonstra validade física dos arquivos de strain nem completude universal do censo de publicações.

## As 14 candidatas e os holds

[REAL] Lista exata, sem perda/duplicação: **14 candidatas; 10 sem hold e quatro com hold**. Ordenação por SNR E0 decrescente, desempate por ID, preservada. CSV, linha, valor SNR, versão e descritor de origem conferidos. Não se usou largura de posterior, peso calculado ou custo para selecionar/admitir eventos.

Holds preservados: `GW240930_035959`, `GW240615_160735`, `GW240515_005301`, `GW241102_144729`. As 14 reviews de publicação têm hash/descritor consistentes com o índice R, `review_passed=true` e timestamps conferidos como instantes com timezone após E2. Não equivalem a resolução DQ. `admission=null` e `blindness_certified_here=false` continuam nos 14 itens.

Os cinco alvos de inspeção documental são exatamente os cinco primeiros **sem hold**. Isso explica `unheld:5` no resumo do builder; o total sem hold é 10, já dito na documentação. As nove candidatas restantes continuam na lista; os metadados remotos anteriores dos cinco não certificam as outras nove. “Não encontrado no escopo” não vira ausência universal de publicação.

## Pesos esperados: quatro objetos distintos

[INPUT — modelo empírico de planejamento] Para x=lnρ, μ=a+bx e dispersão residual s de lnσ:

- mediana condicional de σ: exp(μ);
- proxy inverso da mediana ao quadrado: exp(−2μ);
- esperança lognormal de informação: E[1/σ²]=exp(−2μ+2s²);
- inverso do quadrado da média de σ: 1/E[σ]²=exp(−2μ−s²), que não é nenhum dos dois pesos anteriores.

A propagação usa a matriz completa: Var(μ)=[1,x] Cov(a,b) [1,x]ᵀ, incluindo os termos cruzados. Os IC95 publicados transformam μ±t·sqrt(Var μ), **com s fixo**. A integração exp(2 Var μ) adicional é aproximação gaussiana para os coeficientes, separada do IC t; não é posterior preditivo exato nem incerteza de s integrada.

[REAL — auditoria independente] Usei Decimal com 80 dígitos, produto vetor–matriz–vetor e transformações independentes sobre os coeficientes pinados, sem chamar `project` do produtor. Foram conferidos todos os 28 pares candidata×fit, incluindo dispersão residual 5/50/95, intervalos, proxy, esperança e integração gaussiana. Maior erro relativo **1.4085827202712595e-14**, tolerância fixada antes **1.0e-11**. Covariâncias positivas e preservadas; grades bootstrap antigas preservadas sem interpolação nem draws novos.

Exemplo da primeira candidata, mesma fonte de SNR:

| Fit | Proxy 1/mediana² | E[1/σ²] | 1/E[σ]² | E[I]/proxy |
|---|---:|---:|---:|---:|
| GWTC5_31 | 12.17257810 | 13.47072363 | 11.57119978 | 1.10664508 |
| GWTC5_33 | 12.66261862 | 13.99631093 | 12.04421499 | 1.10532516 |

Fit31 e fit33 são populações sobrepostas, não replicações independentes. Três extrapolações no fit31 (ρ<12,9): `GW240515_005301`, `GW241102_144729`, `GW250104_015122`; nenhuma no fit33. As flags estão corretas e os eventos não foram descartados por esse motivo.

[OPEN] Os intervalos não incluem erro de SNR, incerteza de s, seleção, mudança de priors/família, cobertura ou transferência para a PE própria. SNR de rede/preferred pode incluir Virgo; não é automaticamente SNR H1/L1 nem de ringdown. Coeficientes compartilhados correlacionam a incerteza entre candidatas; não somar erros como independentes ou usar os fits31/33 como duas evidências. `information_for_actual_new_PE` permanece null nas 28 linhas. Não há ganho por hora, informação observada ou potência física pagos.

## Datas: correção antes de reutilizar o construtor

**R1 [P2, alcance futuro]** `build_readiness.py` compara `reg['registered_utc'] <= review['reviewed_utc'] <= now.isoformat()` como strings. Essa relação não preserva ordem cronológica entre fusos e não exige timezone. Fixture finita: now=`2026-09-22T10:00:00+00:00`; review=`2026-09-22T09:30:00-02:00` passa lexicalmente, mas é 11:30 UTC, portanto futura. Parsear timestamps aware e comparar instantes normalizados em nova versão, com negativos futuro/naive/malformed.

Isso **não invalida as 14 datas desta entrega**: a revisão independente converteu todas para UTC e confirmou E2 ≤ review ≤ agora. O builder é documental, não guard de admissão; nenhuma autorização foi concedida pelo defeito. Não editar retrospectivamente o artefato ou manifesto publicado.

## Sequência A→B e limites do guard

[REAL — código e fixtures locais] O adendo descreve corretamente que `ORCAMENTO_40H.json` é o **conteúdo completo ativo** no caminho fixado pelo E2, não um arquivo apontador nem descoberta automática de versões. A proposta de dois estágios exige decisão explícita do principal de tratar esse slot como projeção substituível de versões arquivadas imutáveis. Se o slot também for imutável para sempre, a transição não cabe no contrato atual; o adendo não resolve isso por autorização implícita.

Fase A: configuração imutável downloads-only (`jobs={}`, schema E2_PE_JOBS_V2), hash da configuração → orçamento A completo/versionado → mesmos bytes no slot ativo → testemunha A do orçamento → validação antes de baixar. Jobs estáticos permanecem. MD5 do provedor não gera SHA256 local; esse hash só é conhecido/verificado nos recibos após streaming/integridade. Nenhum SHA ausente foi inventado.

Fase B: configuração sucessora imutável com hashes locais, priors/janelas/reviews completos; orçamento/testemunha novos e referência documental à fase anterior. Preservar A/config/testemunha/recibos. Parar downloads e controladores dependentes durante a troca; sem execução na janela entre troca do slot e testemunha nova. Revalidar relógio global e configuração antes de cada lançamento. A ordem e o prazo não reiniciam.

As nove fixtures com a função exata do guard e testemunhas reais **dentro da raiz fictícia** confirmaram: ausência da testemunha A ou B é recusada; downloads-only preserva job estático; versões A permanecem idênticas; B não herda automaticamente downloads A. Campo extra `lineage_INPUT` falso não é rejeitado pelo guard: a cadeia histórica é responsabilidade da revisão, não gate core. O guard verifica a versão corrente e seus pins.

**Limitação de hold confirmada:** receita downloads-only para candidata fictícia held atravessa `load_authorized_configuration`; `authorize_event` também só classifica elegibilidade/censo. Não há job dinâmico ao qual aplicar `validate_job_reviews`. Isso não libera held real: o principal deve restringir fase A às candidatas autorizáveis sem hold/reviews pendentes. Ao existir job, review de publicação ausente foi recusada. Nenhum fetch foi chamado na fixture. Não apresentar essa diferença como nova proteção core.

O helper antigo continua inadequado às duas fases: exige jobs não vazios, fixa downloads vazio, exige piloto aceito e recusa slot já existente. Esta revisão não o corrige nem reutiliza; preserva o parecer anterior. Um sucessor para custo parcial/emenda do piloto e download-only precisa de revisão própria. O fracasso do piloto informado pelo principal não oferece custo convergido: gasto observado é gasto; custo por PE convergida e ganho/hora seguem OPEN. Não é motivo para suspender a ordem nem para preencher custos fictícios.

## Metadados não são dados admitidos

[REAL documental] 18 registros de arquivo conferidos contra as linhas MD5 locais arquivadas e mapeamento de licença pinado. `local_sha256`, `expected_bytes` e `maximum_bytes` dos fragmentos permanecem null; checksums do provedor não foram verificados contra strain. Templates sem schema de jobs, incompletos e explicitamente não executáveis. Não há alocação nem publicação ativa aqui.

As flags no instante do evento e os blocos de 256 s são apenas sondagens documentais. A futura análise exige cobertura integral da janela, finitude, PSD positiva/adequada e corte anterior ao início de análise; passing de timeline não remove hold. Priors, tempos, banda/Nyquist e suporte em toda a região relevante precisam de revisão própria; não transportar 16 s/20 Hz ou medianas GR como configuração certificada. Nenhuma licença foi reavaliada juridicamente nem disponibilidade remota reconfirmada por esta auditoria.

## Pins e custódia desta entrega

- Manifesto produtor: `3974c3d68335e36349ab4da2df21c3630c913738c7408fc0d29f6b1c37750ac3`.
- Expected information: `583167a3e37c9c6731159815942db3bbc6d8d7d79273a9cca67d86d7d802b25c`.
- Builder: `13b7f7308e7f911a1c11a1315be2af9671e9c19c6fc4a1fb4396bed45f4782f0`.
- Adendo da sequência: `10b3c77c19ccab87705c158441e9aee72cb87b5ec3ee4a2e662e9230e190b974`.
- Guard congelado: `3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7`.
- Recibos próprios: `AUDIT_RESULTS_V1.json`, `PHASE_CONTRACT_RESULTS_V1.json`, `SOURCE_SNAPSHOT_V1.json`; cópia byte a byte em `snapshot_001/`.

Originais, E2, parecer de alocação, E4/E7 e E6 intactos. E6 continua sem execução, E7 sem extração. Resultado limitado à revisão documental/aritmética e ao contrato em fixtures fictícias; nenhuma candidata admitida, alocação selecionada ou ordem concluída.
