[REAL — medido e conferido; predições condicionais DERIVED/INPUT/CONJECTURE; NÃO-CEGO]

# Ordem 013 — GWTC-3 e reprodução dos posteriores/injeções

Data UTC: 2026-09-22T02:37:52.756708+00:00. Axiomas: N/A — sem Lean.

## Critérios e resultados

- **PAGO:** 18 HDF5 pSEOB220, 844880 amostras; ZIP conferido contra MD5 oficial e SHA medido. Convenções de prior e amortecimento documentadas com fontes versionadas.
- **PAGO:** 12 sobreposições com o catálogo corrente e seis produtos antigos adicionais. A união nominal tem 39 eventos; nenhuma evidência foi multiplicada entre releases.
- **PAGO:** seleção primária recuperada da Tabela 13 e das duas exclusões explícitas: dez eventos. O controle de todos os 18 arquivos permanece separado.
- **PAGO:** cinco reproduções em pastas novas, desde os posteriores ou ruído bruto; 88563 campos numéricos coincidem, sem diferença nos campos conferidos. Isso conta campos, não medições independentes. Manifestos, arquivos e resultados recalculados foram reconferidos nesta rodada.
- **PAGO:** integridade do registro C6 e de todos os seus insumos. Nenhuma nova leitura do strain nesta entrega.
- **NÃO PAGO:** empacotar o acréscimo GWTC-3 e terminar a auditoria integral C0-C7. Objetivo ativo.

## Seleção publicada do GWTC-3

| leitura | ln B condicional contra RG | veredito |
|---|---:|---|
| R-A | 0 | INCONCLUSIVE_SYSTEMATICS |
| R-B | -0.82083377 | INCONCLUSIVE_SYSTEMATICS |
| R-RAIZ-0 | -1.5687495 | INCONCLUSIVE_SYSTEMATICS |
| R-RAIZ-EP4 | 0 | INCONCLUSIVE_SYSTEMATICS |
| R-RAIZ-REST | 0 | INCONCLUSIVE_SYSTEMATICS |
| R-LIN | -3.3906752 | INCONCLUSIVE_SYSTEMATICS |
| R-MOD | -1.4915603 | INCONCLUSIVE_SYSTEMATICS |
| R-GLOBAL | 0 | INCONCLUSIVE_SYSTEMATICS |

Controle central: 8192 pontos, ESS=2357.48; conteúdo HPD no ponto RG=0.969096. As quatro verificações deixam RG fora de 95%. A regra relativa impede exclusão da TGL com esse diagnóstico. A incerteza Monte Carlo não cobre viés de KDE ou sistemáticas; não convertê-la em sigma.

A soma do controle de 18 tem pouco suporte local em dois produtos e não reproduz a seleção do artigo. As razões são do setor 220 sob priors uniformes condicionais; não representam uma teoria TGL completa. Versões originais do binário/fits não recuperadas.

Seleção conferida em [LVK, VIII.1.2 e Tabela 13](https://arxiv.org/html/2112.06861v3#S8.SS1.SSS2), com leitura do Apêndice A.3. Não se declara leitura integral nem se substituem amostras por números do artigo.

## Reprodução e entrega

Na bancada: `python -B gwtc3_posterior_readout.py`, `python -B read_gwtc3_selection.py`, `python -B combine_gwtc3.py`. Os dois últimos recusam sobrescrita; repetir em pasta nova com os insumos relativos. O backup ALL18_ONLY preserva o gerador do controle anterior.

Os suplementos já testados estão em `cache/C7_POSTERIOR_REPRODUCTION_v1.zip` e `cache/C7_INJECTION_REPRODUCTION_v1.zip`. Cada um contém README em inglês, manifesto, scripts e recibos. No primeiro: `python reproduce.py primary|joint|free_clock|catalog --source-root /path/to/ORDEM_013_RINGDOWN` (escolher um estágio). No segundo: `python reproduce.py full --source-root /path/to/ORDEM_013_RINGDOWN --imr-python /path/to/pycbc/python`.

`--download` é a alternativa pública documentada; essa via de rede não foi novamente exercitada na reprodução local. Samplers LVK não foram rerodados. Tabela adicional: `C7_GWTC3_EVENT_READINGS.csv`, 144 linhas, com indicação da seleção publicada e de sobreposição.

## Memória, limites e aproveitamento

A automação de posteriores/injeções já foi entregue e não deve ser refeita. O adendo C0 corrige o rótulo antigo de três leituras integrais falhadas. STATUS e PROGRESSO recebem backups byte a byte; nenhuma memória canônica ou programa de outra casa foi alterado.

Reutilizados ratio_pair, local_support, weighted_quantile, registro C4 e grade QNM. Acrescentados os posteriores antigos e sua seleção documental. Nenhuma função nova no um.py. Falhas de URL, codificação e patch ficam no STATUS; não viraram dados científicos.

A calibração de duas famílias continua negativa. A partição, relógio e desenrolamento físico não foram escolhidos. O objetivo não exige números favoráveis, nem permite transformar NOT_EXCLUDED em confirmação.

## Custódia medida

| arquivo | SHA-256 |
|---|---|
| `C0_ADENDO_ESCOPO_LITERATURA.md` | `15ff3b8fd2e82484f0fe2e1bdd4d916cb859ad8ffadbef714cac660373341775` |
| `C4_GWTC3_220.json` | `d9dc9b09a8d91dc7f85c5e849091db619b1c22a633b09c97d82bcf434e9c6053` |
| `C4_GWTC3_SCHEMA.json` | `59570d2dd11e6077198dffb39f9d8addcc06945c07f88c822905bebbaa7b7a7e` |
| `C4_GWTC3_COMBINATION.json` | `f88c2aa84f98891734f6dc67229a97777bd201ffca40bc479c86bc2fd4fd1f4e` |
| `C4_GWTC3_PUBLISHED_COMBINATION.json` | `f6dbd853223b803984d352aebe3fd64f786b3f26458988cbb4b37a752f8b1ddd` |
| `C4_GWTC3_SELECTION.json` | `ef18f3b0495d58bffc5f968f86ca860eefd3becb570cd75bfc9f88fa8fee5dd3` |
| `C4_GWTC3_CONVENTIONS.json` | `01205e018dc407304194cc18d04b9d9ad42b3b01cc42659b7c8cbd950770bfe1` |
| `C4_GWTC3_SOURCE_DOCS.json` | `134de77ce9a820455d50de9c73ec5c95e48b04fd816bbb3690502e4468ae0c0a` |
| `C4_GWTC3_PAPER_RECEIPT.json` | `a3087776d05a48cb166f649593686a7e6cb876484abf91ceda724e886fbe29dd` |
| `gwtc3_posterior_readout.py` | `f1e876b1d41a318030613d3c09ef9e882103d2ff2d98dbc12151987694abfe6b` |
| `combine_gwtc3.py` | `b1f13be86cba773e58801a846f0fd3c1aa080f3ece5de0f0886581d22d0c6db1` |
| `combine_gwtc3.py.bak_ALL18_ONLY` | `4181b278a4fa27cd2e6d0d9b9697c08dd7563a90984b54ab570174eae03f77c6` |
| `read_gwtc3_selection.py` | `139cdcbedb2dfe2f14423a060b84b55f2da5acf91aee44562ec3298446dd6d7f` |
| `record_gwtc3_conventions.py` | `16997d65eaf6bde312fff79a9eef706cc3ba227608296165cedada0a34c01816` |
| `C7_GWTC3_EVENT_READINGS.csv` | `d48eca4106876c068e1bf01acb0be7d112e9303436b77f6d8597c54a90b1dddb` |
| `C7_SUPPLEMENTS_VALIDATION.json` | `da1b54fcd7e40dc76b3218f11acfdd6942315beb52077484adcea655e3a92f17` |
| `cache/C7_POSTERIOR_REPRODUCTION_v1.zip` | `194a0a02b703d6ae49723d435a06fd73144bc1b9a138dbcb604c8cc3fbb8eecc` |
| `cache/C7_INJECTION_REPRODUCTION_v1.zip` | `0e94898309569440f3aab339f3c2b1c2e1eac41a96ace904bb5d7d23c05a4492` |
| `cache/MANIFESTO_DOWNLOADS.json` | `f3e8103571721e6712b68ab99013a97d6baba396e8b11535469e9e915febe495` |
