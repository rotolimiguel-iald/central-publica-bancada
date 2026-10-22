# E0.3/E0.7 — metadados e bases documentais

[REAL documental/contagem de metadados; NÃO-CEGO; nenhuma nova inferência física]

Gerado 2026-09-22T19:24:01.438609+00:00. Relógio da Parte B preservado em `SCENARIOS_AND_SCHEDULES.json`; fonte `bis/PART_B_BUDGET_START.json`, SHA256 `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f`. Trabalho leve e sequencial, um processo de cálculo por vez. Instantes inicial/final e duração de cada aquisição constam de SOURCE_LEDGER; o snapshot entre endpoints não é atômico. A duração de download não é exposição observacional.

## Convenção e inventário

Uma convenção: **network_matched_filter_snr preferencial/default publicado pelo GWOSC**, com cortes inclusivos sobre o valor arredondado. Cumulativo oficial confident é a base; acrescenta-se a última versão de discovery ausente desse cumulativo. Deduplicação por commonName. Isso não torna os pipelines de origem idênticos. Não misturamos SNR TGR, SNR de ringdown ou um valor recalculado. [API documentada](https://gwosc.org/api/v1/docs/), [cumulativo](https://gwosc.org/eventapi/jsonfull/GWTC/), [API v2](https://gwosc.org/api/v2/).

| Corrida | únicos no inventário | ≥12 | ≥30 | ≥53 | ≥78 | ≥95 |
|---|---:|---:|---:|---:|---:|---:|
| O1 | 3 | 2 | 0 | 0 | 0 | 0 |
| O2 | 8 | 7 | 1 | 0 | 0 | 0 |
| O3a | 44 | 21 | 0 | 0 | 0 | 0 |
| O3b | 35 | 10 | 0 | 0 | 0 | 0 |
| O4a | 140 | 28 | 2 | 0 | 0 | 0 |
| O4b | 161 | 45 | 5 | 1 | 1 | 0 |
| O4c_discovery_only | 1 | 1 | 1 | 1 | 0 | 0 |
| O4_public_total | 302 | 74 | 8 | 2 | 1 | 0 |
| all_public_selected | 392 | 114 | 9 | 2 | 1 | 0 |

São 391 eventos cumulativos + GW250207_115645 = 392. O inventário inclui CBCs de diferentes classes, **não é amostra BBH pura**: por exemplo GW170817 explica o evento O2 ≥30. Catálogos marginais/terceiros e alertas sem publicação não entram. Os 433 latest da API ampla e 671 versões não são 433/671 eventos elegíveis deste recorte. GWTC4.0 não é somado a GWTC4.1. Todas as listas completas por corrida/corte constam em `GWOSC_INVENTORY.json`; `GWOSC_EVENTS.csv` carrega os campos por evento. Contagem foi cruzada com o mesmo campo da API v2 em 361 versões coincidentes; as demais são escolhas diferentes do endpoint latest, não equivalência presumida.

O4 público tem 302 eventos nominais e 74 ≥12; os 74 têm links de strain anunciados, **nenhum baixado ou validado aqui**. Entre esses 74, 69 têm massa final de fonte e spin efetivo; zero têm **spin final** no resumo default. `chi_eff` não é `chi_f`. Não derivamos massa detector multiplicando medianas, não cortamos M/spin e não certificamos que PE GR resumida seja inspiral-only. Esses campos são anteriores à futura seleção por δτ, mas a certificação mais forte permanece OPEN. Há parâmetros/links em GWOSC; isso não certifica posterior δτ disponível. O4c é apenas uma discovery publicada, não cobertura integral da corrida. [Corridas da API](https://gwosc.org/api/v2/runs).

Eventos ≥30:

- GW170817 — O2, SNR 33.0
- GW230814_230901 — O4a, SNR 43.0
- GW231226_101520 — O4a, SNR 34.7
- GW240920_124024 — O4b, SNR 37.4
- GW240925_005809 — O4b, SNR 31.2
- GW241011_233834 — O4b, SNR 35.8
- GW241127_061008 — O4b, SNR 31.3
- GW250114_082203 — O4b, SNR 78.6
- GW250207_115645 — O4c_discovery_only, SNR 68.91

GW250114 usa 78,6 nesta convenção, não 76,9 de outra análise. GW250207 usa 68,91. Não há evento ≥95 neste universo público consultado. Incertezas de SNR e de classificação não foram propagadas às contagens nominais; eventos próximos do corte podem mudar com nova versão. Isso não é uma declaração sobre eventos não publicados.

`SNR_JOIN_FOR_A.json` entrega chaves/GPS/SNR/Mfonte/z/chi_eff e ausência explícita de spin final para a bancada A. **σ(SNR) não foi ajustada**, aguardando os stds e a conciliação de conjuntos de A. Não foi escolhida leitura científica.

## Comparação com insumos

`HISTORICAL_COMPARISON.json` compara a nova resposta byte-arquivada ao antigo `E_instrumento/gwosc_catalogs_raw.json` por catálogo/evento/SNR. GWTC4.0 (129), 4.1 (140), 5.0 (161) e discovery (8): nenhum acréscimo, remoção ou mudança de SNR. Isto verifica estabilidade entre arquivos; os números antigos não foram copiados como medição nova. Reobtivemos GWTC5 ≥30 = 5, ≥78 = 1, ≥95 = 0. A diferença 45 GWTC5 versus 74 O4 ≥12 é cobertura de corridas, não melhora de sensibilidade. Nenhuma ausência de δτ pública ou contagem de eventos “cegos” foi inferida só destes metadados.

## O5: fatores com escopos distintos

[KNOWN/DERIVED] Releitura da **Tabela 2, página impressa 10**, [Observing Scenarios v55](https://dcc.ligo.org/LIGO-P1200087-v55/public), PDF arquivado com Last-Modified 04/09/2019: BBH30+30 aLIGO O4 1400–1600 Mpc e O5 2500 Mpc. Divisão independente: **1.5625–1.7857143**. São alcances projetados de detector individual com limiar 8 e média de orientação/volume; não um fator universal de SNR da rede ou do ringdown. A tabela BNS dá 330/(160–190); **2.0625 é apenas o teto desse cenário BNS**, não ganho BBH autorizado.

[DECLARADO — artefato local conferido] C5_FISHER_v3 fornece **1.987241229884**, SHA256 `ef7a800369ba07328852b2ffe6a54c13f9b20476775f557113ca31fc50a5a22b`. Fonte ilustrativa de massa detector 68,1 Msol, spin 0,68, banda 20–2048 Hz, passo 0,125 Hz, mesma fonte/projeção e PSD individual de referência. O código define o fator como razão das normas espectrais; nesta frente lemos a implementação e o resultado, **não repetimos C5**. Não é contagem medida, ganho da rede ou calibração do estimador pSEOB. O ganho não pode ser aplicado duas vezes.

[KNOWN atual] [T2500310-v2](https://dcc.ligo.org/T2500310-v2/public) distingue O5a/b/c e associa O5 à troca por massas A+; O5c corresponde à sensibilidade final projetada. Isso impede rotular a curva antiga como sensibilidade garantida desde o começo de O5. Não baixamos novas PSDs nem calculamos novos forecasts.

## Datas e disponibilidade

- **O5:** [plano IGWN, atualização 03/09/2026](https://observing.docs.ligo.org/plan/): cronograma em discussão/refinamento. IR1 previsto para início/meados de novembro de 2026, por seis meses; não confundir IR1 com O5. Data firme de O5 permanece OPEN. Datas antigas do insumo não se tornam promessa atual.
- **ET:** [overview oficial](https://einsteintelescope.eu/about-et/overview/) prevê início dos anos 2040 e escolha do sítio em 2027. [FAQ italiana](https://www.einstein-telescope.it/en/questions-answers/) mantém 2035 no caso mais otimista, condicionado a construção/financiamento. As páginas não exibem data editorial verificada; registramos acesso, não inventamos publicação. Não combinamos cenários em uma data firme.
- **CE:** [apresentação CE-G2600054 de 03/09/2026](https://dcc.cosmicexplorer.org/CE-G2600054/public), slide 5, gráfico atualizado em 10/03/2026: construção 2035–2039, commissioning até 2040, “Run” em 2041. Imagem extraída arquivada e inspecionada. É linha de planejamento, não compromisso entregue/financiado. A referência histórica a meados dos anos 2030 não foi promovida a cronograma atual. O PDF do white paper de 2023 retornou incompleto e não sustenta nenhuma conclusão aqui.
- **GWTC6:** não aparece nos 18 catálogos da [API consultada](https://gwosc.org/api/v2/catalogs); a busca primária não encontrou data oficial. Maio/junho de 2027 permanece analogia do insumo, não anúncio. O GWTC5 registra publicação em [26/05/2026](https://gwosc.org/GWTC-5.0/). Ausência nas fontes consultadas não é prova de inexistência de toda comunicação futura.

## Base 3G e janela

[KNOWN — forecast condicional] [Berti et al., v3, §7.1/Fig.76](https://arxiv.org/html/2505.23895v3) dá ordem de 100 eventos/ano com SNR_RD ≳50 e ordem de 10 com ≳100 na população/rede ilustrada. Não são observações ou precisão garantida de δτ220.

A origem [Bhagwat et al., v2, §II/Tabelas 2–3](https://arxiv.org/html/2304.02283v2) fixa os ajustes de amplitudes/fases e a integração da SNR a aproximadamente **10M depois do pico do strain**. Releitura das tabelas: ET triangular 10km: 28±7/3±1 por ano acima de 50/100; ET dois L de 15km: 70±9/7±3; acrescentando CE: 161±14/13±5 e 246±16/18±7. São resultados de população sintética e Fisher multimodo, não taxas medidas. Preservamos os erros publicados, sem chamar isso de novo IC Poisson. A fonte explicita degenerescência do 220 com massa/spin sem informação adicional.

Não está certificada aqui a equivalência exata do símbolo M da fonte ao tM de massa final usado localmente, nem o endpoint temporal superior. Não se transporta SNR_IMR→SNR_RD, janela no pico→10M, ET isolado→ET+CE ou previsão multimodo→δτ220 por igualdade nominal. O número de eventos úteis depende da população, configuração e critérios.

## Limites e próximos insumos

Esta frente fecha **inventário e base documental** de E0.3/E0.7, não seus forecasts completos. Permanecem a calibração σ(SNR) por A, seleção admissível por M/chi_f, população/exposição e bandas de contagem/tempo. Um intervalo-calendário não é live time; catálogo selecionado não fornece sozinho taxa Poisson completa. Fontes foram lidas nos trechos discriminados em `READING_SCOPE.json`; arquivamento integral não equivale a leitura integral.

## Custódia

| Fonte/cache | HTTP | utilizável | SHA256 |
|---|---:|---|---|
| [berti_2505_23895v3.html](https://arxiv.org/html/2505.23895v3) | 200 | True | `3a855bb4cfc0d2211a607d8ca396be60f52bbd5bfe2ee3312fa4484ff194db7c` |
| [bhagwat_2304_02283v2.html](https://arxiv.org/html/2304.02283v2) | 200 | True | `879ba8193ab52ee7455113b2070de88e71666010c62b6ff212bdaf277d402443` |
| [ce_home.html](https://cosmicexplorer.org/) | 200 | True | `a5833feafda5e287420482d783351b521c2facefdf682ed0658cff23aaebc841` |
| [ce_update_2026.html](https://dcc.cosmicexplorer.org/CE-G2600054/public) | 200 | True | `748335e2d0cbe6b111c1546a97a54daeefb00eef5fb8f6f96bfd6b139b0f8680` |
| [ce_whitepaper_v1.pdf](https://arxiv.org/pdf/2306.13745v1) | 200 | False | `1e90d047b3e4a7576e7f0554b0a374433a76a0c626b35163001500ebebbdc9a6` |
| [ce_whitepaper_v3.html](https://arxiv.org/html/2306.13745v3) | 406 | False | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| [et_italy_questions.html](https://www.einstein-telescope.it/en/questions-answers/) | 200 | True | `aecc7d96e4de7e04af42e56efee85539ed0e28b741de30b7f1d154c4f5d22475` |
| [et_overview.html](https://einsteintelescope.eu/about-et/overview/) | 200 | True | `28b3902a3c0a0ba3fac0961b65637ba504312979b955666423f023ce3d98d3b4` |
| [gw250114_parameters.json](https://gwosc.org/api/v2/event-versions/GW250114_082203-v2/parameters) | 200 | True | `170e300989270202a069965620d751e1c269092225cd212ce423ade125347858` |
| [gwosc_all_event_versions.json](https://gwosc.org/eventapi/jsonfull/allevents/) | 200 | True | `21a9933741ad503d52101faa5e0cb5446652f15e75c33deba26e510f8b7e338c` |
| [gwosc_api_root.json](https://gwosc.org/api/v2/) | 200 | True | `5e607c4944c129b4496e0e3b354d2f78f4b47bdfcc927dd978048a535b78740d` |
| [gwosc_api_v1_docs.html](https://gwosc.org/api/v1/docs/) | 200 | True | `eff3688f4be5d0f6fa7d5d42f3513cf3cd9421ae07e5f344aa6fb996b8661231` |
| [gwosc_catalogs_v2.json](https://gwosc.org/api/v2/catalogs) | 200 | True | `fcd8eef741cb536010539f3e42e6bb5d3a5e0fb7a120289fe95b8a1711f59e0c` |
| [gwosc_cumulative_GWTC.json](https://gwosc.org/eventapi/jsonfull/GWTC/) | 200 | True | `0a38575285bdf3c299fdcfd92ebf7f021cf6e133d492c9a04f50953545015a29` |
| [gwosc_latest_v2_page1.json](https://gwosc.org/api/v2/event-versions?include-default-parameters=true&lastver=true&pagesize=500) | 200 | True | `5915d769771a20b37d2701e6046c8dd7860c6f850256e233e6743c33174f59f1` |
| [gwosc_runs.json](https://gwosc.org/api/v2/runs) | 200 | True | `4011d08ba2945bbfe7f243b7a64fc3219d8910af76969eb266e65573ffe084a6` |
| [gwtc5_release.html](https://gwosc.org/GWTC-5.0/) | 200 | True | `b7f87ef6d14ae1114583a5af713887b1766b35c343b797ae76c15afbbd6e64fb` |
| [igwn_capabilities.html](https://emfollow.docs.ligo.org/userguide/capabilities.html) | 200 | True | `564be764a2bcde695f008698dfe4de7725c4364f05c12fe62215a2936a2a7e40` |
| [igwn_observing_plan.html](https://observing.docs.ligo.org/plan/) | 200 | True | `3d295173300a5e570749ee1ecfce4377e0e7cd3887bc7a781936710008a093f2` |
| [o5_psd_projections_v2.html](https://dcc.ligo.org/T2500310-v2/public) | 200 | True | `abccc1f89a7bcc54bfcccefda3adb2f6dc929090799cc14ae4f316a578337475` |
| [observing_scenarios_v55.pdf](https://dcc.ligo.org/public/0094/P1200087/055/ObservingScenarios.pdf) | 200 | True | `784a26387e429c87f88483df0d368fccbbdb4fe468e094f71e58289b70a4ef56` |
| [observing_scenarios_v55_page.html](https://dcc.ligo.org/LIGO-P1200087-v55/public) | 200 | True | `af173ecf94c84c676f214122921ede722a6f70c6fde690d6a1cce2b08405e84e` |

SOURCE_LEDGER contém URL final, tipo, bytes, datas HTTP e de aquisição e flags. A tentativa HTML v3 do white paper CE retornou 406; a versão v1 PDF retornou HTTP200 com truncamento e falha de parse. Ambas ficam visíveis e inutilizáveis para sustentar afirmações. Nenhum posterior/strain novo, PE ou alteração de produção/canônico/memória.
