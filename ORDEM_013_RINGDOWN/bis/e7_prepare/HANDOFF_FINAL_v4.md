# E7 v4 — correção focada de F3 antes de E2

> [nota operacional do operador — omitida no retrato público]

`checked_authorization` exige timestamps textuais, fuso explícito e **E2 <= autorização <= datetime.now(timezone.utc)**. A guarda continua verificando separadamente o prazo de execução. Mesmo recibo/hash e mesma função compartilhada por extrator e consumidor; um hash não autentica pessoa. Ausência/erro de cronologia nunca autoriza I/O do payload.

**Integrar E2_INCLUDE_FINAL_v4.json e MANIFEST_FINAL_v4.json; E7_ASSEMBLY_V4.json é o descritor ativo.** Atualizar também a proveniência/origem do fragmento para v4. O principal foi expressamente autorizado a recalcular o hash da guarda final na montagem pré-E2, conservando a proveniência do fragmento e a revisão. Não usar o pin observado como aprovação de bytes futuros nem alterar registro já publicado.

Todos os arquivos listados no manifesto v3 foram copiados byte a byte e conferidos em snapshot_v3_before_F3_fix, incluindo manifesto e descritor. A v2 também permanece preservada. Extrator, plano, fórmulas e todas as funções científicas são idênticos à v3; comparação AST registrada em UNIT_TESTS_F3_V4.json. Só a cronologia de checked_authorization mudou, com import datetime de stdlib.

Interface mantida: consumidor com posterior exige `--authorization` e `--authorization-sha256` fornecidos independentemente pelo principal após E2. Schema de cinco campos, preservação de amostras, priors, fonte/tar e validações F1/F2 permanecem. NumPy é a única dependência científica do consumidor; h5py fica no extrator.

Russell fechou F1/F2 em E7_INDEPENDENT_REVIEW_V3.md. **Fechamento independente de F3/v4 ainda PENDING**, a conferir apenas nos bytes novos de autorização, testes e pins. LnB, z físicos, normalização/seleção/covariância física seguem null/OPEN; matemática e estatutos da v3 não mudaram. Isto não registra E2, não libera extração e não encerra ORDEM013BIS.
