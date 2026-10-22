[REAL] A-1.b4 — fluxo identidade rejeitado por KMS em estado não tracial.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

[DERIVED — termo Lean compilado] identity_flow_not_kms usa o predicado KMSAt real da v3.1. Para A,B na álgebra da cunha, se ⟨A*Ω,BΩ⟩≠⟨B*Ω,AΩ⟩, o fluxo α(t)=id não satisfaz KMSAt W α 1.

A extensão KMS teria valor constante na borda inferior. Três linhas força constância no interior; continuidade passa ao fecho e à borda superior, impondo a igualdade dos dois valores, contrária à hipótese. O campo kms é portanto consumido analiticamente, separado dos outros campos que também poderiam excluir um fluxo trivial.

[OPEN] A,B com essa desigualdade são dados explícitos do controle; nenhum W físico novo foi construído. O resultado compilou com rc 0 como teorema de rejeição, não como um arquivo negativo rc 1. O sítio matemático da incompatibilidade é precisamente KMSAt.

Reprodução: executar o vetor de argumentos integral nos recibos, com o runner isolado A0/compile_isolated_v2.py e LEAN_PATH incluindo A1/minimal_imports. Cada resultado listado teve rc 0, #print axioms no trio permitido, sem sorry, sem axiom novo e zero arquivo canônico posterior ao marcador. Auditoria: A1/partial_controls_axioms.json, SHA256 c30b83c1ecd79d5f896063a020218f85b685e8682792d4991ce13ccb47ccf497.

Recursos dos passes citados: 38.218000 s parede, 37.968750 s CPU; máquina pesada B: 0 h. São tempos dos passes, não total das tentativas. Falhas anteriores preservadas nos recibos *_01. Coordenação remota: nenhuma chamada; preview local selecionou rota proibida.

- Fonte: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\AnalyticBoundaryControl_v2.lean — SHA256 c48ac659d6e816ca5c04d3b76dca018bf49684376dace9bab486b811b987852a
- Log: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\analytic_boundary_02.log — SHA256 7ef1232fd225222a845ff582a741348e14b6646a7a1a7ad9d0676be016932fff
- Recibo/comando: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\analytic_boundary_02.json — SHA256 7c549a9bdb155f6d3a9089f7e1ca82773e5acbbbf4cc7513428e497096215deb
- Fonte: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\ProbeNonKMS_v3.lean — SHA256 304445b3e0401d696b0b05234410bc90e2cace8e7d4ca0fef31642c39e0f78f1
- Log: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\non_kms_02.log — SHA256 0bc1adc23ea0d1d0846adaff617f4888354725d96724bc3c4ce36200a9cd8bbb
- Recibo/comando: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\non_kms_02.json — SHA256 3e02f96fffe70ce8f55c32b1e37a2f9e5bcc51b24a77e71510ba6d70580568dd

Move / não move: NÃO MOVE H2, H3, import-H3 nem gate. Provas condicionais isoladas, ainda não incorporadas ao kernel; nenhum par físico ou índice do operador foi escolhido.
