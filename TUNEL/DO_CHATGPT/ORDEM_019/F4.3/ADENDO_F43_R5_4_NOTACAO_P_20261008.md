# F4.3 — R5.4 ao lado: somente notação P com uma casa

[REAL — consulta e fonte] O Nós Vivo F4.3 foi consultado antes desta camada. A R5.3 já está AUDITADA pela c1 (a9f3787c): recusava Unicode e zeros à esquerda, mas ainda aceitava ponto e várias casas fracionárias. O V1 pinado 86f98fcc contém POWER_0P2_OF_5_SIGMA dentro de um veredito composto. A regra de interface desta camada segue o despacho da c1: somente P maiúsculo com exatamente uma casa decimal ASCII para o átomo de poder.

[REAL — regra executável] A regex do token atômico usa ((?:0|[1-9][0-9]*)P[0-9]) com re.ASCII e fullmatch. POWER_0P2 e POWER_4P9 passam; 4.9, 4P09, 0P02, 4 sem P, dígitos Unicode e zeros iniciais na parte inteira são recusados. A guarda numérica exige valor < 5 no token NOT_FALSIFIED_UNDERPOWERED. O veredito composto com prefixo completo continua recusado pela interface atômica; não se extrai substring automaticamente.

[REAL — teste] f43_r5_4_selftest.py rodou com Python -B: 30 verificações sintéticas passaram, inclusive aceitação da notação P, recusas do ponto e de duas casas, recibos sintéticos, amostra insuficiente e recusa do modo de produção sem os sete recibos. Nenhum cache novo foi criado. O gate R5.4 pina os resultados e gates anteriores e o veredito novo por hashes lidos dos arquivos.

[OPEN] Poder exato não medido; adaptador full IMR e recibos científicos de produção não existem nesta camada. A campanha de injeções aguarda o levantamento do ADENDO 001. O pedido ao operador permanece SUSPENSO. Nenhum dado observacional foi aberto; a Bancada e o gate não mudaram.