[REAL — C6-pre NÃO-CEGA, não calibrada; «ln B ≈ 0 por construção (NON_IDENTIFIABLE_SINGLE_220)» tem escopo local 220, não identidade de evidência 220+440]

# ENTREGA 013 M5 — reclassificação C6-pre

A degenerescência exata local entre parâmetros de um único 220 não obriga ln B finito a ser zero sob todos os priors. Somente R-GLOBAL é igualdade relacional por construção nesta implementação. A rodada histórica fica preservada como diagnóstico pré-portão e não calibrado.

| Critério | Disposição e prova |
|---|---|
| Não reabrir strain em F5 | PAGO: builder lê JSONs, grade QNM e auditoria textual. Não abre HDF5/strain. A reprodução F6 é tarefa separada, não uma reclassificação retroativa da cronologia. |
| Cortes realmente realizados e pyRing | PAGO: timing por detector no JSON; L1 10 e 10,5 t_M têm o mesmo corte. A referência temporal e a diferença para pyRing estão explícitas. |
| Dez leituras, delta, sigma e z | PAGO como tabela abaixo. Sigma/z efetivos NÃO PAGOS: null, não Fisher de fonte fixa disfarçado. R-PROP/coerente mantêm mapeamento OPEN e null no C6. |
| Referencial das predições | PAGO após revisão: z=0,086 registrado, perfil CODATA2018_IAU2015; predições na mediana GR, não marginalizadas. Versão sem z preservada ao lado. ln B permanece intacto. |
| Variante somente220 | PAGO como transcrição DECLARADA do auditor, com hash. NÃO PAGO rerun nessa etapa. Deformar 440 é INPUT da partição, não escolha da bancada. |
| Guarda e cronologia | PAGO documental: runner e fetches fora do hash antigo, recibo editável; registro antes do strain não significa antes do portão. |
| PSD e ruído | PAGO nos metadados existentes: H1 escala baixa (~14 sigma no erro iid aproximado), L1 não estacionário; aproximação não é teste calibrado de detector. Treino/validação GPS e limitações no adendo. |
| 6–8 t_M, atraso e rede | PAGO aviso de possível221. NÃO PAGO atraso fracionário, rede coerente e equivalência posterior pyRing: E3.1 da Parte B. |
| Contrato, ficha e cético | PAGO documental; revisão independente encerrou C6-R1, sem mudar os dez ln B. |

| Leitura | delta na mediana GR | ln B 220+440 histórico | sigma/z da rota |
|---|---:|---:|---|
| R-A | -3.239771675534261e-42 | 0.0 | null / null — não medidos/calibrados |
| R-B | -0.017176580635735218 | -0.002595069772098668 | null / null — não medidos/calibrados |
| R-MOD | -0.05060694871893885 | -0.25129496433683585 | null / null — não medidos/calibrados |
| R-RAIZ-0 | -0.03403741972095873 | -0.043068118398281285 | null / null — não medidos/calibrados |
| R-RAIZ-EP4 | -3.2397716755342616e-42 | 0.0 | null / null — não medidos/calibrados |
| R-RAIZ-REST | -1.5014386838782304e-82 | 0.0 | null / null — não medidos/calibrados |
| R-RAIZ-COHERENT | None | None | null / null — não medidos/calibrados |
| R-LIN | -0.06583401929524743 | -0.09086267688607563 | null / null — não medidos/calibrados |
| R-GLOBAL | -0.0 | 0.0 | null / null — não medidos/calibrados |
| R-PROP | None | None | null / null — não medidos/calibrados |

NÃO PAGO: cobertura/viés com fonte marginalizada, posterior pyRing coerente, efeitos de PSD e mapeamento físico de realização. Nenhuma escolha física, gate ou confirmação decorre de ln B pequeno. Tentativa anterior preservada: C6_ADENDO_REALIZADO.json usou default z=0 em três predições sub-resolução; a v2 corrige somente essas taxas e os metadados de referência.

Reprodução documental: `/opt/lal_env/bin/python -B refeito/record_c6pre_013bis_v2.py` em cópia isolada. Controle independente `bis/c1_review/close_f2_c6_findings.py`, também em cópia isolada. Abaixo, hashes do resultado histórico e de suas correções separadas.

| Artefato | SHA256 lido |
|---|---|
| [C6_RESULTS.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C6_RESULTS.json>) | `781a3741a68875eba0fcef02d596dab7d36103d9e926edc6bec18fb485a055e8` |
| [C6_ADENDO_REALIZADO.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C6_ADENDO_REALIZADO.json>) | `0d377951463a2557e4cdcebbb297b57dacb2fc685efeead958f6ce3cccc4aa6c` |
| [C6_ADENDO_REALIZADO_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C6_ADENDO_REALIZADO_v2.json>) | `df39aee5e80ad97d1ccb74d094dbd19a1c2a391011995e36dcaca1e88394917e` |
| [REGISTRO_C6.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REGISTRO_C6.json>) | `ded00f09b5010d622b67b4ea4e559a216818f578440a0f60772130174ececf14` |
| [bis/C3_C6_TIMING_013BIS.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/C3_C6_TIMING_013BIS.json>) | `56906841f92020988defa1dd774b02add88c34e6d18e9617375aab0323abcc1b` |
| [C6_PYRING_START_COMPARISON.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C6_PYRING_START_COMPARISON.json>) | `59dfef3554288c6117debec7827a8b7cd56c6422ff3710a8a39deb4470645a18` |
| [C5_EMPIRICAL_NOISE.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C5_EMPIRICAL_NOISE.json>) | `a748e279a04f08e0218bcda347ff9d2750068e53b2cefed35a6b36935199e3ef` |
| [PORTAO_DO_PODER_013_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/PORTAO_DO_PODER_013_v2.json>) | `c2972e3cc32286532908875b2a3ddb5d168d0669a6846e3e2c1d16e855c2b133` |
| [refeito/record_c6pre_013bis_v2.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/record_c6pre_013bis_v2.py>) | `29df659d14aafad63642ca510df821ae2f3826a28477cb3998ae8cbe76b85d71` |
| [bis/F2_TABLES_C6PRE_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_TABLES_C6PRE_REVIEW.md>) | `9f02f4fd723aab2450f7e9f78c39e41212c2de7d18eafdb442c459345fd57ea4` |
| [bis/F2_C6_CLOSING_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_C6_CLOSING_REVIEW.md>) | `54b03758a92dc8f25220b6db3b64a0c907c095e20b61a110ec4da9141996a097` |
| [REAPROVEITAMENTO_C6_v2.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_C6_v2.md>) | `af5245e8f990b359c5048418bc9a207e3cdb47fdddd660c1d78f9814fd43eb48` |

Data UTC: 2026-09-22T18:31:19.422508+00:00. Abertura do operador SHA256 `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`. Ordem 013BIS e protocolo do túnel. Axiomas: **N/A — sem Lean**. Teoremas novos: **0**; esta entrega gera Markdown/JSON e não declara fonte Lean. Nenhum canônico, memória ou gate foi alterado.

Verificação de custódia nesta máquina:
```powershell
& C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\refeito\deliver_m3_m5_013bis.py" --verify
```
Os medidores/revisores listados devem ser reproduzidos em cópia isolada, pois recusam sobrescrita. Hashes certificam identidade de bytes, não a interpretação física. Critérios NÃO PAGOS continuam explícitos; a entrega não os promove por nome de marco.
