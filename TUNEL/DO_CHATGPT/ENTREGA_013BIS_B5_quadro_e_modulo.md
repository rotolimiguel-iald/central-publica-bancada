[REAL — B5 entregue: quadro condicional e módulo executado/revisado; inferência física NÃO PAGA]

# B5 — quadro de alcance e módulo para incorporação

Abertura `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`; ficha `d5277c4d033062fd0214df008f2631837f5b0e485e7f1cadec040a3dee93abfc`.

| Critério | PAGO / limite |
|---|---|
| E6 | PAGO:180 células,3 rotas×10 leituras×6 grupos, cenários e ponteiros de origem conferidos. |
| E7 extração | PAGO:33 produtos arquivados, cinco campos pareados completos, priors com estatuto, fontes/tar/runtime e hashes. |
| E7 consumidor | PAGO: execução NumPy, guardas, descritores condicionais e matriz de estado. |
| E7 inferência física | NÃO PAGA: seleção, likelihood restrita normalizada, covariância física e adaptador de liberação cega. |
| Incorporação no um.py | Não realizada pela bancada; responsabilidade da gerência após auditoria. |

Foram transportadas 608,681 linhas de amostras em33 produtos de calibração, preservando a ordem comum de delta_f220, delta_tau220, Mf no referencial do detector, spin final e redshift. Sem thinning. Pesos são os iguais armazenados no produto de origem; isso não demonstra independência das amostras nem uniformidade dos priors derivados. O JSON completo está em cache, separado do consumidor; os quantis não substituem amostras.

A fronteira de dependências permanece explícita: extrator com h5py; consumidor com NumPy como única dependência científica. A guarda externa confere o runtime e os bytes registrados. Os dois módulos congelados são entregues nos seus caminhos registrados, sem copiar um executável para outro lugar e alegar que o pin antigo aprova esse novo local.

## Matriz de estado

| Leitura | Variante | Estatuto | Veredito | Gate |
|---|---|---|---|---|
| R-A | 220_only | INPUT | AWAITING_DATA | red |
| R-A | 220_plus_440_INPUT | INPUT | AWAITING_DATA | red |
| R-B | 220_only | INPUT | AWAITING_DATA | red |
| R-B | 220_plus_440_INPUT | INPUT | AWAITING_DATA | red |
| R-MOD | 220_only | CONJECTURE | AWAITING_DATA | red |
| R-MOD | 220_plus_440_INPUT | CONJECTURE | AWAITING_DATA | red |
| R-RAIZ-0 | 220_only | INPUT | AWAITING_DATA | red |
| R-RAIZ-0 | 220_plus_440_INPUT | INPUT | AWAITING_DATA | red |
| R-RAIZ-EP4 | 220_only | INPUT | AWAITING_DATA | red |
| R-RAIZ-EP4 | 220_plus_440_INPUT | INPUT | AWAITING_DATA | red |
| R-RAIZ-REST | 220_only | CONJECTURE | AWAITING_DATA | red |
| R-RAIZ-REST | 220_plus_440_INPUT | CONJECTURE | AWAITING_DATA | red |
| R-RAIZ-COHERENT | 220_only | CONJECTURE | AWAITING_DATA | red |
| R-RAIZ-COHERENT | 220_plus_440_INPUT | CONJECTURE | AWAITING_DATA | red |
| R-LIN | 220_only | CONJECTURE | AWAITING_DATA | red |
| R-LIN | 220_plus_440_INPUT | CONJECTURE | AWAITING_DATA | red |
| R-GLOBAL | 220_only | INPUT | AWAITING_DATA | red |
| R-GLOBAL | 220_plus_440_INPUT | INPUT | AWAITING_DATA | red |
| R-PROP | 220_only | CONJECTURE | AWAITING_DATA | red |
| R-PROP | 220_plus_440_INPUT | CONJECTURE | AWAITING_DATA | red |

Nenhum evento de teste foi acrescentado. A variante220+440 mantém aviso de posterior440/QNM exato não extraído neste contrato. Amostras do catálogo público são calibração NÃO-CEGA; não pagam a ampliação por teste novo. Todos os números físicos de significância continuam null.

## Quadro e interpretação

O4 hoje é cenário derivado de calibração arquivada; O4 cego registra a ausência de novos posteriores. O4c/GWTC-6, O5, ET e CE conservam somente projeções condicionais, com dados futuros AWAITING_DATA. As taxas/IC, ganhos de SNR, âncoras de fonte e limites de sistemática não são combinados em promessa de calendário. O quadro separa informação, contagem e equivalentes; não transporta piso220 para440 ou para variância de frequência. Correção/sigma condicional é identificada como tal; gate vermelho não permite z físico.

## Verificação, execução e limites

Parede observada da execução E7=256.918262s, dentro da reserva; não inclui novamente o tempo dos estudos anteriores. Os comandos exatos de extração/consumo estão em E7_FINAL_EXECUTION_V1.json, e a autorização está pinada antes dos processos. O processo filho direto foi aguardado; não se declara medição independente de ausência de uma árvore de processos.

A revisão E6 conferiu o transporte de valores/ponteiros e os estados. A revisão E7 tem seu escopo no parecer vinculado; essa aprovação de custódia/aritmética não é certificação da teoria pela natureza. As fixtures anteriores incluem recusas de hashes, formatos, cronologia e dados ausentes; as falhas históricas e suas versões permanecem.

Comandos/localizadores: E6 `generate_reach_table.py --execute --authorization ... --authorization-sha256 ...`; E7 `refeito/activate_e7_final_v2_013bis.py --e6-result ... --e6-review ... --e6-review-sha256 ...`. As reticências são abreviação; usar os comandos integrais pinados nos recibos para reprodução em destino isolado. N/A — sem Lean. Nenhum canônico foi executado ou alterado por estes scripts.

## Arquivos e hashes

- [ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.json>) — `f021e0c94df00d23a8f9fff236856c6227019762a98ce2738161f486fda6678b` (17870774 B).
- [ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.md>) — `7b2e772c464033df5edc247613b469e3256ad865851f3876db12c33eef141263` (1671106 B).
- [ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/RESULT_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/RESULT_RECEIPT.json>) — `971142f08e53d3f1bbb4e0c98c9ab4a9dd18a5d85624e5e61539ae55948801bd` (455 B).
- [ORDEM_013_RINGDOWN/bis/e6_actual_review/E6_ACTUAL_RESULT_REVIEW_002.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_actual_review/E6_ACTUAL_RESULT_REVIEW_002.json>) — `44e1817a5eb59ab087661c055e29b584e818079d8ba0403be79a30fd3509e8ed` (5856 B).
- [ORDEM_013_RINGDOWN/bis/e7_execution_review/E7_EXECUTION_INDEPENDENT_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_execution_review/E7_EXECUTION_INDEPENDENT_REVIEW.json>) — `284a3cddb6eaa4b799c4268f76844f1d1f1a6da5704a58946f09271ded397e26` (263584 B).
- [ORDEM_013_RINGDOWN/bis/E7_FULLSAMPLE_RESULT_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E7_FULLSAMPLE_RESULT_V1.json>) — `c2f96864c18f3aea1e3da7b74da17fdd482230e626adbfaf1fb533094fc4e9ea` (384193 B).
- [ORDEM_013_RINGDOWN/cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json>) — `81e65ff3c54260611ae4bf7539624119050f9ee7389d52cbc4ef2756f54771c0` (92737524 B).
- [ORDEM_013_RINGDOWN/bis/E7_FINAL_EXECUTION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E7_FINAL_EXECUTION_V1.json>) — `035212e25370f7d7c780c4a2e1f4a5732785d83b55e60417e8c5ee9ea31f10c9` (3489 B).
- [ORDEM_013_RINGDOWN/bis/E7_FINAL_AUTHORIZATION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E7_FINAL_AUTHORIZATION_V1.json>) — `2848e969bcbbeb6807eaac5fa2137dd9122bce802efecaf09e0d6dc78fab60a7` (982 B).
- [ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py>) — `3e896bd014db610c9b83c6171de2b3b98db506e597b068da20617e189734e330` (7673 B).
- [ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py>) — `99a9ebc8e8a22c3a14f06b8f6dd465400beaf4d95cbef989d7d5652b5b4b8355` (29940 B).
- [ORDEM_013_RINGDOWN/bis/e7_prepare/EXTRACTION_PLAN.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/EXTRACTION_PLAN.json>) — `7dc138a1690d45d381fc36d6e5cb54967b028741158f625ac814fb92159a7335` (47760 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/E7_ORCHESTRATION_V2_CLOSING_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/E7_ORCHESTRATION_V2_CLOSING_REVIEW.json>) — `6dc86ef2e1963eb073dd257ac6384752f38709c4a4cedc9fd25b799abbc4b19b` (1067 B).
- [ORDEM_013_RINGDOWN/bis/e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json>) — `5cb67afe68462376e1e1fc093326cb82dfe1405a00098a9045dad3440070f0dd` (1947 B).
- [ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B5.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B5.md>) — `d5277c4d033062fd0214df008f2631837f5b0e485e7f1cadec040a3dee93abfc` (469 B).
