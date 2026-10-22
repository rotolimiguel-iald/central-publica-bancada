# F2.3 — diagnóstico tipado da ligação da lei de campo no curvo

[REAL — fontes lidas em 2026-10-08] O Nós Vivo já indexa Fundação, os contratos H2/H3, a entrega 065 de reexame da v338 e as rotas do levantamento QG. A F2.3 está reivindicada por codex-gerente-tgl. O item QG-03 do consolidado classifica a implicação como EXISTE_NA_BANCADA_NAO_LIGADO, sem bloquear a prova. A leitura deste diagnóstico não executa o kernel nem altera o gate.

## O que cada fonte realmente fornece

1. **TGLExt.Fundacao.the_post_lives_in_the_passage** (Fundacao.lean:166): dadas positividade e injetividade da diagonal, unitariedade finita e preservação de ω, conclui a identidade de esperança condicional sob adU. Seu tipo usa matrizes finitas; não contém atlas, métrica, tela nula ou tensor de matéria.
2. **TGLExt.ContratoQGv31.ContratoH3** (ContratoQG_v31.lean:334) e **TGLExt.ImportedSQ.lightH3v32** (TheImportedSecondQuantization.lean:558): o contrato da luz tem o mesmo horizonte H2 e uma lei local de Raychaudhuri/Einstein para a direção fixa nullDir. A conservação do tensor no contrato v3.2 é formulada na representação plana/distribucional. Não é, por igualdade de tipo, a conservação covariante em uma carta curva nem o H3 de todas as direções.
3. **ChatgptAudit.horizon_einstein_reconstruction** (HorizonEinsteinReconstruction.lean:101): com frame e inverso suaves, T regular, simétrico e conservado, e lápis de horizonte em todo ponto e direção nula, fornece Einstein em uma carta pré-conexa. **ChatgptAudit.entropy_density_einstein_coefficient** (linha 127) prova 2π/((4G)⁻¹) = 8πG para G ≠ 0. Ter a primeira pedra no fecho de import não fornece suas hipóteses.
4. **ChatgptAudit.GeneralMetric.metric_only_einstein_equation** (GeneralMetricEinstein.lean:245) e **ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius** (GeneralMetricClausius.lean:83): para métrica lorentziana suave, fonte diferenciável, simétrica e conservada, telas em todo ponto/direção nula, rate ≠ 0, η ≠ 0 e Clausius em cada tela, deduzem ∃Λ na carta. São implicações condicionais já formalizadas.
5. **ChatgptAudit.ChartGluing.AreaChart** (GravitationalChartGluing.lean:124) inclui domínio aberto pré-conexo, GravitationalResponseRecord, MetricScreenFamily, conservação covariante e área/Clausius em toda tela nula. **area_atlas_unique_global_einstein** (linha 159) cola um Λ único sob não-vacuidade e cadeia de sobreposições. O campo area continua entrada explícita.
6. **ChatgptAudit.TopologicalGluing.connected_chart_cover_einstein** (TopologicalAtlasGluing.lean:79) obtém a cadeia de sobreposições de cobertura aberta de espaço pré-conexo, com mapas de carta e casamento tensorial. **ChatgptAudit.SmoothAtlasGluing.connected_smooth_atlas_einstein** (SmoothSelectedAtlasGluing.lean:161) obtém o casamento de transições suaves tipadas e conclui ∃!Λ no atlas, ainda a partir de AreaChart η.

A via de AreaChart consome unified_einstein_from_area → record_einstein_from_area → general_source_einstein_from_area. Esta dependência não invoca diretamente metric_einstein_from_screen_clausius; as duas são implicações formalizadas distintas para a lei local.

## Fecho local dos imports, medido por script

Leitura recursiva das linhas import TGLExt.* / TGL.* nas quatro raízes, sem inferir pelo nome:

| Raiz | Módulos locais | Quatro pedras v338 | HorizonEinsteinReconstruction |
|---|---:|---|---|
| TGLExt.QGSolutionComplete | 755 | fora | dentro |
| TGLExt.TetelestaiOneObject | 764 | fora | dentro |
| TGLExt.TheWholeIsOne | 768 | fora | dentro |
| TGLExt.Fundacao | 14 | fora | fora |

TGLExt.lean importa GeneralMetricClausius na linha 646, GravitationalChartGluing na 681, TopologicalAtlasGluing na 684 e SmoothSelectedAtlasGluing na 690. As quatro pedras entram, portanto, no build guarda-chuva, embora estivessem fora do fecho das raízes acima. HorizonEinsteinReconstruction está no fecho das três declarações principais; não está no fecho próprio de Fundacao.

## Árvore anti-parede e tipo da pedra F2.3

- **A — ContratoH3 da luz:** falta uma transformação tipada do H3 sobre a cunha e nullDir fixo para a lei de área sobre todos os pontos e direções nulas de cada carta. O contrato sozinho não preenche AreaChart.area.
- **B — horizon_einstein_reconstruction:** já está importado pelas declarações principais, mas pede lápis para todas as direções, inverso/frame suaves, T simétrico e conservação covariante. Esses dados não são fabricados por estar no fecho de imports.
- **C — ligante condicional explícito:** a pedra F2.3 nomeia NamedAtlasH3 η e aceita hH3: identidade finita da passagem → NamedAtlasH3 ((4G)⁻¹). Usa the_post_lives_in_the_passage para obter a identidade; hH3 entrega a lei de área sem declará-la derivada do estado; constrói AreaChart a partir de records, screens, conservação e domínios nomeados; aplica connected_smooth_atlas_einstein e reescreve o coeficiente pelo lema de η. A ponte entre tipos é hipótese [INPUT], não teorema físico produzido pela Fundação.
- **D — limite se C falhar:** relatar a incompatibilidade tipada entre matriz finita/única cunha e atlas curvo; não preencher H3 por axioma, sorry ou um habitante inventado.

A conclusão da pedra, se o build e o relatório de axiomas forem verdes, é uma **implicação com H3 nomeado**, ∃!Λ para o atlas fornecido e 2π/η = 8πG. Ela não constrói soluções globais, não deriva H3 do estado e não move o gate. A integração no um.py é atribuição da gerência na v392.

## Pinos SHA-256 lidos dos bytes

| Fonte | Bytes | SHA-256 |
|---|---:|---|
| Fundacao.lean | 9536 | 66332d58fd216317ec5196a64a7aa670c87dcaa5edc59f57a5506bc621d3e073 |
| ContratoQG_v31.lean | 24897 | 2f2c6561a5a5d832b43f11f7bacccf4811eb4392f1832f78cf4a5838a72a4808 |
| TheImportedSecondQuantization.lean | 35835 | ef35478400ef07f20476f2bb937d8fbe2df7b9e506139f54dc5a37401e7d5242 |
| HorizonEinsteinReconstruction.lean | 7283 | 77180ae46c3ed6e897639e598a623193a3e30a334ea31e13449b0882bafed1bf |
| GeneralMetricEinstein.lean | 15000 | 5874bbdd22bf8530c0d407e4916a5578dde326a98c839e029884e7fdfd6fe62c |
| GeneralMetricClausius.lean | 9744 | d635b15c7197800ae26034bbf8d11ddc422a2dbf17633c743b603d3d66143109 |
| GravitationalChartGluing.lean | 10713 | 3b98010f08eed5c81c9a618f0e7e74902132292fd13c7f6ac5d029e708da30e3 |
| TopologicalAtlasGluing.lean | 7548 | 4289a0b55babc8e01a5028ed01def2d8051d3b87e85fbb78f3b3410447a2ca71 |
| SmoothSelectedAtlasGluing.lean | 12360 | c9421c54795a6dfa85cbea780ea88ec0766e15e4a0292b7f089260971c771046 |
| TGLExt.lean | 39081 | f4ce055421c785e952599471b87b4290269fc8afae5158d510d78e0041af9577 |
| consolidado.json | 562347 | 7a8aaaeb8d17a3e6fb3cc9a52676d68711e0744534de56c183934b4fe231f9fe |

O inventário completo com caminhos absolutos, âncoras e fecho de imports está em FONTES_SHA256.json. Os hashes do novo .lean e dos logs de build pertencem ao recibo de entrega da pedra, não a este pin de fontes originais.
