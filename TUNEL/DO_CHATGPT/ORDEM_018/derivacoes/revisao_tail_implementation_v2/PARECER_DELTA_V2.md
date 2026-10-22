# Revisão independente estática — implementação do envelope F9, delta V2

[REAL — leitura de bytes e código; DERIVED — análise dos caminhos] Aceite do delta no escopo de preparação de controles sintéticos. Os dois bloqueadores do parecer seq510 foram resolvidos no snapshot V2 selado seq515. Este aceite permite à coordenação decidir a execução específica; não é autorização, execução de controle ou certificação física. O snapshot original permanece bloqueado e preservado. Consulta/registro prévio: seq516.

## TI-01 — domínio completo vinculado

family_payload inclui schema, test_id, null_model_id, lista ordenada inteira e referências da família/modelo/algoritmo. _family_semantic exige o papel FROZEN_DOMAIN_FAMILY; _semantic confere o hash da representação canônica destacada, o papel e a tupla exata das referências. Tanto tail_upper quanto aggregate_bounds chamam essa validação antes do cálculo ou do máximo. A lista encurtada com o hash antigo agora produz outro payload, que não tem o recibo registrado. A implementação preserva o significado do hash científico existente: cabe ao verificador externo confirmar a correspondência entre esse hash e o manifesto inteiro.

Os negativos N08 preparam precisamente o contraexemplo anterior (duas linhas válidas de três e Domain encurtado conservando os pins), a reordenação, a falta do recibo de família apesar dos recibos individuais e a chamada de cauda com domínio alterado. Nenhum deles foi executado nesta revisão. O registro sintético admite apenas as duas famílias explicitamente nomeadas. Permanece correta a fronteira: esse registro não é um verificador físico.

O mapa fixo teste/nulo pode continuar no verificador semântico externo, pois os dois IDs são apresentados em cada payload e no payload da família. Não há lacuna oculta de acesso como havia com a lista omitida. Isto não declara certificado um nulo físico nem transfere ao módulo a aprovação da família F9.

## TI-02 — persistência e saída tardias

finalization.py guarda PENDING_FINAL_DEADLINE_CHECK quando os controles dizem PASS. O arquivo e stdout são explicitamente provisórios. Depois de persistir e reler/calcular o digest, verifica o relógio; depois de emit retornar (o supervisor real usa print(..., flush=True)), verifica novamente. Só retorna 0 quando ambos os pontos estão antes do deadline e os controles passaram. Nesse ramo não há outro hash, I/O ou callback.

Atraso, digest inválido ou erro produz tentativa de FINALIZATION_FAILURE.json e saída não zero; falha nessa tentativa também não converte o resultado em sucesso. A aceitação externa exige saída zero observada, pins/identidades e todos os controles corretos, além da ausência do arquivo de invalidação. Recibo provisório sozinho, interrupção ou ausência de exit code não bastam. Falha no relato pode bloquear/falhar no SO; o contrato só promete recusar sucesso tardio detectado, não hard realtime.

N09 prepara seis doubles: sucesso pontual; atraso na persistência, digest e saída; erro ao persistir e erro na saída. Confere saída esperada, tentativa de invalidação quando cabível e ausência de PASS terminal em qualquer objeto provisório. Os doubles não fazem I/O real nem foram executados aqui. Os limites 30 s totais nominais, 25 s de trabalho/coleta e 23 s cooperativos foram preservados, sem reserva adicional depois do total.

## TI-03 — saída e alcance

Os limites de 2 MiB/64 KiB são agora explicitamente de aceitação após communicate. Não limitam a memória retida durante a captura. O worker fixo e pinado reduz o risco, sem convertê-lo em uma garantia. A alternativa de captura incremental limitada permanece documentada e não foi introduzida silenciosamente.

## Preservação e limite do aceite

Comparação textual e AST mostrou preservação das classes de domínio/recibo/erro, parsing canônico, tipos, limites de inteiros, validação semântica, Budget e certificado da raiz. As mudanças em tail_upper são o vínculo da família e seu transporte ao recibo; o corpo racional e a guarda d=0 permanecem. N=256, Q=10^30, 512/524288 bits, expressões d>0, fallback de recurso separado, fatores de família, estatísticas e regras V2 foram preservados. Os oito grupos T01–T08 continuam sendo os alvos originais; duas famílias de negativos foram acrescidas para os reparos, total de nove grupos negativos.

Ressalva documental não bloqueante: a docstring histórica de Budget diz “hard process budget”. Ler isso à luz do contrato V2, que define prazo cooperativo/nominal e declara OS_deadline_guarantee=false. Uma errata ao lado basta; não exige reabrir a implementação ou alegar garantia dura.

Alternativas consideradas para TI-01: recibo explícito do domínio completo (adotado) ou hash direto de representação canônica de família (não adotado). Para TI-02: recibo provisório mais aceitação por exit externo (adotado) ou invalidação posterior de um recibo final, que seria mais ambígua. Para TI-03: declarar corretamente o limite de aceitação (adotado) ou captura incremental (não necessária para este delta).

[OPEN] Resultado real dos controles, custos, adequação/certificados físicos e aplicação ao composto. Nada disso foi medido nesta revisão. Nenhum centro, catálogo, CDF/SF, simulação, CAMB, fit ou evidência foi aberto/calculado; nenhum candidato foi importado, nenhuma autorização ou CLAIM foi criado. O recibo registra as comparações de pins e o estado de ausência dos marcadores no momento da leitura.
