# Alternativas registradas antes do código

[REAL documental] Preparação do controlador Q02. Nenhuma execução numérica foi autorizada por este documento.

1. **Ligação direta do motor existente por adaptação isolada (escolhida).** Invocar apenas `background_controls.prediction_worker(configuration, point_id, profile_id)`; conservar física, metadados e verificação de runtime do motor. Criar o callable ausente, sem chamar os mains ou claims históricos. Todas as identidades novas dependem de decisão futura ROOT. Exige supervisor externo concreto e qualificado para runtime, auditoria e prazo de chamada nativa.
2. **Reutilizar o worker c435 como processo por nó (recusada nesta preparação).** O main fixa g.REQUEST, CLAIM/RUN e o primeiro ponto. Reaproveitá-lo consumiria uma unidade histórica ou exigiria alterar seu contrato. Fonte usada somente como referência da cadeia de recibos.
3. **Tabela/interpolação na caixa inteira (alternativa posterior).** Requer cobertura, interpolador e validação próprios; não substituir valores fora da tabela por zero, nem estreitar/renormalizar prior. Não implementada nesta unidade.

Para persistência: (A) conservar DurableStore POSIX já preparado, com FS qualificado e diretórios protegidos; (B) novo backend Windows, que demandaria revisão e qualificação independentes. Escolhida A; disponibilidade do NumPy Windows não torna o store POSIX compatível.

Para orçamento: (A) grade diádica inteira previamente fixada e tetos INPUT explícitos; (B) encerrar por tempo entregando grade parcial. Escolhida A; esgotamento produz falha terminal, sem integral parcial e sem repetir nó incerto.

A implementação desta unidade não pressupõe a assinatura de um supervisor já disponível: define uma porta abstrata obrigatória, sem implementação permissiva, e lista seus requisitos pendentes. A parte executiva que depende dela permanece bloqueada por padrão.
