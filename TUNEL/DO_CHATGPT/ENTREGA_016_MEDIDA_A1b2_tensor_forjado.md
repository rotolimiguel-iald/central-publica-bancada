[REAL] A-1.b2 — transformação condicional de um H3 em outro H3 com fonte não simétrica.

Abertura SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a

[DERIVED — termo Lean compilado] Tome n=(1,1,0,0), A23=1, A32=-1, demais componentes zero, f(ψ,x)=T_nn(ψ,x). Então T̃=T+fA e F̃(S)=F(sym S). A função transportH3 recebe C:ContratoH3 W R N T e a hipótese explícita de T simétrico. Produz ContratoH3 W R N T̃, preservando o H2, G, estados admissíveis, carga modular, resposta geométrica e equação local Raychaudhuri–Einstein. A não trivialidade de C implica um estado admissível/ponto com f≠0; ali T̃ não é simétrico.

Isto é mais específico que dizer que «o tipo não menciona simetria»: a transformação habita exatamente as definições da v3.1 e não lê uma hipótese de que T̃ seja um tensor físico. A preparação minimal_imports preservou byte a byte todo o corpo original; alterou somente os imports. A reprodução byte a byte original A-1.a continua NÃO PAGA.

[OPEN] A existência do H3 inicial e de uma fonte simétrica compatível não foi construída. O resultado é uma transformação condicional, não prova de não-vacuidade do contrato. A violação demonstrada é SIMETRIA; não se infere não-localidade de operadores a partir de uma matriz de expectativas. A-1.c deve rejeitar este ataque pela simetria e declarar separadamente o que ainda não tipa sobre localidade.

Reprodução: executar o vetor de argumentos integral nos recibos, com o runner isolado A0/compile_isolated_v2.py e LEAN_PATH incluindo A1/minimal_imports. Cada resultado listado teve rc 0, #print axioms no trio permitido, sem sorry, sem axiom novo e zero arquivo canônico posterior ao marcador. Auditoria: A1/partial_controls_axioms.json, SHA256 c30b83c1ecd79d5f896063a020218f85b685e8682792d4991ce13ccb47ccf497.

Recursos dos passes citados: 33.406000 s parede, 33.093750 s CPU; máquina pesada B: 0 h. São tempos dos passes, não total das tentativas. Falhas anteriores preservadas nos recibos *_01. Coordenação remota: nenhuma chamada; preview local selecionou rota proibida.

- Fonte: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\ProbeForgedStress_v2.lean — SHA256 48c1255f29e2a3ddcb3c3e177fbda3ecb78e99e283bc62eb8876d79711e19c02
- Log: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\forged_stress_02.log — SHA256 ef7f804bfa114e35df55bd20f0d3e097052462cfe778b1aaf20ca61f5dc4333d
- Recibo/comando: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\forged_stress_02.json — SHA256 b89bd7e821f781bfaea83739c5cc78276075fc64671de954106bd66ec24c6f2e
- Fonte: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\ProbeForgedStressContract.lean — SHA256 a5c58d7646681e57b02a2963f4a576a2c19afc11534519bef34f807ef76b1ad7
- Log: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\forged_contract_01.log — SHA256 be6e547585dbb20badf5d9ce9866f8ae5377aeb13fc11a6ac1d87bdac96fec4e
- Recibo/comando: C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A1\probes\forged_contract_01.json — SHA256 0f1c19d7f6065e550783bca46e591b64e5bac60543581bc8d9a0227d1ad8e284

Move / não move: NÃO MOVE H2, H3, import-H3 nem gate. Provas condicionais isoladas, ainda não incorporadas ao kernel; nenhum par físico ou índice do operador foi escolhido.
