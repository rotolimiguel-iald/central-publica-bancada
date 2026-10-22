# Função lógica de decisão F9 — preparação bf6d6747

Implementa os predicados do contrato candidato V2 pinado em REQUEST.json. Não calcula
estatística, calibração, evidência, potência ou dados observados. A função é pura e não
escreve arquivos. Usa somente math. Nenhuma função candidata foi chamada nesta preparação.

`evaluate_decisions(records, *, scenario_ids, readiness, contract_sha256)` recebe a família
finita de cenários congelada e registros previamente verificados por um chamador confiável.
Um hash escrito na entrada e flags true não autenticam um certificado, ratificam o V1 nem
autorizam dados. Verificar os artefatos e a decisão real do operador é obrigação externa.
O redutor nunca lê certificados ou aceita sua própria saída como prova de calibração.

readiness contém quatro booleanos exatos: data_released, v1_ratified, integrity_valid,
common_support_valid. Se os dois primeiros não estiverem ambos true, records deve ser None
e todos os campos observados ficam None. Integridade/suporte inválidos também requerem None
e produzem falha explícita de contrato. Diagnósticos brutos desses casos pertencem ao
chamador, fora de registros admitidos. Os IDs de cenários precisam ser únicos e não vazios.

records é dict por teste, depois cenário; ausência de teste/cenário ou valor None significa
incompleto. IDs desconhecidos são erro. Os cinco testes são COMPAT_H1, LAW_H1_VS_FREE,
H2_TO_H1, H4_TO_H1 e H5_TO_H1. Não se cria um teste contra H3 contendo H1.
Cada registro presente exige exatamente RECORD_KEYS do módulo. A estatística é finita
quando disponível, e None quando indisponível. G/Q válidos são não negativos. Um registro
calibrado exige estatística válida, escopo não vazio, duas referências externas id+sha256
(numerical_certificate e calibration_reference) e log_p_upper finito <=0. Os demais
status de calibração não podem transportar um p admitido. Uma direção certificada exige
teste rival, estatística válida positiva e direction_reference; sem direção, essa referência
é None. Os nomes de campos acompanham o V2; acrescenta-se a referência de calibração para
localizar o artefato que o chamador deve verificar. Isso não redefine validade estatística.

O limite de probabilidade entra em log natural para evitar p=0 por underflow. Esse valor
deve ser o log de uma cota superior já validada, incluindo erro numérico; converter uma
estimativa pontual ou p Monte Carlo zero em log não a torna válida. A equivalência é
max_s log p = log max_s p e log p_FWER=min(0,log5+max_s log p). A comparação usa
log(0.5 erfc(5/sqrt2)), calculado em runtime. Não converte lnB ou raiz de estatística em sigma.
Se exp(log p) underflowa, a representação em p é None e o log finito fica explícito como
referência da comparação. Z equivalente permanece indisponível; a decisão de limiar não
precisa inventar um Z ou uma inversa normal sem qualificação.

Cada teste só recebe cota robusta quando todos os cenários congelados estão completos.
Não se calcula máximo sobre o subconjunto disponível. Rejeição H1 é OR das duas rejeições
completas; uma rejeição válida sobrevive à falta da outra. Não-rejeição calibrada de H1
requer ambas completas e não rejeitadas. Discriminação combinada de cada rival requer
essa não-rejeição H1, teste rival completo/rejeitado e direção positiva certificada em
todos os cenários. Rejeição de um rival sem esses requisitos permanece em null_rejected,
mas combined_discrimination é false. Uma estatística positiva não certificada não basta.

Saída conserva cada registro/sua disponibilidade, cotas por cenário, incompletudes e
campos separados de compatibilidade/comparações. O status de topo é um resumo; não apaga
rejeições completas, testes ausentes ou sensibilidade entre cenários. A cobertura física
permanece limitada à família finita. relative_evidence, sigma, potência e novidade de uso
permanecem None: são componentes externos distintos, não campos implicitamente satisfeitos.
O predicado de discriminação é condicional às entradas verificadas, não veredito observado
da ORDEM018 ou alegação de novidade de uso por si só.

Preparação: revisão estática independente antes de execução. A validação planejada é uma
tabela lógica finita de registros inventados: completude, faltas, rejeição unilateral H1,
direção, multiplicidade, extremos de log e falhas de schema. Não gera observações simuladas,
covariâncias, cálculos cosmológicos, replicações de calibração ou nova campanha científica.
Não repetir controles ou unidades científicas consumidas. V2, originais e gate preservados.
