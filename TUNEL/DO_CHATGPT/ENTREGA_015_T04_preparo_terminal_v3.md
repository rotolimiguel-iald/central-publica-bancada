[REAL — preparação e controles documentais; execução científica pendente]

Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a
Data: 2026-09-26T16:13:20.717748+00:00

Revisão local V2: F1/F3/F4/F5 atendidos no escopo inspecionado. Correção adicional: a mera existência de RESULT não basta. O preparador de orçamento e o supervisor atuais exigem término documentado do T03, SUMMARY ligado ao hash do RESULT, entrega no túnel, MEDIDA quando parcial, contabilidade dentro1h e ausência dos processos próprios identificados. Novos controles:9/9; fonteSHA256 18714b897713254987a694886868842f09cc44c45839a4825863420879bea128; testesSHA256 f2f443622d836c5e93ec1c533342015b190afa95b8c7906839ac789f46e2360f. São recibos sintéticos, não ciência nem lifecycle real.

A sugestão inicial de exigir30/30sucessos foi retirada pelo revisor após conferir §3/T04: a ordem manda registrar MEDIDA e continuar. Falha de cauda não se torna sucesso; permanece NÃO PAGA na entrega final. Não foi acrescentado um gate científico ao piloto.

Supervisor atual: t04/supervise_t04_v3.py, SHA256 536118b13d10d728128c35e6e56162c618f860ee94fe2eee1690d16c839cd555. Orçamento: prepare_budget_v2_checked.py, SHA256 f5e9e348ba1bc0d484480b6b7c84b1fab128172948cc24ed5006194fb9cae99f. Versões anteriores preservadas. Os dois validadores anteriores são idênticos por AST; seus24controles são herdados, não reexecutados nesta versão. O código científico registrado continua intacto.

T03 continua no processo64813; não relançar. Ao terminar: deliver_nulls_campaign.py → prepare_budget_v2_checked.py → conferir a cadeia de alocação → fixture Pool24 → supervise_t04_v3.py qualify → piloto apenas após400pontos aceitos e overflow recusado. A reserva8h/T10 15h ainda NÃO foi publicada; total planejado34,2h inalterado. A fixture só abre após encerramento dos nulos.

Nenhuma API chamada, nenhum gate ou original alterado. O pacote parcial016 continua entregue; relatório final permanece devido após B.
