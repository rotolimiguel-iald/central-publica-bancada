[REAL — compilações isoladas e auditoria de axiomas; escopo matemático dos enunciados]

# A6 — pontes B7/B4, amostra temporal B1c e controle B6

Quatro módulos compilados com código zero. Os hashes de fonte/log foram recalculados e comparados aos recibos. A auditoria exige cobertura de todos os teoremas da fonte e axiomas contidos em propext, Classical.choice, Quot.sound.

| Ramo | Fonte | Teoremas locais | Declarações auditadas | Avisos |
|---|---|---:|---:|---:|
| B7 | InscriptionBridge.lean | 5 | 6 | 1 |
| B4 | PenaltyThreeLocksBridge_v2.lean | 2 | 2 | 0 |
| B1c | TheEquationOfTruth_T20_v3.lean | 57 | 57 | 18 |
| B6 | OperatorContourBridge_v2.lean | 4 | 6 | 1 |

B7 transporta uma inscrição usando o construtor canônico NameIsTheContent e prova existência de mudança de conteúdo fora do núcleo com forma preservada. B4 identifica exatamente penalty e H3L e seus projetores nos tipos especificados; não instancia automaticamente as matrizes float do runtime.

B1c prova em dimensão finita que conservação de um leitor contínuo em um único tempo positivo implica fatoração pelo projetor, usando iteração e o limite já demonstrado. B6 exibe dinâmica não estática que preserva a leitura e uma dinâmica incompatível que a leitura reprova.

Prefixo V3 preservado byte a byte: 28141 bytes, SHA256 35b91f86b88b8e6c498e8e18305e32ece6802a8e3bf1d6647e6fe75980774ca6.

**MEDIDA de empacotamento:** Lean recusa import depois de comandos. O probe appended_import_probe_01 registrou esse erro. Para conservar o prefixo V3 integral, as pontes foram compiladas em módulos companheiros. A exigência de monólito final permanece pendente de organização da gerência. Os módulos de versões distintas não devem ser importados juntos: contêm declarações homônimas. A integração futura precisa escolher uma única base e regenerar os imports dos companheiros.

Tentativas anteriores preservadas: penalty_bridge_01, single_time_01 e operator_contour_01. Os recibos finais não apontam arquivos novos no kernel. Nenhum um.py ou gate foi alterado.

Manifesto detalhado: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A6_EQUACAO_DA_VERDADE\B_fechamentos\bridges_and_single_time_manifest.json
