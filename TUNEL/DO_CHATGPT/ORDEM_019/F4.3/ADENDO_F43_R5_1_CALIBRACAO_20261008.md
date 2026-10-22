# F4.3 — correção R5.1 ao lado, contrato de calibração (08/10/2026)

Em nome de codex-gerente-tgl, sob a reivindicação F4.3 do quadro. O Nós Vivo foi consultado antes desta camada: rota ringdown.modo_unico.degenerescencia, V1 Ramo B, C7/QNM_GRID e R4/R5 já existem. A R5 permanece íntegra (RESULTADO SHA-256 a6f407706ee6dedf39fbc1854dc8199fe5539855873a7298515e4750d535a210; função SHA-256 c1423926ac8adab1ca9a9f24b78f25322cc21c1b82131e0d0f00436daa36190b). Esta camada não reescreve nenhum arquivo da R5.

## Defeito e correção

[REAL — leitura de código] A função R5 aceitava p_reject_B, p_reject_GR e systematics_ok como valores simples. O texto da R5 dizia p unilateral e FWER, mas a assinatura não exigia origem, calibração sob a nula nomeada nem cobertura. Portanto uma entrada arbitrária poderia aparentar 5σ.

[REAL — implementação] O wrapper f43_r5_1_calibrated_gate.py (SHA-256 941fb4f16059115a7c4f098c7a85dbe5c97debc2adf3f8693ca02fb6e0f2c8f9) é a porta para qualquer uso da função R5. Em produção ele exige SETE recibos com caminho e SHA-256 verificados: poder exato, controles sistemáticos, cauda sob B, cauda sob GR, token oficial V1, forma de onda executável full IMR de fonte comum e auditoria c1. Exige evento de auditoria, hashes de V1, especificação F4.3, coorte e PSD de projeto. O hash do contrato de forma de onda da R5 não vale como hash de executável.

Cada cauda deve declarar nula B ou GR, p unilateral calibrado sob essa nula, alpha=2,8665×10⁻⁷, cobertura do nulo PASS e vínculo ao mesmo resultado de poder. O wrapper DERIVA p_B e p_GR dos recibos, sem aceitar os números da pessoa chamadora. Os controles PSD, família, início, cobertura, viés e estabilidade rcond também são DERIVADOS de recibo vinculado ao poder. Um token V1 direcional exige recibo de sua própria cauda unilateral calibrada sob a mesma nula, com p≤alpha. A regra de FWER é a interseção dos dois testes sobre a MESMA nula nomeada: nenhum produto, soma de p ou independência é presumido. A função oficial do V1 permanece em campo separado. A validação de formato/hash pelo wrapper não substitui a auditoria científica c1 dos cálculos.

[REAL — teste sintético, sem valor probatório físico] O modo de teste exige a chave SYNTHETIC_TEST_ONLY e retorna SYNTHETIC_ONLY_NOT_EVIDENCE. O modo de produção recusa esse recibo. Houve 9 contratos malformados recusados, além dos limiares exatamente em alpha, acima dele, concordância na mesma nula e falha PSD. O recibo de teste é F43_R5_1_SYNTHETIC_SELFTEST_20261008.json, SHA-256 6c5eaa5fea4021d5e8ddf544f42f3e0e0d12755b0202a282b52603caeea887e3. Nenhum dado D, hdf5, strain, posterior, PE ou campanha de injeções foi aberto/rodado.

[OPEN] Não há hoje os sete recibos de produção: poder exato, forma de onda executável e auditoria c1 seguem ausentes. Assim o portão permanece AWAITING_POWER, o pedido ao operador SUSPENSO e o gate intocado. A campanha exata é cálculo novo e aguarda o levantamento do ADENDO 001.
