[REAL — fechamento somente de T1/T2/C6-R1; sem mudança de gate]

# Fechamento F2/C6

Data UTC: 2026-09-22T18:26:49.936026+00:00. **Os três achados estão encerrados nas versões examinadas.** Não restou bloqueante desses achados. Isto não aprova toda a ordem, o pacote v3 em construção, a calibração ou limites físicos.

| Achado | Controle independente e resultado |
|---|---|
| T1 — cobertura | Bloco real das guardas isolado por AST e compilado com optimize=1. Dados íntegros passam; 9/9 mutações são recusadas: falta de R-MOD, duplicata e leitura extra, cada uma em pyRing, pSEOB e GWTC3. O bloco precede a primeira escrita; nenhuma mutação alcança o ponto posterior às guardas. |
| T2 — CSV/estatutos | 60/60 linhas conservam os números e vereditos condicionais anteriores. CSV transporta analytic, analytic_scope, scope, nonblind, physical_status, z_scope, source_conditional_verdict, result_type e reason. Caminho e SHA256 do JSON companheiro conferem nas 60 linhas. |
| C6-R1 — referencial | A chamada usa redshift do registro (0,086) e perfil CODATA2018_IAU2015, ambos gravados em primary_reference. Os valores corrigidos coincidem com o controle independente anterior. |

As guardas exigem oito leituras calculadas nas fontes pSEOB/GWTC3 e as quatro explícitas do pyRing. A complementação analítica não é mais acionada pela mera ausência de um resultado obrigatório. As categorias separam identidade relacional R-GLOBAL, equivalência sub-resolução e R-PROP/coerente com mapeamento OPEN. `analytic` conserva sua função de origem/complemento, enquanto result_type registra o significado físico-condicional.

No C6, as três predições corrigidas são:

| Leitura | delta no referencial registrado |
|---|---:|
| R-A | -3.23977167553426e-42 |
| R-RAIZ-EP4 | -3.23977167553426e-42 |
| R-RAIZ-REST | -1.50143868387823e-82 |

A mediana de massa/spin permaneceu fixa. As demais predições conferem; as duas rotas abertas continuam null. Os dez lnB, sigma/z efetivos null, Fisher de referência separado, timing, ruído, variante DECLARADO do auditor, limitações e vereditos permanecem iguais. Nenhuma ciência foi refeita: confrontei as correções com os valores esperados já medidos na revisão anterior e conferi a passagem explícita dos parâmetros no código.

Proveniência: supersedes, fontes, builders, abertura e vínculo CSV→JSON conferem. REAPROVEITAMENTO_C6_v2.md cita o hash correto do adendo v2 e mantém NÃO-CEGO/não calibrado e as lacunas. Os insumos antigos monitorados mantêm os hashes da revisão anterior; todos os insumos novos/antigos permaneceram intactos durante esta verificação. Os builders foram encontrados em `ORDEM_013_RINGDOWN/refeito/`; não existe a subpasta `B/` mencionada no pedido.

Controle próprio: `bis/c1_review/close_f2_c6_findings.py`, executado com Python bundled `-B -O`. Evidência: `bis/c1_review/f2_c6_closing_results.json`, SHA256 `669d27bedfe747cda49837feb68041c902d1272b4eb7a058b44eef4fb11a0501`. Script SHA256 `7e1a2ae2a447a75405bdd801062eb5aeb3b50198ce91620b8a1489682c4a4a5e`. Para repetir, usar cópia isolada mantendo os caminhos relativos; saídas recusam sobrescrita. Somente o bloco puro de guardas foi executado, com dados em memória; nenhum builder/escritor de produção foi executado. Sem strain, posteriores, C5, memória ou canônico. Axiomas: N/A — sem Lean.

| Caminho relativo a ORDEM_013_RINGDOWN | SHA256 lido |
|---|---|
| `refeito/summarize_f2_tables_013bis_v2.py` | `74fd157caa118d3943edf5396f12cd7ed200de717f788feaa8b63f2636cf702c` |
| `bis/F2_ALL_READING_TABLES_v2.json` | `761eb108231aef3db26a07adcecab08884b299ad5ffb7b45a0360516d63e178f` |
| `bis/F2_ALL_READING_TABLES_v2.csv` | `6df05db50416c3ce5e75aa0071f4999a6766535c3cb7b8fee4990e4eceaf41cb` |
| `refeito/record_c6pre_013bis_v2.py` | `29df659d14aafad63642ca510df821ae2f3826a28477cb3998ae8cbe76b85d71` |
| `C6_ADENDO_REALIZADO_v2.json` | `df39aee5e80ad97d1ccb74d094dbd19a1c2a391011995e36dcaca1e88394917e` |
| `REAPROVEITAMENTO_C6_v2.md` | `af5245e8f990b359c5048418bc9a207e3cdb47fdddd660c1d78f9814fd43eb48` |
