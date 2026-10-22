[REAL — medição de potência; OPEN — z_free, N90 e significância física]

# ORDEM 015 / T07 — veredito de bancada

Foram cadastrados 33 eventos; a norma de potência na janela 10 tM foi medida em **31**. Em **17** o excesso foi positivo e a raiz define rho; em **14** o excesso foi não positivo e rho fica indefinido pelo estimador F4. Dois eventos ficaram sem medida válida. Isso não é uma tabela de 31 SNRs de detecção.

O controle GW250114 deu rho=19.099703012, contra F4=19.099706003, desvio relativo=1.57e-07. A W foi recalculada pelo mesmo algoritmo, não copiada do npz congelado; a referência temporal dos demais eventos vem da mediana do posterior público. Um detector on-source falhou na máscara DQ e foi retirado da soma com registro. Dois eventos exibem potência extrema descritiva (>10 por grau de liberdade em um detector); permanecem flagados, sem interpretação como sinal.

As quatro buscas de fonte livre terminaram com candidatos finitos, mas todos os otimizadores atingiram maxfev. Por isso z_free e N90 reescrito permanecem **não pagos**. O resultado T07 é parcial e **não fornece sigma**, Bayes, exclusão de GR ou alteração do gate.

Tempo de máquina conservador: 1.195637 h; JSON final `e66afcfade58f2f796cea0f46299de9d58df9bfdb7bbc0294c30650ebcb61455`; busca de fonte `aa14a98646428fb0d6531df2f745097828d895cfab16ff2ae8657bb5cc9b103e`; catálogo inicial `40c71fd5460be093a3829f73ba5cb796a001d63a47e21ee795eb3ddf3be16c4f`; recuperação `d12912bcf092a6e995a5ad370ff921f5fba31df341fe74e91cf1111c4f7fbd26`; qualidade on-source `9bdf585662a7bcb06731d5b081f149897789f922f347336c43ec00ab0cd760fa`. Cada linha do JSON final remete ao resultado por evento e às fontes custodidas.

| Evento | Detectores após QC | Excesso | rho de potência | Observação |
|---|---|---:|---:|---|
| GW170104_101158 | H1,L1 | -24.157 | indef. |  |
| GW190519_153544 | H1,L1,V1 | -42.753 | indef. |  |
| GW190521_074359 | H1,L1 | 49.395 | 7.0282 |  |
| GW190630_185205 | L1 | -28.092 | indef. | rede parcial |
| GW190828_063405 | H1,L1,V1 | -80.451 | indef. |  |
| GW191109_010717 | H1,L1 | 60.465 | 7.7759 | rede parcial |
| GW200129_065458 | H1,V1 | 102.48 | 10.123 | DQ rejeitou L1 |
| GW200208_130117 | H1,L1,V1 | 26.407 | 5.1387 |  |
| GW200224_222234 | H1,L1,V1 | 6.2035e+05 | 787.62 | POTÊNCIA EXTREMA: H1 |
| GW200311_115853 | H1,V1,L1 | -6.6299 | indef. |  |
| GW230628_231200 | — | — | indef. | NO_USABLE_DETECTOR |
| GW230914_111401 | H1,L1 | -16.451 | indef. |  |
| GW230927_153832 | H1,L1 | -115.9 | indef. |  |
| GW231028_153006 | H1,L1 | 122.73 | 11.078 |  |
| GW231102_071736 | H1,L1 | 15.157 | 3.8932 |  |
| GW231226_101520 | H1 | 28.529 | 5.3413 | rede parcial |
| GW240511_031507 | H1,L1,V1 | 6245.7 | 79.03 | POTÊNCIA EXTREMA: H1 |
| GW240514_121713 | H1,L1 | 29.358 | 5.4183 | rede parcial |
| GW240615_113620 | H1,L1,V1 | 37.733 | 6.1427 |  |
| GW240621_195059 | L1,V1 | -43.185 | indef. | rede parcial |
| GW240705_053215 | L1,V1 | 120.26 | 10.966 | rede parcial |
| GW240716_034900 | L1,V1 | -0.66684 | indef. |  |
| GW240919_061559 | H1,L1,V1 | 55.148 | 7.4262 |  |
| GW240920_124024 | H1,L1 | 86.545 | 9.303 |  |
| GW241006_015333 | H1,L1,V1 | -76.08 | indef. |  |
| GW241127_061008 | H1 | -11.065 | indef. | rede parcial |
| GW241129_021832 | H1,L1,V1 | -31.581 | indef. |  |
| GW241225_082815 | H1,L1 | 65.44 | 8.0895 |  |
| GW250114_082203 | H1,L1 | 364.8 | 19.1 |  |
| GW250119_025138 | H1,L1,V1 | 51.501 | 7.1764 |  |
| GW150914_095045 | H1 | -26.503 | indef. | rede parcial |
| GW231206_233901 | H1 | -51.317 | indef. | rede parcial |
| GW190910_112807 | — | — | indef. | NO_REGISTERED_COMPLETE_OFFSOURCE_FRAME |
