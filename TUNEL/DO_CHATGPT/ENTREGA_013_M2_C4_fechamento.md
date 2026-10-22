[REAL — NÃO-CEGO; C4 fecha como medida condicional INCONCLUSIVE_SYSTEMATICS, não confirmação]

# ENTREGA 013 M2 — confrontação com os produtos publicados

| Critério F2 | PAGO / NÃO PAGO, escopo e prova |
|---|---|
| Dez leituras × seis conjuntos | PAGO: 60 linhas únicas JSON/CSV, com ln B, bandas, delta, sigma, z, HPD, motivo e estatuto. Guardas recusam ausência de cálculo em vez de completar com zero. |
| Escopo 220 e modos superiores | PAGO documental: todo ln B de catálogo vale no setor 220 condicional com modos superiores de Kerr; 440 fixo na RG em 32/33 eventos (HIGHER_MODE_DEVIATIONS_FIXED_TO_GR). Efeito de liberar440 NÃO PAGO aqui, E4.2. |
| Jackknife e peso máximo | PAGO por leitura/seleção; métricas de ln B e de informação são separadas. Nenhuma evidência repetida é multiplicada. |
| Estimador independente | PAGO: gaussiana2D nos mesmos draws; C4_VALIDATION é controle de quadratura do mesmo KDE, não densidade independente. |
| Delta positivo e literatura | PAGO no adendo com quatro hipóteses não escolhidas; V2 da casa separado e seções primárias relidas. NÃO PAGO identificar a causa física ou corrigir seleção. |
| GWTC3 18/10 | PAGO: duas tabelas lado a lado, primário documental e efeito do ajuste posterior dito. Cronologia do auditor explicitamente DECLARADA. |
| GWTC4 TGR III | PAGO localizar release DCC e inspecionar texto/inventário. NÃO PAGO mesmo ln B: arquivo examinado remete a draws individuais externos e não contém joint df/dtau/spin por evento verificado. Não declarar inexistência de release. |
| RD e QNMRF | PAGO: download/pinos/checksums, inventários. RD inspecionado por cético: Kerr220 fixo, livre221 não é livre220; mesmo ln B não aplicável, null. QNMRF só listado, sem desserializar pickle. |
| Injeção LVK | PAGO extração local e esquema: uma injeção com/sem44, não curva de SNR. Interpretação/calibração é E1.3, não se inventa cobertura a partir de duas análises. |
| Relógio livre | PAGO recomputar dois priors e estender grade além do teto antigo. NÃO PAGO corte sustentado: todos os cruzamentos -ln100 têm ESS<100; data_supported_cut=null. Estabilidade de quadratura não valida cauda da densidade. |
| Emenda e contrato | PAGO: emenda NÃO-CEGA declara ESS100/status técnicos; revisões independentes encerram omissões e guardas, preservando lacunas físicas. |

GW250114, R-B: gaussiana2D ln B=-0.0371658008; KDE conjunto central=0.0290261615, controles de banda até 0.0727946422; bootstrap 2,5/50/97,5%=[-0.03364357129888176, 0.027358577656555028, 0.09183101867182289]. Assim, |ln B| é aproximadamente menor que0,1, com sinal indeterminado entre estimadores. Bootstrap do mesmo estimador não resolve incerteza de modelagem da densidade.

GWTC5_31, R-LIN: ln B=-8.219008727, jackknife [-8.3147235; -7.538585597], maior fração absoluta de ln B=0.079173499. R-B: maior fração absoluta=0.11267213. A maior fração de informação inversa da variância é 0.33746552; portanto “nenhum peso>13%” não pode ser usado genericamente. Sem a cláusula relativa de RG, R-LIN cruzaria a regra de exclusão do setor220 condicional. Com a regra registrada, HPD_RG=0.983038697>0,95: INCONCLUSIVE_SYSTEMATICS.

## Relógio livre e parede de suporte

Prior uniform [INPUT]: ln B livre=0.0259748263, quantil95 de tau_source=0.00029209333s, condicionado aos limites declarados.

Prior log_uniform [INPUT]: ln B livre=0.000644797326, quantil95 de tau_source=3.34417752e-06s, condicionado aos limites declarados.

Banda 0.7: cruzamento bruto q=9.40318084, corte sustentado=None.

Banda 1: cruzamento bruto q=9.65770364, corte sustentado=None.

Banda 1.4: cruzamento bruto q=10.0477625, corte sustentado=None.

Os priors originais e o estendido não foram recortados/renormalizados para esconder cauda. O número do cruzamento é diagnóstico da aproximação, não limite físico. Os próprios quantis dependem do prior e da validade da normalização.

## Tabela completa

| Conjunto | Leitura | ln B | banda min/max | delta | sigma | z diagnóstico | HPD RG | veredito |
|---|---|---:|---|---:|---:|---:|---:|---|
| GWTC5_31 | R-A | 0 | 0/0 | -3.455573e-42 | 0.03357379 | 1.990436 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-B | -1.808278 | -2.094241/-1.702312 | -0.02029174 | 0.03357379 | 2.594828 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-RAIZ-0 | -3.66212 | -3.978688/-3.473463 | -0.037558 | 0.03357379 | 3.109106 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-RAIZ-EP4 | 0 | 0/0 | -3.455573e-42 | 0.03357379 | 1.990436 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-RAIZ-REST | 0 | 0/0 | -1.500397e-82 | 0.03357379 | 1.990436 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-LIN | -8.219009 | -8.504576/-7.973844 | -0.07239103 | 0.03357379 | 4.146613 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-MOD | -3.558157 | -3.880191/-3.353932 | -0.03574677 | 0.03357379 | 3.055159 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-GLOBAL | 0 | 0/0 | 0 | 0.03357379 | 1.990436 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-PROP | 0 | 0/0 | 0 | 0.03357379 | 1.990436 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_31 | R-RAIZ-COHERENT | 0 | 0/0 | 0 | 0.03357379 | 1.990436 | 0.9830387 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-A | 0 | 0/0 | -3.407464e-42 | 0.03305922 | 1.85796 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-B | -2.475591 | -3.198034/-2.062956 | -0.02025686 | 0.03305922 | 2.470705 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-RAIZ-0 | -5.161778 | -6.621903/-4.263161 | -0.03751889 | 0.03305922 | 2.99286 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-RAIZ-EP4 | 0 | 0/0 | -3.407464e-42 | 0.03305922 | 1.85796 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-RAIZ-REST | 0 | 0/0 | -1.472e-82 | 0.03305922 | 1.85796 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-LIN | -11.90115 | -16.34584/-9.839176 | -0.07231844 | 0.03305922 | 4.045503 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-MOD | -4.736211 | -5.448501/-4.088709 | -0.0358762 | 0.03305922 | 2.94317 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-GLOBAL | 0 | 0/0 | 0 | 0.03305922 | 1.85796 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-PROP | 0 | 0/0 | 0 | 0.03305922 | 1.85796 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC5_33 | R-RAIZ-COHERENT | 0 | 0/0 | 0 | 0.03305922 | 1.85796 | 0.9901693 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-A | 0 | 0/0 | -3.533671e-42 | 0.06176942 | 1.935047 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-B | -0.8208338 | -0.8213704/-0.7874452 | -0.02085263 | 0.06176942 | 2.272635 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-RAIZ-0 | -1.568749 | -1.592135/-1.460433 | -0.03818794 | 0.06176942 | 2.553281 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-RAIZ-EP4 | 0 | 0/0 | -3.533671e-42 | 0.06176942 | 1.935047 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-RAIZ-REST | 0 | 0/0 | -1.492289e-82 | 0.06176942 | 1.935047 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-LIN | -3.390675 | -3.427066/-3.2702 | -0.07356114 | 0.06176942 | 3.125946 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-MOD | -1.49156 | -1.49156/-1.446059 | -0.03358663 | 0.06176942 | 2.478789 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-GLOBAL | 0 | 0/0 | 0 | 0.06176942 | 1.935047 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-PROP | 0 | 0/0 | 0 | 0.06176942 | 1.935047 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_10 | R-RAIZ-COHERENT | 0 | 0/0 | 0 | 0.06176942 | 1.935047 | 0.970122 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-A | 0 | 0/0 | -2.972464e-42 | 0.05034647 | 1.055343 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-B | -5.397375 | -10.42566/-3.020915 | -0.02088553 | 0.05034647 | 1.470179 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-RAIZ-0 | -10.26068 | -19.47104/-5.813694 | -0.03821174 | 0.05034647 | 1.814319 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-RAIZ-EP4 | 0 | 0/0 | -2.972464e-42 | 0.05034647 | 1.055343 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-RAIZ-REST | 0 | 0/0 | -1.147878e-82 | 0.05034647 | 1.055343 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-LIN | -18.11097 | -33.57815/-10.86231 | -0.07359439 | 0.05034647 | 2.517102 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-MOD | -7.985924 | -13.95811/-5.12131 | -0.03463974 | 0.05034647 | 1.74337 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-GLOBAL | 0 | 0/0 | 0 | 0.05034647 | 1.055343 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-PROP | 0 | 0/0 | 0 | 0.05034647 | 1.055343 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GWTC3_18 | R-RAIZ-COHERENT | 0 | 0/0 | 0 | 0.05034647 | 1.055343 | 1 | INCONCLUSIVE_SYSTEMATICS |
| GW250114_pSEOB | R-A | 0 | 0/0 | -3.517896e-42 | 0.05779438 | -0.2317936 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-B | 0.02902616 | 0.005077976/0.07279464 | -0.01984529 | 0.05779438 | 0.1115838 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-RAIZ-0 | -0.1253204 | -0.1253204/-0.1078198 | -0.03706305 | 0.05779438 | 0.4094979 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-RAIZ-EP4 | 0 | 0/0 | -3.517896e-42 | 0.05779438 | -0.2317936 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-RAIZ-REST | 0 | 0/0 | -1.529551e-82 | 0.05779438 | -0.2317936 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-LIN | -0.6804231 | -0.6827724/-0.650169 | -0.07147694 | 0.05779438 | 1.004952 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-MOD | -0.1393663 | -0.1393663/-0.1258441 | -0.03683972 | 0.05779438 | 0.4056338 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-GLOBAL | 0 | 0/0 | -0 | 0.05779438 | -0.2317936 | 0.5237862 | NOT_EXCLUDED |
| GW250114_pSEOB | R-PROP | 0 | 0/0 | 0 | 0.05779438 | -0.2317936 | 0.5237862 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |
| GW250114_pSEOB | R-RAIZ-COHERENT | 0 | 0/0 | 0 | 0.05779438 | -0.2317936 | 0.5237862 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |
| GW250114_pyRing | R-A | 0 | 0/0 | 0 | 0.1465873 | -0.9340486 | 0.5418 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |
| GW250114_pyRing | R-B | 0.1411394 | 0.1253472/0.1414049 | -0.01999394 | 0.1465873 | -0.7976525 | 0.5418 | NOT_EXCLUDED |
| GW250114_pyRing | R-RAIZ-0 | 0.245767 | 0.235357/0.2583655 | -0.03723037 | 0.1465873 | -0.6800677 | 0.5418 | NOT_EXCLUDED |
| GW250114_pyRing | R-RAIZ-EP4 | 0 | 0/0 | 0 | 0.1465873 | -0.9340486 | 0.5418 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |
| GW250114_pyRing | R-RAIZ-REST | 0 | 0/0 | 0 | 0.1465873 | -0.9340486 | 0.5418 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |
| GW250114_pyRing | R-LIN | 0.4094334 | 0.3983555/0.4094334 | -0.07178804 | 0.1465873 | -0.4443197 | 0.5418 | NOT_EXCLUDED |
| GW250114_pyRing | R-MOD | 0.120487 | 0.1147628/0.1245137 | -0.03623804 | 0.1465873 | -0.6868372 | 0.5418 | NOT_EXCLUDED |
| GW250114_pyRing | R-GLOBAL | 0 | 0/0 | 0 | 0.1465873 | -0.9340486 | 0.5418 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |
| GW250114_pyRing | R-PROP | 0 | 0/0 | 0 | 0.1465873 | -0.9340486 | 0.5418 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |
| GW250114_pyRing | R-RAIZ-COHERENT | 0 | 0/0 | 0 | 0.1465873 | -0.9340486 | 0.5418 | NUMERICALLY_EQUIVALENT_TO_GR_CONDITIONAL |

Nos zeros analíticos PROP/coerente, trata-se do cenário sub-resolução solicitado, com mapeamento físico OPEN; não de identidade universal. R-GLOBAL tem identidade relacional condicionada. PyRing sigma é proxy gaussiano do intervalo5–95%, não desvio-padrão amostral; catálogos usam diagnóstico inverso da variância, não posterior hierárquico. O CSV companheiro carrega essas ressalvas e hash do JSON.

## Reprodução, falhas e artefatos

Tentativas preservadas: dependência h5py ausente no Python bundled, distro WSL incorreta e normalização de caminhos corrigidas antes da inspeção; console cp1252 falhou ao imprimir HTML, relido com UTF-8; primeira tabela tinha guarda defeituosa e omitia estatutos no CSV, ambas versões preservadas. Relógio bruto inicialmente omitia ESS da cauda; v2 preserva números e reprova o suporte. Não foi rodada PE nova, nem escolhida uma leitura física.

- [F2_ALL_READING_TABLES_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_ALL_READING_TABLES_v2.json>) SHA256 `761eb108231aef3db26a07adcecab08884b299ad5ffb7b45a0360516d63e178f`
- [F2_ALL_READING_TABLES_v2.csv](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_ALL_READING_TABLES_v2.csv>) SHA256 `6df05db50416c3ce5e75aa0071f4999a6766535c3cb7b8fee4990e4eceaf41cb`
- [F2_INDEPENDENT_GAUSSIAN_DENSITY.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json>) SHA256 `93ad1a92fcfc1df2d5cbfa8362120c92182bf677e2c69e8517dc1932aefa4b6b`
- [C4_VALIDATION.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_VALIDATION.json>) SHA256 `817bc63ea74f4131d1a97fa53c274fef59cd60470b8c1560bbecc6be648d3785`
- [F2_FREE_CLOCK_EXTENDED_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_FREE_CLOCK_EXTENDED_v2.json>) SHA256 `6443db084c8fad29db425914eb77a3238648cd069c3bff535f5851f557225d7d`
- [F2_CLOSING_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_CLOSING_REVIEW.md>) SHA256 `81a5e24e8abb6df6aaffa7ab1c14452bfbefb0764d919062bc5f742496b60ede`
- [F2_C6_CLOSING_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_C6_CLOSING_REVIEW.md>) SHA256 `54b03758a92dc8f25220b6db3b64a0c907c095e20b61a110ec4da9141996a097`
- [F2_RD_APPLICABILITY_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_RD_APPLICABILITY_REVIEW.md>) SHA256 `8e48acb49334c3d66b424320d37369b5bffc2ad9f938ef050bd788d51ad4c87c`
- [F2_RD_APPLICABILITY_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_RD_APPLICABILITY_REVIEW.json>) SHA256 `2076f9fc296b30063dbe1272f834c0135e33dcd015fc948d50362a0a84daa5b3`
- [F2_ARCHIVE_DOWNLOADS.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_ARCHIVE_DOWNLOADS.json>) SHA256 `45dd7a291942bb53551d80f790763e6c7fdc60ff1676affaafd2570df0e3174d`
- [F2_CONTROL_EXTRACTION.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_CONTROL_EXTRACTION.json>) SHA256 `88384c3eb4240dc159f0aa3b16d9353b5b63bdb990415e8d1073f9507d366e97`
- [F2_CONTROL_SCHEMAS.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_CONTROL_SCHEMAS.json>) SHA256 `e54e648e06625cc6f96094c7c16d4b89cd40001498d1f4fd5cd9c7f30f417dbf`
- [F2_GWTC4_RELEASE_SEARCH.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/F2_GWTC4_RELEASE_SEARCH.json>) SHA256 `ecef9bbaee6f66923ae43cfd4c2b187500bc6c8673de668703216453faff4c56`
- [GWTC4_DCC_APPLICABILITY_REVIEW.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/f2_review/GWTC4_DCC_APPLICABILITY_REVIEW.md>) SHA256 `e988802f34ab1a569203bc88d1cefe2653378287bb1f52fbb1a81e0e9da81362`
- [REGISTRO_C4.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REGISTRO_C4.json>) SHA256 `2bebc171ddbcef43d7b50b9076dd806b64829a05a769b6e4fe23b73ec121ac59`
- [REGISTRO_C4_EMENDA_013BIS.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/REGISTRO_C4_EMENDA_013BIS.json>) SHA256 `fbe9cb9bbb0d5215bd91dff7be7066c3bbec086729e0c034daf587dc19ffacc7`
- [C4_EMENDA_TECNICA_013BIS.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_EMENDA_TECNICA_013BIS.md>) SHA256 `f733f305177ae105767d424db538f6e34c19def53b7bab622dba6d5b8288d916`
- [C4_ADENDO_DTAU_POSITIVO.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_ADENDO_DTAU_POSITIVO.md>) SHA256 `b0c32db01c47eb1dbf622472a6f4fd9ebbec6fa7ccfaede6015e3ffbed8b4390`
- [C4_ADENDO_GWTC3_18_vs_10.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C4_ADENDO_GWTC3_18_vs_10.md>) SHA256 `7e7f262aa9d63cc549933c35029e365d17f7784a7be64694de3e81dfc6b05ab5`
- [REAPROVEITAMENTO_C4.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_C4.md>) SHA256 `abb9627882351362469e15725a116299e01a100e243f6e735a9a64cb9e17b953`
- [MANIFESTO_DOWNLOADS_013BIS_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/MANIFESTO_DOWNLOADS_013BIS_v2.json>) SHA256 `2fb3898fe9607ecd78a8ba70a3ebdb36f76d068cd6e0b43149be70222f8c777d`
- [summarize_f2_tables_013bis_v2.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/summarize_f2_tables_013bis_v2.py>) SHA256 `74fd157caa118d3943edf5396f12cd7ed200de717f788feaa8b63f2636cf702c`
- [measure_f2_density_clock_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/measure_f2_density_clock_013bis.py>) SHA256 `0b54942ad5311f1f06eb70c4a5e58885d29c897ec6ed0bc3b00c39b851a1d4c2`
- [correct_f2_clock_support_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/correct_f2_clock_support_013bis.py>) SHA256 `0e1fc61d2bd47d9c621341e2e326106ec7f3a2d7ec8c7cf774cfeeeb896b4aa9`

Verificação nesta máquina: `C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\refeito\deliver_m2_013bis.py" --verify`. Para repetir cálculos, usar cópia isolada com os scripts citados e ambiente /opt/lal_env/bin/python -B. Não executar notebooks ou pickles dos releases.


Data UTC 2026-09-22T18:39:20.838920+00:00. Abertura SHA256 `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`. Axiomas: N/A — sem Lean; teoremas novos: 0, nenhum fonte Lean emitido. Nenhum gate, memória ou canônico alterado.
