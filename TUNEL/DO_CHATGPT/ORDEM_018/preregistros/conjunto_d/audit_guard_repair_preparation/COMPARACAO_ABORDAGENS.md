# Preparação do reparo operacional de audit — comparação anterior ao código

[INPUT] Unidade restrita concedida pela coordenação: preparar reparo e controles com doubles; não executar suíte, inicialização, PE, fonte nativa ou sampler. INIT003 e seus IDs permanecem consumidos.

## Alternativas comparadas

A. Trocar PermissionError por SystemExit/BaseException, ou antecipar todos os imports. Uma exceção mais ampla ainda pode ser capturada; pré-carregamento reduz probes mas não certifica ausência de novos atos negados. Tampouco resolve o supervisor que aceita parcial apenas pelo rótulo. Não selecionada.

B. Manter a recusa atual e acrescentar latch monotônico, registro do primeiro ato e journal pré-aberto, checkpoints pré/pós likelihood, após imports e antes de chamadas nativas e na finalização; supervisor valida independentemente recibo, journal e invariantes antes de aceitar parcial ou continuar. Selecionada como delta operacional mínimo, sem alargar allowlist nem alterar ciência/limites. Não é confinamento do SO e não garante interrupção no interior de C; a parada ocorre nos checkpoints alcançados e permanece sujeita à supervisão externa herdada.

C. Isolar cada avaliação em processo separado sob política do SO. Poderia fortalecer isolamento, mas altera arquitetura, custo e administração do sampler; exige outra qualificação. Fora desta unidade.

## Contrato do preparo

A fonte e o driver candidatos são cópias instrumentadas; entrypoints driver/supervisor recusam execução nesta pasta. Não há novo CONTRATO_P3, autorização, CLAIM, job ou comando de PE. A suíte utiliza somente doubles e módulos puros. Nesta fase somente parsing AST, inspeção estática e hashes são permitidos; existência de testes não equivale à sua aprovação.

O resultado original STOPPED_NOT_CONVERGED com bloqueios permanece evidência operacional rejeitada, não falha física. Não há inferência a partir de NPZ nem reconstrução de resultados RB ausentes.

## Limites preservados

A garantia é do hook Python instalado após imports/pins e de checkpoints cooperativos. FDs, syscalls nativas e mutação hostil do processo não ficam confinados pelo latch. Sinais/erros de IO/kill podem impedir recibo do filho; ausência/inconsistência causa rejeição do supervisor. O wait herdado de 3610 s limita a espera inicial por filho; cleanup, IO e wait após kill não viram teto absoluto do SO. Nunca apresentar SystemExit/BaseException como infalível.
