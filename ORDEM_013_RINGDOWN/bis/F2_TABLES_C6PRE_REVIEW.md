[REAL — transporte numérico conferido; OPEN — três correções de guarda/contexto/referencial; sem veredito físico novo]

# Revisão compacta: tabelas F2 e C6-pre

2026-09-22T18:21:18.847028+00:00. Caminhos relativos a `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`.

**As 60 linhas JSON/CSV conferem numericamente com suas fontes. A aprovação sem ressalvas depende de T1/T2/C6-R1 abaixo.** A sonda T1 expõe um defeito de guarda, não uma perda já ocorrida no conjunto atual. C6-R1 afeta três predições sub-resolução e não muda lnB ou veredito. F2-R1 do relógio foi encerrado antes, em `bis/F2_CLOSING_REVIEW.md`; não se reabre esse achado.

## Conferências pagas

Cobertura exata: seis conjuntos × dez leituras = 60 chaves únicas — GWTC5 31/33, GWTC3 10/18, GW250114 pSEOB e pyRing. Conferi seleção e unicidade dos eventos; 24/31 medianas positivas. Recalculei somas de lnB e de cada banda, faixas, jackknife, frações de contribuição, ponderação inversa da variância, sigma, centro e z. Os vereditos e HPD foram transportados das fontes corretas; nenhum lnB foi convertido em sigma. As 60 linhas CSV coincidem com a projeção de colunas do JSON.

R-LIN, GWTC5_31: lnB=−8,21900872685; jackknife [−8,31472350007; −7,53858559715]. Os pesos não devem ser confundidos: máximo de |lnB_i|/sum|lnB_i|=7,91735%, enquanto a maior fração de informação inversa da variância é 33,74655%. O JSON distingue essas duas quantidades corretamente; uma frase genérica “nenhum peso >13%” não valeria para a segunda.

Sigma dos catálogos é diagnóstico gaussiano de desvios-padrão marginais, com centros e predições por medianas; não é o posterior KDE comum nem significância calibrada. Para pyRing, sigma=0,146587305982 é a aproximação gaussiana do intervalo 5–95%, explicitamente rotulada; não foi inventado um desvio-padrão amostral. NOT_EXCLUDED individual é rótulo condicional da fonte, não confirmação física. Os conjuntos e métodos alternativos não foram multiplicados entre si.

No C6, há dez leituras: cinco lnB calculados no arquivo histórico, três aliases numéricos sub-resolução do registro e duas rotas abertas (R-PROP/R-RAIZ-COHERENT) com lnB e delta null. As cinco razões conferem com o início primário/prior de amplitude corretos. A referência GR fixa M_det=64,12336383320982 e chi=0,5955467423117662; as predições são explicitamente avaliadas nessa mediana, não marginalizadas. Sigma/z da rota efetiva são null em todas as linhas, separados do Fisher otimista e da degenerescência local 220. A possível quebra da degenerescência por 440 não foi promovida a calibração.

Timing e diferenças de pyRing são transportes exatos; médias/erros aproximados do ruído conferem com o JSON de origem e têm limitação iid explícita. A variante only220 tem hash conferido e quatro números localizados no texto do auditor, sob DECLARADO_INDEPENDENT_AUDITOR__NOT_RERUN_IN_F5. Isso verifica a transcrição, não a execução do auditor. R-GLOBAL é a igualdade condicional por construção; os outros zeros não são identidades físicas universais.

Conferem hashes diretos de fontes, builders, abertura e supersedes. A dependência de `tgl_ringdown_prediction.py` está vinculada transitivamente pelo REGISTRO_C6 hasheado e coincide com os bytes atuais; não a classifiquei como proveniência ausente. As fontes históricas continuam históricas: hash interno de gerador anterior não é automaticamente o hash da versão atual. O manifesto próprio preserva as âncoras lidas.

## Correções exatas

**T1 — P2, guarda de cobertura:** `summarize_f2_tables_013bis.py:65` usa `analytic=not matches`. Retirei somente R-MOD do pyRing em memória e executei o laço puro isolado por AST sob `-O`: lnB=0,12048702642846765 tornou-se 0,0 com analytic=true e veredito NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL. A contagem final continuaria 60, passando a guarda atual. Nenhum arquivo-fonte foi alterado.

Correção: antes de gerar linhas, exigir unicidade e conjunto exato das leituras calculadas de cada fonte: oito no pSEOB e quatro no pyRing (R-B, R-RAIZ-0, R-LIN, R-MOD). Usar lista explícita por conjunto para complementos analíticos; ausência de leitura calculada deve lançar erro, nunca virar zero. Preservar separadamente a identidade R-GLOBAL, a sub-resolução das leituras planckianas e os cenários R-PROP/coerente com mapeamento aberto. Teste de aceitação: remover R-MOD do pyRing deve recusar a tabela antes da escrita; os dados intactos devem conservar os 60 valores atuais.

**T2 — P2, perda de estatuto no CSV:** a seleção de colunas em `summarize_f2_tables_013bis.py:80` omite analytic/analytic_scope, scope, reason e o status NÃO-CEGO global. Há 16 linhas analíticas no JSON; no CSV sua origem desaparece, em especial nos catálogos onde o veredito é igual ao das linhas calculadas. O z também perde a explicação do centro/hipótese usada; sigma_scope sozinho não transporta todo esse contexto.

Correção em nova versão: incluir ao menos analytic, analytic_scope, scope, nonblind, physical_status e z_scope, preservando o veredito condicional da origem em campo próprio. Identificar o JSON companheiro por caminho/hash no manifesto ou em coluna. Os zeros devem continuar numericamente iguais, mas com tipo explícito “equivalência numérica condicional”, “identidade relacional” ou “resultado calculado”, conforme a origem. Não é necessário refazer posterior ou lnB.

**C6-R1 — P2, redshift silenciosamente zerado:** `record_c6pre_013bis.py:31` chama prediction sem redshift. O default é zero; o REGISTRO_C6 fixa reference_redshift=0,086 e `c6_engine.py:88` o usa. Recalculei por fórmulas independentes e os números atuais reproduzem precisamente z=0. Usando o referencial registrado:

| Leitura | delta atual (z=0) | delta com z=0,086 | aumento do módulo |
|---|---:|---:|---:|
| R-A | -2.98321517084186e-42 | -3.23977167553426e-42 | 8.6% |
| R-RAIZ-EP4 | -2.98321517084186e-42 | -3.23977167553426e-42 | 8.6% |
| R-RAIZ-REST | -1.27305729702172e-82 | -1.50143868387823e-82 | 17.9396% |

Correção: passar `redshift=reg['reference_redshift']` na predição e gravar redshift/profile em primary_reference, preservando a versão anterior. As demais cinco predições finitas permanecem iguais dentro do arredondamento; as duas rotas abertas continuam null. Se z=0 for intencional como cenário alternativo, rotulá-lo explicitamente e publicar a referência registrada ao lado. Não transferir o Fisher de referência para sigma_actual, não recalcular strain e não mudar lnB por essa correção documental.

## Escopo e reprodução

Li os dois builders; não executei/importei produção. O controle `f2_tables_c6_checks.py` usa apenas JSON/CSV e a grade QNM (B-spline independente), sem strain ou posteriores. A sonda `table_missing_row_probe.py` executa somente o laço de montagem isolado, com uma cópia de dados em memória. Nenhuma C5 foi refeita. `on_source_strain_read_this_run=false` é consistente com o código lido; esta revisão não reconstrói o histórico do processo por um booleano. O testemunho textual editável também não é prova externa imutável de cronologia.

Comandos executados: `/opt/lal_env/bin/python -B <raiz>/bis/c1_review/f2_tables_c6_checks.py` em WSL e Python bundled `-B -O <raiz>/bis/c1_review/table_missing_row_probe.py`. Saídas recusam sobrescrita; reprodução em cópia isolada. Insumos novamente conferidos na escrita, intactos. Sem PE, novos posteriores, memória, canônico ou alteração de gate. Axiomas: N/A — sem Lean.

| Arquivo | SHA256 lido |
|---|---|
| `bis/F2_ALL_READING_TABLES.json` | `0797b9d6779cde734bdfdb8a97c6f204c41c23c3941042206679639132aaaf8e` |
| `bis/F2_ALL_READING_TABLES.csv` | `9dd2ac0a3d80fd2536b2b209ac32f7f723f1787908c53efd3c6e095be4904a29` |
| `refeito/summarize_f2_tables_013bis.py` | `2acfa26ac603fb2cb9686889e157703fa7485a8ab545ba3f2ff2dcf697c1138c` |
| `C6_ADENDO_REALIZADO.json` | `0d377951463a2557e4cdcebbb297b57dacb2fc685efeead958f6ce3cccc4aa6c` |
| `refeito/record_c6pre_013bis.py` | `61ec0d023d6beb79f49e0e58d9a2a11475575460847b2709c7d5fce9c7c27e13` |
| `bis/c1_review/f2_tables_c6_checks.py` | `240c6fbbde1d1866eb7df66494b8796dcb72900bb89616a83f0b912c90993237` |
| `bis/c1_review/f2_tables_c6_results.json` | `a431a2ca0021a2ec74ef53d3591ceb2ec94514d927aa48a6724f0427771d9239` |
| `bis/c1_review/table_missing_row_probe.py` | `1bfe704bef4ca949484733d374d7b5f57b0a57be3852467f794b91d7c2ab68f6` |
| `bis/c1_review/table_missing_row_results.json` | `6235369ff5ddcbb6d865c6baaf2e2a3f1340e6c1353e9228a21f18072fc65835` |
| `bis/c1_review/write_tables_c6_review.py` | `b3d58be2483aac90e2ae1c72232a3db25c719ee045f7c387e27dc8068bb4bddf` |
