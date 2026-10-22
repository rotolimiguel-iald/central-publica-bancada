# Revisão estática independente — implementação proposta do envelope F9

[REAL — somente leitura estática e custódia] Request4893d182-7efc-419f-ac8a-ec6803ea8d7a, pacote selado f9_tail_envelope_implementation. Consulta do mapa antes; revisão iniciada em508. Conferidos manifesto, módulo, worker, supervisor, contrato, fontes/pins e descrição dos controles. Foram aprovadas316 comparações de pins:15 arquivos do manifesto,7 fontes,140 arquivos do runtime e154 entradas de execução (há sobreposição). Nenhum candidato foi importado/executado. AST e comparação de JSON não são execução de controles ou avaliação de caudas.

**Conclusão:** o ramo aritmético e as guardas principais estão coerentes com a proposta V2 por revisão estática. Há dois bloqueadores de integração antes de consumir a unidade: TI-01 (lista da família não vinculada ao certificado) e TI-02 (prazo não revisto após persistência terminal). TI-03 qualifica a alegação de limite de saída. O pacote não recebe aceite de execução nesta versão. Nenhum desses achados exige prova física adicional, nova ciência ou repetição de controle consumido.

## TI-01 — cobertura completa pode virar máximo parcial

[REAL — fonte] tail_envelope.py:85–97 valida Domain.scenarios como tuple não vazia, com labels e sem duplicatas, e valida family_sha256 separadamente como hash. Não confere vínculo entre lista e hash. aggregate_bounds, linhas333–365, compara quantidade e cobertura com a tuple recebida. _semantic recebe uma linha por vez, linhas356–359, com referências/hashes; não recebe Domain, lista completa ou um certificado dessa correspondência.

[DERIVED — rastreio de controle, não execução] Considere os três registros válidos a,b,c do registro sintético preparado em bound_records. Mantendo o mesmo hash da família a,b,c, substitua apenas Domain.scenarios por(a,b) e passe os dois registros originais a,b. A quantidade coincide com a tuple encurtada, cada linha mantém os hashes/payloads originalmente admitidos, os dois recibos de BOUND_RECORD continuam válidos, e seen coincide com a tuple. O ramo retorna COMPLETE_CONDITIONAL_BOUND. Assim, o código não garante o enunciado de aggregation do contrato: toda a família CONGELADA exatamente uma vez. Este é um contraexemplo por leitura dos ramos; não foi lançado nem calculado um agregado.

A verificação externa de cada registro não basta para resolver isso: ela vê o cenário individual e o hash, mas não a lista passada ao agregado. A documentação delega semântica física externa, porém o defeito aqui é a ligação documental da cobertura, não a ausência de um solver ou certificado físico.

Duas correções possíveis antes da execução:
1. Exigir recibo DOMAIN/FAMILY para payload canônico contendo lista ordenada completa, test/null, model e algorithm refs e hash da família; validar sua identidade antes de qualquer agregado. O verificador externo poderá conferir esse payload contra o manifesto congelado. Recomendada por não impor nova definição de hash à família científica.
2. Definir e conferir o hash direto de uma representação canônica da lista/identidades completas, se essa representação for compatível com o contrato científico. Não reinterpretar silenciosamente um hash que hoje identifica outro documento.

O controle novo precisa distinguir encurtamento da tuple mantendo hash antigo de simples ausência de uma linha no domínio original. N06 atualmente cobre ausência/duplicação de registros e tuple duplicada, mas não este encurtamento coerente apenas com a tuple alterada.

## TI-02 — PASS pode sobreviver a persistência tardia

[REAL — fonte] CONTROL_CONTRACT.timer_scope inclui startup, trabalho, coleta, validação e tentativa de persistência terminal no intervalo nominal30s. supervisor.py:251–252 confere prazo antes de montar o recibo; linha272 persiste TERMINAL_RECEIPT; linhas280–284 relê/hash/imprime e retorna0 quando o status anterior é PASS. Não há nova leitura do relógio depois dessas operações de I/O. execution_wall_seconds também é capturado antes da persistência.

[DERIVED — ramo possível, não medido] Se os controles/coleta terminarem antes do limite, mas o I/O terminal cruzar o deadline, o arquivo pode conservar PASS e o processo pode sair0 após o prazo incluído no contrato. A ressalva de que o OS não dá garantia de tempo real é correta, mas não justifica aceitar como PASS um excesso que pode ser detectado após o I/O.

Duas correções possíveis:
1. Acrescentar checagem final após os I/Os terminais e sinal inequívoco de falha tardia com saída não zero; o protocolo de aceite deve invalidar qualquer PASS provisório persistido antes dessa checagem. Registrar o tempo que inclui a etapa terminal.
2. Separar explicitamente recibo provisório de trabalho e decisão final do supervisor; o consumidor exige a decisão final e o retorno do processo dentro do contrato. Nenhum recibo provisório pode ser considerado suficiente.

Não pedir contenção impossível em tempo real, não adicionar5s fora do total, não relançar processo. A guarda serve para recusar sucesso tardio e preservar incerteza, não para prometer que um syscall sempre terminará no prazo.

## TI-03 — cap de aceitação não é cap de retenção

[REAL] supervisor.py:212 usa communicate com pipes; os limites2MiB/64KiB são comparados somente na linha219 após a coleta. terminate_and_collect também usa communicate. Portanto os valores limitam ACEITAÇÃO do resultado, não o total de bytes retidos durante a captura. O worker fixo e pinado emite um único JSON pequeno no desenho atual, o que reduz o risco concreto; não há evidência de saída excessiva medida.

Não é defeito da majorante nem motivo para inventar um novo teste científico. Deve-se escolher/documentar uma das alternativas: (a) declarar claramente cap de aceitação pós-coleta e o alcance limitado ao worker fixo; (b) usar captura incremental limitada com falha visível ao exceder o limite e recolhimento dentro do mesmo deadline. Somente(b) sustenta a expressão retenção limitada durante execução. Este parecer não executou produtor de saída ou benchmark.

## Pontos estáticos aceitos e limites efetivos

[REAL/DERIVED] O guard d=0 e lower positivo aparece antes de Budget e de retorno trivial em tail_upper:289–290, com INVALID/null. Para lower não positivo retorna1 após semântica. O resto não usa cauda abstrata0 como p F9; aggregate_bounds recusa inclusive p=0. N04 prevê relógio que falharia se chamado antes dessa guarda, um controle discriminante para a ordem.

Os inteiros são strings de tipo exato, gramática ASCII, sem sinais extras/zeros à esquerda/-0; comprimento e máximo lexical512bits precedem int. Denominador deve ser positivo e a fração irredutível, inclusive zero representado0/1. d exige type int, excluindo bool. Não há conversão silenciosa de float nem tolerância numérica para aceitar igualdade. Os labels/hashes e a quantidade máxima de cenários também são limitados.

A aritmética usa R=(a/(bd))^d*(512b/(a+(512-d)b))^512. O produto é precedido por previsão conservadora de bits e o loop de potência verifica prazo/tamanho. Produtos pequenos fora desse helper (d*b, Q², k²/u²) têm limites derivados dos inputs/Q, não alocações livres gigantes. A previsão por soma de bit_lengths pode recusar um produto que caberia por um bit; isso torna o instrumento mais conservador pelo fallback declarado, sem subestimar p ou ocultar uma tolerância científica. A raiz usa isqrt do piso e distingue quadrado perfeito por igualdade inteira, confere a desigualdade estrita inferior/inclusiva superior e emite R em hexadecimal limitado. Os campos do certificado provêm de inteiros limitados pelo scratch cap; não afirmamos que um leitor externo arbitrário de certificado já foi implementado.

ResourceLimit é tratado separadamente e apenas depois de semântica e guardad0. Falha de tipo/entrada/identidade/verificador resulta null; falha de certificado ou exceção aritmética vira INVALID/null. O recurso retorna1 rotulado, sem prometer monotonicidade entre estados de recurso, e não é sucesso do cálculo apertado. Os testes N03/N04/N05 diferenciam essas rotas. Erros de relógio inválido não são promovidos a cauda. O deadline cooperativo não substitui o supervisor.

A agregação usa frações positivas canônicas, máximo por produto cruzado exato e fator5, sem alpha/sigma/lnB. Os produtos cruzados estão limitados pelos inputs512bits. As duplicatas, registros extras/ausentes, p adulterado não registrado, zero e tuple duplicada são recusados nos ramos correspondentes; TI-01 descreve a lacuna restante.

## Test/null e fronteira do verificador

Não foi encontrado bloqueador separado no mapa fixo test/null: ambos os identificadores entram no payload assinado e podem ser confrontados pelo verificador externo exigido. O módulo faz coerência com o Domain recebido, mas não possui enumeração científica interna dos nulos. A delegação está explicitada em semantic_boundary e physical_certification permanecefalse. O fixture usa H1_TGL como identidade sintética, sem alegar certificação física. Um futuro verificador físico precisa validar esse par contra seu contrato; não é necessário inventá-lo nesta revisão. Diferentemente de TI-01, os dois campos necessários estão presentes na interface que ele recebe.

Um VerificationReceipt prova somente que o callable externo fornecido aceitou o payload/referências; não autentica por si a correção física do verifier. A documentação já declara essa fronteira. Sem verificador físico instalado, o alcance possível desta unidade é qualificação SINTÉTICA do instrumento, jamais abertura da F9 observada.

## Controles e supervisor

T01–T08 preservam as expectativas documentais por comparação de JSON. T03 tem alvo racional par independente; T04 confere a expressão ímpar; T05 compara pontos fixos sem alegar prova numérica global de monotonicidade; T06 exige piso positivo1/Q; T07 verifica orientação e mutação do certificado; T08 trata máximo completo/falhas. N01–N07 exercitam identidade, recibo inadequado, gramática/tamanho, recurso após semântica, pré-produto, família/adulteração e fronteiras da raiz. Esses controles são pertinentes e não meros status vazios. Não executamos nenhum.

O supervisor exige autorizaçãoROOT com request/pins/escopo, reserva CLAIM exclusivo e fsync antes de Popen, usa um único filho e recusa nova invocação com CLAIM/RUN/terminal existente. Falha/incerteza não relança. O worker verifica request, parentPID, nonce, pins de claim/contrato/autorização antes dos controles, instala audit hook com latch e não é descrito como sandboxOS. 23s cooperativo/25s corte/30s total compartilham referência; recolhimento usa tempo restante, sem novo orçamento após30. Não há novo resultado científico ou processo nesta revisão. TI-02 e TI-03 qualificam os pontos restantes desse supervisor.

## Fechamento do snapshot

[REAL] Autorização, CLAIM, RUN e recibo terminal continuam ausentes na conferência desta revisão. Integração V2, fontes e oito expectativas principais coincidem. Pins/AST válidos não equivalem a controles passados. Originais, propostas498/502, revisão503 e memórias compartilhadas não foram alterados.

[OPEN] Solicitar delta selado ao lado para TI-01/TI-02 e redação/implementação coerente de TI-03, então revisar somente essas diferenças antes da decisão da coordenação. Não executar o contraexemplo, os candidatos ou os controles durante esse reparo documental/estático.
